from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
model = "gemini-2.5-flash-lite"

print(f"Testing {model}...")
client = genai.Client(api_key=api_key)
try:
    response = client.models.generate_content(model=model, contents="Are you the lite version?")
    print(f"[SUCCESS] {model} is available!")
    print(response.text)
except Exception as e:
    print(f"[FAILED] {model} error: {e}")
