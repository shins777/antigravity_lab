---
name: adk-realestate-report-agent
description: Google ADK(Agent Development Kit, Python)로 로컬에서 동작하는 멀티 에이전트 부동산 리포트 생성기를 설계·구현·디버깅하는 방법. 모델은 gemini-3.8-flash, 검색은 ADK 내장 google_search 도구를 사용한다. 사용자가 ADK, adk web, adk run, root_agent, SequentialAgent/ParallelAgent/LoopAgent, google_search 도구, Gemini 에이전트를 언급하거나, 부동산·아파트·단지·시세·실거래가·재건축·입지·임장 리포트를 자동으로 조사·작성하는 에이전트를 만들고 싶어 할 때 반드시 이 스킬을 사용할 것. "리서치 에이전트", "보고서 자동화", "검색해서 리포트 써주는 봇"처럼 ADK를 직접 말하지 않아도 Gemini + 검색 기반 리포트 에이전트라면 이 스킬을 적용한다.
---

# ADK 부동산 리포트 에이전트 (Local, Gemini 3.8 Flash + Google Search)

이 스킬은 "요청 → 조사 계획 → 병렬 검색 → 검증/보완 루프 → 리포트 작성 → 파일 저장"으로 이어지는
중간 복잡도의 ADK 멀티 에이전트를 로컬에서 만드는 표준 절차와 코드 템플릿을 제공한다.
목표는 **숫자마다 기준일과 출처가 붙은, 반박 가능한 부동산 리포트**를 만드는 것이다.

---

## 1. 핵심 설계 원칙 (먼저 읽을 것)

1. **google_search는 전용 에이전트에 격리한다.**
   Gemini의 내장 검색 도구는 다른 function tool과 한 에이전트에 섞으면 `400 INVALID_ARGUMENT
   ("Multiple tools are supported only when they are all search tools")`가 날 수 있다.
   ADK Python 1.16+에는 `bypass_multi_tools_limit=True` 우회가 있지만, 버전 의존적이므로
   기본 설계는 "검색 에이전트는 `tools=[google_search]`만 가진다"로 고정한다.
   검색 결과가 필요한 에이전트는 `output_key`로 state를 넘겨받거나 `AgentTool`로 검색 에이전트를 호출한다.

2. **LLM 라우터(`LlmAgent(sub_agents=[...])`)보다 워크플로 에이전트를 쓴다.**
   리포트 생성은 순서가 정해진 파이프라인이다. `SequentialAgent / ParallelAgent / LoopAgent`로
   흐름을 코드로 고정하면 재현성이 높고, 검색 도구와 function tool이 섞인 sub-agent 전이 버그도 피한다.

3. **에이전트 간 데이터는 session state로 전달한다.**
   각 에이전트는 `output_key="..."`로 결과를 state에 쓰고, 다음 에이전트는 instruction 안에서
   `{key}`(필수) 또는 `{key?}`(없어도 됨)로 읽는다.

4. **ParallelAgent의 하위 에이전트는 서로 다른 state 키에 쓴다.** 같은 키를 쓰면 덮어쓰기 경합이 난다.

5. **출처는 LLM이 쓰게 두지 말고 grounding metadata에서 코드로 수집한다.**
   `after_model_callback`에서 `llm_response.grounding_metadata.grounding_chunks`를 읽어 state에 쌓고,
   최종 파일 저장 시 부록으로 붙인다. LLM이 URL을 지어내는 문제를 원천 차단한다.

6. **Gemini 3.8 Flash 설정 규칙**
   - 모델 ID: `gemini-3.8-flash`
   - `temperature`, `top_p`, `top_k`, `candidate_count`를 설정하지 않는다.
   - 추론량은 `thinking_budget`(정수)이 아니라 `thinking_level`(`LOW` / `MEDIUM` 기본 / `HIGH`)로 제어한다.
     `MINIMAL`은 3.8 Flash에서 검증 오류가 난다.
   - 검색 에이전트는 `MEDIUM`, 계획·검증·작성 에이전트는 `HIGH`를 권장한다(토큰 사용량 증가 감안).

