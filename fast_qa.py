
import json
import time
import sys
from main import app
from db_engine import DatabaseEngine

# Flush print helper
def log(msg):
    print(msg)
    sys.stdout.flush()

def run_tests():
    log("Initializing Fast QA...")
    client = app.test_client()
    
    # 1. Login
    log("Logging in...")
    db = DatabaseEngine()
    db.connect()
    student = db.student_coll.find_one({"STUDENT_NAME": {"$exists": True}}) or db.student_coll.find_one()
    s_id = str(student.get('STUDENT_NUMBER') or "1001234567")
    s_name = student.get('STUDENT_NAME') or "Test Student"
    
    resp = client.post('/api/login', json={"student_number": s_id, "name": s_name})
    token = json.loads(resp.data).get('token')
    headers = {"Authorization": f"Bearer {token}"}
    log(f"Logged in as {s_name}")

    test_cases = [
        ("Who are you?", "Persona"),
        ("What is the capital of France?", "General Knowledge"),
        ("How many students?", "DB Stats"),
        ("What is my name?", "Personal Info"),
        ("My GPA", "Security Trigger")
    ]
    
    log(f"Running {len(test_cases)} cases...")
    
    for i, (q, desc) in enumerate(test_cases):
        start = time.time()
        res = client.post('/api/chat', json={"message": q, "session_id": "fast_qa"}, headers=headers)
        data = json.loads(res.data)
        elapsed = time.time() - start
        log(f"[{i+1}/{len(test_cases)}] {desc}: '{q}' -> {data.get('response')[:30]}... ({elapsed:.2f}s)")
        
    log("Fast QA Complete.")

if __name__ == "__main__":
    run_tests()
