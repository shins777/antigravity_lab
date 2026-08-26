# Antigravity Lab (antigravity_lab)

Google Antigravity CLI 기반 개발 환경 구축, 핵심 기능 확장, ADK(Agent Development Kit) 비즈니스 전략 에이전트 개발, GCP Vertex AI Agent Engine(Reasoning Engine) 배포 및 Gemini Enterprise 연동을 다루는 종합 핸즈온 실습 저장소입니다.

---

## 1. 실습 디렉터리 구조 (Lab Directory Structure)

모든 실습 프로젝트는 공통 루트 디렉터리(`~/antigravity-lab`) 아래의 **`lab/`** 폴더 내에 실습 모듈별로 격리되어 구성됩니다.

```text
~/antigravity-lab/
└── lab/                                     # 실습 통합 디렉터리
    ├── agy_setting/                         # Lab 1: 설치 및 기본 환경 구성 실습
    │   ├── .venv/                           # Python 독립 가상환경
    │   └── .agents/                         # 워크스페이스 에이전트/규칙 설정
    │
    ├── agy_command/                         # Lab 2: CLI 기본 실행 및 명령어 실습
    │   └── src/                             # 실습용 샘플 스크립트
    │
    ├── agy_features/                        # Lab 3: Agent, Skill, Rule, MCP, Plugin 확장 실습
    │   ├── .agents/
    │   │   ├── agents/                      # 커스텀 에이전트 정의 (code-reviewer.md)
    │   │   ├── skills/                      # 커스텀 스킬 정의
    │   │   ├── rules/                       # 보안 및 코딩 가드레일
    │   │   └── plugins/                     # 플러그인 확장 모듈
    │   ├── mcp_servers.json                 # MCP 서버 연동 설정
    │   └── src/                             # 대상 소스 코드
    │
    ├── agy_agent/                           # Lab 4: ADK 전략 분석 에이전트 및 GCP 배포 실습
    │   ├── src/
    │   │   ├── agent.py                     # ADK 에이전트 핵심 로직 (A4 1장 보고서 생성)
    │   │   ├── tools.py                     # 커스텀 도구 정의 (검색/데이터 요약)
    │   │   └── deploy.py                    # Vertex AI Reasoning Engine 배포 스크립트
    │   ├── tests/                           # 로컬 및 원격 질의 테스트
    │   └── requirements.txt                 # 패키지 의존성 정의
    │
    └── agy_ge/                              # Lab 5: Gemini Enterprise 등록 및 연동 실습
        ├── config/
        │   └── agent_definition.json        # Discovery Engine 등록 페이로드
        └── scripts/
            ├── register_agent.sh            # Discovery Engine REST API 등록 스크립트
            └── test_ge_agent.py             # GE 연동 검증 스크립트
```

---

## 2. 핸즈온 실습 커리큘럼 가이드 (Hands-on Labs)

각 실습 모듈별 상세 단계와 가이드는 아래 링크된 Markdown 문서를 참조하세요:

|  단계  | 실습 모듈명      | 실습 작업 디렉터리                   |                                      실습 가이드 문서                                       | 주요 학습 내용                                                                                 |
| :----: | :--------------- | :----------------------------------- | :-----------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------- |
| **01** | **agy_setting**  | `~/antigravity-lab/lab/agy_setting`  |                          [agy_setting.md](agy_lab/agy_setting.md)                           | Antigravity CLI 설치, Python 가상환경, Google 계정 인증, TUI 세션 시작                         |
| **02** | **agy_command**  | `~/antigravity-lab/lab/agy_command`  | [agy_command.md](agy_lab/agy_command.md)<br>([Deep-Dive](agy_lab/deep-dive/agy_all_cmd.md)) | 슬래시(`/`) 내장 명령어 5대 카테고리(세션/계획/서브에이전트/분석/설정) 정복                    |
| **03** | **agy_features** | `~/antigravity-lab/lab/agy_features` |                         [agy_features.md](agy_lab/agy_features.md)                          | Agent 페르소나 정의, Skill 바인딩, Rule 가드레일, MCP 서버 연동, Plugin 확장                   |
| **04** | **agy_agent**    | `~/antigravity-lab/lab/agy_agent`    |                            [agy_agent.md](agy_lab/agy_agent.md)                             | ADK 기반 1-Page 비즈니스 전략 리포트 에이전트 개발 및 GCP Vertex AI Agent Engine 배포          |
| **05** | **agy_ge**       | `~/antigravity-lab/lab/agy_ge`       |                               [agy_ge.md](agy_lab/agy_ge.md)                                | 배포된 Agent Engine을 Gemini Enterprise(Discovery Engine) 커스텀 에이전트로 등록 및 E2E 테스트 |

---

## 3. 빠른 시작 가이드 (Quick Start)

### Step 1: 실습 통합 디렉터리 준비

```bash
# 1. 실습 통합 디렉터리 생성
mkdir -p ~/antigravity-lab/lab
cd ~/antigravity-lab/lab

# 2. 개별 실습 모듈 디렉터리 생성 (필요에 따라 생성)
mkdir -p ~/antigravity-lab/lab/agy_setting
mkdir -p ~/antigravity-lab/lab/agy_command
mkdir -p ~/antigravity-lab/lab/agy_features
mkdir -p ~/antigravity-lab/lab/agy_agent
mkdir -p ~/antigravity-lab/lab/agy_ge
```

### Step 2: 실습 진행

원하는 실습 디렉터리로 이동하여 Antigravity CLI를 실행하고 실습 가이드 문서를 따라 실습을 진행합니다.

```bash
# 예시: agy_setting 실습 진입
cd ~/antigravity-lab/lab/agy_setting
agy
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
- **`.agents/rules/`**: 프로젝트 코딩 컨벤션 및 에러 처리 가드레일
- **`.agents/agents/`**: 서브에이전트 정의 (`code-reviewer.md`)