---

## 2. 전체 아키텍처

```
realestate_report_pipeline (SequentialAgent)   ← root_agent, before_agent_callback: 오늘 날짜 주입
├── planner              (LlmAgent, 도구 없음)            → state["research_plan"]
├── research_team        (ParallelAgent)
│   ├── market_searcher      (google_search)          → state["market_findings"]
│   ├── policy_searcher      (google_search)          → state["policy_findings"]
│   ├── supply_searcher      (google_search)          → state["supply_findings"]
│   └── location_searcher    (google_search)          → state["location_findings"]
├── refinement_loop      (LoopAgent, max_iterations=2)
│   ├── critic               (function tool: exit_loop) → state["critique"]
│   └── gap_filler           (google_search)          → state["gap_findings"]
└── report_writer        (LlmAgent, 도구 없음)            → state["final_report"]
                          after_agent_callback: reports/*.md 저장 + 출처 부록
```

- 검색 에이전트 4개는 `after_model_callback=collect_sources`로 `state["sources_<agent_name>"]`에 출처를 쌓는다.
- `critic`이 충분하다고 판단하면 `exit_loop`를 호출해 `escalate=True` → 루프 즉시 종료(gap_filler 건너뜀).

---

## 3. 로컬 환경 준비

```bash
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -U google-adk google-genai python-dotenv
```

프로젝트 구조 (ADK는 **패키지 폴더 안의 `root_agent`** 를 찾는다):

```
project/
├── realestate_agent/
│   ├── __init__.py        # from . import agent
│   ├── agent.py           # root_agent 정의
│   ├── prompts.py         # 긴 instruction 분리
│   └── .env
├── reports/               # 생성된 리포트 저장 위치 (자동 생성)
└── run_local.py           # 프로그램 방식 실행(선택)
```

`realestate_agent/.env` (Google AI Studio 키 사용 시):

```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=YOUR_KEY
REPORT_MODEL=gemini-3.8-flash
```

Vertex AI(Gemini Enterprise Agent Platform)를 쓸 경우:

```
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your-project
GOOGLE_CLOUD_LOCATION=global
```

`realestate_agent/__init__.py`:

```python
from . import agent
```

---

## 4. 코드 템플릿

### 4.1 `prompts.py`

프롬프트는 길어지므로 분리한다. `{key}` 는 ADK가 state 값으로 치환한다. 리터럴 중괄호가 필요하면 쓰지 말 것.

