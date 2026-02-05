import os
from pymongo import MongoClient
from dotenv import load_dotenv
import json

load_dotenv()

uri = os.getenv("MONGO_URI")
try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    db_name = uri.split('/')[-1].split('?')[0]
    db = client[db_name]
    
    # Find student collection
    colls = db.list_collection_names()
    student_coll = None
    for c in colls:
        if "student" in c.lower() or "ucsi" in c.lower():
            student_coll = db[c]
            break
            
    if student_coll is not None:
        doc = student_coll.find_one({}, {"_id": 0})
        print("SAMPLE_DOCUMENT_START")
        print(json.dumps(doc, default=str, indent=2))
        print("SAMPLE_DOCUMENT_END")
    else:
        print("NO_STUDENT_COLLECTION_FOUND")
        print(f"Available collections: {colls}")
        
except Exception as e:
    print(f"ERROR: {e}")
