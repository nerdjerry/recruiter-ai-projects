"""Base tool and web search tool wrapping the Tavily API."""

from abc import ABC, abstractmethod

import requests as http_requests

from app.models.schemas import ToolResult


class BaseTool(ABC):
    """Abstract base class all research tools must implement."""

    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def run(self, query: str) -> list[ToolResult]: ...


class WebSearchTool(BaseTool):
    """Wraps the Tavily search API (SRP: web search only)."""

    def __init__(self, api_key: str = "") -> None:
        self._api_key = api_key

    @property
    def name(self) -> str:
        return "web_search"

    def run(self, query: str) -> list[ToolResult]:
        if not self._api_key:
            return [
                ToolResult(
                    content="Tavily API key not configured. Skipping web search.",
                    source_name=self.name,
                )
            ]
        try:
            resp = http_requests.post(
                "https://api.tavily.com/search",
                json={"api_key": self._api_key, "query": query, "max_results": 5},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            return [
                ToolResult(
                    content=r.get("content", ""),
                    source_name=self.name,
                    source_url=r.get("url"),
                )
                for r in data.get("results", [])
            ] or [ToolResult(content="No web results found.", source_name=self.name)]
        except Exception as exc:
            return [ToolResult(content=f"Web search error: {exc}", source_name=self.name)]
