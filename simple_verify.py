from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
model = os.getenv("GEMINI_MODEL")

print(f"Connecting to {model}...")
client = genai.Client(api_key=api_key)
try:
    response = client.models.generate_content(model=model, contents="Just say: CONNECTION OK")
    print(response.text)
except Exception as e:
    print(e)
