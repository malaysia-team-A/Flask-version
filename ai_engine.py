import requests
import json
from learning_engine import learning_engine
from rag_engine import rag_engine

class AIEngine:
    def __init__(self, model_name="llama3.2:3b"):
        """
        Initialize with Ollama local model
        """
        self.model_name = model_name
        self.base_url = "http://localhost:11434"
        self.chat_history = []
        
        # System prompt context
        self.system_prompt = """You are a helpful and friendly chatbot for UCSI University.
You assist students and visitors with information about the university.
You have access to student data when provided in the context.

RESPONSE STYLE:
- Be concise and friendly
- Use emojis sparingly for visual appeal
- Format data in a clean, readable way

FORMATTING RULES:

1. For STUDENT INFORMATION, use this format:

📋 Student Information
━━━━━━━━━━━━━━━━━━━━━━━━
Student Number: [value]
Name: [value]
Nationality: [value]
Gender: [value]
Programme: [value]
Intake: [value]
Status: [value]
━━━━━━━━━━━━━━━━━━━━━━━━

2. For STATISTICS, use this format:

📊 University Statistics
━━━━━━━━━━━━━━━━━━━━━━━━
Total Students: [number]

👥 Gender Distribution:
   Female: [number] ([percentage]%)
   Male: [number] ([percentage]%)

🌍 Top Nationalities:
   1. [country]: [number]
   2. [country]: [number]
━━━━━━━━━━━━━━━━━━━━━━━━

3. For GENERAL questions, just be helpful and concise.

IMPORTANT: Always put each data field on its OWN LINE. Never concatenate multiple fields on one line."""

        # Check if Ollama is running
        self._check_connection()
    
    def _check_connection(self):
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m["name"] for m in models]
                print(f"Ollama connected. Available models: {model_names}")
        except requests.exceptions.ConnectionError:
            print("Warning: Ollama server not running.")
        except Exception as e:
            print(f"Warning: Could not connect to Ollama: {e}")

    def classify_intent(self, user_message: str) -> dict:
        """
        Use LLM to classify the intent of the user's message.
        Returns a dict with 'intent' and optionally 'search_term'.
        
        Simplified Intents:
        - GENERAL: Everything that doesn't require authentication (greetings, university info, statistics)
        - PERSONAL_DATA: Anything related to student personal information (my info, who is X, student records)
        """
        classification_prompt = """Classify the following user message into ONE of these intents:

1. GENERAL - General conversation, greetings, university info, programs, statistics (student count, gender ratio, nationality breakdown), campus facilities, etc. Anything that is PUBLIC information.

2. PERSONAL_DATA - Any request for STUDENT PERSONAL information. This includes:
   - User asking about their OWN data ("my grades", "my enrollment", "my info", "show me my details")
   - User asking about a SPECIFIC student by name ("who is John?", "tell me about Mary", "find student X")
   - Any request that would reveal individual student records

If the intent is PERSONAL_DATA and a specific student name is mentioned, extract it as search_term.

Respond in this exact JSON format only, no other text:
{"intent": "INTENT_NAME", "search_term": "student name if mentioned or null"}

User message: """ + user_message

        try:
            payload = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": classification_prompt}],
                "stream": False,
                "format": "json"
            }
            
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("message", {}).get("content", "{}")
                try:
                    parsed = json.loads(content)
                    return parsed
                except json.JSONDecodeError:
                    # Fallback: try to extract intent from text
                    content_upper = content.upper()
                    if "PERSONAL" in content_upper or "STUDENT" in content_upper:
                        return {"intent": "PERSONAL_DATA", "search_term": None}
                    return {"intent": "GENERAL", "search_term": None}
            
            return {"intent": "GENERAL", "search_term": None}
            
        except Exception as e:
            print(f"Intent classification error: {e}")
            return {"intent": "GENERAL", "search_term": None}

    def get_response(self, user_message, data_context=""):
        """
        Get a response from the local LLM
        """
        try:
            # RAG Integration: If no specific context (like personal data), try to get from Knowledge Base
            if not data_context:
                rag_context = rag_engine.search(user_message)
                if rag_context:
                    data_context = f"UNIVERSITY KNOWLEDGE BASE:\n{rag_context}"

            # Build the prompt with context
            if data_context:
                full_prompt = f"""Context Data:
{data_context}

User Question: {user_message}

Please answer based on the context data provided above. Be specific and use the data."""
            else:
                full_prompt = user_message
            
            # Prepare the request
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    *self.chat_history[-10:],  # Keep last 10 messages
                    {"role": "user", "content": full_prompt}
                ],
                "stream": False
            }
            
            # Call Ollama API
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                assistant_message = result.get("message", {}).get("content", "")
                
                # Check for refusal / low confidence
                refusal_phrases = ["i don't know", "i'm not sure", "i do not know", "unable to answer", "cannot find payment", "please contact"]
                lower_msg = assistant_message.lower()
                
                if any(phrase in lower_msg for phrase in refusal_phrases):
                    learning_engine.log_issue(
                        question=user_message,
                        issue_type="unanswered",
                        confidence=0.1,
                        response=assistant_message
                    )
                
                # Update chat history
                self.chat_history.append({"role": "user", "content": user_message})
                self.chat_history.append({"role": "assistant", "content": assistant_message})
                
                return assistant_message
            else:
                return f"Error: Ollama returned status {response.status_code}"
                
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama. Make sure Ollama is running."
        except requests.exceptions.Timeout:
            return "Error: Request timed out. Please try a simpler question."
        except Exception as e:
            return f"Error: {str(e)}"

    def clear_history(self):
        """Clear chat history"""
        self.chat_history = []


if __name__ == "__main__":
    print("Testing AI Engine with Intent Classification...")
    engine = AIEngine("llama3.2:3b")
    
    # Test intent classification
    test_messages = [
        "Hello!",
        "How many students are enrolled?",
        "Who is Vicky Yiran?",
        "Tell me about John Smith",
        "What are my grades?",
        "Show me my enrollment status"
    ]
    
    for msg in test_messages:
        intent = engine.classify_intent(msg)
        print(f"Message: '{msg}' -> Intent: {intent}")
