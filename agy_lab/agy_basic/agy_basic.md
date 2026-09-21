# Antigravity Cloud Shell 설치 및 환경 구성 실습 가이드 (agy_basic)

본 문서는 **GCP Cloud Shell** 환경에서 **Antigravity CLI(`agy`)** 를 설치하고, 가상환경 구성, Google 계정 인증 및 초기 실행을 검증하기 위한 핸즈온 실습 가이드입니다.

> [!NOTE]
> 본 가이드는 웹 브라우저만으로 실습이 가능한 **GCP Cloud Shell** 환경을 기준으로 작성되었습니다. 로컬 PC에 별도의 개발 도구나 설치 권한이 없어도 웹 브라우저에서 즉시 실습을 진행할 수 있습니다.

---

## 1. 개요 및 학습 목표

- **GCP Cloud Shell 환경 준비**: 웹 브라우저에서 Cloud Shell 터미널 및 Cloud Shell Editor를 활성화합니다.
- **실습 워크스페이스 및 Python 가상환경 구성**: 워크스페이스 디렉터리(`~/antigravity-lab`)를 생성하고 `.venv` 가상환경을 활성화합니다.
- **Antigravity CLI 설치**: Cloud Shell 환경에 Antigravity CLI 바이너리를 배치하고 시스템 경로(PATH)를 설정합니다.
- **Google 계정 및 라이선스 인증**: 브라우저 기반 헤드리스 OAuth 인증을 통해 Google 계정을 연동하고 Gemini 라이선스를 선택합니다.
- **초기 실행 검증**: 워크스페이스 신뢰 설정 및 첫 TUI 세션 진입, 기본 명령어(`/help`, `/model`, `/config`)와 코드 생성을 검증합니다.
- **환경 아키텍처 이해**: 전역 설정(`.gemini`) 및 프로젝트 커스터마이징(`.agents`) 디렉터리 구조를 파악합니다.

---

## 2. 사전 준비 사항 (Prerequisites)

GCP Cloud Shell은 필요한 기본 개발 도구가 사전에 모두 구성되어 제공되므로 별도의 복잡한 설치 작업이 필요 없습니다.

| 구분              | 요구사항                              | Cloud Shell 제공 상태                        |
| :---------------- | :------------------------------------ | :------------------------------------------- |
| **운영체제 (OS)** | Linux (Debian 기반 컨테이너)          | 브라우저 기반 기본 제공                      |
| **Python**        | Python 3.10 이상                      | Python 3.11+ 기본 설치됨                     |
| **기본 도구**     | `git`, `curl`, `gcloud`, `ripgrep`    | 사전 설치 및 PATH 등록 완료                  |
| **코드 편집기**   | Cloud Shell Editor (VS Code 기반)     | 상단 'Open Editor' 버튼으로 즉시 사용 가능   |
| **계정 및 권한**  | GCP 프로젝트 접근 권한 및 Google 계정 | GCP Console 로그인 계정 활용                 |
| **실습 경로**     | `~/antigravity-lab`                   | Cloud Shell 영구 홈 디렉터리(`$HOME`)에 구성 |

---

## 3. 단계별 실습 가이드 (Hands-on Lab Steps)

### Step 1: GCP Console 접속 및 Cloud Shell 활성화

GCP Cloud Shell은 웹 브라우저에서 바로 사용할 수 있는 사전 구성된 리눅스 기반 가상 개발 환경(CLI 터미널)입니다.

#### 1-1. GCP Console 접속

브라우저에서 아래 주소로 이동하여 실습용 Google 계정으로 로그인합니다.

- https://console.cloud.google.com/

_GCP 콘솔 접속 화면_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab1-2.png" width="700" alt="GCP 콘솔 접속 화면"></p>

서비스 약관 동의 창이 나타나면 **Terms of Service**에 동의합니다.

_서비스 약관 동의_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab1-3.png" width="700" alt="GCP 서비스 약관 동의 화면"></p>

#### 1-2. 프로젝트 선택

상단의 **Select a Project**를 클릭하여 실습에 배정된 GCP 프로젝트를 선택합니다.

_프로젝트 선택_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab1-4.png" width="700" alt="GCP 프로젝트 선택 화면"></p>

#### 1-3. Cloud Shell 터미널 열기

