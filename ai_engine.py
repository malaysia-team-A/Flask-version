try:
    from langchain_ollama import ChatOllama
except ImportError:
    try:
        from langchain_community.chat_models import ChatOllama
    except ImportError:
        print("CRITICAL: langchain-ollama or langchain-community not installed.")
        raise

from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
import json
import re

class AIEngine:
    def __init__(self, model_name="gemma3:12b"):
        """
        Initialize with LangChain ChatOllama
        """
        self.llm = ChatOllama(model=model_name, temperature=0.7)
        self.model_name = model_name
        
        # Intent Classification Prompt
        self.intent_prompt = PromptTemplate(
            input_variables=["user_message"],
            template="""
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
        )
        
        # QA Prompt
        self.qa_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are UCSI University's official AI assistant.
Answer based on the provided context. Be concise and direct.

Context:
{context}

Question: {question}

Instructions:
- Give a direct, helpful answer in 2-4 sentences when possible
- Use bullet points for lists
- Do NOT say "I don't have specific knowledge" or add disclaimers
- If context is empty, give a brief helpful answer based on general knowledge
"""
        )

    def classify_intent(self, user_message: str) -> dict:
        """
        Classify intent using LangChain
        """
        try:
            formatted_prompt = self.intent_prompt.format(user_message=user_message)
            response = self.llm.invoke([HumanMessage(content=formatted_prompt)])
            content = response.content.strip()
            
            # Extract JSON from response (handle potential markdown blocks)
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {"intent": "GENERAL", "search_term": None}
                
        except Exception as e:
            print(f"Intent Error: {e}")
            return {"intent": "GENERAL", "search_term": None}

    def get_response(self, user_message: str, data_context: str = "") -> str:
        """
        Get answer using LangChain
        """
        try:
            formatted_prompt = self.qa_prompt.format(context=data_context, question=user_message)
            response = self.llm.invoke([HumanMessage(content=formatted_prompt)])
            return response.content.strip()
            
        except Exception as e:
            print(f"Response Error: {e}")
            return "I apologize, but I encountered an error generating a response."
