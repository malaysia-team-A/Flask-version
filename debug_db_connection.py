import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def check_db():
    uri = os.getenv("MONGO_URI")
    print(f"Connecting to: {uri}")
    client = MongoClient(uri)
    try:
        client.admin.command('ping')
        print("✅ Ping successful!")
        
        db_name = uri.split('/')[-1].split('?')[0] or 'UCSI_DB'
        db = client[db_name]
        
        print(f"Database: {db_name}")
        print(f"Collections: {db.list_collection_names()}")
        
        # Check UCSI collection
        sample = db.UCSI.find_one()
        if sample:
            print("\n=== Sample Student ===")
            for k, v in sample.items():
                print(f"{k}: {v}")
        else:
            print("\n❌ No students found in UCSI collection.")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_db()
