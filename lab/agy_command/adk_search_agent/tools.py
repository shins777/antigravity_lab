"""Search tools and schema definitions for the ADK Web Search Agent."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class SearchResultItem(BaseModel):
    """Structured search result item."""
    title: str = Field(description="Title of the web page or resource")
    url: str = Field(description="URL link to the website")
    snippet: str = Field(description="Summary snippet or excerpt from the webpage")


class SearchResponse(BaseModel):
    """Collection of search result items."""
    query: str = Field(description="The search query executed")
    results: List[SearchResultItem] = Field(default_factory=list, description="List of retrieved search results")


def format_search_citations(search_results: List[SearchResultItem]) -> str:
    """Helper function to format search result items as markdown citations.

    Args:
        search_results: List of SearchResultItem objects.

    Returns:
        Formatted markdown citation string.
    """
    if not search_results:
        return "No external web sources found."

    citations = ["### 🌐 Sources & References\n"]
    for idx, item in enumerate(search_results, start=1):
        citations.append(f"{idx}. [{item.title}]({item.url}) - {item.snippet}")
    return "\n".join(citations)
