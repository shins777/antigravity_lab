"""Deploys the Google Maps MCP Agent onto GCP Vertex AI Agent Engine (Reasoning Engine)."""
import os
import sys
import vertexai
from vertexai.preview import reasoning_engines
from dotenv import load_dotenv

# Allow importing agent
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from agent import GoogleMapsMCPAgent

load_dotenv()


def deploy():
    project_id = os.getenv("GCP_PROJECT_ID", "ai-hangsik")
    location = os.getenv("GCP_LOCATION", "us-central1")
    staging_bucket = os.getenv("GCS_STAGING_BUCKET", f"gs://{project_id}-staging")
    mcp_server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8080")
    model_name = os.getenv("MODEL_NAME", "gemini-1.5-pro-002")

    print("============================================================")
    print("🚀 Deploying Google Maps Agent to Vertex AI Agent Engine")
    print(f"   - GCP Project:    {project_id}")
    print(f"   - Region:         {location}")
    print(f"   - Staging Bucket: {staging_bucket}")
    print(f"   - MCP Server URL: {mcp_server_url}")
    print(f"   - Gemini Model:   {model_name}")
    print("============================================================")

    # 1. Initialize Vertex AI
    vertexai.init(
        project=project_id,
        location=location,
        staging_bucket=staging_bucket,
    )

    # 2. Package and Deploy Agent
    print("\n📦 Packaging and deploying Reasoning Engine resource...")
    try:
        remote_agent = reasoning_engines.ReasoningEngine.create(
            GoogleMapsMCPAgent(
                mcp_server_url=mcp_server_url,
                model_name=model_name,
                project_id=project_id,
                location=location,
            ),
            requirements=[
                "google-cloud-aiplatform>=1.60.0",
                "httpx>=0.27.0",
                "pydantic>=2.0.0",
                "python-dotenv>=1.0.0",
                "requests>=2.31.0",
            ],
            display_name="google-maps-mcp-agent",
            description="ADK Agent connected to Google Maps Streamable HTTP MCP Server on Cloud Run.",
            extra_packages=[current_dir],
        )

        print("\n🎉 Deployment Complete!")
        print(f"   - Resource Name: {remote_agent.resource_name}")
        print(f"\n💡 To test remote inference, run:")
        print(f"   python test_remote_agent_engine.py --resource=\"{remote_agent.resource_name}\"")
        return remote_agent.resource_name
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    deploy()
