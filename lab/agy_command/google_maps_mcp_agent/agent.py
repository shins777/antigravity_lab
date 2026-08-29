"""Google Maps Agent for ADK and GCP Vertex AI Agent Engine.

Connects to Google Maps Streamable HTTP MCP Server (on Cloud Run or local)
and executes function calling reasoning loops with Gemini models.
"""
import os
import sys
import json
import logging
from typing import Optional, Dict, Any, List, Union

import vertexai
from vertexai.generative_models import (
    GenerativeModel,
    Tool,
    FunctionDeclaration,
    Part,
    GenerationConfig,
)
from dotenv import load_dotenv

# Allow relative and package imports
try:
    from .http_mcp_client import GoogleMapsHTTPClient
    from .mcp_client import GoogleMapsMCPClient
except ImportError:
    from http_mcp_client import GoogleMapsHTTPClient
    from mcp_client import GoogleMapsMCPClient

load_dotenv()
logger = logging.getLogger("GoogleMapsMCPAgent")


class GoogleMapsMCPAgent:
    """ADK / Vertex AI Reasoning Engine Agent connecting to Google Maps MCP Server."""

    def __init__(
        self,
        mcp_server_url: Optional[str] = None,
        model_name: str = "gemini-1.5-pro-002",
        project_id: Optional[str] = None,
        location: str = "us-central1",
        use_stdio: bool = False,
    ):
        """Initialize GoogleMapsMCPAgent.

        Args:
            mcp_server_url: Cloud Run or local HTTP URL of the MCP Server (e.g. 'https://...a.run.app').
            model_name: Gemini model name.
            project_id: GCP Project ID. Defaults to env var or 'ai-hangsik'.
            location: GCP Region. Defaults to 'us-central1'.
            use_stdio: If True, uses local stdio subprocess instead of HTTP.
        """
        self.mcp_server_url = mcp_server_url or os.getenv("MCP_SERVER_URL", "http://localhost:8080")
        self.model_name = model_name
        self.project_id = project_id or os.getenv("GCP_PROJECT_ID", "ai-hangsik")
        self.location = location or os.getenv("GCP_LOCATION", "us-central1")
        self.use_stdio = use_stdio
        self.model: Optional[GenerativeModel] = None
        self.client: Optional[Union[GoogleMapsHTTPClient, GoogleMapsMCPClient]] = None

    def set_up(self) -> None:
        """Initializes Vertex AI client, connects to MCP Server (HTTP or Stdio), and configures Gemini."""
        try:
            logger.info("Initializing Vertex AI (Project: %s, Region: %s)...", self.project_id, self.location)
            vertexai.init(project=self.project_id, location=self.location)

            # Initialize appropriate MCP Client
            if self.use_stdio:
                logger.info("Using Stdio MCP Client...")
                self.client = GoogleMapsMCPClient()
            else:
                logger.info("Using Streamable HTTP MCP Client connecting to %s...", self.mcp_server_url)
                self.client = GoogleMapsHTTPClient(base_url=self.mcp_server_url)

            self.client.start()
            mcp_tools = self.client.list_tools()

            # Convert MCP Tool schemas to Vertex AI FunctionDeclarations
            function_declarations = []
            for tool in mcp_tools:
                fn_decl = FunctionDeclaration(
                    name=tool["name"],
                    description=tool.get("description", ""),
                    parameters=tool.get("inputSchema", {}),
                )
                function_declarations.append(fn_decl)

            gemini_tool = Tool(function_declarations=function_declarations)

            system_instruction = [
                "You are an expert Google Maps AI Assistant powered by the Model Context Protocol (MCP).",
                "You have access to Google Maps tools: maps_search_places, maps_geocode, maps_place_details, and maps_distance_matrix.",
                "Always call appropriate tools when the user asks for places, directions, addresses, ratings, or distances.",
                "Format your final response in clean GitHub Flavored Markdown with:",
                "  1. Summary & Overview: Direct, clear answer to the user's question.",
                "  2. Place / Location Details: Names, formatted addresses, ratings, user reviews count, and status.",
                "  3. Direct Google Maps Links: Clickable markdown links [Open in Google Maps](https://www.google.com/maps/search/...).",
                "  4. Distances & Directions (if applicable): Distance in km/miles and travel duration.",
            ]

            self.model = GenerativeModel(
                model_name=self.model_name,
                tools=[gemini_tool],
                system_instruction=system_instruction,
            )
            logger.info("Agent setup complete with %d MCP tools.", len(function_declarations))
        except Exception as e:
            logger.error("Failed to set up GoogleMapsMCPAgent: %s", e)
            raise RuntimeError(f"[GoogleMapsMCPAgent.set_up] Setup failed: {e}") from e

    def query(self, prompt: str) -> str:
        """Executes a user query using Gemini with tool calling via MCP."""
        if not self.model or not self.client:
            raise ValueError("[GoogleMapsMCPAgent.query] Agent not initialized. Call agent.set_up() first.")

        if not prompt or not prompt.strip():
            raise ValueError("[GoogleMapsMCPAgent.query] Prompt cannot be empty.")

        try:
            chat = self.model.start_chat()
            generation_config = GenerationConfig(temperature=0.2, max_output_tokens=4096)

            response = chat.send_message(prompt, generation_config=generation_config)

            # Function Calling Loop
            max_turns = 8
            turn = 0

            while turn < max_turns:
                turn += 1
                function_calls = []
                for candidate in response.candidates:
                    for part in candidate.content.parts:
                        if part.function_call:
                            function_calls.append(part.function_call)

                if not function_calls:
                    return response.text

                response_parts = []
                for fn in function_calls:
                    fn_name = fn.name
                    fn_args = dict(fn.args)
                    logger.info("Invoking MCP tool via %s: %s with args %s", type(self.client).__name__, fn_name, fn_args)

                    try:
                        tool_result = self.client.call_tool(fn_name, fn_args)
                    except Exception as err:
                        logger.error("Error executing MCP tool '%s': %s", fn_name, err)
                        tool_result = {"error": str(err)}

                    response_parts.append(
                        Part.from_function_response(
                            name=fn_name,
                            response={"content": tool_result},
                        )
                    )

                response = chat.send_message(response_parts, generation_config=generation_config)

            return response.text
        except Exception as e:
            logger.error("Error during agent query execution: %s", e)
            raise RuntimeError(f"[GoogleMapsMCPAgent.query] Query failed: {e}") from e

    def close(self) -> None:
        """Closes client connection."""
        if self.client:
            self.client.close()
            self.client = None

    def __enter__(self):
        self.set_up()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
