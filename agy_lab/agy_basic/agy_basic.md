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

#### 1-5. 다중 터미널 탭 기능 및 실행 환경 구분

Cloud Shell은 여러 명령을 동시에 수행할 수 있도록 **다중 터미널 탭** 기능을 기본 제공합니다. 본 실습에서는 **리눅스 셸 명령(Shell Command)** 과 **Antigravity AI 대화창(Antigravity TUI)** 두 실행 환경을 오가며 진행하므로 다중 탭을 적극 활용합니다:

- **🖥️ Cloud Shell 터미널 (일반 bash 셸 환경)**:
  - 프롬프트: `user@cloudshell:~$ ` (기본 리눅스 셸)
  - 역할: 리눅스 기본 명령(`mkdir`, `cd`, `cat`), 가상환경 구성, `agy` 실행 및 코드 실행
  - 문서 표기: `> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**`
- **🤖 Antigravity 대화창 (agy TUI 환경)**:
  - 프롬프트: `> ` (화면 하단의 Antigravity 입력창)
  - 역할: 에이전트 지시 프롬프트, 슬래시 명령어(`/help`, `/model`, `/config`, `/skills`, `/agents`, `/hooks`) 입력
  - 문서 표기: `> 📍 **실행 위치: 🤖 Antigravity 대화창 (agy 프롬프트)**`
- **다중 탭 활용 패턴**:
  - **Tab 1 (Antigravity 대화 세션)**: `agy`를 실행해두고 AI와 실시간으로 대화하고 지시하는 메인 창
  - **Tab 2 (일반 bash 셸 탭)**: 상단 `+` 버튼으로 열어 생성된 파일 확인, 스크립트 실행, git 작업 등을 병행하는 보조 창

---

### Step 2: 실습 워크스페이스 생성 및 Python 가상환경(venv) 구성

Cloud Shell 터미널에서 실습 전용 워크스페이스를 생성하고 Python 가상환경을 활성화합니다.

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

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

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
cd ~/antigravity-lab
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

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
cd ~/antigravity-lab

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

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
cd ~/antigravity-lab
agy
```

#### 4-1. 로그인 방식 선택

> 📍 **진행 위치: 🤖 Antigravity 대화창 (TUI 로그인 선택 화면)**

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
> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**
>
> ```bash
> export $(dbus-launch)
> ```

#### 4-3. 라이선스 및 프로젝트 선택

> 📍 **진행 위치: 🤖 Antigravity 대화창 (TUI 라이선스 선택 화면)**

사용 가능한 라이선스 목록이 표시되면 실습에 할당된 프로젝트 항목(예: Gemini Enterprise Plus)을 선택하고 **Enter**를 누릅니다.

_라이선스 선택_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab4-5.png" width="600" alt="라이선스 선택 화면"></p>

#### 4-4. 초기 환경 설정

> 📍 **진행 위치: 🤖 Antigravity 대화창 (TUI 환경 설정 화면)**

컬러 스킴 및 마이그레이션 옵션 화면에서는 기본값을 유지하고 **Enter**를 눌러 진행합니다.

_컬러 스킴 및 마이그레이션 옵션 선택_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab4-6.png" width="600" alt="컬러 스킴 선택 화면"></p>

---

### Step 5: 워크스페이스 신뢰 및 TUI 진입 확인

#### 5-1. 워크스페이스 신뢰 승인 (Workspace Trust)

> 📍 **진행 위치: 🤖 Antigravity 대화창 (TUI 신뢰 확인 화면)**

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

> 📍 **진행 위치: 🤖 Antigravity 대화창 (TUI 화면)**

아래와 같이 Antigravity 로고와 세션 정보가 표시되는 터미널 인터페이스(TUI)가 나타나면 CLI 환경 준비가 완료된 것입니다.

_TUI 초기 화면_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab4-8.png" width="600" alt="Antigravity CLI TUI 초기 화면"></p>

- 확인 후 다음 설정을 위해 `/exit` 또는 `Ctrl + C` 로 세션을 일시 종료합니다.

---

### Step 6: (선택) GCP Application Default Credentials(ADC) 설정

BigQuery, Vertex AI, Cloud Storage 등 GCP 리소스 연동 실습을 진행하는 경우 ADC 인증을 설정합니다.

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
cd ~/antigravity-lab
gcloud auth application-default login --no-launch-browser
```

_ADC 인증 진행 화면 (Cloud Shell 예시)_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab4-0.png" width="600" alt="gcloud ADC 인증 화면"></p>

1. 명령 실행 후 계속 진행할지 묻는 프롬프트에 `y`를 입력합니다.
2. 출력된 URL을 로컬 브라우저에 열고 로그인하여 인증 코드를 발급받습니다.
3. 터미널의 verification code 입력 프롬프트에 붙여넣고 **Enter**를 누릅니다.

---

### Step 7: 초기 실행 및 기본 도구 동작 검증

