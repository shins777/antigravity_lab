# Antigravity CLI 명령어 개요 및 사용법 가이드 (agy_command)

본 문서는 **Antigravity CLI**의 기본 실행 구조와 TUI 대화형 세션 내에서 슬래시(`/`)를 통해 호출할 수 있는 전체 명령어 체계를 기능별로 분류(Categorization)하고, 각 명령어의 개요(Overview), 사용법(Usage), 옵션/별칭(Options & Aliases), 실습 예제(Examples)를 정리한 가이드입니다.

---

## 1. 개요 및 학습 목표

- Antigravity CLI의 실행 구조(`agy [options]`) 및 대화형 쉘 환경을 이해합니다.
- `/` 슬래시 키를 통해 제공되는 핵심 내장 명령어 체계를 5가지 주요 카테고리로 분류하여 학습합니다.
- 세션 관리, 계획 수립, 서브에이전트 제어, 워크스페이스 분석, 시스템 설정 명령어를 자유롭게 활용할 수 있도록 실습합니다.

---

## 2. 사전 준비 사항 (Prerequisites)

- `agy_setting` 실습 완료 (Antigravity 패키지 설치 및 가상환경 활성화 상태)
- 터미널 환경에서 `agy` 명령어로 CLI 세션에 정상 진입 가능한 상태

---

## 3. Antigravity CLI 기본 시작 및 터미널 옵션

터미널에서 Antigravity CLI를 실행할 때 사용할 수 있는 기본 플래그 옵션입니다:

```bash

# Project root 디렉토리로 전환
cd ~/antigravity-lab/

# 기본 대화형 세션 시작
agy

# 특정 서브에이전트를 메인으로 지정하여 실행
agy --agent code-reviewer

# 사용할 기본 모델을 지정하여 실행
agy --model gemini-3.5-flash

# 특정 워크스페이스 디렉터리로 바로 진입
agy --dir ~/Documents/my_project/antigravity_lab
```

---

## 4. 슬래시(`/`) 명령어 카테고리별 상세 가이드

---

### 카테고리 1: 세션 및 대화 관리 (Conversation & Session Management)

대화 컨텍스트, 히스토리 롤백, 브랜치 분기 및 세션 전환을 제어하는 명령어 그룹입니다.

```
                    ┌── /resume (/switch, /conversation) : 이전 대화 복원/전환
                    ├── /rewind (/undo)                 : 직전 턴 상태로 롤백
                    ├── /clear (/new)                   : 대화 메모리 초기화
세션 및 대화 관리 ──----┼── /fork (/branch)                 : 현재 문맥 복제 새 브랜치 생성
                    ├── /rename                         : 활성 세션 이름 변경
                    ├── /btw                            : 메인 작업 중단 없이 사이드 질문
                    └── /copy                           : 직전 에이전트 응답 클립보드 복사
```

---

#### 1. `/resume`

- **Overview (개요):** 이전에 저장된 대화 세션 목록을 TUI 창으로 조회하고, 특정 세션을 선택하여 과거 대화 기록과 워크스페이스 상태를 복원합니다.
- **Aliases (별칭):** `/switch`, `/conversation`
- **Usage (사용법):**
  ```text
  /resume
  ```
- **Examples (예시):**
  1. 프롬프트에 `/resume` 입력 후 방향키(↑/↓)로 원하는 세션 선택 후 `Enter`
  2. 세션 검색창에 키워드 입력 후 필터링된 세션으로 즉시 전환

---

#### 2. `/rewind`

- **Overview (개요):** 에이전트가 잘못된 방향으로 코드를 수정했거나 이전 단계로 되돌리고 싶을 때, 대화 기록과 파일 수정 상태를 직전 체크포인트로 롤백합니다.
- **Aliases (별칭):** `/undo`
- **Usage (사용법):**
  ```text
  /rewind
  ```
