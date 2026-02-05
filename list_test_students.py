from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def list_students():
    uri = os.getenv("MONGO_URI")
    client = MongoClient(uri)
    db_name = uri.split('/')[-1].split('?')[0] or 'UCSI_DB'
    db = client[db_name]
    
    # Check if UCSI collection exists
    colls = db.list_collection_names()
    print(f"Collections present: {colls}")
    
    # Try different collection names if UCSI doesn't exist
    target_coll = "UCSI"
    if "UCSI" not in colls and len(colls) > 0:
        target_coll = colls[0]
        print(f"UCSI not found, using {target_coll} instead.")

    students = list(db[target_coll].find().limit(10))
    print(f"\nFound {len(students)} students in '{target_coll}':")
    for s in students:
        s_id = s.get("STUDENT_NUMBER")
        s_name = s.get("STUDENT_NAME")
        print(f"- ID: {s_id} (Type: {type(s_id).__name__}), Name: '{s_name}'")

if __name__ == "__main__":
    list_students()