실습 워크스페이스(`~/antigravity-lab`)에서 `agy`를 실행하고, 기본 명령어(`/help`, `/model`, `/config`, `/skills`, `/agents`) 및 코드 생성 동작을 검증합니다:

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
cd ~/antigravity-lab
agy
```

#### 7-1. 도움말 및 단축키 확인

> 📍 **실행 위치: 🤖 Antigravity 대화창 (agy 프롬프트)**

```text
> /help
```

Antigravity TUI에서 지원하는 슬래시 명령어, 단축키 및 주요 사용법을 확인합니다.

#### 7-2. 현재 모델 확인 및 Gemini 3.8 Flash (Medium) 설정

> 📍 **실행 위치: 🤖 Antigravity 대화창 (agy 프롬프트)**

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

#### 7-3. 도구 실행 권한(Tool Permission) 설정

> 📍 **실행 위치: 🤖 Antigravity 대화창 (agy 프롬프트)**

- 에이전트의 도구 실행 시 매번 승인 팝업을 거치지 않고 원활히 실습하려면 권한 모드를 변경할 수 있습니다.
- `/config` 입력 후 **Tool Permission** 항목을 `always-proceed` 로 설정합니다. (기본값: `request-review`)

```text
> /config
```

_`/config` 의 Tool Permission 설정 화면_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/setup/lab6-1.png" width="600" alt="Tool Permission 설정 화면"></p>

#### 7-4. 스킬 및 에이전트 목록 조회 명령 확인 (`/skills`, `/agents`)

> 📍 **실행 위치: 🤖 Antigravity 대화창 (agy 프롬프트)**

Antigravity TUI 프롬프트에서 스킬과 서브에이전트 목록을 확인하는 명령어를 실행해 봅니다:

1. **스킬 목록 확인 (`/skills`)**:

   ```text
   > /skills
   ```

   Antigravity CLI가 기본 제공하는 내장 스킬 모듈 목록이 출력되는 것을 확인합니다.

2. **서브에이전트 목록 확인 (`/agents`)**:
   ```text
   > /agents
   ```
   현재 사용 가능한 서브에이전트 목록이 출력되는 것을 확인합니다.

> [!NOTE]
> 현재는 기본 내장 항목들만 표시됩니다. 이어지는 **Step 8**에서 우리만의 맞춤형 Rule, Agent, Skill을 직접 만들어 이 목록에 등록하고 활용해 볼 것입니다.

#### 7-5. 코드 생성 및 도구 호출 테스트

> 📍 **실행 위치: 🤖 Antigravity 대화창 (agy 프롬프트)**

프롬프트에 아래 내용을 입력하여 에이전트가 파일을 생성하는지 확인합니다:

```text
> Python으로 1부터 10까지의 합을 구하는 sum_1_to_10.py 파일을 생성해줘.
```

#### 7-6. Cloud Shell 탭 추가를 통한 실행 검증 (다중 커맨드 창 활용)

Antigravity CLI가 실행 중일 때는 터미널 화면이 대화형 TUI 인터페이스로 점유됩니다. 생성된 파일을 실행하거나, 프로세스 로그를 확인하고, git 상태를 점검하는 등 **추가 셸 명령어가 필요한 경우 `agy`를 종료할 필요 없이 Cloud Shell의 탭 추가 기능을 활용**하여 여러 개의 명령 창을 동시에 사용할 수 있습니다.

##### 방법 1: Cloud Shell 새 탭(`+`) 추가하여 병행 실행 (권장)

1. **새 탭 열기**: Cloud Shell 터미널 상단 탭 표시줄 우측의 **`+` (새 탭 열기)** 버튼을 클릭합니다.
2. **명령 실행 및 검증 (Tab 2)**: 새 탭이 열리면 워크스페이스로 이동하고 가상환경을 활성화한 뒤, 방금 Antigravity가 생성한 코드를 실행해 봅니다:

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (Tab 2 - 새 bash 탭)**

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

> 📍 **실행 위치: 🤖 Antigravity 대화창 (Tab 1)**

```text
> /exit
```

터미널로 복귀한 후 실행:

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
cd ~/antigravity-lab
cat sum_1_to_10.py
python3 sum_1_to_10.py
```

---

### Step 8: 프로젝트 커스터마이징 디렉터리(`.agents`) 구성 및 Rule, Agent, Skill, Hook 실습

기본 동작 검증을 완료했다면, 이제 워크스페이스의 `.agents` 디렉터리를 통해 에이전트의 행동 규칙(**Rule**), 전문 서브에이전트(**Agent**), 재사용 가능한 표준 업무 워크플로우(**Skill**), 자동화 이벤트 트리거(**Hook**)을 직접 작성하고 활용해 봅니다.

#### 8-1. 디렉터리 구조 생성

Tab 2(일반 bash 터미널) 또는 `agy` 종료 후 터미널에서 `.agents` 하위 폴더들을 생성합니다:

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (Tab 2 또는 일반 bash 셸)**

```bash
# 1. Antigravity 워크스페이스 루트로 이동 (기준점)
cd ~/antigravity-lab

# 2. 프로젝트 루트에 .agents 하위 디렉터리 생성 (규칙, 스킬, 에이전트, 스크립트)
mkdir -p .agents/rules .agents/skills .agents/agents .agents/scripts

# 3. 생성 결과 확인
ls -la .agents
```

#### 8-2. Rule (행동 규칙) — 개념, 작성 예제 및 실제 활용 방법

##### 1. Rule의 개념 및 작동 원리

- **개념**: 에이전트가 모든 대화와 작업에서 **항상(Always-on)** 지켜야 하는 기본 원칙, 말투, 답변 서식, 가드레일입니다.
- **작동 원리**: 사용자가 별도로 명령어를 입력하거나 호출하지 않아도, Antigravity가 프롬프트 컨텍스트에 규칙을 **자동으로 주입**하여 에이전트의 태도와 답변 형식을 일관되게 제어합니다.

##### 2. Rule 파일 작성 예제 (`.agents/rules/friendly-response.md`)

항상 친절한 한국어 존댓말로 답변하고, 어려운 용어는 쉬운 비유로 풀며, 답변 시작 시 **[핵심 3줄 요약]**을 제공하도록 규칙을 생성합니다:

> 📍 **파일 생성 위치 (절대 경로)**: `~/antigravity-lab/.agents/rules/friendly-response.md`  
> Antigravity는 워크스페이스 루트(`.agents/rules/`)에 위치한 마크다운(`.md`) 규칙 파일을 자동으로 감지하여 모든 대화에 주입합니다.

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (Tab 2 또는 일반 bash 셸)**

