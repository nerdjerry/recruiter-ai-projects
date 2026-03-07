"""Tests for EmailAgent — all external calls are mocked."""

from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from app.agents.email_agent import EmailAgent
from app.models.schemas import (
    Classification,
    DraftReply,
    EmailMessage,
    ProcessedEmail,
)
from app.services.gmail_client import MockEmailClient


@pytest.fixture
def mock_classify():
    tool = MagicMock()
    tool.run.return_value = Classification(
        intent="inquiry", urgency="medium", confidence=0.9
    )
    return tool


@pytest.fixture
def mock_draft():
    tool = MagicMock()
    tool.run.side_effect = lambda email, classification: DraftReply(
        email_id=email.id,
        subject=f"Re: {email.subject}",
        body="Thank you for your email.",
        tone="formal",
    )
    return tool


@pytest.fixture
def agent(mock_classify, mock_draft):
    return EmailAgent(
        email_client=MockEmailClient(),
        classify_tool=mock_classify,
        draft_tool=mock_draft,
        max_emails=10,
    )


def test_process_emails_returns_all(agent):
    results = agent.process_emails()
    assert len(results) == 4
    assert all(isinstance(r, ProcessedEmail) for r in results)


def test_process_emails_all_pending(agent):
    results = agent.process_emails()
    assert all(r.status == "pending" for r in results)


def test_approve_sets_status(agent):
    agent.process_emails()
    assert agent.approve("msg-001") is True
    processed = {p.email.id: p for p in agent.get_processed()}
    assert processed["msg-001"].status == "approved"


def test_reject_sets_status(agent):
    agent.process_emails()
    assert agent.reject("msg-002") is True
    processed = {p.email.id: p for p in agent.get_processed()}
    assert processed["msg-002"].status == "rejected"


def test_approve_unknown_id_returns_false(agent):
    assert agent.approve("nonexistent") is False


def test_reject_unknown_id_returns_false(agent):
    assert agent.reject("nonexistent") is False


def test_get_processed_empty_initially(agent):
    assert agent.get_processed() == []


def test_mock_client_implements_base():
    """Liskov: MockEmailClient is a valid BaseEmailClient."""
    from app.services.gmail_client import BaseEmailClient

    client = MockEmailClient()
    assert isinstance(client, BaseEmailClient)
    emails = client.fetch_unread()
    assert len(emails) > 0
    assert all(isinstance(e, EmailMessage) for e in emails)