```python
PLANNER = """
당신은 한국 부동산 리서치 총괄이다. 오늘 날짜: {today}

사용자 요청을 분석해 아래 형식의 조사 계획만 출력하라. 검색은 하지 않는다.

## 대상
- 지역/단지명/평형(전용㎡)/용도(매매·전세·월세·재건축 투자 등): 요청에서 명시된 것만. 불명확하면 "미지정"이라 적고 합리적 가정을 [가정]으로 표시.
## 핵심 질문 (3~6개)
## 영역별 검색 키워드 (한국어, 각 3~5개)
- 시세/거래: ...
- 정책/금리/규제: ...
- 공급/개발/정비사업: ...
- 입지(교통·학군·생활인프라): ...
## 조사 기간
- 기본: 최근 12개월 + 최근 3개월 집중
"""

SEARCHER_COMMON = """
오늘 날짜: {today}
조사 계획:
{research_plan}

규칙:
- 반드시 google_search를 여러 번(최소 3회, 다른 키워드) 사용한다.
- 모든 수치에는 [기준일/기간, 출처 기관·매체명]을 붙인다. 출처 없는 수치는 쓰지 않는다.
- 실거래가와 호가(매물가)를 절대 섞지 않는다. 구분 표기: (실거래) / (호가).
- 실거래가는 신고 기한(계약 후 30일) 때문에 최근 1개월 데이터가 불완전함을 감안한다.
- 우선 출처: 국토교통부 실거래가 공개시스템, 한국부동산원(R-ONE), KB부동산, 한국은행, 국토교통부·지자체 보도자료, 주요 언론. 블로그·카페 글은 보조로만.
- 상충되는 수치는 둘 다 기록하고 차이를 명시한다.
- 확인 못 한 것은 "확인 불가"로 남긴다. 추측으로 메우지 않는다.
- 출력: 불릿 요약(최대 25줄) + 각 불릿 끝에 출처 표기.
"""

MARKET = SEARCHER_COMMON + """
담당 영역: 시세·거래 동향.
대상 단지/인근 비교 단지의 최근 실거래(가격, 층, 전용면적, 계약월), 호가 범위, 전세가율, 거래량 추이, 지역 매매가격지수 변동률.
"""

POLICY = SEARCHER_COMMON + """
담당 영역: 정책·금리·규제.
기준금리/주담대 금리 추이, 대출 규제(DSR 등), 규제지역·토지거래허가구역 여부, 세제(취득세·양도세·종부세) 변경, 최근 정부 부동산 대책.
"""

SUPPLY = SEARCHER_COMMON + """
담당 영역: 공급·개발.
대상 지역 향후 2~3년 입주 물량, 분양 일정, 재건축·재개발 진행 단계, 교통·개발 호재의 확정 여부(계획/착공/개통 단계 구분).
"""

LOCATION = SEARCHER_COMMON + """
담당 영역: 입지.
지하철역·도로 접근성(도보 분), 학군(배정 학교, 학원가), 생활 인프라, 주변 혐오·위험 시설, 단지 자체 특성(세대수, 준공연도, 시공사, 주차).
"""

CRITIC = """
당신은 까다로운 부동산 리포트 검수자다. 오늘 날짜: {today}

조사 계획:
{research_plan}

수집 자료:
[시세] {market_findings}
[정책] {policy_findings}
[공급] {supply_findings}
[입지] {location_findings}
[보완] {gap_findings?}

평가 기준:
1. 조사 계획의 핵심 질문에 모두 답할 근거가 있는가
2. 핵심 수치(최근 실거래가, 전세가율, 금리, 입주 물량)에 기준일과 출처가 있는가
3. 6개월 이상 지난 데이터가 "최신"처럼 쓰이지 않았는가
4. 수치 간 모순이 해결되었는가

판단:
- 충분하면 exit_loop 도구를 호출하고 아무것도 출력하지 마라.
- 부족하면 exit_loop를 호출하지 말고, 보완이 필요한 항목을 최대 5개,
  각각 "무엇이 부족한지 + 추천 검색어"로 출력하라.
"""

GAP_FILLER = """
오늘 날짜: {today}
검수자의 보완 요청:
{critique}

이전 보완 결과(있다면 유지하고 추가하라):
{gap_findings?}

google_search로 보완 요청 항목만 조사하라. SEARCHER 규칙과 동일하게 모든 수치에 기준일·출처를 붙인다.
출력: 이전 보완 결과 + 이번에 새로 확인한 내용을 합친 불릿 목록.
"""

WRITER = """
당신은 한국어 부동산 리서치 리포트 작성자다. 오늘 날짜: {today}

조사 계획:
{research_plan}

근거 자료(이 자료에 있는 내용만 사용, 새 수치 창작 금지):
[시세] {market_findings}
[정책] {policy_findings}
[공급] {supply_findings}
[입지] {location_findings}
[보완] {gap_findings?}

아래 구조의 Markdown 리포트를 작성하라.

# <대상> 부동산 리포트 (작성일: {today})
## 1. 핵심 요약 — 결론 3줄 + 핵심 수치 표
## 2. 대상 개요 — 단지/지역 기본 정보
## 3. 시세·거래 동향 — 실거래/호가 구분 표, 전세가율, 거래량
## 4. 정책·금리 환경
## 5. 수급 — 입주 물량, 정비사업, 개발 호재(단계 표기)
## 6. 입지 분석
## 7. 리스크 요인 — 최소 3개, 발생 조건과 영향 방향
## 8. 시나리오 — 강세/기본/약세, 각 시나리오의 전제 조건
## 9. 데이터 한계 — "확인 불가" 항목, 상충 수치
## 10. 고지 — 본 리포트는 공개 자료 기반 분석이며 투자 권유나 법률·세무 자문이 아님

작성 규칙:
- 모든 수치 옆에 (기준일, 출처)를 괄호로 유지한다.
- 1평 = 3.3058㎡. 면적은 전용㎡ 기준, 필요 시 평 환산 병기.
- 금액은 "억 원" 단위, 소수 첫째 자리까지.
- 결론은 근거에서 도출 가능한 만큼만 단정적으로 쓰고, 근거가 약하면 그렇다고 밝힌다.
- URL은 쓰지 마라(출처 부록은 시스템이 자동 첨부한다).
"""
```

