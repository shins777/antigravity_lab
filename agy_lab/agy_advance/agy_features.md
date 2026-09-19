# Antigravity 핵심 기능 구성 및 확장 실습 가이드 (agy_features)

> [!IMPORTANT]
> **OS별 표기 규칙**
>
> 이 문서의 모든 실행 예제는 아래 세 가지 표기 중 하나를 따릅니다. 자신의 환경에 해당하는 블록만 실행하세요.
>
> | 표기                     | 의미                                                       |
> | ------------------------ | ---------------------------------------------------------- |
> | **macOS / Linux**        | macOS(zsh) 및 Linux(bash) 터미널에서 실행                  |
> | **Windows (PowerShell)** | Windows PowerShell 5.1+ 또는 PowerShell 7.x 에서 실행      |
> | **모든 OS 동일**         | agy TUI 내부 입력·프롬프트·파일 내용 등 OS와 무관하게 동일 |
>
> - **WSL2 / Git Bash** 사용자는 `macOS / Linux` 블록을 그대로 사용하세요.
> - Windows에서는 `python3` → `python`, `curl` → `curl.exe`, `/` → `\` 로 바뀌는 점에 유의하세요.

본 문서는 **Antigravity**의 5대 핵심 확장 아키텍처인 **Agents(서브에이전트), Skills(스킬), Rules(가드레일 규칙), MCP(Model Context Protocol), Plugins & Hooks(플러그인 및 훅)**의 개념을 이해하고, 프로젝트 및 전역 환경에 직접 구성하여 실습하는 종합 가이드입니다.

---

## 1. 개요 및 학습 목표

- **Agents & Skills:** 특화된 역할의 커스텀 에이전트(Persona)를 정의하고 다단계 절차를 수행하는 스킬(Skill)을 바인딩합니다.
- **Rules & Guardrails:** 코딩 컨벤션, 보안 정책, 에러 핸들링 가이드 등 에이전트 행동을 제어하는 규칙을 적용합니다.
- **MCP (Model Context Protocol):** 표준 프로토콜을 통해 외부 데이터베이스, GitHub, 파일시스템 등 외부 도구 서버와 연동합니다.
- **Plugins & Lifecycle Hooks:** 스킬·규칙 번들 패키징 및 도구 호출 전/후 런타임 이벤트 훅을 구성합니다.
- **우선순위 및 점진적 노출(Progressive Disclosure):** 컨텍스트 윈도우를 최적화하면서 워크스페이스/전역 설정을 효율적으로 로드하는 메커니즘을 습득합니다.

---

## 2. 사전 준비 사항 (Prerequisites)

| 항목                | 요구사항                       | 비고                  |
| :------------------ | :----------------------------- | :-------------------- |
| **Antigravity CLI** | 최신 버전 설치 및 로그인 완료  | `agy --version` 확인  |
| **Python 환경**     | Python 3.10 이상 가상환경      | `.venv` 활성화        |
| **Node.js 런타임**  | Node.js 18.x 이상 및 `npx`     | MCP 서버 실행용       |
| **기초 실습 완료**  | `agy_setting` 및 `agy_command` | 기본 명령어 체계 숙지 |

---

## 3. 핵심 아키텍처 및 디렉터리 구성 체계

Antigravity는 프로젝트 로컬(Workspace)과 시스템 전역(Global) 설정을 계층적으로 탐색하여 적용합니다.

```
┌────────────────────────────────────────────────────────────────────────┐
│                      커스터마이징 우선순위 (Precedence)                  │
│                                                                        │
│  1. Workspace Project (.agents/)  ──> 프로젝트 루트 탐색 (최상위 우선순위) │
│  2. Declared Configurations (JSON)──> skills.json / plugins.json 명시  │
│  3. Global Config (~/.gemini/)    ──> 사용자 머신 전역 설정           │
│  4. Built-in Customizations       ──> Antigravity CLI 기본 내장 스킬   │
└────────────────────────────────────────────────────────────────────────┘
```

### 3.1 OS별 설정 파일 경로 매핑

| 논리 경로 | macOS / Linux | Windows |
| :--- | :--- | :--- |
| 프로젝트 설정 (`.agents/`) | `~/<Project>/.agents/` | `%USERPROFILE%\<Project>\.agents\` |
| 전역 설정 (`~/.gemini/`) | `~/.gemini/` | `%USERPROFILE%\.gemini\` |

### 주요 구성 요소 요약

| 구성 요소      | 역할 및 기능                                             | 표준 파일 경로                         |
| :------------- | :------------------------------------------------------- | :------------------------------------- |
| **Agent**      | 전문화된 작업 수행 주체(LLM 지침, 권한, 전용 도구) 정의  | `.agents/agents/<name>.md`             |
| **Skill**      | 다단계 절차, 런북, 워크플로우를 가르치는 온디맨드 모듈   | `.agents/skills/<name>/SKILL.md`       |
| **Rule**       | 시스템 보안 정책, 코딩 스타일, 에러 핸들링 상시 가드레일 | `.agents/rules/<name>.md`              |
| **MCP Server** | 외부 DB, API, 도구와 연결하는 표준 컨텍스트 프로토콜     | `mcp_servers.json` / `mcp_config.json` |
| **Hook**       | 도구 실행 전/후(Pre/Post) 자동 실행되는 쉘/스크립트 훅   | `hooks.json`                           |
| **Plugin**     | 에이전트, 스킬, 규칙, MCP를 하나로 묶은 배포 번들        | `plugins/<name>/plugin.json`           |

---

## 4. 단계별 실습 가이드 (Hands-on Lab Steps)

### Step 1: 기능 실습용 워크스페이스 디렉터리 구성

실습 프로젝트 디렉터리를 생성하고 핵심 기능별 하위 폴더 구조를 준비합니다.

#### macOS / Linux

```bash
# 1. 실습 루트 디렉터리 생성 및 이동
mkdir -p ~/antigravity-lab/lab/agy_features
cd ~/antigravity-lab/lab/agy_features

