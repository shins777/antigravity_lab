# Antigravity Lab (antigravity_lab)

Google Antigravity CLI 기반 개발 환경 구축, 핵심 기능 확장, Model Context Protocol (MCP) 서버 연동, ADK(Agent Development Kit) 에이전트 개발, GCP Cloud Run 및 Vertex AI Agent Engine(Reasoning Engine) 배포, 실시간 시스템 모니터링 대시보드를 다루는 종합 핸즈온 실습 저장소입니다.

> [!IMPORTANT]
> **모든 실습 가이드는 `macOS / Linux` 와 `Windows (PowerShell)` 두 가지 버전으로 제공됩니다.**
> 각 문서 상단의 _OS별 표기 규칙_ 안내를 먼저 확인하세요. agy TUI 내부 입력처럼 OS와 무관한 예제는 `모든 OS 동일` 로 표기되어 있습니다.
> WSL2 / Git Bash 사용자는 `macOS / Linux` 블록을 그대로 사용하면 됩니다.

---

## 1. 저장소 디렉터리 구조 (Repository Structure)

학습 **가이드 문서**는 `agy_lab/` 아래에 난이도별로, 실제 **실습 소스 코드**는 `src/` 아래에 모듈별로 격리되어 있습니다.

```text
antigravity_lab/
├── agy_lab/                                 # 📘 학습 가이드 문서 (난이도별 분류)
│   ├── agy_basic/                           # 기초 과정
│   │   ├── agy_basic.md                     # Cloud Shell 설치·환경 구성, Rule·Agent·Skill 예제 및 아키텍처
│   │   ├── agy_webapp.md                    # 로컬 웹앱 2종 제작 실습 (대시보드 · 테트리스)
│   │   └── resources/setup/                 # 가이드용 스크린샷 이미지
│   └── agy_advance/                         # 심화 과정
│       ├── agy_command.md                   # CLI 슬래시(/) 명령어 및 Agent · Skill · Rule · MCP 기능 상세 가이드
│       ├── agy_sdd.md                       # 명세 주도 개발(SDD) 기반 실전 에이전트 구축 실습
│       ├── build_agent.md                   # Ch1 ADK 멀티 에이전트 개발 + Ch2 Agent Engine 배포
│       └── agy_ge.md                        # Gemini Enterprise 등록 및 연동
│
└── src/                                     # 🧪 실습 코드 디렉터리
    ├── agy_command/                         # CLI 명령어 및 에이전트 개발 실습
    │   ├── adk_search_agent/                # 🔍 Vertex AI Search Grounding 기반 검색 에이전트
    │   ├── google_maps_mcp_agent/           # 🗺️ Streamable HTTP MCP Server (Cloud Run) & Agent Engine
    │   └── plan/                            # 실습 구현 계획 문서 모음
    │
    └── cpu_dashboard/                       # ⚡ Desktop CPU & System Status 실시간 대시보드 (Streamlit)
        ├── app.py                           # 대시보드 메인 UI
        ├── metrics.py                       # psutil 기반 메트릭 수집기
        └── run.sh                           # 원클릭 실행 스크립트
```

---

## 2. 핸즈온 실습 커리큘럼 가이드 (Hands-on Labs)

### 2.1 기초 과정 (`agy_lab/agy_basic/`)

|  단계  | 가이드 문서                                      |    분량 | 주요 학습 내용                                                                               |
| :----: | :----------------------------------------------- | ------: | :------------------------------------------------------------------------------------------- |
| **01** | [agy_basic.md](agy_lab/agy_basic/agy_basic.md)   | 1,404줄 | Cloud Shell 환경 설정, Antigravity CLI 검증, Rule·Agent·Skill 구성, `.gemini`/`.agents` 구조 |
| **02** | [agy_webapp.md](agy_lab/agy_basic/agy_webapp.md) | 1,445줄 | agy로 로컬 웹앱 2종 제작 — 실시간 시스템 대시보드(FastAPI+SSE), 웹 테트리스(Express+Canvas)  |

