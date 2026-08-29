"""HTTP / SSE Client for communicating with the Google Maps Streamable HTTP MCP Server."""
import os
import sys
import json
import logging
from typing import Dict, Any, List, Optional
import httpx

logger = logging.getLogger("GoogleMapsHTTPClient")


class GoogleMapsHTTPClient:
    """Client that communicates with the Streamable HTTP MCP Server (Local or Cloud Run)."""

    def __init__(self, base_url: Optional[str] = None, timeout: float = 30.0):
        """Initialize HTTP MCP Client.

        Args:
            base_url: Base URL of the MCP Server (e.g., 'http://localhost:8080' or Cloud Run URL).
                      Defaults to env var MCP_SERVER_URL or 'http://localhost:8080'.
            timeout: HTTP request timeout in seconds.
        """
        self.base_url = (base_url or os.getenv("MCP_SERVER_URL", "http://localhost:8080")).rstrip("/")
        self.timeout = timeout
        self._request_id = 0
        self.server_info: Dict[str, Any] = {}
        self.available_tools: List[Dict[str, Any]] = []

    def start(self) -> None:
        """Performs initialize handshake and fetches available tools from the remote server."""
        logger.info("Connecting to Google Maps HTTP MCP Server at: %s", self.base_url)

        # 1. Initialize Handshake via JSON-RPC HTTP POST
        init_payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "adk-agent-http-client", "version": "1.0.0"},
            },
        }

        try:
            resp = self._post_rpc(init_payload)
            self.server_info = resp.get("result", {}).get("serverInfo", {})
            logger.info("Successfully connected to MCP Server: %s", self.server_info)
        except Exception as e:
            logger.error("Failed to initialize connection to %s: %s", self.base_url, e)
            raise RuntimeError(f"Cannot connect to MCP Server at '{self.base_url}': {e}") from e

        # 2. Discover Tools via tools/list
        tools_payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/list",
            "params": {},
        }
        tools_resp = self._post_rpc(tools_payload)
        self.available_tools = tools_resp.get("result", {}).get("tools", [])
        logger.info("Discovered %d MCP tools from %s", len(self.available_tools), self.base_url)

    def list_tools(self) -> List[Dict[str, Any]]:
        """Returns the list of available tools from the MCP server."""
        if not self.available_tools:
            self.start()
        return self.available_tools

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Calls a tool on the remote HTTP MCP server.

        Args:
            name: Tool name (e.g. 'maps_search_places').
            arguments: Tool arguments dictionary.

        Returns:
            Parsed response content dictionary.
        """
        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        }

        response = self._post_rpc(payload)
        if response.get("error"):
            raise RuntimeError(f"MCP Tool execution error ({name}): {response['error']}")

        result = response.get("result", {})
        content_items = result.get("content", [])
        combined_text = ""
        for item in content_items:
            if item.get("type") == "text":
                combined_text += item.get("text", "")

        try:
            return json.loads(combined_text)
        except json.JSONDecodeError:
            return {"raw_output": combined_text}

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def _post_rpc(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        rpc_url = f"{self.base_url}/rpc"
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(rpc_url, json=payload)
            response.raise_for_status()
            return response.json()

    def close(self) -> None:
        """Closes client session."""
        logger.info("HTTP MCP Client closed.")
