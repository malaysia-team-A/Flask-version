import os
import json

class LearningEngine:
    def __init__(self, log_path="data/unanswered_log.json"):
        self.log_path = log_path

    def log_issue(self, question, issue_type, confidence, response=""):
        pass

    def get_unanswered_questions(self):
        return []

learning_engine = LearningEngine()