# 2. Antigravity 표준 확장 디렉터리 생성
mkdir -p .agents/agents
mkdir -p .agents/skills/data-fetcher
mkdir -p .agents/rules
mkdir -p .agents/plugins
mkdir -p src
```

#### Windows (PowerShell)

```powershell
# 1. 실습 루트 디렉터리 생성 및 이동
$LabPath = "$HOME\antigravity-lab\lab\agy_features"
New-Item -ItemType Directory -Force -Path $LabPath | Out-Null
Set-Location $LabPath

# 2. Antigravity 표준 확장 디렉터리 생성
".agents\agents", ".agents\skills\data-fetcher", ".agents\rules", ".agents\plugins", "src" | ForEach-Object {
    New-Item -ItemType Directory -Force -Path $_ | Out-Null
}
```

---

### Step 2: Custom Agent 정의 및 호출 실습

전문화된 **코드 리뷰어 에이전트(`code-reviewer`)**를 정의합니다. YAML Frontmatter로 메타데이터와 권한을 정의하고, Markdown 본문으로 지침(System Prompt)을 작성합니다.

#### 1. 에이전트 정의 파일 생성 (`.agents/agents/code-reviewer.md`)

#### macOS / Linux

```bash
cat << 'EOF' > .agents/agents/code-reviewer.md
---
name: code-reviewer
description: 코드 보안 취약점, 성능 병목, 스타일 가이드 분석 및 리팩토링 제안 전문 에이전트
tools:
  - view_file
  - grep_search
  - list_dir
mainAgent: true
subagent: true
model: inherit
commandExecutionPolicy: sandbox
---

# Code Reviewer Instructions

당신은 시니어 코드 리뷰어입니다. 전달받은 코드에 대해 다음 3가지 핵심 축을 기준으로 정밀 분석을 수행하세요:

1. **보안성 (Security):** SQL/명령어 인젝션, 민감 정보 노출, 미흡한 입력 검증 여부
2. **성능 (Performance):** 불필요한 연산 루프(O(N) -> O(1)), 메모리 누수, 병목 지점 탐지
3. **가독성 및 컨벤션:** PEP8/프로젝트 스타일 가이드 및 모범 사례 준수 여부

## 응답 규칙
- 문제점 지적 시 구체적인 라인 번호와 발생 원인을 반드시 명시하세요.
- 개선된 코드는 즉시 적용 가능한 마크다운 코드 블록으로 제공하세요.
EOF
```

#### Windows (PowerShell)

```powershell
@'
---
name: code-reviewer
description: 코드 보안 취약점, 성능 병목, 스타일 가이드 분석 및 리팩토링 제안 전문 에이전트
tools:
  - view_file
  - grep_search
  - list_dir
mainAgent: true
subagent: true
model: inherit
commandExecutionPolicy: sandbox
---

# Code Reviewer Instructions

