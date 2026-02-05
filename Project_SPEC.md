# UCSI University Chatbot - 프로젝트 명세서

## 프로젝트 개요

| 항목 | 내용 |
|------|------|
| **프로젝트명** | UCSI University AI Chatbot |
| **목적** | 학생 개인정보 보호와 RAG 기반 질의응답 |
| **버전** | 2.1.0 |
| **최종 업데이트** | 2026-02-05 |

---

## 기술 스택

### Backend
- **Language**: Python 3.13+
- **Framework**: Flask
- **Data Processing**: Pandas, Openpyxl
- **Database**: MongoDB (예정)

### AI/LLM
- **Engine**: Ollama (Local LLM)
- **Model**: gemma3:12b (또는 llama3.2:3b)
- **RAG**: FAISS + Sentence-Transformers

### Frontend
- **HTML5** + **Tailwind CSS** (CDN)
- **JavaScript** (Vanilla)
- **Icons**: Material Icons (CDN)

### 인증
- **방식**: Session-based (Student Number + Name)
- **보안**: 본인 정보만 접근 가능

---

## 파일 구조

```
project_MALAYSIA/
├── main.py                 # Flask 메인 서버
├── ai_engine.py            # AI 엔진 (Ollama 연결, 의도분류)
├── data_engine.py          # 데이터 엔진 (Excel 처리)
├── rag_engine.py           # RAG 엔진 (FAISS 기반)
├── feedback_engine.py      # 피드백 수집
├── learning_engine.py      # 미답변 질문 로깅
├── requirements.txt        # Python 의존성 (버전 고정)
│
├── knowledge_base/         # RAG 문서 및 인덱스
├── admin/                  # 관리자 페이지
│   └── admin.html
├── UI_hompage/
│   └── code_hompage.html   # 메인 웹 UI
│
├── Chatbot_TestData.xlsx   # 학생 데이터
└── README.md               # 인수인계 문서
```

---

## 핵심 기능

### 1. AI 의도 분류 (Intent Classification)
LLM이 사용자 메시지를 분석하여 2가지 의도로 분류:
- `GENERAL`: 일반 대화/통계 (인증 불필요)
- `PERSONAL_DATA`: 개인 정보 요청 (인증 필요)

### 2. 개인정보 보호
- 개인정보 요청 → 로그인 필수
- 로그인 후에도 **본인 정보만** 접근 가능
- 타인 정보 접근 시도 → 차단

### 3. RAG (문서 기반 검색)
- FAISS 벡터 DB 사용
- Admin 패널에서 PDF/TXT 업로드 가능

---

## API 엔드포인트

| Method | Path | 설명 | 인증 |
|--------|------|------|------|
| GET | `/` | 메인 페이지 | - |
| GET | `/admin` | 관리자 대시보드 | PW필요 |
| POST | `/api/verify` | 학생 인증 | - |
| POST | `/api/chat` | 챗봇 대화 | 선택적 |
| POST | `/api/logout` | 로그아웃 | - |
| POST | `/api/feedback` | 피드백 제출 | - |
| GET | `/api/admin/stats` | 통계 조회 | - |
| POST | `/api/admin/upload` | 문서 업로드 | - |

---

## 실행 방법

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. Ollama 설치 및 모델 다운로드
```bash
# https://ollama.com 에서 설치 후
ollama pull gemma3:12b
```

### 3. 서버 시작
```bash
python main.py
```

### 4. 브라우저 접속
```
http://localhost:8000
```

---

## 변경 이력

| 날짜 | 버전 | 변경 내용 |
|------|------|----------|
| 2026-02-05 | 2.1.0 | Flask 전환, FAISS RAG, requirements 버전 고정 |
| 2026-02-04 | 2.0.0 | Feedback, Self-Learning, Admin Panel 추가 |
| 2026-02-04 | 1.0.0 | 로컬 LLM 전환, 의도분류 추가 |
