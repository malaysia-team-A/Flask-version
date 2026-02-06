from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

target_model = os.getenv("GEMINI_MODEL")
api_key = os.getenv("GOOGLE_API_KEY")

print(f"--- Final Configuration Check ---")
print(f"Model configured in env: {target_model}")
print(f"API Key present: {'Yes' if api_key else 'No'}")

client = genai.Client(api_key=api_key)

try:
    print(f"\nSending test request to {target_model}...")
    response = client.models.generate_content(
        model=target_model,
        contents="State your name and version."
    )
    print(f"\n[SUCCESS] Response received:")
    print(f"> {response.text}")
except Exception as e:
    print(f"\n[FAILED] Error: {e}")
