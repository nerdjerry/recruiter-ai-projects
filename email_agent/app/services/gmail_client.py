"""Email client abstraction and implementations."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path

from app.models.schemas import EmailMessage

logger = logging.getLogger(__name__)


class BaseEmailClient(ABC):
    """Interface every email client must implement."""

    @abstractmethod
    def fetch_unread(self, max_count: int = 20) -> list[EmailMessage]:
        ...

    @abstractmethod
    def send_reply(self, email_id: str, reply_body: str) -> bool:
        ...

    @abstractmethod
    def mark_read(self, email_id: str) -> bool:
        ...


class GmailClient(BaseEmailClient):
    """Real Gmail API wrapper (requires OAuth credentials)."""

    def __init__(self, credentials_path: str) -> None:
        self._credentials_path = credentials_path
        if not Path(credentials_path).exists():
            logger.warning(
                "Gmail credentials not found at %s — "
                "GmailClient methods will raise NotImplementedError.",
                credentials_path,
            )

    def fetch_unread(self, max_count: int = 20) -> list[EmailMessage]:
        raise NotImplementedError("Configure Gmail OAuth credentials")

    def send_reply(self, email_id: str, reply_body: str) -> bool:
        raise NotImplementedError("Configure Gmail OAuth credentials")

    def mark_read(self, email_id: str) -> bool:
        raise NotImplementedError("Configure Gmail OAuth credentials")


class MockEmailClient(BaseEmailClient):
    """Returns realistic sample emails for testing and demo."""

    _SAMPLES: list[dict] = [
        {
            "id": "msg-001",
            "sender": "alice.jones@example.com",
            "subject": "Job inquiry — Senior Data Engineer",
            "body": (
                "Hi,\n\nI came across your posting for a Senior Data "
                "Engineer and would love to learn more about the role. "
                "Could you share details on the tech stack and team "
                "structure?\n\nBest,\nAlice"
            ),
        },
        {
            "id": "msg-002",
            "sender": "bob.smith@clientcorp.com",
            "subject": "Urgent: Invoice discrepancy",
            "body": (
                "Hello,\n\nI noticed a billing error on invoice #4821. "
                "The amount charged is $2,400 but our contract states "
                "$1,800. Please resolve this immediately.\n\nRegards,\nBob"
            ),
        },
        {
            "id": "msg-003",
            "sender": "carol.wu@partnerfirm.io",
            "subject": "Meeting request — Q3 planning",
            "body": (
                "Hi team,\n\nCan we schedule a 30-minute call next week "
                "to discuss the Q3 roadmap? I'm available Tuesday or "
                "Thursday afternoon.\n\nThanks,\nCarol"
            ),
        },
        {
            "id": "msg-004",
            "sender": "noreply@promos.example.com",
            "subject": "🎉 Flash sale — 50% off everything!",
            "body": (
                "Don't miss our biggest sale of the year! Use code "
                "SAVE50 at checkout. Offer ends midnight.\n\n"
                "Unsubscribe: https://promos.example.com/unsub"
            ),
        },
    ]

    def fetch_unread(self, max_count: int = 20) -> list[EmailMessage]:
        now = datetime.now(tz=timezone.utc)
        return [
            EmailMessage(received_at=now, **sample)
            for sample in self._SAMPLES[:max_count]
        ]

    def send_reply(self, email_id: str, reply_body: str) -> bool:
        logger.info("MockEmailClient.send_reply(%s) — no-op", email_id)
        return True

    def mark_read(self, email_id: str) -> bool:
        logger.info("MockEmailClient.mark_read(%s) — no-op", email_id)
        return True
