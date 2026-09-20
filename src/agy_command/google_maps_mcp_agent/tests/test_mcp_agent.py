"""Unit and integration tests for Google Maps MCP Agent, Stdio Server, and Streamable HTTP Server."""
import os
import sys
import unittest
from fastapi.testclient import TestClient

# Add parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from mcp_client import GoogleMapsMCPClient
from mcp_server import GoogleMapsService, MCP_TOOLS
from http_mcp_server import app


class TestGoogleMapsMCP(unittest.TestCase):
    """Test suite for Google Maps MCP Server, Client, and HTTP Endpoints."""

    def setUp(self):
        self.client = GoogleMapsMCPClient()
        self.http_test_client = TestClient(app)

    def tearDown(self):
        self.client.close()

    def test_mcp_tool_definitions(self):
        """Verify that all required MCP tools are declared."""
        tool_names = [t["name"] for t in MCP_TOOLS]
        self.assertIn("maps_search_places", tool_names)
        self.assertIn("maps_geocode", tool_names)
        self.assertIn("maps_place_details", tool_names)
        self.assertIn("maps_distance_matrix", tool_names)

    def test_mcp_client_handshake_and_tool_discovery(self):
        """Verify stdio client starts server, performs handshake, and lists tools."""
        self.client.start()
        self.assertEqual(self.client.server_info.get("name"), "google-maps-mcp-server")

        tools = self.client.list_tools()
        self.assertGreaterEqual(len(tools), 4)

    def test_mcp_search_places_tool(self):
        """Verify executing maps_search_places tool via stdio MCP client."""
        result = self.client.call_tool("maps_search_places", {"query": "Gangnam Station"})
        self.assertIn("results", result)
        self.assertGreater(len(result["results"]), 0)
        self.assertIn("maps_url", result["results"][0])

    def test_mcp_geocode_tool(self):
        """Verify executing maps_geocode tool via stdio MCP client."""
        result = self.client.call_tool("maps_geocode", {"address": "Seoul City Hall"})
        self.assertIn("results", result)
        self.assertGreater(len(result["results"]), 0)
        self.assertIn("location", result["results"][0])

    def test_mcp_distance_matrix_tool(self):
        """Verify executing maps_distance_matrix tool via stdio MCP client."""
        result = self.client.call_tool(
            "maps_distance_matrix",
            {"origins": "Seoul Station", "destinations": "Gangnam Station", "mode": "driving"},
        )
        self.assertIn("status", result)
        self.assertTrue("distance" in result or "rows" in result)

    def test_http_health_check_endpoint(self):
        """Verify /health endpoint for Cloud Run."""
        response = self.http_test_client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "healthy")
        self.assertEqual(data.get("service"), "google-maps-mcp-server")

    def test_http_rpc_initialize_and_tools_list(self):
        """Verify HTTP /rpc endpoint handles initialize and tools/list."""
        # Initialize
        init_resp = self.http_test_client.post(
            "/rpc",
            json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        )
        self.assertEqual(init_resp.status_code, 200)
        self.assertEqual(init_resp.json().get("result", {}).get("serverInfo", {}).get("name"), "google-maps-mcp-server")

        # Tools list
        tools_resp = self.http_test_client.post(
            "/rpc",
            json={"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        )
        self.assertEqual(tools_resp.status_code, 200)
        tools = tools_resp.json().get("result", {}).get("tools", [])
        self.assertGreaterEqual(len(tools), 4)

    def test_http_rpc_tool_execution(self):
        """Verify HTTP /rpc endpoint executes tools/call for maps_search_places."""
        call_resp = self.http_test_client.post(
            "/rpc",
            json={
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": "maps_search_places", "arguments": {"query": "Tokyo Tower"}},
            },
        )
        self.assertEqual(call_resp.status_code, 200)
        content = call_resp.json().get("result", {}).get("content", [])
        self.assertGreater(len(content), 0)


if __name__ == "__main__":
    unittest.main()
