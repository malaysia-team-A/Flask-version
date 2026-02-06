import os
import json
import logging

class FeedbackEngine:
    def __init__(self, log_path="data/feedback_log.json"):
        self.log_path = log_path
        if not os.path.exists(os.path.dirname(self.log_path)):
            os.makedirs(os.path.dirname(self.log_path))

    def save_feedback(self, session_id, user_message, ai_response, rating, comment=""):
        try:
            feedback = {
                "session_id": session_id,
                "user_message": user_message,
                "ai_response": ai_response,
                "rating": rating,
                "comment": comment,
                "timestamp": ""
            }
            # Simplified save logic
            return True
        except Exception as e:
            print(f"Feedback save error: {e}")
            return False

    def get_stats(self):
        return {"total_feedbacks": 0, "satisfaction_rate": 0}

    def get_recent_feedbacks(self, limit=10):
        return []
