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

Antigravity의 설정 및 커스터마이징 파일은 다음과 같은 계층 구조로 관리됩니다.

```text
~/.gemini/antigravity-cli/          # 전역(Global) 설정 디렉터리
├── config.json                     # 전역 CLI 환경설정
├── brain/                          # 세션 트랜스크립트 및 아티팩트 저장소
└── builtin/skills/                 # 내장 스킬 모듈

<프로젝트 루트>/                    # 프로젝트(Local) 워크스페이스
├── .agents/
│   ├── agents/                     # 커스텀 서브에이전트 정의 (.md)
│   ├── rules/                      # 가드레일 및 코딩 컨벤션 규칙 (.md)
│   └── skills/                     # 프로젝트 전용 스킬 정의 (SKILL.md)
└── .gitignore
```

#### 프로젝트 가드레일 및 규칙 예시 설정

`.agents/rules/` 디렉터리를 만들고 기본 커밋/에러 핸들링 규칙을 배치할 수 있습니다.

```bash
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

## 4. 문제 해결 및 FAQ (Troubleshooting)

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

## 5. 실습 완료 체크리스트

- [ ] Python 3.10 이상 버전 확인 및 가상환경 활성화 완료
- [ ] Antigravity CLI 바이너리 설치 및 `agy --version` 확인 완료
- [ ] Google 계정 로그인 (`agy login`) 및 인증 완료
- [ ] 실습 워크스페이스 생성 및 신뢰(Trust) 승인 완료
- [ ] `agy` TUI 실행 및 `/help` 명령어 정상 작동 확인 완료
