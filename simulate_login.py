import sys
import traceback

print("Importing modules...")
try:
    from data_engine import DataEngine
    from auth_utils import create_access_token
    import logging_utils
    
    print("Initializing DataEngine...")
    data_engine = DataEngine()
    
    # Test Data
    STUDENT_NUMBER = "5004273354"
    NAME = "Vicky Yiran"
    
    print(f"Simulating Login for {NAME} ({STUDENT_NUMBER})...")
    
    # 1. Verify
    print("Calling verify_student...")
    is_valid, student_data, msg = data_engine.verify_student(STUDENT_NUMBER, NAME)
    
    print(f"Verification Result: Valid={is_valid}, Msg='{msg}'")
    
    if is_valid:
        print("Student Data:", student_data)
        
        # 2. Token
        print("Creating Token...")
        token = create_access_token({
            "student_number": STUDENT_NUMBER,
            "name": NAME,
            "role": "student"
        })
        print(f"Token created: {token[:20]}...")
        
        # 3. Log
        print("Logging audit...")
        logging_utils.log_audit("LOGIN", f"{NAME} ({STUDENT_NUMBER})", "Login successful")
        print("Login Simulation Complete: SUCCESS")
    else:
        print("Login Simulation Complete: FAILED (Expected if user not in DB)")

except Exception:
    print("\n❌ CRITICAL CRASH DURING SIMULATION:")
    traceback.print_exc()