우측 상단의 **Cloud Shell** 버튼(`>_`)을 클릭합니다. 화면 하단에 세션 창이 나타나면 **Continue**를 눌러 세션을 시작합니다.

_Cloud Shell 활성화_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab1-5.png" width="700" alt="Cloud Shell 활성화 화면"></p>

아래와 같이 리눅스 bash 셸이 준비됩니다.

_Cloud Shell 터미널_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab1-6.png" width="700" alt="Cloud Shell 터미널 화면"></p>

#### 1-4. Cloud Shell Editor 확인

Cloud Shell 상단의 **Open Editor** 버튼을 클릭하면 브라우저 내부에서 VS Code 기반의 편리한 GUI 코드 편집기를 함께 사용할 수 있습니다.

_Cloud Shell Editor_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab1-7.png" width="700" alt="Cloud Shell Editor 화면"></p>

#### 1-5. 다중 터미널 탭 기능 확인

Cloud Shell은 여러 명령을 동시에 수행할 수 있도록 **다중 터미널 탭** 기능을 기본 제공합니다.

- **새 탭 추가 (`+`)**: 터미널 상단 탭 바 우측의 **`+` (새 탭 열기 / Open a new tab)** 버튼을 클릭하면 동일한 환경의 새로운 독립 bash 셸 탭이 열립니다.
- 이는 이후 Antigravity TUI 세션을 유지한 채 다른 터미널 탭에서 코드 실행, 로그 모니터링, git 명령 등을 병행할 때 유용하게 활용됩니다.

---

### Step 2: 실습 워크스페이스 생성 및 Python 가상환경(venv) 구성

Cloud Shell 터미널에서 실습 전용 워크스페이스를 생성하고 Python 가상환경을 활성화합니다.

```bash
# 1. 실습 워크스페이스 디렉터리 생성 및 이동
mkdir -p ~/antigravity-lab
cd ~/antigravity-lab
pwd     # /home/<user>/antigravity-lab 확인

# 2. Python 버전 확인 (3.10 이상 기본 제공)
python3 --version

# 3. 프로젝트 격리 가상환경(.venv) 생성
python3 -m venv .venv

# 4. 가상환경 활성화
source .venv/bin/activate

# 5. 활성화 확인 (프롬프트 앞에 (.venv) 표시 확인)
which python
```

---

### Step 3: (선택) Antigravity CLI 다운로드 및 설치 (비-Cloud Shell 환경 대상)

> [!IMPORTANT]
> **Cloud Shell 사용 시 Antigravity CLI 기본 설치 제공 (설치 불필요)**
> **GCP Cloud Shell 환경을 사용하는 경우 Antigravity CLI(`agy`)가 기본으로 사전 설치**되어 제공됩니다.
> 따라서 Cloud Shell 사용자는 수동 다운로드 및 설치 과정을 진행할 필요가 없으며, **3-1**에서 버전 확인 후 바로 **Step 4**로 이동하시면 됩니다.
>
> 본 단계의 수동 설치 가이드(3-2)는 **Cloud Shell이 아닌 자체 Linux 환경(로컬 Linux, 온프레미스 서버, 독자 VM 등)을 사용하는 실습자**를 위한 선택적(Optional) 안내입니다.

#### 3-1. Cloud Shell 기본 설치 확인 (Cloud Shell 사용자)

Cloud Shell 터미널에서 기본 설치된 Antigravity CLI 버전을 확인합니다.

```bash
agy --version
agy
```

_터미널에서 `agy` 실행_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab3-2.png" width="600" alt="Cloud Shell에서 agy 명령 실행"></p>

_로그인 방식 선택 화면이 나타나면 정상 동작 확인_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab3-3.png" width="600" alt="Antigravity CLI 로그인 방식 선택 화면"></p>

- 위 화면이 나타나면 정상 작동하는 상태입니다. 실제 로그인은 Step 4에서 진행하므로 `Ctrl + C` 로 세션을 종료한 후 **Step 4**로 바로 진행하세요.

#### 3-2. (선택) 수동 다운로드 및 설치 (Cloud Shell 외 환경 사용자 대상)

Cloud Shell이 아닌 일반 Linux 환경에서 `agy` 바이너리가 존재하지 않는 경우 아래 절차에 따라 다운로드 및 설치를 진행합니다.

