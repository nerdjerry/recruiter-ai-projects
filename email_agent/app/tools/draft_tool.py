"""Tool: generate a draft reply for a classified email via OpenAI."""

from __future__ import annotations

import json
import logging

from openai import OpenAI

from app.core.config import Settings
from app.core.prompts import DRAFT_REPLY_PROMPT
from app.models.schemas import Classification, DraftReply, EmailMessage

logger = logging.getLogger(__name__)


class DraftTool:
    """SRP: draft-reply generation only."""

    def __init__(self, settings: Settings) -> None:
        self._model = settings.chat_model
        self._client = OpenAI(api_key=settings.openai_api_key)

    def run(
        self, email: EmailMessage, classification: Classification
    ) -> DraftReply:
        prompt = DRAFT_REPLY_PROMPT.format(
            intent=classification.intent,
            urgency=classification.urgency,
            subject=email.subject,
            body=email.body,
        )
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        raw = response.choices[0].message.content or "{}"
        data = json.loads(raw)
        return DraftReply(email_id=email.id, **data)
