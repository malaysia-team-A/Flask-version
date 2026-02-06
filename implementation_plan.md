# Implementation Plan - Security & Cleanup

## Goal
Address security risks and inconsistencies identified during the codebase audit (v2.3).

## User Review Required
> [!WARNING]
> This plan removes the hardcoded backdoor password ("password123"). If any legacy systems or dev tests rely on this, they will break.

## Proposed Changes

### 1. Security Hardening
#### [MODIFY] [auth_utils.py](file:///c:/Users/leejb/Desktop/project_MALAYSIA/auth_utils.py)
- **Remove**: Hardcoded `password123` check in `verify_password`.
- **Reason**: Critical security risk.

### 2. Logging Cleanup
#### [MODIFY] [main.py](file:///c:/Users/leejb/Desktop/project_MALAYSIA/main.py)
- **Update**: Startup log message from "LangChain Model" to "Google GenAI Model (Native)".
- **Reason**: Reduces confusion about the underlying architecture.

## Verification Plan

### Automated Tests
- Run `qa_runner_100.py` to ensure the chatbot still responds to general queries (proving `main.py` and `ai_engine.py` are healthy).

### Manual Verification
- **Login Test**: Attempt to verify identity with a real student ID/Name (should succeed).
- **Backdoor Test**: Attempt to verify identity or high-security mode using "password123" (should FAIL).