### 4.2 `agent.py`

```python
import os
import re
import pathlib
from datetime import date, datetime

from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse
from google.adk.tools import google_search, ToolContext
from google.genai import types

from . import prompts

MODEL = os.getenv("REPORT_MODEL", "gemini-3.8-flash")
REPORT_DIR = pathlib.Path(os.getenv("REPORT_DIR", "reports"))


def gen_cfg(level: str) -> types.GenerateContentConfig:
    # Gemini 3.8 Flash: temperature/top_p/top_k 설정 금지, thinking_level 사용
    return types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level=level)
    )


# ---------- callbacks ----------
def init_state(callback_context: CallbackContext):
    callback_context.state["today"] = date.today().isoformat()
    return None


def collect_sources(callback_context: CallbackContext, llm_response: LlmResponse):
    """google_search grounding 결과에서 출처를 수집해 에이전트별 state 키에 누적."""
    gm = getattr(llm_response, "grounding_metadata", None)
    if not gm or not gm.grounding_chunks:
        return None
    key = f"sources_{callback_context.agent_name}"
    sources = list(callback_context.state.get(key, []))
    for chunk in gm.grounding_chunks:
        web = getattr(chunk, "web", None)
        if web and web.uri:
            item = {"title": web.title or "", "uri": web.uri}
            if item not in sources:
                sources.append(item)
    callback_context.state[key] = sources
    return None  # 응답은 수정하지 않음


def save_report(callback_context: CallbackContext):
    """최종 리포트 + 출처 부록을 reports/ 에 저장."""
    state = callback_context.state.to_dict()
    report = state.get("final_report", "")
    if not report:
        return None

    lines, seen = [], set()
    for k, v in state.items():
        if k.startswith("sources_"):
            for s in v:
                if s["uri"] not in seen:
                    seen.add(s["uri"])
                    lines.append(f"- [{k.removeprefix('sources_')}] {s['title']} — {s['uri']}")
    appendix = "\n\n---\n## 부록: 검색 출처 (자동 수집)\n" + ("\n".join(lines) or "- 없음")

    title = report.splitlines()[0].lstrip("# ").strip() or "report"
    slug = re.sub(r"[^\w가-힣]+", "_", title)[:60]
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIR / f"{slug}_{datetime.now():%Y%m%d_%H%M}.md"
    path.write_text(report + appendix, encoding="utf-8")
    callback_context.state["report_path"] = str(path)
    return None


# ---------- tools ----------
def exit_loop(tool_context: ToolContext) -> dict:
    """수집 자료가 리포트 작성에 충분할 때 호출하여 보완 루프를 종료한다."""
    tool_context.actions.escalate = True
    tool_context.actions.skip_summarization = True
    return {}


# ---------- agents ----------
def make_searcher(name: str, instruction: str, output_key: str) -> LlmAgent:
    return LlmAgent(
        name=name,
        model=MODEL,
        description=f"{output_key} 수집용 검색 에이전트",
        instruction=instruction,
        tools=[google_search],               # 검색 도구 단독
        generate_content_config=gen_cfg("MEDIUM"),
        after_model_callback=collect_sources,
        output_key=output_key,
    )


planner = LlmAgent(
    name="planner",
    model=MODEL,
    instruction=prompts.PLANNER,
    generate_content_config=gen_cfg("HIGH"),
    output_key="research_plan",
)

research_team = ParallelAgent(
    name="research_team",
    sub_agents=[
        make_searcher("market_searcher", prompts.MARKET, "market_findings"),
        make_searcher("policy_searcher", prompts.POLICY, "policy_findings"),
        make_searcher("supply_searcher", prompts.SUPPLY, "supply_findings"),
        make_searcher("location_searcher", prompts.LOCATION, "location_findings"),
    ],
)

critic = LlmAgent(
    name="critic",
    model=MODEL,
    instruction=prompts.CRITIC,
    tools=[exit_loop],                       # function tool 단독 (검색과 분리)
    generate_content_config=gen_cfg("HIGH"),
    output_key="critique",
)

gap_filler = make_searcher("gap_filler", prompts.GAP_FILLER, "gap_findings")

refinement_loop = LoopAgent(
    name="refinement_loop",
    sub_agents=[critic, gap_filler],
    max_iterations=2,                        # 비용 상한. 3 이상은 효용 대비 비쌈
)

report_writer = LlmAgent(
    name="report_writer",
    model=MODEL,
    instruction=prompts.WRITER,
    generate_content_config=gen_cfg("HIGH"),
    output_key="final_report",
    after_agent_callback=save_report,
)

root_agent = SequentialAgent(
    name="realestate_report_pipeline",
    description="부동산 리포트를 조사·검증·작성하는 파이프라인",
    sub_agents=[planner, research_team, refinement_loop, report_writer],
    before_agent_callback=init_state,
)
```

