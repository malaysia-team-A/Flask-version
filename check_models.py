
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print(f"Checking models for API Key: {api_key[:10]}...")

try:
    print("\n--- Available Models ---")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
            
    print("\n--- check complete ---")
except Exception as e:
    print(f"Error listing models: {e}")
