# Antigravity 설치 및 환경 구성 실습 가이드 (agy_setting)

본 문서는 **Antigravity CLI**를 로컬 시스템에 설치하고, 개발 환경과 의존성을 구성한 뒤 초기 실행 및 동작을 검증하기 위한 교육·실습용 가이드입니다.

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

---

## 1. 개요 및 학습 목표

- **시스템 요구사항 점검**: Antigravity 실행에 필요한 OS, Python 버전 및 도구 의존성을 확인합니다.
- **가상 환경 구축**: 독립된 Python 가상 환경(venv)을 생성하고 격리된 실행 환경을 구성합니다.
- **Antigravity CLI 설치**: 플랫폼별 바이너리/패키지를 다운로드하고 시스템 경로(PATH)에 등록합니다.
- **인증 및 기본 설정**: Google 계정 연동, 권한 모드 설정 및 기본 설정 파일 구조를 이해합니다.
- **초기 실행 검증**: 워크스페이스 신뢰 설정 및 첫 세션 실행을 통해 정상 동작 여부를 확인합니다.

---

## 2. 사전 준비 사항 (Prerequisites)

| 구분              | 요구사항                                                                                                | 권장 사항                      |
| :---------------- | :------------------------------------------------------------------------------------------------------ | :----------------------------- |
| **운영체제 (OS)** | macOS (Intel / Apple Silicon), Linux (Ubuntu 22.04 LTS 이상), Windows 10/11 (PowerShell 5.1+ 또는 WSL2) | macOS / Linux Ubuntu 22.04 LTS |
| **Python**        | Python 3.10 이상                                                                                        | Python 3.11 또는 3.12          |
| **패키지 매니저** | `pip`, `venv`                                                                                           | `uv` 또는 `poetry`             |
| **추가 도구**     | `git`, `curl`, `ripgrep`                                                                                | Node.js 18+ (MCP 서버 연동 시) |
| **계정 및 권한**  | 터미널 쉘 접근 권한, 패키지 설치 권한, Google 계정                                                      | GCP 프로젝트 접근 권한         |

### 2.1 OS별 터미널 및 패키지 매니저

| 항목          | macOS                           | Linux (Ubuntu)                                | Windows                                  |
| :------------ | :------------------------------ | :-------------------------------------------- | :--------------------------------------- |
| 권장 터미널   | iTerm2 / Ghostty / Terminal.app | GNOME Terminal / Ghostty                      | Windows Terminal (PowerShell 7 권장)     |
| 패키지 매니저 | Homebrew (`brew`)               | `apt`                                         | `winget`                                 |
| Python 설치   | `brew install python@3.12`      | `sudo apt install python3.12 python3.12-venv` | `winget install Python.Python.3.12`      |
| Git 설치      | `brew install git`              | `sudo apt install git`                        | `winget install Git.Git`                 |
| ripgrep 설치  | `brew install ripgrep`          | `sudo apt install ripgrep`                    | `winget install BurntSushi.ripgrep.MSVC` |
| Node.js 설치  | `brew install node`             | `sudo apt install nodejs npm`                 | `winget install OpenJS.NodeJS.LTS`       |

---

## 3. 단계별 실습 가이드 (Hands-on Lab Steps)

### Step 1: 시스템 요구사항 점검 및 작업 디렉터리 생성

터미널을 열고 현재 시스템의 Python 버전 및 필수 도구가 정상적으로 설치되어 있는지 확인합니다.

#### macOS / Linux

```bash
# 1. Python 버전 확인 (3.10 이상 필수)
python3 --version

# 2. Git 및 필수 유틸리티 확인
git --version
curl --version

# 3. pip 최신 버전 업그레이드
python3 -m pip install --upgrade pip

# 4. 실습용 전용 디렉터리 생성
mkdir -p ~/antigravity-lab/lab/agy_setting
```

#### Windows (PowerShell)

