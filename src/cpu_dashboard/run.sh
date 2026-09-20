#!/usr/bin/env bash
# Launch Desktop CPU Status Dashboard
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

echo "============================================================"
echo "⚡ Starting Desktop CPU Status Dashboard (Streamlit)..."
echo "============================================================"

streamlit run app.py --server.port 8501 --server.headless false
