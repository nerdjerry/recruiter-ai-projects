"""Research agent — orchestrates tools and synthesises answers (no LangChain)."""

from __future__ import annotations

import openai

from app.core.prompts import RESEARCH_SYNTHESIS_PROMPT
from app.models.schemas import Citation, ResearchResponse, ToolResult
from app.services.confidence import ConfidenceService
from app.tools.web_search_tool import BaseTool


class ResearchAgent:
    """Dependency-inverted agent: receives tools + services via constructor."""

    def __init__(
        self,
        tools: list[BaseTool],
        chat_model: str,
        openai_api_key: str,
        confidence_service: ConfidenceService,
    ) -> None:
        self._tools = tools
        self._chat_model = chat_model
        self._client = openai.OpenAI(api_key=openai_api_key)
        self._confidence = confidence_service

    def research(
        self, question: str, document_ids: list[str] | None = None
    ) -> ResearchResponse:
        all_results: list[ToolResult] = []
        trace: list[str] = []

        for tool in self._tools:
            trace.append(f"Querying {tool.name}...")
            results = tool.run(question)
            if document_ids and tool.name == "knowledge_base":
                results = [r for r in results if getattr(r, "doc_id", None) in document_ids]
                trace.append(f"{tool.name} returned {len(results)} result(s) (filtered to doc IDs: {document_ids}).")
            else:
                trace.append(f"{tool.name} returned {len(results)} result(s).")
            all_results.extend(results)

        # Build numbered source block for the prompt
        source_lines: list[str] = []
        for i, r in enumerate(all_results, 1):
            url_part = f" ({r.source_url})" if r.source_url else ""
            source_lines.append(f"[{i}] [{r.source_name}]{url_part}: {r.content}")
        sources_text = "\n".join(source_lines) or "No sources available."

        prompt = RESEARCH_SYNTHESIS_PROMPT.format(
            question=question, sources=sources_text
        )
        trace.append("Synthesising answer with LLM...")

        answer = self._synthesise(prompt)
        trace.append("Computing confidence score...")

        confidence = self._confidence.compute_confidence(answer, all_results)

        citations = [
            Citation(
                source=r.source_name,
                title=r.source_url or r.source_name,
                snippet=r.content[:200],
            )
            for r in all_results
            if r.content and "error" not in r.content.lower()
        ]

        return ResearchResponse(
            answer=answer,
            citations=citations,
            confidence_score=confidence,
            reasoning_trace=trace,
        )

    def _synthesise(self, prompt: str) -> str:
        resp = self._client.chat.completions.create(
            model=self._chat_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return resp.choices[0].message.content or ""