```powershell
# 1. Python 버전 확인 (3.10 이상 필수)
python --version
py -3 --version          # 여러 버전이 설치된 경우 런처로 확인

# 2. Git 및 필수 유틸리티 확인
git --version
curl.exe --version       # PowerShell의 curl 은 별칭이므로 curl.exe 로 실행

# 3. pip 최신 버전 업그레이드
python -m pip install --upgrade pip

# 4. 실습용 전용 디렉터리 생성
New-Item -ItemType Directory -Force -Path "$HOME\antigravity-lab\lab\agy_setting" | Out-Null
```

> [!TIP]
> Windows에서 `python` 실행 시 Microsoft Store가 열린다면, 앱 실행 별칭이 켜져 있는 상태입니다.
> **설정 > 앱 > 고급 앱 설정 > 앱 실행 별칭**에서 `python.exe`, `python3.exe` 항목을 끄거나, `py -3` 런처를 사용하세요.

---

#### GCP Cloud Shell

사용자들의 환경이 제약이 있거나, 간단한 클라이언트 에뮬레이터가 필요한 경우에는 GCP Cloud Shell을 활용할수 있습니다. 
GCP Cloud Shell은 웹 브라우저에서 바로 사용할 수 있는 사전 구성된 리눅스 기반 가상 개발 환경(또는 CLI 터미널)입니다. 

Cloud Shell의 구체적인 기능이나 사용법은 아래와 같습니다.

* 터미널 내 내장된 코드 편집기(Cloud Shell Editor) 기능 
* 기본 제공되는 개발 도구 및 CLI(gcloud, docker 등) 종류 
* 무료 제공되는 스토리지 용량 및 세션 제한 조건 

Cloud Shell을 접근하기 위해서 브라우저를 열고 아래 주소로 이동합니다. 
* https://console.cloud.google.com/


<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab1-2.png" width="700" ></p>

로긴을 하게 되면 아래와 같이 창이 뜨는데, Term of service에 동의합니다.
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab1-3.png" width="700" ></p>

좌측 상단의 "Select a Project"를 클릭해서 아래와 같이 사용할 프로젝트를 선택합니다.
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab1-4.png" width="700" ></p>

우측상단에 Cloud Shell 버튼을 클릭합니다. 그러면 아래 하단에 Cloud Shell 화면이 나타나고 Continue를 툴러서 인증을 진행합니다. 
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab1-5.png" width="700" ></p>

아래 Linux환경에서의 Shell을 확인 할수 있으며 해당 환경에서 Antigravity 를 사용할 수 있습니다.  Cloud Shell 상단에서 Open Editor를 클릭해보세요.
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab1-6.png" width="700" ></p>

Open Editor를 클릭하면 아래와 같이 브라우저 내의 VS Code를 사용할수 있습니다. 
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab1-7.png" width="700" ></p>



### Step 2: Python 가상환경(venv) 생성 및 활성화

프로젝트 간 패키지 충돌을 방지하기 위해 가상환경을 생성하고 활성화합니다.

#### macOS / Linux

```bash
# 1. Project root 디렉토리로 변경
cd ~/antigravity-lab/

# 2. 가상환경 생성 (.venv)
python3 -m venv .venv

# 3. 가상환경 활성화
source .venv/bin/activate

# 4. 활성화 확인 (프롬프트 앞에 (.venv) 표시, 경로가 .venv 내부인지 확인)
which python
```

#### Windows (PowerShell)

```powershell
# 1. Project root 디렉토리로 변경
Set-Location "$HOME\antigravity-lab"

# 2. 가상환경 생성 (.venv)
python -m venv .venv

# 3. 가상환경 활성화
.\.venv\Scripts\Activate.ps1

# 4. 활성화 확인 (프롬프트 앞에 (.venv) 표시)
Get-Command python | Select-Object -ExpandProperty Source
```

> [!WARNING]
> Windows에서 `이 시스템에서 스크립트를 실행할 수 없으므로...` 오류가 발생하면 현재 세션에 한해 실행 정책을 완화합니다.
>
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> .\.venv\Scripts\Activate.ps1
> ```
>
> 명령 프롬프트(CMD)를 사용한다면 `.\.venv\Scripts\activate.bat` 를 실행합니다.

> [!TIP]
> 가상환경 생성 및 활성화를 위해서 속도가 빠른 패키지 매니저인 `uv`를 사용하는 경우 다음과 같이 가상환경을 생성할 수 있습니다:
>
> **macOS / Linux**
>
> ```bash
> uv venv .venv
> source .venv/bin/activate
> ```
>
> **Windows (PowerShell)**
>
> ```powershell
> uv venv .venv
> .\.venv\Scripts\Activate.ps1
> ```
>
> `uv` 자체 설치: macOS/Linux는 `curl -LsSf https://astral.sh/uv/install.sh | sh`, Windows는 `winget install astral-sh.uv` 입니다.