- **Examples (예시):**
  ```text
  > /rewind
  Rewind Conversation
    generate a python code to sum 1 to given input number.
    if I give 10 to the function, what's the result?
  > how did you calculate the function? (current)
  ```
  - 원하는 턴을 선택하여 엔터를 누르면 이후에 실행된 파일 변경 및 프롬프트가 모두 롤백됩니다.

---

#### 3. `/clear`

- **Overview (개요):** 현재 세션의 대화 히스토리 및 컨텍스트 토큰 메모리를 초기화하여 깨끗한 상태에서 새 작업을 시작합니다. (디스크의 실제 소스 코드는 유지됩니다.)
- **Aliases (별칭):** `/new`
- **Usage (사용법):**
  ```text
  /clear
  ```
- **Examples (예시):**
  ```text
  > /clear

  ```

---

#### 4. `/fork`

- **Overview (개요):** 현재 시점의 대화 맥락과 파일 상태를 그대로 복제하여 독립적인 새로운 브랜치 세션을 생성합니다. (A/B 테스트 및 실험적 리팩토링 시 유용)
- **Aliases (별칭):** `/branch`
- **Usage (사용법):**
  ```text
  /fork
  ```
- **Examples (예시):**
  ```text
  > /fork
  ```

---

#### 5. `/rename`

- **Overview (개요):** 자동 생성된 세션 명칭을 직관적이고 구분하기 쉬운 이름으로 변경합니다.
- **Usage (사용법):**
  ```text
  /rename <새_세션명>
  ```
- **Examples (예시):**
  ```text
  > /rename auth-refactor-v2
  세션명이 'auth-refactor-v2'로 변경되었습니다.
  ```

---

#### 6. `/btw`

- **Overview (개요):** 백그라운드에서 실행 중인 메인 태스크나 빌드 작업을 중단하지 않고, 가벼운 사이드 질문을 격리된 블록에서 즉시 해결합니다.
- **Usage (사용법):**
  ```text
  /btw <질문 내용>
  ```
- **Examples (예시):**
  ```text
  > /btw Python의 asyncio.gather와 wait의 차이점이 뭐였지?
  ```

---

#### 7. `/copy`

- **Overview (개요):** 에이전트가 직전에 출력한 응답(계획서, 코드 스니펫, 요약 보고서 등)을 OS 클립보드로 복사합니다.
- **Usage (사용법):**
  ```text
  /copy
  ```
- **Examples (예시):**
  ```text
  > /copy
  마지막 응답이 클립보드에 복사되었습니다. (Ctrl+V / Cmd+V로 붙여넣기 가능)
  ```

---

### 카테고리 2: 계획 및 실행 제어 (Planning & Execution Control)

에이전트의 작업 전략 수립 방식, 자율 루프 실행, 인터뷰 모드 및 추론 깊이를 제어하는 명령어 그룹입니다.

```
                    ┌── /planning : 작업 전 영향도 분석 및 단계별 계획 수립
                    ├── /fast     : 계획 생략 즉시 코드 수정/도구 실행
                    ├── /goal     : 목표 100% 완료 시까지 자율 반복 루프 실행
계획 및 실행 제어 ──┼── /grill-me : 요구사항 구체화를 위한 대화형 인터뷰 진행
                    ├── /effort   : 모델 추론 깊이(low/medium/high) 설정
                    └── /schedule : 지연 실행 타이머 또는 주기적 Cron 작업 등록
```

---

#### 1. `/planning`

- **Overview (개요):** 코드를 즉시 수정하지 않고 요구사항 분석, 영향받는 파일 목록, 단계별 실행 계획(체크리스트)을 먼저 수립하여 사용자의 검토를 받습니다.
- **Usage (사용법):**
  ```text
  /planning <작업 지시사항>
  ```
- **Examples (예시):**
  ```text
  > /planning Vertex AI Agent Engine 배포를 위한 아키텍처 구성 및 코드 스캐폴딩
  ```

---

#### 2. `/fast`

