"""Wikipedia tool using the REST API (SRP: Wikipedia only)."""

import urllib.parse

import requests as http_requests

from app.tools.web_search_tool import BaseTool
from app.models.schemas import ToolResult

_WIKI_API = "https://en.wikipedia.org/api/rest_v1/page/summary"


class WikipediaTool(BaseTool):
    """Fetches Wikipedia article summaries via the REST API."""

    @property
    def name(self) -> str:
        return "wikipedia"

    def run(self, query: str) -> list[ToolResult]:
        try:
            title = urllib.parse.quote(query.replace(" ", "_"))
            resp = http_requests.get(
                f"{_WIKI_API}/{title}",
                headers={"User-Agent": "ResearchCopilot/1.0"},
                timeout=10,
            )
            if resp.status_code == 200:
                data = resp.json()
                return [
                    ToolResult(
                        content=data.get("extract", ""),
                        source_name=self.name,
                        source_url=data.get("content_urls", {})
                        .get("desktop", {})
                        .get("page"),
                    )
                ]
            return [
                ToolResult(
                    content=f"No Wikipedia article found for '{query}'.",
                    source_name=self.name,
                )
            ]
        except Exception as exc:
            return [
                ToolResult(content=f"Wikipedia error: {exc}", source_name=self.name)
            ]