### 4.3 `run_local.py` (CLI/배치 실행용, 선택)

```python
import asyncio, sys
from dotenv import load_dotenv
load_dotenv("realestate_agent/.env")

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from realestate_agent.agent import root_agent

APP = "realestate_report"

async def main(query: str):
    svc = InMemorySessionService()
    runner = Runner(agent=root_agent, app_name=APP, session_service=svc)
    session = await svc.create_session(app_name=APP, user_id="local")
    msg = types.Content(role="user", parts=[types.Part(text=query)])

    async for ev in runner.run_async(user_id="local", session_id=session.id, new_message=msg):
        if ev.is_final_response() and ev.content and ev.content.parts:
            text = ev.content.parts[0].text or ""
            print(f"\n[{ev.author}] {text[:400]}")

    final = await svc.get_session(app_name=APP, user_id="local", session_id=session.id)
    print("\n저장 위치:", final.state.get("report_path"))

if __name__ == "__main__":
    asyncio.run(main(" ".join(sys.argv[1:]) or "서울 강남구 개포동 대단지 아파트 전용 84㎡ 매매 시장 리포트"))
```

---

## 5. 실행과 확인

```bash
# 프로젝트 루트(= realestate_agent 폴더의 부모)에서
adk web            # 브라우저 UI: 이벤트·state·tool call 트레이스 확인 (개발 시 기본)
adk run realestate_agent
python run_local.py "마포구 아현동 재개발 구역 투자 리포트"
```

`adk web`의 Events / State 탭에서 반드시 확인할 것:
- `research_plan`, `*_findings`, `critique`, `final_report`가 순서대로 채워지는지
- 검색 에이전트 이벤트에 grounding metadata가 있고 `sources_*` 키가 쌓이는지
- critic이 `exit_loop`를 호출했는지 또는 `max_iterations`로 끝났는지