- **공식 다운로드 포털:** [https://antigravity.google/product/antigravity-cli](https://antigravity.google/product/antigravity-cli)

_다운로드 페이지_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab3-1.png" width="600" alt="Antigravity CLI 다운로드 페이지"></p>

터미널에서 Linux 바이너리를 사용자 실행 경로(`~/.local/bin`)에 설치합니다:

```bash
# 1. 다운로드 파일 압축 해제 (파일명은 실제 다운로드 파일명에 맞춤)
tar -xzf agy-linux-*.tar.gz

# 2. 실행 권한 부여
chmod +x agy

# 3. 사용자 바이너리 경로로 이동
mkdir -p ~/.local/bin
mv agy ~/.local/bin/

# 4. PATH 환경 변수 등록 확인
export PATH="$HOME/.local/bin:$PATH"

# 5. 설치 확인
agy --version
which agy
```

---

### Step 4: 첫 실행 및 Google 계정 인증 (Cloud Shell 헤드리스 OAuth)

Antigravity는 Gemini 백엔드 모델과 통신하기 위해 Google 계정 인증을 수행합니다. Cloud Shell은 원격 가상환경이므로 터미널에 출력된 URL을 로컬 브라우저에서 열어 인증하는 **헤드리스 OAuth** 방식으로 진행됩니다.

```bash
cd ~/antigravity-lab
agy
```

#### 4-1. 로그인 방식 선택

`Select login method:` 화면에서 실습 환경에 맞는 방식을 선택합니다.

- **Use a Google Cloud project**: GCP 프로젝트 라이선스(Gemini Enterprise 등)로 로그인 (**실습 권장**)
- **Google OAuth**: 개인 Google 계정으로 로그인

_로그인 방식 선택_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab4-1.png" width="600" alt="로그인 방식 선택 화면"></p>

_Google Cloud 로그인 방식 선택 (`Continue with Google Cloud`)_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab4-2.png" width="600" alt="Google Cloud 로그인 방식 선택 화면"></p>

#### 4-2. 브라우저 인증 및 인증 코드 입력

1. Cloud Shell 터미널에 출력된 긴 인증 URL을 복사하여 PC의 새 브라우저 탭에 붙여넣습니다.
2. 실습용으로 부여받은 Google 계정으로 로그인하고 권한을 승인합니다.
3. 브라우저 화면에 표시된 인증 코드(verification code)를 복사합니다.

_인증 URL 확인 및 인증 코드 입력 위치_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab4-3.png" width="600" alt="인증 URL 및 인증 코드 입력 화면"></p>

_브라우저에 표시된 인증 코드 (Copy to Clipboard)_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab4-4.png" width="600" alt="브라우저 인증 코드 화면"></p>

4. Cloud Shell 터미널의 `authorization code...` 입력란에 붙여넣고 **Enter**를 누릅니다.

> [!TIP]
> Linux 헤드리스 환경에서 키링 오류(`secret keyring is locked` 또는 `Cannot autolaunch D-Bus`)가 발생하면 터미널에서 다음 명령을 먼저 실행한 뒤 `agy`를 다시 실행하세요:
>
> ```bash
> export $(dbus-launch)
> ```

#### 4-3. 라이선스 및 프로젝트 선택

사용 가능한 라이선스 목록이 표시되면 실습에 할당된 프로젝트 항목(예: Gemini Enterprise Plus)을 선택하고 **Enter**를 누릅니다.

_라이선스 선택_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab4-5.png" width="600" alt="라이선스 선택 화면"></p>

#### 4-4. 초기 환경 설정

컬러 스킴 및 마이그레이션 옵션 화면에서는 기본값을 유지하고 **Enter**를 눌러 진행합니다.

_컬러 스킴 및 마이그레이션 옵션 선택_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab4-6.png" width="600" alt="컬러 스킴 선택 화면"></p>

---

### Step 5: 워크스페이스 신뢰 및 TUI 진입 확인

#### 5-1. 워크스페이스 신뢰 승인 (Workspace Trust)

처음 진입하는 디렉터리(`~/antigravity-lab`)인 경우 보안을 위한 신뢰 확인 프롬프트가 표시됩니다.

_워크스페이스 신뢰 확인 프롬프트_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab4-7.png" width="600" alt="워크스페이스 신뢰 확인 프롬프트"></p>

```text
Accessing workspace:
/home/<user>/antigravity-lab
Do you trust the contents of this project?
Antigravity CLI requires permission to read, edit, and execute files here.
> Yes, I trust this folder
   No, exit
   ↑/↓ Navigate · enter Confirm
```

- 방향키로 `Yes, I trust this folder`를 선택하고 **Enter**를 누릅니다.

#### 5-2. Antigravity TUI 초기 화면 확인

아래와 같이 Antigravity 로고와 세션 정보가 표시되는 터미널 인터페이스(TUI)가 나타나면 CLI 환경 준비가 완료된 것입니다.

_TUI 초기 화면_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab4-8.png" width="600" alt="Antigravity CLI TUI 초기 화면"></p>

- 확인 후 다음 설정을 위해 `/exit` 또는 `Ctrl + C` 로 세션을 일시 종료합니다.

---

### Step 6: (선택) GCP Application Default Credentials(ADC) 설정

BigQuery, Vertex AI, Cloud Storage 등 GCP 리소스 연동 실습을 진행하는 경우 ADC 인증을 설정합니다.

```bash
gcloud auth application-default login --no-launch-browser
```

_ADC 인증 진행 화면 (Cloud Shell 예시)_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab4-0.png" width="600" alt="gcloud ADC 인증 화면"></p>

1. 명령 실행 후 계속 진행할지 묻는 프롬프트에 `y`를 입력합니다.
2. 출력된 URL을 로컬 브라우저에 열고 로그인하여 인증 코드를 발급받습니다.
3. 터미널의 verification code 입력 프롬프트에 붙여넣고 **Enter**를 누릅니다.

---

### Step 7: 프로젝트 커스터마이징 디렉터리(`.agents`) 구성 및 Rule, Agent, Skill 예제 작성

Antigravity는 워크스페이스의 `.agents` 디렉터리를 통해 에이전트의 행동 규칙(**Rule**), 전문 서브에이전트(**Agent**), 재사용 가능한 워크플로우(**Skill**)를 확장합니다. 디렉터리를 생성하고 각각의 예제 파일을 직접 구성해 봅니다.

#### 7-1. 디렉터리 구조 생성

```bash
cd ~/antigravity-lab

# 프로젝트 루트에 .agents 하위 디렉터리 생성
mkdir -p .agents/rules .agents/skills .agents/agents

# 생성 결과 확인
ls -la .agents
```

#### 7-2. Rule 생성 예제 (`.agents/rules/commit-convention.md`)

**Rule**은 에이전트가 코드를 작성하거나 Git 커밋을 수행할 때 항상(Always-on) 준수해야 하는 코딩 컨벤션, 가드레일, 보안 지침입니다.

Git 커밋 메시지 규칙을 강제하는 규칙 파일을 생성합니다:

```bash
cat > .agents/rules/commit-convention.md <<'EOF'
# Git Commit Convention Rule

Git 커밋 메시지를 작성할 때는 반드시 Conventional Commits 명세를 엄격히 준수하세요:

1. 형식: `<type>(<scope>): <subject>` (예: `feat(auth): add jwt token validation`)
2. 허용 타입:
   - `feat`: 새로운 기능 추가
   - `fix`: 버그 수정
   - `docs`: 문서 내용 변경
   - `style`: 코드 의미에 영향을 주지 않는 서식 및 공백 변경
   - `refactor`: 기능 추가나 버그 수정이 없는 리팩토링
   - `test`: 테스트 코드 추가 및 수정
   - `chore`: 빌드, 패키지 설정 등 보조 도구 관련 변경
3. 규칙:
   - 제목은 명령형, 현재 시제로 작성하며 마침표를 찍지 않습니다.
   - 본문이 필요한 경우 변경 이유와 영향을 상세히 기술합니다.
EOF
```

#### 7-3. Agent 생성 예제 (`.agents/agents/code-reviewer.md`)

**Agent**는 특정 도메인이나 작업(코드 리뷰, DB 쿼리 최적화, 보안 감사 등)에 특화된 서브에이전트(Persona)를 정의합니다. YAML Frontmatter로 도구 권한(`tools`)과 모델을 지정하고, 본문에 역할 지침(System Prompt)을 작성합니다.

코드 보안 및 성능을 전문으로 리뷰하는 서브에이전트 파일을 생성합니다:

```bash
cat > .agents/agents/code-reviewer.md <<'EOF'
---
name: code-reviewer
description: 코드 보안 취약점, 성능 병목, 스타일 가이드 분석 및 리팩토링 제안 전문 에이전트
model: inherit
tools:
  - view_file
  - grep_search
  - list_dir
---

# Code Reviewer Instructions

당신은 시니어 코드 리뷰어입니다. 전달받은 코드에 대해 다음 3가지 핵심 축을 기준으로 정밀 분석을 수행하세요:

1. **보안성 (Security):** SQL/명령어 인젝션, 민감 정보(API 키, 토큰) 노출, 미흡한 입력 검증 여부
2. **성능 (Performance):** 불필요한 반복 루프, 메모리 누수 위험, 병목 지점 탐지
3. **가독성 및 컨벤션:** PEP8/스타일 가이드 준수 및 클린 코드 원칙 준수 여부

## 응답 규칙
- 문제점 지적 시 구체적인 라인 번호와 발생 원인을 반드시 명시하세요.
- 개선된 코드는 즉시 적용 가능한 마크다운 코드 블록으로 제공하세요.
EOF
```

#### 7-4. Skill 생성 예제 (`.agents/skills/data-fetcher/SKILL.md`)

**Skill**은 에이전트가 특정 도메인 작업이나 다단계 복합 작업을 수행할 때 참고하는 절차형 매뉴얼(Workflow)입니다. 각 스킬은 독립된 폴더 내의 `SKILL.md` 파일로 정의되며, 평상시에는 설명(`description`)만 컨텍스트에 포함되다가 필요한 시점에 본문이 온디맨드로 로드되는 **점진적 노출(Progressive Disclosure)** 방식으로 토큰을 절약합니다.

외부 REST API로부터 데이터를 안전하게 수집하고 전처리하는 스킬을 생성합니다:

```bash
# 스킬 전용 하위 디렉터리 생성
mkdir -p .agents/skills/data-fetcher

# SKILL.md 파일 생성
cat > .agents/skills/data-fetcher/SKILL.md <<'EOF'
---
name: data-fetcher
title: 외부 REST API 데이터 수집 및 전처리 워크플로우
version: 1.0.0
description: REST API 엔드포인트에서 JSON 데이터를 수집하고 정규화된 형식으로 가공하는 표준 절차 스킬
tags:
  - data
  - api
  - etl
---

# Data Fetcher Skill Instructions

본 스킬은 외부 API 엔드포인트로부터 데이터를 수집하고 Python을 사용해 안전하게 클렌징하는 표준 절차를 안내합니다.

## 표준 실행 워크플로우

1. **API 요청 및 예외 처리:**
   - `urllib.request` 또는 `requests` 라이브러리를 사용하며, 네트워크 지연을 방지하기 위해 반드시 타임아웃(기본 10초)을 설정합니다.
   - HTTP 상태 코드가 200이 아닌 경우 명시적으로 에러 로그를 출력하고 비정상 종료를 방지합니다.
2. **데이터 파싱 및 스키마 검증:**
   - 응답 JSON 데이터의 필수 필드 누락 여부와 데이터 타입을 검사합니다.
3. **결과 저장:**
   - 정제된 데이터를 `output.json` 또는 `output.csv` 파일로 안전하게 저장합니다.
EOF
```

---

### Step 8: 초기 실행 및 도구 동작 검증

다시 `agy`를 실행하고 Antigravity 프롬프트(`> `)에서 동작을 검증합니다:

```bash
cd ~/antigravity-lab
agy
```

#### 8-1. 도움말 및 단축키 확인

```text
> /help
```

#### 8-2. 현재 모델 확인 및 Gemini 3.8 Flash (Medium) 설정

`/model` 명령을 실행하여 현재 활성화된 모델을 확인하고, 실습에 가장 최적화된 **Gemini 3.8 Flash** 모델 및 추론 강도 **medium**으로 설정합니다.

```text
> /model
```

_모델 선택 및 Effort 설정 화면_

```text
───────────────────────────────────────────────────────────────────────────────────────────────────
Switch Model

> Gemini 3.8 Flash
  Gemini 3.7 Flash
  Gemini 3.1 Pro

Effort  ◂        ○──────────────◉──────────────○        ▸
                  low          medium          high
            Balanced responses and reasoning for everyday coding tasks
───────────────────────────────────────────────────────────────────────────────────────────────────
↑/↓ Select model · ←/→ Adjust effort · enter Confirm · esc Cancel
```

1. **모델 선택**: 위/아래 방향키(`↑`/`↓`)로 **`Gemini 3.8 Flash`** 를 선택합니다.
2. **Effort(추론 강도) 설정**: 좌/우 방향키(`←`/`→`)를 눌러 **`medium`** (중간 단계)으로 맞춥니다.
   - `medium`: 일상적인 코딩 및 에이전트 개발 실습에 최적의 응답 속도와 논리적 추론력을 제공하는 균형 잡힌 설정입니다.
3. **설정 적용**: **Enter**를 눌러 설정을 확정합니다. 화면 상단 또는 상태 표시줄에 `Gemini 3.8 Flash (Medium)` 로 반영된 것을 확인합니다.

#### 8-3. 도구 실행 권한(Tool Permission) 설정

- 에이전트의 도구 실행 시 매번 승인 팝업을 거치지 않고 원활히 실습하려면 권한 모드를 변경할 수 있습니다.
- `/config` 입력 후 **Tool Permission** 항목을 `always-proceed` 로 설정합니다. (기본값: `request-review`)

```text
> /config
```

_`/config` 의 Tool Permission 설정 화면_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab6-1.png" width="600" alt="Tool Permission 설정 화면"></p>

#### 8-4. 코드 생성 및 도구 호출 테스트

프롬프트에 아래 내용을 입력하여 에이전트가 파일을 생성하는지 확인합니다:

```text
> Python으로 1부터 10까지의 합을 구하는 sum_1_to_10.py 파일을 생성해줘.
```

#### 8-5. Cloud Shell 탭 추가를 통한 실행 검증 (다중 커맨드 창 활용)

Antigravity CLI가 실행 중일 때는 터미널 화면이 대화형 TUI 인터페이스로 점유됩니다. 생성된 파일을 실행하거나, 프로세스 로그를 확인하고, git 상태를 점검하는 등 **추가 셸 명령어가 필요한 경우 `agy`를 종료할 필요 없이 Cloud Shell의 탭 추가 기능을 활용**하여 여러 개의 명령 창을 동시에 사용할 수 있습니다.

##### 방법 1: Cloud Shell 새 탭(`+`) 추가하여 병행 실행 (권장)

1. **새 탭 열기**: Cloud Shell 터미널 상단 탭 표시줄 우측의 **`+` (새 탭 열기)** 버튼을 클릭합니다.
2. **명령 실행 및 검증 (Tab 2)**: 새 탭이 열리면 워크스페이스로 이동하고 가상환경을 활성화한 뒤, 방금 Antigravity가 생성한 코드를 실행해 봅니다:

```bash
cd ~/antigravity-lab
source .venv/bin/activate

# 생성된 파일 내용 확인
cat sum_1_to_10.py

# 파이썬 스크립트 실행
python3 sum_1_to_10.py
```

3. **Antigravity 세션 유지 (Tab 1)**: 첫 번째 탭(Tab 1)으로 다시 전환하면 `agy` 대화 세션이 그대로 유지되어 있으므로, 추가 기능 구현 요구나 버그 수정을 끊김 없이 이어서 지시할 수 있습니다.

##### 방법 2: 단일 터미널 창에서 세션 종료 후 확인

만약 추가 탭을 열지 않고 현재 터미널에서 바로 확인하려면, `agy` 프롬프트에서 `/exit` 를 입력하여 세션을 종료한 뒤 터미널로 복귀합니다:

```text
> /exit
```

터미널로 복귀한 후 실행:

```bash
cat sum_1_to_10.py
python3 sum_1_to_10.py
```

#### 8-6. 등록된 Skill, Agent, Rule 인식 및 호출 검증

Step 7에서 생성한 Rule, Agent, Skill 자산들이 Antigravity TUI 세션 내에서 정상적으로 감지되고 작동하는지 검증합니다:

1. **스킬 목록 확인 (`/skills`)**:
   프롬프트에 `/skills` 를 입력하면 `.agents/skills/` 에 정의된 스킬 목록이 출력됩니다.

   ```text
   > /skills
   ```

   목록에서 `data-fetcher` 스킬과 설명(`REST API 엔드포인트에서 JSON 데이터를 수집하고...`)이 정상 인식되는지 확인합니다.

2. **서브에이전트 목록 확인 (`/agents`) 및 호출**:
   프롬프트에 `/agents` 를 입력하여 등록된 서브에이전트를 확인합니다.

   ```text
   > /agents
   ```

   목록에 `code-reviewer`가 확인되면 다음과 같이 직접 호출할 수 있습니다:

   ```text
   > @code-reviewer 방금 생성한 sum_1_to_10.py 코드의 보안성과 구조를 리뷰해줘.
   ```

3. **Rule 가드레일 자동 적용 확인**:
   `.agents/rules/` 에 저장된 규칙은 명시적 호출 없이도 컨텍스트에 자동 주입됩니다.
   ```text
   > sum_1_to_10.py 파일을 Git에 커밋하려 해. 적절한 커밋 메시지를 추천해줘.
   ```
   에이전트가 Rule에 정의된 Conventional Commits 명세에 맞춰 `feat(math): add script to calculate sum from 1 to 10` 형식으로 생성하는지 확인합니다.

---

## 4. Cloud Shell 환경 디렉터리 구조 및 설정 파일 상세 가이드

Antigravity는 사용자 홈 디렉터리의 **전역 설정(`.gemini/`)** 과 프로젝트 디렉터리의 **워크스페이스 자산(`.agents/`)** 으로 구성됩니다.

### 4.1 전체 디렉터리 구조

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
│   │   │       └── *.md                    # 구조화된 아티팩트 문서
│   │   └── builtin/skills/                 # CLI 내장 기본 스킬 모듈
│   └── config/
│       ├── skills/                         # 머신 전역 커스텀 스킬
│       ├── plugins/                        # 머신 전역 플러그인
│       └── mcp_config.json                 # 머신 전역 MCP 서버 설정
│
└── ~/antigravity-lab/                       # [워크스페이스] 실습 프로젝트 루트
    ├── .agents/                             # 프로젝트 전용 에이전트 커스터마이징 폴더
    │   ├── rules/                           # 가드레일, 코딩 스타일, 보안 제약 규칙 (.md)
    │   ├── skills/                          # 도메인 특화 절차형 스킬 워크플로우 (SKILL.md)
    │   ├── agents/                          # 전문 서브에이전트 정의 파일 (.md)
    │   ├── mcp_config.json                  # 프로젝트 전용 MCP 서버 연동 설정
    │   └── hooks.json                       # 에이전트 라이프사이클 이벤트 훅 정의
    ├── GEMINI.md                            # 워크스페이스 전역 규칙 및 가드레일 (로컬 전용)
    └── .gitignore                           # 시크릿(.env) 및 임시 파일 제외 설정
```

### 4.2 주요 설정 파일 예시

#### 1. 전역 설정 (`~/.gemini/antigravity-cli/settings.json`)

```bash
mkdir -p ~/.gemini/antigravity-cli
cat > ~/.gemini/antigravity-cli/settings.json <<'EOF'
{
  "model": "gemini-3.8-flash",
  "effort": "medium",
  "sandbox": false,
  "dangerously_skip_permissions": false
}
EOF
```

#### 2. 프로젝트 커밋 컨벤션 규칙 (`.agents/rules/commit-convention.md`)

```bash
cd ~/antigravity-lab
cat > .agents/rules/commit-convention.md <<'EOF'
---
trigger: always_on
description: Git commit message conventional format rule
---

# Conventional Commits Guidelines

- Format: `<type>(<scope>): <subject>`
- Allowed Types: feat, fix, docs, style, refactor, test, chore
EOF
```

#### 3. 서브에이전트 정의 예시 (`.agents/agents/code-reviewer.md`)

```bash
cat > .agents/agents/code-reviewer.md <<'EOF'
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
EOF
```

#### 4. 커스텀 스킬 정의 예시 (`.agents/skills/data-fetcher/SKILL.md`)

```bash
mkdir -p .agents/skills/data-fetcher
cat > .agents/skills/data-fetcher/SKILL.md <<'EOF'
---
name: data-fetcher
title: 외부 REST API 데이터 수집 및 전처리 워크플로우
version: 1.0.0
description: REST API 엔드포인트에서 JSON 데이터를 수집하고 정규화된 형식으로 가공하는 표준 절차 스킬
tags:
  - data
  - api
  - etl
---

# Data Fetcher Skill Instructions

본 스킬은 외부 API 엔드포인트로부터 데이터를 수집하고 Python을 사용해 안전하게 클렌징하는 표준 절차를 안내합니다.

## 표준 실행 워크플로우

1. **API 요청 및 예외 처리:**
   - `urllib.request` 또는 `requests` 라이브러리를 사용하며, 네트워크 지연을 방지하기 위해 반드시 타임아웃(기본 10초)을 설정합니다.
   - HTTP 상태 코드가 200이 아닌 경우 명시적으로 에러 로그를 출력하고 비정상 종료를 방지합니다.
2. **데이터 파싱 및 스키마 검증:**
   - 응답 JSON 데이터의 필수 필드 누락 여부와 데이터 타입을 검사합니다.
3. **결과 저장:**
   - 정제된 데이터를 `output.json` 또는 `output.csv` 파일로 안전하게 저장합니다.
EOF
```

---

## 5. Cloud Shell 환경 문제 해결 및 FAQ (Troubleshooting)

### Q1. `agy: command not found` 오류가 발생합니다.

- **원인:** 바이너리가 PATH에 등록되지 않았습니다.
- **해결 방법:**
  ```bash
  export PATH="$HOME/.local/bin:$PATH"
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
  source ~/.bashrc
  ```

### Q2. Cloud Shell에서 브라우저가 자동으로 열리지 않습니다.

- **원인:** Cloud Shell은 원격 헤드리스 Linux 환경이므로 직접 GUI 브라우저를 실행할 수 없습니다.
- **해결 방법:** 터미널에 출력된 URL을 복사하여 PC의 웹 브라우저에서 열고, 로그인 후 나타나는 인증 코드를 복사하여 Cloud Shell 터미널에 붙여넣으세요.

### Q3. `secret keyring is locked` 또는 D-Bus 오류가 발생합니다.

- **원인:** 헤드리스 환경에서 GUI 키링 데몬 세션이 실행되지 않은 상태입니다.
- **해결 방법:**
  ```bash
  export $(dbus-launch)
  agy
  ```

### Q4. 일정 시간 후 Cloud Shell 터미널 연결이 끊겼습니다.

- **원인:** Cloud Shell은 약 20분 이상 유휴(idle) 상태가 지속되면 세션이 자동 종료됩니다.
- **해결 방법:** 브라우저에서 **Reconnect**를 클릭하여 다시 접속한 뒤 가상환경을 재활성화하고 실습을 이어갑니다:
  ```bash
  cd ~/antigravity-lab
  source .venv/bin/activate
  agy
  ```

### Q5. `/config`에서 `always-proceed`가 `disabled by admin`으로 표시됩니다.

- **원인:** 조직(관리자) 정책으로 해당 권한 모드가 차단된 상태입니다.
- **해결 방법:** 기본값인 `request-review`를 그대로 사용하고 도구 호출 시 수동으로 승인합니다. 실습 진행에는 아무런 문제가 없습니다.

---

## 6. 실습 완료 체크리스트

- [ ] GCP Console 접속 및 Cloud Shell 터미널 / Cloud Shell Editor 활성화 완료
- [ ] 실습 워크스페이스(`~/antigravity-lab`) 생성 및 `.venv` 가상환경 활성화 완료
- [ ] Antigravity CLI 동작 확인 완료 (Cloud Shell 기본 제공 또는 수동 설치 후 agy --version 확인)
- [ ] 브라우저 헤드리스 OAuth 로그인 및 Gemini 프로젝트 라이선스 선택 완료
- [ ] 워크스페이스 신뢰(Trust) 승인 및 Antigravity TUI 초기 화면 진입 완료
- [ ] (선택) GCP ADC 설정 완료 (`gcloud auth application-default login --no-launch-browser`)
- [ ] `.agents` 커스터마이징 디렉터리 구성 및 Rule, Agent, Skill 예제 작성 완료
- [ ] `/help`, `/model` (Gemini 3.8 Flash Medium 설정), `/config`, `/skills`, `/agents` 실행 및 도구 호출 검증 완료
- [ ] Cloud Shell 환경에서의 `.gemini` 및 `.agents` 디렉터리 역할 이해 완료

---

## 7. 다음 단계

Cloud Shell 환경 구성과 초기 검증이 완료되었다면 다음 실습 가이드를 진행하세요:

- [agy_command.md](./agy_command.md) — Antigravity CLI 기본 명령어 및 TUI 조작 실습
- [agy_webapp.md](./agy_webapp.md) — Antigravity를 활용한 웹 애플리케이션 개발 실습
