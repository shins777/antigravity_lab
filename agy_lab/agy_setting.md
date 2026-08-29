# Antigravity 설치 및 환경 구성 실습 가이드 (agy_setting)

본 문서는 **Antigravity CLI**를 로컬 시스템에 설치하고, 개발 환경과 의존성을 구성한 뒤 초기 실행 및 동작을 검증하기 위한 교육·실습용 가이드입니다.

---

## 1. 개요 및 학습 목표

- **시스템 요구사항 점검**: Antigravity 실행에 필요한 OS, Python 버전 및 도구 의존성을 확인합니다.
- **가상 환경 구축**: 독립된 Python 가상 환경(venv)을 생성하고 격리된 실행 환경을 구성합니다.
- **Antigravity CLI 설치**: 플랫폼별 바이너리/패키지를 다운로드하고 시스템 경로(PATH)에 등록합니다.
- **인증 및 기본 설정**: Google 계정 연동, 권한 모드 설정 및 기본 설정 파일 구조를 이해합니다.
- **초기 실행 검증**: 워크스페이스 신뢰 설정 및 첫 세션 실행을 통해 정상 동작 여부를 확인합니다.

---

## 2. 사전 준비 사항 (Prerequisites)

| 구분              | 요구사항                                                                     | 권장 사항                      |
| :---------------- | :--------------------------------------------------------------------------- | :----------------------------- |
| **운영체제 (OS)** | macOS (Intel / Apple Silicon), Linux (Ubuntu 22.04 LTS 이상), Windows (WSL2) | macOS / Linux Ubuntu 22.04 LTS |
| **Python**        | Python 3.10 이상                                                             | Python 3.11 또는 3.12          |
| **패키지 매니저** | `pip`, `venv`                                                                | `uv` 또는 `poetry`             |
| **추가 도구**     | `git`, `curl`, `ripgrep`                                                     | Node.js 18+ (MCP 서버 연동 시) |
| **계정 및 권한**  | 터미널 쉘 접근 권한, 패키지 설치 권한, Google 계정                           | GCP 프로젝트 접근 권한         |

---

## 3. 단계별 실습 가이드 (Hands-on Lab Steps)

### Step 1: 시스템 요구사항 점검 및 작업 디렉터리 생성

터미널을 열고 현재 시스템의 Python 버전 및 필수 도구가 정상적으로 설치되어 있는지 확인합니다.

```bash
# 1. Python 버전 확인 (3.10 이상 필수)
python3 --version

# 2. Git 및 필수 유틸리티 확인
git --version
curl --version

# 3. pip 최신 버전 업그레이드
pip install --upgrade pip

# 4. 실습용 전용 디렉터리 생성
mkdir -p ~/antigravity-lab/lab/agy_setting

```

---

### Step 2: Python 가상환경(venv) 생성 및 활성화

프로젝트 간 패키지 충돌을 방지하기 위해 가상환경을 생성하고 활성화합니다.

```bash

# 1. Project root 디렉토리로 변경
cd ~/antigravity-lab/

# 2. 가상환경 생성 (.venv)
python3 -m venv .venv

# 3. 가상환경 활성화
# macOS / Linux:
source .venv/bin/activate

# Windows (WSL2 / PowerShell):
# source .venv/bin/activate  또는  .venv\Scripts\activate

```

> [!TIP]
> 가상환경 생성 및 활성화를 위해서 속도가 빠른 패키지 매니저인 `uv`를 사용하는 경우 다음과 같이 가상환경을 생성할 수 있습니다:
>
> ```bash
> uv venv .venv
> source .venv/bin/activate
> ```

---

### Step 3: Antigravity CLI 다운로드 및 설치

공식 다운로드 포털에서 사용 중인 운영체제에 맞는 Antigravity CLI 패키지를 다운로드합니다.

