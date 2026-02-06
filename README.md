# 🎓 UCSI University AI Chatbot (Kai)

![Version](https://img.shields.io/badge/version-2.2-blue.svg) ![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg) ![Gemini](https://img.shields.io/badge/AI-Gemini%202.0%20Flash-4285F4.svg)

> **UCSI 대학교 학생들을 위한 차세대 지능형 학사 도우미 "Kai"**  
> Google **Gemini 2.0 Flash**의 강력한 성능, RAG(검색 증강 생성) 기술, 그리고 **이중 보안 시스템**이 결합된 하이브리드 솔루션입니다.

---

## 🌟 프로젝트 개요
이 프로젝트는 단순한 Q&A 봇을 넘어, **실시간 데이터 연동**과 **문맥 인식**이 가능한 AI 에이전트입니다. 학생들은 복잡한 학사 행정 시스템에 접속하는 대신, 자연어로 질문하여 필요한 정보를 즉시 얻을 수 있습니다.

### 핵심 차별점
1.  **초고속 AI 엔진**: **Gemini 2.0 Flash**를 탑재하여 로컬 LLM 대비 압도적인 속도와 정확성을 자랑합니다.
2.  **할루시네이션 최소화**: RAG 기술을 통해 실제 학교 규정 문서(PDF)에 기반한 답변만 제공합니다.
3.  **개인화 & 보안**: 본인의 성적, 재무 상태 등 민감한 정보는 **이중 인증(Dual Auth)**을 거쳐야만 조회 가능합니다.
4.  **자율 판단**: DB에 없는 일반 상식 질문(색깔, 농담 등)에도 유연하게 대처합니다.

---

## 🚀 주요 기능 (Key Features)

| 기능 | 설명 |
| :--- | :--- |
| **🤖 AI 챗봇 (Kai)** | `Gemini 2.0 Flash` 기반의 똑똑하고 빠른 대화 엔진 |
| **🔎 RAG 검색** | 교내 정책 문서, 핸드북 등을 벡터 DB화하여 정확한 근거 제시 |
| **📊 학사 데이터 조회** | MongoDB Atlas 연동을 통한 실시간 학생 정보(GPA, 학적) 조회 |
| **🔐 보안 인증** | JWT 기반 세션 관리 및 **성적 조회 시 비밀번호 재확인** 절차 |
| **🧪 자동화 테스트** | 100가지 시나리오를 검증하는 QA 자동화 스크립트 내장 |
| **🗣️ 피드백 루프** | 답변 만족도(좋아요/싫어요) 수집을 통한 지속적인 품질 개선 |

---

## 🛠 아키텍처 및 기술 스택

### 백엔드 (Backend)
*   **Flask (Python)**: REST API 서버
*   **LangChain**: LLM 오케스트레이션 및 RAG 파이프라인 구축
*   **MongoDB Atlas**: 클라우드 NoSQL 데이터베이스

### AI & 데이터 (AI & Data)
*   **Google Gemini 2.0 Flash**: 메인 추론 엔진 (Cloud LLM)
*   **FAISS**: 고속 벡터 유사도 검색 엔진
*   **SentenceTransformers**: `all-MiniLM-L6-v2` 임베딩 모델

### 프론트엔드 (Frontend)
*   Vanilla JS / HTML5 / CSS3
*   **Glassmorphism Design**: 현대적이고 깔끔한 UI/UX 적용

---

## 📂 프로젝트 구조

```bash
project_MALAYSIA/
├── ai_engine.py        # 🧠 AI 엔진 (Gemini 2.0 Flash + LangChain)
├── rag_engine.py       # 📚 RAG 엔진 (문서 수집, FAISS 인덱싱)
├── db_engine.py        # 🗄️ DB 엔진 (MongoDB 연결, 통계)
├── data_engine.py      # ⚙️ 데이터 처리 계층
├── auth_utils.py       # 🔐 보안 모듈 (JWT, 이중 인증)
├── qa_runner_100.py    # 🧪 QA 자동화 테스트 스크립트
├── main.py             # 🚀 Flask 메인 서버
├── admin/              # 👨‍💼 관리자 대시보드
├── UI_hompage/         # 🎨 사용자 채팅 웹 인터페이스 (Kai)
└── knowledge_base/     # 📖 RAG 참조용 문서 저장소
```

---

## ⚡ 빠른 시작 (Quick Start)

상세한 설치 방법은 [SETUP_GUIDE.md](SETUP_GUIDE.md) 파일을 참고하세요.

### 1. 환경 설정
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. API 키 설정 (.env)
```ini
GOOGLE_API_KEY=AIzaSy... (당신의 Gemini API 키)
MONGO_URI=mongodb+srv://...
```

### 3. 서버 실행
```bash
python main.py
```

---

## 📝 라이선스 및 정보
*   **Author**: UCSI University AI Dev Team
*   **Status**: Production Ready (v2.2)
*   **Engine**: Powered by Google Gemini
