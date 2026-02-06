# 프로젝트 인수인계서 (Handover Document)

**작성일**: 2026-02-06
**프로젝트**: UCSI University AI Chatbot Project
**상태**: MVP 완성 및 UI 최적화 완료

---

## 1. 프로젝트 개요 (Overview)
본 프로젝트는 **Flask** 백엔드와 **Google Gemini AI**를 기반으로 한 대학 학사 행정 챗봇 시스템입니다. 학생들은 자연어로 학사 정보를 문의할 수 있으며, RAG(검색 증강 생성) 기술을 통해 정확한 학칙 및 행정 정보를 제공받습니다. 또한 성적 등 민감 정보는 이중 인증을 통해 안전하게 보호됩니다.

## 2. 핵심 성과 (Key Achievements)

1.  **핵심 인프라 구축**: Flask(서버), MongoDB(DB), Gemini AI(지능형 엔진) 연동 완료.
2.  **RAG 지식 검색 시스템**: 대학 관련 문서 및 데이터를 기반으로 할루시네이션(거짓 답변)을 최소화한 정확한 답변 제공.
3.  **이중 보안 시스템 (Dual Auth)**: JWT 토큰 로그인 + 2차 비밀번호 입력을 통한 성적 조회 보안 강화.
4.  **Premium UI/UX**: Glassmorphism 디자인, 모바일 풀스크린 반응형, 자연스러운 애니메이션(`fadeInUp`) 적용.
5.  **비용 및 성능 최적화**: AI 호출 구조를 단일 호출(Single-Call)로 개선하여 비용 절감 및 응답 속도 향상.

---

## 3. UI/UX 주요 기능 (Key Features)

*   **스마트 추천 질문 (Smart Suggestions)**: AI가 답변과 함께 연관된 질문 버튼(예: "✨ 장학금 정보?")을 자동으로 제안합니다.
*   **반응형 인터페이스**: 데스크탑에서는 우측 하단 위젯으로, 모바일에서는 앱처럼 전체 화면으로 작동합니다.
*   **보안 아일랜드 (Security Island)**: 채팅창 내부의 Floating Glass UI를 통해 현재 보안 상태(잠금/해제)를 직관적으로 표시합니다.
*   **감성적 디테일**: 'Inter' 폰트 적용, 부드러운 등장 애니메이션, 타이핑 효과 등 프리미엄 사용자 경험 제공.

---

## 4. 실행 및 테스트 (Execution Guide)

### 필수 요구 사항
*   Python 3.9+
*   MongoDB Atlas 계정 (또는 로컬 MongoDB)
*   Google Gemini API Key

### 설치 및 실행
1.  **패키지 설치**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **서버 실행**:
    ```bash
    python main.py
    ```
    또는 `start_chatbot.bat` 파일을 더블 클릭하세요.

### 기능 테스트 시나리오
1.  **일반 대화**: "컴퓨터 공학과는 어떤 곳이야?" → 자연스러운 답변과 추천 질문 버튼 확인.
2.  **성적 조회 (보안 테스트)**:
    *   "내 성적 보여줘" 입력.
    *   로그인 버튼 클릭 → 학번/이름 입력 (예: `5004273609` / 데이터베이스 내 학생).
    *   보안 패널의 **UNLOCK** 클릭 → 비밀번호 입력.
    *   잠금 해제 후 성적 데이터 표시 확인.

---

## 5. 프로젝트 구조 (File Structure)

*   `main.py`: Flask 웹 서버 메인 진입점.
*   `ai_engine.py`: Google Gemini API 연동 및 프롬프트 처리 로직.
*   `rag_engine.py`: 학교 관련 문서 검색 및 RAG 로직.
*   `db_engine.py` / `data_engine.py`: MongoDB 데이터 핸들링.
*   `UI_hompage/code_hompage.html`: 메인 프론트엔드 파일 (HTML/JS/Tailwind).
*   `requirements.txt`: 프로젝트 의존성 목록.

---

## 6. 문제 해결 (Troubleshooting)
*   **`ModuleNotFoundError: No module named 'jwt'`**:
    *   `pip install pyjwt` 명령어로 모듈을 재설치하세요.
*   **서버 실행 즉시 종료**:
    *   `.env` 파일에 `GOOGLE_API_KEY`와 `MONGO_URI`가 올바르게 설정되었는지 확인하세요.
*   **AI 응답 없음**:
    *   API 할당량(Quota) 문제일 수 있습니다. 잠시 후 재시도하거나 API 키를 점검하세요.

---
**Note**: 이 문서는 프로젝트의 최신 상태(v2.0 Premium UI 적용)를 기준으로 작성되었습니다. 기존의 임시 파일들은 정리되었습니다.
