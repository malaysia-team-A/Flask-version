import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# User credentials to test
TARGET_ID = "5004273354"
TARGET_NAME = "Vicky Yiran"

print(f"--- Debugging Login for: {TARGET_NAME} ({TARGET_ID}) ---")

uri = os.getenv("MONGO_URI")
if not uri:
    print("❌ MONGO_URI missing")
    sys.exit(1)

try:
    print("Connecting to MongoDB...")
    # 5s timeout
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("✅ Connected!")
    
    db_name = uri.split('/')[-1].split('?')[0] or "UCSI_DB"
    db = client[db_name]
    print(f"Database: {db_name}")
    
    # List collections
    colls = db.list_collection_names()
    print(f"Collections: {colls}")
    
    found = False
    
    # Search ALL collections
    for coll_name in colls:
        try:
            coll = db[coll_name]
            print(f"\nScanning collection: {coll_name}")
            
            # 1. Search by ID (String)
            doc = coll.find_one({"STUDENT_NUMBER": str(TARGET_ID)})
            
            # 2. Search by ID (Int)
            if not doc and TARGET_ID.isdigit():
                doc = coll.find_one({"STUDENT_NUMBER": int(TARGET_ID)})
                
            # 3. Fuzzy ID Search
            if not doc:
                id_fields = ["student_number", "StudentNumber", "student_id", "id", "ID"]
                for field in id_fields:
                    doc = coll.find_one({field: str(TARGET_ID)})
                    if not doc and TARGET_ID.isdigit():
                        doc = coll.find_one({field: int(TARGET_ID)})
                    if doc: break
            
            if doc:
                print(f"✅ Found Document in '{coll_name}':")
                print(doc)
                found = True
                
                # Check Name Match
                # Standardize field checking
                name_val = doc.get("STUDENT_NAME") or doc.get("name") or doc.get("Name") or doc.get("full_name")
                print(f"Name in DB: '{name_val}'")
                
                if str(name_val).strip().lower() == TARGET_NAME.strip().lower():
                    print("✅ Name MATCHED!")
                else:
                    print(f"❌ Name MISMATCH! Expected '{TARGET_NAME.lower()}', got '{str(name_val).lower()}'")
                
                break # Stop after finding ID
                
        except Exception as e:
            print(f"Error scanning {coll_name}: {e}")

    if not found:
        print("\n❌ User ID NOT FOUND in any collection.")

except Exception as e:
    print(f"\n❌ CRITICAL ERROR: {e}")
