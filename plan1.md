1. 교육 구성 개요 및 선수 학습
대상: 소프트웨어 엔지니어, 솔루션 아키텍트, 기술 PM 등 AI 에이전트 워크플로를 고도화하려는 개발자
목표:
Antigravity의 기본 Plan → Act → Verify 루프와 하위 에이전트(Subagent) 위임 모델을 이해한다.
프롬프트 토큰을 절약하는 점진적 공개(Progressive Disclosure) 방식의 Skill을 작성하고 배포할 수 있다.
보안 감사, 린팅, 명령어 차단 등 결정론적 가드레일 역할을 하는 Lifecycle Hook을 구성할 수 있다.
사내/외 외부 데이터와 도구를 연결하는 MCP(Model Context Protocol) 서버를 연동할 수 있다.
2. 모듈별 상세 교육 내용
모듈 1: Agent 기본 사용 및 하위 에이전트 (Subagents)
에이전트는 단순 대화형 LLM이 아니라 파일 읽기/쓰기, 쉘 명령어 실행, 브라우저 조작을 수행하는 "행동 주체(Actor)"입니다.

핵심 개념:
Plan → Act → Verify 루프: 작업 계획 수립(/plan) → 도구 실행 및 diff 생성 → 테스트 및 검증(Walkthrough 생성).
보안 모드: Default (매 도구 호출 확인), Auto / Proceed in Sandbox, Turbo (완전 자율 실행).
Subagent 패턴: 컨텍스트 오염을 막기 위해 리서치, 코드 리뷰, 브라우저 자동화 작업을 별도 컨텍스트로 분리 위임 (invoke_subagent 또는 /owl).
실습 과제:
간단한 버그 수정 요청 시 에이전트가 생성한 Implementation Plan 검토 후 승인하기.
복잡한 이슈 조사 시 리서치용 Subagent를 호출하여 메인 대화창의 토큰을 보존하는 방법 체험.
모듈 2: Skill (재사용 가능한 업무 지침)
규칙(AGENTS.md)은 매 턴마다 프롬프트에 포함되어 토큰을 소모하지만, Skill은 필요할 때만 본문을 로드하는 Progressive Disclosure(점진적 공개) 방식으로 동작합니다.

디렉터리 구조:

.agents/skills/my-custom-skill/
├── SKILL.md       # 메인 지침 (필수)
├── scripts/        # 도우미 스크립트 (선택)
└── references/     # 예시 코드, 스키마 정의 (선택)
SKILL.md 작성 표준:

---
name: my-custom-skill
description: >-
  1~2문장의 명확한 설명. 에이전트가 언제 이 스킬을 활성화해야 하는지
  트리거 조건과 목적을 구체적으로 명시 (1024자 이하 권장).
---

# My Custom Skill

## Workflow
1. 단계별 실행 절차
2. 주의사항 및 금지 패턴
교육 포인트:
description의 품질이 스킬 활성화 정확도를 결정함.
직접 호출(/[skill-name])과 에이전트의 자율적 선택(Intent Matching) 비교.
모듈 3: Hook (결정론적 라이프사이클 가드레일)
Hook은 LLM의 확률적 판단에 의존하지 않고, 도구 실행 전/후 또는 세션 시작/종료 시점에 쉘 스크립트/명령어를 강제 실행하는 결정론적(Deterministic) 제어 장치입니다. (0 토큰 소모)

Hook 주요 이벤트:
PreToolUse: 도구가 실행되기 직전에 가로챔 (파라미터 검증, 위험 명령 차단).
PostToolUse: 도구 실행 완료 직후 실행 (코드 생성 후 자동 linter/formatter 실행).
PreInvocation / PostInvocation: 모델 호출 전/후 컨텍스트 주입 및 검사.
Stop: 에이전트 작업 완료 선언 시 완료 조건 미충족 시 작업 계속 진행 요구.
설정 파일 (.agents/hooks.json) 예시:

{
  "security-and-formatting": {
    "PreToolUse": [
      {
        "matcher": "run_command",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .agents/scripts/block_destructive_commands.py",
            "timeout": 10
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "write_file|edit_file",
        "hooks": [
          {
            "type": "command",
            "command": "git diff --name-only | grep -E '\\.(py|ts)$' | xargs -r npx prettier --write",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
교육 포인트: rm -rf, 프로덕션 DB 접근 등 파괴적 명령어 사전 차단 가드레일 구현 실습.
모듈 4: MCP (Model Context Protocol) 서버 연동
MCP는 에이전트에게 파일 시스템 너머의 외부 시스템(사내 DB, Issue Tracker, 외부 API 등)을 안전하게 도구(Tools) 및 리소스(Resources) 형태로 노출하는 오픈 표준 프로토콜입니다.

설정 파일 (mcp_config.json) 구조:

{
  "mcpServers": {
    "github-issue-tracker": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "custom-internal-api": {
      "url": "https://internal-service.example.com/mcp",
      "authProviderType": "google_credentials"
    }
  }
}
교육 포인트:
Stdio 기반 로컬 실행 방식 vs HTTP/SSE 기반 원격 서비스 연결 방식의 차이.
너무 많은 도구(Tool Bloat)를 한 번에 등록하면 모델의 추론 정확도가 떨어지므로, 필요한 도구만 선별하거나 Skill과 조합하는 최적화 패턴 소개.
모듈 5: 종합 실습 (종합 플러그인 빌드)
Skill, Hook, MCP를 하나로 묶어 팀 단위로 재사용·배포할 수 있는 Plugin 형태로 패키징하는 캡스톤 프로젝트입니다.

플러그인 패키지 구조:

my-team-plugin/
├── plugin.json         # 매니페스트 (name, description, displayName)
├── README.md           # 사용자 가이드
├── mcp_config.json     # 번들된 MCP 설정
├── hooks.json          # 번들된 보안/린트 훅
└── skills/             # 도메인 특화 스킬들
    └── deploy-pipeline/
        └── SKILL.md
실습 시나리오 예시: "안전한 원클릭 배포 에이전트"
MCP: 클라우드 인프라 배포 상태를 조회하는 MCP 연결.
Skill: 서비스 배포 체크리스트 및 롤백 절차가 담긴 deploy-pipeline 스킬 작성.
Hook: 프로덕션 배포 전 테스트 실패 시 명령어 실행을 원천 차단하는 PreToolUse 훅 구현.
Agent 실행: "Staging 환경에 현재 브랜치를 배포하고 모니터링해줘"라는 자연어 명령을 에이전트가 안전하게 완수하는지 검증.