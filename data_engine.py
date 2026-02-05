"""
Data Engine - Student Data Access Layer
Handles Excel data loading and student verification
"""
import pandas as pd
import os

class DataEngine:
    def __init__(self, excel_path):
        self.excel_path = excel_path
        self.df = None
        self.load_data()

    def load_data(self):
        if os.path.exists(self.excel_path):
            try:
                self.df = pd.read_excel(self.excel_path)
                print(f"Data Loaded. Columns: {self.df.columns.tolist()}")
                # Standardize column names
                self.df.columns = [str(c).strip() for c in self.df.columns]
            except Exception as e:
                print(f"Error loading Excel: {e}")
                self.df = pd.DataFrame()
        else:
            print(f"File not found: {self.excel_path}")
            self.df = pd.DataFrame()

    def get_column_names(self):
        """Return available column names"""
        if self.df is None or self.df.empty:
            return []
        return self.df.columns.tolist()

    def verify_student(self, student_number, name):
        """
        Verify a student exists with matching student number and name
        Returns the student record if found, None otherwise
        """
        if self.df is None or self.df.empty:
            return None
        
        # Find columns that might be student number and name
        cols = [c.lower() for c in self.df.columns]
        
        # Try to find student number column
        student_num_col = None
        for col in self.df.columns:
            col_lower = col.lower()
            if 'student' in col_lower and ('number' in col_lower or 'no' in col_lower or 'id' in col_lower):
                student_num_col = col
                break
            if col_lower in ['studentno', 'student_no', 'student_id', 'studentid', 'id']:
                student_num_col = col
                break
        
        # Try to find name column
        name_col = None
        for col in self.df.columns:
            col_lower = col.lower()
            if 'name' in col_lower and 'nick' not in col_lower:
                name_col = col
                break
        
        if not student_num_col or not name_col:
            print(f"Could not find student number or name columns. Available: {self.df.columns.tolist()}")
            # Fallback: use first two columns
            if len(self.df.columns) >= 2:
                student_num_col = self.df.columns[0]
                name_col = self.df.columns[1]
            else:
                return None
        
        print(f"Using columns: StudentNum='{student_num_col}', Name='{name_col}'")
        
        # Search for matching student
        mask = (
            (self.df[student_num_col].astype(str).str.strip().str.lower() == str(student_number).strip().lower()) &
            (self.df[name_col].astype(str).str.strip().str.lower() == str(name).strip().lower())
        )
        
        matches = self.df[mask]
        
        if len(matches) > 0:
            # Return first match as dict
            student_data = matches.iloc[0].to_dict()
            return student_data
        
        return None

    def get_student_info(self, student_number):
        """Get a specific student's information by student number"""
        if self.df is None or self.df.empty:
            return None
        
        # Find student number column
        student_num_col = None
        for col in self.df.columns:
            col_lower = col.lower()
            if 'student' in col_lower and ('number' in col_lower or 'no' in col_lower or 'id' in col_lower):
                student_num_col = col
                break
            if col_lower in ['studentno', 'student_no', 'student_id', 'studentid', 'id']:
                student_num_col = col
                break
        
        if not student_num_col:
            student_num_col = self.df.columns[0]
        
        mask = self.df[student_num_col].astype(str).str.strip().str.lower() == str(student_number).strip().lower()
        matches = self.df[mask]
        
        if len(matches) > 0:
            return matches.iloc[0].to_dict()
        return None

    def get_summary_stats(self):
        """Get general statistics (non-sensitive)"""
        if self.df is None or self.df.empty:
            return {"error": "No data available"}
        
        stats = {
            "total_students": len(self.df),
            "columns": self.df.columns.tolist()
        }
        
        # Add gender breakdown if available
        for col in self.df.columns:
            if 'gender' in col.lower():
                stats["gender_breakdown"] = self.df[col].value_counts().to_dict()
                break
        
        # Add nationality breakdown if available
        for col in self.df.columns:
            if 'national' in col.lower():
                stats["nationality_breakdown"] = self.df[col].value_counts().to_dict()
                break
        
        return stats

    def search_students(self, query):
        """Search students (limited info for privacy)"""
        if self.df is None or self.df.empty:
            return []
        
        results = self.df[self.df.astype(str).apply(
            lambda x: x.str.contains(query, case=False, na=False)
        ).any(axis=1)]
        
        return results.head(5).to_dict(orient='records')


if __name__ == "__main__":
    engine = DataEngine("Chatbot_TestData.xlsx")
    print("\n=== Summary Stats ===")
    print(engine.get_summary_stats())
    print("\n=== Columns ===")
    print(engine.get_column_names())
