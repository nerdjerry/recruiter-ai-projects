"""Tool: generate a draft reply for a classified email via LangChain."""

from __future__ import annotations

import json
import logging

from langchain_openai import ChatOpenAI

from app.core.config import Settings
from app.core.prompts import DRAFT_REPLY_PROMPT
from app.models.schemas import Classification, DraftReply, EmailMessage

logger = logging.getLogger(__name__)


class DraftTool:
    """SRP: draft-reply generation only."""

    def __init__(self, settings: Settings) -> None:
        self._llm = ChatOpenAI(
            model=settings.chat_model,
            api_key=settings.openai_api_key,
            temperature=0.7,
        )

    def run(
        self, email: EmailMessage, classification: Classification
    ) -> DraftReply:
        prompt = DRAFT_REPLY_PROMPT.format(
            intent=classification.intent,
            urgency=classification.urgency,
            subject=email.subject,
            body=email.body,
        )
        response = self._llm.invoke([("human", prompt)])
        raw = response.content or "{}"
        data = json.loads(raw)
        return DraftReply(email_id=email.id, **data)
