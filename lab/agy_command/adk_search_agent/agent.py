"""ADK Web Search Agent implementation using Google Cloud Vertex AI and Gemini Grounding."""
import os
from typing import Optional, Dict, Any
import vertexai
from vertexai.generative_models import (
    GenerativeModel,
    Tool,
    ground_with_google_search,
    GenerationConfig,
)


class WebSearchAgent:
    """ADK / Vertex AI Reasoning Engine Agent that dynamically searches the web

    to answer user queries with live citations and direct website links.
    """

    def __init__(
        self,
        model_name: str = "gemini-1.5-pro-002",
        project_id: Optional[str] = None,
        location: str = "us-central1",
    ):
        """Initialize the WebSearchAgent configuration.

        Args:
            model_name: The Gemini model identifier (e.g., 'gemini-1.5-pro-002', 'gemini-2.0-flash').
            project_id: GCP Project ID. Defaults to env var GCP_PROJECT_ID or 'ai-hangsik'.
            location: GCP Region. Defaults to 'us-central1'.
        """
        self.model_name = model_name
        self.project_id = project_id or os.getenv("GCP_PROJECT_ID", "ai-hangsik")
        self.location = location or os.getenv("GCP_LOCATION", "us-central1")
        self.model: Optional[GenerativeModel] = None

    def set_up(self) -> None:
        """Initializes Vertex AI client and configures Gemini model with Google Search Tool."""
        try:
            vertexai.init(project=self.project_id, location=self.location)

            # Native Google Search Grounding Tool
            search_tool = Tool.from_google_search_retrieval(ground_with_google_search)

            system_instruction = [
                "You are an expert AI Web Research Assistant.",
                "Your objective is to find the most accurate, up-to-date websites and web information for any given user query.",
                "Always use the Google Search tool when searching for live facts, documentation, or recent news.",
                "Structure your output in clean GitHub-Flavored Markdown with:",
                "  1. Executive Summary: A concise direct answer to the query.",
                "  2. Detailed Findings: Core explanations, bullet points, code snippets, or key data.",
                "  3. Sources & Links: Direct clickable markdown links to referenced websites.",
            ]

            self.model = GenerativeModel(
                model_name=self.model_name,
                tools=[search_tool],
                system_instruction=system_instruction,
            )
        except Exception as e:
            raise RuntimeError(
                f"[WebSearchAgent.set_up] Failed to initialize Vertex AI for project '{self.project_id}': {e}"
            ) from e

    def query(self, prompt: str) -> str:
        """Executes a web search query and returns synthesized findings with citations.

        Args:
            prompt: The user query, question, or research topic.

        Returns:
            The synthesized markdown response with citations.
        """
        if not self.model:
            raise ValueError(
                "[WebSearchAgent.query] Model not initialized. Please call agent.set_up() before querying."
            )

        if not prompt or not prompt.strip():
            raise ValueError("[WebSearchAgent.query] Query prompt cannot be empty.")

        try:
            generation_config = GenerationConfig(
                temperature=0.3,
                max_output_tokens=4096,
            )
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
            )

            result_text = response.text if response.text else "No response generated."

            # Append grounding search queries and metadata if available
            grounding_metadata = self._extract_grounding_metadata(response)
            if grounding_metadata:
                result_text = f"{result_text}\n\n{grounding_metadata}"

            return result_text
        except Exception as e:
            raise RuntimeError(
                f"[WebSearchAgent.query] Error during search generation for query '{prompt}': {e}"
            ) from e

    def _extract_grounding_metadata(self, response: Any) -> str:
        """Extracts and formats search queries or metadata from Gemini grounding response."""
        try:
            if not hasattr(response, "candidates") or not response.candidates:
                return ""

            candidate = response.candidates[0]
            if not hasattr(candidate, "grounding_metadata") or not candidate.grounding_metadata:
                return ""

            meta = candidate.grounding_metadata
            search_queries = getattr(meta, "web_search_queries", [])
            search_chunks = getattr(meta, "grounding_chunks", [])

            lines = []
            if search_queries:
                lines.append(f"🔍 *Searched Queries:* `{', '.join(search_queries)}`")

            sources = []
            for chunk in search_chunks:
                web = getattr(chunk, "web", None)
                if web and hasattr(web, "uri") and hasattr(web, "title"):
                    sources.append(f"- [{web.title}]({web.uri})")

            if sources:
                lines.append("\n**Web References:**\n" + "\n".join(sources[:5]))

            return "\n".join(lines)
        except Exception:
            return ""
