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
        self.student_collection_name = "UCSI"  # Default
        
        if HAS_PYMONGO:
            self._connect()
    
    def _connect(self):
        """Establish connection to MongoDB Atlas with timeout"""
        try:
            # Load environment variables
            if not os.getenv("MONGO_URI"):
                load_dotenv()
            if not os.getenv("MONGO_URI"):
                load_dotenv()
            
            uri = os.getenv("MONGO_URI")
            if not uri:
                print("Error: MONGO_URI not found in .env")
                return

            # Add timeout to prevent hanging
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            
            # Verify connection
            self.client.admin.command('ping')
            
            # Get Database
            db_name = uri.split('/')[-1].split('?')[0] or "UCSI_DB"
            self.db = self.client[db_name]
            self.connected = True
            print(f"✅ Successfully connected to MongoDB: {db_name}")

            # Smart detection of Student Collection
            try:
                colls = self.db.list_collection_names()
                candidates = ["UCSI", "students", "Students", "UCSI_STUDENTS"]
                found = False
                # First check if default candidates exist
                for c in candidates:
                    if c in colls:
                        self.student_collection_name = c
                        found = True
                        break
                
                # If not found, look for any collection with 'student' in name
                if not found:
                    for c in colls:
                        if "student" in c.lower() or "ucsi" in c.lower():
                            self.student_collection_name = c
                            found = True
                            print(f"DEBUG: Auto-detected student collection: {c}")
                            break
                            
                # Validate by checking if it has STUDENT_NUMBER
                if found or colls:
                    target = self.student_collection_name if found else colls[0]
                    sample = self.db[target].find_one()
                    if sample:
                        print(f"DEBUG: Using collection '{target}' for student data.")
                        self.student_collection_name = target
            except Exception as e:
                print(f"Warning: Could not auto-detect collections: {e}")
            
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            self.connected = False
    
    @property
    def student_coll(self):
        """Helper to get the student collection object"""
        if self.db is not None:
            return self.db[self.student_collection_name]
        return None

    # ===========================================
    # STUDENTS COLLECTION
    # ===========================================
    
    def get_student_by_number(self, student_number: str) -> Optional[Dict]:
        """Find student by student number (handles string and int)"""
        if self.student_coll is None or not self.connected:
            return None
        
        try:
            # Try string
            student = self.student_coll.find_one({"STUDENT_NUMBER": str(student_number)})
            if student: return student
            
            # Try int
            if str(student_number).isdigit():
                student = self.student_coll.find_one({"STUDENT_NUMBER": int(student_number)})
                if student: return student
                
            # Try fuzzy field names if standard query failed
            id_fields = ["student_number", "StudentNumber", "student_id", "id", "ID"]
            for field in id_fields:
                s = self.student_coll.find_one({field: str(student_number)})
                if s: return s
                if str(student_number).isdigit():
                    s = self.student_coll.find_one({field: int(student_number)})
                    if s: return s
                    
            return None
        except Exception as e:
            print(f"DB Error: {e}")
            return None
    
    def get_student_by_name(self, name: str) -> Optional[Dict]:
        """Find student by name (case-insensitive)"""
        if self.student_coll is None or not self.connected:
            return None
        try:
            # Try standard field
            res = self.student_coll.find_one({
                "STUDENT_NAME": {"$regex": f"^{name}$", "$options": "i"}
            })
            if res: return res
            
            # Try common variations
            name_fields = ["name", "Name", "StudentName", "full_name"]
            for field in name_fields:
                res = self.student_coll.find_one({
                    field: {"$regex": f"^{name}$", "$options": "i"}
                })
                if res: return res
            return None
        except Exception as e:
            print(f"DB Error: {e}")
            return None
    
    def get_all_students(self) -> List[Dict]:
        """Get all students"""
        if self.student_coll is None or not self.connected:
            return []
        try:
            return list(self.student_coll.find({}, {"_id": 0}))
        except Exception as e:
            print(f"DB Error: {e}")
            return []
    
    def get_student_stats(self) -> Dict:
        """Get student statistics"""
        if self.student_coll is None or not self.connected:
            return {}
        try:
            total = self.student_coll.count_documents({})
            
            # Gender distribution
            gender_pipeline = [
                {"$group": {"_id": "$GENDER", "count": {"$sum": 1}}}
            ]
            gender_stats = {str(doc.get("_id", "Unknown")): doc["count"] for doc in self.student_coll.aggregate(gender_pipeline)}
            
            # Nationality distribution
            nationality_pipeline = [
                {"$group": {"_id": "$NATIONALITY", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 10}
            ]
            nationalities = {str(doc.get("_id", "Unknown")): doc["count"] for doc in self.student_coll.aggregate(nationality_pipeline)}
            
            return {
                "total_students": total,
                "gender": gender_stats,
                "top_nationalities": nationalities
            }
        except Exception as e:
            print(f"DB Error: {e}")
            return {}
    
    # ===========================================
    # FEEDBACKS & LOGS (Using separate collections)
    # ===========================================
    
    def save_feedback(self, feedback_data: Dict) -> bool:
        if self.db is None or not self.connected: return False
        try:
            self.db.feedbacks.insert_one(feedback_data)
            return True
        except: return False

    def get_feedback_stats(self) -> Dict:
        if self.db is None or not self.connected: return {"total": 0}
        try:
            return {
                "total": self.db.feedbacks.count_documents({}),
                "positive": self.db.feedbacks.count_documents({"rating": "positive"}),
                "negative": self.db.feedbacks.count_documents({"rating": "negative"})
            }
        except: return {"total": 0}

    def log_unanswered(self, question_data: Dict) -> bool:
        if self.db is None or not self.connected: return False
        try:
            self.db.unanswered.insert_one(question_data)
            return True
        except: return False
    
    def get_unanswered_questions(self, limit: int = 50) -> List[Dict]:
        if self.db is None or not self.connected: return []
        try:
            return list(self.db.unanswered.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit))
        except: return []

# Singleton instance
db_engine = DatabaseEngine()

if __name__ == "__main__":
    if db_engine.connected:
        print("Database connection test successful!")
        print(f"Collections: {db_engine.db.list_collection_names()}")
    else:
        print("Database not connected. Check your .env file and MongoDB Atlas settings.")