```bash
# 1. Antigravity 워크스페이스 루트로 이동 (파일 생성 위치의 기준점)
cd ~/antigravity-lab

# 2. Rule 파일 생성 (경로: ~/antigravity-lab/.agents/rules/friendly-response.md)
cat > .agents/rules/friendly-response.md <<'EOF'
# 친절한 응답 및 핵심 요약 규칙 (Response Style Rule)

모든 질문에 응답할 때는 다음 지침을 반드시 준수하세요:

1. **말투:** 항상 정중하고 친절한 한국어 존댓말(~해요, ~합니다)로 답변하세요.
2. **쉬운 설명:** 전문 용어나 어려운 개념이 나오면 초보자도 이해하기 쉬운 일상적인 비유를 곁들여 설명하세요.
3. **3줄 핵심 요약:** 긴 설명에 앞서, 답변 맨 위에 반드시 `[핵심 3줄 요약]`을 글머리 기호(`-`)로 먼저 제시하세요.
4. **추천 액션:** 답변 끝에 사용자가 바로 따라 해볼 수 있는 '다음 추천 단계'를 1~2가지 제안하세요.
EOF

# 3. 파일 생성 위치 및 정상 생성 여부 확인
ls -la ~/antigravity-lab/.agents/rules/friendly-response.md
```

##### 3. 실제 실행 및 활용 방법

Antigravity 세션(`agy`)에서 일반적인 질문을 던지면 Rule이 어떻게 자동으로 적용되는지 확인합니다.

> 📍 **실행 위치: 🤖 Antigravity 대화창 (Tab 1 agy 프롬프트)**

- **프롬프트 입력 예시:**

  ```text
  > 클라우드 컴퓨팅이 뭔지 쉽게 설명해줘.
  ```

- **에이전트 실제 응답 결과 (Rule 자동 반영):**
  ```text
  [핵심 3줄 요약]
  - 내 컴퓨터 대신 인터넷 너머에 있는 거대한 데이터센터의 컴퓨터 자원을 빌려 쓰는 기술입니다.
  - 별도의 고가 장비를 사지 않고도 필요한 만큼만 사용하고 쓴 만큼만 요금을 지불합니다.
  - 구글 드라이브, 넷플릭스, 웹 서비스 등 일상에서 쓰는 거의 모든 서비스가 클라우드 기반입니다.

  안녕하세요! 클라우드 컴퓨팅에 대해 알기 쉽게 설명해 드릴게요. 😊

  클라우드 컴퓨팅을 일상에 비유하자면 '정수기 렌탈'이나 '공유 자전거'와 비슷해요!
  집에 거대한 정수 시설을 직접 만들지 않아도 매달 적은 비용으로 깨끗한 물을 마실 수 있듯이,
  비싼 컴퓨터 서버를 회사나 집에 직접 사두지 않고 구글(GCP)이나 아마존(AWS) 같은 클라우드 기업의
  성능 좋은 컴퓨터를 인터넷을 통해 빌려 쓰는 것이랍니다.

  💡 다음 추천 단계:
  1. 클라우드의 3대 서비스 모델(IaaS, PaaS, SaaS)의 차이점이 궁금하시다면 "SaaS가 뭐야?"라고 질문해 보세요.
  2. 현재 우리가 실습 중인 GCP Cloud Shell이 왜 클라우드 환경인지 확인해 보세요.
  ```

> [!TIP]
> 사용자가 규칙을 전혀 언급하지 않았음에도 Rule 파일의 지침에 따라 `[핵심 3줄 요약]`, `친절한 비유`, `추천 단계`가 자동으로 포함되어 응답합니다.

---

#### 8-3. Agent (맞춤형 AI 비서) — 개념, 작성 예제 및 실제 활용 방법

##### 1. Agent의 개념 및 작동 원리

- **개념**: 이메일 작성, 보고서 윤문, 데이터 분석 등 **특정 업무 목적에 맞춰 역할을 특화한 전담 서브에이전트(Persona)**입니다.
- **작동 원리**: YAML 메타데이터로 에이전트의 이름(`name`)과 설명(`description`), 허용 도구(`tools`)를 정의하고, 본문 시스템 프롬프트로 작업 지침을 부여합니다. 대화 중 `@에이전트명`으로 직접 호출하거나 업무를 위임할 수 있습니다.

##### 2. Agent 파일 작성 예제 (`.agents/agents/writing-assistant.md`)

비즈니스 이메일, 업무 보고서, 공지사항을 정중하고 깔끔하게 다듬어 주는 문서 작성 비서를 생성합니다:

> 📍 **파일 생성 위치 (절대 경로)**: `~/antigravity-lab/.agents/agents/writing-assistant.md`  
> Antigravity는 워크스페이스의 `.agents/agents/` 디렉터리에 위치한 마크다운 설정 파일을 자동으로 읽어 서브에이전트로 등록합니다.

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (Tab 2 또는 일반 bash 셸)**

```bash
# 1. Antigravity 워크스페이스 루트로 이동 (파일 생성 위치의 기준점)
cd ~/antigravity-lab

# 2. Agent 파일 생성 (경로: ~/antigravity-lab/.agents/agents/writing-assistant.md)
cat > .agents/agents/writing-assistant.md <<'EOF'
---
name: writing-assistant
description: 비즈니스 이메일, 업무 보고서, 공지사항, 블로그 초안 작성 및 문장 교정 전문 비서
model: inherit
tools:
  - view_file
  - list_dir
---

# Writing Assistant Instructions

당신은 직관적이고 설득력 있는 글을 작성하는 전문 문서 비서입니다. 사용자가 초안이나 메모를 제공하면 다음 작업을 수행하세요:

1. **맞춤법 및 문장 교정:** 어색하거나 모호한 표현을 자연스럽고 명확한 문장으로 수정합니다.
2. **문맥에 맞는 톤 조정:**
   - 비즈니스 이메일/보고서: 격식 있고 정중하며 핵심이 바로 드러나는 어조
   - 블로그/SNS/안내문: 친근하고 가독성이 높은 편안한 어조
3. **가독성 개선:** 단락을 보기 좋게 나누고, 중요한 항목은 글머리 기호(bullet points)로 시각화합니다.
EOF

# 3. 파일 생성 위치 및 정상 생성 여부 확인
ls -la ~/antigravity-lab/.agents/agents/writing-assistant.md
```

##### 3. 실제 실행 및 활용 방법

