"""Confidence scoring heuristic (ISP: only consumes answer + sources)."""

from app.models.schemas import ToolResult


class ConfidenceService:
    """Pure-logic confidence scorer — no LLM calls."""

    def compute_confidence(self, answer: str, sources: list[ToolResult]) -> float:
        if not sources:
            return 0.1

        # Factor 1: number of sources (max contribution 0.4)
        source_score = min(len(sources) / 5.0, 1.0) * 0.4

        # Factor 2: answer length — reasonable length boosts confidence
        word_count = len(answer.split())
        if word_count < 10:
            length_score = 0.05
        elif word_count > 500:
            length_score = 0.25
        else:
            length_score = 0.3

        # Factor 3: source diversity (unique source_names)
        unique_sources = len({s.source_name for s in sources})
        diversity_score = min(unique_sources / 3.0, 1.0) * 0.3

        return round(min(source_score + length_score + diversity_score, 1.0), 2)
