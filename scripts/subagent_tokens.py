#!/usr/bin/env python3
"""
Antigravity Subagent Token Stats
서브에이전트별 호출 횟수, 총 소비 토큰, 호출당 평균 토큰 분석기
"""
import glob
import json
import os
import sys

def main():
    # 1. 대상 로그 파일 탐색 (CLI 인자 지정 또는 가장 최근 세션 로그)
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

    # 2. 로그 파일 분석
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

    # 3. 결과 출력
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