전문화된 서브에이전트는 멘션(`@`)을 붙여 직접 작업을 지시합니다.

> 📍 **실행 위치: 🤖 Antigravity 대화창 (Tab 1 agy 프롬프트)**

- **프롬프트 입력 예시:**

  ```text
  > @writing-assistant 팀원들에게 이번 주 금요일 오후 3시에 2분기 프로젝트 킥오프 온라인 회의가 열린다는 사내 공지 이메일 초안을 작성해줘.
  ```

- **에이전트 실제 응답 결과 (전문 비서 스타일):**
  ```text
  안녕하세요, 문서 작성 비서 writing-assistant입니다. 요청하신 사내 공지 이메일 초안을 정중한 비즈니스 톤으로 작성했습니다:

  ────────────────────────────────────────────────────────
  [제목] [공지] 2분기 프로젝트 킥오프 회의 안내 (금요일 15:00)

  팀원 여러분, 안녕하십니까.

  희망찬 2분기를 맞이하여 새로운 프로젝트 목표를 공유하고 팀별 실행 계획을 논의하고자
  아래와 같이 2분기 프로젝트 킥오프 회의를 진행합니다. 바쁘시더라도 일정 확인 후 참석 부탁드립니다.

  ■ 회의 개요
  - 일시: 2026년 3월 27일 (금요일) 15:00 ~ 16:00 (총 1시간)
  - 방식: 온라인 화상 회의 (Google Meet 링크: meet.google.com/abc-defg-hij)
  - 참석 대상: 프로젝트 전 팀원

  ■ 주요 안건
  1. 2분기 핵심 마일스톤 및 주요 목표 공유
  2. 팀별/개인별 역할과 책임(R&R) 확인
  3. Q&A 및 자유 건의 사항 논의

  사전 검토가 필요한 발표 자료는 회의 전날 메일로 공유해 드릴 예정입니다.
  일정에 변동이 있으신 분은 미리 회신 부탁드립니다. 감사합니다.
  ────────────────────────────────────────────────────────
  ```

---

#### 8-4. Skill (표준 업무 절차) — 개념, 작성 예제 및 실제 활용 방법

##### 1. Skill의 개념 및 작동 원리

- **개념**: 복잡하거나 여러 단계가 필요한 업무를 누구나 일관되게 수행할 수 있도록 만든 **표준 업무 매뉴얼(Workflow / SOP)**입니다.
- **작동 원리 (점진적 노출, Progressive Disclosure)**:
  스킬이 수십 개 등록되어 있더라도 평소에는 이름과 한 줄 설명(`description`)만 가볍게 메모리에 올려둡니다. 사용자가 해당 업무를 요청했을 때만 본문 전체(`SKILL.md`)가 온디맨드로 로드되어 **토큰 낭비를 획기적으로 방지**합니다.

##### 2. Skill 파일 작성 예제 (`.agents/skills/meeting-summary/SKILL.md`)

폴더를 생성하고, 산만한 회의 메모에서 '핵심 결정 사항'과 '담당자별 할 일(Action Items)'을 표로 깔끔하게 정리하는 스킬을 생성합니다:

> 📍 **파일 생성 위치 (절대 경로)**: `~/antigravity-lab/.agents/skills/meeting-summary/SKILL.md`  
> 각 스킬은 고유한 전용 디렉터리(`meeting-summary/`)를 가지며, 그 내부의 `SKILL.md` 파일에 표준 지침을 작성합니다.

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (Tab 2 또는 일반 bash 셸)**

```bash
# 1. Antigravity 워크스페이스 루트로 이동 (파일 생성 위치의 기준점)
cd ~/antigravity-lab

# 2. 스킬 전용 하위 디렉터리 생성 (경로: ~/antigravity-lab/.agents/skills/meeting-summary)
mkdir -p .agents/skills/meeting-summary

# 3. SKILL.md 파일 생성 (경로: ~/antigravity-lab/.agents/skills/meeting-summary/SKILL.md)
cat > .agents/skills/meeting-summary/SKILL.md <<'EOF'
---
name: meeting-summary
title: 회의록 요약 및 할 일(Action Items) 자동 추출 워크플로우
version: 1.0.0
description: 회의 메모나 대화 텍스트를 읽고 핵심 안건, 결정 사항, 담당자별 할 일을 표로 깔끔하게 정리하는 스킬
tags:
  - productivity
  - meeting
  - notes
---

# Meeting Summary Skill Instructions

사용자가 회의 메모, 대화 기록, 또는 미팅 노트를 제공하면 아래 3단계 표준 절차에 따라 정리된 마크다운 문서를 작성하세요:

## 표준 정리 워크플로우

1. **기본 정보 및 안건 요약:**
   - 회의 일시, 참석자, 주요 논의 주제를 상단에 간결하게 정리합니다.
2. **핵심 결정 사항 (Key Decisions):**
   - 회의 중 최종 결정되거나 합의된 사항을 글머리 기호(`-`)로 명확하게 요약합니다.
3. **Action Items (담당자별 할 일 목록 표):**
   - 아래 서식의 마크다운 표를 작성하여 각 항목의 담당자와 마감 기한을 명시합니다:

   | 번호 | 담당자 | 할 일 (Action Item) | 완료 기한 | 우선순위 |
   | :--: | :----: | :------------------ | :-------: | :------: |
   | 1    | 담당자 | 세부 작업 내용      | 마감일    | 보통/높음|
EOF

# 4. 파일 생성 위치 및 정상 생성 여부 확인
ls -la ~/antigravity-lab/.agents/skills/meeting-summary/SKILL.md
```

##### 3. 실제 실행 및 활용 방법

TUI 세션에서 등록된 스킬 목록을 확인하고, 실제 회의 메모 텍스트를 입력하여 표준 절차대로 문서를 자동 정리해 봅니다.

> 📍 **실행 위치: 🤖 Antigravity 대화창 (Tab 1 agy 프롬프트)**

