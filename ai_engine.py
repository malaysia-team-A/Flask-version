import os
import re
import json
import os
import re
import json
from google import genai # New SDK


class AIEngine:
    def __init__(self, model_name="gemini-2.5-flash-lite"):
        """
        Initialize using the NEW Google Gen AI SDK (google-genai)
        """
        self.raw_model_name = model_name
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.client = None

        if self.api_key:
            try:
                # New SDK Client Initialization
                print(f"[INIT] Initializing Gemini AI ({self.raw_model_name}) via NEW Google Gen AI SDK...")
                self.client = genai.Client(api_key=self.api_key)
                
                # Normalize model name for new SDK (e.g., remove 'models/' prefix if present)
                # The new SDK typically expects 'gemini-1.5-flash'
                self.model_name = self.raw_model_name.replace("models/", "")
                
            except Exception as e:
                print(f"Gemini Init Failed: {e}")
                self.client = None
        else:
            print("[ERROR] GOOGLE_API_KEY not found.")

        # PROMPTS (Kept same)
        self.intent_template = """
        You are an intent classifier for a University Chatbot.
        Classify the following user message into one of these intents:
        
        1. GENERAL: General questions about the university, statistics, campus, facilities, programs.
        2. PERSONAL_DATA: Questions requiring student personal data (grades, enrollment status, "who is X?", "my info").
        
        Also extract any specific entity/name mentioned.
        
        Output strictly in JSON format:
        {{
            "intent": "GENERAL" or "PERSONAL_DATA",
            "search_term": "extracted name or entity or null"
        }}
        
        User Message: {user_message}
        """
        
        self.qa_template = """You are Kai, a smart and energetic student assistant for UCSI University.
Answer using the structured context and prior conversation. Resolve pronouns or follow-up references using the conversation log before relying on general knowledge.

Conversation History:
{conversation}

Context:
{context}

Question: {question}

Instructions:
- Be concise. Answer directly without filler phrases like "As an AI...".
- Keep responses short (1-2 sentences) for simple questions.
- Use bullet points only for data listings.
- Maintain a helpful and friendly tone.
- CRITICAL: The [Context] may be JSON data. Read it carefully to answer questions like "how many" or "ratio".
- If the user asks about YOU (personality, favorite color, jokes), ignore the context and answer creatively and enthusiastically as 'Kai'.
- If the answer is in the Context, you MUST use it.
- If the Context is empty or irrelevant, use your general knowledge to be helpful.
"""

    def classify_intent(self, user_message: str) -> dict:
        """Classify intent using New Google SDK"""
        if not self.client:
            return {"intent": "GENERAL", "search_term": None}
            
        try:
            prompt = self.intent_template.format(user_message=user_message)
            
            # New SDK Call Structure
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            content = response.text.strip()
            
            # Extract JSON
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {"intent": "GENERAL", "search_term": None}
        except Exception as e:
            print(f"Intent Error: {e}")
            return {"intent": "GENERAL", "search_term": None}

    def get_response(self, user_message: str, data_context: str = "", conversation_history=None) -> str:
        """Get answer using New Google SDK"""
        if not self.client:
            return "System Error: AI Model not initialized."

        try:
            conversation_text = ""
            if conversation_history:
                recent_history = conversation_history[-8:]
                segments = []
                for item in recent_history:
                    role = item.get("role")
                    speaker = "User" if role == "user" else "Model" 
                    segments.append(f"{speaker}: {item.get('content', '')}")
                conversation_text = "\n".join(segments)

            prompt = self.qa_template.format(
                context=data_context or "No structured context provided.",
                conversation=conversation_text or "No prior conversation.",
                question=user_message
            )
            
            # New SDK Call Structure
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text.strip()

        except Exception as e:
            print(f"Response Error: {e}")
            return "I apologize, but I encountered an error generating a response."

