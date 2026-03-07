from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from app.core.config import Settings
from app.models.schemas import CandidateResult, ScreeningResponse
from app.services.scorer import ScoringService


class TestCandidateResultSchema:
    def test_valid_candidate(self) -> None:
        c = CandidateResult(name="Alice", score=0.85, explanation="Good fit", skill_gaps=["AWS"])
        assert c.name == "Alice"
        assert c.score == 0.85

    def test_score_out_of_range(self) -> None:
        with pytest.raises(ValidationError):
            CandidateResult(name="Bob", score=1.5, explanation="Bad", skill_gaps=[])

    def test_default_skill_gaps(self) -> None:
        c = CandidateResult(name="Eve", score=0.5, explanation="Average")
        assert c.skill_gaps == []


class TestScreeningResponse:
    def test_create_response(self) -> None:
        candidate = CandidateResult(name="Alice", score=0.9, explanation="Great", skill_gaps=[])
        resp = ScreeningResponse(job_description="Python dev", candidates=[candidate])
        assert len(resp.candidates) == 1
        assert resp.job_description == "Python dev"


class TestScoringService:
    @patch("app.services.scorer.ChatOpenAI")
    def test_explain_match_returns_candidate(self, mock_chat_cls: MagicMock) -> None:
        mock_llm = MagicMock()
        mock_chat_cls.return_value = mock_llm
        mock_llm.invoke.return_value = MagicMock(
            content=json.dumps(
                {
                    "name": "Alice",
                    "score": 0.88,
                    "explanation": "Strong match for Python role.",
                    "skill_gaps": ["Kubernetes"],
                }
            )
        )

        settings = Settings(openai_api_key="test-key", chat_model="gpt-4o-mini")
        service = ScoringService(settings)
        result = service.explain_match("Need Python dev", "Alice resume text", 0.85)

        assert isinstance(result, CandidateResult)
        assert result.name == "Alice"
        assert result.score == 0.88
        assert "Kubernetes" in result.skill_gaps
