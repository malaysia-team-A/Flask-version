"""
University Chatbot API - Main Server (Flask Version)
Features:
- AI-powered chatbot with LangChain + Local Ollama LLM
- JWT Authentication (OAuth2 Style)
- Dual Authentication for Sensitive Data (Grades)
- RAG (Retrieval-Augmented Generation)
- Log Anonymization
"""
from flask import Flask, request, jsonify, send_from_directory
from app.engines.data_engine import DataEngine
from app.engines.ai_engine import AIEngine
from app.engines.feedback_engine import FeedbackEngine
import os
import json
import logging
from datetime import datetime, timedelta
import secrets
from functools import wraps
from collections import deque

# Custom Modules
from app.utils import auth_utils
from app.utils import logging_utils
from app.engines.learning_engine import learning_engine

# Setup Logging
logger = logging_utils.get_logger()

# Suppress noisy external libraries
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("faiss").setLevel(logging.WARNING)
logging.getLogger("werkzeug").setLevel(logging.WARNING) # Optional: cleaner flask logs

# Initialize Flask App
app = Flask(__name__, static_folder="static/site", static_url_path="/site")
app.secret_key = auth_utils.SECRET_KEY

# Initialize Engines
DATA_FILE = "data/Chatbot_TestData.xlsx" # Config artifact, logic moved to MongoDB
data_engine = DataEngine(DATA_FILE)

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
ai_engine = AIEngine(MODEL_NAME)
feedback_engine = FeedbackEngine()

# In-memory storage for Dual Auth (High Security) sessions
# Format: { "student_number": datetime_expiry }
high_security_sessions = {}

# In-memory conversation history (prototype for follow-up context)
CONVERSATION_HISTORY_LIMIT = 12  # store last 6 exchanges
conversation_history_store = {}

# Ensure directories exist
if not os.path.exists("knowledge_base"):
    os.makedirs("knowledge_base")

PERSONAL_DATA_FIELDS = [
    "STUDENT_NUMBER",
    "STUDENT_ID",
    "STUDENT_NAME",
    "PREFERRED_NAME",
    "PROGRAMME_CODE",
    "PROGRAMME_NAME",
    "PROGRAMME",
    "PROFILE_STATUS",
    "PROFILE_TYPE",
    "ENROLLMENT_STATUS",
    "SEMESTER",
    "INTAKE",
    "CAMPUS",
    "FACULTY",
    "NATIONALITY",
    "GENDER",
    "EMAIL",
    "PHONE",
    "HOSTEL",
    "ADVISOR",
    "CURRENT_GPA",
    "CURRENT_CGPA",
    "GRADES",
    "LATEST_RESULTS",
    "DOB",
    "DATE_OF_BIRTH"
]

def build_student_context(student_record):
    """Return sanitized JSON context for the LLM."""
    if not isinstance(student_record, dict):
        return "STUDENT DATA:\n{}"
    filtered = {}
    for field in PERSONAL_DATA_FIELDS:
        value = student_record.get(field)
        if value not in (None, ""):
            filtered[field] = value
    if not filtered:
        filtered["notice"] = "No eligible student profile fields available."
    return f"STUDENT DATA:\n{json.dumps(filtered, indent=2, default=str)}"

def log_learning_issue(question, issue_type, response_text=""):
    """Persist unanswered or low-confidence prompts for future review."""
    try:
        learning_engine.log_issue(
            question=question or "",
            issue_type=issue_type,
            confidence=0.0,
            response=response_text
        )
    except Exception as e:
        logger.warning(f"Learning log failed: {e}")

def resolve_conversation_session(current_user, payload):
    """Return session key + conversation_id based on auth state."""
    if current_user and current_user.get("student_number"):
        student_number = current_user.get("student_number")
        return f"user:{student_number}", student_number, False

    payload_id = (payload or {}).get("conversation_id") if isinstance(payload, dict) else None
    if payload_id:
        return f"guest:{payload_id}", payload_id, False

    new_id = secrets.token_hex(8)
    return f"guest:{new_id}", new_id, True


def get_conversation_history(session_key):
    history = conversation_history_store.get(session_key)
    if not history:
        return []
    return list(history)


def append_conversation_message(session_key, role, content):
    if not session_key or not content:
        return
    history = conversation_history_store.setdefault(
        session_key,
        deque(maxlen=CONVERSATION_HISTORY_LIMIT)
    )
    history.append({"role": role, "content": content})

def is_grade_query(message):
    return any(k in message.lower() for k in ['grade', 'result', 'exam', 'score', 'gpa'])

def check_personal_intent(message, search_term):
    # Heuristic: Check for explicit "my" + data keywords OR if AI identified a personal search term
    if "my " in message.lower():
        return True
    return False


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Check Authorization header (Bearer token)
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            payload = auth_utils.decode_access_token(token)
            if payload is None:
                return jsonify({'message': 'Token is invalid or expired!'}), 401
            current_user = payload
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401
            
        return f(current_user, *args, **kwargs)
    
    return decorated

@app.route('/')
def home():
    return jsonify({"status": "University Chatbot API is running", "docs": "/site/code_hompage.html"})

