"""Tests for ClassifyTool — LangChain calls are mocked."""

from unittest.mock import MagicMock, patch

import pytest

from app.core.config import Settings
from app.tools.classify_tool import ClassifyTool


def _make_settings() -> Settings:
    return Settings(openai_api_key="test-key", chat_model="gpt-4o")


def _mock_langchain_response(json_str: str) -> MagicMock:
    response = MagicMock()
    response.content = json_str
    return response


@pytest.fixture
def classify_tool():
    with patch("app.tools.classify_tool.ChatOpenAI") as mock_cls:
        tool = ClassifyTool(_make_settings())
        tool._llm = mock_cls.return_value
        yield tool


CASES = [
    ("inquiry", "medium", 0.92),
    ("complaint", "high", 0.88),
    ("scheduling", "low", 0.95),
    ("spam", "low", 0.99),
    ("other", "medium", 0.70),
]


@pytest.mark.parametrize("intent,urgency,confidence", CASES)
def test_classify_returns_valid_classification(
    classify_tool, intent, urgency, confidence
):
    json_str = (
        f'{{"intent":"{intent}","urgency":"{urgency}",'
        f'"confidence":{confidence}}}'
    )
    classify_tool._llm.invoke.return_value = _mock_langchain_response(json_str)

    result = classify_tool.run("test body", "test subject")

    assert result.intent == intent
    assert result.urgency == urgency
    assert result.confidence == pytest.approx(confidence)


def test_classify_calls_openai_once(classify_tool):
    classify_tool._llm.invoke.return_value = _mock_langchain_response(
        '{"intent":"inquiry","urgency":"low","confidence":0.9}'
    )
    classify_tool.run("body", "subject")
    classify_tool._llm.invoke.assert_called_once()