---

## 6. 확장 패턴 (필요할 때만)

| 필요 | 방법 |
|---|---|
| 한 에이전트에서 검색 + 계산 도구를 같이 쓰기 | 검색 에이전트를 `AgentTool(agent=search_agent)`로 감싸 `tools=[AgentTool(...), calc_fn]` 로 사용. 또는 ADK ≥1.16 에서 `GoogleSearchTool(bypass_multi_tools_limit=True)` |
| 공공데이터 API(국토부 실거래가 등) 연동 | 별도 function tool 에이전트로 만들고 ParallelAgent에 추가. 결과는 고유 `output_key`에 저장. API 키는 `.env` |
| 대화형 후속 질문(리포트 생성 후 Q&A) | 바깥에 `LlmAgent`를 두고 `AgentTool(agent=root_agent)`로 파이프라인을 호출하게 한다. 파이프라인을 sub_agents 라우팅으로 연결하지 말 것 |
| 여러 단지 비교 리포트 | planner가 단지 목록을 만들고, 단지별 searcher를 동적 생성하기보다 한 searcher에 "비교 표 형식" 지시를 주는 편이 안정적 |
| 비용 절감 | searcher를 `LOW`, writer만 `HIGH`. 또는 `refinement_loop` 제거 |
| 세션 영속화 | `InMemorySessionService` → `DatabaseSessionService(db_url="sqlite:///sessions.db")` |

---

## 7. 문제 해결

| 증상 | 원인 / 조치 |
|---|---|
| `Multiple tools are supported only when they are all search tools` | google_search와 다른 도구가 한 에이전트에 있음, 또는 LLM 라우터가 sub_agents 전이 도구를 추가함. 검색 에이전트 격리 / 워크플로 에이전트로 전환 |
| `KeyError` 또는 instruction에 `{market_findings}` 가 그대로 남음 | 앞선 에이전트가 해당 키를 아직 안 씀. 순서 확인, 선택 값은 `{key?}` 사용 |
| `thinking_level` 검증 오류 | `MINIMAL` 사용 금지. SDK가 구버전이면 `pip install -U google-genai google-adk`. 그래도 안 되면 SDK의 `types.ThinkingLevel` enum 값 확인 |
| 출처 부록이 비어 있음 | 모델이 검색을 안 함 → instruction의 "최소 3회 검색" 강제 확인. grounding URI는 리다이렉트 URL 형태일 수 있음(정상) |
| 리포트에 근거 없는 수치 | writer instruction의 "근거 자료에 있는 내용만" 규칙 강화, critic 기준에 "출처 없는 수치 목록화" 추가 |
| 루프가 항상 2회 다 돔 | critic 기준이 너무 엄격. 핵심 수치 4종만 필수로 완화 |
| `adk web`에서 에이전트가 안 보임 | `__init__.py`의 `from . import agent` 누락, 또는 패키지 폴더 안에서 실행함(부모 폴더에서 실행해야 함) |

---

## 8. 구현 시 체크리스트

- [ ] 모델 ID `gemini-3.8-flash`, temperature/top_p/top_k 미설정
- [ ] google_search를 가진 에이전트는 그 도구 하나만 가짐
- [ ] 모든 LlmAgent에 고유 `output_key`, ParallelAgent 하위 키 중복 없음
- [ ] `today`를 state에 주입해 검색·작성이 날짜를 인식
- [ ] 출처는 callback으로 수집, LLM이 URL을 쓰지 않음
- [ ] LoopAgent `max_iterations` 상한 설정
- [ ] 리포트에 기준일·출처·데이터 한계·고지 섹션 포함
- [ ] `adk web`으로 state 흐름을 한 번 눈으로 검증한 뒤 `run_local.py`로 배치 실행
