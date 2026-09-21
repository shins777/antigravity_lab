# Antigravity 웹앱 핸즈온 랩 (agy_webapp)

> **대상:** GCP Cloud Shell 환경에서 Antigravity CLI(`agy`) 설치 및 로그인을 마친 개발자
> **목표:** `agy` 에이전트와 함께 **Cloud Shell 환경에서 바로 실행하고 웹 미리보기로 확인하는 웹 애플리케이션 2개**를 완성한다.
> **전제 조건:** [agy_basic.md](./agy_basic.md) 의 Cloud Shell 설치·로그인 단계를 완료한 상태

| Lab   | 만드는 것                                                  | 스택                            | 포트 | 브라우저 접속 방법      |
| ----- | ---------------------------------------------------------- | ------------------------------- | ---- | ----------------------- |
| **A** | Cloud Shell 인스턴스의 **실시간 시스템 모니터링 대시보드** | Python · FastAPI · psutil · SSE | 8000 | 웹 미리보기 (포트 8000) |
| **B** | 브라우저에서 바로 즐기는 **테트리스 게임**                 | Node.js · Express · Canvas      | 3000 | 웹 미리보기 (포트 3000) |

---

## 1. 실습 준비

### 1-1. 작업공간 및 실습 폴더 생성

> 📍 **실행 위치: 🖥️ [Cloud Shell 터미널 ①]** (일반 bash 셸)

[agy_basic.md](./agy_basic.md) 에서 생성한 워크스페이스 루트(`~/antigravity-lab`)로 이동한 뒤, 실제 소스코드가 작성될 `agy_webapp` 디렉터리와 하위 프로젝트 폴더들(`sysinfo_dashboard`, `tetris_game`)을 만듭니다.

```bash
# 1. 워크스페이스 루트로 이동
cd ~/antigravity-lab
pwd

# 2. agy_webapp 실습 디렉터리 및 하위 프로젝트 폴더 일괄 생성
mkdir -p ~/antigravity-lab/agy_webapp/sysinfo_dashboard
mkdir -p ~/antigravity-lab/agy_webapp/tetris_game

# 3. 생성된 디렉터리 구조 확인
ls -la ~/antigravity-lab/agy_webapp
```

> [!NOTE]
> **디렉터리 역할 및 구성**
>
> - **워크스페이스 루트 (`~/antigravity-lab`)**: Antigravity CLI(`agy`)를 실행하고 프로젝트 전역 규칙 파일(`AGENTS.md`)이 위치하는 최상위 디렉터리입니다.
> - **웹앱 실습 폴더 (`~/antigravity-lab/agy_webapp`)**: 이번 랩의 애플리케이션 프로젝트 소스코드가 위치하는 공간입니다.
>   - **Lab A (`~/antigravity-lab/agy_webapp/sysinfo_dashboard`)**: 실시간 시스템 대시보드 FastAPI 애플리케이션 소스코드 및 가상환경
>   - **Lab B (`~/antigravity-lab/agy_webapp/tetris_game`)**: 테트리스 웹 게임 Express 애플리케이션 소스코드 및 정적 자산

### 1-2. 환경 확인

> 📍 **실행 위치: 🖥️ [Cloud Shell 터미널 ①]** (일반 bash 셸)

Cloud Shell에는 실습에 필요한 기본 도구가 사전에 모두 설치되어 있습니다. 버전을 확인합니다.

```bash
python3 --version    # 3.10 이상 (Cloud Shell 기본 3.11+)
node --version       # 18 이상 (Cloud Shell 기본 설치됨)
curl --version
```

### 1-3. 프로젝트 규칙 파일(`AGENTS.md`) 작성

> 📍 **실행 위치: 🖥️ [Cloud Shell 터미널 ①]** (일반 bash 셸)

> [!IMPORTANT]
> **`AGENTS.md`의 적합한 위치: `~/antigravity-lab/AGENTS.md` (워크스페이스 루트)**
>
> - Antigravity CLI(`agy`)는 세션이 실행된 현재 작업 디렉터리(`~/antigravity-lab`)에서 `AGENTS.md` 또는 `GEMINI.md`를 검색하여 에이전트의 시스템 컨텍스트로 자동 주입합니다.
> - 워크스페이스 최상위 루트에 규칙 파일을 두면, 에이전트가 `agy_webapp/sysinfo_dashboard/` 및 `agy_webapp/tetris_game/` 프로젝트의 코드를 작성할 때 공통 환경 및 개별 기술 스택 규칙을 빠짐없이 인식하여 적용합니다.

아래 명령을 실행하여 워크스페이스 루트(`~/antigravity-lab`)에 `AGENTS.md`를 생성합니다.

