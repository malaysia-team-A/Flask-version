# 🛠️ Python Virtual Environment Setup Guide (Windows)

현재 시스템의 글로벌 파이썬 환경과 프로젝트의 의존성 충돌이 발생하고 있습니다 (`langchain` 모듈 인식 불가 등).  
아래 단계에 따라 **독립적인 가상환경(Virtual Environment)**을 구축하면 문제가 해결될 것입니다.

### 1단계: 기존 가상환경 삭제 (Clean Start)
프로젝트 폴더(`c:\Users\leejb\Desktop\project_MALAYSIA`)에서 터미널(PowerShell 또는 CMD)을 열고 아래 명령어를 입력하세요.
(이미 `.venv` 폴더가 있다면 삭제합니다)

**PowerShell:**
```powershell
Remove-Item -Recurse -Force .venv
```
**CMD:**
```cmd
rmdir /s /q .venv
```

### 2단계: 새 가상환경 생성
Python 내장 모듈을 사용하여 깨끗한 가상환경을 생성합니다.

```powershell
python -m venv .venv
```

### 3단계: 가상환경 활성화
가상환경을 활성화하면 터미널 프롬프트 앞에 `(.venv)`가 표시됩니다.

**PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```
*만약 보안 오류(PecurityError)가 발생하면:* `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` 입력 후 다시 시도하세요.

**CMD:**
```cmd
.\.venv\Scripts\activate
```

### 4단계: 필수 라이브러리 설치
가상환경이 활성화된 상태(`(.venv)` 표시 확인)에서 의존성을 설치합니다.

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5단계: 서버 실행
설치가 완료되면 서버를 실행합니다.

```powershell
python main.py
```

---

## 💡 주요 확인 사항
1. **Ollama 실행 여부**: 별도의 터미널에서 `ollama serve`가 실행 중이어야 합니다.
2. **MongoDB 연결**: `.env` 파일의 `MONGO_URI`가 올바른지 확인하세요 (현재 설정은 되어 있음).
3. **접속 주소**: 서버가 켜지면 브라우저에서 `http://localhost:5000/site/code_hompage.html` (또는 터미널에 표시된 포트)로 접속하세요.
