"""Retriever tool wrapping the vector store service (SRP: retrieval only)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.tools.web_search_tool import BaseTool
from app.models.schemas import ToolResult

if TYPE_CHECKING:
    from app.services.vectorstore import VectorStoreService


class RetrieverTool(BaseTool):
    """Searches the private knowledge base via vector similarity."""

    def __init__(self, vectorstore: VectorStoreService) -> None:
        self._vectorstore = vectorstore

    @property
    def name(self) -> str:
        return "knowledge_base"

    def run(self, query: str) -> list[ToolResult]:
        try:
            results = self._vectorstore.search(query, top_k=3)
            if not results:
                return [
                    ToolResult(
                        content="No relevant documents found in knowledge base.",
                        source_name=self.name,
                    )
                ]
            return results
        except Exception as exc:
            return [
                ToolResult(content=f"Retriever error: {exc}", source_name=self.name)
            ]
