# 🧪 Testing Guide for UCSI Chatbot (Kai)

This document outlines the testing procedures and automated scripts available to verify the integrity of the chatbot system.

## 📂 Available Test Scripts

We have provided three levels of testing scripts in the project root:

| Script Filename | Purpose | Duration | Focus |
| :--- | :--- | :--- | :--- |
| `fast_qa.py` | **Sanity Check** | ~10 sec | Connects to DB, Logs in, Runs 5 basic queries. |
| `qa_runner_100_mock.py` | **Logic Verification** | ~5 sec | Runs **100 test cases** with the AI mocked. Verifies Auth flow, DB routing, and Security logic instantly. |
| `qa_runner_100.py` | **Full AI Validation** | ~15 min | Runs **100 test cases** with the **REAL AI engine**. Generates a detailed `QA_REPORT_100.md`. |

---

## 🚀 How to Run Tests

### 1. Logic Verification (Recommended First)
Run this to ensure the "Brain" logic (Authentication, Database, Routing) is working correctly without waiting for the AI model.

```powershell
python qa_runner_100_mock.py
```
*   **Check Output**: Open `QA_REPORT_MOCK.md` to spot any logic failures.

### 2. Full System Test (End-to-End)
Run this to verify the quality of AI responses.

```powershell
python qa_runner_100.py
```
*   **Note**: This takes time as it interacts with the local Ollama model 100 times.
*   **Result**: A file named `QA_REPORT_100.md` will be generated with Pass/Fail statistics.

---

## ✅ Test Categories Covered

The 100 test cases cover the following scenarios:

1.  **Persona & Chit-Chat**: Verifying identity ("Who are you?", "Kai") and handling small talk.
2.  **RAG / General Knowledge**: Checking if fallback to general knowledge works when DB is empty.
3.  **Database Statistics**: "Gender ratio", "Total students", "Nationality".
4.  **Authentication**: Guest vs Student access control.
5.  **Personal Data**: "My name", "My ID", "My DOB" (Requires valid token).
6.  **High Security (Dual Auth)**: "My CGPA", "My Grades" (Must trigger password prompt).
7.  **Edge Cases**: Empty strings, XSS attempts `<script>`, SQL Injection attempts.
8.  **Feedback Loop**: API stability for submitting user feedback.

---

## 🛠️ FAQ

**Q: Why do some tests fail in `qa_runner_100.py`?**
A: AI responses can vary. The test script looks for keywords. If the AI answers correctly but uses different words (e.g., "Total: 50" vs "There are 50 students"), it might be marked as a false negative. Review the report manually.

**Q: "Password Required" tests failed?**
A: Ensure you have `SECRET_KEY` set in `.env` and the `auth_utils.py` is configured to allow legacy passwords if your test data is old.
