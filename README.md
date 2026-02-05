# 🎓 UCSI University AI 챗봇 - 인수인계서

## 📋 프로젝트 개요

**UCSI University AI Chatbot**은 학생들이 대학 정보 및 개인 정보(성적, 등록상태)를 AI와 대화를 통해 조회할 수 있는 시스템입니다.

- **LangChain** + **Ollama** 기반 로컬 LLM 사용
- **MongoDB Atlas**에서 학생 데이터 조회
- **FAISS** 벡터 DB로 대학 문서 검색 (RAG)
- **이중 인증**으로 민감 정보(성적) 보호

---

## 🛠️ 설치 및 실행 가이드

### 사전 요구사항
- **Python 3.10 이상**
- **Ollama** 설치 및 실행 ([https://ollama.com](https://ollama.com))
- **MongoDB Atlas** 계정 및 연결 문자열

### Step 1: 가상환경 생성 및 활성화

```powershell
# 프로젝트 폴더로 이동
cd c:\Users\leejb\Desktop\project_MALAYSIA

# 가상환경 생성
python -m venv .venv

# 가상환경 활성화 (PowerShell)
.\.venv\Scripts\Activate.ps1

# 만약 보안 오류 발생 시:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\Activate.ps1
```

### Step 2: 의존성 설치

```powershell
# 가상환경 활성화된 상태에서 실행
pip install -r requirements.txt
```

### Step 3: Ollama 모델 다운로드

```powershell
# 별도 터미널에서 실행
ollama pull gemma3:12b
```

### Step 4: 환경변수 설정

`.env` 파일이 프로젝트 루트에 있어야 합니다:

```
MONGO_URI=mongodb+srv://[사용자]:[비밀번호]@cluster.mongodb.net/UCSI_DB
OLLAMA_MODEL=gemma3:12b
OLLAMA_URL=http://localhost:11434
ADMIN_PASSWORD=admin123
```

### Step 5: 서버 실행

```powershell
# 가상환경 활성화 상태에서
python main.py
```

**접속 주소:**
- 챗봇 UI: [http://localhost:5000/site/code_hompage.html](http://localhost:5000/site/code_hompage.html)
- 관리자 패널: [http://localhost:5000/admin](http://localhost:5000/admin)

---

## 🧪 테스트 시나리오

| 시나리오 | 입력 | 예상 결과 |
|----------|------|-----------|
| 일반 정보 조회 | "What faculties are there?" | 지식베이스 기반 학과 목록 응답 |
| 로그인 | 학번: `1001`, 이름: `Alice` | 로그인 성공, JWT 토큰 발급 |
| 프로필 조회 | "What is my student ID?" | 본인 학번 표시 |
| 성적 조회 (이중인증) | "Show me my grades" | 비밀번호 재입력 요청 |
| 통계 조회 | "How many students are there?" | MongoDB 집계 결과 표시 |

---

## 📁 핵심 파일 설명

| 파일 | 역할 |
|------|------|
| `main.py` | Flask 서버, API 엔드포인트 정의 |
| `ai_engine.py` | LangChain 의도분류 및 응답 생성 |
| `db_engine.py` | MongoDB Atlas 연결 및 쿼리 |
| `rag_engine.py` | FAISS 벡터 검색 (RAG) |
| `auth_utils.py` | JWT 토큰 및 비밀번호 해싱 |
| `requirements.txt` | Python 의존성 목록 |
| `.env` | 환경변수 (MongoDB URI, Ollama 설정) |

---

## ⚠️ 주의사항

1. **Ollama 서버 필수**: `main.py` 실행 전에 `ollama serve`가 실행 중이어야 합니다.
2. **가상환경 사용**: 반드시 `.venv` 가상환경 내에서 실행하세요.
3. **MongoDB 연결**: `.env`의 `MONGO_URI`가 올바른지 확인하세요.
4. **포트**: 기본 포트는 `5000`입니다. 변경 시 `main.py` 수정 필요.

---

## 🔧 문제 해결

### ModuleNotFoundError 발생 시
```powershell
# 가상환경이 활성화되어 있는지 확인 (프롬프트에 (.venv) 표시)
# 안 되어 있다면:
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### MongoDB 연결 실패 시
- `.env` 파일의 `MONGO_URI` 확인
- MongoDB Atlas에서 IP 화이트리스트에 현재 IP 추가

### Ollama 연결 실패 시
- 별도 터미널에서 `ollama serve` 실행 확인
- `ollama list`로 모델 설치 여부 확인