```bash
# 1. 워크스페이스 루트로 이동
cd ~/antigravity-lab

# 2. 워크스페이스 루트에 AGENTS.md 생성
cat > ~/antigravity-lab/AGENTS.md <<'MDEOF'
# antigravity-lab 실습 규칙

## 공통 환경
- 실행 환경은 GCP Cloud Shell (Debian Linux bash) 컨테이너다.
- 워크스페이스 루트는 `~/antigravity-lab` 이다.
- 이번 웹앱 실습의 모든 소스코드는 `agy_webapp/` 하위 디렉터리(`agy_webapp/sysinfo_dashboard/`, `agy_webapp/tetris_game/`)에 작성한다.
- 로컬 개발 및 Cloud Shell 웹 미리보기(Web Preview) 전용 예제다. 배포 설정(Docker, k8s, CI)은 만들지 않는다.
- 비밀키·토큰·API 키를 코드에 하드코딩하지 않는다.
- 포트는 Lab A=8000, Lab B=3000 으로 고정한다.
- 서버 바인딩 호스트는 0.0.0.0 또는 127.0.0.1 을 지원하도록 한다.
- 프런트엔드는 외부 CDN·프레임워크 없이 순수 HTML/CSS/JS 로만 작성한다.

## 실행 스크립트 (필수)
- 각 프로젝트 루트(`agy_webapp/sysinfo_dashboard/`, `agy_webapp/tetris_game/`)에 아래 3개 bash 스크립트를 반드시 작성한다.
  - run.sh    : 의존성 설치 + 포트 정리 + 서버 백그라운드/포그라운드 실행까지 한 번에
  - verify.sh : 주요 엔드포인트를 curl 등으로 점검하고 ✅/❌ 로 결과 출력
  - stop.sh   : 해당 포트(8000 또는 3000)를 사용하는 프로세스 종료
- 셸 스크립트(*.sh)에는 `chmod +x` 로 실행 권한을 부여한다.
- 스크립트는 어느 경로에서 실행해도 동작하도록 자기 디렉터리(`cd "$(dirname "$0")"`)로 이동한 뒤 작업한다.
- 실패 시 원인을 한글로 명확히 출력하고 0이 아닌 종료 코드로 마감한다.

## Lab A (Python) — agy_webapp/sysinfo_dashboard/
- FastAPI + uvicorn + psutil 사용. 타입 힌트와 Pydantic 모델을 반드시 쓴다.
- 의존성은 가상환경(`agy_webapp/sysinfo_dashboard/.venv`) 안에만 설치한다. 전역 pip install 금지.
- Linux 가상 컨테이너 환경을 전제로 작성하되, 지원되지 않는 지표(온도, 배터리 등)는 예외를 삼키지 말고
  {"supported": false, "reason": "..."} 형태로 명시해 반환한다.
- 테스트는 pytest 로 작성한다.

## Lab B (Node.js) — agy_webapp/tetris_game/
- Express 사용. CommonJS(require) 문법으로 작성한다.
- 외부 의존성은 express 하나만. 나머지는 Node 내장 모듈(fs, path, http 등)로 해결한다.

## 오류 처리
- 예외를 빈 블록으로 삼키지 않는다 (`except Exception: pass`, 빈 `catch {}` 금지).
- 오류 응답은 HTTP 상태 코드와 사유를 JSON 으로 명확히 반환한다.
- 구체적인 예외 타입(ValueError, PermissionError 등)을 사용한다.

## 검증
- 코드 작성 후 반드시 서버를 띄우고 verify.sh 스크립트로 엔드포인트를 점검한 뒤 결과를 보고한다.
MDEOF

# 3. 파일 위치 및 내용 확인
ls -la ~/antigravity-lab/AGENTS.md
```

### 1-4. Antigravity CLI 실행 및 초기 설정

> 📍 **실행 위치: 🖥️ [Cloud Shell 터미널 ①]** (일반 bash 셸)

워크스페이스 루트(`~/antigravity-lab`)에서 Antigravity CLI를 실행하여 **대화형 TUI 세션으로 진입**합니다.

```bash
cd ~/antigravity-lab
agy
```

처음 진입하는 디렉터리이므로 워크스페이스 신뢰 확인 프롬프트가 나타나면 방향키로 `Yes, I trust this folder` 를 선택하고 Enter를 누릅니다.

---

> 📍 **실행 위치: 🤖 [agy 대화창 (터미널 ①)]** (화면 하단 `> ` 프롬프트)

이제 터미널이 Antigravity 대화창 화면으로 바뀌었습니다. 여기서부터는 **자연어 및 슬래시(`/`) 명령**을 입력합니다.

**Tool Permission 설정 변경 (실습 편의용)**

기본값(`request-review`)에서는 에이전트가 파일을 쓰거나 명령을 실행할 때마다 승인을 요청합니다.
이 랩은 생성할 파일이 많으므로 **실습 동안만** 자동 진행으로 바꿔 둡니다.

1. agy 프롬프트(`> `)에서 아래 명령을 입력하고 Enter를 누릅니다.
   ```text
   /config
   ```
2. 메뉴 목록에서 **Tool Permission** 항목으로 방향키를 이용해 이동합니다.
3. **`always-proceed`** 를 선택하고 **Enter** 로 저장합니다. (설정 창을 닫으려면 `Esc`를 누릅니다.)

_`/config` 의 Tool Permission 설정 화면_
<p align="left"><img style="border: 1px solid #e0e0e0; border-radius: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);" src="resources/webapp/lab1-1.png" width="700" alt="agy /config 의 Tool Permission 설정 화면"></p>

> [!WARNING]
> `always-proceed` 는 사용자 확인 없이 파일 수정·명령 실행을 수행합니다. **실습용 편의 설정**으로만 사용하고,
> 실제 운영 프로젝트에서는 기본값 `request-review` 유지를 권장합니다.
> 조직 정책에 따라 `(disabled by admin)` 으로 표시되어 선택할 수 없다면 기본값을 그대로 두고
> 각 도구 호출 시 수동으로 승인(`y` 또는 `A`)하면 됩니다.

✅ **확인 체크리스트**

- [ ] 상단 헤더에 로그인된 Google 계정과 현재 경로(`~/antigravity-lab`)가 표시된다.
- [ ] agy 프롬프트에서 `!ls` 를 입력했을 때 워크스페이스 루트의 `AGENTS.md` 와 `agy_webapp` 디렉터리가 확인된다.
- [ ] agy 프롬프트에서 `!ls agy_webapp` 를 입력했을 때 `sysinfo_dashboard` 와 `tetris_game` 폴더가 확인된다.

---

## 2. Lab A. Cloud Shell 실시간 시스템 대시보드

🎯 **목표:** 지금 실행 중인 **Cloud Shell 가상 인스턴스의 시스템 정보**를 실시간으로 수집하고, 브라우저에서 **웹 미리보기(포트 8000)** 로 갱신되는 대시보드를 구축한다.

> [!TIP]
> **실습 핵심 포인트: "클라우드 컨테이너 환경의 지표 지원 여부 처리"**
> Cloud Shell은 가상화된 Linux 컨테이너이므로 물리 하드웨어 센서(CPU 온도, 팬 속도)나 노트북 배터리 지표가 노출되지 않습니다.
> 에이전트에게 _"지원되지 않는 지표는 빈 값이나 가짜 0으로 채우지 말고, `{"supported": false, "reason": "..."}` 형태로 정직하게 명시하고 UI에 '미지원' 배지를 띄우라"_ 고 요구하는 엔지니어링 패턴을 실습합니다.

