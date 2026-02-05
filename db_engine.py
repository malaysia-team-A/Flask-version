"""
Database Engine - MongoDB Atlas Connection Manager
Handles all MongoDB operations for the UCSI Chatbot
"""
import os
from typing import Optional, Dict, List, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Conditional import
try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
    HAS_PYMONGO = True
except ImportError:
    HAS_PYMONGO = False
    print("Warning: pymongo not installed. Run: pip install pymongo")

class DatabaseEngine:
    def __init__(self):
        self.client = None
        self.db = None
        self.connected = False
        
        if HAS_PYMONGO:
            self._connect()
    
    def _connect(self):
        """Connect to MongoDB Atlas"""
        try:
            mongo_uri = os.getenv("MONGO_URI")
            if not mongo_uri:
                print("Warning: MONGO_URI not found in .env file")
                return
            
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            
            # Test connection
            self.client.admin.command('ping')
            
            # Get database name from URI or use default
            db_name = mongo_uri.split('/')[-1].split('?')[0] or 'ucsi_chatbot'
            self.db = self.client[db_name]
            
            self.connected = True
            print(f"✅ MongoDB Connected: {db_name}")
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"❌ MongoDB Connection Failed: {e}")
            self.connected = False
        except Exception as e:
            print(f"❌ MongoDB Error: {e}")
            self.connected = False
    
    # ===========================================
    # STUDENTS COLLECTION
    # ===========================================
    
    def get_student_by_number(self, student_number: str) -> Optional[Dict]:
        """Find student by student number"""
        if not self.connected:
            return None
        try:
            return self.db.students.find_one({"STUDENT_NUMBER": student_number})
        except Exception as e:
            print(f"DB Error: {e}")
            return None
    
    def get_student_by_name(self, name: str) -> Optional[Dict]:
        """Find student by name (case-insensitive)"""
        if not self.connected:
            return None
        try:
            return self.db.students.find_one({
                "STUDENT_NAME": {"$regex": f"^{name}$", "$options": "i"}
            })
        except Exception as e:
            print(f"DB Error: {e}")
            return None
    
    def get_all_students(self) -> List[Dict]:
        """Get all students"""
        if not self.connected:
            return []
        try:
            return list(self.db.students.find({}, {"_id": 0}))
        except Exception as e:
            print(f"DB Error: {e}")
            return []
    
    def get_student_stats(self) -> Dict:
        """Get student statistics"""
        if not self.connected:
            return {}
        try:
            total = self.db.students.count_documents({})
            
            # Gender distribution
            gender_pipeline = [
                {"$group": {"_id": "$GENDER", "count": {"$sum": 1}}}
            ]
            gender_stats = {doc["_id"]: doc["count"] for doc in self.db.students.aggregate(gender_pipeline)}
            
            # Nationality distribution
            nationality_pipeline = [
                {"$group": {"_id": "$NATIONALITY", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 10}
            ]
            nationalities = {doc["_id"]: doc["count"] for doc in self.db.students.aggregate(nationality_pipeline)}
            
            return {
                "total_students": total,
                "gender": gender_stats,
                "top_nationalities": nationalities
            }
        except Exception as e:
            print(f"DB Error: {e}")
            return {}
    
    # ===========================================
    # FEEDBACKS COLLECTION
    # ===========================================
    
    def save_feedback(self, feedback_data: Dict) -> bool:
        """Save user feedback"""
        if not self.connected:
            return False
        try:
            self.db.feedbacks.insert_one(feedback_data)
            return True
        except Exception as e:
            print(f"DB Error: {e}")
            return False
    
    def get_feedback_stats(self) -> Dict:
        """Get feedback statistics"""
        if not self.connected:
            return {"total": 0, "positive": 0, "negative": 0}
        try:
            total = self.db.feedbacks.count_documents({})
            positive = self.db.feedbacks.count_documents({"rating": "positive"})
            negative = self.db.feedbacks.count_documents({"rating": "negative"})
            return {"total": total, "positive": positive, "negative": negative}
        except Exception as e:
            print(f"DB Error: {e}")
            return {"total": 0, "positive": 0, "negative": 0}
    
    # ===========================================
    # UNANSWERED QUESTIONS COLLECTION
    # ===========================================
    
    def log_unanswered(self, question_data: Dict) -> bool:
        """Log unanswered question"""
        if not self.connected:
            return False
        try:
            self.db.unanswered.insert_one(question_data)
            return True
        except Exception as e:
            print(f"DB Error: {e}")
            return False
    
    def get_unanswered_questions(self, limit: int = 50) -> List[Dict]:
        """Get recent unanswered questions"""
        if not self.connected:
            return []
        try:
            return list(self.db.unanswered.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit))
        except Exception as e:
            print(f"DB Error: {e}")
            return []

# Singleton instance
db_engine = DatabaseEngine()

if __name__ == "__main__":
    if db_engine.connected:
        print("Database connection test successful!")
        print(f"Collections: {db_engine.db.list_collection_names()}")
    else:
        print("Database not connected. Check your .env file and MongoDB Atlas settings.")
