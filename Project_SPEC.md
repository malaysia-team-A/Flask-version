# 📋 Project Specification: UCSI AI Chatbot (Kai) v2.2

## 1. Introduction
본 문서는 UCSI 대학교 학생들을 위한 AI 챗봇 **"Kai"**의 기술 명세서입니다.  
버전 2.3에서는 핵심 AI 엔진을 **Google Gemini 2.0 Flash** (via Native SDK)로 업그레이드하여 속도와 정확성을 극대화했습니다. 불필요한 추상화 레이어(LangChain Wrapper)를 제거하고 **Google GenAI Python SDK**를 직접 통합하여 API 연결 안정성을 확보했습니다.

---

## 2. System Architecture

### 2.1 Tech Stack (기술 스택)
*   **Language**: Python 3.10+
*   **Web Framework**: Flask (RESTful API)
*   **LLM Engine**: **Google Gemini 2.0 Flash** (Native Integration)
    *   *Note*: 안정적인 API 호출을 위해 `google-genai` 최신 SDK 사용
*   **Vector DB**: FAISS (CPU Optimized)
*   **Database**: MongoDB Atlas (Student Data, Logs)
*   **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)
*   **Frontend**: HTML5, TailwindCSS, Vanilla JS

### 2.2 Core Modules
1.  **AI Engine (`ai_engine.py`)**
    *   **Intent Classification**: 사용자의 의도를 분석 (General vs Personal Data).
    *   **Native SDK**: LangChain 래퍼의 호환성 문제를 해결하기 위해 Google GenAI SDK를 직접 구현.
    *   **Optimized Prompting**: 모델이 데이터를 더 정확하게 참조하도록 프롬프트 구조 개선.

2.  **RAG Engine (`rag_engine.py`)**
    *   PDF, TXT, CSV 문서를 로드하여 Chunking 및 Vectorizing.
    *   질문과 가장 유사한 문서 조각(Context)을 검색하여 AI에게 제공.

3.  **Data Engine (`db_engine.py`)**
    *   MongoDB 연결 및 쿼리 최적화.
    *   성비, 국적별 통계 등을 위한 `Aggregation Pipeline` 구현 (대소문자 무시 로직 적용).

4.  **Security Module (`auth_utils.py`)**
    *   **Dual Authentication**: 성적 등 민감 정보 접근 시 비밀번호 재확인 강제.
    *   **JWT**: 세션 관리 및 토큰 기반 인증.

---

## 3. Functional Requirements

### 3.1 Chatbot Persona (Kai)
*   **Name**: Kai
*   **Role**: Smart & Energetic Student Assistant
*   **Behavior**:
    *   학교 관련 질문은 DB/RAG 데이터를 최우선으로 답변.
    *   일상적인 질문(인사, 유머 등)은 일반 지식으로 유연하게 대처.
    *   모르는 학교 정보에 대해서는 솔직하게 "정보가 없다"고 답변.

### 3.2 Key Features
*   **General Inquiry**: 장학금, 수강신청 기간, 캠퍼스 위치 등 (RAG 활용).
*   **Personal Data**: 학번, 이름, 학과, 담당 교수님 조회 (로그인 필요).
*   **Sensitive Data**: **GPA, CGPA, 성적표** 조회 (이중 인증 필요).
*   **Feedback System**: 답변에 대한 좋아요/싫어요 평가 및 관리자 분석.
*   **QA Automation**: 100개 이상의 테스트 케이스를 통한 자동 검증 시스템.

---

## 4. Database Schema (MongoDB)

### 4.1 Collection: `students` (or `UCSI`)
| Field | Type | Description |
| :--- | :--- | :--- |
| `student_number` | String | Unique ID |
| `name` | String | Full Name |
| `password` | String | Hashed or Plaintext (Legacy support) |
| `gender` | String | Male/Female (Case Insensitive) |
| `dob` | String | Date of Birth (Access Allowed) |
| `cgpa` | Float | **Protected (Dual Auth)** |

### 4.2 Collection: `feedbacks`
*   `user_message`, `ai_response`, `rating(positive/negative)`, `timestamp`

---

## 5. Deployment & Testing
*   **Environment**: Windows (Local Dev) / Linux (Production)
*   **Testing Tool**: `qa_runner_100.py` (Full System Test)
*   **API Keys**: Managed via `.env` (GOOGLE_API_KEY mandatory for v2.2 performance)