- **Overview (개요):** 사전 계획 수립 단계를 생략하고 즉시 파일 수정 및 명령 도구를 실행하여 간단한 작업을 신속하게 처리합니다.
- **Usage (사용법):**
  ```text
  /fast <작업 지시사항>
  ```
- **Examples (예시):**
  ```text
  > /fast src/main.py의 15번째 줄 디버그 로그 삭제해줘
  ```

---

#### 3. `/goal`

- **Overview (개요):** 명시된 완료 조건(DoD: Definition of Done)이 충족될 때까지 에이전트가 `분석 ➜ 수정 ➜ 테스트 ➜ 오류 해결` 루프를 자율적으로 반복 수행합니다.
- **Usage (사용법):**
  ```text
  /goal <목표 및 명확한 종료 조건>
  ```
- **Examples (예시):**
  ```text
  > /goal pytest tests/test_auth.py가 100% 통과할 때까지 버그를 찾고 코드를 수정해줘
  ```

---

#### 4. `/grill-me`

- **Overview (개요):** 요구사항이 불명확하거나 아키텍처 결정이 필요할 때, 에이전트가 사용자에게 역으로 질문을 던져 요구사항을 명확히 정의하는 인터뷰 모드입니다.
- **Usage (사용법):**
  ```text
  /grill-me <구상 중인 기능 또는 아이디어>
  ```
- **Examples (예시):**
  ```text
  > /grill-me 실시간 트래픽을 모니터링하는 대시보드를 만들고 싶어
  ```

---

#### 5. `/effort`

- **Overview (개요):** 모델의 사고 과정(Thinking/Reasoning budget) 깊이를 `low`, `medium`, `high` 단계로 제어합니다.
- **Usage (사용법):**
  ```text
  /effort [low | medium | high]
  ```
- **Examples (예시):**
  ```text
  > /effort high    # 복잡한 동시성 버그 분석 시
  > /effort low     # 단순 텍스트 변환 및 오타 수정 시
  ```

---

#### 6. `/schedule`

- **Overview (개요):** 특정 작업을 지정한 시간 뒤(Delay) 또는 주기적인 크론(Cron) 스케줄로 백그라운드 큐에 등록합니다.
- **Usage (사용법):**
  ```text
  /schedule in <시간> "<프롬프트>"
  /schedule "<크론_표현식>" "<프롬프트>"
  ```
- **Examples (예시):**
  ```text
  > /schedule in 10m "현재 실행 중인 빌드 로그를 확인하고 요약해줘"
  > /schedule "0 9 * * *" "매일 아침 최신 브랜치 변경사항 요약"
  ```

---

### 카테고리 3: 서브에이전트, 툴 및 확장성 (Agents, Tools & Extensibility)

에이전트 페르소나 관리, 비동기 백그라운드 태스크, 스킬, 훅, MCP(Model Context Protocol) 연동을 다루는 명령어 그룹입니다.

```
                    ┌── /agents : 등록된 서브에이전트 목록 조회 및 호출
                    ├── /tasks  : 백그라운드 비동기 태스크 상태 점검 및 중단
서브에이전트, 툴    ├── /skills : 로컬 및 글로벌 스킬(Skill) 목록 조회
및 확장성           ├── /learn  : 최근 피드백 및 성공 패턴을 영구 규칙/스킬로 학습
                    ├── /mcp    : Model Context Protocol 서버 연결 관리
                    └── /hooks  : 이벤트 트리거 훅(Hooks) 설정 관리
```

---

#### 1. `/agents`

- **Overview (개요):** 프로젝트 및 글로벌 환경에 정의된 서브에이전트(예: `code-reviewer`, `db-optimizer`) 목록을 조회하고 직접 작업을 위임합니다.
- **Usage (사용법):**
  ```text
  /agents
  @[경로/에이전트.md] <요청사항>
  ```
- **Examples (예시):**
  ```text
  > /agents
  > @[.agents/agents/code-reviewer.md] 작성된 코드의 보안 취약점을 점검해줘
  ```

---

#### 2. `/tasks`

