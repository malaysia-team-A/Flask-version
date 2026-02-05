"""
Learning Engine - Self-Learning & Improvement System
Logs unanswered questions and low-confidence responses for future training
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

LEARNING_LOG_FILE = "unanswered_log.json"

class LearningEngine:
    def __init__(self, log_file: str = LEARNING_LOG_FILE):
        self.log_file = log_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Ensure the learning log file exists"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump({"unanswered": [], "low_confidence": [], "stats": {"total_issues": 0}}, f)
    
    def _load_data(self) -> Dict:
        """Load learning data"""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"unanswered": [], "low_confidence": [], "stats": {"total_issues": 0}}
    
    def _save_data(self, data: Dict):
        """Save learning data"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def log_issue(self, 
                  question: str, 
                  issue_type: str,  # "unanswered" or "low_confidence"
                  confidence: float = 0.0,
                  response: Optional[str] = None):
        """
        Log an issue for future learning
        """
        try:
            data = self._load_data()
            
            entry = {
                "id": data["stats"]["total_issues"] + 1,
                "timestamp": datetime.now().isoformat(),
                "question": question,
                "confidence": confidence,
                "response": response
            }
            
            if issue_type == "unanswered":
                data["unanswered"].append(entry)
            elif issue_type == "low_confidence":
                data["low_confidence"].append(entry)
            
            data["stats"]["total_issues"] += 1
            self._save_data(data)
            return True
            
        except Exception as e:
            print(f"Error logging learning issue: {e}")
            return False

    def get_unanswered_questions(self) -> List[Dict]:
        """Get list of unanswered questions"""
        data = self._load_data()
        return data.get("unanswered", [])

    def get_low_confidence_responses(self) -> List[Dict]:
        """Get list of low confidence responses"""
        data = self._load_data()
        return data.get("low_confidence", [])

# Singleton
learning_engine = LearningEngine()
