from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: GOOGLE_API_KEY not found in environment.")
    exit(1)

try:
    print(f"Checking models with key: {api_key[:5]}... via google-genai SDK")
    client = genai.Client(api_key=api_key)
    
    # List models provided by the API
    # Note: genai.Client doesn't have a direct 'list_models' in the same way as the old SDK.
    # We might need to use the lower level client or try a simple generation to check specific models.
    
    # Actually, let's try to generate with the configured model first to see if it works.
    target_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    print(f"\nAttempting to generate with model: '{target_model}'")
    
    try:
        response = client.models.generate_content(
            model=target_model,
            contents="Hello, justify your existence."
        )
        print(f"[SUCCESS] Model '{target_model}' is working.")
        print(f"Response: {response.text[:50]}...")
    except Exception as e:
        print(f"[FAILED] to use '{target_model}'. Error: {e}")
        
    print(f"\n--- Checking Account Capability (Limit: 0 means model is not enabled) ---\n")
    try:
        print("Listing available models for this key...")
        found_any = False
        # iterate over list
        for m in client.models.list():
            # Just print the name for now to avoid attribute errors
            print(f"  - Found: {m.name}")
            found_any = True
        
        if not found_any:
            print("  [WARNING] No models found. This API Key seemingly has access to NOTHING.")
            
    except Exception as e:
        print(f"Error listing models: {e}")

    print(f"\n--- Targeted Verification: gemini-2.5-flash ---\n")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Confirm you are working."
        )
        print("[SUCCESS] gemini-2.5-flash is working!")
        print(f"Response: {response.text[:50]}...")
    except Exception as e:
        print(f"[FAILED] gemini-2.5-flash failed: {e}")

except Exception as e:
    print(f"Fatal Error: {e}")