### 2.2 심화 과정 (`agy_lab/agy_advance/`)

|  단계  | 가이드 문서                                          |    분량 | 주요 학습 내용                                                                                                  |
| :----: | :--------------------------------------------------- | ------: | :-------------------------------------------------------------------------------------------------------------- |
| **03** | [agy_command.md](agy_lab/agy_advance/agy_command.md) | 1,868줄 | Antigravity CLI 명령어 완벽 가이드 — 슬래시(`/`) 명령어, 세션 관리, 도구·권한 제어, Agent/Skill/MCP 확장 |
| **04** | [agy_sdd.md](agy_lab/agy_advance/agy_sdd.md)         |   315줄 | 명세 주도 개발(SDD) 기반 비즈니스 기획서로부터 완벽한 자동화 프로그램 도출 실습                                |
| **05** | [build_agent.md](agy_lab/agy_advance/build_agent.md) | 3,460줄 | Ch1 ADK 멀티 에이전트 로컬 개발 + Ch2 Vertex AI Agent Engine 클라우드 배포                                      |
| **06** | [agy_ge.md](agy_lab/agy_advance/agy_ge.md)           |   427줄 | 배포된 Agent Engine을 Gemini Enterprise(Discovery Engine) 커스텀 에이전트로 등록 및 연동                        |

### 2.3 실습 코드 프로젝트 (`src/`)

| 프로젝트             | 작업 디렉터리                                                                      | 문서                                                         | 주요 학습 내용                                                                       |
| :------------------- | :--------------------------------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------------------------------- |
| **google_maps_mcp**  | [`src/agy_command/google_maps_mcp_agent/`](src/agy_command/google_maps_mcp_agent/) | [README.md](src/agy_command/google_maps_mcp_agent/README.md) | Streamable HTTP (SSE) MCP 서버 구현, GCP Cloud Run 배포, Vertex AI Agent Engine 배포 |
| **adk_search_agent** | [`src/agy_command/adk_search_agent/`](src/agy_command/adk_search_agent/)           | [README.md](src/agy_command/adk_search_agent/README.md)      | Vertex AI Search Grounding 기반 웹 검색 에이전트                                     |
| **cpu_dashboard**    | [`src/cpu_dashboard/`](src/cpu_dashboard/)                                         | [README.md](src/cpu_dashboard/README.md)                     | `psutil` + `Streamlit` + `Plotly` 기반 시스템 자원 실시간 모니터링                   |

---

## 3. 대표 실습 프로젝트 실행 가이드

### 1) Google Maps Streamable HTTP MCP 에이전트

**macOS / Linux**

```bash
# MCP 진단 테스트
python3 src/agy_command/google_maps_mcp_agent/main.py --test-mcp

# GCP Cloud Run 배포
./src/agy_command/google_maps_mcp_agent/deploy_cloud_run.sh

# Vertex AI Agent Engine 배포
python3 src/agy_command/google_maps_mcp_agent/deploy_agent_engine.py
```

**Windows (PowerShell)**

```powershell
# MCP 진단 테스트
python src\agy_command\google_maps_mcp_agent\main.py --test-mcp

# GCP Cloud Run 배포 (bash 스크립트이므로 WSL2 또는 Git Bash 필요)
bash src/agy_command/google_maps_mcp_agent/deploy_cloud_run.sh

# Vertex AI Agent Engine 배포
python src\agy_command\google_maps_mcp_agent\deploy_agent_engine.py
```

### 2) Desktop CPU 상태 모니터링 대시보드

**macOS / Linux**

```bash
./src/cpu_dashboard/run.sh
```

**Windows (PowerShell)**

```powershell
streamlit run src\cpu_dashboard\app.py
```

### 3) ADK Web Search 에이전트

**macOS / Linux**

```bash
python3 src/agy_command/adk_search_agent/main.py "Antigravity CLI 최신 업데이트 요약해줘"
```

**Windows (PowerShell)**

```powershell
python src\agy_command\adk_search_agent\main.py "Antigravity CLI 최신 업데이트 요약해줘"
```
