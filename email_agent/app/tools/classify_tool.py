"""Tool: classify a single email's intent and urgency via OpenAI."""

from __future__ import annotations

import json
import logging

from openai import OpenAI

from app.core.config import Settings
from app.core.prompts import CLASSIFY_PROMPT
from app.models.schemas import Classification

logger = logging.getLogger(__name__)


class ClassifyTool:
    """SRP: classification only."""

    def __init__(self, settings: Settings) -> None:
        self._model = settings.chat_model
        self._client = OpenAI(api_key=settings.openai_api_key)

    def run(self, email_body: str, email_subject: str) -> Classification:
        prompt = CLASSIFY_PROMPT.format(subject=email_subject, body=email_body)
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )
        raw = response.choices[0].message.content or "{}"
        data = json.loads(raw)
        return Classification(**data)