### 2-1. 완성 후 프로젝트 구조

> [!TIP]
> **폴더 위치 및 경로 가이드**:
>
> - 워크스페이스 루트는 `~/antigravity-lab/` 이며, 실제 소스코드가 작성되는 프로젝트 경로는 `~/antigravity-lab/agy_webapp/sysinfo_dashboard/` 입니다.
> - `agy` 프롬프트에 `agy_webapp/sysinfo_dashboard/` 경로를 명시하여 이 디렉터리 내부에만 모든 소스코드와 파일이 생성되도록 지시합니다.

```text
~/antigravity-lab/
├── AGENTS.md
└── agy_webapp/
    └── sysinfo_dashboard/
        ├── .venv/                  # 가상환경 (커밋 대상 아님)
        ├── app/
        │   ├── __init__.py
        │   ├── main.py             # FastAPI 앱 · 정적 서빙 · SSE 스트리밍
        │   ├── models.py           # Pydantic 응답 모델
        │   └── collectors.py       # psutil 기반 지표 수집기 (지원 여부 분기)
        ├── static/
        │   ├── index.html          # 대시보드 UI (순수 HTML)
        │   ├── app.js              # EventSource(SSE) 구독 및 DOM 렌더링
        │   └── style.css           # 다크 테마 카드 레이아웃
        ├── tests/
        │   └── test_api.py         # pytest 기반 엔드포인트 단위 테스트
        ├── run.sh                  # ⭐ 의존성 설치 + 포트 정리 + uvicorn 서버 실행
        ├── verify.sh               # ⭐ 엔드포인트 자동 점검 (curl 기반)
        ├── stop.sh                 # ⭐ 8000 포트 점유 프로세스 종료
        ├── requirements.txt        # fastapi, uvicorn, psutil, pytest, httpx
        └── README.md
```

**수집 대상 및 Cloud Shell(Linux) 지원 여부**

| 카테고리 | 항목                                                          | Cloud Shell 지원 상태          | 비고                                   |
| -------- | ------------------------------------------------------------- | ------------------------------ | -------------------------------------- |
| 시스템   | OS 이름/릴리스/버전, 커널, 호스트명, 아키텍처, 부팅/가동 시간 | ✅ 지원                        | Linux 컨테이너 정보 정상 수집          |
| CPU      | 논리/물리 코어 수, 코어별 사용률, 전체 사용률, 주파수         | ✅ 지원                        | vCPU 사양 반영                         |
| CPU      | Load Average (1분 / 5분 / 15분)                               | ✅ 지원                        | Linux 네이티브 지원                    |
| 메모리   | 총량/사용량/가용량/사용률, 스왑 총량/사용량/사용률            | ✅ 지원                        | 가상 머신 할당 메모리                  |
| 디스크   | 마운트별(루트, /home) 용량/사용률, 디스크 I/O                 | ✅ 지원                        | Cloud Shell 영구 스토리지 지표         |
| 네트워크 | 인터페이스별 IP/MAC, 송수신 바이트·패킷, 초당 전송 속도       | ✅ 지원                        | 가상 네트워크 인터페이스               |
| 프로세스 | 총 프로세스 수, CPU/메모리 점유 상위 10개                     | ✅ 지원                        | psutil.process_iter() 기반             |
| 센서     | CPU 온도, 팬 회전수                                           | ⚠️ 미지원 (`supported: false`) | 컨테이너 환경으로 하드웨어 센서 미제공 |
| 전원     | 배터리 잔량, 충전 상태                                        | ⚠️ 미지원 (`supported: false`) | 클라우드 서버 인스턴스 특성            |

**엔드포인트 명세**

| 메서드 | 경로                               | 설명                                               |
| ------ | ---------------------------------- | -------------------------------------------------- |
| `GET`  | `/`                                | 대시보드 웹 UI (static/index.html)                 |
| `GET`  | `/api/system`                      | 정적 사양 정보 (OS, 커널, CPU 모델, 마운트 목록)   |
| `GET`  | `/api/metrics`                     | 실시간 시스템 지표 1회 스냅샷                      |
| `GET`  | `/api/processes?sort=cpu&limit=10` | CPU 또는 메모리 기준 상위 프로세스 목록            |
| `GET`  | `/api/stream`                      | **SSE(Server-Sent Events)** 2초 간격 실시간 스트림 |
| `GET`  | `/health`                          | 서버 상태 헬스 체크 (`{"status": "ok"}`)           |

---

### 2-2. Step 1 — 계획 요청

> 📍 **실행 위치: 🤖 [agy 대화창 (터미널 ①)]** (하단 `> ` 프롬프트에 붙여넣기)

`agy` 프롬프트에 **아래 프롬프트를 그대로 복사하여 입력합니다.**