---

### Step 3: Antigravity CLI 다운로드 및 설치

공식 다운로드 포털에서 사용 중인 운영체제에 맞는 Antigravity CLI 패키지를 다운로드합니다.

- **공식 다운로드 URL:** [https://antigravity.google/product/antigravity-cli](https://antigravity.google/product/antigravity-cli)

<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab3-1.png" width="600" ></p>


#### 설치 및 실행 권한 부여

1. 다운로드한 바이너리 파일의 압축을 해제합니다.
2. 실행 바이너리(`agy` / `agy.exe`)를 시스템 경로에 등록된 디렉터리로 이동합니다.

#### macOS / Linux

설치 위치는 `/usr/local/bin` 또는 `~/.local/bin` 을 사용합니다.

```bash
# 1. 다운로드 폴더로 이동 후 압축 해제 (파일명은 실제 다운로드 파일에 맞게 변경)
cd ~/Downloads
tar -xzf agy-*.tar.gz

# 2. 실행 권한 부여
chmod +x agy

# 3. PATH에 등록되어 있는 디렉터리로 이동 (예: /usr/local/bin)
sudo mv agy /usr/local/bin/

#    관리자 권한 없이 설치하려면 ~/.local/bin 사용
#    mkdir -p ~/.local/bin && mv agy ~/.local/bin/

# 4. 설치 버전 확인
agy --version
which agy
```

> [!TIP]
> macOS에서 `"agy"을(를) 열 수 없습니다. 개발자를 확인할 수 없습니다.` 경고가 뜨면 격리 속성을 제거합니다.
>
> ```bash
> xattr -d com.apple.quarantine /usr/local/bin/agy
> ```

#### Windows (PowerShell)

설치 위치는 `%LOCALAPPDATA%\agy\bin` 을 사용합니다.

```powershell
# 1. 설치 디렉터리 생성
$AgyBin = "$env:LOCALAPPDATA\agy\bin"
New-Item -ItemType Directory -Force -Path $AgyBin | Out-Null

# 2. 다운로드한 zip 압축 해제 (파일명은 실제 다운로드 파일에 맞게 변경)
Expand-Archive -Path "$HOME\Downloads\agy-windows.zip" -DestinationPath $AgyBin -Force

# 3. 사용자 PATH 에 영구 등록
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($UserPath -notlike "*$AgyBin*") {
    [Environment]::SetEnvironmentVariable("Path", "$UserPath;$AgyBin", "User")
    Write-Host "PATH 등록 완료. 터미널을 새로 열어야 적용됩니다."
}

# 4. 현재 세션에도 즉시 반영
$env:Path = "$env:Path;$AgyBin"

# 5. 설치 버전 확인
agy --version
where.exe agy
```

> [!NOTE]
> Windows에서 실행 파일이 어디에 풀렸는지 확실하지 않다면 아래로 찾을 수 있습니다.
>
> ```powershell
> Get-ChildItem -Path $env:LOCALAPPDATA -Filter agy.exe -Recurse -ErrorAction SilentlyContinue |
>     Select-Object -ExpandProperty FullName
> ```

---

### Step 4: 사용자 인증 및 계정 연동 (Authentication)

Antigravity는 Google 계정 및 Gemini 모델 백엔드와의 통신을 위한 인증을 필요로 합니다.

#### macOS / Linux

```bash
# Google 계정 로그인 및 인증 진행
agy login
```

#### Windows (PowerShell)

```powershell
# Google 계정 로그인 및 인증 진행
agy login
```

1. 명령어를 실행하면 브라우저에 인증 페이지가 열립니다.
2. Antigravity를 사용할 Google 계정으로 로그인 후 권한을 승인합니다.
3. 인증이 완료되면 터미널에 인증 완료 메시지가 표시됩니다.

**인증 토큰 저장 위치 (OS별)**

| OS      | 자격 증명 저장소                                |
| :------ | :---------------------------------------------- |
| macOS   | Apple Keychain (키체인 접근)                    |
| Linux   | Secret Service / D-Bus (GNOME Keyring, KWallet) |
| Windows | 자격 증명 관리자 (Credential Manager)           |

> [!NOTE]
> **원격 SSH / WSL2 환경**에서는 브라우저가 자동으로 열리지 않을 수 있습니다. 이 경우 터미널에 출력된 URL을 로컬 PC 브라우저에 붙여넣어 로그인한 뒤, 발급된 인증 코드를 터미널에 붙여넣습니다.
> Linux 헤드리스 환경에서 키링 오류(`secret keyring is locked`)가 발생하면 D-Bus 세션을 먼저 시작하세요: `export $(dbus-launch)`

> [!IMPORTANT]
> GCP 인프라 또는 Vertex AI 환경과 연동해야 하는 경우 Application Default Credentials(ADC)가 설정되어 있어야 합니다. 명령은 **모든 OS 동일**합니다.
>
> ```bash
> gcloud auth application-default login
> ```
>
> 원격 SSH 등 브라우저를 열 수 없는 환경에서는 `--no-launch-browser` 옵션을 사용합니다.

---

### Step 5: 워크스페이스 신뢰 및 초기 세션 실행

실습 디렉터리에서 Antigravity CLI 대화형 세션을 시작합니다.

#### macOS / Linux

```bash
cd ~/antigravity-lab/
agy
```

#### Windows (PowerShell)

```powershell
Set-Location "$HOME\antigravity-lab"
agy
```

#### 1. 워크스페이스 신뢰 확인 (Workspace Trust)

처음 진입하는 디렉터리인 경우 보안을 위한 워크스페이스 신뢰 확인 프롬프트가 표시됩니다.

**macOS / Linux 출력 예시**

```text
Accessing workspace:
/Users/hangsik/antigravity-lab/lab/agy_setting
Do you trust the contents of this project?
Antigravity CLI requires permission to read, edit, and execute files here.
> Yes, I trust this folder
   No, exit
   ↑/↓ Navigate · enter Confirm
```

**Windows 출력 예시**

```text
Accessing workspace:
C:\Users\hangsik\antigravity-lab\lab\agy_setting
Do you trust the contents of this project?
Antigravity CLI requires permission to read, edit, and execute files here.
> Yes, I trust this folder
   No, exit
   ↑/↓ Navigate · enter Confirm
```

- 방향키로 `Yes, I trust this folder`를 선택하고 **Enter**를 누릅니다.

#### 2. Antigravity TUI 초기 화면 확인

정상적으로 진입하면 아래와 같은 터미널 인터페이스(TUI)가 나타납니다. (경로 표기만 OS별로 다릅니다)

**모든 OS 동일**

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

> Windows에서는 네 번째 줄의 경로가 `C:\Users\hangsik\antigravity-lab\lab\agy_setting` 형태로 표시됩니다.
> 박스 문자가 깨져 보이면 Windows Terminal에서 폰트를 **Cascadia Mono / D2Coding** 등 고정폭 폰트로 변경하세요.

---

### Step 6: 디렉터리 구조 및 설정 파일 관리

Antigravity의 설정 및 커스터마이징 파일은 전역(Global)과 프로젝트(Workspace) 계층으로 나뉘어 관리됩니다.

#### macOS / Linux

```bash
# 프로젝트 루트에서 .agents 커스터마이징 디렉터리 생성
mkdir -p .agents/rules .agents/skills .agents/agents

# 생성 결과 확인
ls -la .agents
```

#### Windows (PowerShell)

```powershell
# 프로젝트 루트에서 .agents 커스터마이징 디렉터리 생성
"rules", "skills", "agents" | ForEach-Object {
    New-Item -ItemType Directory -Force -Path ".agents\$_" | Out-Null
}

# 생성 결과 확인
Get-ChildItem .agents
```

---

### Step 7: 초기 실행 검증 (Verification)

Antigravity 프롬프트(`> `)에서 아래 명령어를 순서대로 입력하여 동작을 검증합니다.
**이 단계의 명령은 agy TUI 내부에서 입력하므로 `모든 OS 동일` 입니다.**

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

**생성된 파일 확인 (터미널로 복귀 후)**

**macOS / Linux**

```bash
cat sum_0_to_10.py
python3 sum_0_to_10.py
```

**Windows (PowerShell)**

```powershell
Get-Content sum_0_to_10.py
python sum_0_to_10.py
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

### 4.0 OS별 실제 경로 매핑

위 구조의 `~/.gemini/` 는 OS에 따라 아래 실제 경로에 대응합니다.

| 논리 경로      | macOS / Linux                                | Windows                                               |
| :------------- | :------------------------------------------- | :---------------------------------------------------- |
| 홈 디렉터리    | `~` (`/Users/<user>`, `/home/<user>`)        | `%USERPROFILE%` (`C:\Users\<user>`)                   |
| 전역 설정 파일 | `~/.gemini/antigravity-cli/settings.json`    | `%USERPROFILE%\.gemini\antigravity-cli\settings.json` |
| 전역 MCP 설정  | `~/.gemini/config/mcp_config.json`           | `%USERPROFILE%\.gemini\config\mcp_config.json`        |
| 세션 아티팩트  | `~/.gemini/antigravity-cli/brain/`           | `%USERPROFILE%\.gemini\antigravity-cli\brain\`        |
| 전역 스킬      | `~/.gemini/config/skills/`                   | `%USERPROFILE%\.gemini\config\skills\`                |
| CLI 바이너리   | `/usr/local/bin/agy` 또는 `~/.local/bin/agy` | `%LOCALAPPDATA%\agy\bin\agy.exe`                      |

**설정 디렉터리 열어보기**

**macOS / Linux**

```bash
ls -la ~/.gemini/antigravity-cli/
cat ~/.gemini/antigravity-cli/settings.json
```

**Windows (PowerShell)**

```powershell
Get-ChildItem "$HOME\.gemini\antigravity-cli\"
Get-Content "$HOME\.gemini\antigravity-cli\settings.json"
```

---

### 4.1 `.gemini` 폴더 (전역 설정 및 런타임 저장소)

사용자의 홈 디렉터리(`~/.gemini/`, Windows는 `%USERPROFILE%\.gemini\`)에 위치하며, Antigravity 런타임 구동 시 필요한 전역 설정, 대화 기록, 캐시 데이터를 관리합니다.

#### 주요 파일 및 디렉터리

1. **`settings.json` (전역 CLI 환경설정 파일)**
   - 기본 AI 모델, 추론 강도(Reasoning Effort), 권한 승인 모드, 터미널 UI 테마 등을 전역적으로 제어합니다.
   - 예시 (파일 내용은 `모든 OS 동일`):
     ```json
     {
       "model": "gemini-3.6-pro",
       "effort": "medium",
       "sandbox": false,
       "dangerously_skip_permissions": false
     }
     ```
   - **설정 파일 생성/편집 예시**

     **macOS / Linux**

     ```bash
     mkdir -p ~/.gemini/antigravity-cli
     cat > ~/.gemini/antigravity-cli/settings.json <<'EOF'
     {
       "model": "gemini-3.6-pro",
       "effort": "medium",
       "sandbox": false,
       "dangerously_skip_permissions": false
     }
     EOF
     ```

     **Windows (PowerShell)**

     ```powershell
     New-Item -ItemType Directory -Force -Path "$HOME\.gemini\antigravity-cli" | Out-Null
     @'
     {
       "model": "gemini-3.6-pro",
       "effort": "medium",
       "sandbox": false,
       "dangerously_skip_permissions": false
     }
     '@ | Set-Content -Encoding UTF8 "$HOME\.gemini\antigravity-cli\settings.json"
     ```

2. **`cache/projects.json` (프로젝트 매핑 캐시)**
   - 로컬 작업 디렉터리 경로와 고유 `project_id`의 매핑 정보를 유지하여 `/fork <project_id>` 또는 `--project` 옵션 실행 시 프로젝트 범위를 추적합니다.

3. **`brain/<conversation_id>/` (세션 메모리 및 아티팩트)**
   - 각 대화 세션의 트랜스크립트 로그(`transcript.jsonl`, `transcript_full.jsonl`)가 보관됩니다.
   - 복잡한 분석 보고서, 아키텍처 다이어그램, 계획 문서 등 사용자에게 제시된 아티팩트(`.md`) 및 임시 실행 스크립트(`scratch/`)가 영구 보존됩니다.

4. **`config/mcp_config.json` (전역 MCP 설정 파일)**
   - 모든 워크스페이스에서 공통으로 사용할 Model Context Protocol 서버(예: PostgreSQL 브리지, 로컬 파일 서버, 웹 브라우저 자동화 도구 등)를 정의합니다.

---

### 4.2 `.agents` 폴더 (프로젝트 레벨 에이전트 커스터마이징)

프로젝트 루트 디렉터리에 위치하며, Git과 같은 버전 관리 시스템(VCS)에 커밋하여 **팀 전체가 동일한 AI 코딩 표준과 전문 스킬을 공유**할 수 있도록 설계된 핵심 폴더입니다.

#### 1. `.agents/rules/` (규칙 및 가드레일)

- 코딩 컨벤션, 에러 핸들링 원칙, 커밋 메시지 규약, 보안 정책 등을 마크다운(`.md`)으로 정의합니다.
- YAML Frontmatter를 통해 규칙이 활성화되는 조건을 제어할 수 있습니다.
- **예시 (`.agents/rules/commit-convention.md`) — 파일 내용은 `모든 OS 동일`:**

  ```markdown
  ---
  trigger: always_on
  description: Git commit message conventional format rule
  ---

  # Conventional Commits Guidelines

  - Format: `<type>(<scope>): <subject>`
  - Allowed Types: feat, fix, docs, style, refactor, test, chore
  ```

- **파일 생성 명령**

  **macOS / Linux**

  ```bash
  mkdir -p .agents/rules
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

  **Windows (PowerShell)**

  ```powershell
  New-Item -ItemType Directory -Force -Path ".agents\rules" | Out-Null
  @'
  ---
  trigger: always_on
  description: Git commit message conventional format rule
  ---

  # Conventional Commits Guidelines

  - Format: `<type>(<scope>): <subject>`
  - Allowed Types: feat, fix, docs, style, refactor, test, chore
  '@ | Set-Content -Encoding UTF8 ".agents\rules\commit-convention.md"
  ```

#### 2. `.agents/skills/` (스킬 모듈)

- 에이전트에게 특정 비즈니스 로직, 복잡한 빌드/배포 절차, 런북 가이드를 가르치는 모듈입니다.
- 각 스킬은 독립된 폴더 내 `SKILL.md` 파일로 작성되며, 점진적 공개(Progressive Disclosure) 방식으로 동작하여 필요한 시점에만 컨텍스트에 로드됩니다.
- **구조 (`모든 OS 동일`):**

  ```text
  .agents/skills/deploy-pipeline/
  ├── SKILL.md             # 스킬 메타데이터 및 지침 (필수)
  ├── scripts/             # 자동화 보조 셸/파이썬 스크립트
  ├── examples/            # 참조 예제 코드
  └── references/          # 상세 매뉴얼 문서
  ```

- **스킬 골격 생성 명령**

  **macOS / Linux**

  ```bash
  mkdir -p .agents/skills/deploy-pipeline/{scripts,examples,references}
  touch .agents/skills/deploy-pipeline/SKILL.md
  ```

  **Windows (PowerShell)**

  ```powershell
  "scripts", "examples", "references" | ForEach-Object {
      New-Item -ItemType Directory -Force -Path ".agents\skills\deploy-pipeline\$_" | Out-Null
  }
  New-Item -ItemType File -Force -Path ".agents\skills\deploy-pipeline\SKILL.md" | Out-Null
  ```

#### 3. `.agents/agents/` (서브에이전트 정의)

- 전문적인 역할을 수행하는 독립 서브에이전트(Subagent)를 선언합니다.
- **예시 (`.agents/agents/code-reviewer.md`) — 파일 내용은 `모든 OS 동일`:**

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

- **파일 생성 명령**

  **macOS / Linux**

  ```bash
  mkdir -p .agents/agents
  $EDITOR .agents/agents/code-reviewer.md     # 또는 vi / code 등 선호 에디터
  ```

  **Windows (PowerShell)**

  ```powershell
  New-Item -ItemType Directory -Force -Path ".agents\agents" | Out-Null
  notepad ".agents\agents\code-reviewer.md"   # 또는 code .agents\agents\code-reviewer.md
  ```

#### 4. `.agents/mcp_config.json` (프로젝트 전용 MCP 설정)

- 프로젝트 개발에 필요한 로컬 DB, 사내 API 도구, Docker 컨테이너와의 연동을 정의합니다.
- **예시 (macOS / Linux):**
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
- **예시 (Windows):** 실행 파일 확장자와 경로 구분자에 유의합니다. JSON 문자열 안에서는 역슬래시를 `\\` 로 이스케이프하거나 슬래시(`/`)를 사용하세요.
  ```json
  {
    "mcpServers": {
      "sqlite-db": {
        "command": "uvx.exe",
        "args": ["mcp-server-sqlite", "--db-path", "./data/app.db"]
      }
    }
  }
  ```

#### 5. `.agents/hooks.json` (에이전트 라이프사이클 훅)

- 에이전트가 도구를 호출하기 전(`pre_tool_call`), 호출한 후(`post_tool_call`), 또는 세션이 시작될 때 자동으로 실행할 셸 명령어를 바인딩합니다. (예: 파일 수정 후 자동 linter/formatter 실행)
- 훅에 등록하는 명령은 **OS 셸에 직접 전달**되므로, 팀에 Windows·macOS 사용자가 섞여 있다면 크로스 플랫폼으로 동작하는 명령(`python -m black .`, `npx prettier --write .`)을 사용하는 편이 안전합니다.

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

**`.gitignore` 등록 예시**

**macOS / Linux**

```bash
cat >> .gitignore <<'EOF'
.env
.env.local
.venv/
__pycache__/
EOF

git status --short
```

**Windows (PowerShell)**

```powershell
@"
.env
.env.local
.venv/
__pycache__/
"@ | Add-Content -Encoding UTF8 .gitignore

git status --short
```

---

## 5. 문제 해결 및 FAQ (Troubleshooting)

### Q1. `agy: command not found` 오류가 발생합니다.

- **원인:** `agy` 실행 바이너리가 시스템의 `PATH` 환경 변수에 등록되지 않았습니다.
- **해결 방법:**

  **macOS / Linux**

  ```bash
  # 바이너리 위치 확인
  ls -l ~/.local/bin/agy /usr/local/bin/agy 2>/dev/null

  # 현재 셸에 임시 등록
  export PATH="$HOME/.local/bin:$PATH"

  # ~/.zshrc 또는 ~/.bashrc 에 영구 추가
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
  source ~/.zshrc
  ```

  **Windows (PowerShell)**

  ```powershell
  # 바이너리 위치 확인
  Get-ChildItem -Path $env:LOCALAPPDATA -Filter agy.exe -Recurse -ErrorAction SilentlyContinue |
      Select-Object -ExpandProperty FullName

  # 현재 세션에 임시 등록
  $env:Path = "$env:Path;$env:LOCALAPPDATA\agy\bin"

  # 사용자 PATH 에 영구 등록 (터미널 재시작 후 적용)
  $UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
  [Environment]::SetEnvironmentVariable("Path", "$UserPath;$env:LOCALAPPDATA\agy\bin", "User")

  # 등록 확인
  where.exe agy
  ```

> [!TIP]
> Windows에서 큰따옴표 안의 `~` 는 확장되지 않습니다. macOS/Linux에서도 `"~/.local/bin"` 대신 **`"$HOME/.local/bin"`** 을 사용하는 것이 안전합니다.

### Q2. Python 버전이 3.9 이하로 인식됩니다.

- **원인:** 시스템 기본 Python 버전이 구버전이거나 가상환경이 비활성화되어 있습니다.
- **해결 방법:**

  **macOS**

  ```bash
  brew install python@3.12
  python3.12 -m venv .venv
  source .venv/bin/activate
  python --version
  ```

  **Linux (Ubuntu)**

  ```bash
  sudo apt update && sudo apt install -y python3.12 python3.12-venv
  python3.12 -m venv .venv
  source .venv/bin/activate
  python --version
  ```

  **Windows (PowerShell)**

  ```powershell
  winget install Python.Python.3.12

  # 설치된 버전 목록 확인
  py --list

  # 특정 버전으로 가상환경 재생성
  py -3.12 -m venv .venv
  .\.venv\Scripts\Activate.ps1
  python --version
  ```

### Q3. 인증 토큰 만료 또는 로그인 오류가 발생합니다.

- **원인:** 구글 로그인 세션이 만료되었거나 캐시된 토큰에 이상이 발생한 경우입니다.
- **해결 방법:** TUI 내부에서 `/logout` 을 실행한 뒤 CLI를 재시작해 다시 로그인합니다. (**모든 OS 동일**)

  ```text
  > /logout
  > /exit
  ```

  ```bash
  agy login
  ```

- 그래도 실패한다면 OS 자격 증명 저장소에 남은 항목을 직접 확인합니다.

  **macOS**

  ```bash
  security find-generic-password -s "Antigravity CLI" 2>/dev/null && echo "키체인 항목 존재"
  # 키체인 접근 앱에서 'Antigravity CLI' 항목을 삭제 후 재로그인
  ```

  **Linux**

  ```bash
  # 헤드리스/SSH 환경에서 키링이 잠겨 있는 경우
  export $(dbus-launch)
  agy login
  ```

  **Windows (PowerShell)**

  ```powershell
  # 자격 증명 관리자에서 관련 항목 확인
  cmdkey /list | Select-String -Pattern "antigravity|gemini"

  # 특정 항목 삭제 후 재로그인 (TARGET 은 위 결과에서 확인한 값)
  # cmdkey /delete:<TARGET>
  agy login
  ```

### Q4. Windows에서 스크립트 실행이 차단됩니다.

- **원인:** PowerShell 실행 정책(Execution Policy)이 `Restricted` 로 설정되어 있습니다.
- **해결 방법:**

  ```powershell
  # 현재 정책 확인
  Get-ExecutionPolicy -List

  # 현재 세션에만 허용 (가장 안전)
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

  # 사용자 범위로 영구 허용 (서명된 원격 스크립트만 허용)
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
  ```

### Q5. 한글이 깨지거나 박스 문자가 이상하게 보입니다.

- **macOS / Linux:** 로케일을 UTF-8로 설정합니다.

  ```bash
  export LANG=ko_KR.UTF-8
  export LC_ALL=ko_KR.UTF-8
  ```

- **Windows (PowerShell):** 콘솔 인코딩을 UTF-8로 변경하고 고정폭 폰트를 사용합니다.

  ```powershell
  chcp 65001
  [Console]::OutputEncoding = [System.Text.Encoding]::UTF8

  # 영구 적용: PowerShell 프로필에 추가
  if (-not (Test-Path $PROFILE)) { New-Item -ItemType File -Force -Path $PROFILE | Out-Null }
  Add-Content -Path $PROFILE -Value '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8'
  ```

---

## 6. 실습 완료 체크리스트

- [ ] Python 3.10 이상 버전 확인 및 가상환경 활성화 완료 (OS에 맞는 활성화 명령 사용)
- [ ] Antigravity CLI 바이너리 설치 및 `agy --version` 확인 완료
- [ ] PATH 등록 확인 완료 (`which agy` / `where.exe agy`)
- [ ] Google 계정 로그인 (`agy login`) 및 인증 완료
- [ ] 실습 워크스페이스 생성 및 신뢰(Trust) 승인 완료
- [ ] `agy` TUI 실행 및 `/help` 명령어 정상 작동 확인 완료
- [ ] `.gemini` 및 `.agents` 환경 디렉터리 역할 및 설정 파일 구조 이해 완료
- [ ] 내 OS의 실제 설정 파일 경로(`~/.gemini` 또는 `%USERPROFILE%\.gemini`) 확인 완료