- **스킬 목록 확인:**

  ```text
  > /skills
  ```

  화면에 `meeting-summary` 스킬과 설명이 등록되어 있는지 확인합니다.

- **프롬프트 입력 예시:**

  ```text
  > 아래 회의 메모를 meeting-summary 스킬에 맞춰서 깔끔한 회의록으로 정리해줘:
  >
  > [회의 메모]
  > 3월 25일 마케팅팀 주간회의 진행함. 김팀장, 이대리, 박사원 참석.
  > 봄맞이 프로모션 이벤트 페이지는 이번 주 금요일까지 이대리가 디자인 완료하기로 확정.
  > 고객 대상 설문조사 결과 분석은 박사원이 다음 주 화요일까지 보고서 제출하기로 함.
  > 김팀장은 다음 주 월요일까지 전체 예산안 결재 올릴 예정.
  > 다음 회의는 4월 1일 수요일 오전 10시로 잡음.
  ```

- **에이전트 실제 응답 결과 (스킬의 3단계 워크플로우대로 구조화):**
  ```text
  # 📝 주간 마케팅 회의록

  ## 1. 기본 정보
  - **일시:** 2026년 3월 25일
  - **참석자:** 김팀장, 이대리, 박사원
  - **주요 안건:** 봄맞이 프로모션 준비 및 고객 설문 분석 일정 조율

  ## 2. 핵심 결정 사항 (Key Decisions)
  - 봄맞이 프로모션 이벤트 페이지 디자인 오픈 일정 확정 (이번 주 금요일)
  - 차기 주간 회의: 2026년 4월 1일 (수) 오전 10:00

  ## 3. Action Items (담당자별 할 일 목록)
  | 번호 | 담당자 | 할 일 (Action Item) | 완료 기한 | 우선순위 |
  | :--: | :----: | :--------------------------------- | :----------: | :------: |
  | 1    | 이대리 | 봄맞이 프로모션 이벤트 페이지 디자인 완료 | 이번 주 금요일 | 높음     |
  | 2    | 박사원 | 고객 설문조사 결과 분석 보고서 제출 | 다음 주 화요일 | 보통     |
  | 3    | 김팀장 | 2분기 전체 프로모션 예산안 결재 진행 | 다음 주 월요일 | 보통     |
  ```

---

#### 8-5. Hook (자동화 이벤트 트리거) — 개념, 작성 예제 및 실제 활용 방법

##### 1. Hook의 개념 및 5대 이벤트 유형

- **개념**: 스마트홈의 자동화 루틴(예: "센서가 감지되면 조명을 켠다")이나 스마트폰의 자동 실행 기능처럼, Antigravity에서 **특정 사건(이벤트)이 일어날 때 사전에 지정한 동작(스크립트 또는 명령어)을 자동으로 가로채 실행해 주는 자동화 트리거**입니다.
- **Antigravity 5대 Hook 유형 (`/hooks`)**:
  Antigravity CLI는 에이전트의 작업 단계에 따라 다음 5가지 표준 훅 이벤트를 지원합니다:

  | 훅 이벤트명          | 발생 시점 (When it fires)                      | 주요 역할 및 활용 예시                                             |
  | :------------------- | :--------------------------------------------- | :----------------------------------------------------------------- |
  | **`PreInvocation`**  | 모델(LLM)이 답변을 생성하기 직전               | 답변 전 추가 지침이나 임시 가이드(`ephemeralMessage`) 자동 주입    |
  | **`PostInvocation`** | 모델(LLM)이 답변을 완료한 직후                 | 생성된 답변 검토 및 추가 연속 작업 강제(`force_continue`)          |
  | **`PreToolUse`**     | 도구(명령어 실행, 파일 수정 등) 실행 직전      | 명령어 실행 전 안전 점검 또는 자동 승인(`allow`)/차단(`deny`) 제어 |
  | **`PostToolUse`**    | 도구 실행이 완료된 직후                        | 파일 생성/수정 직후 코드 포맷팅이나 사후 정리 작업 실행            |
  | **`Stop`**           | 에이전트가 작업을 마치고 세션을 종료하려 할 때 | 목표 달성 여부 확인, 종료 차단 또는 세션 마무리 안내               |

##### 2. Hook 파일 작성 예제 (`.agents/hooks.json`)

일반 사용자도 직관적으로 이해할 수 있는 실용적인 훅을 작성합니다:

1. **`PreInvocation` 훅 (`friendly-guide`)**: 에이전트가 답변을 생각하기 직전, "초보자도 이해하기 쉬운 일상 비유로 설명하라"는 실시간 가이드를 모델에 귓속말(`ephemeralMessage`)처럼 주입합니다.
2. **`PreToolUse` 훅 (`command-guard`)**: 에이전트가 터미널 명령어 도구(`run_command`)를 실행할 때 안전하게 자동 승인(`allow`)을 부여합니다.

> 📍 **파일 생성 위치 (절대 경로)**: `~/antigravity-lab/.agents/hooks.json`  
> Antigravity는 워크스페이스 루트의 `.agents/hooks.json` 설정 파일을 자동으로 감지하여 에이전트 라이프사이클 이벤트 발생 시 실행합니다.

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (Tab 2 또는 일반 bash 셸)**

```bash
# 1. Antigravity 워크스페이스 루트로 이동 (파일 생성 위치의 기준점)
cd ~/antigravity-lab

# 2. 5대 훅 규격에 맞춘 Hook 설정 파일 생성 (경로: ~/antigravity-lab/.agents/hooks.json)
cat > .agents/hooks.json <<'EOF'
{
  "friendly-guide": {
    "PreInvocation": [
      {
        "type": "command",
        "command": "echo '{\"injectSteps\": [{\"ephemeralMessage\": \"[사전 가이드] 초보자도 이해하기 쉬운 일상 비유와 함께 친절하게 설명하세요.\"}]}'"
      }
    ]
  },
  "command-guard": {
    "PreToolUse": [
      {
        "matcher": "run_command",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"decision\": \"allow\"}'"
          }
        ]
      }
    ]
  }
}
EOF

# 3. 파일 생성 위치 및 정상 생성 여부 확인
ls -la ~/antigravity-lab/.agents/hooks.json
```

