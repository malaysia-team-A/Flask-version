# 🛠️ UCSI Chatbot - Setup & Installation Guide (v2.2)

이 가이드는 UCSI 대학교 챗봇(Kai)을 로컬 Windows 환경에 설치하고 실행하는 방법을 상세히 설명합니다.
버전 2.2부터는 **Google Gemini**를 사용하여 더욱 강력한 성능을 제공합니다.

---

## ✅ 1. 사전 요구사항 (Prerequisites)

설치를 시작하기 전에 다음 항목들을 준비하세요.

1.  **Python 3.10 이상**: [다운로드 링크](https://www.python.org/downloads/)
2.  **Google AI Studio API Key**: [키 발급 받기](https://aistudio.google.com/app/apikey)
    *   무료로 발급 가능합니다.
3.  **MongoDB Atlas 계정**: [MongoDB Cloud](https://www.mongodb.com/cloud/atlas)
    *   무료 클러스터 연결 문자열(URI)이 필요합니다.
4.  *(선택)* **Ollama**: 인터넷 연결이 없는 환경에서 로컬 모델을 쓰고 싶을 때만 필요합니다.

---

## 📥 2. 프로젝트 설치 (Installation)

### 2.1 가상환경 생성 및 활성화
깨끗한 환경을 위해 기존 가상환경을 제거하고 새로 생성하는 것을 권장합니다.

```powershell
# 기존 가상환경 삭제
Remove-Item -Recurse -Force .venv

# 새 가상환경 생성
python -m venv .venv

# 가상환경 활성화
.\.venv\Scripts\activate
```

### 2.2 의존성 라이브러리 설치
Gemini 연동을 위한 `langchain-google-genai` 등 필수 패키지를 설치합니다.

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ⚙️ 3. 환경 설정 (Configuration)

### 3.1 .env 파일 설정 (중요)
프로젝트 루트 폴더에 `.env` 파일을 생성하고 아래 내용을 채워넣으세요.

**.env 파일 예시:**
```ini
# Google Gemini API Key (필수)
GOOGLE_API_KEY=AIzaSy... (여기에 발급받은 키 입력)
GEMINI_MODEL=gemini-2.0-flash

# MongoDB Atlas 연결
MONGO_URI=mongodb+srv://admin:<password>@cluster0.mongodb.net/UCSI_DB

# 보안 키 & 관리자 비번
SECRET_KEY=UCSI_CHATBOT_SECRET_KEY_2026
ADMIN_PASSWORD=admin123
```

---

## 🚀 4. 서버 실행 및 테스트

### 4.1 서버 시작
```powershell
python main.py
```
정상 실행 시: `Running on http://0.0.0.0:5000` 메시지가 뜹니다.

### 4.2 접속 주소
*   **채팅 인터페이스**: [http://localhost:5000/site/code_hompage.html](http://localhost:5000/site/code_hompage.html)
*   **관리자 페이지**: [http://localhost:5000/admin](http://localhost:5000/admin)

---

## 🧪 5. 자동화 테스트 (QA)

시스템이 정상 작동하는지 확인하려면 내장된 테스트 스크립트를 실행하세요.

```powershell
# 1. 빠른 로직 검증 (5초)
python qa_runner_100_mock.py

# 2. 전체 AI 답변 검증 (시간 소요)
python qa_runner_100.py
```

---

## ❓ 문제 해결 (Troubleshooting)

*   **Google API Key Error**: `.env` 파일에 `GOOGLE_API_KEY`가 정확히 입력되었는지 확인하세요. 키가 없으면 자동으로 느린 로컬 모델(Ollama)로 전환됩니다.
*   **ModuleNotFoundError**: `pip install -r requirements.txt`를 다시 실행하세요.
*   **MongoDB Timeout**: 인터넷 연결을 확인하고 `MONGO_URI`의 비밀번호가 맞는지 확인하세요.
