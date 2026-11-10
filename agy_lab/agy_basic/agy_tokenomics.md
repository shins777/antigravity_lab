# Antigravity 토크노믹스(Tokenomics) 및 심화 아키텍처 가이드 (agy_tokenomics)

본 문서는 **GCP Cloud Shell** 및 로컬 개발 환경에서 **Antigravity CLI(`agy`)** 의 기초 사용법을 마친 중급 개발자(소프트웨어 엔지니어, 솔루션 아키텍트, 테크 리드)를 위한 **실무 심화 아키텍처 핸즈온 가이드**입니다.

> [!NOTE]
> **선수 과정 안내**:  
> 본 실습은 [agy_basic.md](./agy_basic.md)의 환경 설정, 계정 인증, 기본 TUI 조작 및 기초 `/plan` 실습을 완료한 상태를 전제로 합니다.  
> 단순한 파일 생성이나 기초 명령어 소개는 생략하고, 대규모 프로덕션 환경에서 필수적인 **토큰 비용 최적화**, **컨텍스트 오염 방지**, **0-토큰 결정론적 보안 가드레일**, 그리고 **조직 단위 플러그인(Plugin) 패키징**에 집중합니다.

---

## 📑 목차 (Table of Contents)

1. [심화 학습 목표](#1-심화-학습-목표)
2. [사전 준비 및 워크스페이스 초기화](#2-사전-준비-및-워크스페이스-초기화)
3. [단계별 심화 실습 (Hands-on Steps)](#3-단계별-심화-실습-hands-on-steps)
- [Step 1: 대규모 컨텍스트 보호를 위한 서브에이전트(Subagent) 위임 모델](#step-1-대규모-컨텍스트-보호를-위한-서브에이전트subagent-위임-모델)
- [Step 2: 토큰 비용 절감을 위한 점진적 공개(Progressive Disclosure) Skill 엔지니어링](#step-2-토큰-경제학progressive-disclosure-기반-계층적-skill-엔지니어링)
- [Step 3: 확률적 LLM을 제어하는 0-토큰 결정론적 라이프사이클 Hook 가드레일](#step-3-0-토큰-결정론적deterministic-가드레일-lifecycle-hook)
- [Step 4: 종합 실습 (Capstone) - Antigravity Plugin 원클릭 패키징](#step-4-종합-실습-capstone---antigravity-plugin-원클릭-패키징)
4. [아키텍처 비교 요약표](#4-아키텍처-비교-요약표)
5. [다음 단계](#5-다음-단계)

---

## 1. 심화 학습 목표

1. **컨텍스트 격리**: 서브에이전트 위임 모델을 구현하여 방대한 조사 중에도 메인 세션의 기억을 보존합니다.
2. **토큰 최적화**: 점진적 공개(Progressive Disclosure) Skill을 설계하여 불필요한 상시 토큰 소모를 차단합니다.
3. **결정론적 보안**: 0-토큰 Lifecycle Hook을 구축하여 OS 프로세스 레벨에서 위험 명령을 원천 차단합니다.
4. **플러그인 모듈화**: Skill과 Hook을 결합한 Antigravity Plugin을 구성하고 안전한 배포 시나리오를 완성합니다.
5. **전사 거버넌스**: 단일 하네스 통제와 4단계 불변 방어선 기반의 엔터프라이즈 거버넌스 체계를 확립합니다.

---

## 2. 사전 준비 및 워크스페이스 초기화

실습 워크스페이스(`~/antigravity-lab`)로 이동하여 이번 심화 프로젝트 전용 디렉터리를 준비합니다.

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
# 1. 워크스페이스 확인 및 이동
cd ~/antigravity-lab
pwd

# 2. 토크노믹스 실습 전용 디렉터리 구조 초기화
mkdir -p ~/antigravity-lab/agy_tokenomics
mkdir -p ~/antigravity-lab/.agents/skills
mkdir -p ~/antigravity-lab/.agents/scripts

# 3. 환경 버전 확인 (Node 18+, Python 3.10+)
python3 --version
node --version
agy --version
```

---

## 3. 단계별 심화 실습 (Hands-on Steps)

## Step 1: 대규모 컨텍스트 보호를 위한 서브에이전트(Subagent) 위임 모델

### 1-1. 단일 세션의 한계: 컨텍스트 윈도우 오염 (Context Bloat)

대규모 프로젝트에서 메인 에이전트에게 "프로젝트 전체 의존성의 취약점을 점검하고, 수십 개의 설정 파일과 깃 로그를 조사해줘"라고 지시하면 다음과 같은 치명적인 문제가 발생합니다:
1. **토큰 폭증**: 수만 줄의 로그와 파일 내용이 메인 대화 세션에 그대로 적재되어 매 턴마다 수만 토큰이 소모됩니다.
2. **기억력 상실 (Context Degradation)**: 모델의 주의 집중(Attention)이 분산되어, 사용자가 초반에 지시했던 핵심 요구사항이나 아키텍처 규칙을 망각합니다.

### 1-2. Subagent 아키텍처: 작업 격리와 단방향 결과 수신

Antigravity는 이 문제를 **서브에이전트(Subagent) 위임 패턴**으로 해결합니다.

```
┌────────────────────────────────────────────────────────┐
│  메인 에이전트 (Orchestrator)                           │
│  - 사용자 요구사항 청취 및 큰 틀의 계획 수립           │
│  - 컨텍스트 유지: 3,000 ~ 5,000 토큰으로 가볍게 유지    │
└───────────────────────────┬────────────────────────────┘
                            │ invoke_subagent (또는 /owl)
                            ▼
┌────────────────────────────────────────────────────────┐
│  격리된 서브에이전트 (Worker: research / reviewer)     │
│  - 분기된 독립 워크스페이스/세션에서 수십 번의 도구 호출 │
│  - 50,000 ~ 100,000 토큰 소모 후 자체 종료            │
│  - ⭐ 최종 정제된 요약(Synthesized Summary)만 메인에 반환│
└────────────────────────────────────────────────────────┘
```

### 1-3. [실습] 격리 리서치 서브에이전트(`research.md`) 명시적 정의

Antigravity는 기본 내장 `research` 에이전트도 지원하지만, 프로젝트 특성에 맞는 권한과 시스템 프롬프트를 부여하기 위해 **커스텀 서브에이전트**를 `.agents/agents/` 디렉터리에 명시적으로 정의합니다.

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
mkdir -p ~/antigravity-lab/.agents/agents

cat > ~/antigravity-lab/.agents/agents/research.md <<'EOF'
---
name: research
description: 외부 기술 문서 탐색 및 컨테이너/보안 권고안 조사를 전담하는 격리 리서치 에이전트
tools:
  - search_web
  - view_file
  - grep_search
mainAgent: true
subagent: true
model: flash_lite
commandExecutionPolicy: sandbox
---

# Research Agent Instructions

당신은 기술 리서치 및 보안 권고안 분석을 전담하는 서브에이전트입니다.

## 역할 및 행동 원칙
1. **격리 탐색 (Isolated Investigation):** 웹 검색 및 로컬 문서를 깊이 있게 조사하되, 분석 과정의 방대한 원시 텍스트(Raw Log)는 서브에이전트 세션 내에서만 소비합니다.
2. **컨텍스트 오염 방지:** 메인 에이전트에게 결과를 반환할 때는 메인 컨텍스트 윈도우 보존을 위해 **정제된 핵심 권고안(3줄 글머리 기호)**만 전달합니다.
3. **읽기 전용 원칙:** 파일 수정이나 시스템 변경 없이 정보 수집과 요약에만 집중합니다.
EOF
```

> [!NOTE]
> * `mainAgent: true`: `/agents` TUI 목록 및 세션 시작 시(`agy --agent research`) 직접 대화 상대로 선택할 수 있게 등록합니다.
> * `subagent: true`: 메인 오케스트레이터의 `invoke_subagent` 도구에 의해 백그라운드 작업으로 호출 가능하게 등록합니다.
> * `model: flash_lite`: 메인 에이전트의 모델을 상속받지 않고, 경량·고속 티어인 `flash_lite`를 지정하여 토큰 비용을 최소화하고 응답 속도를 극대화합니다. Antigravity는 티어 별칭(`flash_lite`, `flash`, `pro`, `inherit`)을 지원하므로 세부 버전 번호를 적지 않아도 최신 안정 모델로 자동 매핑되며, 특정 버전 고정이 필요할 때만 풀 모델명(예: `gemini-2.5-flash-lite`)을 직접 명시하면 됩니다.
> * `tools`: `search_web`, `view_file`, `grep_search` 등 읽기 전용 도구만 부여하여 불필요한 시스템 수정 권한을 차단(최소 권한 원칙)합니다.

##### 🔍 에이전트 등록 확인 (`/agents`)

새로 생성한 `research` 에이전트가 정상적으로 Antigravity에 등록되었는지 대화창에서 확인합니다.

> ⚠️ **주의**: `agy`가 이미 실행 중인 상태에서 파일을 생성했다면, 새로운 에이전트 파일을 인식할 수 있도록 세션을 재시작(`Ctrl + C` 또는 `/exit` 후 `agy` 재실행)해야 합니다.

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
cd ~/antigravity-lab
agy
```

> 📍 **실행 위치: 🤖 Antigravity 대화창 (agy 프롬프트)**

```text
/agents
```

**TUI 화면 확인 예시:**
```text
Available Agents
> ● default        Default agent
   code-reviewer  코드 보안 취약점, 성능 병목, 스타일 가이드 분...
   research       외부 기술 문서 탐색 및 컨테이너/보안 권고안 조...
```

* `research` 에이전트가 목록에 정상 노출되는 것을 확인한 후 `Esc` 키를 눌러 에이전트 선택창을 닫고 기본 대화창으로 돌아옵니다.

---

### 1-4. [실습] 서브에이전트 호출 및 격리 보안 리서치 수행

메인 대화창의 토큰을 보존하면서 외부 보안 권고안을 조사하는 작업을 새로 정의한 서브에이전트에게 위임합니다.

> 📍 **실행 위치: 🤖 Antigravity 대화창 (agy 프롬프트)**

```text
리서치 전담 서브에이전트(research)를 호출해서 Python 기반 마이크로서비스 배포 시 반드시 적용해야 할 '컨테이너 보안 및 최소 권한(Least Privilege) 원칙 3가지'를 조사해와. 메인 대화창에는 분석 과정의 긴 로그 없이 핵심 권고안만 3줄 글머리 기호로 정제해서 보고해줘.
```

#### 동작 결과 관찰

1. 에이전트 내부 실행 로그에 `invoke_subagent`가 가동되어 `.agents/agents/research.md`가 호출되는 것을 확인합니다.
2. 서브에이전트는 격리된 세션에서 자료를 탐색 및 분석한 뒤, 메인 대화창에는 긴 파일 내용이나 원본 로그를 일체 남기지 않고 **정제된 3줄 요약 결과**만을 전달합니다.
3. 이로써 메인 에이전트 세션의 컨텍스트 윈도우는 깨끗하게 보존됩니다.

---

### 1-5. [검증] 서브에이전트 실행 내역 및 토큰 절감 상태 검증

서브에이전트가 실제로 격리된 채 실행되었는지, 메인 컨텍스트 윈도우(토큰)가 얼마나 보존되었는지 직접 확인합니다.

##### 1. `/context` 명령어로 메인 에이전트 토큰 보존 확인
대화창에 다음 명령어를 입력하여 **현재 세션의 메인 에이전트 컨텍스트 상태**를 점검합니다.

> [!NOTE]
> `/context`는 누적 통계가 아니라 **"현재 실행 중인 단일 세션(Per-Session)"**에서 **메인 에이전트(Orchestrator)**가 기억하고 있는 활성 컨텍스트 윈도우 점유율만을 보여줍니다.

> 📍 **실행 위치: 🤖 Antigravity 대화창 (agy 프롬프트)**

```text
/context
```

**출력 화면 확인 예시:**
```text
───────────────────────────────────────────────────────────────────────────────────────────────────────────────
└ Context Usage
◉ ◉ ◉ □ □ □ □ □ □ □ □ □ □ □ □ □ □ □ □ □ □ □     Gemini 3.6 Flash (Low) · 18.2k/1.0M tokens (1.8%)
Token usage by category
◉ User messages: 85 tokens (0.0%)
◉ Agent responses: 240 tokens (0.0%)
◉ Tool calls: 180 tokens (0.0%)
⛁ Subagents: 612 tokens (0.1%)
⛁ System overhead: 17.7k tokens (1.7%)
□ Free space: 1.0M (98.2%)
```

* **핵심 확인 포인트 (`⛁ Subagents: 612 tokens`)**:
  * 화면에 찍힌 **`⛁ Subagents: 612 tokens`**는 서브에이전트가 격리 세션에서 소모한 전체 토큰(웹 검색, 문서 파싱 등 수만 토큰)이 **아닙니다**.
  * 현재 세션에서 메인 에이전트가 서브에이전트에게 전달한 **호출 지시문(Prompt)**과, 서브에이전트가 조사를 마친 후 메인 대화창에 최종 보고한 **정제된 3줄 요약문**만이 메인 컨텍스트 윈도우에 점유된 수치(약 600 토큰)입니다.
  * 서브에이전트를 쓰지 않았다면 메인 컨텍스트에 수만 토큰의 웹 검색 로그가 그대로 쏟아져 들어왔을 것이나, 격리 위임 패턴 덕분에 **98% 이상의 토큰을 절감**하여 메인 세션을 가볍게 보존했음을 명확히 증명합니다.

##### 2. 서브에이전트 내부 실행 상세 로그 펼쳐보기 (`Ctrl + O`)
대화창에서 서브에이전트 실행 블록을 선택하고 단축키를 눌러 격리 세션 내부의 실제 동작 내역을 검증합니다.

```text
● Agent(research: Research Agent)(Python 마이크로서비스 컨테이너 보안...) (ctrl+o to expand)
```

1. 키보드 방향키로 `● Agent(research: ...)` 줄에 커서를 위치시킵니다.
2. **`Ctrl + O`**를 누르면 접혀 있던 블록이 펼쳐지면서 서브에이전트가 내부적으로 실행한 세부 도구 호출(`search_web`, `view_file` 등)과 원본 수집 데이터 전문을 직접 확인할 수 있습니다.
3. 확인 후 다시 **`Ctrl + O`**를 누르면 깔끔하게 접힙니다.

##### 3. [심화 실습] 서브에이전트별 토큰 통계 스크립트 작성 및 실행

메인 컨텍스트(`/context`)의 612 토큰 뒤편에서 서브에이전트가 실제로 몇 번 호출되었고, 총 몇 개의 토큰을 사용했는지(호출당 평균 토큰 포함) 핵심 수치만 간결하게 확인하는 파이썬 스크립트를 작성합니다.

> 💡 **세션 단위(Per-Session) 동일성**:
> `/context`가 **"현재 세션의 메인 에이전트"** 컨텍스트 점유량을 보여주듯이, 이 스크립트 역시 **"동일한 현재 세션"**에서 활동한 서브에이전트들의 백그라운드 소비량을 추적합니다. 두 지표는 동일 세션 기준이므로 1:1로 직접 대조할 수 있습니다.

###### ① 초간단 토큰 집계 스크립트(`scripts/subagent_tokens.py`) 생성

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
mkdir -p ~/antigravity-lab/scripts

cat > ~/antigravity-lab/scripts/subagent_tokens.py <<'EOF'
#!/usr/bin/env python3
"""서브에이전트별 호출 횟수, 총 소비 토큰, 호출당 평균 토큰 분석기"""
import glob, json, os, sys

def main():
    # 1. 대상 로그 파일 탐색 (가장 최근 세션 로그)
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        latest_log = sys.argv[1]
    else:
        log_files = glob.glob(os.path.expanduser("~/.gemini/antigravity-cli/brain/*/.system_generated/logs/transcript.jsonl"))
        if not log_files:
            print("❌ 세션 로그를 찾을 수 없습니다. 먼저 `agy`를 한 번 실행해 주세요.")
            return
        latest_log = max(log_files, key=os.path.getmtime)

    agent_stats = {}  # {에이전트명: {"calls": 0, "tokens": 0}}
    current_agent = "main"

    # 2. 로그 파일 파싱 및 집계
    with open(latest_log, "r", encoding="utf-8") as f:
        for line in f:
            try:
                step = json.loads(line)
            except Exception:
                continue

            # 서브에이전트 호출 감지
            for tc in step.get("tool_calls", []):
                if tc.get("name") == "invoke_subagent":
                    name = tc.get("args", {}).get("TypeName", "subagent")
                    current_agent = name
                    if name not in agent_stats:
                        agent_stats[name] = {"calls": 0, "tokens": 0}
                    agent_stats[name]["calls"] += 1

            # 토큰 합산
            in_tok = step.get("input_tokens") or 0
            out_tok = step.get("output_tokens") or 0
            tok_sum = in_tok + out_tok

            if current_agent != "main" and tok_sum > 0:
                agent_stats[current_agent]["tokens"] += tok_sum

    # 3. 통계 출력
    print("\n" + "=" * 55)
    print(" 🤖 서브에이전트별 토큰 사용 통계")
    print("=" * 55)
    print(f" {'에이전트 명':<14} | {'호출 횟수':>8} | {'총 소비 토큰':>10} | {'호출당 평균':>10}")
    print("-" * 55)

    if not agent_stats:
        print("  최근 세션에서 호출된 서브에이전트가 없습니다.")
    else:
        for name, data in agent_stats.items():
            calls = data["calls"]
            tokens = data["tokens"]
            avg = tokens // calls if calls > 0 else 0
            print(f"  {name:<13} | {calls:>7}회 | {tokens:>9,} | {avg:>9,} tok")

    print("=" * 55 + "\n")

if __name__ == "__main__":
    main()
EOF
```

###### ② 대화창에서 스크립트 실행 및 결과 확인

`agy` 대화창에서는 프롬프트 맨 앞에 `!`를 붙여 세션을 나가지 않고 즉시 실행할 수 있습니다.

> 📍 **실행 위치: 🤖 Antigravity 대화창 (agy 프롬프트)**

```text
!python3 scripts/subagent_tokens.py
```

**출력 화면 확인 예시:**
```text
=======================================================
 🤖 서브에이전트별 토큰 사용 통계
=======================================================
 에이전트 명         |    호출 횟수 |    총 소비 토큰 |     호출당 평균
-------------------------------------------------------
  research      |       1회 |    28,450 |    28,450 tok
=======================================================
```

* **학습 포인트**:
  * `research` 에이전트가 단 1회 호출되어 백그라운드에서 **28,450 토큰**을 소비했음을 바로 파악할 수 있습니다.
  * 반면 메인 세션의 `/context`는 **612 토큰**만 사용했으므로, **약 28,000 토큰(97.8%)의 컨텍스트 절감 효과**를 숫자로 명확하게 입증할 수 있습니다.

##### 4. [종합 분석] 메인 에이전트 vs 서브에이전트 토큰 소비 모델 비교 (본 실습 예제 기준)

실습을 통해 측정한 메인 에이전트와 서브에이전트의 단일 세션 내 실제 토큰 소비량을 종합 비교합니다:

> ⚠️ **안내 (실습 예제 기준)**:
> 아래 표에 기재된 토큰 수치(612 tokens, 28,450 tokens 등)는 **본 실습 예제(Python 마이크로서비스 컨테이너 보안 원칙 3가지 조사)를 1회 실행했을 때 실측된 데이터**입니다. 검색 대상 웹사이트의 분량, 호출된 외부 도구 수, 모델 버전에 따라 실제 수치는 달라질 수 있으며, 핵심은 **"수만 토큰의 백그라운드 작업이 메인 컨텍스트에는 2~3% 수준의 극소량만 적재된다"**는 격리 아키텍처 원리입니다.

| 비교 항목 | 메인 에이전트 (Orchestrator) | 서브에이전트 (Worker: `research`) | 아키텍처적 의의 및 해석 |
| :--- | :--- | :--- | :--- |
| **역할 및 세션 수명** | 사용자와의 전체 대화 흐름 총괄 (세션 내내 유지) | 특정 작업 위임 시 분기되어 완료 후 즉시 소멸 | 불필요한 작업 메모리가 영구 잔존하지 않음 |
| **토큰 확인 방법** | 대화창 내 **`/context`** 명령어 | 전용 분석 스크립트 **`scripts/subagent_tokens.py`** | 둘 다 **동일한 현재 단일 세션(Per-Session)** 기준 실측치 |
| **실측 소비 토큰** | **612 tokens** (0.1%) | **28,450 tokens** (1회 호출당) | 서브에이전트 소모 토큰의 약 2.1%만 메인 세션에 보고됨 |
| **세션 토큰 범위** | 현재 대화창의 활성 컨텍스트 윈도우 점유율 | 동일 세션에서 발생한 백그라운드 격리 작업 총합 | 메인과 서브의 메모리 영역이 완벽히 분리됨 |
| **컨텍스트 영향** | 98% 이상의 대용량 컨텍스트 여유 공간 보존 | 방대한 웹 검색 로그 및 크롤링 원문을 세션 종료 시 폐기 | 메인 대화 세션의 기억력 상실(Degradation) 원천 차단 |
| **격리 절감 효과** | **-27,838 tokens (약 97.8% 컨텍스트 절감)** | - | 대규모 프로젝트에서 토큰 비용 폭증을 방지하는 핵심 기법 |

---

## Step 2: 토큰 경제학(Progressive Disclosure) 기반 계층적 Skill 엔지니어링

### 2-1. [비즈니스 문제] AS-IS: 모든 업무 지침을 몰아넣은 거대한 `AGENTS.md`의 폐해

과거(또는 초보적인 프롬프트 구성) 방식에서는 회사의 모든 개발 가이드, 배포 절차, 인프라 점검표를 전부 **`AGENTS.md`** 파일 하나에 길게 몰아서 작성해 두었습니다.

##### ❌ [AS-IS 예시] 모든 절차서가 통째로 들어간 비대한 `AGENTS.md`
```markdown
# 프로젝트 규칙 (AGENTS.md)

## 1. 전역 기본 규칙
- 모든 답변은 한국어로 정중하게 작성한다.
- 보안 키(API_KEY, 비밀번호)는 절대 커밋하지 않는다.

## 2. 서비스 배포 표준 운영 절차서 (매 턴마다 3,500 토큰 강제 소비!)
배포를 수행할 때는 반드시 다음 단계를 순서대로 엄격히 지켜야 한다:
1. 배포 전 인프라 헬스체크 수행:
   - curl -s http://127.0.0.1:8080/health 상태 점검을 수행한다.
   - DB 커넥션 풀 상태 및 응답 지연(Latency)이 정상인지 확인한다.
   - 포트 충돌 여부 및 메모리 사용률을 사전에 체크한다.
2. 배포 전 필수 체크리스트 점검:
   - [보안] 프로덕션 DB 직접 삭제/수정 금지
   - [무결성] 애플리케이션 헬스체크 HTTP 200 반환 확인
   - [격리] staging 환경 검증 완료 전 production 배포 불가
   - [모니터링] Datadog 및 Cloud Monitoring 알림 상태 확인
   - [롤백 대기] 이전 릴리즈 태그 확인 및 롤백 스크립트 준비
3. 환경별 배포 승인 절차:
   - staging 환경: 개발팀 리드의 사전 승인이 있어야 배포 가능
   - production 환경: QA 테스트 통과 증빙 및 보안팀 승인 티켓 필수
... (이하 수백 줄의 배포 매뉴얼 계속)
```

##### 🚨 치명적인 문제점:
`AGENTS.md`는 시스템 프롬프트이므로, **질문 내용과 상관없이 사용자가 대화를 나눌 때마다 무조건 100% 강제로 매 턴마다 API 요청에 포함**됩니다.
1. **토큰 비용 폭증**: 사용자가 *"오늘 날씨 어때?"*, *"파이썬 print 문법 알려줘"* 같은 배포와 전혀 상관없는 질문을 해도 매번 3,500 토큰짜리 배포 매뉴얼이 함께 전송되어 **막대한 API 요금이 낭비**됩니다.
2. **업무 확장 불가**: 배포뿐만 아니라 DB 마이그레이션, 회계 정산 등 회사 매뉴얼을 추가할 때마다 `AGENTS.md`가 20,000~50,000 토큰으로 비대해져 **컨텍스트 한도 초과 및 모델 혼란(Attention 분산)**이 발생합니다.

---

### 2-2. [개선 방향] TO-BE: `AGENTS.md` 다이어트와 `Skill`로의 점진적 분리 (Refactoring)

이를 해결하기 위해 **항상 지켜야 할 최소 규칙**과 **필요할 때만 꺼내 읽는 전문 매뉴얼**을 엄격히 분리(리팩토링)합니다:

##### ✅ 1. 슬림해진 `AGENTS.md` (상시 로딩: 단 150 토큰 유지)
```markdown
# 프로젝트 규칙 (AGENTS.md)
- 모든 답변은 한국어로 정중하게 작성한다.
- 보안 키(API_KEY, 비밀번호)는 절대 커밋하지 않는다.
- Git 커밋 시 Conventional Commits 규격을 엄격히 준수한다.
```

##### ✅ 2. 서랍장 방식의 점진적 공개 (`Skill`: 평소 30 토큰 ➔ 필요할 때만 인출)
수천 줄에 달하는 세부 배포 매뉴얼은 독립된 스킬 디렉터리(`.agents/skills/deploy-pipeline/`)로 떼어냅니다.

```
[평상시 대화] ──▶ AI 주머니에는 "배포 매뉴얼이 있다"는 라벨(30 토큰)만 보관
                   │
                   ▼ (사용자가 "배포 준비해줘"라고 요청할 때만)
[1단계 서랍 오픈] ──▶ SKILL.md 본문(표준 절차서) 로드 (1,000 토큰)
                   │
                   ▼ (실제 점검 작업에 착수할 때만)
[2단계 서랍 오픈] ──▶ references/checklist.md 세부 점검표 로드 (300 토큰)
                   │
                   ▼ (인프라 검증이 필요할 때만)
[3단계 도구 실행] ──▶ scripts/check_health.sh 실행
```

| 접근 방식 | 동작 메커니즘 | 토큰 비용 | 비즈니스 적합성 |
| :--- | :--- | :--- | :--- |
| **AS-IS: 상시 주입 (`AGENTS.md`)** | 질문 내용과 무관하게 **모든 대화 턴마다** 전체 텍스트 주입 | 대화마다 수천~수만 토큰 지속 누적 | 전역 코딩 규칙, 절대 보안 원칙 등 필수 지침 |
| **TO-BE: 점진적 공개 (`Skill`)** | 평소에는 목차(약 30토큰)만 유지, **해당 업무 발생 시에만** 서랍을 열어 본문 로드 | **평상시 토큰 비용 98% 절감** | 서비스 배포 절차, 데이터 마이그레이션 등 전문 실무 절차 |

---

### 2-3. [실습] 3단 서랍장 형태의 배포 스킬 파일 생성

실제 배포 프로세스를 모델링하여, 본문 외에 필요할 때만 꺼내 읽는 **참조 문서(`references/`)**와 **자동화 스크립트(`scripts/`)**로 분리 구성합니다.

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
# 1. 계층적 스킬 디렉터리 생성
mkdir -p ~/antigravity-lab/.agents/skills/deploy-pipeline/scripts
mkdir -p ~/antigravity-lab/.agents/skills/deploy-pipeline/references

# 2. [참조 문서] 필요 시에만 에이전트가 꺼내 읽는 배포 필수 체크리스트
cat > ~/antigravity-lab/.agents/skills/deploy-pipeline/references/checklist.md <<'EOF'
# 서비스 배포 필수 체크리스트
1. [보안] 프로덕션 DB 직접 삭제/수정 금지
2. [무결성] 애플리케이션 헬스체크 HTTP 200 반환 확인
3. [격리] staging 환경 검증 완료 전 production 배포 불가
EOF

# 3. [헬퍼 스크립트] 인프라 정상 여부를 검증하는 헬스체크 자동화 스크립트
cat > ~/antigravity-lab/.agents/skills/deploy-pipeline/scripts/check_health.sh <<'EOF'
#!/usr/bin/env bash
echo "=== 인프라 헬스체크 시뮬레이션 ==="
sleep 1
echo "✅ App Server: OK (HTTP 200)"
echo "✅ DB Connection: OK"
exit 0
EOF
chmod +x ~/antigravity-lab/.agents/skills/deploy-pipeline/scripts/check_health.sh
```

---

### 2-4. [실습] 자연어 인식(Intent Matching) 스킬 매니페스트(`SKILL.md`) 작성

사용자가 복잡한 슬래시 명령어(`/deploy-pipeline`)를 직접 기억해서 치지 않아도, 일상적인 대화("배포할래", "릴리즈")를 듣고 **에이전트가 스스로 스킬을 활성화하도록 유도하는 `description`**을 작성합니다.

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
cat > ~/antigravity-lab/.agents/skills/deploy-pipeline/SKILL.md <<'EOF'
---
name: deploy-pipeline
description: >-
  서비스 배포, 스테이징(staging) 및 프로덕션(production) 릴리즈,
  인프라 헬스체크 및 배포 전 체크리스트 점검 요청 시 반드시 활성화할 것.
  사용자가 '배포', 'deploy', '릴리즈', '점검'을 언급할 때 자율적으로 로드한다.
---

# Deploy Pipeline Standard Operating Procedure

이 문서는 안전한 서비스 릴리즈를 위한 표준 운영 절차(SOP)입니다.

## 배포 실행 절차
1. `references/checklist.md` 파일을 읽어 배포 전 누락된 요구사항을 점검한다.
2. `scripts/check_health.sh` 스크립트를 실행하여 인프라 정상 여부를 사전 확인한다.
3. 대상 환경이 `staging`인 경우 배포를 승인하고, `production`인 경우 반드시 사용자에게 재확인을 요청한다.
EOF
```

---

### 2-5. [실습] 스킬 등록 확인 (`/skills`)

새로 만든 배포 스킬이 Antigravity에 올바르게 인식되었는지 확인합니다.

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
cd ~/antigravity-lab
agy
```

> 📍 **실행 위치: 🤖 Antigravity 대화창 (agy 프롬프트)**

```text
/skills
```

* 목록에 `deploy-pipeline` 항목과 작성한 설명문이 나타나는 것을 확인하고 `Esc`를 눌러 닫습니다.

---

### 2-6. [실습] 자연어 명령을 통한 스킬 자율 로딩 검증

직접 스킬 이름을 지정하지 않고, 비즈니스 실무자처럼 자연스러운 문장으로 질문하여 에이전트가 스스로 필요한 스킬과 문서를 찾아서 꺼내 읽는지 확인합니다.

> 📍 **실행 위치: 🤖 Antigravity 대화창 (agy 프롬프트)**

```text
다음 주 릴리즈 예정인 서비스를 스테이징에 배포하려고 해. 어떤 사전 절차를 밟아야 하는지 표준 체크리스트를 확인해줘.
```

#### 동작 결과 관찰

1. 에이전트 실행 로그에 `Activating skill: deploy-pipeline`이 스스로 판단되어 뜹니다.
2. 에이전트가 `references/checklist.md` 파일을 스스로 열어보고, 체크리스트의 3대 항목(보안, 무결성, 격리)을 바탕으로 답변을 구성합니다.
3. `/context`를 입력해 보면 평소에는 이 긴 매뉴얼이 메모리에 전혀 없다가, **필요한 순간에만 최소한의 토큰으로 인출되어 처리**된 것을 확인할 수 있습니다.

---

## Step 3: 0-토큰 결정론적(Deterministic) 가드레일 (Lifecycle Hook)

### 3-1. [비즈니스 개념] 프롬프트 당부 vs OS 레벨 강제 차단기

기업에서 AI를 도입할 때 최고경영진과 보안팀이 가장 두려워하는 것은 **"AI가 중요한 데이터베이스나 운영 서버를 실수로 삭제하는 대형 보안 사고"**입니다.

* **프롬프트 가드레일의 한계**: AI에게 *"중요한 파일은 지우지 마"*라고 아무리 당부해도, 복잡한 사용자 질문이나 악의적인 우회 질문(탈옥 프롬프트)에 속아 넘어갈 확률이 존재합니다 (확률적 모델의 근본적 한계).
* **Lifecycle Hook (결정론적 가드레일)**: AI의 생각이나 판단에 맡기지 않고, **호스트 운영체제(OS) 문지기가 명령어 실행 직전에 가로채어 위험 패턴(`rm -rf`, `drop table` 등) 탐지 시 즉각 물리적으로 차단(`exit 1`)**하는 절대적인 안전장치입니다.
* **비용 절감 효과**: AI에게 매번 보안 규칙을 읽히지 않으므로 **토큰 비용이 0원(0-Token)**입니다.

```
[Agent의 도구 실행 요청 (run_command)]
               │
               ▼
   ┌───────────────────────┐
   │ PreToolUse Hook 검사  │ ──── (정규식: rm -rf, drop table, secret 유출 등 차단)
   └───────────┬───────────┘
               │
       ┌───────┴───────┐
       │               │
  [위험 탐지]     [안전한 명령]
       │               │
       ▼               ▼
  sys.exit(1)     sys.exit(0)
  (즉각 물리적 강제 차단)  (정상 도구 실행 허용)
```

---

### 3-2. [실습] 파괴적 명령어 사전 차단 스크립트 작성

도구(`run_command`)가 실행되기 직전에 호출되어, 명령어가 안전한지 검사하는 파이썬 가드레일 스크립트를 작성합니다.

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
mkdir -p ~/antigravity-lab/.agents/scripts

cat > ~/antigravity-lab/.agents/scripts/block_destructive.py <<'EOF'
#!/usr/bin/env python3
import sys, json, re

# 기업 시스템에서 원천 차단해야 할 치명적 위험 명령어 패턴
FORBIDDEN_PATTERNS = [
    r"rm\s+-rf\s+[/~]",              # 루트(/) 또는 홈(~) 디렉터리 삭제
    r"drop\s+database",              # 데이터베이스 전체 삭제
    r"drop\s+table",                 # 데이터 테이블 삭제
    r"gcloud\s+projects\s+delete",   # 클라우드 프로젝트 삭제
    r"mkfs",                         # 디스크 포맷
    r"(PRIVATE_KEY|API_KEY)=.*git",  # 시크릿 키 깃 커밋 시도
]

def main():
    try:
        raw_payload = sys.stdin.read()
        if not raw_payload.strip():
            sys.exit(0)
            
        data = json.loads(raw_payload)
        command_line = data.get("tool_input", {}).get("CommandLine", "")
        
        for pattern in FORBIDDEN_PATTERNS:
            if re.search(pattern, command_line, re.IGNORECASE):
                sys.stderr.write(f"\n🚨 [DETERMINISTIC HOOK VIOLATION] 파괴적 명령어가 감지되어 실행이 강제 차단되었습니다!\n")
                sys.stderr.write(f" • 차단된 명령어: {command_line}\n")
                sys.stderr.write(f" • 위반 보안 정책: {pattern}\n\n")
                # 0이 아닌 종료 코드를 반환하면 Antigravity가 도구 실행을 즉시 취소합니다.
                sys.exit(1)
                
    except Exception as e:
        sys.stderr.write(f"Hook Error: {e}\n")
        sys.exit(0)

    # 안전한 정상 명령은 통과 (종료 코드 0)
    sys.exit(0)

if __name__ == "__main__":
    main()
EOF
chmod +x ~/antigravity-lab/.agents/scripts/block_destructive.py
```

---

### 3-3. [실습] 훅 설정 파일(`.agents/hooks.json`) 바인딩

작성한 차단 스크립트를 Antigravity의 `PreToolUse`(도구 사용 직전) 이벤트에 등록합니다.

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
cat > ~/antigravity-lab/.agents/hooks.json <<EOF
{
  "production-security-guard": {
    "PreToolUse": [
      {
        "matcher": "run_command",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /home/$USER/antigravity-lab/.agents/scripts/block_destructive.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
EOF
```

---

### 3-4. [실습] 파괴적 명령 시도 및 강제 차단 실전 검증

에이전트에게 고의로 위험한 파일 삭제 명령을 지시하여, OS 레벨에서 물리적으로 실행이 거부되는지 테스트합니다.

> ⚠️ **주의**: `hooks.json` 변경 사항을 로드하기 위해 `agy` 대화창을 재시작(`Ctrl + C` 후 `agy` 재실행)합니다.

> 📍 **실행 위치: 🤖 Antigravity 대화창 (agy 프롬프트)**

```text
디스크 공간을 확보해야 하니까 터미널에서 rm -rf /tmp/cache_dir 명령을 실행해줘.
```

#### 동작 결과 관찰

1. 에이전트가 도구를 호출하려는 순간, 터미널에 `🚨 [DETERMINISTIC HOOK VIOLATION]` 경고 메시지가 출력되며 명령어 실행이 **즉시 취소**됩니다.
2. 에이전트는 자신의 실수가 아니라 **"시스템 보안 정책에 의해 실행이 거부되었음"**을 명확히 인지하고 사용자에게 안전한 대안을 제시합니다.
3. 이로써 아무리 교묘한 프롬프트 공격이 들어와도 시스템을 완벽하게 보호할 수 있음을 입증합니다.

---

## Step 4: 종합 실습 (Capstone) - Antigravity Plugin 원클릭 패키징

### 4-1. [비즈니스 개념] 원클릭 전사 배포를 위한 Plugin 아키텍처

기업에서 훌륭한 AI 업무 자동화 체계를 구축했더라도, 동료들이나 타 부서에 배포할 때 "스킬 폴더 복사하고, 훅 파일 붙여넣으세요"라고 하면 현업 도입(Adoption)이 실패합니다.

* **스마트폰의 앱(App)과 같은 원리**: 스마트폰에서 앱 하나만 깔면 아이콘, 설정, 내부 기능이 한 번에 설치되듯,
* **Antigravity Plugin(`plugin.json`)**은 앞서 만든 **[표준 배포 스킬 + 파괴 방지 보안 훅]을 하나의 번들(Bundle)**로 묶어 팀원 누구나 원클릭으로 쓸 수 있게 만들어 주는 최종 패키징 기술입니다.

---

### 4-2. [실습] 재사용 가능한 플러그인 번들 구성

앞서 개별적으로 작성했던 자산들을 `my-deploy-plugin` 폴더 하나로 통합 복사하고 플러그인 매니페스트(`plugin.json`)를 작성합니다.

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
# 1. 플러그인 통합 디렉터리 생성
mkdir -p ~/antigravity-lab/my-deploy-plugin/skills/deploy-pipeline
mkdir -p ~/antigravity-lab/my-deploy-plugin/scripts

# 2. 앞서 작성한 자산들을 플러그인 폴더로 통합 복사
cp -r ~/antigravity-lab/.agents/skills/deploy-pipeline/* ~/antigravity-lab/my-deploy-plugin/skills/deploy-pipeline/
cp ~/antigravity-lab/.agents/scripts/block_destructive.py ~/antigravity-lab/my-deploy-plugin/scripts/

# 3. 플러그인 매니페스트 (plugin.json) 작성
cat > ~/antigravity-lab/my-deploy-plugin/plugin.json <<'EOF'
{
  "name": "safe-deploy-guard",
  "version": "1.0.0",
  "displayName": "Safe Continuous Deployment Guard",
  "description": "배포 전 체크리스트 점검 및 파괴적 명령 차단 가드레일을 번들링한 통합 엔지니어링 플러그인",
  "capabilities": {
    "skills": ["skills/deploy-pipeline"],
    "hooks": "hooks.json"
  }
}
EOF

# 4. 플러그인 전용 hooks.json 생성
cat > ~/antigravity-lab/my-deploy-plugin/hooks.json <<EOF
{
  "plugin-guard": {
    "PreToolUse": [
      {
        "matcher": "run_command",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /home/$USER/antigravity-lab/my-deploy-plugin/scripts/block_destructive.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
EOF
```

---

### 4-3. [실습] 배포 대상 샘플 웹 서비스 애플리케이션 준비

실제로 배포하고 헬스체크를 수행할 간단한 파이썬 HTTP 웹 서비스와 배포 스크립트를 만듭니다.

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
mkdir -p ~/antigravity-lab/agy_tokenomics/target_service

# 1. 헬스체크 지원 서비스 앱 (app.py) 작성
cat > ~/antigravity-lab/agy_tokenomics/target_service/app.py <<'EOF'
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "UP", "version": "v1.5.0"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), SimpleHandler)
    server.serve_forever()
EOF

# 2. 안전 배포 셸 스크립트 (deploy.sh) 작성
cat > ~/antigravity-lab/agy_tokenomics/target_service/deploy.sh <<'EOF'
#!/usr/bin/env bash
set -e
echo "🚀 [Deploy] target_service 배포 시작..."
pkill -f "app.py" 2>/dev/null || true
nohup python3 app.py > app.log 2>&1 &
sleep 2
curl -s http://127.0.0.1:8080/health | grep -q "UP"
echo "✅ [Deploy] 배포 및 헬스체크 성공!"
EOF
chmod +x ~/antigravity-lab/agy_tokenomics/target_service/deploy.sh
```

---

### 4-4. [실습] 종합 엔드투엔드(End-to-End) 안전 배포 미션 수행

이제 플러그인이 제공하는 **표준 점검(Skill) + 삭제 방지(Hook)** 2대 자산이 종합적으로 연동되어 실제 서비스를 안전하게 배포하는 시나리오를 수행합니다.

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
cd ~/antigravity-lab
agy
```

> 📍 **실행 위치: 🤖 Antigravity 대화창 (agy 프롬프트)**

```text
deploy-pipeline 스킬의 사전 점검을 거친 뒤 target_service/deploy.sh를 실행해서 서비스를 안전하게 배포해줘. 단, 기존 파일을 rm -rf로 지우려는 시도는 보안 정책상 차단되어야 해.
```

---

### 4-5. [검증] 배포 성공 결과 및 서비스 헬스체크 확인

에이전트가 작업을 마친 후, 실제로 백그라운드에서 서비스가 가동 중인지 터미널에서 직접 호출해 봅니다.

> 📍 **실행 위치: 🖥️ Cloud Shell 터미널 (일반 bash 셸)**

```bash
curl -s http://127.0.0.1:8080/health
```

**기대 출력:**
```json
{"status": "UP", "version": "v1.5.0"}
```

* **종합 성과 확인**:
  1. **표준 절차서 자동 준수**: `deploy-pipeline` 스킬로 체크리스트 점검 완료
  2. **보안 무결성 보장**: `block_destructive.py` 훅으로 파괴적 명령어 사전 차단 완료
  3. **신규 릴리즈 성공**: 신규 버전(`v1.5.0`) 배포 및 헬스체크 정상 통과

---

## 4. 아키텍처 비교 요약표

| 아키텍처 요소 | 토큰 소모 | 실행 주체 | 비즈니스 도입 및 운영 가치 |
| :--- | :--- | :--- | :--- |
| **규칙 (`AGENTS.md`)** | 상시 소모 (High) | 시스템 프롬프트 | 코딩 컨벤션, 시크릿 하드코딩 금지 등 회사 전사 필수 원칙 |
| **스킬 (`SKILL.md`)** | 온디맨드 (Low) | 자연어 인텐트 매칭 | 배포, 데이터 마이그레이션 등 필요 시에만 꺼내 읽어 **토큰 비용 98% 절감** |
| **훅 (`hooks.json`)** | **0 토큰 (None)** | 호스트 OS 프로세스 | AI 탈옥이나 실수에도 `rm -rf`, `drop table`을 100% 물리 차단하는 **사고 방지 가드레일** |
| **서브에이전트 (`/owl`)** | 격리 소모 (Isolated) | 독립 LLM 워커 세션 | 수만 토큰의 방대한 리서치를 수행해도 메인 대화창의 기억을 해치지 않는 **컨텍스트 격리** |
| **플러그인 (`plugin.json`)**| 구조화 번들링 | Antigravity 엔진 | Skill + Hook을 스마트폰 앱처럼 하나로 묶어 **팀 및 전사 부서에 원클릭 배포** |

---

## 5. 다음 단계

중급 심화 아키텍처를 마스터하셨다면, 실제 엔터프라이즈 클라우드 인프라와 결합하는 고급 엔지니어링 과정을 진행하세요:
- **GCP Vertex AI Reasoning Engine 배포 실습**: [agy_advance/build_agent.md](../agy_advance/build_agent.md)
- **Gemini Enterprise 네이티브 에이전트 연계**: [agy_advance/agy_ge.md](../agy_advance/agy_ge.md)
