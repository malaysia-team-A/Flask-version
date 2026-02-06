import unittest
import json
import time
from main import app
from db_engine import DatabaseEngine

class TestQAMini(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True
        cls.db = DatabaseEngine()
        cls.db.connect()
        
        # Helper to find a real student
        cls.student = cls.db.student_coll.find_one({"STUDENT_NAME": {"$exists": True}}) or cls.db.student_coll.find_one()
        cls.student_id = str(cls.student.get('STUDENT_NUMBER') or "1001234567")
        cls.student_name = cls.student.get('STUDENT_NAME') or "Test Student"
        
        # Login
        resp = cls.app.post('/api/login', json={"student_number": cls.student_id, "name": cls.student_name})
        cls.token = json.loads(resp.data).get('token')
        cls.auth_headers = {"Authorization": f"Bearer {cls.token}"}

    def run_chat_test(self, message, headers=None, expected_keywords=None):
        print(f"Testing: {message}...", end=" ", flush=True)
        time.sleep(1) # Rate limit protection
        response = self.app.post('/api/chat', json={"message": message}, headers=headers)
        data = json.loads(response.data)
        answer = data.get("response", "")
        
        passed = True
        if expected_keywords:
            if not any(k.lower() in answer.lower() for k in expected_keywords):
                passed = False
        
        status = "PASSED" if passed else f"FAILED (Got: {answer[:30]}...)"
        print(status)
        return passed

    def test_mini_suite(self):
        print("\n=== MINI QA SUITE (10 Cases) ===")
        tests = [
            ("Hello", ["Hello", "Hi", "Kai"], None),
            ("What is your favorite color?", ["yellow", "energy"], None), # Personality
            ("How many students are there?", ["500", "total"], None), # DB Stats
            ("What is the gender ratio?", ["female", "male", "ratio"], None), # DB Calc
            ("Where is UCSI located?", ["Kuala Lumpur", "Sarawak", "Cheras"], None), # GK/RAG
            ("What is my student ID?", [str(self.student_id)], self.auth_headers), # Personal
            ("What is my name?", [self.student_name.split()[0]], self.auth_headers), # Personal
            ("Show my grades", ["password", "Security"], self.auth_headers), # Dual Auth
            ("hkjhdfskjhdf", ["apologize", "don't know", "clarify"], None), # Garbage
            ("Tell me a java joke", ["Java", "joke"], None) # Creative
        ]
        
        passed_count = 0
        for input_text, keywords, headers in tests:
            if self.run_chat_test(input_text, headers, keywords):
                passed_count += 1
                
        print(f"\nResult: {passed_count}/{len(tests)} Passed")

if __name__ == '__main__':
    unittest.main()
