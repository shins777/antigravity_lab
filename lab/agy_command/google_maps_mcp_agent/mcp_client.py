"""Client for communicating with the Google Maps MCP Server via JSON-RPC stdio transport."""
import os
import sys
import json
import subprocess
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("GoogleMapsMCPClient")


class GoogleMapsMCPClient:
    """Client that communicates with the Google Maps MCP Server."""

    def __init__(self, server_script_path: Optional[str] = None):
        """Initialize MCP client.

        Args:
            server_script_path: Path to mcp_server.py. Defaults to adjacent mcp_server.py.
        """
        if server_script_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            server_script_path = os.path.join(base_dir, "mcp_server.py")

        self.server_script_path = server_script_path
        self.process: Optional[subprocess.Popen] = None
        self._request_id: int = 0
        self.server_info: Dict[str, Any] = {}
        self.available_tools: List[Dict[str, Any]] = []

    def start(self) -> None:
        """Starts the MCP server subprocess and performs the initialize handshake."""
        if self.process is not None:
            return

        cmd = [sys.executable, self.server_script_path]
        logger.info("Starting Google Maps MCP Server process: %s", " ".join(cmd))

        self.process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=sys.stderr,
            text=True,
            bufsize=1,
        )

        # 1. Initialize Handshake
        init_response = self._send_request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "antigravity-mcp-client", "version": "1.0.0"},
            },
        )
        self.server_info = init_response.get("result", {}).get("serverInfo", {})
        logger.info("Connected to MCP Server: %s", self.server_info)

        # 2. Initialized Notification
        self._send_notification("notifications/initialized", {})

        # 3. Discover Available Tools
        tools_response = self._send_request("tools/list", {})
        self.available_tools = tools_response.get("result", {}).get("tools", [])
        logger.info("Discovered %d MCP tools: %s", len(self.available_tools), [t["name"] for t in self.available_tools])

    def list_tools(self) -> List[Dict[str, Any]]:
        """Returns the list of discovered MCP tools."""
        if not self.available_tools:
            self.start()
        return self.available_tools

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Calls an MCP tool by name with the given arguments.

        Args:
            name: Name of the tool (e.g., 'maps_search_places').
            arguments: Dict of argument key-values.

        Returns:
            Dict containing the parsed result or content.
        """
        if self.process is None:
            self.start()

        response = self._send_request(
            "tools/call",
            {"name": name, "arguments": arguments},
        )

        result = response.get("result", {})
        if response.get("error"):
            raise RuntimeError(f"MCP Tool error ({name}): {response['error']}")

        # Extract text content from MCP result format
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

    def _send_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if not self.process or not self.process.stdin or not self.process.stdout:
            raise RuntimeError("MCP server process is not running.")

        req_id = self._next_id()
        msg = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": method,
            "params": params,
        }

        req_line = json.dumps(msg) + "\n"
        self.process.stdin.write(req_line)
        self.process.stdin.flush()

        res_line = self.process.stdout.readline()
        if not res_line:
            raise RuntimeError("MCP server terminated unexpectedly or closed stdout.")

        return json.loads(res_line)

    def _send_notification(self, method: str, params: Dict[str, Any]) -> None:
        if not self.process or not self.process.stdin:
            return

        msg = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
        }
        self.process.stdin.write(json.dumps(msg) + "\n")
        self.process.stdin.flush()

    def close(self) -> None:
        """Terminates the MCP server process and closes I/O pipes."""
        if self.process is not None:
            try:
                if self.process.stdin:
                    self.process.stdin.close()
                if self.process.stdout:
                    self.process.stdout.close()
                self.process.terminate()
                self.process.wait(timeout=2)
            except Exception:
                self.process.kill()
            finally:
                self.process = None
                logger.info("MCP server process terminated.")

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
