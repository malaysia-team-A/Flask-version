
import os
import sys
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# Redirect output to file for reliability
class Tee(object):
    def __init__(self, name, mode):
        self.file = open(name, mode, encoding='utf-8')
        self.stdout = sys.stdout
        sys.stdout = self
    def __del__(self):
        sys.stdout = self.stdout
        self.file.close()
    def write(self, data):
        self.file.write(data)
        self.stdout.write(data)
    def flush(self):
        self.file.flush()
        self.stdout.flush()

# Start capturing
sys.stdout = Tee("verify_result.txt", "w")

print("--- VERIFICATION START ---")
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

print(f"🔑 API Key Loaded: {'Yes' if API_KEY else 'No'} (Start: {API_KEY[:5]}...)")
print(f"🎯 Target Model: {MODEL_NAME}")
print("-" * 30)

# 1. Test via REST API (List Models)
print("1️⃣ Testing API Key validity via REST (List Models)...")
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
try:
    resp = requests.get(url)
    if resp.status_code == 200:
        print("✅ REST API Call Success! API Key is VALID.")
        data = resp.json()
        models = [m['name'] for m in data.get('models', []) if 'generateContent' in m.get('supportedGenerationMethods', [])]
        
        print(f"   Available Models (partial): {models[:5]}")
        
        # Check normalized names
        target_name_clean = MODEL_NAME.replace("models/", "")
        found = False
        for m in models:
            if target_name_clean in m:
                found = True
                print(f"✅ Target model '{m}' found in permission list.")
                break
        
        if not found:
            print(f"⚠️ Target model '{MODEL_NAME}' NOT explicitly found in list.")
    else:
        print(f"❌ REST API Failed: {resp.status_code} - {resp.text}")
except Exception as e:
    print(f"❌ REST Request Error: {e}")

print("-" * 30)

# 2. Test via Google SDK
print(f"2️⃣ Testing Generation using SDK...")
try:
    genai.configure(api_key=API_KEY)
    
    # Force prefix used in fix
    test_name = f"models/{MODEL_NAME}" if not MODEL_NAME.startswith("models/") else MODEL_NAME
    print(f"   👉 Trying model name: '{test_name}'...")
    
    model = genai.GenerativeModel(test_name)
    response = model.generate_content("Hello")
    if response and response.text:
        print(f"   ✅ SUCCESS! Response: {response.text.strip()}")
    else:
        print("   ❌ Generation executed but returned empty text.")

except Exception as e:
    print(f"❌ SDK Error: {e}")

print("--- VERIFICATION END ---")
