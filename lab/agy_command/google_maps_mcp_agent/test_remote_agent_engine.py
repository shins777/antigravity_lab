"""Tests inference on a remotely deployed Vertex AI Agent Engine resource."""
import os
import sys
import argparse
import vertexai
from vertexai.preview import reasoning_engines
from dotenv import load_dotenv

load_dotenv()


def parse_args():
    parser = argparse.ArgumentParser(description="Test Remote Google Maps Agent Engine")
    parser.add_argument(
        "--resource",
        required=False,
        default=os.getenv("AGENT_ENGINE_RESOURCE_NAME", ""),
        help="Vertex AI Reasoning Engine Resource Name (e.g. projects/.../locations/.../reasoningEngines/...)",
    )
    parser.add_argument(
        "query",
        nargs="*",
        default=["강남역 인근 추천 일식당 3곳 알려줘"],
        help="Query to test against the remote agent",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if not args.resource:
        print("❌ Please provide a resource name via --resource or AGENT_ENGINE_RESOURCE_NAME env var.", file=sys.stderr)
        sys.exit(1)

    project_id = os.getenv("GCP_PROJECT_ID", "ai-hangsik")
    location = os.getenv("GCP_LOCATION", "us-central1")
    vertexai.init(project=project_id, location=location)

    query_str = " ".join(args.query)
    print(f"📡 Querying Remote Agent Engine: {args.resource}")
    print(f"📝 Prompt: '{query_str}'")
    print("=" * 70)

    try:
        remote_agent = reasoning_engines.ReasoningEngine(args.resource)
        response = remote_agent.query(prompt=query_str)
        print(response)
    except Exception as e:
        print(f"❌ Remote query failed: {e}", file=sys.stderr)
        sys.exit(1)
    print("=" * 70)


if __name__ == "__main__":
    main()
