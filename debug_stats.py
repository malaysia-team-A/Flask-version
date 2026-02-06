from data_engine import DataEngine
import json

d = DataEngine()
stats = d.get_summary_stats()
print("\n--- RAW STATS FROM DB ---")
print(json.dumps(stats, indent=2, default=str))

# Also check one student to see actual field names
print("\n--- SAMPLE STUDENT ---")
students = d.db.get_all_students()
if students:
    print(json.dumps(students[0], indent=2, default=str))
else:
    print("No students found.")