##### 3. 실제 실행 및 활용 방법

Antigravity 세션(`agy`)에서 `/hooks` 명령어를 실행하여 등록된 5대 훅 상태를 확인합니다:

> 📍 **실행 위치: 🤖 Antigravity 대화창 (Tab 1 agy 프롬프트)**

- **등록된 훅 목록 확인 (`/hooks`):**

  ```text
  > /hooks
  ```

  TUI 화면에 아래와 같이 Antigravity 5대 훅 유형 메뉴가 표시됩니다:

  ```text
   Hooks
     5 hook types

     PreToolUse      Before tool execution
     PostToolUse     After tool execution
     PreInvocation   Before each LLM invocation
     PostInvocation  After each LLM invocation
   > Stop            When agent tries to exit
  ```

  - 키보드 방향키(`↑`/`↓`)로 `PreInvocation` 또는 `PreToolUse` 항목을 선택하고 **Enter**를 누르면, 방금 등록한 `friendly-guide`와 `command-guard` 훅이 활성화되어 로드된 것을 확인할 수 있습니다.
  - 확인 후 `Esc` 키를 눌러 대화 화면으로 복귀합니다.

- **프롬프트 입력 및 자동 가이드 주입 확인:**

  ```text
  > 클라우드 방화벽(Firewall)이 뭔지 쉽게 알려줘.
  ```

- **에이전트 실제 응답 결과:**  
  에이전트가 답변을 생성하기 직전 `PreInvocation` 훅이 작동하여 모델에 일상 비유 가이드가 주입되므로, "방화벽은 아파트 입구의 경비실이나 건물 출입 게이트와 같아요!"처럼 일상적인 쉬운 비유와 함께 친절한 설명이 출력됩니다.

---

#### 8-6. Rule, Agent, Skill, Hook 한눈에 비교하기

| 구분               | 역할 (Role)                                   | 비유                      | 로딩 및 적용 방식                             | 호출/실행 방법                       | 실생활/업무 활용 예시                                    |
| :----------------- | :-------------------------------------------- | :------------------------ | :-------------------------------------------- | :----------------------------------- | :------------------------------------------------------- |
| **Rule** (규칙)    | 항상 지켜야 할 말투, 서식, 행동 가이드라인    | 사내 행동 규정, 근무 수칙 | **항시 자동 주입** (Always-on)                | 별도 호출 불필요 (질문 시 자동 적용) | 친절한 존댓말 쓰기, 상단 3줄 요약 강제, 보안 금지어 차단 |
| **Agent** (비서)   | 특정 역할에 특화된 맞춤형 전담 페르소나       | 전문 비서, 특정 부서 직원 | **독립 세션 및 도구 제한**                    | `@에이전트명` 또는 자연어 위임       | 문서 작성 비서, 영어 회화 튜터, 고객 응대 상담원         |
| **Skill** (매뉴얼) | 여러 단계로 진행되는 표준 업무 처리 절차(SOP) | 업무 매뉴얼, 체크리스트   | **필요할 때만 로드** (Progressive Disclosure) | 스킬명 언급 또는 자연어 지시         | 회의록 정리, 주간 업무 보고서 생성, 데이터 클렌징        |
| **Hook** (트리거)  | 특정 상황(이벤트) 발생 시 자동 실행되는 동작  | 스마트홈 루틴, 예약 알람  | 라이프사이클 이벤트 발생 시 **자동 실행**     | 이벤트 발생 시 자동 트리거           | 친절 가이드 자동 주입, 위험 명령어 실행 가드             |

---

#### 8-7. 등록된 커스텀 자산 종합 검증 (All-in-One 테스트)

> [!TIP]
> **새로 생성한 Hook, Skill, Agent 등이 TUI에 잘 안 보일 때의 해결 팁 (세션 재기동)**  
> `.agents/` 디렉터리에 새로운 Rule, Agent, Skill, Hook 설정 파일이나 스크립트를 작성한 직후, 현재 실행 중인 Antigravity TUI 세션의 슬래시 명령어(`/skills`, `/agents`, `/hooks`) 목록에 즉시 나타나지 않거나 이전 캐시 상태로 머물러 있을 수 있습니다.  
> 이 경우 당황하지 마시고 TUI 프롬프트에서 `/exit` 로 세션을 종료한 뒤, 워크스페이스에서 `agy` 를 다시 실행(재기동)하면 새로 작성한 파일들이 정상적으로 감지되어 나타납니다:
>
> 📍 **실행 위치: 🤖 Antigravity 대화창 (Tab 1)**
>
> ```bash
> > /exit
> ```
>
> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (Tab 1 bash 셸)**
>
> ```bash
> cd ~/antigravity-lab
> agy
> ```

방금 생성한 Rule, Agent, Skill, Hook 자산들이 Antigravity TUI 세션 내에서 정상적으로 감지되고 유기적으로 협업하는지 종합 점검합니다:

1. **전체 컴포넌트 목록 점검**:

   > 📍 **실행 위치: 🤖 Antigravity 대화창 (Tab 1 agy 프롬프트)**
   - `/skills` : `meeting-summary` 스킬 등록 확인
   - `/agents` : `writing-assistant` 에이전트 등록 확인
   - `/hooks` : 5개 훅 타입 중 `PreInvocation`(`friendly-guide`), `PreToolUse`(`command-guard`) 등록 확인

2. **종합 연계 협업 테스트 (Agent + Rule + Hook 올인원 시나리오)**:

   > 📍 **실행 위치: 🤖 Antigravity 대화창 (Tab 1 agy 프롬프트)**
   > 프롬프트에 아래와 같이 지시해 봅니다:

   ```text
   > @writing-assistant 이번 주 금요일 오후 3시 2분기 킥오프 온라인 회의에 팀원들을 초대하는 정중한 이메일 초안을 작성해줘.
   ```