```text
/planning
현재 워크스페이스(~/antigravity-lab) 내의 agy_webapp/sysinfo_dashboard/ 디렉터리에
GCP Cloud Shell (Linux) 환경의 실시간 시스템 정보를 보여주는 FastAPI 웹 대시보드를 만들려고 해.
모든 소스 파일과 스크립트는 반드시 agy_webapp/sysinfo_dashboard/ 폴더 내부에 작성되도록 설계해줘. 먼저 시스템 환경을 파악하고 안정적으로 동작하는 구조로 계획을 세워줘.

[수집 항목]
1. 시스템: OS 이름/릴리스, 커널, 호스트명, 아키텍처, Python 버전, 부팅 시각, 가동 시간(human-readable)
2. CPU: 논리/물리 코어 수, 전체 사용률, 코어별 사용률 배열, 주파수, Load Average (1/5/15분)
3. 메모리: total/used/available/percent, 스왑 total/used/percent
4. 디스크: 파티션별 mountpoint/fstype/total/used/percent, 읽기·쓰기 I/O
5. 네트워크: 인터페이스별 IP/MAC, 송수신 바이트·패킷, 직전 샘플 대비 초당 속도(KB/s)
6. 프로세스: 전체 개수, CPU 상위 10개, 메모리 상위 10개 (pid, name, cpu_percent, memory_percent)
7. 센서/배터리: Cloud Shell 가상 컨테이너 환경이므로 psutil 미지원 시 {"supported": false, "reason": "Cloud Shell container does not expose sensors/battery"} 형태로 반환

[설계 요구사항]
- 지원되지 않는 지표는 빈 값이나 0으로 덮지 말고 supported: false 와 사유를 명시해 반환하고, UI 카드에 "미지원" 배지를 표시한다.
- PermissionError 등 권한 부족은 {"error": "permission denied"} 로 명확히 구분한다.
- FastAPI uvicorn 서버는 Cloud Shell 웹 미리보기가 가능하도록 host="0.0.0.0", port=8000 으로 바인딩한다.

[엔드포인트]
- GET /                 : static/index.html
- GET /api/system       : 정적 사양 정보 (캐시)
- GET /api/metrics      : 현재 시스템 스냅샷
- GET /api/processes?sort=cpu|memory&limit=N
- GET /api/stream       : SSE 2초 간격 스트림 (클라이언트 연결 종료 시 태스크 정리 필수)
- GET /health           : {"status":"ok"}

[UI 요구사항 — static/index.html + app.js + style.css]
- 깔끔한 다크 테마 카드 레이아웃
- CPU 코어별 사용률 막대 게이지 (코어 수에 맞게 자동 생성)
- 메모리/스왑/디스크 사용률 게이지 (80% 이상 빨강 / 60~80% 주황 / 이하 초록)
- 네트워크 속도는 최근 30개 샘플 스파크라인 막대로 표시
- 프로세스 표: CPU / 메모리 정렬 토글 버튼 제공
- EventSource 로 /api/stream 구독, 끊김 시 자동 재연결 안내
- 외부 CDN 없이 순수 HTML/CSS/JS 로만 작성

[실행 스크립트 — agy_webapp/sysinfo_dashboard/ 하위에 반드시 3개 모두 작성]
- run.sh : .venv 생성 및 활성화 → requirements.txt 설치 → 8000 포트 정리 →
  uvicorn 실행 (0.0.0.0:8000). 실행 전 "Cloud Shell 웹 미리보기(포트 8000)를 여세요" 안내 출력.
- verify.sh : 서버가 떠 있는 상태에서 curl 로 주요 엔드포인트(/health, /api/system, /api/metrics, /api/processes)를 점검하고 항목별 ✅/❌ 및 최종 성공 여부를 출력. 실패 시 exit 1.
- stop.sh : 8000 포트를 점유한 프로세스를 안전하게 종료.
- 모든 스크립트에는 `chmod +x` 실행 권한을 부여하고, 스크립트 위치로 cd 후 실행되게 작성.

[테스트]
- tests/test_api.py : pytest 기반 엔드포인트 응답 상태 및 스키마 검증

아직 전체 코드는 작성하지 말고, agy_webapp/sysinfo_dashboard/ 내부 디렉터리 구조, 모듈 책임, 데이터 스키마, 스크립트 흐름이 담긴 계획을 먼저 아티팩트로 작성해줘.
```

계획이 생성되면 프롬프트에 **`승인합니다`** 또는 `Ctrl+R` 후 `y` 로 승인합니다.

---

### 2-3. Step 2 — 구현 요청

> 📍 **실행 위치: 🤖 [agy 대화창 (터미널 ①)]** (하단 `> ` 프롬프트에 붙여넣기)

`agy` 프롬프트에 아래를 입력합니다.

```text
작성된 계획대로 agy_webapp/sysinfo_dashboard/ 디렉터리 내부에 구현을 진행해줘.
모든 파일은 반드시 agy_webapp/sysinfo_dashboard/ 하위 경로에 생성해야 해:
1) agy_webapp/sysinfo_dashboard/requirements.txt (fastapi, uvicorn, psutil, pytest, httpx)
2) agy_webapp/sysinfo_dashboard/app/models.py, app/collectors.py, app/main.py
3) agy_webapp/sysinfo_dashboard/static/index.html, static/app.js, static/style.css
4) agy_webapp/sysinfo_dashboard/tests/test_api.py
5) agy_webapp/sysinfo_dashboard/run.sh, verify.sh, stop.sh (chmod +x 적용)

모든 파일 작성이 끝나면 agy_webapp/sysinfo_dashboard/ 디렉터리 내에 가상환경(.venv)을 만들고 의존성을 설치한 뒤,
agy_webapp/sysinfo_dashboard/.venv/bin/python -m pytest -q agy_webapp/sysinfo_dashboard/tests 로 테스트를 실행해줘.
테스트가 실패하면 통과할 때까지 원인을 분석해 수정해줘.
```

에이전트가 파일들을 생성하고 테스트를 실행합니다. 완료될 때까지 기다립니다.

---

### 2-4. Step 3 — 서버 실행 및 웹 미리보기 접속

이제 서버를 백그라운드로 실행하고 Cloud Shell 브라우저 기능으로 접속합니다.

> 📍 **실행 위치: 🖥️ [Cloud Shell 터미널 ②]** (새 bash 탭 열기)
>
> Cloud Shell 터미널 상단 탭 바 우측의 **`+` (새 탭 열기)** 버튼을 클릭하여 **두 번째 터미널 탭(터미널 ②)** 을 열어 아래 명령을 실행합니다.

```bash
cd ~/antigravity-lab/agy_webapp/sysinfo_dashboard
./run.sh
```

출력 예시:

