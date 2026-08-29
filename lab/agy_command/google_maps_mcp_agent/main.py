"""CLI entrypoint for Google Maps MCP Agent."""
import os
import sys
import argparse
import json
from dotenv import load_dotenv

# Allow importing directly
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from mcp_client import GoogleMapsMCPClient
from agent import GoogleMapsMCPAgent

load_dotenv()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Google Maps MCP Agent: Search places, geocode addresses, and calculate routes via MCP."
    )
    parser.add_argument(
        "query",
        nargs="*",
        help="Search query or prompt (e.g. 'Find coffee shops near Tokyo Tower'). If omitted, starts interactive mode.",
    )
    parser.add_argument(
        "--test-mcp",
        action="store_true",
        help="Directly test the Google Maps MCP Server connection and tools without LLM.",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("MODEL_NAME", "gemini-1.5-pro-002"),
        help="Gemini model name (default: gemini-1.5-pro-002)",
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


def test_mcp_server():
    """Directly tests the MCP Server tools."""
    print("\n🛠️  [MCP Diagnostic] Testing Google Maps MCP Server...")
    print("=" * 70)
    with GoogleMapsMCPClient() as client:
        print(f"✅ Connected to MCP Server: {client.server_info}")
        tools = client.list_tools()
        print(f"✅ Available Tools ({len(tools)}):")
        for t in tools:
            print(f"   • {t['name']}: {t.get('description')}")

        print("\n🧪 Executing Tool: maps_search_places(query='Google Korea Gangnam')")
        result = client.call_tool("maps_search_places", {"query": "Google Korea Gangnam"})
        print(json.dumps(result, indent=2, ensure_ascii=False))

        print("\n🧪 Executing Tool: maps_geocode(address='Seoul Station')")
        geo_result = client.call_tool("maps_geocode", {"address": "Seoul Station"})
        print(json.dumps(geo_result, indent=2, ensure_ascii=False))
    print("=" * 70)
    print("🎉 MCP Server diagnostic test completed successfully!\n")


def run_agent_query(agent: GoogleMapsMCPAgent, query_str: str) -> None:
    print(f"\n🗺️  [Google Maps Agent] Processing: '{query_str}' ...")
    print("=" * 70)
    try:
        response = agent.query(query_str)
        print(response)
    except Exception as e:
        print(f"\n❌ Error during execution: {e}", file=sys.stderr)
    print("=" * 70)


def main():
    args = parse_args()

    if args.test_mcp:
        test_mcp_server()
        return

    print("🚀 Initializing Google Maps MCP Agent...")
    print(f"   - Model:     {args.model}")
    print(f"   - Project:   {args.project}")
    print(f"   - Region:    {args.location}")
    maps_key = os.getenv("GOOGLE_MAPS_API_KEY", "")
    if maps_key and not maps_key.startswith("YOUR_"):
        print("   - Maps API:  Configured (Live API active)")
    else:
        print("   - Maps API:  Not configured (Will use structured mock data)")
    print()

    agent = GoogleMapsMCPAgent(
        model_name=args.model,
        project_id=args.project,
        location=args.location,
    )

    try:
        agent.set_up()
        print("✅ Agent ready with Google Maps MCP Tools.\n")
    except Exception as e:
        print(f"❌ Initialization failed: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        if args.query:
            query_text = " ".join(args.query)
            run_agent_query(agent, query_text)
        else:
            print("💬 Interactive Mode: Enter your Google Maps queries (type 'exit' or 'quit' to end):")
            while True:
                try:
                    user_input = input("\n[Google Maps Query] > ").strip()
                    if not user_input:
                        continue
                    if user_input.lower() in ["exit", "quit", "q"]:
                        print("👋 Exiting Google Maps Agent.")
                        break
                    run_agent_query(agent, user_input)
                except (KeyboardInterrupt, EOFError):
                    print("\n👋 Exiting session.")
                    break
    finally:
        agent.close()


if __name__ == "__main__":
    main()
