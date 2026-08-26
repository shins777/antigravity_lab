---
name: agy_features
title: Antigravity 핵심 기능 확장 및 아키텍처 실습 (Agents, Skills, Rules, MCP, Plugins)
version: 1.0.0
description: Antigravity의 Agent 정의, Skill 바인딩, Rule 가드레일 적용, MCP 서버 연동 및 Plugin 확장 설정 실습 모듈
tags:
  - agents
  - skills
  - rules
  - mcp
  - plugins
  - antigravity
  - lab
---

# Antigravity 핵심 기능 구성 및 확장 실습

## 1. 개요 및 학습 목표

- **Agents & Skills:** 에이전트 페르소나 정의 및 호출 가능한 Skill 모듈을 바인딩합니다.
- **Rules:** 에이전트의 실행 정책, 제약 조건, 보안 가드레일을 설정합니다.
- **MCP (Model Context Protocol):** 외부 컨텍스트 및 도구 서버와의 프로토콜 연동을 구성합니다.
- **Plugins:** 서드파티 확장 플러그인을 로드하여 런타임 기능을 확장합니다.

---

## 2. 사전 준비 사항 (Prerequisites)

- `agy_setting` 및 `agy_command` 실습 완료
- Node.js / npx (MCP 서버 연동 테스트용, Node 18+ 권장)
- Python 3.10+ 활성화 가상환경

---

## 3. 핵심 아키텍처 구성 요소

| 구성 요소  | 역할 및 기능                                                | 설정 파일 위치                 |
| :--------- | :---------------------------------------------------------- | :----------------------------- |
| **Agent**  | LLM 기반 추론 엔진 및 작업 실행 주체 정의                   | `agents/<agent_name>.yaml`     |
| **Skill**  | 에이전트가 실행 가능한 특정 도구 및 Python/API 함수         | `skills/<skill_name>/SKILL.md` |
| **Rule**   | 시스템 레벨 보안 정책, 프롬프트 가드레일, 실행 제약         | `.antigravity/rules.yaml`      |
| **MCP**    | Model Context Protocol 표준 기반 외부 컨텍스트/DB/도구 서버 | `mcp_servers.json`             |
| **Plugin** | 로깅, 모니터링, 서드파티 인증 확장 모듈                     | `plugins/` 또는 `config.yaml`  |

---

## 4. 실습 단계 (Lab Steps)

### Step 1: 기능 실습용 프로젝트 디렉터리 구성

```bash
mkdir -p ~/antigravity-lab/lab/agy_features
cd ~/antigravity-lab/lab/agy_features

# 기능별 하위 디렉터리 생성
mkdir -p agents skills/data_fetcher .antigravity plugins
```