@app.route('/site/<path:filename>')
def serve_static(filename):
    return send_from_directory('static/site', filename)

# ===========================================
# AUTH ENDPOINTS
# ===========================================

@app.route('/api/login', methods=['POST'])
def login():
    """Login to get JWT Token"""
    try:
        data = request.get_json()
        student_number = data.get('student_number')
        name = data.get('name')
        
        # Verify user exists (Basic check for Name+ID match)
        is_valid, student_data, msg = data_engine.verify_student(student_number, name)
        
        if is_valid:
            # Generate JWT
            token = auth_utils.create_access_token({
                "student_number": student_number,
                "name": name,
                "role": "student"
            })
            
            logging_utils.log_audit("LOGIN", f"{name} ({student_number})", "Login successful")
            return jsonify({"success": True, "token": token, "user": {"name": name, "student_number": student_number}})
        else:
            logging_utils.log_audit("LOGIN_FAILED", f"{name} ({student_number})", f"Reason: {msg}")
            return jsonify({"success": False, "message": msg}), 401
            
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({"success": False, "message": "Server error"}), 500

@app.route('/api/verify_password', methods=['POST'])
@token_required
def verify_high_security(current_user):
    """Verify password for Dual Auth"""
    try:
        data = request.get_json()
        password = data.get('password')
        student_number = current_user.get('student_number')
        
        # Get actual student record securely
        student = data_engine.get_student_info(student_number)
        
        if not student:
            return jsonify({"success": False, "message": "Student record not found"}), 404
            
        # Robust Password Retrieval (Case-insensitive)
        stored_password_hash = student.get("PASSWORD") or student.get("Password") or student.get("password") or ""

        # Verify
        if auth_utils.verify_password(password, stored_password_hash):
            # Grant high security access for 10 minutes
            high_security_sessions[student_number] = datetime.now() + timedelta(minutes=10)
            logging_utils.log_audit("HIGH_SECURITY_AUTH", student_number, "Password verification successful")
            return jsonify({"success": True, "message": "Identity verified. You can now access grades."})
        else:
            logging_utils.log_audit("HIGH_SECURITY_FAIL", student_number, "Password verification failed")
            return jsonify({"success": False, "message": "Incorrect password"}), 401
            
    except Exception as e:
        logger.error(f"Auth error: {e}")
        return jsonify({"success": False, "message": "Server error"}), 500

# ===========================================
# CHAT ENDPOINTS
# ===========================================

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint supporting JWT and Dual Auth"""
    try:
        data = request.get_json() or {}
        user_message = data.get("message")
        
        # Get Token if available
        current_user = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1] if "Bearer " in request.headers['Authorization'] else None
            if token:
                current_user = auth_utils.decode_access_token(token)
        
        session_key, conversation_id, _ = resolve_conversation_session(current_user, data)
        conversation_history = get_conversation_history(session_key)

        if not user_message:
            return jsonify({"error": "Message is required", "conversation_id": conversation_id}), 400

        append_conversation_message(session_key, "user", user_message)
        
        # --- OPTIMIZED SINGLE-CALL FLOW ---
        
        # 1. Initial Attempt (No Data Context)
        # This checks if the AI can answer directly OR if it needs data.
        initial_result = ai_engine.process_message(user_message, conversation_history=list(conversation_history))
        
        response_payload = {}
        response_text = ""
        context_used = ""

        if initial_result.get("needs_context"):
            # 2. Context Required -> Fetch Data & Re-Prompt
            try:
                print(f"DEBUG: AI requested context for '{user_message}'")
                search_term = initial_result.get("search_term")
                
                # A. Check for Personal Data / Grades first (Security)
                is_personal = check_personal_intent(user_message, search_term)
                if is_personal:
                     if not current_user:
                        return jsonify({
                            "response": "🔒 Please login to access personal information.",
                            "type": "login_hint",
                            "conversation_id": conversation_id
                        })
                     # Dual Auth Check for Grades
                     if is_grade_query(user_message):
                        expiry = high_security_sessions.get(current_user.get("student_number"))
                        if not expiry or datetime.now() > expiry:
                            return jsonify({
                                "response": "🔒 Security Check: Please enter your password to view examination results.",
                                "type": "password_prompt",
                                "conversation_id": conversation_id
                            })
                            
                     student_data = data_engine.get_student_info(current_user.get("student_number"))
                     if student_data:
                         context_used = build_student_context(student_data)
                     else:
                         context_used = "Student record not found."

                # B. If not personal, check DB Stats or RAG
                if not context_used:
                    # Simple heuristic: if query mentions "how many" or "stats", check stats first
                    if "count" in user_message.lower() or "how many" in user_message.lower():
                        context_used = data_engine.get_summary_stats()
                    
                    # If still no context, try RAG
                    if not context_used or "error" in str(context_used).lower():
                        from app.engines.rag_engine import rag_engine
                        rag_docs = rag_engine.search(user_message)
                        if rag_docs:
                             context_used = "\n".join([d.page_content for d in rag_docs])

                # 3. Final call with context
                final_result = ai_engine.process_message(
                    user_message, 
                    data_context=context_used or "No specific data found.", 
                    conversation_history=list(conversation_history)
                )
                
                response_text = final_result.get("response", "I couldn't find that info.")
                response_payload = {
                    "text": response_text,
                    "suggestions": final_result.get("suggestions", [])
                }
            except Exception as e:
                logger.error(f"Context Fetch Error: {e}")
                response_text = "I encountered an error looking up that information."
                response_payload = {"text": response_text, "suggestions": []}

        else:
            # AI Answered directly (Saved 1 Call!)
            response_text = initial_result.get("response", "")
            response_payload = {
                "text": response_text,
                "suggestions": initial_result.get("suggestions", [])
            }

        # Update History
        append_conversation_message(session_key, "assistant", json.dumps(response_payload))

        # Return structured JSON for frontend
        # format: { response: JSON_STRING, session_id: STR }
        return jsonify({
            "response": json.dumps(response_payload),
            "session_id": conversation_id,
            "type": "message",
            "user": current_user.get("name") if current_user else "Guest"
        })

    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({"error": str(e)}), 500

# ===========================================
# FEEDBACK & ADMIN
# ===========================================
# FEEDBACK & ADMIN
# ===========================================

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    try:
        data = request.get_json()
        logging_utils.log_audit("FEEDBACK", "User", f"Rating: {data.get('rating')}")
        feedback_engine.save_feedback(
            session_id="jwt_session", # Simplified for now
            user_message=data.get("user_message"),
            ai_response=data.get("ai_response"),
            rating=data.get("rating"),
            comment=data.get("comment")
        )
        if data.get("rating") == "negative":
            try:
                learning_engine.log_issue(
                    question=data.get("user_message") or "",
                    issue_type="low_confidence",
                    confidence=0.0,
                    response=data.get("ai_response")
                )
            except Exception as err:
                logger.warning(f"Failed to log negative feedback for learning: {err}")
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout (Client should also delete token)"""
    # For stateless JWT, we can't really invalidate unless we blacklist. 
    # For this demo, we just log it.
    logging_utils.log_audit("LOGOUT", "User", "Logout request")
    return jsonify({"success": True})