3. **기대되는 동작 결과**:
   - **Agent 역할**: `writing-assistant` 비서가 격식 있는 비즈니스 서식으로 이메일 본문을 정중하게 작성합니다.
   - **Rule 가드레일**: `friendly-response` 규칙에 따라 상단에 `[핵심 3줄 요약]`을 먼저 제공하고 친절한 어조를 유지합니다.
   - **Hook 자동 지원**: 에이전트가 생각하기 전 `PreInvocation` 훅이 작동하여 친절한 설명 가이드를 자동 주입하고, 도구 실행 전 `PreToolUse` 가 안전하게 실행을 자동 승인합니다.

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
    │   ├── rules/                           # 답변 스타일, 행동 원칙 및 가드레일 규칙 (.md)
    │   ├── skills/                          # 업무별 표준 처리 절차 워크플로우 (SKILL.md)
    │   ├── agents/                          # 역할별 맞춤형 AI 비서 정의 파일 (.md)
    │   ├── scripts/                         # MCP 서버 또는 자동화 헬퍼 스크립트 (.py)
    │   ├── mcp_config.json                  # 프로젝트 전용 MCP 서버 연동 설정
    │   └── hooks.json                       # 에이전트 라이프사이클 이벤트 훅 정의
    ├── GEMINI.md                            # 워크스페이스 전역 규칙 및 가드레일 (로컬 전용)
    └── .gitignore                           # 시크릿(.env) 및 임시 파일 제외 설정
```

### 4.2 주요 설정 파일 예시

#### 1. 전역 설정 (`~/.gemini/antigravity-cli/settings.json`)

> 📍 **파일 생성 위치 (절대 경로)**: `~/.gemini/antigravity-cli/settings.json`  
> 사용자 홈 디렉터리에 위치하며, 모든 Antigravity 프로젝트에 공통으로 적용되는 전역 설정 파일입니다.

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
# 1. Antigravity 워크스페이스 홈으로 이동
cd ~/antigravity-lab

# 2. 전역 설정 디렉터리 생성 및 settings.json 작성
mkdir -p ~/.gemini/antigravity-cli
cat > ~/.gemini/antigravity-cli/settings.json <<'EOF'
{
  "model": "gemini-3.8-flash",
  "effort": "medium",
  "sandbox": false,
  "dangerously_skip_permissions": false
}
EOF

# 3. 파일 생성 확인
ls -la ~/.gemini/antigravity-cli/settings.json
```

#### 2. 친절한 응답 및 요약 규칙 (`.agents/rules/friendly-response.md`)

> 📍 **파일 생성 위치 (절대 경로)**: `~/antigravity-lab/.agents/rules/friendly-response.md`  
> 워크스페이스 루트의 `.agents/rules/` 에 저장되어 모든 대화에 자동으로 상시 주입되는 행동 규칙입니다.

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
# 1. Antigravity 워크스페이스 홈으로 이동 (파일 생성 기준점)
cd ~/antigravity-lab

# 2. Rule 파일 생성 (경로: ~/antigravity-lab/.agents/rules/friendly-response.md)
cat > .agents/rules/friendly-response.md <<'EOF'
---
trigger: always_on
description: 친절한 한국어 응답 및 3줄 핵심 요약 규칙
---

# 친절한 응답 및 핵심 요약 규칙 (Response Style Rule)

모든 질문에 응답할 때는 다음 지침을 준수하세요:

1. **말투:** 항상 정중하고 친절한 한국어 존댓말(~해요, ~합니다)로 답변하세요.
2. **쉬운 설명:** 전문 용어가 나오면 초보자도 이해하기 쉬운 일상적인 비유나 쉬운 단어로 풀어 설명하세요.
3. **3줄 핵심 요약:** 긴 설명에 앞서, 답변 맨 위에 반드시 `[핵심 3줄 요약]`을 글머리 기호로 먼저 제시하세요.
4. **추천 액션:** 답변 끝에 사용자가 바로 따라 해볼 수 있는 '다음 추천 단계'를 1~2가지 제안하세요.
EOF

# 3. 파일 생성 확인
ls -la ~/antigravity-lab/.agents/rules/friendly-response.md
```

#### 3. 문서 작성 비서 서브에이전트 (`.agents/agents/writing-assistant.md`)

> 📍 **파일 생성 위치 (절대 경로)**: `~/antigravity-lab/.agents/agents/writing-assistant.md`  
> 워크스페이스 루트의 `.agents/agents/` 에 저장되어 `@writing-assistant` 로 호출 가능한 전문 비서입니다.

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
# 1. Antigravity 워크스페이스 홈으로 이동 (파일 생성 기준점)
cd ~/antigravity-lab

# 2. Agent 파일 생성 (경로: ~/antigravity-lab/.agents/agents/writing-assistant.md)
cat > .agents/agents/writing-assistant.md <<'EOF'
---
name: writing-assistant
description: 비즈니스 이메일, 업무 보고서, 공지사항, 블로그 초안 작성 및 문장 교정 전문 비서
model: inherit
tools:
  - view_file
  - list_dir
---

# Writing Assistant Instructions

당신은 직관적이고 설득력 있는 글을 작성하는 전문 문서 비서입니다. 사용자가 초안이나 메모를 제공하면 다음 작업을 수행하세요:

1. **맞춤법 및 문장 교정:** 어색하거나 모호한 표현을 자연스럽고 명확한 문장으로 수정합니다.
2. **문맥에 맞는 톤 조정:**
   - 비즈니스 이메일/보고서: 격식 있고 정중하며 핵심이 바로 드러나는 어조
   - 블로그/SNS/안내문: 친근하고 가독성이 높은 편안한 어조
3. **가독성 개선:** 단락을 보기 좋게 나누고, 중요한 항목은 글머리 기호(bullet points)로 시각화합니다.
EOF

# 3. 파일 생성 확인
ls -la ~/antigravity-lab/.agents/agents/writing-assistant.md
```