당신은 시니어 코드 리뷰어입니다. 전달받은 코드에 대해 다음 3가지 핵심 축을 기준으로 정밀 분석을 수행하세요:

1. **보안성 (Security):** SQL/명령어 인젝션, 민감 정보 노출, 미흡한 입력 검증 여부
2. **성능 (Performance):** 불필요한 연산 루프(O(N) -> O(1)), 메모리 누수, 병목 지점 탐지
3. **가독성 및 컨벤션:** PEP8/프로젝트 스타일 가이드 및 모범 사례 준수 여부

## 응답 규칙
- 문제점 지적 시 구체적인 라인 번호와 발생 원인을 반드시 명시하세요.
- 개선된 코드는 즉시 적용 가능한 마크다운 코드 블록으로 제공하세요.
'@ | Set-Content -Encoding UTF8 ".agents\agents\code-reviewer.md"
```

#### 2. 에이전트 호출 및 동작 검증

1. **터미널 진입 시 메인 에이전트로 지정:**

**macOS / Linux**

```bash
agy --agent code-reviewer
```

**Windows (PowerShell)**

```powershell
agy --agent code-reviewer
```

2. **세션 내 멘션(`@`) 호출:**

**모든 OS 동일**

```text
> @[.agents/agents/code-reviewer.md] src/main.py 파일의 보안성과 성능을 리뷰해줘
```

3. **자연어 위임 호출:**

**모든 OS 동일**

```text
> 작성된 파이썬 코드에 대해 코드리뷰어를 호출해서 리뷰 보고서를 작성해줘
```

---

### Step 3: Skill 정의 및 점진적 노출(Progressive Disclosure) 실습

에이전트에게 특정 API 호출 및 데이터 가공 절차를 가르치는 **`data-fetcher`** 스킬을 작성합니다.

> [!NOTE]
> **점진적 노출 (Progressive Disclosure):**
> 수십 개의 스킬이 있더라도 평상시에는 이름과 한 줄 설명(`description`)만 컨텍스트에 포함됩니다. 모델이 해당 스킬을 실행하기로 결정했을 때만 본문 전체(`SKILL.md`)가 온디맨드로 로드되어 토큰 낭비를 방지합니다.

#### 1. 스킬 정의 파일 생성 (`.agents/skills/data-fetcher/SKILL.md`)

#### macOS / Linux

```bash
cat << 'EOF' > .agents/skills/data-fetcher/SKILL.md
---
name: data-fetcher
title: 외부 REST API 데이터 수집 및 전처리 워크플로우
version: 1.0.0
description: 공공 데이터 또는 REST API 엔드포인트에서 JSON 데이터를 수집하고 정규화된 CSV로 변환하는 스킬
tags:
  - data
  - api
  - etl
---

# Data Fetcher Skill Instructions

본 스킬은 외부 API 엔드포인트로부터 데이터를 수집하고 Pandas/Python을 사용해 클렌징하는 표준 절차를 안내합니다.

## 표준 실행 워크플로우

1. **API 요청 및 응답 검증:**
   - `requests` 또는 `httpx` 라이브러리를 사용하여 타임아웃(기본 10초)과 함께 GET 요청을 수행합니다.
   - HTTP 상태 코드가 200이 아닌 경우 적절한 예외 로그를 출력합니다.
2. **데이터 파싱 및 스키마 검증:**
   - 응답 JSON 데이터의 필수 필드 누락 여부를 검사합니다.
3. **로컬 저장 및 캐싱:**
   - 정제된 데이터를 `data/output.json` 또는 `data/output.csv` 파일로 저장합니다.
EOF
```

#### Windows (PowerShell)

```powershell
@'
---
name: data-fetcher
title: 외부 REST API 데이터 수집 및 전처리 워크플로우
version: 1.0.0
description: 공공 데이터 또는 REST API 엔드포인트에서 JSON 데이터를 수집하고 정규화된 CSV로 변환하는 스킬
tags:
  - data
  - api
  - etl
---

# Data Fetcher Skill Instructions

본 스킬은 외부 API 엔드포인트로부터 데이터를 수집하고 Pandas/Python을 사용해 클렌징하는 표준 절차를 안내합니다.

## 표준 실행 워크플로우

1. **API 요청 및 응답 검증:**
   - `requests` 또는 `httpx` 라이브러리를 사용하여 타임아웃(기본 10초)과 함께 GET 요청을 수행합니다.
   - HTTP 상태 코드가 200이 아닌 경우 적절한 예외 로그를 출력합니다.