- **Overview (개요):** 백그라운드에서 비동기로 실행 중인 작업(장시간 테스트, 크론 스케줄러 등)의 목록과 로그를 확인하고 필요 시 중단(`kill`)합니다.
- **Usage (사용법):**
  ```text
  /tasks
  ```
- **Examples (예시):**
  ```text
  > /tasks
  Active Tasks:
  [task-102] Running - pytest test_all.py (elapsed: 1m 20s)
  ```

---

#### 3. `/skills`

- **Overview (개요):** 현재 워크스페이스(`.agents/skills/`) 및 전역(`~/.gemini/antigravity-cli/builtin/skills/`)에 활성화된 스킬 목록과 설명을 조회합니다.
- **Usage (사용법):**
  ```text
  /skills
  ```

---

#### 4. `/learn`

- **Overview (개요):** 사용자가 제공한 피드백이나 성공적으로 해결된 작업 컨텍스트를 분석하여 향후 작업에 재사용할 수 있는 규칙(`.agents/rules/`)이나 스킬로 자동 저장합니다.
- **Usage (사용법):**
  ```text
  /learn
  ```
- **Examples (예시):**
  ```text
  > /learn "우리 프로젝트는 commit 시 feat(scope): subject 규칙을 엄격히 적용해야 해"
  ```

---

#### 5. `/mcp`

- **Overview (개요):** 외부 데이터베이스, GitHub, Jira 등과 통신하는 Model Context Protocol(MCP) 서버의 연결 상태를 확인하고 관리합니다.
- **Usage (사용법):**
  ```text
  /mcp
  ```

---

#### 6. `/hooks`

- **Overview (개요):** 파일 쓰기 전/후, 커밋 전/후 등 특정 툴 이벤트 발생 시 자동으로 실행될 스크립트나 가드레일 훅을 관리합니다.
- **Usage (사용법):**
  ```text
  /hooks
  ```

---

### 카테고리 4: 작업 공간 및 코드 유틸리티 (Workspace & Code Utilities)

코드 변경 사항 비교, 프로젝트 전역 검색, 아티팩트 관리 및 컨텍스트 토큰 모니터링 명령어 그룹입니다.

```
                    ┌── /diff        : 스테이징/미커밋 코드 변경사항 인터랙티브 뷰어
                    ├── /codesearch  : 실시간 인덱스 기반 고속 코드 검색
작업 공간 및        ├── /open        : 특정 파일이나 변경된 코드를 외부 IDE로 열기
코드 유틸리티       ├── /add-dir     : 추가 워크스페이스 디렉터리 경로 등록
                    ├── /artifact    : 에이전트가 생성한 설계서, 다이어그램 등 산출물 조회
                    └── /context     : 현재 모델 컨텍스트 윈도우 토큰 사용량 시각화
```

---

#### 1. `/diff`

- **Overview (개요):** 에이전트가 수정한 파일의 변경 내역을 터미널 내에서 인터랙티브한 줄 단위 diff 뷰어로 검토합니다.
- **Usage (사용법):**
  ```text
  /diff
  ```

---

#### 2. `/codesearch`

- **Overview (개요):** 대규모 코드베이스 전체를 대상으로 고속 인덱싱 검색을 수행하여 함수, 클래스, 변수 선언 및 참조 위치를 찾습니다.
- **Usage (사용법):**
  ```text
  /codesearch <검색어>
  ```
- **Examples (예시):**
  ```text
  > /codesearch def authenticate_user
  ```

---

#### 3. `/open`

- **Overview (개요):** 특정 파일 또는 에이전트가 최근 수정한 파일 목록을 외부 에디터(VS Code, Cursor, Vim 등)로 엽니다.
- **Usage (사용법):**
  ```text
  /open <파일명 또는 경로>
  ```

---

#### 4. `/add-dir`

