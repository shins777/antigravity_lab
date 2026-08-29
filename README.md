# Antigravity Lab (antigravity_lab)

Google Antigravity CLI 기반 개발 환경 구축, 핵심 기능 확장, Model Context Protocol (MCP) 서버 연동, ADK(Agent Development Kit) 에이전트 개발, GCP Cloud Run 및 Vertex AI Agent Engine(Reasoning Engine) 배포, 실시간 시스템 모니터링 대시보드를 다루는 종합 핸즈온 실습 저장소입니다.

---

## 1. 실습 디렉터리 구조 (Lab Directory Structure)

모든 실습 프로젝트는 공통 루트 디렉터리 아래의 **`lab/`** 폴더 내에 실습 모듈별로 격리되어 구성됩니다.

```text
antigravity_lab/
├── lab/                                     # 실습 통합 디렉터리
│   ├── agy_command/                         # Lab: CLI 명령어 및 에이전트 개발 실습
│   │   ├── adk_search_agent/                # 🔍 Vertex AI Search Grounding 기반 검색 에이전트
│   │   ├── google_maps_mcp_agent/           # 🗺️ Streamable HTTP MCP Server (Cloud Run) & Agent Engine
│   │   └── plan/                            # 실습 구현 계획 문서 모음
│   │
│   ├── cpu_dashboard/                       # ⚡ Desktop CPU & System Status 실시간 대시보드 (Streamlit)
│   │   ├── app.py                           # 대시보드 메인 UI
│   │   ├── metrics.py                       # psutil 기반 메트릭 수집기
│   │   └── run.sh                           # 원클릭 실행 스크립트
│   │
│   ├── agy_setting/                         # Lab: 설치 및 기본 환경 구성 실습
│   ├── agy_features/                        # Lab: Agent, Skill, Rule, MCP, Plugin 확장 실습
│   ├── agy_agent/                           # Lab: ADK 전략 분석 에이전트 및 GCP 배포 실습
│   └── agy_ge/                              # Lab: Gemini Enterprise 등록 및 연동 실습
│
├── agy_lab/                                 # Antigravity 학습 가이드 문서 모음
│   ├── agy_setting.md                       # 환경 설정 및 .gemini/.agents 구조 가이드
│   ├── agy_command.md                       # CLI 슬래시 명령어 완벽 가이드
│   ├── agy_features.md                      # 커스텀 아키텍처 확장 가이드
│   ├── agy_agent.md                         # ADK 에이전트 개발 가이드
│   └── agy_ge.md                            # Gemini Enterprise 연동 가이드
│
└── .agents/                                 # Antigravity 설정 및 커스텀 확장 자산
    ├── agents/                              # 서브에이전트 정의 (code-reviewer.md)
    ├── rules/                               # 프로젝트 규칙 및 가드레일 (commit, error handling)
    ├── skills/                              # 가이드 생성 및 개발 보조 Skill
    └── mcp_config.json                      # 전역 MCP 서버 연동 설정
```

---

## 2. 핸즈온 실습 커리큘럼 가이드 (Hands-on Labs)

각 실습 모듈별 상세 단계와 가이드는 아래 링크된 문서를 참조하세요:

|  단계  | 실습 모듈명         | 실습 작업 디렉터리                                                                 |                       실습 가이드 문서                       | 주요 학습 내용                                                                           |
| :----: | :------------------ | :--------------------------------------------------------------------------------- | :----------------------------------------------------------: | :--------------------------------------------------------------------------------------- |
| **01** | **agy_setting**     | [`lab/agy_setting/`](lab/agy_setting/)                                             |           [agy_setting.md](agy_lab/agy_setting.md)           | Antigravity CLI 설치, 가상환경 구성, `.gemini`/`.agents` 디렉터리 아키텍처 이해          |
| **02** | **agy_command**     | [`lab/agy_command/`](lab/agy_command/)                                             |           [agy_command.md](agy_lab/agy_command.md)           | 슬래시(`/`) 내장 명령어(`/plan`, `/fork`, `/clear`, `/btw` 등) 및 ADK 에이전트 실습      |
| **03** | **google_maps_mcp** | [`lab/agy_command/google_maps_mcp_agent/`](lab/agy_command/google_maps_mcp_agent/) | [README.md](lab/agy_command/google_maps_mcp_agent/README.md) | Streamable HTTP (SSE) MCP 서버 구현, GCP Cloud Run 배포, Vertex AI Agent Engine 배포     |
| **04** | **cpu_dashboard**   | [`lab/cpu_dashboard/`](lab/cpu_dashboard/)                                         |           [README.md](lab/cpu_dashboard/README.md)           | `psutil` + `Streamlit` + `Plotly` 기반 데스크톱 CPU 및 시스템 자원 실시간 모니터링       |
| **05** | **agy_features**    | [`lab/agy_features/`](lab/agy_features/)                                           |          [agy_features.md](agy_lab/agy_features.md)          | Agent 페르소나 정의, Skill 바인딩, Rule 가드레일, MCP 서버 연동, Plugin 확장             |
| **06** | **agy_agent**       | [`lab/agy_agent/`](lab/agy_agent/)                                                 |             [agy_agent.md](agy_lab/agy_agent.md)             | ADK 기반 비즈니스 전략 리포트 에이전트 개발 및 GCP Vertex AI Agent Engine 배포           |
| **07** | **agy_ge**          | [`lab/agy_ge/`](lab/agy_ge/)                                                       |                [agy_ge.md](agy_lab/agy_ge.md)                | 배포된 Agent Engine을 Gemini Enterprise(Discovery Engine) 커스텀 에이전트로 등록 및 연동 |

---

## 3. 대표 실습 프로젝트 실행 가이드

### 1) Google Maps Streamable HTTP MCP 에이전트

```bash
# MCP 진단 테스트
python lab/agy_command/google_maps_mcp_agent/main.py --test-mcp

# GCP Cloud Run 배포
./lab/agy_command/google_maps_mcp_agent/deploy_cloud_run.sh

# Vertex AI Agent Engine 배포
python lab/agy_command/google_maps_mcp_agent/deploy_agent_engine.py
```

### 2) Desktop CPU 상태 모니터링 대시보드

```bash
# 대시보드 실행 (Streamlit)
./lab/cpu_dashboard/run.sh
```

### 3) ADK Web Search 에이전트

```bash
# 웹 검색 에이전트 실행
python lab/agy_command/adk_search_agent/main.py "Antigravity CLI 최신 업데이트 요약해줘"
```

---

## 4. 저장소 관리 자산

- **`.agents/skills/`**: 실습 가이드 생성 및 개발 보조를 위한 Antigravity 전용 Skill 모듈
  - `agy_setting`: 환경 구성 가이드 생성 모듈
  - `agy_command`: CLI 명령어 체계 가이드 생성 모듈
  - `agy_features`: 핵심 확장 아키텍처 실습 모듈
  - `agy_agent`: ADK & Agent Engine 실습 모듈
  - `agy_ge`: Gemini Enterprise 연동 실습 모듈
  - `git-commit-helper`: Conventional Commits 규격 커밋 지원 모듈
- **`.agents/rules/`**: 프로젝트 코딩 컨벤션 및 에러 처리 가드레일 (`commit-convention.md`, `error-handling.md`)
- **`.agents/agents/`**: 서브에이전트 정의 (`code-reviewer.md`)
- **`.agents/mcp_config.json`**: Antigravity 전역 MCP 서버 연동 설정
