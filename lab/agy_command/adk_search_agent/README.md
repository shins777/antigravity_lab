# ADK Web Search Agent

Google Cloud **ADK (Agent Development Kit)** 및 **Vertex AI Gemini Search Grounding**을 활용하여 사용자 질의에 맞춰 실시간 웹사이트를 검색하고, 근거와 출처 링크를 포함한 정형화된 요약 답변을 제공하는 지능형 에이전트입니다.

---

## 1. 주요 기능 및 특징

- **실시간 웹 검색 및 그라운딩 (Live Search Grounding)**: 최신 웹 정보, 공식 기술 문서, 뉴스 기사를 검색하여 답변에 반영합니다.
- **클라우드 & 로컬 호환 (ADK Interface)**: Vertex AI Reasoning Engine 표준 인터페이스(`set_up()`, `query()`)를 준수하여 로컬 실행 및 GCP 클라우드 배포가 모두 가능합니다.
- **출처 및 링크 인용 (Citations & References)**: 답변 하단에 신뢰할 수 있는 웹사이트 제목 및 클릭 가능한 마크다운 링크를 자동 포함합니다.
- **대화형 CLI & 단일 질의 모드 지원**: 단일 명령행 인자 전달 또는 대화형 대화 모드로 손쉽게 테스트할 수 있습니다.

---

## 2. 디렉터리 구조

```text
lab/agy_command/adk_search_agent/
├── __init__.py           # 패키지 진입점
├── agent.py              # ADK WebSearchAgent 클래스 구현
├── tools.py              # 검색 스키마 및 출처 포맷팅 유틸리티
├── main.py               # CLI 실행 및 테스트 스크립트
├── requirements.txt      # Python 의존성 목록
├── .env.example          # 환경 변수 예시 템플릿
└── README.md             # 사용 가이드
```

---

## 3. 사전 준비 사항 (Prerequisites)

1. **Python 가상환경 활성화**:

   ```bash
   cd ~/Documents/my_project/antigravity_lab
   source .venv/bin/activate
   ```

2. **의존성 패키지 설치**:

   ```bash
   pip install -r lab/agy_command/adk_search_agent/requirements.txt
   ```

3. **Google Cloud 인증 (ADC)**:

   ```bash
   gcloud auth application-default login
   gcloud config set project ai-hangsik
   ```

4. **환경 변수 설정 (선택 사항)**:
   ```bash
   cp lab/agy_command/adk_search_agent/.env.example lab/agy_command/adk_search_agent/.env
   ```

---

## 4. 실행 및 테스트 방법

### 1) 단일 질의 실행 (CLI Argument)

```bash
python lab/agy_command/adk_search_agent/main.py "Google Antigravity latest features and tutorials"
```

### 2) 대화형 모드 (Interactive Mode)

인자 없이 실행하면 연속해서 질문할 수 있는 대화형 프롬프트가 실행됩니다:

```bash
python lab/agy_command/adk_search_agent/main.py
```

```text
💬 Interactive Mode: Enter your search queries (type 'exit' or 'quit' to end):

[Search Query] > What are the key improvements in Python 3.12?
```

### 3) 사용자 지정 옵션 사용

```bash
python lab/agy_command/adk_search_agent/main.py \
  --project="ai-hangsik" \
  --location="us-central1" \
  --model="gemini-1.5-pro-002" \
  "Latest Gemini 2.0 Flash announcements"
```

---

## 5. 핵심 코드 사용 예시 (Python Code)

```python
from lab.agy_command.adk_search_agent import WebSearchAgent

# 1. 에이전트 인스턴스 생성
agent = WebSearchAgent(
    model_name="gemini-1.5-pro-002",
    project_id="ai-hangsik",
    location="us-central1"
)

# 2. 런타임 및 검색 도구 초기화
agent.set_up()

# 3. 질의 수행
response = agent.query("GCP Vertex AI Reasoning Engine deployment steps")
print(response)
```
