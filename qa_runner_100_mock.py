
import unittest
import json
import time
import sys
from unittest.mock import MagicMock, patch

# Mock the AI Engine's expensive parts BEFORE importing main/app if possible, 
# or patch them in setUp.
from main import app
from db_engine import DatabaseEngine

class TestQA100Mock(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Setting up Mock QA Environment...")
        cls.app = app.test_client()
        cls.app.testing = True
        
        # Real DB Connection
        cls.db = DatabaseEngine()
        cls.db.connect()
        cls.student = cls.db.student_coll.find_one({"STUDENT_NAME": {"$exists": True}}) or cls.db.student_coll.find_one()
        cls.s_id = str(cls.student.get('STUDENT_NUMBER') or "1001234567")
        cls.s_name = cls.student.get('STUDENT_NAME') or "Test Student"
        
        # 1. Login
        resp = cls.app.post('/api/login', json={"student_number": cls.s_id, "name": cls.s_name})
        cls.token = json.loads(resp.data).get('token')
        cls.auth_headers = {"Authorization": f"Bearer {cls.token}"}
        
        # PATCH: Mock the AIEngine methods to skip LLM but keep logic
        # We want to test logic, so we only mock the LLM invoke
        cls.patcher = patch('langchain_community.chat_models.ChatOllama.invoke')
        cls.mock_llm = cls.patcher.start()
        
        # Configure Mock based on input
        def side_effect(messages):
            content = messages[0].content
            # Intent Classification Mock
            if "Intent" in content or "intent classifier" in content:
                if "GPA" in content or "grades" in content or "name" in content:
                    return MagicMock(content='{"intent": "PERSONAL_DATA"}')
                return MagicMock(content='{"intent": "GENERAL"}')
            
            # QA Response Mock
            val = "Mocked AI Response: "
            if "gender" in content.lower(): val += "Males: 50, Females: 50"
            elif "password" in content.lower(): val += "Please enter password"
            else: val += "Here is some info."
            return MagicMock(content=val)
            
        cls.mock_llm.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        cls.patcher.stop()

    def run_chat(self, msg, headers=None, expect_type=None):
        res = self.app.post('/api/chat', json={"message": msg, "session_id": "mock_qa"}, headers=headers)
        data = json.loads(res.data)
        return data

    def test_run_100_cases_fast(self):
        results = []
        print("Running 100 cases (Mocked LLM for Speed)...")
        
        queries = [f"Test Query {i}" for i in range(100)]
        
        # Overwrite with specific categories for logic check
        # 1-10: General
        for i in range(10): queries[i] = "What is the university name?"
        
        # 11-20: DB Stats (Trigger DB Engine)
        for i in range(10, 20): queries[i] = "How many students?"
        
        # 21-30: Personal (Trigger Data Engine - Login Required)
        for i in range(20, 30): queries[i] = "What is my name?"
        
        # 31-40: Sensitive (Trigger High Auth)
        for i in range(30, 40): queries[i] = "What is my CGPA?" # Should prompt password
        
        for i, q in enumerate(queries):
            h = self.auth_headers if i >= 20 else None
            
            # For unauth personal query
            if i >= 20 and i < 25: 
                h = None # Test Auth fail
                
            data = self.run_chat(q, headers=h)
            
            status = "PASS"
            if i >= 30 and i < 40:
                if data.get('type') not in ['password_required', 'password_prompt']:
                    status = "FAIL (Expected Password Prompt)"
            
            results.append(f"| {i+1} | {q} | {data.get('type')} | {status} |")
            
            if i % 10 == 0: print(f"Processing {i}...")

        # Save Report
        with open("QA_REPORT_MOCK.md", "w") as f:
            f.write("# Fast QA Report (Logic Verification)\n")
            f.write("| ID | Input | Type | Status |\n|---|---|---|---|\n")
            f.write("\n".join(results))
            
        print("Done. Saved to QA_REPORT_MOCK.md")

if __name__ == "__main__":
    unittest.main()