- **Overview (개요):** 모노레포 환경이나 외부 공유 라이브러리 폴더를 현재 워크스페이스 컨텍스트에 추가하여 에이전트가 읽고 분석할 수 있도록 합니다.
- **Usage (사용법):**
  ```text
  /add-dir <디렉터리 경로>
  ```

---

#### 5. `/artifact`

- **Overview (개요):** 계획서, 아키텍처 다이어그램(Mermaid), 보고서 등 세션 중 생성된 아티팩트 파일들을 확인하고 탐색합니다.
- **Usage (사용법):**
  ```text
  /artifact
  ```

---

#### 6. `/context`

- **Overview (개요):** 현재 세션의 컨텍스트 윈도우(토큰 소비 현황)를 시각적인 게이지 차트로 출력하여 한도 초과 여부를 점검합니다.
- **Usage (사용법):**
  ```text
  /context
  ```

---

### 카테고리 5: 환경 설정 및 시스템 관리 (Configuration & System Management)

추론 모델 선택, 권한 정책, 테마/단축키, 도움말 및 세션 종료를 담당하는 명령어 그룹입니다.

```
                    ┌── /model             : 활성 추론 모델(Gemini Pro / Flash) 선택
                    ├── /permissions       : 도구 실행 자율성(승인 모드) 설정
                    ├── /config (/settings): 통합 환경설정 패널 오픈
                    ├── /keybindings       : TUI 키보드 단축키 커스텀
환경 설정 및        ├── /statusline        : 하단 실시간 상태 표시줄 설정
시스템 관리         ├── /help              : 전체 명령어 및 단축키 안내 탭
                    ├── /antigravity-guide : 종합 공식 가이드 확인
                    ├── /changelog         : 최신 버전 릴리즈 노트 확인
                    ├── /feedback          : 버그 및 개선 피드백 제출
                    ├── /credits           : 오픈소스 라이선스 확인
                    ├── /logout            : 계정 로그아웃 및 토큰 캐시 삭제
                    └── /exit (/quit)      : Antigravity CLI 세션 종료
```

---

#### 1. `/model`

- **Overview (개요):** 대화 및 추론에 사용할 Gemini 모델(예: Gemini 3.6 Flash, Gemini 3.6 Pro 등)을 대화형 메뉴에서 전환합니다.
- **Usage (사용법):**
  ```text
  /model
  ```

---

#### 2. `/permissions`

- **Overview (개요):** 파일 생성, 코드 수정, 쉘 명령어 실행 시의 사용자 승인 모드(`request-review`, `always-proceed`, `strict`)를 설정합니다.
- **Usage (사용법):**
  ```text
  /permissions
  ```

---

#### 3. `/config`

- **Overview (개요):** CLI의 출력 상세도(Verbosity), 테마(Theme), 자동 완성 등 전반적인 환경설정 패널을 호출합니다.
- **Aliases (별칭):** `/settings`
- **Usage (사용법):**
  ```text
  /config
  ```

---

#### 4. `/help`

- **Overview (개요):** 전체 슬래시 명령어 목록과 키보드 단축키 안내를 탭 기반으로 제공합니다.
- **Usage (사용법):**
  ```text
  /help
  ```

---

#### 5. `/logout` 및 `/exit`

- **Overview (개요):** 계정 인증을 해제하거나 현재 CLI 세션을 안전하게 종료합니다.
- **Usage (사용법):**
  ```text
  /logout    # 계정 인증 해제
  /exit      # 세션 종료 (별칭: /quit)
  ```

---

## 5. 실습 체크리스트 (Verification Checklist)

- [ ] `/resume`을 실행하여 이전 세션 목록이 정상적으로 브라우징되는지 확인
- [ ] `/planning`을 사용하여 사전 계획서를 아티팩트로 생성해보았는지 확인
- [ ] `/effort` 명령어로 추론 강도를 `low`/`high`로 변경해보았는지 확인
- [ ] `/context`를 통해 현재 토큰 점유율을 확인해보았는지 확인
- [ ] `/model`을 통해 원하는 Gemini 모델로 정상 변경되는지 확인
