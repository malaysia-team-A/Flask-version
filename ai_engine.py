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
        
        self.qa_template = """You are Kai, a smart and energetic student assistant for UCSI University.
Answer based on the Context and Conversation History.

Context:
{context}

Conversation History:
{conversation}

Question: {question}

Instructions:
1. **Persona**: Friendly, energetic, helpful.
2. **Format**: **STRICT JSON OUTPUT ONLY**. No markdown block ` ```json `. Just the raw JSON.
3. **Structure**:
   {{
      "text": "The actual answer text here...",
      "suggestions": ["Follow-up Q1", "Follow-up Q2", "Follow-up Q3"]
   }}
4. **Suggestions**: Provide 3 short, relevant follow-up questions that the user might want to ask next.
5. **Accuracy**: Use Context if available. If asking about YOU (personality), be creative. if unknown, say you don't know politely.

Response (JSON):
"""

    def process_message(self, user_message: str, data_context: str = "", conversation_history=None) -> dict:
        """
        Unified processing to save API calls.
        Returns JSON: { "response": str, "suggestions": list, "needs_context": bool, "search_term": str }
        """
        if not self.client:
            return {"response": "System Error: AI Model not initialized.", "suggestions": []}

        try:
            # 1. Prepare Conversation Text
            conversation_text = ""
            if conversation_history:
                recent = conversation_history[-6:] # Keep it short to save tokens
                segments = []
                for item in recent:
                    role = "User" if item.get("role") == "user" else "Model"
                    content = item.get('content', '')
                    # Clean previous JSON outputs from history to avoid confusion
                    try:
                        c_json = json.loads(content)
                        if isinstance(c_json, dict):
                            content = c_json.get('text', '')
                    except:
                        pass
                    segments.append(f"{role}: {content}")
                conversation_text = "\n".join(segments)

            # 2. Construct Prompt (One-Shot Decision)
            # If data_context is provided, we force an answer.
            # If NO data_context, we check if we NEED it.
            
            if data_context:
                # PHASE 2: We have data, generate answer.
                prompt = self.qa_template.format(
                    context=data_context,
                    conversation=conversation_text,
                    question=user_message
                )
            else:
                # PHASE 1: Decide Intent OR Answer directly
                prompt = f"""You are Kai, a university assistant.
Current Conversation:
{conversation_text}

User Question: {user_message}

Instructions:
1. If the user asks about SPECIFIC student data (count, gender, grades, verification), request DB access.
   Output: {{ "needs_context": true, "search_term": "extracted keywords" }}
   
2. If it's a GENERAL question (greetings, about university info, jokes, personality), ANSWER IT DIRECTLY.
   Output: {{ 
      "text": "Your answer here...", 
      "suggestions": ["Follow-up 1", "Follow-up 2", "Follow-up 3"] 
   }}

3. STRICT JSON OUTPUT ONLY.
"""

            # 3. Call API
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            raw_text = response.text.strip()
            
            # 4. Parse JSON
            json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                # Normalize output keys
                return {
                    "response": data.get("text", ""),
                    "suggestions": data.get("suggestions", []),
                    "needs_context": data.get("needs_context", False),
                    "search_term": data.get("search_term", None)
                }
            else:
                # Fallback for plain text response
                return {
                    "response": raw_text, 
                    "suggestions": ["Menu", "Contact"],
                    "needs_context": False
                }

        except Exception as e:
            print(f"AI Error: {e}")
            return {"response": "I'm having trouble connecting right now.", "suggestions": []}

    # ... (Unified process_message method kept above) ...
    # Deprecated fallback methods removed for cleanliness.