# ===========================================
# ADMIN ENDPOINTS
# ===========================================

@app.route('/admin')
def admin_page():
    """Serve Admin Dashboard"""
    if os.path.exists("static/admin/admin.html"):
        return send_from_directory('static/admin', 'admin.html')
    return "Admin panel not found", 404

@app.route('/api/admin/stats', methods=['GET'])
def get_admin_stats():
    """Get statistics for admin dashboard"""
    try:
        # Get Feedback Stats
        feedback_stats = feedback_engine.get_stats()
        recent_feedbacks = feedback_engine.get_recent_feedbacks(limit=10)
        
        # Get Learning Stats
        unanswered = learning_engine.get_unanswered_questions()
        
        return jsonify({
            "satisfaction_rate": feedback_stats.get("satisfaction_rate", 0),
            "total_feedbacks": feedback_stats.get("total_feedbacks", 0),
            "unanswered_count": len(unanswered),
            "unanswered_logs": unanswered[-10:], # Last 10
            "recent_feedbacks": recent_feedbacks
        })
    except Exception as e:
        logger.error(f"Admin stats error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/upload', methods=['POST'])
def upload_document():
    """Upload a document to the knowledge base"""
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "message": "No file part"}), 400
            
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"success": False, "message": "No selected file"}), 400
            
        if file:
            # Ensure directory exists
            if not os.path.exists("data/knowledge_base"):
                os.makedirs("data/knowledge_base")
                
            file_path = f"data/knowledge_base/{file.filename}"
            file.save(file_path)
            
            # Ingest into RAG
            from app.engines.rag_engine import rag_engine
            success = rag_engine.ingest_file(file_path)
            
            if success:
                return jsonify({"success": True, "message": f"Successfully ingested {file.filename}"})
            else:
                return jsonify({"success": False, "message": "File saved but failed to ingest into Vector DB"})
            
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/admin/files', methods=['GET'])
def list_files():
    """List files in knowledge base"""
    try:
        files = []
        kb_path = "data/knowledge_base"
        if os.path.exists(kb_path):
            for f in os.listdir(kb_path):
                if f.endswith(('.pdf', '.txt', '.csv', '.docx')):
                    files.append(f)
        return jsonify({"files": files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/files', methods=['DELETE'])
def delete_file():
    """Delete a file from knowledge base"""
    try:
        data = request.get_json()
        filename = data.get('filename')
        if not filename:
            return jsonify({"success": False, "message": "Filename required"}), 400
        
        file_path = os.path.join("data/knowledge_base", filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            # Note: Ideally we should re-index RAG here, but for now we just delete source
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "File not found"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    try:
        # Setup File Logging
        file_handler = logging.FileHandler('server.log')
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        print(f"Starting Flask server with Google GenAI Native Model: {MODEL_NAME}")
        # Disable reloader to prevent double-execution/subprocess issues in certain envs
        app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
    except Exception as e:
        with open("crash_log.txt", "w") as f:
            f.write(f"Server Crashed: {str(e)}")
        print(f"Server Crashed: {e}")

