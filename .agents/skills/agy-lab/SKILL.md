---
name: agy_lab
description: Google Antigravity CLI(`agy`)를 설치부터 헤드리스 CI 자동화까지 단계별로 실습시키는 한국어 핸즈온 개발자 가이드. 설치·인증(키링/SSH OAuth/Gemini API 키), TUI 조작, settings.json, 키바인딩, 대화 관리(/rewind·/fork·/resume), 아티팩트 리뷰와 /diff, 권한 엔진(action(target) 규칙), 터미널 샌드박스, 서브에이전트(/agents·/tasks), 룰 파일(GEMINI.md/AGENTS.md), 스킬, 플러그인, 훅, MCP 서버, 헤드리스 모드(-p, json/stream-json, --json-schema, stdin 스트리밍), 문제 해결까지 모두 다룬다. 사용자가 Antigravity, agy, AGY CLI, Antigravity 터미널/CLI, Gemini CLI 마이그레이션, agy 실습/랩/워크숍/교육 자료, agy 설정·권한·MCP·플러그인·헤드리스 사용법을 언급하면 명시적으로 "가이드"를 요청하지 않더라도 반드시 이 스킬을 사용한다.
---

# agy_lab — Antigravity CLI 핸즈온 개발자 가이드

> 기준 문서: Antigravity CLI **v1.2.0** 공식 문서(antigravity.google/docs/cli/*) — 2026년 9월 기준 스냅샷.
> CLI는 백그라운드 자동 업데이트가 되므로, 명령/키가 다르게 동작하면 `?` 또는 `/help`로 현재 버전을 먼저 확인한다.

## 이 스킬을 사용하는 방법 (에이전트용 지침)

이 문서는 강사가 워크숍을 진행하듯 **실습(Lab) 단위**로 구성되어 있다. 사용자의 요청에 따라 다음과 같이 활용한다.

1. **전체 교육 과정 요청** → Lab 0부터 순서대로 진행하되, 각 Lab의 "✅ 확인" 체크리스트로 완료를 검증한 뒤 다음 Lab으로 넘어간다.
2. **특정 기능 질문** (예: "agy에서 MCP 붙이는 법") → 해당 Lab과 부록 A(레퍼런스)만 발췌해 답한다.
3. **오류 해결** → Lab 20(문제 해결) 표에서 증상을 먼저 매칭한다.
4. **실습 자료/교재 제작** → 이 문서의 구조(목표 → 실습 → 확인 → 팁)를 유지해 재구성한다.
5. 모든 설명은 **한국어**로 하되, 명령어·설정 키·파일 경로·키 이름은 원문 그대로 둔다(번역하면 동작하지 않는다).
6. 공식 문서끼리 서로 다르게 기술된 부분이 있다(부록 C). 해당 항목을 안내할 때는 불일치를 숨기지 말고 "실제 환경에서 `/help`로 확인"하라고 함께 알려준다.

## 목차

| Lab | 주제 | 핵심 산출물 |
|---|---|---|
| 0 | Antigravity CLI 개요 | 도구 선택 기준 이해 |
| 1 | 설치 | `agy` 바이너리 |
| 2 | 인증 | 로그인된 세션 / API 키 세션 |
| 3 | 첫 번째 에이전트 작업 | `agy-demo/main.py` |
| 4 | TUI 기본 조작 | 프롬프트 조작 숙련 |
| 5 | 설정(settings.json) | 개인화된 설정 파일 |
| 6 | 키바인딩 | `keybindings.json` |
| 7 | 대화 관리 | rewind / fork / resume 흐름 |
| 8 | 아티팩트 리뷰와 Diff | 검토·승인 워크플로 |
| 9 | 탐색 → 계획 → 실행, 검증 루프 | 테스트 주도 에이전트 작업 |
| 10 | 권한(Permissions) 엔진 | allow / ask / deny 정책 |
| 11 | 터미널 샌드박스 | OS 수준 격리 |
| 12 | 서브에이전트와 백그라운드 작업 | 병렬 작업 운영 |
| 13 | 룰 파일 (GEMINI.md / AGENTS.md) | 프로젝트 규칙 |
| 14 | 스킬 | 커스텀 슬래시 명령 |
| 15 | 플러그인 | 배포 가능한 번들 |
| 16 | 훅(Hooks) | 사전/사후 자동화 |
| 17 | MCP 서버 연결 | 외부 도구 연동 |
| 18 | 헤드리스 모드와 CI | 스크립트/파이프라인 연동 |
| 19 | 부가 기능 (상태줄·타이틀·음성·쿼터·크레딧) | 작업 환경 개선 |
| 20 | 문제 해결 | 트러블슈팅 런북 |
| 21 | 캡스톤 실습 | 종합 과제 |
| 부록 A~C | 레퍼런스 / 경로 지도 / 문서 불일치 | — |

---

## Lab 0. Antigravity CLI 개요

**목표:** CLI가 무엇이고 언제 Antigravity 2.0(데스크톱)을 대신 쓰는지 이해한다.

Antigravity CLI(`agy`)는 Antigravity의 경량 TUI(Terminal User Interface)다. Antigravity 2.0과 **동일한 에이전트 하네스**를 사용하므로 다단계 추론, 다중 파일 편집, 도구 호출, 대화 이력 기능이 똑같이 제공된다.

| 항목 | Antigravity CLI | Antigravity 2.0 |
|---|---|---|
| 주 인터페이스 | 키보드 중심 TUI | 비주얼 데스크톱 에디터/IDE |
| 성능 오버헤드 | 거의 없음, 매우 가벼움 | 일반 데스크톱 IDE 수준 |
| 워크플로 초점 | 빠른 로컬 반복, SSH, 헤드리스 | 전체 프로젝트 관리, 시각적 작업공간 |
| 탐색 방식 | 범용 키보드 단축키 | 마우스 + 멀티 패널 |
| 원격 사용성 | SSH, tmux 등 멀티플렉서 네이티브 지원 | 로컬 작업공간 또는 원격 개발 컨테이너 |

**두 제품 간 연동**
- **공유 에이전트 하네스**: 추론·도구 사용 개선이 양쪽에 동시에 반영된다.
- **설정 동기화**: 환경설정, 권한, 보안 설정이 자동 동기화된다. 한쪽에서 권한 규칙을 바꾸면 다른 쪽에도 즉시 반영된다.
- **대화 내보내기**: 터미널 세션이 복잡해지면 대화를 Antigravity 2.0으로 넘겨 시각적 편집기에서 이어갈 수 있다.

**Gemini CLI 사용자라면:** 첫 실행 온보딩에서 기존 Gemini CLI 확장·스킬·설정을 **1회 자동 가져오기**할 수 있다.

✅ **확인:** "SSH로 접속한 원격 서버에서 에이전트를 돌려야 한다면 어느 쪽?" → CLI.

---

## Lab 1. 설치

**목표:** OS별로 `agy`를 설치하고 PATH에서 실행되는지 확인한다.

### 1-1. macOS / Linux
`~/.local/bin/agy`에 설치된다.
```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

### 1-2. Windows
`C:\Users\<username>\AppData\Local\agy\bin`에 설치된다.

PowerShell:
```powershell
irm https://antigravity.google/cli/install.ps1 | iex
```
명령 프롬프트(CMD):
```cmd
curl -fsSL https://antigravity.google/cli/install.cmd -o install.cmd && install.cmd && del install.cmd
```

### 1-3. 설치 플래그
| 플래그 | 효과 |
|---|---|
| `--skip-aliases` | 셸 프로필의 기존 `agy`/`antigravity` 별칭을 정리·갱신하지 않는다 |
| `--skip-path` | 셸 프로필에 `PATH` 추가를 하지 않는다 (PATH를 직접 관리하는 경우) |

파이프 설치 시 플래그 전달 예:
```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash -s -- --skip-path
```

### 1-4. 설치 확인
```bash
which agy        # Windows: where agy
agy --help
```
`agy: command not found`가 나오면 → Lab 20-1.

### 1-5. 자동 업데이트
CLI에는 백그라운드 자가 업데이터가 내장되어 있다(15분 디바운스). 버전 고정이 필요한 CI 환경에서는 비활성화한다.
```bash
export AGY_CLI_DISABLE_AUTO_UPDATE=true
```

✅ **확인:** 새 터미널을 열어도 `agy`가 실행된다.

---

## Lab 2. 인증

**목표:** 로컬/원격/API 키 세 가지 인증 방식을 모두 경험한다.

### 2-1. 로컬: 키링 무음(silent) 로그인
`agy`를 실행하면 OS 키링(Apple Keychain, Linux Secret Service/dbus, Windows Credential Manager)을 먼저 조회한다.
- 유효한 토큰이 있으면 → 브라우저 없이 바로 로그인.
- 없으면 → 기본 브라우저가 열리고 승인된 계정으로 로그인.

### 2-2. 원격 SSH: 수동 OAuth 루프
SSH 환경은 자동 감지된다.
1. 원격 터미널에서 `agy` 실행
2. 출력된 인증 URL 복사
3. **로컬 PC 브라우저**에 붙여넣고 로그인
4. 브라우저에 표시된 영숫자 인증 코드 복사
5. 원격 터미널 프롬프트에 붙여넣기

### 2-3. Gemini API 키 사용 (헤드리스/CI 권장)
계정 세션 없이 Gemini API로 직접 요청한다. 키는 Google AI Studio에서 발급한다.

> ⚠️ `GEMINI_API_KEY`만 설정하면 **아무 효과가 없다.** 반드시 provider 설정과 함께 써야 한다.

1) `~/.gemini/antigravity-cli/settings.json`:
```json
{
    "modelProvider": "gemini"
}
```
2) 환경 변수 (영구 적용하려면 `~/.zshrc`/`~/.bashrc`에 추가):
```bash
export GEMINI_API_KEY="your-api-key"
```
3) 실행: `agy` → 로그인 화면 없이 바로 시작되고, 헤더에 계정 이메일 대신 **Gemini API key**가 표시된다.

**커스텀 엔드포인트** (Gemini 호환 게이트웨이 등):
```bash
export GOOGLE_GEMINI_BASE_URL="https://your-endpoint.example.com"
```

**기본(계정) 인증으로 복귀:** settings.json에서 `modelProvider`를 삭제하고 CLI 재시작.

| 증상 | 원인 | 해결 |
|---|---|---|
| 시작 시 `GEMINI_API_KEY` 미설정으로 종료 | `modelProvider: gemini`인데 키 없음 | 키를 export하거나 `modelProvider` 제거 |
| 설정이 무시되고 일반 로그인됨 | `modelProvider` 값 오타 | 허용 값은 `gemini` 하나뿐 |
| `GOOGLE_API_KEY`나 `.env`의 키가 무시됨 | CLI는 환경변수 `GEMINI_API_KEY`만 읽고 `.env`를 로드하지 않음 | 셸에서 `GEMINI_API_KEY` export |
| 세션 중 일반 모델 오류 | 키가 무효/폐기/모델 권한 없음 | AI Studio에서 키 확인. 시작 시엔 "비어있지 않은지"만 검사하므로 첫 대화에서야 드러남 |

### 2-4. 로그아웃
```
/logout
```
키링의 인증 프로필이 삭제된다. API 키 모드에서는 저장된 세션이 없으므로 효과가 없다.

✅ **확인:** 헤더에 계정 이메일(또는 "Gemini API key")이 보인다.

---

## Lab 3. 첫 번째 에이전트 작업 (공식 튜토리얼)

**목표:** 에이전트에게 코드를 생성시키고, 리뷰·승인·실행·종료의 전체 사이클을 1회 완주한다.

```bash
mkdir agy-demo && cd agy-demo
agy
```

1. 프롬프트 박스에 입력 후 `Enter`:
   ```
   Write a simple python script to fetch web page text
   ```
   에이전트가 작업공간을 읽고(비어 있음) 스크립트 생성 계획을 세우는 과정이 실시간으로 표시된다.
2. 생성 완료 알림이 뜨면 `Ctrl+R` → **Artifact Review** 화면
   - `↑`/`↓`로 `main.py` 선택
   - 전체 내용과 diff 확인
   - `Y`로 생성 승인, `Esc`로 패널 닫기
3. 실행 검증:
   ```
   Run the python script and show me the output
   ```
   에이전트가 `python3 main.py` 실행을 제안하면 `Y` → 출력이 터미널에 스트리밍된다.
4. 종료: `Ctrl+D`(프롬프트가 비어 있을 때) 또는 `/exit`. 종료 시 **이 세션을 재개하는 정확한 명령**이 출력되므로 메모해 둔다.

✅ **확인:** `agy-demo/main.py`가 존재하고 실행 결과를 봤다.

---

## Lab 4. TUI 기본 조작

**목표:** 프롬프트 입력의 생산성 기능을 손에 익힌다.

| 기능 | 방법 | 실습 |
|---|---|---|
| 파일 경로 자동완성 | `@` 입력 → 경로 제안 오버레이 | `@main.py 에 예외처리 추가해줘` |
| 셸 명령 직접 실행 | 프롬프트 맨 앞에 `!` | `!ls -la` |
| 도움말/명령 목록 | `?` 또는 `/help` | |
| 슬래시 명령 자동완성 | `/` 입력 후 `Tab` | `/re` + `Tab` |
| 여러 줄 입력 | `Shift+Enter`, `Ctrl+J`, `Alt+Enter` | 요구사항을 줄 단위로 작성 |
| 외부 에디터로 작성 | `Ctrl+G` (`$EDITOR` 실행) | 긴 프롬프트 작성 |
| 이미지/미디어 붙여넣기 | `Ctrl+V` | UI 버그 스크린샷 첨부 |
| 프롬프트 비우기 | `Esc` `Esc` (스트리밍 중이 아닐 때) | |
| 진행 중인 턴 중단 | `Esc` | 에이전트가 엉뚱한 방향일 때 즉시 |
| 도구 추론 상세 펼치기/접기 | `Ctrl+O` | |
| 화면 정리 | `Ctrl+L` | |
| 마지막 응답 복사 | `/copy` | |
| 컨텍스트 사용량 시각화 | `/context` | |
| 방해 없이 곁가지 질문 | `/btw <질문>` | `/btw 이 프로젝트 파이썬 버전 뭐야?` |
| 파일을 외부 에디터로 열기 | `/open <path>` | `/open main.py` |
| 작업공간 디렉터리 추가 | `/add-dir <path>` | 모노레포의 다른 패키지 추가 |
| 도구 호출 출력 줄이기 | `/config` → verbosity `low` | |

✅ **확인:** `@`로 파일을 지정하고, `!`로 명령을 실행하고, `Esc`로 턴을 중단해 봤다.

---

## Lab 5. 설정 (settings.json)

**목표:** 설정 파일 구조와 우선순위를 이해하고 나만의 설정을 만든다.

- 파일: `~/.gemini/antigravity-cli/settings.json` (평문 JSON)
- UI: `/config` 또는 `/settings` → 전체 화면 오버레이. 항목을 선택하면 즉시 디스크에 저장된다.
- **실행 플래그 오버라이드**: `--sandbox`, `--dangerously-skip-permissions` 같은 플래그가 설정보다 우선한다. 설정 화면에 "Sandbox Mode on overridden by `--sandbox`" 식으로 출처가 표시되며, 디스크 설정을 바꿔도 **재시작 전까지는 플래그가 적용**된다.

### 설정 키 전체 목록
| 키 | 타입 | 기본값 | 값 / 설명 |
|---|---|---|---|
| `colorScheme` | string | `"terminal"` | `light`, `solarized light`, `colorblind-friendly light`, `dark`, `solarized dark`, `colorblind-friendly dark`, `tokyo night`, `terminal` |
| `altScreenMode` | string | `"default"` | `default`(자동), `always`(대체 화면 강제), `never`(인라인 강제) |
| `toolPermission` | string | `"request-review"` | `request-review`, `proceed-in-sandbox`, `always-proceed`, `strict` (Lab 10) |
| `artifactReviewPolicy` | string | `"asks-for-review"` | `asks-for-review`, `agent-decides`, `always-proceed` (Lab 8) |
| `notifications` | boolean | `false` | 작업 완료 시 데스크톱 알림 + 터미널 벨 |
| `showTips` | boolean | `true` | 생성 중 팁 표시 |
| `showFeedbackSurvey` | boolean | `true` | 주기적 피드백 설문 |
| `editor` | string | `"auto"` | 외부 에디터: `auto`(`$EDITOR`), `vim`, `emacs`, 사용자 지정 |
| `editorMode` | string | `"default"` | 프롬프트 편집 방식: `default` 또는 `vim`(모달 편집) |
| `vimInsertFirst` | boolean | `false` | Vim 모드를 Insert로 시작, `Enter`로 제출. `editorMode: vim` 필요 |
| `allowNonWorkspaceAccess` | boolean | `false` | 파일 도구가 Git/작업공간 루트 밖에 접근 허용 |
| `enableTerminalSandbox` | boolean | `false` | 에이전트 명령을 OS 격리 환경에서 실행 (Lab 11) |
| `useG1Credits` | boolean | `false` | (외부 빌드 전용) 플랜 쿼터 소진 시 개인 AI 크레딧 사용 |
| `enableTelemetry` | boolean | `true` | 지표·크래시 로그 전송 |
| `verbosity` | string | `"high"` | `high`(생각·도구 출력 전체), `low`(최소 진행 표시) |
| `runningLightSpeed` | string | `"medium"` | 진행 애니메이션: `fast`, `medium`, `slow`, `off` |
| `modelProvider` | string | (없음) | `gemini` 설정 시 API 키 인증 (Lab 2-3) |
| `permissions` | object | (없음) | 세분화된 allow/ask/deny 규칙 (Lab 10) |

### 실습: 권장 시작 설정
```json
{
    "colorScheme": "tokyo night",
    "altScreenMode": "always",
    "toolPermission": "request-review",
    "notifications": true,
    "enableTerminalSandbox": true,
    "verbosity": "high"
}
```

**모델 선택:** `/model`로 기본 추론 모델을 고른다(세션 간 유지). 사용 가능한 모델 목록은 셸에서 `agy models`.

✅ **확인:** `/config`에서 colorScheme을 바꾸고 settings.json에 반영된 것을 `cat`으로 확인했다.

---

## Lab 6. 키바인딩

**목표:** 기본 단축키를 익히고 하나 이상 재정의한다.

- 파일: `~/.gemini/antigravity-cli/keybindings.json`, 또는 `/keybindings`로 대화형 편집
- 초기화: `keybindings.json` 삭제
- 한 액션에 여러 키 매핑 가능. 빈 배열 `[]`로 비활성화.
- 파일이 일부 깨져도 유효한 부분만 적용되고 나머지는 기본값으로 대체된다.
- `cli.exit`, `cli.enter`는 **비활성화 불가**.

전역 / 프롬프트 / 탐색 / 확인 키 전체 표는 **부록 A-2** 참조.

✅ **확인:** `/keybindings`로 단축키 하나를 바꾸고 동작을 확인한 뒤, 파일을 삭제해 기본값으로 되돌렸다.

---

## Lab 7. 대화 관리

**목표:** 실패한 시도를 버리지 않고 되감고, 분기하고, 복귀하는 흐름을 익힌다.

| 명령 | 별칭 | 용도 |
|---|---|---|
| `/rewind` | `/undo` | 대화 이력을 이전 체크포인트로 되감기 |
| `/fork` | `/branch` | 현재 대화를 별도 작업공간의 병렬 세션으로 복제 |
| `/resume` | `/switch`, `/conversation` | 대화 선택기로 이전 세션 재개/전환 (`←`/`→`로 페이지 이동) |
| `/rename <name>` | — | 현재 대화 이름 변경 |
| `/clear` | `/new` | 화면·컨텍스트 초기화, 새 대화 시작 |

**실습 시나리오: 안전한 실험**
1. 안정적인 상태에서 `/rename baseline-auth`
2. `/fork` → 분기 세션에서 과감한 리팩터링 시도
3. 실패하면 `/resume`으로 `baseline-auth`로 복귀
4. 원래 세션에서 빌드가 깨지는 연속 변경이 생겼다면 `/rewind`로 안정 지점까지 되감기

**종료 후 재개:** CLI 종료 시 해당 세션을 재개하는 명령이 자동 출력된다. 헤드리스에서는 `--continue`/`--conversation <ID>` (Lab 18).

✅ **확인:** fork한 세션과 원래 세션을 `/resume`으로 오갔다.

---

## Lab 8. 아티팩트 리뷰와 Diff

**목표:** "투명성을 통한 신뢰" 모델 — 에이전트의 계획·변경을 검토하고 승인한다.

- `Ctrl+R` 또는 `/artifact` → **Artifact Review 패널**
  - `y` 승인, `n` 거절, `A` 생성된 아티팩트 **전체 일괄 승인**
- `/diff` → **대화형 Diff 뷰어**: 변경사항·턴·커밋 단위로 확인하고 에이전트를 조향
- `/open <path>` → 결과 파일을 선호 에디터로 바로 열기

**리뷰 정책 (`artifactReviewPolicy`)**
| 값 | 동작 | 권장 상황 |
|---|---|---|
| `asks-for-review` (기본) | 코드 작성 전 항상 확인 | 학습, 중요한 코드베이스 |
| `agent-decides` | 에이전트가 동적으로 판단 | 익숙한 저위험 작업 |
| `always-proceed` | 확인 없이 진행 | 일회성 스크래치 프로젝트 |

✅ **확인:** 하나의 변경을 `n`으로 거절하고 이유를 프롬프트로 전달해 수정본을 받아 `y`로 승인했다.

---

## Lab 9. 탐색 → 계획 → 실행, 그리고 검증 루프

**목표:** 에이전트 정확도를 가장 크게 끌어올리는 두 가지 습관을 실습한다.

### 9-1. 검증 루프 (가장 효과적인 단일 기법)
에이전트에게 **스스로 확인할 수단**(테스트, 빌드, 포매터)을 준다.
1. 테스트 스위트가 있는지 확인
2. 없으면 테스트부터 작성시킨다
3. 구현 후 로컬 테스트 명령을 실행하도록 지시
4. 에이전트가 결과를 보고 자동으로 반복 수정하는 것을 지켜본다
```
> Implement feature X in main.py. Run npm test afterward to verify the build.
```

### 9-2. 탐색 → 계획 → 실행
- **탐색**: 코드 변경 전에 구조·정의 위치를 설명하게 한다
- **계획**: 대상 파일·의존성·변경 로직을 담은 구현 계획 아티팩트를 요청
- **실행**: 계획을 승인한 뒤 편집 적용
```
> Explore how our router resolves `/docs/:page`. Write down an implementation plan to add `/docs/best-practices`.
```

### 9-3. 작업 난이도별 모드 선택
| 명령 | 용도 |
|---|---|
| `/planning` | 복잡한 엔지니어링 작업을 위한 다중 턴 계획 생성 모드 |
| `/fast` | 추론 계획을 건너뛰는 빠른 모드 (간단한 수정) |
| `/boost <task>` | 다중 에이전트 심층 추론 (까다로운 버그, 레이스 컨디션, 알고리즘) |
| `/teamwork-preview <task>` (별칭 `/teamwork`) | 장기 프로젝트용 협업 에이전트 팀 (유료 플랜) |
| `/codesearch` | 코드 검색 명령 |

✅ **확인:** 테스트 없는 함수에 대해 "테스트 먼저 → 구현 → 테스트 실행" 흐름을 끝까지 돌렸다.

---

## Lab 10. 권한(Permissions) 엔진

**목표:** 자율성과 안전 사이의 균형을 정책으로 설계한다.

### 10-1. 전역 프리셋 (`toolPermission` 또는 `/permissions`)
| 프리셋 | 동작 |
|---|---|
| `request-review` (기본) | 쓰기·bash·웹 도구 실행 전 확인 |
| `proceed-in-sandbox` | 샌드박스 안에서 자동 진행, 위험 명령만 확인 |
| `always-proceed` | 확인 없음 (`--dangerously-skip-permissions`와 동일 효과) |
| `strict` | 읽기가 아닌 모든 작업마다 확인 |

### 10-2. 세분화 규칙: `action(target)`
`settings.json`의 `permissions` 아래 세 목록으로 평가한다. **우선순위: Deny > Ask > Allow.**
(예: `ask`에 `command(*)`, `allow`에 `command(git)`이 있으면 ask가 이겨서 git도 매번 확인한다.)

| 액션 | 대상 형식 | 매칭 방식 | 기본값 |
|---|---|---|---|
| `read_file` | `/path`, `dir`, `*` | 절대경로 또는 작업공간 기준 상대경로, 하위 재귀 | Ask (작업공간 내부는 자동 허용) |
| `write_file` | `/path`, `*` | read_file과 동일, 같은 경로의 read 권한 포함 | Ask (작업공간 내부는 자동 허용) |
| `read_url` | `domain`, `*` | 호스트 + 서브도메인 (`google.com` ⊃ `mail.google.com`), 경로 무시 | Ask |
| `execute_url` | `domain`, `*` | 웹 요소 조작(클릭·입력), 브라우저 워크플로 | Ask |
| `command` | `prefix`, `regex:pattern`, `*` | 기본은 단어 단위 접두사 리터럴 매칭 | Ask |
| `unsandboxed` | `prefix`, `regex:pattern`, `*` | 샌드박스 켜진 상태에서 격리 밖 실행 허용 | Ask |
| `mcp` | `server/tool`, `server/*`, `*` | 특정 MCP 도구 또는 서버 전체 | Ask |

**암묵 규칙**
- Write 허용 ⇒ 같은 경로 Read 허용
- Read 거부 ⇒ 같은 경로 Write 거부

**크로스 플랫폼**
- Windows 경로는 평가 전에 드라이브 문자 제거 + `\` → `/` 정규화
- PowerShell/CMD에서 단어 분리가 어려운 명령은 기본적으로 완전 일치 필요 → 하위 명령까지 허용하려면 `command(regex:git .*)`

### 10-3. 실습 정책
```json
{
    "permissions": {
        "allow": [
            "command(git)",
            "command(regex:npm run (build|lint|test))",
            "unsandboxed(git push)",
            "read_file(/var/log/app)",
            "write_file(src/)",
            "read_url(google.com)",
            "mcp(linter/*)"
        ],
        "deny": [
            "command(rm -rf)",
            "command(regex:curl .*)",
            "command(sudo)",
            "write_file(.git/)",
            "write_file(/home/user/.ssh)"
        ],
        "ask": ["command(*)", "execute_url(aws.amazon.com)", "mcp(sql/execute_mutation)"]
    }
}
```
> 위 예시는 `ask`에 `command(*)`가 있으므로 우선순위 규칙상 `command(git)` allow도 결국 확인을 요청한다. 실습에서 이 동작을 직접 관찰하고, git을 무확인으로 하고 싶다면 `ask`에서 `command(*)`를 빼 보라.

### 10-4. 대화형 승인 시 범위 확장
파일·URL·MCP 권한 확인 카드에서 **Allow 전에 대상 문자열을 직접 편집**해 범위를 넓힐 수 있다(예: `/project/file.txt` → `/project`). 편집된 범위는 해당 턴 동안 적용된다. 터미널 명령은 범위 편집 불가.

✅ **확인:** `command(sudo)`를 deny에 넣고 에이전트에게 sudo가 필요한 작업을 시켜 차단되는 것을 확인했다.

---

## Lab 11. 터미널 샌드박스

**목표:** 에이전트의 셸 명령을 OS 네이티브 기능으로 격리한다.

VM/컨테이너 없이 OS 기능을 사용하므로 시작 오버헤드가 없다.
| OS | 격리 메커니즘 |
|---|---|
| Linux | `nsjail` |
| macOS | `sandbox-exec` |
| Windows | `AppContainer` |

파괴적 파일 조작과 무단 외부 네트워크 요청으로부터 호스트를 보호한다.

**활성화 방법**
```json
{ "enableTerminalSandbox": true }
```
또는 1회성: `agy --sandbox`

**확인 프롬프트의 변화**
- 샌드박스 **켜짐**: "Yes, and run without sandbox restrictions" 옵션 → 신뢰하는 단일 명령만 격리 해제
- 샌드박스 **꺼짐**: "Yes, and run in sandbox" 옵션 → 위험해 보이는 명령만 격리 실행

**권장 조합:** `toolPermission: "proceed-in-sandbox"` + `enableTerminalSandbox: true` + 필요한 명령만 `unsandboxed(...)` allow.

✅ **확인:** 샌드박스를 켜고 확인 프롬프트에 격리 해제 옵션이 나타나는 것을 봤다.

---

## Lab 12. 서브에이전트와 백그라운드 작업

**목표:** 메인 대화를 막지 않고 병렬 작업을 운영한다.

- **서브에이전트**: 메인 에이전트가 문서 조사, 빌드, 수정 검증 같은 작업을 위해 자동으로 생성하는 독립·동시 세션. 코드 검색, 파일 편집, 터미널, 웹 검색 도구를 쓸 수 있으며, **어떤 도구·권한(MCP 사용, 파일 쓰기 여부)을 줄지는 메인 에이전트가 결정**한다.
- `/agents` → 에이전트 관리 패널: 실행 중/완료 서브에이전트의 상태(running, done, killed 등)와 현재 단계. 항목 선택 시 전체 대화·생각·도구 로그 상세 뷰. 커스텀 에이전트 전환도 여기서.
- `/tasks` → 백그라운드 셸 작업 모니터링, 로그 보기, 종료

**승인 처리 두 가지 경로**
1. **상세 뷰 승인**: 서브에이전트 상세 화면의 대기 목록에서 선택적 승인/거부. 승인 대기 중인 다음 서브에이전트로 바로 이동(텔레포트)하는 키가 있다(부록 C 참고: 문서에 따라 `Ctrl+J` 또는 `Alt+J`).
2. **Fast Path 알림**: 프롬프트 위에 알림이 뜨면 `Ctrl+K`로 메인 대화를 떠나지 않고 즉시 승인.

**실습 프롬프트 (팬아웃)**
```
src/ 아래 모든 모듈의 deprecated API 사용처를 병렬 서브에이전트로 나눠 조사하고, 결과를 모듈별 표로 합쳐줘.
```

✅ **확인:** `/agents`에서 서브에이전트 하나의 상세 로그를 열어봤다.

---

## Lab 13. 룰 파일 (GEMINI.md / AGENTS.md)

**목표:** 프로젝트 규칙을 에이전트에게 영구적으로 주입한다.

작업공간 루트에 `GEMINI.md` 또는 `AGENTS.md`를 만들면 에이전트가 **시작 시 자동으로 읽고** 변경 제안 전에 참고한다.

```markdown
# 프로젝트 규칙
## 구조
- 소스는 src/, 테스트는 tests/ 에 둔다.
## 스타일
- Python은 black + ruff 규칙을 따른다. 타입 힌트 필수.
## 검증
- 변경 후 반드시 `pytest -q` 를 실행한다.
## 금지/폐기
- utils/legacy_http.py 는 deprecated. 새 코드에서 import 금지.
```
플러그인의 `rules/` 디렉터리로도 규칙을 배포할 수 있다(Lab 15).

✅ **확인:** 룰 파일 작성 후 새 세션에서 "이 프로젝트 테스트 어떻게 돌려?"라고 물어 규칙대로 답하는지 확인했다.

---

## Lab 14. 스킬 (커스텀 슬래시 명령)

**목표:** 반복 작업을 마크다운 스킬로 만들어 `/명령`으로 호출한다.

스킬은 지시 프로토콜·스크립트·대상 리소스를 기술한 마크다운 파일이며, **등록되면 자동으로 슬래시 명령이 된다.**

### 14-1. 작업공간 스킬 (저장소와 함께 버전 관리)
```bash
mkdir -p .agents/skills
```
`.agents/skills/format-tests.md`:
```markdown
---
name: format-tests
description: Standardize and re-format Python unittest assertions
---
tests/ 아래 모든 unittest 파일에서:
1. assertEquals → assertEqual 로 교체한다.
2. assertTrue(a == b) 형태는 assertEqual(a, b) 로 바꾼다.
3. 변경 후 `python -m pytest -q` 로 검증하고 결과를 요약한다.
```
이 디렉터리에서 `agy` 실행 → `/format-tests` 사용 가능.

### 14-2. 전역 스킬 (모든 작업공간 공유)
`~/.gemini/antigravity-cli/skills/` 에 마크다운 파일을 두면 어느 디렉터리에서든 전역 슬래시 명령으로 로드된다.

### 14-3. 확인
`/skills` → 로드된 로컬·전역 스킬 목록

✅ **확인:** `/format-tests`가 `/` 자동완성에 나타나고 실행된다.

---

## Lab 15. 플러그인

**목표:** 스킬·에이전트·룰·MCP·훅을 하나의 배포 단위로 패키징한다.

### 15-1. 구조
설치 시 `~/.gemini/antigravity-cli/plugins/<plugin_name>/`에 스테이징되고 에이전트가 자동 탐색·로드한다.
```
~/.gemini/antigravity-cli/
├── plugins/
│   └── <plugin_name>/
│       ├── plugin.json         # 필수 마커 파일
│       ├── mcp_config.json     # 선택: MCP 서버 정의
│       ├── hooks.json          # 선택: 이벤트 훅
│       ├── skills/             # 선택: 스킬
│       ├── agents/             # 선택: 서브에이전트 정의
│       └── rules/              # 선택: 규칙
└── import_manifest.json        # 가져오기 추적 매니페스트
```

### 15-2. 매니페스트 `plugin.json`
```json
{
    "$schema": "https://antigravity.google/schemas/v1/plugin.json",
    "name": "my-plugin",
    "description": "A brief description of what my plugin does."
}
```
| 필드 | 필수 | 규칙 |
|---|---|---|
| `name` | 예 | 영숫자·하이픈·언더스코어만 (`^[a-zA-Z0-9-_]+$`). CLI 명령에서 참조하는 이름 |
| `description` | 아니오 | 목록에 표시되는 설명 |

스키마는 `additionalProperties: false` → **다른 필드를 넣으면 검증 실패**. `$schema`를 넣으면 VS Code/WebStorm에서 자동완성·검증이 된다.

### 15-3. 관리 명령 (`plugin` 또는 `plugins`)
```bash
agy plugin list                          # 설치된 플러그인과 로드된 구성요소
agy plugin install /path/to/local/plugin # 스테이징 설치
agy plugin disable <plugin_name>         # 자산 유지, 도구만 중지
agy plugin enable <plugin_name>
agy plugin uninstall <plugin_name>       # 디렉터리 삭제 + 레지스트리 정리
```

### 15-4. 실습: 팀 공용 플러그인 만들기
```bash
mkdir -p ~/lab/team-kit/{skills,rules}
cat > ~/lab/team-kit/plugin.json <<'EOF'
{
  "$schema": "https://antigravity.google/schemas/v1/plugin.json",
  "name": "team-kit",
  "description": "팀 공용 스킬과 코딩 규칙"
}
EOF
cp .agents/skills/format-tests.md ~/lab/team-kit/skills/
agy plugin install ~/lab/team-kit
agy plugin list
```

✅ **확인:** `agy plugin list`에 `team-kit`이 보이고, disable/enable을 토글해 봤다.

---

## Lab 16. 훅(Hooks)

**목표:** 에이전트 동작 직전/직후에 자동 스크립트를 끼워 넣는다.

- 용도: 사전 점검(pre-flight), 사후 포맷팅(예: 파일 작성 후 `prettier` 실행)
- 정의 위치: 플러그인의 `hooks.json` 또는 기본 `settings.json`
- 확인: `/hooks` → 로드된 활성 훅 목록

> CLI 문서에는 `hooks.json`의 상세 스키마가 실려 있지 않다. 스키마는 Antigravity 공통 Hooks 문서(antigravity.google/docs/hooks)를 참조하고, 작성 후 반드시 `/hooks`로 로드 여부를 확인한다.

✅ **확인:** `/hooks`를 열어 현재 로드된 훅을 확인했다.

---

## Lab 17. MCP 서버 연결

**목표:** 외부 DB·API·도구를 에이전트에 연결한다.

### 17-1. 관리 방법
- `/mcp` → **MCP Manager 오버레이**: 서버별 상태(활성/연결 끊김/로딩), 설정 재로드, 실시간 연결 로그
- 설정 파일 직접 편집:
  - 전역: `~/.gemini/config/mcp_config.json`
  - 작업공간: `.agents/mcp_config.json`
  - 플러그인: `<plugin>/mcp_config.json`

### 17-2. 설정 구조
```json
{
  "mcpServers": {
    "sqlite-explorer": {
      "command": "node",
      "args": ["/usr/local/bin/sqlite-mcp-server.js"],
      "env": { "SQLITE_DB_PATH": "/var/data/app.db" }
    },
    "my-remote-server": {
      "serverUrl": "https://api.example.com/mcp/",
      "headers": { "Authorization": "Bearer YOUR_API_TOKEN" }
    }
  }
}
```
| 속성 | 설명 |
|---|---|
| `command` | (전송 방식 택1) `stdio` 실행 파일 경로 |
| `serverUrl` | (전송 방식 택1) 원격 Streamable HTTP / SSE URL. **`url`, `httpUrl` 같은 레거시 필드는 미지원** |
| `args` | stdio 인자 |
| `env` | stdio 프로세스 환경변수 |
| `cwd` | stdio 작업 디렉터리 |
| `headers` | 원격 서버용 HTTP 헤더 |
| `authProviderType` | `"google_credentials"` → Google ADC 사용 |
| `oauth` | `clientId`, `clientSecret` 수동 지정 |
| `disabled` | 설정 유지한 채 일시 비활성화 |
| `disabledTools` | 모델에 숨길 도구 이름 배열 |

### 17-3. 인증
- **Google ADC**:
  ```json
  { "mcpServers": { "my-gcp-service": {
      "serverUrl": "https://example.googleapis.com/mcp/",
      "authProviderType": "google_credentials" } } }
  ```
  ```bash
  gcloud auth application-default login
  gcloud auth application-default set-quota-project {QUOTA_PROJECT}
  ```
- **OAuth**: 동적 클라이언트 등록(DCR) 지원 서버는 `serverUrl`만 있으면 자동. 미지원 서버는 `oauth.clientId/clientSecret`을 넣고 리디렉트 URI `https://antigravity.google/oauth-callback`을 제공자에 등록. 토큰은 `~/.gemini/antigravity/mcp_oauth_tokens.json`에 저장되며 만료 시 자동 갱신.
- **커스텀 헤더**: `headers` 객체에 API 키/Bearer 토큰.

### 17-4. MCP 권한
미설정 MCP 도구는 기본 **Ask**. 신뢰 서버는 allow로 올린다.
```json
{ "permissions": {
    "allow": ["mcp(github/*)"],
    "ask":   ["mcp(sql/execute_mutation)"] } }
```

### 17-5. 대표 지원 서버 (MCP Store)
- DB/스토리지: AlloyDB, BigQuery, Bigtable, ClickHouse, Cloud SQL, Dataplex, MCP Toolbox for Databases, MongoDB, Neon, Pinecone, Prisma, Redis, Spanner, Supabase
- 개발도구/CI·CD: Apigee, Atlassian, Cloud CLI Execution, GitHub, GitLab Orbit, GKE, Harness, Heroku, Linear, Netlify, Postman, SonarQube 등
- 프런트엔드/디자인: Chrome DevTools, Dart, Figma Dev Mode, Locofy, Lovable, Mobbin
- 분석/AI/클라우드: Firebase, Looker, Notion, PostHog, Sequential Thinking, Splunk, Stripe 등

✅ **확인:** 작업공간 `.agents/mcp_config.json`에 서버 하나를 추가하고 `/mcp`에서 활성 상태를 확인했다.

---

## Lab 18. 헤드리스 모드와 CI

**목표:** `agy`를 스크립트·파이프라인 부품으로 사용한다.

> 사전 조건: 헤드리스는 캐시된 인증을 쓴다. 대화형 `agy`로 한 번 로그인하거나, CI라면 `GEMINI_API_KEY` + `modelProvider: gemini`(Lab 2-3)를 사용한다. 미인증 상태의 비대화형 환경에서는 멈추지 않고 `authentication required`로 종료한다.

### 18-1. 단발 실행
```bash
agy -p "In one sentence, what is a git rebase?"      # -p = --print = --prompt
answer=$(agy -p "Name three popular version control systems, comma-separated.")
agy -p "Review this git diff and draft a conventional commit message" --cwd $(pwd)
```
응답은 `stdout`, 진단(오류·인증·진행·권한 알림)은 `stderr`로 분리된다.

### 18-2. 출력 형식 `--output-format`
| 형식 | stdout | 용도 |
|---|---|---|
| `text` (기본) | 응답 텍스트 | 사람이 읽기, 간단한 스크립트 |
| `json` | 완료 시 JSON 객체 1개 | 결과 + 메타데이터 수집 |
| `stream-json` | NDJSON 이벤트 스트림 | 진행·도구·토큰 실시간 관찰 |

`json` 봉투 필드: `conversation_id`, `status`, `response`, `error`(실패 시), `duration_seconds`, `num_turns`, `structured_output`/`json_schema`(스키마 사용 시), `usage`(`input_tokens`, `output_tokens`, `thinking_tokens`, `cache_read_tokens`, `total_tokens`).

### 18-3. 구조화 출력 `--json-schema`
스키마 문자열, `.json` 파일 경로, 또는 원시 타입명(`string`, `number`, `integer`, `boolean`)을 받는다.
```bash
agy -p "Parse the semantic version string v2.14.3 into an object with integer fields major, minor, and patch." \
  --output-format json \
  --json-schema '{"type":"object","properties":{"major":{"type":"integer"},"minor":{"type":"integer"},"patch":{"type":"integer"}},"required":["major","minor","patch"]}' \
  | jq '.structured_output'
```

### 18-4. stream-json 이벤트
`init`(1회) → `step_update`(여러 번) → `result`(1회, json과 같은 형태).
- `init`: `cwd`, `tools`, `permission_mode`, (`model`, `agent`, `json_schema` 지정 시)
- `step_update`: `step_index`, `state`(`ACTIVE`/`DONE`), `step_type`(`user_input`, `agent_response`, `tool`, `checkpoint`), `tool_name`, `text_delta`, `usage`, `tool_info`(`name`, `parameters`, `output`, `error`), `subagent_info`

jq 레시피:
```bash
# 응답 텍스트만
agy -p "..." --output-format json | jq -r '.response'
# 스트리밍 텍스트 이어붙이기 (-j 로 개행 방지)
agy -p "..." --output-format stream-json | jq -j 'select(.event=="step_update") | .step_update.text_delta // empty'
# 최종 토큰 사용량
agy -p "..." --output-format stream-json | jq 'select(.event=="result") | .result.usage'
```

### 18-5. 대화 이어가기
헤드리스는 기본적으로 상태가 없다.
```bash
agy -p "Now explain your previous answer in more detail" --continue   # 또는 -c
agy -p "Summarize what we discussed" --conversation <conversation_id>
```

### 18-6. stdin 스트리밍 (한 프로세스에서 다중 턴)
`--input-format stream-json`은 **반드시** `--output-format stream-json`과 함께 쓴다. 프로세스가 한 번만 뜨므로 `--continue` 반복보다 훨씬 빠르다.
```bash
printf '%s\n' \
  '{"event":"user","message":{"content":"Reply with exactly: one"}}' \
  '{"event":"user","message":{"content":"Reply with exactly: two"}}' \
  | agy --input-format stream-json --output-format stream-json \
  | jq -r 'select(.event=="result") | "\(.result.num_turns): \(.result.response)"'
```
`content`는 문자열 또는 `[{"type":"text","text":"..."}]`. **`text` 외 블록 타입은 세션 오류 종료.**

Python으로 대화형 제어:
```python
import json, subprocess

proc = subprocess.Popen(
    ["agy", "--input-format", "stream-json", "--output-format", "stream-json"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1,
)

def ask(prompt):
    proc.stdin.write(json.dumps({"event": "user", "message": {"content": prompt}}) + "\n")
    proc.stdin.flush()
    for line in proc.stdout:
        event = json.loads(line)
        if event["event"] == "result":
            return event["result"]["response"]

first = ask("Name one popular version control system. Answer with one word.")
print(ask(f"Name a competitor to {first.strip()}. Answer with one word."))
proc.stdin.close()   # stdin 닫기 = 세션 정상 종료 (exit 0)
proc.wait()
```

| 입력 이상 | 결과 | 종료코드 |
|---|---|---|
| 알 수 없는 `event` 이름 | 경고 후 건너뜀 (상위 호환) | — |
| `control_request`/`control_response` | ERROR, 세션 종료 | 2 |
| CLI 자체 처리 슬래시 명령(`/model`, `/usage`) | ERROR, 세션 종료 | 2 |
| `event` 필드 없음 / 잘못된 JSON / text 외 블록 | ERROR, 세션 종료 | 1 |

**흔한 실수**
- `json`/`text` 출력과 조합 → 마지막 턴 외 전부 유실. 항상 `stream-json`.
- `-p`로 프롬프트 전달 → 무시됨. stdin의 `user` 메시지로 보낸다.
- `num_turns`/`usage`/`duration_seconds`를 턴 단위로 착각 → **세션 누적값**이다. 현재 턴 텍스트는 `response`.
- 프로세스 종료를 기다린 뒤 stdout 읽기 → stdin을 닫기 전엔 끝나지 않아 멈춘다. 줄 단위로 읽는다.

### 18-7. 모델·추론 강도·에이전트 지정
```bash
agy models                 # 모델 슬러그 목록
agy agents                 # 에이전트 목록
agy -p "Reverse the string antigravity." --model <slug>
agy -p "Outline a plan to add caching to this service." --effort high   # low | medium | high
agy -p "Review this function for edge cases." --agent <agent-name>
```
대화형 UI와 달리 헤드리스는 **알 수 없는 모델에 대해 폴백하지 않고** exit 1 + `ERROR`로 실패한다(파이프라인이 조용히 다른 모델로 돌지 않게).

### 18-8. 헤드리스 권한
확인 프롬프트를 띄울 수 없으므로 정책으로 처리된다. 승인이 필요한 도구는 **soft-deny**(실행은 계속, exit 0, `stderr`에 허용 방법 안내). 작업공간 파일 읽기/쓰기는 자동 허용, 셸 명령은 기본 Ask → soft-deny.
- 권장: `permissions.allow`에 필요한 것만 사전 허용
- 최후 수단: `--dangerously-skip-permissions` (모든 도구 자동 승인 — 신뢰 가능한 프롬프트·격리 환경에서만). `--sandbox`와 함께 쓰는 것을 권장.

### 18-9. 종료 코드와 상태
성공 0, 실패는 0이 아니며 `stderr`에 사유. `status` 값: `SUCCESS`, `ERROR`, `CANCELED`, `INTERRUPTED`, `INVALID`, `WAITING`, `RUNNING`.
기본 대기 한도 5분 → `--print-timeout 15m`로 조정.

### 18-10. CI 예제
```bash
#!/usr/bin/env bash
set -euo pipefail

result=$(agy -p "Name three popular version control systems, comma-separated." \
  --output-format json \
  --print-timeout 10m)

status=$(echo "$result" | jq -r '.status')
if [[ "$status" != "SUCCESS" ]]; then
  echo "Agent run failed: $(echo "$result" | jq -r '.error')" >&2
  exit 1
fi
echo "$result" | jq -r '.response' > result.txt
```

### 18-11. git 훅 실습 (prepare-commit-msg)
```bash
cat > .git/hooks/prepare-commit-msg <<'EOF'
#!/usr/bin/env bash
[ -n "$2" ] && exit 0   # -m 등으로 메시지가 이미 있으면 건너뜀
git diff --cached | agy -p "Draft a conventional commit message for the staged diff above. Output only the message." > "$1" || true
EOF
chmod +x .git/hooks/prepare-commit-msg
```
> stdin 파이프 + `-p` 조합으로 diff가 컨텍스트에 전달되는지는 버전별로 확인한다. 안 되면 `-p "$(git diff --cached) ..."` 처럼 프롬프트에 직접 포함한다.

✅ **확인:** CI 스크립트가 성공 시 `result.txt`를 만들고, 잘못된 `--model`에서 exit 1로 실패한다.

---

## Lab 19. 부가 기능

| 기능 | 명령 | 내용 |
|---|---|---|
| 상태 표시줄 | `/statusline` | 상태 바 지표 사용자 지정. CWD·모델·토큰·상태 등 JSON 메타데이터를 **사용자 셸 스크립트로 파이프**해 동적 상태줄 생성 가능 |
| 터미널 창 제목 | `/title [on/off]` | 창 제목 자동 갱신 토글/설정. 상태줄과 같은 방식으로 스크립트 연동 가능 |
| 음성 받아쓰기 | `/voice` (별칭 `/record`), `F5` | 마이크로 프롬프트 받아쓰기 시작/중지 |
| 모델 쿼터 | `/usage` (별칭 `/quota`) | 모델 쿼터 사용량 확인 |
| AI 크레딧 | `/credits` | 남은 크레딧과 구매 링크. `useG1Credits: true`면 쿼터 소진 후 개인 크레딧 사용 |
| Vim 편집 | `editorMode: "vim"` | 프롬프트 모달 편집 (`vimInsertFirst`로 Insert 시작) |
| 피드백 | `/feedback` | 피드백 제출 패널 |
| 일시 중단 | `Ctrl+Z` | CLI를 터미널 백그라운드로 (`fg`로 복귀) — 부록 C 참고 |

✅ **확인:** `/usage`로 쿼터를 확인하고 `/statusline`을 열어봤다.

---

## Lab 20. 문제 해결 런북

| 증상 | 원인 | 해결 |
|---|---|---|
| `agy: command not found` | 설치 경로가 PATH에 없음 | 20-1 |
| `Error: failed to retrieve token: secret keyring is locked` / DBUS 경고 / 멈춤 | 키링 잠김 또는 헤드리스 | 20-2 |
| SSH에서 `Ctrl+V` 붙여넣기 실패 (`local pasteboard is empty or unreachable`) | SSH가 그래픽 클립보드를 전달하지 않음 | 20-3 |
| `another background updater process is already active (update.lock)` | 업데이터 잠금 잔존/권한 문제 | 20-4 |
| `GEMINI_API_KEY` 관련 시작 실패 | provider/키 불일치 | Lab 2-3 표 |
| 헤드리스에서 명령이 실행 안 됨 (exit 0) | soft-deny | Lab 18-8 |
| 헤드리스 `authentication required` | 캐시된 인증 없음 | 대화형 로그인 1회 또는 API 키 |
| MCP 원격 서버 연결 안 됨 | `url`/`httpUrl` 레거시 필드 사용 | `serverUrl`로 변경 |
| 플러그인 설치 실패 | `plugin.json` 누락/이름 규칙 위반/추가 필드 | Lab 15-2 |

### 20-1. PATH 설정
macOS/Linux — `~/.zshrc` 또는 `~/.bashrc` 끝에:
```bash
export PATH="$HOME/.local/bin:$PATH"
```
```bash
source ~/.zshrc
```
> 공식 문서는 `"~/.local/bin:$PATH"`로 표기하지만, 큰따옴표 안의 `~`는 확장되지 않아 zsh 등에서 동작하지 않을 수 있다. `$HOME`을 쓰는 것이 안전하다.

Windows(PowerShell, 관리자) — 설치 경로에 맞춰 추가한 뒤 터미널 재시작:
```powershell
[System.Environment]::SetEnvironmentVariable("Path", [System.Environment]::GetEnvironmentVariable("Path", "User") + ";$env:LOCALAPPDATA\agy\bin", "User")
```
> 문제 해결 문서는 `C:\Program Files\Google\antigravity-cli`를 예시로 들지만, 설치 스크립트 기본 경로는 `%LOCALAPPDATA%\agy\bin`이다. 실제 `agy.exe` 위치를 `Get-ChildItem`으로 확인 후 그 경로를 넣는다.

### 20-2. 키링 권한
**macOS**: 키체인 접근 앱 → `Antigravity CLI` 항목 → 정보 가져오기 → 접근 제어 탭에서 `agy` 허용 확인. 헤드리스 SSH라면:
```bash
security unlock-keychain -p "your_keychain_password" login.keychain
```
**Linux**: GNOME Keyring/KWallet 잠금 해제 확인. 헤드리스/SSH에선 D-Bus 세션 시작:
```bash
export $(dbus-launch)
```
**대안**: 키링 문제가 반복되는 서버/CI는 Gemini API 키 인증(Lab 2-3)으로 우회한다.

### 20-3. SSH 클립보드
1. iTerm2 또는 Ghostty 사용
2. iTerm2: 환경설정(`Cmd+,`) → General → Selection → "Applications in terminal may access clipboard" 체크 (OSC 52)
3. tmux:
   ```
   set -s set-clipboard on
   ```

### 20-4. 자가 업데이터 잠금
업데이터는 `~/.gemini/antigravity-cli/updater/`의 `last_check.timestamp`(15분 TTL)와 `update.lock`을 사용한다.
```bash
rm -f ~/.gemini/antigravity-cli/updater/update.lock   # 잠금 해제
export AGY_CLI_DISABLE_AUTO_UPDATE=true               # 자동 업데이트 끄기
```
설치 디렉터리(`~/.local/bin/` 또는 `%LOCALAPPDATA%\agy\bin`)에 사용자 쓰기 권한이 있는지 확인한다.

---

## Lab 21. 캡스톤 실습

**과제:** 작은 Python CLI 프로젝트에 대해 아래를 모두 수행한다.

1. `mkdir capstone && cd capstone && git init` 후 `AGENTS.md` 작성 (구조·스타일·`pytest -q` 검증 규칙)
2. `settings.json`: `toolPermission: proceed-in-sandbox`, `enableTerminalSandbox: true`, `permissions.allow`에 `command(git)`, `command(regex:python -m pytest.*)`, `deny`에 `command(sudo)`, `command(rm -rf)`
3. `/planning` 모드로 "할 일(todo) 관리 CLI" 구현 계획 요청 → 계획 아티팩트 검토 후 승인
4. 테스트 먼저 작성 → 구현 → 테스트 실행 루프 (Lab 9)
5. `/rename capstone-main` → `/fork`로 SQLite 저장소 버전 실험 → 결과 비교 후 `/resume`으로 선택
6. `/diff`로 전체 변경 검토, `Ctrl+R`로 남은 아티팩트 `A` 일괄 승인
7. `.agents/skills/release-notes.md` 스킬을 만들어 `/release-notes`로 변경 요약 생성
8. 스킬과 룰을 `capstone-kit` 플러그인으로 패키징해 `agy plugin install`
9. `.agents/mcp_config.json`에 사용 가능한 MCP 서버 하나 연결, `/mcp`로 상태 확인
10. CI 스크립트: `agy -p ... --output-format json --json-schema` 로 "테스트 실패 개수(integer)"를 구조화 출력받아 0이 아니면 exit 1

**평가 체크리스트**
- [ ] 모든 쓰기/명령이 정책대로 허용·확인·차단되었다
- [ ] 테스트가 녹색이다
- [ ] fork/resume 흐름을 설명할 수 있다
- [ ] `/release-notes`가 동작한다
- [ ] `agy plugin list`에 `capstone-kit`이 있다
- [ ] CI 스크립트가 성공/실패를 올바르게 판정한다

---

## 부록 A. 레퍼런스

### A-1. 슬래시 명령 전체
| 명령 | 분류 | 별칭 | 용도 |
|---|---|---|---|
| `/add-dir <path>` | 유틸 | — | 작업공간에 디렉터리 추가 |
| `/agents` | 도구·작업 | — | 에이전트 관리 패널 (커스텀 에이전트 전환, 서브에이전트 모니터링) |
| `/artifact` | 도구·작업 | — | 아티팩트 리뷰 패널 |
| `/boost <task>` | 추론 | — | 다중 에이전트 심층 추론 |
| `/btw <query>` | 유틸 | — | 메인 대화를 방해하지 않는 곁가지 질문 |
| `/clear` | 유틸 | `/new` | 화면·대화 컨텍스트 초기화 |
| `/codesearch` | 유틸 | — | 코드 검색 |
| `/config` | 설정 | `/settings` | 설정 편집 오버레이 |
| `/context` | 유틸 | — | 컨텍스트 사용량 시각화 |
| `/copy` | 유틸 | — | 마지막 응답 클립보드 복사 |
| `/credits` | 계정 | — | 남은 크레딧·구매 링크 |
| `/diff` | 유틸 | — | 대화형 Diff 뷰어 |
| `/exit` | 코어 | `/quit` | TUI 종료 |
| `/fast` | 설정 | — | 빠른 모드 (추론 계획 생략) |
| `/feedback` | 유틸 | — | 피드백 패널 |
| `/fork` | 대화 | `/branch` | 대화를 병렬 세션으로 복제 |
| `/help` | 유틸 | — | 명령·단축키 도움말 (`?`도 동일) |
| `/hooks` | 도구·작업 | — | 활성 훅 목록 |
| `/keybindings` | 설정 | — | 단축키 편집기 |
| `/logout` | 계정 | — | 로그아웃, 키링 토큰 삭제 |
| `/mcp` | 도구·작업 | — | MCP 서버 관리자 |
| `/model` | 설정 | — | 기본 추론 모델 선택 (유지됨) |
| `/open <path>` | 유틸 | — | 기본 에디터로 파일 열기 |
| `/permissions` | 설정 | — | 도구 권한 관리 패널 |
| `/planning` | 설정 | — | 다중 턴 계획 생성 모드 |
| `/rename <name>` | 대화 | — | 대화 이름 변경 |
| `/resume` | 대화 | `/switch`, `/conversation` | 대화 선택기 |
| `/rewind` | 대화 | `/undo` | 이전 메시지로 되감기 |
| `/skills` | 도구·작업 | — | 로컬·전역 스킬 목록 |
| `/statusline` | 설정 | — | 상태 바 사용자 지정 |
| `/tasks` | 도구·작업 | — | 백그라운드 셸 작업 관리 |
| `/teamwork-preview <task>` | 추론 | `/teamwork` | 협업 에이전트 팀 (유료 플랜) |
| `/title [on/off]` | 설정 | — | 창 제목 갱신 토글 |
| `/usage` | 유틸 | `/quota` | 모델 쿼터 사용량 |
| `/voice` | 유틸 | `/record` | 음성 받아쓰기 |
| `/<skill-name>` | 스킬 | — | 등록된 스킬 실행 |

### A-2. 기본 키바인딩
**전역**
| 키 | 명령 ID | 동작 |
|---|---|---|
| `Esc` | `cli.escape` | 패널 닫기, 스트림 중단, 빈 프롬프트 정리 |
| `Ctrl+C` | `cli.exit` | 종료 (에이전트 작업 중이면 확인) |
| `Ctrl+D` | `cli.exit` | 종료 (프롬프트가 비었을 때만) |
| `Ctrl+L` | `cli.clear_screen` | 화면 버퍼 정리 |

**프롬프트**
| 키 | 명령 ID | 동작 |
|---|---|---|
| `Enter` | `prompt.submit` | 제출 |
| `Shift+Enter` / `Ctrl+J` / `Alt+Enter` | `prompt.newline` | 줄바꿈 |
| `Ctrl+V` | `prompt.paste` | 텍스트/미디어 붙여넣기 |
| `Ctrl+O` | `prompt.toggle_trajectory` | 도구 추론 상세 펼치기/접기 |
| `Ctrl+R` | `prompt.open_review` | 아티팩트 리뷰 패널 |
| `Ctrl+G` | `prompt.external_editor` | `$EDITOR`로 프롬프트 작성 |
| `Alt+J` | `prompt.teleport_agent` | 승인 대기 중인 다음 서브에이전트로 이동 |
| `Ctrl+K` | `prompt.fast_approve` | 대기 중인 서브에이전트 작업 즉시 승인 |
| `Ctrl+A` / `Ctrl+E` | `prompt.cursor_start` / `cursor_end` | 줄 처음/끝 |
| `Ctrl+Z` | `prompt.undo_text` | 텍스트 편집 취소 |
| `Ctrl+Shift+Z` | `prompt.redo_text` | 다시 실행 |
| `Ctrl+Y` | — | 선택 텍스트 복사(yank) |
| `Ctrl+D` | — | 앞 글자 삭제 (프롬프트가 비어있지 않을 때) |
| `F5` | `voice.start_dictation` | 음성 받아쓰기 시작/중지 |

**탐색**
| 키 | 동작 |
|---|---|
| `↑` / `↓` | 목록 항목 이동 |
| `PgUp` / `Shift+↑`, `PgDn` / `Shift+↓` | 페이지 스크롤 |
| `Ctrl+Home` / `Ctrl+End` | 맨 위 / 맨 아래 |
| `←` / `→` | 커서 이동, 다중 페이지 구조(세션 선택기) 페이지 전환 |
| `Tab` | 슬래시 명령 자동완성 확정, 포커스 전환 |

**도구 확인**
| 키 | 동작 |
|---|---|
| `y` | 승인 |
| `n` | 거절 |
| `e` | 제안된 터미널 명령을 에디터로 수정 |
| `A` | (리뷰 패널) 전체 아티팩트 일괄 승인 |

### A-3. 셸 명령·플래그 요약
| 명령/플래그 | 용도 |
|---|---|
| `agy` | TUI 실행 |
| `agy models` / `agy agents` | 모델 슬러그 / 에이전트 목록 |
| `agy plugin list/install/enable/disable/uninstall` | 플러그인 관리 |
| `-p`, `--print`, `--prompt` | 헤드리스 단발 실행 |
| `--output-format text\|json\|stream-json` | 출력 형식 |
| `--input-format text\|stream-json` | stdin 입력 형식 |
| `--json-schema` | 구조화 출력 스키마 |
| `--model`, `--effort low\|medium\|high`, `--agent` | 모델/추론 강도/에이전트 |
| `--continue`, `-c` / `--conversation <id>` | 대화 이어가기 |
| `--dangerously-skip-permissions` | 모든 도구 자동 승인 |
| `--sandbox` | 터미널 샌드박스 강제 |
| `--print-timeout` | 응답 대기 한도 (기본 5m) |
| `--cwd` | 작업 디렉터리 지정 |

### A-4. 환경 변수
| 변수 | 용도 |
|---|---|
| `GEMINI_API_KEY` | API 키 인증 (`modelProvider: gemini` 필수) |
| `GOOGLE_GEMINI_BASE_URL` | Gemini 호환 커스텀 엔드포인트 |
| `AGY_CLI_DISABLE_AUTO_UPDATE` | `true`로 자동 업데이트 비활성화 |
| `EDITOR` | `Ctrl+G`, `editor: auto`가 사용하는 에디터 |

---

## 부록 B. 파일·경로 지도

| 경로 | 용도 |
|---|---|
| `~/.local/bin/agy` / `%LOCALAPPDATA%\agy\bin` | 바이너리 |
| `~/.gemini/antigravity-cli/settings.json` | 설정·권한 |
| `~/.gemini/antigravity-cli/keybindings.json` | 키바인딩 |
| `~/.gemini/antigravity-cli/skills/` | 전역 스킬 |
| `~/.gemini/antigravity-cli/plugins/<name>/` | 설치된 플러그인 |
| `~/.gemini/antigravity-cli/import_manifest.json` | 가져오기 추적 |
| `~/.gemini/antigravity-cli/updater/` | 업데이터 (`update.lock`, `last_check.timestamp`) |
| `~/.gemini/config/mcp_config.json` | 전역 MCP 서버 |
| `~/.gemini/antigravity/mcp_oauth_tokens.json` | MCP OAuth 토큰 |
| `<repo>/GEMINI.md` 또는 `<repo>/AGENTS.md` | 프로젝트 규칙 |
| `<repo>/.agents/skills/*.md` | 작업공간 스킬 |
| `<repo>/.agents/mcp_config.json` | 작업공간 MCP 서버 |

---

## 부록 C. 공식 문서 간 불일치 (안내 시 주의)

같은 v1.2.0 문서 안에서도 페이지별로 기술이 다른 항목이 있다. 사용자에게 안내할 때는 아래를 함께 알리고, 실제 환경에서 `/help`나 `/keybindings`로 확인하도록 한다.

| 항목 | 페이지 A | 페이지 B | 권장 안내 |
|---|---|---|---|
| 서브에이전트 텔레포트 키 | Features: `Ctrl+J` | Reference: `Alt+J` (`Ctrl+J`는 줄바꿈) | `/keybindings`에서 `prompt.teleport_agent` 확인 |
| `Ctrl+C` | Using: Escape/Cancel | Reference: `cli.exit` (작업 중이면 확인) | 중단 목적이면 `Esc`를 쓰도록 안내 |
| `Ctrl+Z` | Using: CLI 일시 중단(백그라운드) | Reference: 텍스트 편집 취소 | 포커스 상태에 따라 다를 수 있음, 직접 확인 |
| 텍스트 undo | Using: `Ctrl+_`, `Ctrl+Shift+-` | Reference: `Ctrl+Z` | 둘 다 시도 |
| `/usage` | Features: 인라인 도움말 매뉴얼 | Reference: 모델 쿼터 사용량 (`/quota`) | 쿼터 확인 용도로 안내, 도움말은 `/help` |
| `/permissions` 선택지 | Features: `request-review`, `always-proceed`, `strict` | Reference: `proceed-in-sandbox` 포함 4종 | 4종으로 안내 |
| Windows PATH 경로 | Install: `%LOCALAPPDATA%\agy\bin` | Troubleshooting: `C:\Program Files\Google\antigravity-cli` | 실제 설치 위치 확인 후 설정 |
| PATH 예시 | Troubleshooting: `"~/.local/bin:$PATH"` | — | `$HOME/.local/bin` 사용 권장 |
| `--model` 예시 슬러그 | Headless: `gemini-3.5-flash-medium` | `agy models` 출력 예시에 없음 | 반드시 `agy models`로 실제 슬러그 확인 |

## 참고 문서
- 개요: https://antigravity.google/docs/cli/overview/
- 설치·인증: https://antigravity.google/docs/cli/install/
- 튜토리얼: https://antigravity.google/docs/cli/tutorial/
- 사용법: https://antigravity.google/docs/cli/using/
- 기능: https://antigravity.google/docs/cli/features/
- 베스트 프랙티스: https://antigravity.google/docs/cli/best-practices/
- 문제 해결: https://antigravity.google/docs/cli/troubleshooting/
- 레퍼런스: https://antigravity.google/docs/cli/reference/
- 보조: headless / permissions / plugins / mcp 페이지 (동일 경로 하위)
