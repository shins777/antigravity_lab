#!/usr/bin/env bash
# Deploy Google Maps Streamable HTTP MCP Server to GCP Cloud Run
set -euo pipefail

# 1. Load configuration from .env if present
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "${SCRIPT_DIR}/.env" ]; then
    echo "📄 Loading configuration from ${SCRIPT_DIR}/.env ..."
    export $(grep -v '^#' "${SCRIPT_DIR}/.env" | xargs -0) || true
fi

# 2. Set variables
PROJECT_ID="${GCP_PROJECT_ID:-ai-hangsik}"
REGION="${GCP_LOCATION:-us-central1}"
SERVICE_NAME="google-maps-mcp-server"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest"

echo "============================================================"
echo "🚀 Deploying Google Maps MCP Server to Cloud Run"
echo "   - Project:  ${PROJECT_ID}"
echo "   - Region:   ${REGION}"
echo "   - Service:  ${SERVICE_NAME}"
echo "============================================================"

# 3. Check Google Cloud authentication
echo "🔐 Checking gcloud authentication..."
gcloud config set project "${PROJECT_ID}"

# 4. Enable required APIs
echo "⚙️  Enabling Cloud Run & Cloud Build APIs..."
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    containerregistry.googleapis.com

# 5. Build and Deploy using Cloud Build and Cloud Run
echo "📦 Building container image and deploying to Cloud Run..."
cd "${SCRIPT_DIR}"

gcloud run deploy "${SERVICE_NAME}" \
    --source . \
    --platform managed \
    --region "${REGION}" \
    --allow-unauthenticated \
    --port 8080 \
    --set-env-vars "GOOGLE_MAPS_API_KEY=${GOOGLE_MAPS_API_KEY:-}" \
    --quiet

# 6. Retrieve Service URL
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" --platform managed --region "${REGION}" --format 'value(status.url)')

echo ""
echo "============================================================"
echo "🎉 Deployment to Cloud Run Successful!"
echo "   - Service URL: ${SERVICE_URL}"
echo "   - SSE Endpoint: ${SERVICE_URL}/sse"
echo "   - Health Check: ${SERVICE_URL}/health"
echo "============================================================"
echo ""
echo "💡 Update your .env or Agent Engine configuration with:"
echo "   MCP_SERVER_URL=${SERVICE_URL}"