2. **데이터 파싱 및 스키마 검증:**
   - 응답 JSON 데이터의 필수 필드 누락 여부를 검사합니다.
3. **로컬 저장 및 캐싱:**
   - 정제된 데이터를 `data/output.json` 또는 `data/output.csv` 파일로 저장합니다.
'@ | Set-Content -Encoding UTF8 ".agents\skills\data-fetcher\SKILL.md"
```

#### 2. 스킬 목록 조회 및 실행

**모든 OS 동일**

```text
> /skills
> data-fetcher 스킬을 사용해서 예제 API 데이터를 가져오는 스크립트를 만들어줘
```

---

### Step 4: Rule 가드레일 및 코딩 컨벤션 적용 실습

에이전트가 코드를 작성하거나 Git 커밋을 수행할 때 반드시 지켜야 하는 **항시 적용 규칙(Always-on Rules)**을 설정합니다.

#### 1. Git 커밋 컨벤션 규칙 (`.agents/rules/commit-convention.md`)

#### macOS / Linux

```bash
cat << 'EOF' > .agents/rules/commit-convention.md
# Commit Message Guidelines

Git 커밋 메시지 작성 시 반드시 Conventional Commits 명세를 엄격히 준수해야 합니다:

1. 형식: `<type>(<scope>): <subject>` (예: `feat(auth): add jwt token validation`)
2. 허용 타입:
   - `feat`: 새로운 기능 추가
   - `fix`: 버그 수정
   - `docs`: 문서 수정
   - `style`: 코드 의미에 영향을 주지 않는 서식/공백 수정
   - `refactor`: 기능 추가나 버그 수정이 없는 코드 리팩토링
   - `test`: 테스트 코드 추가 및 수정
   - `chore`: 빌드 업무, 패키지 매니저 설정 변경
EOF
```

#### Windows (PowerShell)

```powershell
@'
# Commit Message Guidelines

Git 커밋 메시지 작성 시 반드시 Conventional Commits 명세를 엄격히 준수해야 합니다:

1. 형식: `<type>(<scope>): <subject>` (예: `feat(auth): add jwt token validation`)
2. 허용 타입:
   - `feat`: 새로운 기능 추가
   - `fix`: 버그 수정
   - `docs`: 문서 수정
   - `style`: 코드 의미에 영향을 주지 않는 서식/공백 수정
   - `refactor`: 기능 추가나 버그 수정이 없는 코드 리팩토링
   - `test`: 테스트 코드 추가 및 수정
   - `chore`: 빌드 업무, 패키지 매니저 설정 변경
'@ | Set-Content -Encoding UTF8 ".agents\rules\commit-convention.md"
```

#### 2. 에러 핸들링 가이드라인 (`.agents/rules/error-handling.md`)

#### macOS / Linux

```bash
cat << 'EOF' > .agents/rules/error-handling.md
# Error Handling & Logging Guidelines

1. **예외 무시 금지 (No Silent Swallowing):** `except Exception: pass`와 같은 빈 예외 처리 블록을 절대 작성하지 마십시오.
2. **명확한 진단 컨텍스트:** 에러 로그 출력 시 파일명, 함수명, 근본 원인을 명시하세요.
3. **구체적 예외 타입 사용:** 일반 `Exception` 대신 `ValueError`, `KeyError`, `FileNotFoundError` 등 구체적인 타입을 선언하세요.
EOF
```

#### Windows (PowerShell)

```powershell
@'
# Error Handling & Logging Guidelines

