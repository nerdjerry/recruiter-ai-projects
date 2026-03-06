"""Tool: fetch unread emails from any BaseEmailClient."""

from __future__ import annotations

from app.models.schemas import EmailMessage
from app.services.gmail_client import BaseEmailClient


class GmailFetchTool:
    """Wraps BaseEmailClient.fetch_unread() — SRP: fetch only."""

    def __init__(self, client: BaseEmailClient) -> None:
        self._client = client

    def run(self, max_count: int = 20) -> list[EmailMessage]:
        return self._client.fetch_unread(max_count)