```text
▶ 가상환경 확인 및 생성...
▶ 의존성 설치 완료.
▶ 기존 8000 포트 정리 완료.
▶ Uvicorn 서버를 시작합니다 (http://0.0.0.0:8000)
▶ Cloud Shell 상단 [웹 미리보기] -> [포트 변경] -> 8000 을 입력해 접속하세요.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

#### 🌐 브라우저에서 화면 확인하기 — Cloud Shell 웹 미리보기(Web Preview)

Cloud Shell 내부의 웹 앱은 로컬 PC의 `http://localhost:8000` 으로는 열리지 않습니다. Cloud Shell의 **웹 미리보기** 기능을 사용합니다.

1. Cloud Shell 창 우측 상단의 **웹 미리보기(Web Preview)** 아이콘(👁 또는 창 모양 아이콘)을 클릭합니다.
2. 메뉴에서 **포트 변경(Change port)** 을 클릭합니다.
3. 포트 번호에 **`8000`** 을 입력하고 **변경 및 미리보기(Change and Preview)** 버튼을 누릅니다.
4. 새 브라우저 탭에 대시보드 화면이 열리며, CPU/메모리/디스크/네트워크 지표가 실시간(2초 간격)으로 깜빡이며 갱신되는 것을 확인합니다.
5. FastAPI 자동 생성 API 문서는 브라우저 주소 뒤에 `/docs` 를 붙여 확인할 수 있습니다.

---

### 2-5. Step 4 — 기능 검증 및 부하 테스트

> 📍 **실행 위치: 🖥️ [Cloud Shell 터미널 ③]** (새 bash 탭 열기)
>
> Cloud Shell 터미널 상단의 **`+` (새 탭 열기)** 를 눌러 **세 번째 터미널 탭(터미널 ③)** 을 열어 검증 스크립트를 실행합니다.

```bash
cd ~/antigravity-lab/agy_webapp/sysinfo_dashboard
./verify.sh
```

출력 예시:

```text
▶ 엔드포인트 점검 (http://127.0.0.1:8000)
  ✅ GET /health                  200 OK
  ✅ GET /api/system              200 OK
  ✅ GET /api/metrics             200 OK
  ✅ GET /api/processes?limit=5   200 OK
  ✅ GET /api/processes?sort=bad  400 Bad Request
  ✅ GET /api/nonexistent         404 Not Found

▶ 이 환경에서 미지원으로 보고된 지표:
  - sensors: Cloud Shell container does not expose sensors/battery
  - battery: Cloud Shell container does not expose sensors/battery

✅ 전체 검증 통과!
```

**CPU 부하 테스트로 그래프 반응 확인**

> 📍 **실행 위치: 🖥️ [Cloud Shell 터미널 ③]** (일반 bash 셸)

터미널 ③에서 인위적으로 CPU 부하를 발생시켜 대시보드 브라우저의 CPU 코어 사용률 막대가 치솟는지 확인합니다.

```bash
# 4개 프로세스로 CPU 부하 생성 (10초 후 자동 정리)
for i in 1 2 3 4; do (yes > /dev/null &); done; sleep 10; killall yes
```

부하가 걸리는 동안 대시보드 탭의 CPU 사용률 그래프가 급증했다가 10초 후 정상으로 내려앉는 것을 관찰합니다.

**서버 종료 방법**

> 📍 **실행 위치: 🖥️ [Cloud Shell 터미널 ③]** (일반 bash 셸)
>
> 터미널 ③에서 아래 명령을 실행하거나, 서버가 실행 중인 터미널 ②에서 `Ctrl+C` 를 누릅니다.

```bash
./stop.sh
```

---

### 2-6. Step 5 — 개선 요청 실습

> 📍 **실행 위치: 🤖 [agy 대화창 (터미널 ①)]** (하단 `> ` 프롬프트에 붙여넣기)

`agy` 터미널 탭(터미널 ①)으로 돌아와 아래 중 관심 있는 개선안을 골라 요청해 보세요.

```text
@app/main.py 최근 5분간의 CPU와 메모리 사용률을 링버퍼(deque)에 보관하고,
GET /api/history?minutes=5 로 조회할 수 있는 엔드포인트를 추가해줘.
static/index.html 상단에 이 데이터를 기반으로 최근 5분 사용률 추이 미니 그래프를 렌더링하고,
verify.sh 에도 /api/history 점검 항목을 추가해줘.
```

```text
@static/app.js 메모리 사용률이 80%를 초과하면 화면 상단에 경고 배너를 표시하고
해당 카드 테두리를 붉은색으로 깜빡이게(CSS 애니메이션) 해줘.
```

수정 후 터미널 ②에서 `./run.sh`, 터미널 ③에서 `./verify.sh` 를 실행해 결과를 확인합니다.

---

### 2-7. Lab A 트러블슈팅

| 증상                                              | 원인                                               | 해결 방법                                                         |
| ------------------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------------- |
| `Address already in use` (8000)                   | 이전 서버 프로세스가 백그라운드에 남아 있음        | 🖥️ 터미널 ③에서 `./stop.sh` 실행                                  |
| `Permission denied: ./run.sh`                     | 스크립트 실행 권한 누락                            | 🖥️ 터미널 ③에서 `chmod +x *.sh` 실행                              |
| 웹 미리보기 창에 `502 Bad Gateway` 또는 연결 거부 | 서버가 아직 뜨지 않았거나 `127.0.0.1`에만 바인딩됨 | 서버 로그 확인, uvicorn 옵션에 `--host 0.0.0.0 --port 8000` 확인  |
| 웹 미리보기가 엉뚱한 포트로 열림                  | 기본 포트(8080)로 접속됨                           | 웹 미리보기 메뉴에서 **포트 변경** → **8000** 지정                |
| 모니터링 센서/배터리가 "미지원"으로 뜸            | Cloud Shell 가상 컨테이너 특성                     | **정상 동작**. 예외로 죽지 않고 `supported: false` 로 처리된 것임 |

✅ **Lab A 완료 확인**