#### 4. 회의록 정리 및 할 일 추출 스킬 (`.agents/skills/meeting-summary/SKILL.md`)

> 📍 **파일 생성 위치 (절대 경로)**: `~/antigravity-lab/.agents/skills/meeting-summary/SKILL.md`  
> 워크스페이스 루트의 `.agents/skills/meeting-summary/` 디렉터리에 저장되는 표준 업무 절차 지침서입니다.

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
# 1. Antigravity 워크스페이스 홈으로 이동 (파일 생성 기준점)
cd ~/antigravity-lab

# 2. 스킬 전용 하위 디렉터리 생성 및 SKILL.md 작성
mkdir -p .agents/skills/meeting-summary
cat > .agents/skills/meeting-summary/SKILL.md <<'EOF'
---
name: meeting-summary
title: 회의록 요약 및 할 일(Action Items) 자동 추출 워크플로우
version: 1.0.0
description: 회의 메모나 대화 텍스트를 읽고 핵심 안건, 결정 사항, 담당자별 할 일을 표로 깔끔하게 정리하는 스킬
tags:
  - productivity
  - meeting
  - notes
---

# Meeting Summary Skill Instructions

사용자가 회의 메모, 대화 기록, 또는 미팅 노트를 제공하면 아래 3단계 표준 절차에 따라 정리된 마크다운 문서를 작성하세요:

## 표준 정리 워크플로우

1. **기본 정보 및 안건 요약:**
   - 회의 일시, 참석자, 주요 논의 주제를 상단에 간결하게 정리합니다.
2. **핵심 결정 사항 (Key Decisions):**
   - 회의 중 최종 결정되거나 합의된 사항을 글머리 기호(`-`)로 명확하게 요약합니다.
3. **Action Items (담당자별 할 일 목록 표):**
   - 아래 서식의 마크다운 표를 작성하여 각 항목의 담당자와 마감 기한을 명시합니다:

   | 번호 | 담당자 | 할 일 (Action Item) | 완료 기한 | 우선순위 |
   | :--: | :----: | :------------------ | :-------: | :------: |
   | 1    | 홍길동 | 기획안 초안 공유    | 이번 주 금 | 높음     |
EOF

# 3. 파일 생성 확인
ls -la ~/antigravity-lab/.agents/skills/meeting-summary/SKILL.md
```

#### 5. 사전 가이드 및 명령어 자동 승인 훅 (`.agents/hooks.json`)

> 📍 **파일 생성 위치 (절대 경로)**: `~/antigravity-lab/.agents/hooks.json`  
> 워크스페이스 루트의 `.agents/hooks.json` 에 정의되어 Antigravity 5대 훅 이벤트(`PreInvocation`, `PreToolUse` 등) 발생 시 실행되는 트리거 설정입니다.

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
# 1. Antigravity 워크스페이스 홈으로 이동 (파일 생성 기준점)
cd ~/antigravity-lab

# 2. Hook 설정 파일 생성 (경로: ~/antigravity-lab/.agents/hooks.json)
cat > .agents/hooks.json <<'EOF'
{
  "friendly-guide": {
    "PreInvocation": [
      {
        "type": "command",
        "command": "echo '{\"injectSteps\": [{\"ephemeralMessage\": \"[사전 가이드] 초보자도 이해하기 쉬운 일상 비유와 함께 친절하게 설명하세요.\"}]}'"
      }
    ]
  },
  "command-guard": {
    "PreToolUse": [
      {
        "matcher": "run_command",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"decision\": \"allow\"}'"
          }
        ]
      }
    ]
  }
}
EOF

# 3. 파일 생성 확인
ls -la ~/antigravity-lab/.agents/hooks.json
```

---

## 5. Cloud Shell 환경 문제 해결 및 FAQ (Troubleshooting)

### Q1. `agy: command not found` 오류가 발생합니다.

- **원인:** 바이너리가 PATH에 등록되지 않았습니다.
- **해결 방법:**
  > 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**
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
  > 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**
  ```bash
  cd ~/antigravity-lab
  export $(dbus-launch)
  agy
  ```

### Q4. 일정 시간 후 Cloud Shell 터미널 연결이 끊겼습니다.

- **원인:** Cloud Shell은 약 20분 이상 유휴(idle) 상태가 지속되면 세션이 자동 종료됩니다.
- **해결 방법:** 브라우저에서 **Reconnect**를 클릭하여 다시 접속한 뒤 가상환경을 재활성화하고 실습을 이어갑니다:
  > 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**
  ```bash
  cd ~/antigravity-lab
  source .venv/bin/activate
  agy
  ```

### Q5. `/config`에서 `always-proceed`가 `disabled by admin`으로 표시됩니다.

- **원인:** 조직(관리자) 정책으로 해당 권한 모드가 차단된 상태입니다.
- **해결 방법:** 기본값인 `request-review`를 그대로 사용하고 도구 호출 시 수동으로 승인합니다. 실습 진행에는 아무런 문제가 없습니다.

### Q6. `.agents/`에 생성한 Rule, Agent, Skill, Hook이 TUI 화면에 나타나지 않습니다.

- **원인:** 세션이 실행 중인 상태에서 백그라운드 터미널이나 다른 탭에서 파일을 새로 생성한 경우, CLI 프로세스의 인메모리 캐시 또는 파일 감지 지연으로 인해 즉시 반영되지 않을 수 있습니다.
- **해결 방법:** TUI 세션을 종료하고 `agy` 를 다시 실행(재기동)하면 워크스페이스의 `.agents` 하위 파일들을 새로 스캔하여 정상적으로 로드합니다:

  > 📍 **실행 위치: 🤖 Antigravity 대화창 (TUI 세션)**

  ```text
  /exit
  ```

  > 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

  ```bash
  cd ~/antigravity-lab
  agy
  ```

  재기동 후 `/skills`, `/agents`, `/hooks` 명령어를 다시 실행하면 방금 생성한 자산들이 정상적으로 표시됩니다.

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
