
import os
import google.generativeai as genai
import sys

# Hardcode the key to test directly
API_KEY = "AIzaSyDYkWbGlPV9JTSfQgW1AWWpJggbG_BBgrs"
genai.configure(api_key=API_KEY)

print(f"Checking models for key: {API_KEY[:5]}...")

try:
    with open("model_list_log.txt", "w", encoding="utf-8") as f:
        f.write("--- Model List ---\n")
        models = list(genai.list_models())
        print(f"Found {len(models)} models.")
        for m in models:
            line = f"Name: {m.name} | Methods: {m.supported_generation_methods}\n"
            print(line.strip())
            f.write(line)
except Exception as e:
    print(f"Error: {e}")
    with open("model_list_log.txt", "w", encoding="utf-8") as f:
        f.write(f"Error: {e}")