- [ ] `./run.sh` 한 번으로 가상환경 구축 및 서버 구동이 완료된다.
- [ ] Cloud Shell **웹 미리보기(포트 8000)** 에서 실시간 시스템 대시보드가 열린다.
- [ ] `./verify.sh` 가 모든 엔드포인트에 대해 `✅` 통과를 출력한다.
- [ ] 부하 명령 시 대시보드 그래프가 실시간으로 반응한다.
- [ ] `./stop.sh` 로 서버가 정상 종료된다.

---

## 3. Lab B. 웹 테트리스 게임

🎯 **목표:** Node.js Express 기반의 정적 서빙 및 점수 랭킹 API 서버를 구축하고, HTML5 Canvas로 브라우저에서 직접 플레이할 수 있는 테트리스 게임을 완성한다.

### 3-1. 세션 정리

> 📍 **실행 위치: 🤖 [agy 대화창 (터미널 ①)]** (하단 `> ` 프롬프트)

Lab A의 대화 맥락을 비우고 산뜻하게 시작합니다. (작성된 파일들은 디스크에 안전하게 보존됩니다.)

```text
/clear
```

---

### 3-2. 완성 후 프로젝트 구조

> [!TIP]
> **폴더 위치 및 경로 가이드**:
>
> - 워크스페이스 루트는 `~/antigravity-lab/` 이며, 테트리스 소스코드 및 데이터가 작성되는 실제 경로는 `~/antigravity-lab/agy_webapp/tetris_game/` 입니다.
> - `agy` 프롬프트에 `agy_webapp/tetris_game/` 경로를 명시하여 이 디렉터리 내부에만 모든 파일이 작성되도록 지시합니다.

```text
~/antigravity-lab/
├── AGENTS.md
└── agy_webapp/
    └── tetris_game/
        ├── node_modules/           # 의존성 (커밋 대상 아님)
        ├── public/
        │   ├── index.html          # 게임 화면 (보드, 다음 블록, 점수판, 랭킹)
        │   ├── tetris.js           # Canvas 게임 로직 (조작, 충돌, 회전, 7-bag)
        │   └── style.css           # 아케이드 다크 테마 스타일
        ├── data/
        │   └── scores.json         # 랭킹 점수 데이터 (자동 생성)
        ├── server.js               # Express 서버 (정적 파일 서빙 + 점수 API)
        ├── run.sh                  # ⭐ npm install + 3000 포트 정리 + 서버 실행
        ├── verify.sh               # ⭐ 점수 API 유효성 검증
        ├── stop.sh                 # ⭐ 3000 포트 점유 프로세스 종료
        ├── package.json
        └── README.md
```

**게임 사양 및 기능 요약**

| 항목        | 내용                                                                                                                    |
| ----------- | ----------------------------------------------------------------------------------------------------------------------- |
| 보드 사양   | 10열 × 20행, Canvas 2D 렌더링                                                                                           |
| 테트로미노  | 7종 (I, O, T, S, Z, J, L) 표준 색상 및 7-bag 무작위 생성 알고리즘                                                       |
| 조작 키     | `←`/`→`: 좌우 이동 · `↑`: 시계방향 회전 · `↓`: 소프트드롭 · `Space`: 하드드롭 · `C`: 홀드 · `P`: 일시정지 · `R`: 재시작 |
| 점수 체계   | 1줄 100점 · 2줄 300점 · 3줄 500점 · 4줄(Tetris) 800점 (레벨 배수 적용)                                                  |
| 레벨업      | 10줄 삭제 시마다 레벨 상승 및 블록 낙하 속도 증가                                                                       |
| 시각 보조   | 고스트 피스 (블록 착지 예상 위치 반투명 표시), 다음 블록 3개 미리보기                                                   |
| 랭킹 시스템 | 게임 오버 시 닉네임 입력 → `POST /api/scores` 로 점수 서버 저장 및 TOP 10 갱신                                          |

**엔드포인트 명세 (포트 3000)**

| 메서드 | 경로                   | 설명                                              |
| ------ | ---------------------- | ------------------------------------------------- |
| `GET`  | `/`                    | 게임 화면 (`public/index.html`)                   |
| `GET`  | `/api/scores?limit=10` | 랭킹 조회 (점수 내림차순 정렬)                    |
| `POST` | `/api/scores`          | 점수 등록 (`{"name": "...", "score": 1200, ...}`) |
| `GET`  | `/health`              | 서버 헬스 체크 (`{"status": "ok"}`)               |

---

### 3-3. Step 1 — 계획 + 구현 요청

> 📍 **실행 위치: 🤖 [agy 대화창 (터미널 ①)]** (하단 `> ` 프롬프트에 붙여넣기)

`agy` 프롬프트에 **아래 요청을 그대로 붙여넣습니다.**

