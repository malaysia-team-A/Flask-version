# UCSI University AI 챗봇 - 기술명세서 (v3.0)

## 1. 프로젝트 개요

| 항목 | 내용 |
|------|------|
| **프로젝트명** | UCSI University AI Chatbot |
| **목적** | 학생 개인정보(성적, 등록상태) 및 대학 일반정보 조회를 위한 AI 어시스턴트 |
| **버전** | 3.0.0 (Hybrid RAG + Dual Auth) |
| **최종 수정** | 2026-02-05 |

---

## 2. 시스템 아키텍처

### 2.1 핵심 구성요소

| 구성요소 | 기술 | 역할 |
|----------|------|------|
| **오케스트레이터** | LangChain | 사용자 의도 분류 및 데이터 소스 라우팅 |
| **LLM (대규모 언어모델)** | Ollama (로컬) | 자연어 생성 및 의도 분류 (gemma3:12b) |
| **벡터 데이터베이스** | FAISS | 대학 문서(PDF, TXT) 임베딩 저장 및 검색 |
| **문서 데이터베이스** | MongoDB Atlas | 학생 정보, 성적, 피드백 저장 |

### 2.2 데이터 흐름

```
[사용자 질문]
     ↓
[LangChain 의도 분류]
     ↓
┌────────────────────┬────────────────────┐
│   GENERAL 의도     │   PERSONAL_DATA 의도 │
│   (일반 질문)       │   (개인정보 질문)     │
└────────┬───────────┴───────────┬────────┘
         ↓                       ↓
   [FAISS RAG 검색]        [MongoDB 조회]
         ↓                       ↓
         └───────────┬───────────┘
                     ↓
              [LLM 응답 생성]
                     ↓
              [사용자에게 응답]
```

---

## 3. 인증 체계

### 3.1 Level 1: 기본 로그인 (JWT)
- **방식**: 학번 + 이름으로 로그인
- **토큰**: JWT Bearer Token 발급
- **접근 가능 정보**: 기본 프로필 (이름, 학번, 전공)

### 3.2 Level 2: 이중 인증 (Dual Auth)
- **트리거**: 성적(Grades) 관련 질문
- **방식**: 비밀번호 재입력 요구
- **세션**: 10분간 유효

---

## 4. API 명세

| 엔드포인트 | 메소드 | 설명 | 인증 |
|------------|--------|------|------|
| `/api/login` | POST | 로그인 (JWT 발급) | 없음 |
| `/api/verify_password` | POST | 비밀번호 검증 (Dual Auth) | JWT 필요 |
| `/api/chat` | POST | 챗봇 대화 | JWT (선택) |
| `/api/feedback` | POST | 피드백 제출 | 없음 |
| `/api/admin/stats` | GET | 관리자 통계 | 없음 (내부용) |
| `/api/admin/upload` | POST | 지식베이스 문서 업로드 | 없음 (내부용) |

---

## 5. 기술 스택

| 분류 | 기술 |
|------|------|
| **백엔드** | Python, Flask |
| **AI 프레임워크** | LangChain, LangChain-Ollama |
| **LLM** | Ollama (gemma3:12b) |
| **벡터 DB** | FAISS (CPU 버전) |
| **임베딩** | Sentence-Transformers (all-MiniLM-L6-v2) |
| **데이터베이스** | MongoDB Atlas |
| **인증** | PyJWT, Werkzeug |
| **프론트엔드** | HTML5, Vanilla JS |

---

## 6. 보안 기능

1. **로그 익명화**: 모든 시스템 로그에서 학생 이름/학번 마스킹
2. **이중 인증**: 민감한 성적 정보 조회 시 비밀번호 재확인
3. **접근 제어**: 본인 데이터만 조회 가능 (타인 정보 접근 불가)

---

## 7. 핵심 파일 구조

```
project_MALAYSIA/
├── main.py              # Flask 서버 & API 엔드포인트
├── ai_engine.py         # LangChain 오케스트레이션 & 의도분류
├── rag_engine.py        # FAISS 벡터 검색 로직
├── db_engine.py         # MongoDB 연결 및 쿼리
├── data_engine.py       # 데이터 접근 레이어 (추상화)
├── auth_utils.py        # JWT & 비밀번호 해싱
├── feedback_engine.py   # 피드백 수집
├── learning_engine.py   # 미답변 질문 로깅
├── logging_utils.py     # 익명화 로깅
├── knowledge_base/      # FAISS 인덱스 & 원본 문서
├── UI_hompage/          # 프론트엔드 정적 파일
└── admin/               # 관리자 대시보드
```
