# 🤝 인수인계서 (Handover Document)

## 프로젝트: UCSI 챗봇 (Kai) v2.3

**작성일**: 2026-02-06  
**작성자**: Antigravity (Assistant)

---

## 1. 프로젝트 개요
본 프로젝트는 UCSI 대학교 학생들을 위한 지능형 챗봇 서비스입니다.  
학사 정보, 개인 성적 조회, 교내 편의시설 안내 등을 제공하며, 최신 **Google Gemini 2.0 Flash** 모델을 기반으로 동작합니다.

### 주요 변경 사항 (v2.3)
*   **AI 모델 업그레이드**: `Gemini 1.5` -> **`Gemini 2.0 Flash`**
*   **SDK 교체**: 불안정한 LangChain Wrapper 제거 후 **Google GenAI Native SDK** 적용 (404 오류 영구 해결).
*   **Ollama 제거**: 복잡도를 낮추고 클라우드 전용 아키텍처로 전환.

---

## 2. 실행 환경 설정 (Getting Started)

### 2.1 필수 요구 사항
*   **Python 3.10 이상**
*   **Google Cloud API Key** (Gemini 접근용)
*   **MongoDB Atlas URI** (데이터베이스 접근용)

### 2.2 설치 및 실행 방법

1.  **가상 환경 활성화**
    ```bash
    .venv\Scripts\activate
    ```

2.  **의존성 패키지 설치**
    ```bash
    pip install -r requirements.txt
    ```
    *(중요: `google-genai` 패키지가 반드시 최신 버전이어야 합니다.)*

3.  **환경 변수 확인 (`.env`)**
    루트 디렉토리의 `.env` 파일에 다음 내용이 포함되어 있어야 합니다.
    ```properties
    MONGO_URI=mongodb+srv://...
    GOOGLE_API_KEY=AIzaSy...
    GEMINI_MODEL=gemini-2.0-flash
    ADMIN_PASSWORD=admin
    ```

4.  **서버 실행**
    ```bash
    python main.py
    ```
    *정상 실행 시:* `🚀 Initializing Gemini AI (gemini-2.0-flash) via NEW Google Gen AI SDK...` 메시지가 출력됩니다.

---

## 3. 주요 파일 구조 및 설명

*   **`main.py`**: Flask 웹 서버 진입점.
*   **`ai_engine.py`**: **[핵심]** 구글 AI SDK를 이용하여 챗봇 로직을 처리하는 엔진.
    *   *주의*: 코드를 수정할 때 `self.client = genai.Client(...)` 초기화 부분을 건드리지 않도록 주의하십시오.
*   **`db_engine.py`**: MongoDB 연결 및 데이터 조회 (학생 정보, 통계).
*   **`rag_engine.py`**: 학교 문서(PDF/TXT)를 벡터화하여 검색하는 RAG 모듈.
*   **`qa_runner_100.py`**: 100가지 시나리오를 자동으로 테스트하는 스크립트.

---

## 4. 트러블슈팅 가이드 (Troubleshooting)

### Q1. "Models not found 404" 오류가 발생합니다.
*   **원인**: 구버전 라이브러리가 API 주소를 잘못 호출해서 발생했던 문제입니다.
*   **해결**: `ai_engine.py`가 최신 SDK(`google-genai`)를 쓰도록 이미 수정되었습니다. `pip install -r requirements.txt`를 다시 실행해보세요.

### Q2. "Quota Exceeded" 오류가 발생합니다.
*   **원인**: 무료 티어 사용량을 초과했습니다.
*   **해결**: `.env` 파일의 `GOOGLE_API_KEY`를 유효한 새 키로 교체하세요.

### Q3. 학생 정보를 못 찾겠다고 합니다.
*   **원인**: DB에 해당 학생이 없거나 이름 스펠링이 다릅니다.
*   **해결**: `python debug_db_v2.py` 등으로 실제 DB 데이터를 조회하여 확인해보세요.

---

## 5. 보안 주의사항
*   **.env 파일**은 절대 GitHub 등 공개 저장소에 업로드하지 마십시오.
*   `GOOGLE_API_KEY`가 유출되면 과금 폭탄을 맞을 수 있으니 주의하십시오.

(끝)