```text
/planning
현재 워크스페이스(~/antigravity-lab) 내의 agy_webapp/tetris_game/ 디렉터리에
브라우저에서 바로 플레이하고 점수 랭킹을 기록할 수 있는 Express + HTML5 Canvas 테트리스 웹 게임을 만들어줘.
모든 파일(소스 코드, 데이터, 스크립트)은 반드시 agy_webapp/tetris_game/ 폴더 내부에 작성되어야 해:

[서버 — agy_webapp/tetris_game/server.js, 포트 3000]
- 외부 의존성은 express 하나만 사용하고, 파일 I/O는 Node.js 내장 fs, path 모듈 사용.
- Cloud Shell 환경에서 웹 미리보기가 가능하도록 0.0.0.0 또는 포트 3000 리슨.
- GET  /                    : agy_webapp/tetris_game/public/ 정적 파일 서빙
- GET  /api/scores?limit=10 : agy_webapp/tetris_game/data/scores.json 에서 점수 내림차순 정렬 후 상위 목록 반환
- POST /api/scores          : {name, score, lines, level} 점수 등록
    · name: 1~12자 문자열 (공백만 있으면 400 에러)
    · score, lines, level: 0 이상 정수가 아니면 400 에러
    · agy_webapp/tetris_game/data/ 디렉터리가 없으면 자동 생성하고, 원자적(임시 파일 작성 후 rename)으로 저장
- GET  /health              : {"status":"ok"}

[게임 엔진 — agy_webapp/tetris_game/public/tetris.js]
- 보드 10x20 그리드 Canvas 렌더링
- 7종 테트로미노 표준 색상, 7-bag 랜덤 순환 알고리즘
- 벽/바닥/블록 충돌 판정 및 간단한 좌우 wall kick 회전 보정
- 조작키: ArrowLeft/Right(이동), ArrowUp(회전), ArrowDown(소프트드롭),
         Space(하드드롭, e.preventDefault 로 페이지 스크롤 방지),
         C(홀드, 1턴 1회), P(일시정지), R(재시작)
- 고스트 피스(낙하 예상 위치 반투명 표시)
- 줄 삭제 점수 (1줄 100, 2줄 300, 3줄 500, 4줄 800 * (레벨+1))
- 10줄마다 레벨업 및 낙하 속도 가속
- 게임 오버 오버레이 + 닉네임 입력 폼 → POST /api/scores 연동

[UI — agy_webapp/tetris_game/public/index.html, agy_webapp/tetris_game/public/style.css]
- 레트로 아케이드 느낌의 깔끔한 다크 테마
- 좌측: 홀드 슬롯 / 중앙: 테트리스 캔버스 / 우측: 다음 블록 3개 + 점수/레벨/줄 수
- 우측 하단: TOP 10 랭킹 실시간 테이블
- 하단: 단축키 안내 바
- 외부 라이브러리/이미지 없이 순수 Canvas/CSS 로 구성

[실행 스크립트 — agy_webapp/tetris_game/ 하위에 필수 3개 작성]
- agy_webapp/tetris_game/run.sh    : node_modules 확인 및 npm install → 3000 포트 정리 → node server.js 실행.
  실행 전 "Cloud Shell 웹 미리보기(포트 3000)를 여세요" 안내 출력.
- agy_webapp/tetris_game/verify.sh : curl 로 /health, 정상 POST /api/scores, 비정상 POST(400 검증), GET /api/scores 점검 후 ✅/❌ 출력. 실패 시 exit 1.
- agy_webapp/tetris_game/stop.sh   : 3000 포트 점유 프로세스 종료.
- 모든 스크립트에 chmod +x 부여.

계획을 먼저 아티팩트로 보여주고, 승인하면 바로 agy_webapp/tetris_game/ 디렉터리 내부에 구현 및 npm install 까지 완료해줘.
```

계획이 승인되면 에이전트가 코드를 작성하고 `npm install`을 실행합니다.

---

### 3-4. Step 2 — 실행 및 게임 플레이

> 📍 **실행 위치: 🖥️ [Cloud Shell 터미널 ②]** (서버 탭)

터미널 ②로 이동하여 테트리스 서버를 구동합니다.

```bash
cd ~/antigravity-lab/agy_webapp/tetris_game
./run.sh
```

출력 예시:

```text
▶ Node 의존성 확인...
▶ 기존 3000 포트 정리 완료.
▶ Tetris 서버를 포트 3000에서 실행합니다.
▶ Cloud Shell 상단 [웹 미리보기] -> [포트 변경] -> 3000 을 입력해 접속하세요.
Tetris server listening on http://0.0.0.0:3000
```

#### 🌐 브라우저에서 테트리스 즐기기 — 웹 미리보기(포트 3000)

1. Cloud Shell 창 우측 상단의 **웹 미리보기(Web Preview)** 아이콘을 클릭합니다.
2. **포트 변경(Change port)** 을 클릭합니다.
3. 포트 번호에 **`3000`** 을 입력하고 **변경 및 미리보기(Change and Preview)** 를 누릅니다.
4. 브라우저 탭에 테트리스 게임이 열립니다!

**게임 플레이 체크포인트**

- [ ] 방향키(`←`, `→`, `↓`, `↑`) 조작 및 블록 낙하가 부드러운가?
- [ ] `Space` 키를 눌렀을 때 화면 스크롤 없이 하드드롭되는가?
- [ ] 블록이 1줄 완성되면 지워지며 점수가 올라가는가?
- [ ] 게임 오버 시 이름을 입력하면 우측 하단 랭킹판에 즉시 기록되는가?

---

### 3-5. Step 3 — 검증

> 📍 **실행 위치: 🖥️ [Cloud Shell 터미널 ③]** (검증 탭)

터미널 ③에서 점수 API 검증 스크립트를 실행합니다.

```bash
cd ~/antigravity-lab/agy_webapp/tetris_game
./verify.sh
```

출력 예시:

```text
▶ 테트리스 API 점검 (http://127.0.0.1:3000)
  ✅ GET  /health                       200 OK
  ✅ POST /api/scores (정상 점수 등록)     200 OK
  ✅ POST /api/scores (공백 이름 차단)     400 Bad Request
  ✅ POST /api/scores (음수 점수 차단)     400 Bad Request
  ✅ GET  /api/scores?limit=10          200 OK (배열 데이터 반환)
  ✅ GET  /api/unknown                  404 Not Found

✅ 전체 검증 통과!
```

저장된 점수 파일 확인:

```bash
cat data/scores.json
```

**서버 종료**

```bash
./stop.sh
```

---

### 3-6. Step 4 — 개선 요청 실습

> 📍 **실행 위치: 🤖 [agy 대화창 (터미널 ①)]** (하단 `> ` 프롬프트)

`agy` 터미널 탭(터미널 ①)에서 원하는 기능을 추가해 보세요.

```text
@agy_webapp/tetris_game/public/tetris.js 줄이 완성되어 삭제될 때 해당 줄이 하얗게 0.15초간 깜빡인 후
사라지는 시각 효과(애니메이션)를 추가해줘. 애니메이션 재생 중에는 블록 입력을 잠시 대기시켜줘.
```

```text
@agy_webapp/tetris_game/public/tetris.js T-스핀(T-Spin)을 판별하는 로직을 추가하고,
T-스핀으로 줄을 지우면 보드 중앙에 "T-SPIN!" 축하 텍스트를 1초간 띄우고 보너스 점수(1200점)를 부여해줘.
```

