"""CLI entrypoint for running and testing the ADK Web Search Agent."""
import os
import sys
import argparse
from dotenv import load_dotenv

# Allow importing directly when run as script
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from agent import WebSearchAgent


def parse_args():
    parser = argparse.ArgumentParser(
        description="ADK Web Search Agent: Search websites and live information using Gemini & Vertex AI."
    )
    parser.add_argument(
        "query",
        nargs="*",
        help="Search query or topic. If omitted, enters interactive prompt mode.",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("MODEL_NAME", "gemini-1.5-pro-002"),
        help="Gemini Model Name (default: gemini-1.5-pro-002)",
    )
    parser.add_argument(
        "--project",
        default=os.getenv("GCP_PROJECT_ID", "ai-hangsik"),
        help="GCP Project ID (default: ai-hangsik or env GCP_PROJECT_ID)",
    )
    parser.add_argument(
        "--location",
        default=os.getenv("GCP_LOCATION", "us-central1"),
        help="GCP Region (default: us-central1)",
    )
    return parser.parse_args()


def run_agent(agent: WebSearchAgent, query_str: str) -> None:
    print(f"\n🔎 [Web Search Agent] Searching web for: '{query_str}' ...")
    print("=" * 70)
    try:
        response = agent.query(query_str)
        print(response)
    except Exception as e:
        print(f"\n❌ Error during search: {e}", file=sys.stderr)
    print("=" * 70)


def main():
    load_dotenv()
    args = parse_args()

    print("🚀 Initializing ADK Web Search Agent...")
    print(f"   - Model:    {args.model}")
    print(f"   - Project:  {args.project}")
    print(f"   - Location: {args.location}\n")

    try:
        agent = WebSearchAgent(
            model_name=args.model,
            project_id=args.project,
            location=args.location,
        )
        agent.set_up()
        print("✅ Agent successfully initialized with Google Search Grounding.\n")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}", file=sys.stderr)
        sys.exit(1)

    if args.query:
        query_text = " ".join(args.query)
        run_agent(agent, query_text)
    else:
        print("💬 Interactive Mode: Enter your search queries (type 'exit' or 'quit' to end):")
        while True:
            try:
                user_input = input("\n[Search Query] > ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ["exit", "quit", "q"]:
                    print("👋 Exiting ADK Web Search Agent.")
                    break
                run_agent(agent, user_input)
            except (KeyboardInterrupt, EOFError):
                print("\n👋 Exiting session.")
                break


if __name__ == "__main__":
    main()
