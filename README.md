# 📋 UCSI University Chatbot - 프로젝트 인수인계서

## 📌 프로젝트 개요

**프로젝트명**: UCSI University AI Chatbot  
**목적**: 대학교 학생들이 개인 정보를 안전하게 조회할 수 있는 AI 챗봇  
**버전**: 2.0.0  
**최종 업데이트**: 2026-02-04

### 주요 특징:
- 🤖 로컬 LLM (Ollama)을 사용한 무료 AI 응답
- 🧠 LLM 기반 의도 분류 (Intent Classification)
- 🔐 개인정보 보호 (본인 정보만 접근 가능)
- 👤 Student Number + Name 기반 인증
- 🎨 깔끔한 UI/UX (Tailwind CSS)

---

## 🛠️ 기술 스택 (Tech Stack)

### Backend
| 기술 | 버전 | 용도 |
|------|------|------|
| **Python** | 3.10+ | 메인 프로그래밍 언어 |
| **Flask** | 3.0+ | Web Framework |
| **Pandas** | 2.0+ | Excel 데이터 처리 |
| **Openpyxl** | 3.1+ | .xlsx 파일 읽기 |
| **FAISS** | Facebook AI | 고성능 벡터 검색 (Lightweight) |

### AI/LLM
| 기술 | 버전 | 용도 |
|------|------|------|
| **Ollama** | 최신 | 로컬 LLM 실행 엔진 |
| **gemma3:12b** | 12B | AI 모델 (권장) |
| **llama3.2:3b** | 3B | AI 모델 (경량 대안) |

### Frontend
| 기술 | 용도 |
|------|------|
| **HTML5** | 페이지 구조 |
| **Tailwind CSS** | 스타일링 (CDN) |
| **JavaScript (Vanilla)** | 클라이언트 로직 |
| **Material Icons** | 아이콘 (CDN) |

### 인증/보안
| 기술 | 용도 |
|------|------|
| **Session-based Auth** | 세션 기반 인증 |
| **Student Number + Name** | 본인 확인 |

---

## 📁 파일 구조

```
project_MALAYSIA/
├── main.py                 # 🚀 메인 서버 (Flask)
├── ai_engine.py            # 🤖 AI 엔진 (Ollama 연결, 의도분류)
├── data_engine.py          # 📊 데이터 엔진 (Excel 처리)
├── feedback_engine.py      # 👍 피드백 엔진
├── learning_engine.py      # 🧠 셀프러닝 엔진
├── rag_engine.py           # 📚 RAG 엔진 (FAISS 기반)
├── knowledge_base/         # 📁 RAG 문서 및 인덱스 저장
├── admin/                  # 🛠️ 관리자 페이지
│   └── admin.html
├── UI_hompage/             # 🌐 프론트엔드
│   └── code_hompage.html
├── requirements.txt        # 📦 Python 의존성
├── README.md               # 📖 이 문서
└── Chatbot_TestData.xlsx   # 📋 학생 데이터
```

---

## ⚙️ 환경 설정 가이드

### 1단계: Python 설치
```bash
# Python 3.10 이상 필요
python --version
```

### 2단계: Python 의존성 설치
```bash
cd project_MALAYSIA
pip install -r requirements.txt
```

### 3단계: Ollama 설치 (로컬 LLM)
1. **다운로드**: https://ollama.com/download/windows
2. **설치 파일 실행**: OllamaSetup.exe
3. **모델 다운로드**:
```bash
ollama pull gemma3:12b
```

---

## 🚀 실행 방법

### 터미널 실행
```bash
cd project_MALAYSIA
python main.py
```

**성공 시 출력:**
```
Running on http://0.0.0.0:8000
```

### 브라우저 접속
```
http://localhost:8000
```

---

## 🤖 AI 의도 분류 시스템

### 단순화된 2가지 의도

| 의도 | 설명 | 인증 필요 | 예시 |
|------|------|----------|------|
| **GENERAL** | 일반 정보 (통계 포함) | ❌ 불필요 | "Hello", "How many students?", "Gender ratio?" |
| **PERSONAL_DATA** | 학생 개인 정보 | ✅ 필요 | "Who is Vicky?", "My grades", "Tell me my info" |

---

## 🔐 인증 및 보안 로직

### 로그인 방법
1. 챗봇 헤더의 **Login 버튼** 클릭
2. Student Number + Full Name 입력
3. ✅ 인증 성공 시 버튼이 사용자 이름으로 변경

---

## 📊 데이터 파일 (Excel)

### 파일: `Chatbot_TestData.xlsx`
- **중요**: 암호화/보호 해제 필요
- Excel에서 열어서 "다른 이름으로 저장" → 암호 없이 저장

---

## ❗ 트러블슈팅

### 포트 사용 중
```
Address already in use
```
**해결**: `main.py` 맨 아래 포트 번호 변경
```python
app.run(host="0.0.0.0", port=8001)
```

---

## 📝 테스트 시나리오

### 1. 일반 대화 (인증 불필요)
```
입력: "Hello, who are you?"
결과: AI 자기소개 ✅
```

### 2. 통계 조회 (인증 불필요)
```
입력: "How many students are enrolled?"
결과: 📊 통계 정보 표시 ✅
```

### 3. 미로그인 상태에서 개인정보 요청
```
입력: "Who is Vicky Yiran?"
결과: 🔒 "This is student personal information. Please login..." ✅
```

### 4. 로그인 후 본인 정보 조회
```
입력: "Show me my information"
결과: 📋 본인 정보 깔끔하게 표시 ✅
```

### 5. 타인 정보 접근 시도
```
(A로 로그인한 상태)
입력: "Who is B?"
결과: 🔒 "Privacy Protection: You can only access your own information." ✅
```

---

## 📞 Quick Reference

### 필수 명령어
```bash
# 의존성 설치
pip install -r requirements.txt

# Ollama 모델 다운로드
ollama pull gemma3:12b

# 서버 시작
python main.py
```

### 접속 URL
- 메인 페이지: http://localhost:8000
- API Health: http://localhost:8000/api/health
- API Stats: http://localhost:8000/api/stats

---

**마지막 업데이트**: 2026-02-04  
**버전**: 2.0.0
