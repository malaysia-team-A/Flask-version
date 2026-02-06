import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGO_URI")
client = MongoClient(uri)
db_name = uri.split('/')[-1].split('?')[0]
db = client[db_name]

# Find the student collection
colls = db.list_collection_names()
print(f"Collections: {colls}")

student_coll = None
candidates = ["UCSI", "students", "Students", "UCSI_STUDENTS"]
for c in candidates:
    if c in colls:
        student_coll = db[c]
        break

if not student_coll:
    # fallback
    for c in colls:
        if "student" in c.lower() or "ucsi" in c.lower():
            student_coll = db[c]
            break

if student_coll:
    print(f"Using collection: {student_coll.name}")
    student = student_coll.find_one()
    
    if student:
        print("\n--- Student Sample Keys ---")
        print(student.keys())
        
        print("\n--- GENDER Field check ---")
        print(f"GENDER: {student.get('GENDER')}")
        print(f"Gender: {student.get('Gender')}")
        print(f"gender: {student.get('gender')}")
        
        print("\n--- DOB Field check ---")
        print(f"DOB: {student.get('DOB')}")
        print(f"DATE_OF_BIRTH: {student.get('DATE_OF_BIRTH')}")
        print(f"DateOfBirth: {student.get('DateOfBirth')}")
        
        print("\n--- PASSWORD Field check ---")
        pwd = student.get('PASSWORD') or student.get('Password') or student.get('password')
        print(f"Value: {pwd}")
        
        from werkzeug.security import check_password_hash
        try:
            is_valid = check_password_hash(str(pwd), "test")
            print(f"check_password_hash result (with 'test'): {is_valid}")
        except Exception as e:
            print(f"check_password_hash failed/error: {e}")
            
    else:
        print("Collection is empty.")
else:
    print("No student collection found.")
