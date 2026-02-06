
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

print("Checking available Gemini models for your API Key...")
try:
    client = genai.Client(api_key=api_key)
    # List models via new SDK
    count = 0
    for m in client.models.list():
        # We only care about models that can generate content (chat/text)
        if "generateContent" in (m.supported_generation_methods or []):
            print(f"- {m.name} (Display: {m.display_name})")
            count += 1
    
    if count == 0:
        print("No models found. Check your API key permissions.")
        
except Exception as e:
    print(f"Error checking models: {e}")
