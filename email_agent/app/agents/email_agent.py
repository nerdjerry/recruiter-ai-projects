"""Email agent — orchestrates fetch → classify → draft pipeline."""

from __future__ import annotations

import logging

from app.models.schemas import ProcessedEmail
from app.services.gmail_client import BaseEmailClient
from app.tools.classify_tool import ClassifyTool
from app.tools.draft_tool import DraftTool

logger = logging.getLogger(__name__)


class EmailAgent:
    """Dependency-injected orchestrator. Knows nothing about OAuth or LLM
    internals — it only calls the tools it was given."""

    def __init__(
        self,
        email_client: BaseEmailClient,
        classify_tool: ClassifyTool,
        draft_tool: DraftTool,
        max_emails: int = 20,
    ) -> None:
        self._client = email_client
        self._classify = classify_tool
        self._draft = draft_tool
        self._max_emails = max_emails
        self._store: dict[str, ProcessedEmail] = {}

    def process_emails(self) -> list[ProcessedEmail]:
        emails = self._client.fetch_unread(self._max_emails)
        results: list[ProcessedEmail] = []
        for email in emails:
            classification = self._classify.run(email.body, email.subject)
            draft = self._draft.run(email, classification)
            processed = ProcessedEmail(
                email=email,
                classification=classification,
                draft_reply=draft,
            )
            self._store[email.id] = processed
            results.append(processed)
        return results

    def approve(self, email_id: str) -> bool:
        if email_id not in self._store:
            return False
        self._store[email_id].status = "approved"
        self._client.send_reply(
            email_id, self._store[email_id].draft_reply.body
        )
        return True

    def reject(self, email_id: str) -> bool:
        if email_id not in self._store:
            return False
        self._store[email_id].status = "rejected"
        return True

    def get_processed(self) -> list[ProcessedEmail]:
        return list(self._store.values())
