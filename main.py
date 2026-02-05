"""
University Chatbot API - Main Server (Flask Version)
Features:
- AI-powered chatbot with local Ollama LLM
- Student verification by Student Number + Name
- RAG (Retrieval-Augmented Generation) for data queries
- Intent detection by AI
- Admin Panel & Statistics
"""
from flask import Flask, request, jsonify, send_from_directory, render_template_string
from data_engine import DataEngine
from ai_engine import AIEngine
from feedback_engine import FeedbackEngine
import os
import re
import logging
from datetime import datetime, timedelta
import secrets

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("UniversityChatbot")

# Initialize Flask App
app = Flask(__name__, static_folder="UI_hompage", static_url_path="/site")
app.secret_key = secrets.token_hex(16)

# Initialize Engines
DATA_FILE = "Chatbot_TestData.xlsx"
data_engine = DataEngine(DATA_FILE)

MODEL_NAME = "gemma3:12b"
ai_engine = AIEngine(MODEL_NAME)

feedback_engine = FeedbackEngine()

# In-memory session storage (for demo - use Redis/DB in production)
verified_sessions = {}

# Ensure directories exist
if not os.path.exists("knowledge_base"):
    os.makedirs("knowledge_base")

@app.route('/')
def home():
    return jsonify({"status": "University Chatbot API is running", "docs": "/site/code_hompage.html"})

@app.route('/site/<path:filename>')
def serve_static(filename):
    return send_from_directory('UI_hompage', filename)

# ===========================================
# API ENDPOINTS
# ===========================================

@app.route('/api/verify', methods=['POST'])
def verify_student():
    """Verify student identity"""
    try:
        data = request.get_json()
        student_number = data.get("student_number")
        name = data.get("name")
        session_id = data.get("session_id")
        
        # Verify with Excel Data
        is_valid, student_data, message = data_engine.verify_student(student_number, name)
        
        if is_valid:
            # Create Session
            verified_sessions[session_id] = {
                "student_number": student_number,
                "name": name,
                "student_data": student_data,
                "expires": datetime.now() + timedelta(hours=1)
            }
            logger.info(f"Session verified: {session_id} for {name}")
            return jsonify({"success": True, "message": "Verification successful."})
        else:
            return jsonify({"success": False, "message": message})
            
    except Exception as e:
        logger.error(f"Verification error: {e}")
        return jsonify({"success": False, "message": "Server error during verification"}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint"""
    try:
        data = request.get_json()
        user_message = data.get("message")
        session_id = data.get("session_id")
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
            
        # Check Session Logic
        verified_student = None
        if session_id and session_id in verified_sessions:
            verified_student = verified_sessions[session_id]
            # Refresh session
            verified_student["expires"] = datetime.now() + timedelta(hours=1)
        
        # Determine Intent
        intent_result = ai_engine.classify_intent(user_message)
        intent = intent_result.get("intent", "GENERAL")
        search_term = intent_result.get("search_term")
        
        logger.info(f"Intent classified: {intent}, search_term: {search_term}")
        
        context = ""
        response_type = "message"
        
        # ===========================================
        # PERSONAL_DATA: Requires authentication
        # ===========================================
        
        if intent == "PERSONAL_DATA":
            # Check if user is logged in
            if not verified_student:
                return jsonify({
                    "response": "🔒 This is student personal information. To view details, please login using the Login button above.",
                    "type": "login_hint",
                    "user": "guest"
                })
            
            # User is logged in - check if asking about themselves or someone else
            if search_term:
                # Asking about a specific student by name
                logged_in_name = verified_student.get("name", "").lower().strip()
                searched_name = search_term.lower().strip()
                
                # Check if searching for themselves
                is_self_search = (
                    searched_name in logged_in_name or 
                    logged_in_name in searched_name or
                    any(part in logged_in_name for part in searched_name.split())
                )
                
                if is_self_search:
                    student_data = verified_student.get("student_data", {})
                    context = f"YOUR PERSONAL DATA:\n{student_data}\n\nThis is your information."
                else:
                    return jsonify({
                        "response": f"🔒 Privacy Protection: You can only access your own information. You are logged in as '{verified_student['name']}', so you cannot view information about '{search_term}'.",
                        "type": "message",
                        "user": verified_student["name"]
                    })
            else:
                # Asking about their own data
                student_data = verified_student.get("student_data", {})
                context = f"STUDENT'S PERSONAL DATA:\n{student_data}\n\nThis is {verified_student['name']}'s information."
        
        # ===========================================
        # GENERAL: Public information (no auth needed)
        # ===========================================
        
        elif intent == "GENERAL":
            # Check if asking for statistics
            message_lower = user_message.lower()
            if any(kw in message_lower for kw in ["how many", "total student", "gender", "ratio", "nationality", "statistics", "student count"]):
                stats = data_engine.get_summary_stats()
                context = f"UNIVERSITY STATISTICS:\n{stats}"
            # Otherwise, use RAG context or general knowledge
            else:
                from rag_engine import rag_engine
                rag_context = rag_engine.search(user_message)
                if rag_context:
                    context = f"UNIVERSITY KNOWLEDGE BASE:\n{rag_context}"
        
        # Generate response
        response_text = ai_engine.get_response(user_message, data_context=context)
        
        return jsonify({
            "response": response_text,
            "user": verified_student["name"] if verified_student else "guest",
            "type": response_type
        })
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    """Clear verified session"""
    data = request.get_json()
    session_id = data.get("session_id")
    if session_id and session_id in verified_sessions:
        del verified_sessions[session_id]
    return jsonify({"success": True})

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback for an AI response"""
    try:
        data = request.get_json()
        success = feedback_engine.save_feedback(
            session_id=data.get("session_id"),
            user_message=data.get("user_message"),
            ai_response=data.get("ai_response"),
            rating=data.get("rating"),
            comment=data.get("comment")
        )
        return jsonify({"success": success})
    except Exception as e:
        logger.error(f"Feedback error: {e}")
        return jsonify({"error": str(e)}), 500

# ===========================================
# ADMIN ENDPOINTS
# ===========================================

@app.route('/admin')
def admin_page():
    """Serve Admin Dashboard"""
    if os.path.exists("admin/admin.html"):
        return send_from_directory('admin', 'admin.html')
    return "Admin panel not found", 404

@app.route('/api/admin/stats', methods=['GET'])
def get_admin_stats():
    """Get statistics for admin dashboard"""
    try:
        # Get Feedback Stats
        feedback_stats = feedback_engine.get_stats()
        recent_feedbacks = feedback_engine.get_recent_feedbacks(limit=10)
        
        # Get Learning Stats
        from learning_engine import learning_engine
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
            if not os.path.exists("knowledge_base"):
                os.makedirs("knowledge_base")
                
            file_path = f"knowledge_base/{file.filename}"
            file.save(file_path)
            
            # Ingest into RAG
            from rag_engine import rag_engine
            success = rag_engine.ingest_file(file_path)
            
            if success:
                return jsonify({"success": True, "message": f"Successfully ingested {file.filename}"})
            else:
                return jsonify({"success": False, "message": "File saved but failed to ingest into Vector DB"})
            
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    print(f"Starting Flask server with Ollama model: {MODEL_NAME}")
    app.run(host="0.0.0.0", port=8000, debug=True)