1. **예외 무시 금지 (No Silent Swallowing):** `except Exception: pass`와 같은 빈 예외 처리 블록을 절대 작성하지 마십시오.
2. **명확한 진단 컨텍스트:** 에러 로그 출력 시 파일명, 함수명, 근본 원인을 명시하세요.
3. **구체적 예외 타입 사용:** 일반 `Exception` 대신 `ValueError`, `KeyError`, `FileNotFoundError` 등 구체적인 타입을 선언하세요.
'@ | Set-Content -Encoding UTF8 ".agents\rules\error-handling.md"
```

---

### Step 5: MCP (Model Context Protocol) 서버 연동 실습

외부 데이터베이스(SQLite)나 시스템 리소스를 Antigravity에 연결하기 위해 Model Context Protocol 서버를 등록합니다.

#### 1. MCP 설정 파일 작성 (`mcp_servers.json`)

#### macOS / Linux

```bash
cat << 'EOF' > mcp_servers.json
{
  "mcpServers": {
    "sqlite": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sqlite",
        "--db-path",
        "./data/app.db"
      ]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "./src"
      ]
    }
  }
}
EOF
```

#### Windows (PowerShell)

```powershell
@'
{
  "mcpServers": {
    "sqlite": {
      "command": "npx.cmd",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sqlite",
        "--db-path",
        "./data/app.db"
      ]
    },
    "filesystem": {
      "command": "npx.cmd",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "./src"
      ]
    }
  }
}
'@ | Set-Content -Encoding UTF8 "mcp_servers.json"
```

#### 2. MCP 연결 상태 점검

**모든 OS 동일**

```text
> /mcp
# 활성화된 sqlite 및 filesystem MCP 도구/리소스 목록이 확인됩니다.
```

---

### Step 6: Lifecycle Hooks 및 Plugin 번들링 실습

에이전트의 도구 실행 전/후 시점에 자동 실행되는 훅(Hook)을 정의합니다.

#### 1. 훅 정의 파일 생성 (`hooks.json`)

#### macOS / Linux

```bash
cat << 'EOF' > hooks.json
{
  "hooks": [
    {
      "event": "post_tool_execution",
      "filter": {
        "tool": "replace_file_content"
      },
      "command": "npx prettier --write ."
    }
  ]
}
EOF
```

#### Windows (PowerShell)

```powershell
@'
{
  "hooks": [
    {
      "event": "post_tool_execution",
      "filter": {
        "tool": "replace_file_content"
      },
      "command": "npx.cmd prettier --write ."
    }
  ]
}
'@ | Set-Content -Encoding UTF8 "hooks.json"
```

#### 2. 플러그인 번들 매니페스트 생성 (`.agents/plugins/code-quality/plugin.json`)

#### macOS / Linux

```bash
cat << 'EOF' > .agents/plugins/code-quality/plugin.json
{
  "name": "code-quality-pack",
  "version": "1.0.0",
  "description": "보안 점검 에이전트, 컨벤션 규칙, 린트 훅이 통합된 코드 품질 패키지",
  "agents": ["../../agents/code-reviewer.md"],
  "rules": [
    "../../rules/commit-convention.md",
    "../../rules/error-handling.md"
  ]
}
EOF
```

#### Windows (PowerShell)

```powershell
@'
{
  "name": "code-quality-pack",
  "version": "1.0.0",
  "description": "보안 점검 에이전트, 컨벤션 규칙, 린트 훅이 통합된 코드 품질 패키지",
  "agents": ["../../agents/code-reviewer.md"],
  "rules": [
    "../../rules/commit-convention.md",
    "../../rules/error-handling.md"
  ]
}
'@ | Set-Content -Encoding UTF8 ".agents\plugins\code-quality\plugin.json"
```

---

## 5. 기능 통합 테스트 및 검증 시나리오

**모든 OS 동일**

1. **규칙 가드레일 검증:**
   - 프롬프트에 `src/test.py에 0으로 나누는 try-except 코드를 작성해줘` 요청
   - 에이전트가 `.agents/rules/error-handling.md` 규칙에 따라 `except Exception: pass`를 사용하지 않고 `ZeroDivisionError`와 로그 컨텍스트를 작성하는지 확인합니다.
2. **에이전트 위임 검증:**
   - `@code-reviewer`로 해당 코드를 분석하도록 하여 보안/성능 보고서가 정상 출력되는지 검증합니다.
3. **커밋 메시지 검증:**
   - 커밋 생성 요청 시 `feat(test): add zero division handling` 형식으로 작성되는지 확인합니다.

---

## 6. 실습 완료 체크리스트 (Verification Checklist)

- [ ] `.agents/agents/` 디렉터리에 커스텀 에이전트(`code-reviewer.md`) 생성 완료
- [ ] `.agents/skills/` 디렉터리에 온디맨드 스킬(`data-fetcher/SKILL.md`) 등록 완료
- [ ] `.agents/rules/` 디렉터리에 커밋 및 에러 핸들링 가드레일 적용 완료
- [ ] `mcp_servers.json`을 통한 외부 MCP 서버 구성 방법 숙지
- [ ] Progressive Disclosure 메커니즘과 우선순위(Precedence) 계층 이해 완료
- [ ] 자신의 OS(macOS/Linux 또는 Windows) 환경에 맞게 경로와 스크립트 명령이 정상 실행되는지 확인 완료
