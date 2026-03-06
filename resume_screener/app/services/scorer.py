from __future__ import annotations

import json

from openai import OpenAI

from app.core.config import Settings
from app.models.schemas import CandidateResult

_SYSTEM_PROMPT = (
    "You are a recruiting assistant. Given a job description, a resume, and a "
    "similarity score, return a JSON object with keys: "
    '"name" (candidate name extracted from resume), '
    '"score" (float 0-1, your adjusted relevance score), '
    '"explanation" (2-3 sentence summary of fit), '
    '"skill_gaps" (list of missing skills). '
    "Return ONLY valid JSON, no markdown."
)


class ScoringService:
    """Calls the LLM to produce an explanation (SRP).

    Receives a pre-computed similarity score — does NOT depend on EmbeddingService
    (Interface Segregation).
    """

    def __init__(self, settings: Settings) -> None:
        self._client = OpenAI(api_key=settings.openai_api_key)
        self._model = settings.chat_model

    def explain_match(
        self,
        jd_text: str,
        resume_text: str,
        similarity_score: float,
    ) -> CandidateResult:
        user_msg = (
            f"Job Description:\n{jd_text}\n\n"
            f"Resume:\n{resume_text}\n\n"
            f"Cosine similarity score: {similarity_score:.4f}"
        )
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.3,
        )
        raw = response.choices[0].message.content or "{}"
        data = json.loads(raw)
        return CandidateResult(**data)
