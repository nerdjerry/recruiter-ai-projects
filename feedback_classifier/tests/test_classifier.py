"""Tests for ClassificationService (mocked — no API key needed)."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from app.core.config import Settings
from app.core.prompts import CLASSIFICATION_PROMPT
from app.services.classifier import ClassificationService


def _make_service(settings: Settings | None = None) -> ClassificationService:
    settings = settings or Settings(openai_api_key="test-key")
    return ClassificationService(settings, CLASSIFICATION_PROMPT)


def _mock_response(payload: dict) -> MagicMock:
    choice = MagicMock()
    choice.message.content = json.dumps(payload)
    resp = MagicMock()
    resp.choices = [choice]
    return resp


VALID_RESULT = {
    "sentiment": "negative",
    "topic": "billing",
    "summary": "Customer upset about charges.",
    "severity": 4,
}


@patch("app.services.classifier.OpenAI")
def test_classify_returns_expected_keys(mock_openai_cls: MagicMock) -> None:
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = _mock_response(VALID_RESULT)
    mock_openai_cls.return_value = mock_client

    svc = _make_service()
    result = svc.classify("I was charged twice!")

    assert set(result.keys()) == {"sentiment", "topic", "summary", "severity"}
    assert result["sentiment"] in {"positive", "neutral", "negative"}
    assert isinstance(result["severity"], int)


@patch("app.services.classifier.OpenAI")
def test_classify_empty_text(mock_openai_cls: MagicMock) -> None:
    payload = {
        "sentiment": "neutral",
        "topic": "unknown",
        "summary": "No feedback provided.",
        "severity": 1,
    }
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = _mock_response(payload)
    mock_openai_cls.return_value = mock_client

    svc = _make_service()
    result = svc.classify("")
    assert result["severity"] == 1


@patch("app.services.classifier.OpenAI")
def test_classify_forwards_model_setting(mock_openai_cls: MagicMock) -> None:
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = _mock_response(VALID_RESULT)
    mock_openai_cls.return_value = mock_client

    settings = Settings(openai_api_key="k", chat_model="gpt-test")
    svc = ClassificationService(settings, CLASSIFICATION_PROMPT)
    svc.classify("test")

    call_kwargs = mock_client.chat.completions.create.call_args.kwargs
    assert call_kwargs["model"] == "gpt-test"