- **공식 다운로드 URL:** [https://antigravity.google/product/antigravity-cli](https://antigravity.google/product/antigravity-cli)

<p align="left">
  <img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="img/img1.png" width="800" alt="Antigravity Download Page">
</p>

#### 설치 및 실행 권한 부여

1. 다운로드한 바이너리 파일의 압축을 해제합니다.
2. 실행 바이너리(`agy`)를 시스템 경로(`/usr/local/bin` 또는 `~/.local/bin`)로 이동합니다.

```bash
# 실행 권한 부여 (macOS / Linux)
chmod +x agy

# PATH에 등록되어 있는 디렉터리로 이동 (예: /usr/local/bin)
sudo mv agy /usr/local/bin/

# 설치 버전 확인
agy --version
```

---

### Step 4: 사용자 인증 및 계정 연동 (Authentication)

Antigravity는 Google 계정 및 Gemini 모델 백엔드와의 통신을 위한 인증을 필요로 합니다.

```bash
# Google 계정 로그인 및 인증 진행
agy login
```

1. 명령어를 실행하면 브라우저에 인증 페이지가 열립니다.
2. Antigravity를 사용할 Google 계정으로 로그인 후 권한을 승인합니다.
3. 인증이 완료되면 터미널에 인증 완료 메시지가 표시됩니다.

> [!IMPORTANT]
> GCP 인프라 또는 Vertex AI 환경과 연동해야 하는 경우 Application Default Credentials(ADC)가 설정되어 있어야 합니다:
>
> ```bash
> gcloud auth application-default login
> ```

---

### Step 5: 워크스페이스 신뢰 및 초기 세션 실행

실습 디렉터리에서 Antigravity CLI 대화형 세션을 시작합니다.

```bash
cd ~/antigravity-lab/
agy
```

#### 1. 워크스페이스 신뢰 확인 (Workspace Trust)

처음 진입하는 디렉터리인 경우 보안을 위한 워크스페이스 신뢰 확인 프롬프트가 표시됩니다.

```text
Accessing workspace:
/Users/hangsik/antigravity-lab/lab/agy_setting
Do you trust the contents of this project?
Antigravity CLI requires permission to read, edit, and execute files here.
> Yes, I trust this folder
   No, exit
   ↑/↓ Navigate · enter Confirm
```

- 방향키로 `Yes, I trust this folder`를 선택하고 **Enter**를 누릅니다.

#### 2. Antigravity TUI 초기 화면 확인

정상적으로 진입하면 아래와 같은 터미널 인터페이스(TUI)가 나타납니다.

```text
      ▄▀▀▄        Antigravity CLI 1.1.13
     ▀▀▀▀▀▀       user@example.com (Agent Platform)
    ▀▀▀▀▀▀▀▀      Gemini 3.6 Flash (Low)
   ▄▀▀    ▀▀▄     ~/antigravity-lab/lab/agy_setting
  ▄▀▀      ▀▀▄

───────────────────────────────────────────────────────────────────────────────────────────────────
>
───────────────────────────────────────────────────────────────────────────────────────────────────
? for shortcuts                                                              Gemini 3.6 Flash · low
```

---

### Step 6: 디렉터리 구조 및 설정 파일 관리

Antigravity의 설정 및 커스터마이징 파일은 전역(Global)과 프로젝트(Workspace) 계층으로 나뉘어 관리됩니다.

```bash
# 프로젝트 루트에서 .agents 커스터마이징 디렉터리 생성
mkdir -p .agents/rules .agents/skills .agents/agents
```

---

### Step 7: 초기 실행 검증 (Verification)

Antigravity 프롬프트(`> `)에서 아래 명령어를 순서대로 입력하여 동작을 검증합니다.

1. **도움말 및 단축키 확인:**

   ```text
   > /help
   ```
   - 사용 가능한 전체 명령어와 단축키 목록이 정상 출력되는지 확인합니다.

2. **현재 모델 및 추론 수준 확인:**

   ```text
   > /model
   ```
   - 활성화된 Gemini 모델(예: Gemini 3.6 Pro / Flash) 목록이 표시되는지 확인합니다.

3. **간단한 코드 생성 및 도구 호출 테스트:**

   ```text
   > Python으로 1부터 10까지의 합을 구하는 sum_0_to_10.py 파일을 생성해줘.
   ```
   - 에이전트가 `write_to_file` 도구를 호출하여 파일을 정상 생성하는지 확인합니다.

4. **세션 종료:**
   ```text
   > /exit
   ```

---

## 4. 환경 디렉터리 구조 및 설정 파일 상세 가이드 (`.gemini` & `.agents`)

Antigravity는 사용자 개별 머신 레벨의 **전역 설정(`.gemini`)**과 팀 프로젝트 단위로 공유되는 **워크스페이스 커스터마이징(`.agents`)**을 분리하여 체계적인 에이전트 개발 환경을 제공합니다.

```text
├── ~/.gemini/                               # [전역] 사용자 홈 기반 전역 설정 및 런타임 데이터
│   ├── antigravity-cli/
│   │   ├── settings.json                   # CLI 전역 설정 (기본 모델, 테마, 권한 등)
│   │   ├── cache/
│   │   │   └── projects.json               # 프로젝트 경로 - ID 매핑 캐시
│   │   ├── brain/                          # 세션 트랜스크립트 및 생성 아티팩트
│   │   │   └── <conversation_id>/
│   │   │       ├── .system_generated/logs/ # JSONL 대화 로그 (transcript.jsonl)
│   │   │       ├── scratch/                # 임시 분석/디버깅 스크립트 저장소
│   │   │       └── *.md                    # 사용자 제공 구조화된 아티팩트 문서
│   │   └── builtin/skills/                 # CLI 내장 기본 스킬 모듈
│   └── config/
│       ├── skills/                         # 머신 전역 커스텀 스킬
│       ├── plugins/                        # 머신 전역 플러그인
│       └── mcp_config.json                 # 머신 전역 MCP(Model Context Protocol) 서버 설정
│
└── <Workspace Root>/                        # [로컬] 프로젝트 워크스페이스 (Git 형상 관리 대상)
    ├── GEMINI.md                            # 프로젝트/디렉터리 최상위 가이드라인 및 공통 지침
    ├── .agents/                             # 프로젝트 전용 에이전트 커스터마이징 폴더
    │   ├── rules/                           # 가드레일, 코딩 스타일, 보안 제약 규칙 (.md)
    │   ├── skills/                          # 도메인 특화 절차형 스킬 워크플로우 (SKILL.md)
    │   ├── agents/                          # 전문 서브에이전트 정의 파일 (.md)
    │   ├── mcp_config.json                  # 프로젝트 전용 MCP 서버 연동 설정
    │   └── hooks.json                       # 에이전트 라이프사이클 이벤트 훅 정의
    └── .gitignore                           # 시크릿(.env) 및 임시 파일 제외 설정
```

---

### 4.1 `.gemini` 폴더 (전역 설정 및 런타임 저장소)

사용자의 홈 디렉터리(`~/.gemini/`)에 위치하며, Antigravity 런타임 구동 시 필요한 전역 설정, 대화 기록, 캐시 데이터를 관리합니다.

#### 주요 파일 및 디렉터리

1. **`~/.gemini/antigravity-cli/settings.json` (전역 CLI 환경설정 파일)**
   - 기본 AI 모델, 추론 강도(Reasoning Effort), 권한 승인 모드, 터미널 UI 테마 등을 전역적으로 제어합니다.
   - 예시:
     ```json
     {
       "model": "gemini-3.6-pro",
       "effort": "medium",
       "sandbox": false,
       "dangerously_skip_permissions": false
     }
     ```

2. **`~/.gemini/antigravity-cli/cache/projects.json` (프로젝트 매핑 캐시)**
   - 로컬 작업 디렉터리 경로와 고유 `project_id`의 매핑 정보를 유지하여 `/fork <project_id>` 또는 `--project` 옵션 실행 시 프로젝트 범위를 추적합니다.

3. **`~/.gemini/antigravity-cli/brain/<conversation_id>/` (세션 메모리 및 아티팩트)**
   - 각 대화 세션의 트랜스크립트 로그(`transcript.jsonl`, `transcript_full.jsonl`)가 보관됩니다.
   - 복잡한 분석 보고서, 아키텍처 다이어그램, 계획 문서 등 사용자에게 제시된 아티팩트(`.md`) 및 임시 실행 스크립트(`scratch/`)가 영구 보존됩니다.

4. **`~/.gemini/config/mcp_config.json` (전역 MCP 설정 파일)**
   - 모든 워크스페이스에서 공통으로 사용할 Model Context Protocol 서버(예: PostgreSQL 브리지, 로컬 파일 서버, 웹 브라우저 자동화 도구 등)를 정의합니다.

---

### 4.2 `.agents` 폴더 (프로젝트 레벨 에이전트 커스터마이징)

프로젝트 루트 디렉터리에 위치하며, Git과 같은 버전 관리 시스템(VCS)에 커밋하여 **팀 전체가 동일한 AI 코딩 표준과 전문 스킬을 공유**할 수 있도록 설계된 핵심 폴더입니다.

#### 1. `.agents/rules/` (규칙 및 가드레일)

- 코딩 컨벤션, 에러 핸들링 원칙, 커밋 메시지 규약, 보안 정책 등을 마크다운(`.md`)으로 정의합니다.
- YAML Frontmatter를 통해 규칙이 활성화되는 조건을 제어할 수 있습니다.
- **예시 (`.agents/rules/commit-convention.md`):**
  ```markdown
  ---
  trigger: always_on
  description: Git commit message conventional format rule
  ---

  # Conventional Commits Guidelines

  - Format: `<type>(<scope>): <subject>`
  - Allowed Types: feat, fix, docs, style, refactor, test, chore
  ```

#### 2. `.agents/skills/` (스킬 모듈)

- 에이전트에게 특정 비즈니스 로직, 복잡한 빌드/배포 절차, 런북 가이드를 가르치는 모듈입니다.
- 각 스킬은 독립된 폴더 내 `SKILL.md` 파일로 작성되며, 점진적 공개(Progressive Disclosure) 방식으로 동작하여 필요한 시점에만 컨텍스트에 로드됩니다.
- **구조:**
  ```text
  .agents/skills/deploy-pipeline/
  ├── SKILL.md             # 스킬 메타데이터 및 지침 (필수)
  ├── scripts/             # 자동화 보조 셸/파이썬 스크립트
  ├── examples/            # 참조 예제 코드
  └── references/          # 상세 매뉴얼 문서
  ```

#### 3. `.agents/agents/` (서브에이전트 정의)

- 전문적인 역할을 수행하는 독립 서브에이전트(Subagent)를 선언합니다.
- **예시 (`.agents/agents/code-reviewer.md`):**
  ```markdown
  ---
  name: code-reviewer
  description: 코드 리뷰 및 보안 취약점 분석 전문 에이전트
  model: pro
  tools:
    - read_file
    - grep_search
    - find_by_name
  ---

  당신은 시니어 코드 리뷰어입니다. 코드의 잠재적 버그, 메모리 누수, 보안 취약점을 중점적으로 검토하세요.
  ```

#### 4. `.agents/mcp_config.json` (프로젝트 전용 MCP 설정)

- 프로젝트 개발에 필요한 로컬 DB, 사내 API 도구, Docker 컨테이너와의 연동을 정의합니다.
- **예시:**
  ```json
  {
    "mcpServers": {
      "sqlite-db": {
        "command": "uvx",
        "args": ["mcp-server-sqlite", "--db-path", "./data/app.db"]
      }
    }
  }
  ```

#### 5. `.agents/hooks.json` (에이전트 라이프사이클 훅)

- 에이전트가 도구를 호출하기 전(`pre_tool_call`), 호출한 후(`post_tool_call`), 또는 세션이 시작될 때 자동으로 실행할 셸 명령어를 바인딩합니다. (예: 파일 수정 후 자동 linter/formatter 실행)

---

### 4.3 설정 우선순위 및 보안 권장사항

#### 커스터마이징 로딩 우선순위 (Priority)

동일한 이름의 스킬이나 규칙이 존재할 경우 다음 순서로 우선 적용(Override)됩니다:

1. **프로젝트 로컬 커스터마이징** (`<Workspace Root>/.agents/`, `GEMINI.md`) — _최우선_
2. **명시적 설정 파일** (`skills.json`, `plugins.json`)
3. **사용자 전역 설정** (`~/.gemini/config/`)
4. **Antigravity 내장 스킬/설정** (`~/.gemini/antigravity-cli/builtin/`)

> [!CAUTION]
> **보안 및 시크릿 관리 주의사항**
>
> - API 키(`GEMINI_API_KEY`, `GOOGLE_API_KEY`), 데이터베이스 비밀번호, 인증 토큰은 절대로 `.agents/` 또는 `GEMINI.md` 파일 내에 직접 작성하여 Git에 커밋하지 마십시오.
> - 환경 변수 파일(`.env`, `.env.local`)은 반드시 `.gitignore`에 등록하여 버전 관리에서 제외하고, 안전한 템플릿 파일(`.env.example`)만 공유해야 합니다.

---

## 5. 문제 해결 및 FAQ (Troubleshooting)

### Q1. `agy: command not found` 오류가 발생합니다.

- **원인:** `agy` 실행 바이너리가 시스템의 `PATH` 환경 변수에 등록되지 않았습니다.
- **해결 방법:**
  ```bash
  # 바이너리 위치 확인 후 PATH 추가 (예: ~/.local/bin에 있는 경우)
  export PATH="$HOME/.local/bin:$PATH"

  # ~/.zshrc 또는 ~/.bashrc 에 영구 추가
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
  source ~/.zshrc
  ```

### Q2. Python 버전이 3.9 이하로 인식됩니다.

- **원인:** 시스템 기본 Python 버전이 구버전이거나 가상환경이 비활성화되어 있습니다.
- **해결 방법:**
  - `python3.10` 이상의 버전을 설치(`brew install python@3.11` 또는 `apt install python3.11-venv`)
  - 지정된 파이썬 바이너리로 가상환경을 재생성합니다:
    ```bash
    python3.11 -m venv .venv
    source .venv/bin/activate
    ```

### Q3. 인증 토큰 만료 또는 로그인 오류가 발생합니다.

- **원인:** 구글 로그인 세션이 만료되었거나 캐시된 토큰에 이상이 발생한 경우입니다.
- **해결 방법:**
  ```bash
  agy /logout
  agy login
  ```

---

## 6. 실습 완료 체크리스트

- [ ] Python 3.10 이상 버전 확인 및 가상환경 활성화 완료
- [ ] Antigravity CLI 바이너리 설치 및 `agy --version` 확인 완료
- [ ] Google 계정 로그인 (`agy login`) 및 인증 완료
- [ ] 실습 워크스페이스 생성 및 신뢰(Trust) 승인 완료
- [ ] `agy` TUI 실행 및 `/help` 명령어 정상 작동 확인 완료
- [ ] `.gemini` 및 `.agents` 환경 디렉터리 역할 및 설정 파일 구조 이해 완료
