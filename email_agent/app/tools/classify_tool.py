"""Tool: classify a single email's intent and urgency via LangChain."""

from __future__ import annotations

import json
import logging

from langchain_openai import ChatOpenAI

from app.core.config import Settings
from app.core.prompts import CLASSIFY_PROMPT
from app.models.schemas import Classification

logger = logging.getLogger(__name__)


class ClassifyTool:
    """SRP: classification only."""

    def __init__(self, settings: Settings) -> None:
        self._llm = ChatOpenAI(
            model=settings.chat_model,
            api_key=settings.openai_api_key,
            temperature=0.0,
        )

    def run(self, email_body: str, email_subject: str) -> Classification:
        prompt = CLASSIFY_PROMPT.format(subject=email_subject, body=email_body)
        response = self._llm.invoke([("human", prompt)])
        raw = response.content or "{}"
        data = json.loads(raw)
        return Classification(**data)
