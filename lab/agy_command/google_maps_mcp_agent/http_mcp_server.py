"""Streamable HTTP MCP Server for Google Maps.

Implements the Model Context Protocol (MCP) Streamable HTTP transport (SSE & POST)
and runs as a Cloud Run compatible FastAPI service on GCP.
"""
import os
import sys
import json
import uuid
import asyncio
import logging
from typing import Dict, Any, Optional, AsyncGenerator

from fastapi import FastAPI, Request, Response, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv

# Allow importing mcp_server service components
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from mcp_server import GoogleMapsService, MCP_TOOLS, handle_json_rpc

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("GoogleMapsHTTPMCPServer")

app = FastAPI(
    title="Google Maps Streamable HTTP MCP Server",
    description="MCP Server providing Google Maps tools over Streamable HTTP (SSE) and JSON-RPC for Cloud Run.",
    version="1.0.0"
)

# Enable CORS for web and cloud clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

maps_service = GoogleMapsService()

# Active SSE client sessions: session_id -> asyncio.Queue
active_sessions: Dict[str, asyncio.Queue] = {}


@app.get("/health")
async def health_check():
    """Cloud Run health check probe."""
    return {
        "status": "healthy",
        "service": "google-maps-mcp-server",
        "maps_api_configured": maps_service.is_configured(),
        "active_sse_sessions": len(active_sessions),
    }


@app.get("/sse")
async def sse_endpoint(request: Request):
    """MCP Streamable HTTP Server-Sent Events (SSE) endpoint.

    Initializes an SSE session and sends the endpoint URL for POST messages.
    """
    session_id = str(uuid.uuid4())
    queue: asyncio.Queue = asyncio.Queue()
    active_sessions[session_id] = queue
    logger.info("New SSE MCP connection established. Session ID: %s", session_id)

    async def event_generator() -> AsyncGenerator[str, None]:
        try:
            # 1. Send endpoint event telling the client where to send POST messages
            post_url = f"/messages?session_id={session_id}"
            yield f"event: endpoint\ndata: {post_url}\n\n"

            # 2. Stream events pushed to this session queue
            while True:
                if await request.is_disconnected():
                    logger.info("Client disconnected from SSE session: %s", session_id)
                    break
                try:
                    # Wait for next message with a timeout to allow keepalive ping
                    message = await asyncio.wait_for(queue.get(), timeout=15.0)
                    yield f"event: message\ndata: {json.dumps(message)}\n\n"
                except asyncio.TimeoutError:
                    # Send keepalive ping comment
                    yield ": keepalive\n\n"
        except asyncio.CancelledError:
            logger.info("SSE stream cancelled for session: %s", session_id)
        finally:
            active_sessions.pop(session_id, None)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )


@app.post("/messages")
async def post_message(request: Request, session_id: Optional[str] = None):
    """Handles incoming JSON-RPC requests for an active SSE session."""
    try:
        body = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")

    logger.info("Received MCP request for session %s: %s", session_id, body.get("method"))
    response = handle_json_rpc(body, maps_service)

    if response is not None:
        if session_id and session_id in active_sessions:
            await active_sessions[session_id].put(response)
        return JSONResponse(content=response, status_code=200)

    return Response(status_code=202)


@app.post("/rpc")
async def rpc_endpoint(request: Request):
    """Direct JSON-RPC 2.0 HTTP POST endpoint for lightweight clients without SSE."""
    try:
        body = await request.json()
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
        )

    response = handle_json_rpc(body, maps_service)
    if response is None:
        return Response(status_code=204)
    return JSONResponse(content=response)


def start_server(host: str = "0.0.0.0", port: Optional[int] = None):
    """Starts the Uvicorn HTTP server."""
    port = port or int(os.getenv("PORT", "8080"))
    logger.info("Starting Streamable HTTP MCP Server on %s:%d", host, port)
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    start_server()