```text
@agy_webapp/tetris_game/server.js 같은 플레이어 이름으로 점수를 등록할 때,
기존 점수보다 높은 경우에만 랭킹을 갱신하고 낮은 점수면 갱신하지 않는 로직을 반영해줘.
agy_webapp/tetris_game/verify.sh 에도 이 중복 점수 갱신 방지 테스트를 추가해줘.
```

---

### 3-7. Lab B 트러블슈팅

| 증상                                   | 원인                       | 해결 방법                                                           |
| -------------------------------------- | -------------------------- | ------------------------------------------------------------------- |
| `EADDRINUSE :::3000`                   | 3000 포트 프로세스 잔존    | 🖥️ 터미널 ③에서 `./stop.sh` 실행                                    |
| `Cannot find module 'express'`         | npm 패키지 미설치          | 🖥️ 터미널 ③에서 `npm install` 실행                                  |
| 블록 이동 키가 먹지 않음               | 브라우저 포커스 누락       | 캔버스 화면을 마우스로 한 번 클릭하여 포커스 부여                   |
| 스페이스바 누르면 브라우저 스크롤 발생 | `keydown` 기본 동작 미방지 | 🤖 agy에게 `e.code === 'Space'` 에서 `e.preventDefault()` 적용 요청 |
| 웹 미리보기에 화면이 안 뜸             | 포트 번호 불일치           | 웹 미리보기 메뉴에서 포트가 **3000**인지 확인                       |

✅ **Lab B 완료 확인**

- [ ] `./run.sh` 로 Express 서버가 정상 기동된다.
- [ ] Cloud Shell **웹 미리보기(포트 3000)** 에서 테트리스 플레이 및 점수 저장이 정상 작동한다.
- [ ] `./verify.sh` 가 점수 등록/조회 및 유효성 검증을 통과한다.
- [ ] `./stop.sh` 로 서버가 정상 종료된다.

---

## 4. 실습 정리 및 마무리

### 4-1. 실습 정리 및 서버 종료

> 📍 **실행 위치: 🖥️ [Cloud Shell 터미널 ③]** (일반 bash 셸)

실습을 마치면 백그라운드에 남아 있는 서버들을 모두 종료합니다.

```bash
cd ~/antigravity-lab
(cd agy_webapp/sysinfo_dashboard && ./stop.sh) 2>/dev/null
(cd agy_webapp/tetris_game && ./stop.sh) 2>/dev/null

# 생성된 프로젝트 구조 확인
find agy_webapp -maxdepth 2 -not -path '*/node_modules*' -not -path '*/.venv*' -not -path '*/.git*'
```

**`.gitignore` 설정 (권장)**

가상환경(`.venv`), Node 모듈(`node_modules`), 로컬 점수 파일이 git에 추적되지 않도록 설정합니다.

```bash
cat >> .gitignore <<'MDEOF'
.venv/
node_modules/
__pycache__/
*.pyc
data/scores.json
MDEOF

git status --short
```

---

### 4-2. 최종 학습 체크리스트

- [ ] 일반 리눅스 셸 명령(bash)과 Antigravity TUI 명령(agy)의 실행 위치 차이를 이해했다.
- [ ] 다중 터미널 탭을 활용해 agy 세션, 서버 실행, 검증 작업을 분리하여 진행했다.
- [ ] Cloud Shell **웹 미리보기(Web Preview)** 기능을 통해 포트 8000과 3000 웹 앱을 브라우저에서 직접 조작했다.
- [ ] Lab A: 클라우드 가상 컨테이너의 시스템 모니터링 대시보드를 구축하고 SSE 실시간 스트리밍을 구현했다.
- [ ] Lab A: 미지원 하드웨어 지표를 `supported: false` 로 정직하게 핸들링하는 설계를 경험했다.
- [ ] Lab B: Node.js Express + HTML5 Canvas 테트리스 게임을 완성하고 REST API 점수 랭킹을 연동했다.
- [ ] `run.sh`, `verify.sh`, `stop.sh` 3대 스크립트로 서버 라이프사이클을 안전하게 제어했다.

---

## 부록 A. Cloud Shell 웹앱 개발을 위한 좋은 프롬프트 패턴

| 패턴                    | 비효율적인 예          | 효과적인 예                                                                                   |
| ----------------------- | ---------------------- | --------------------------------------------------------------------------------------------- |
| **검증 수단 제공**      | "테스트해줘"           | "`./verify.sh` 를 실행해서 전부 통과할 때까지 원인을 찾아 수정해줘"                           |
| **포트 및 바인딩 명시** | "서버 띄워줘"          | "Cloud Shell 웹 미리보기 접속을 위해 host=0.0.0.0, port=8000 으로 바인딩해줘"                 |
| **파일 지정**           | "대시보드 고쳐줘"      | "`@app/collectors.py` 의 네트워크 수집 함수에서 초당 속도 계산 오류를 수정해줘"               |
| **제약 명시**           | "UI 만들어줘"          | "외부 CDN이나 무거운 프레임워크 없이 순수 HTML/CSS/JS 로만 구성해줘"                          |
| **미지원 지표 처리**    | "정보 다 보여줘"       | "컨테이너 환경에서 미지원되는 센서는 0으로 속이지 말고 `supported: false` 와 사유를 반환해줘" |
| **단계 분할**           | "테트리스 다 만들어줘" | "일단 이동·회전·줄삭제 기본 루프만 먼저 작성해줘. 확인 후 랭킹과 이펙트를 추가할게"           |
| **오류 전달**           | "에러 나는데?"         | (터미널이나 브라우저 개발자 도구 콘솔의 오류 메시지 전체를 그대로 붙여넣기)                   |

---

## 부록 B. 다음 단계

- [agy_basic.md](./agy_basic.md) — Antigravity Cloud Shell 설치 및 환경 구성 가이드
- [agy_command.md](./agy_command.md) — Antigravity CLI 명령어 및 단축키 전체 가이드
