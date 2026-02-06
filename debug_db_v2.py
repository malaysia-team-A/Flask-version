import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

# Load env manually to be sure
load_dotenv()

uri = os.getenv("MONGO_URI")
print(f"DEBUG: Loaded URI: {uri}")

if not uri:
    print("FATAL: MONGO_URI not found in environment")
    sys.exit(1)

print("DEBUG: Attempting connection with 5s timeout...")
try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("SUCCESS: Connected to MongoDB Atlas!")
    
    db_name = uri.split('/')[-1].split('?')[0]
    db = client[db_name]
    print(f"DEBUG: Using Database '{db_name}'")
    
    colls = db.list_collection_names()
    print(f"DEBUG: Collections found: {colls}")
    
    print("\n--- Checking Collections content ---")
    for name in colls:
        count = db[name].count_documents({})
        print(f"Collection '{name}': {count} documents")
        sample = db[name].find_one()
        if sample:
            print(f"Sample in '{name}': {sample}")
            
except Exception as e:
    print(f"FATAL: Connection Failed. Reason: {e}")
