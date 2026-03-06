"""Tests for the research agent (all external calls mocked)."""

from unittest.mock import MagicMock, patch

from app.agents.research_agent import ResearchAgent
from app.models.schemas import ToolResult
from app.services.confidence import ConfidenceService
from app.tools.web_search_tool import BaseTool


class _FakeTool(BaseTool):
    """Concrete tool for testing."""

    def __init__(self, tool_name: str, results: list[ToolResult]) -> None:
        self._name = tool_name
        self._results = results

    @property
    def name(self) -> str:
        return self._name

    def run(self, query: str) -> list[ToolResult]:
        return self._results


def _build_agent(tools: list[BaseTool] | None = None) -> ResearchAgent:
    tools = tools or [
        _FakeTool("web", [ToolResult(content="Web info", source_name="web")]),
        _FakeTool("wiki", [ToolResult(content="Wiki info", source_name="wiki")]),
    ]
    return ResearchAgent(
        tools=tools,
        chat_model="gpt-4o",
        openai_api_key="test-key",
        confidence_service=ConfidenceService(),
    )


@patch("app.agents.research_agent.openai.OpenAI")
def test_agent_calls_all_tools(mock_openai_cls):
    mock_client = MagicMock()
    mock_openai_cls.return_value = mock_client
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Synthesised answer."))]
    )
    tool_a = _FakeTool("a", [ToolResult(content="A result", source_name="a")])
    tool_b = _FakeTool("b", [ToolResult(content="B result", source_name="b")])

    agent = _build_agent([tool_a, tool_b])
    resp = agent.research("test question")

    assert len(resp.citations) == 2
    assert any("a" in c.source for c in resp.citations)
    assert any("b" in c.source for c in resp.citations)


@patch("app.agents.research_agent.openai.OpenAI")
def test_reasoning_trace_captured(mock_openai_cls):
    mock_client = MagicMock()
    mock_openai_cls.return_value = mock_client
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Answer."))]
    )

    agent = _build_agent()
    resp = agent.research("What is AI?")

    assert any("Querying" in s for s in resp.reasoning_trace)
    assert any("Synthesising" in s for s in resp.reasoning_trace)


@patch("app.agents.research_agent.openai.OpenAI")
def test_confidence_is_computed(mock_openai_cls):
    mock_client = MagicMock()
    mock_openai_cls.return_value = mock_client
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Detailed answer."))]
    )

    agent = _build_agent()
    resp = agent.research("Explain gravity")

    assert 0.0 <= resp.confidence_score <= 1.0


@patch("app.agents.research_agent.openai.OpenAI")
def test_agent_handles_no_results(mock_openai_cls):
    mock_client = MagicMock()
    mock_openai_cls.return_value = mock_client
    mock_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="No data available."))]
    )

    agent = _build_agent([_FakeTool("empty", [])])
    resp = agent.research("Unknown topic")

    assert resp.answer == "No data available."
    assert resp.confidence_score <= 0.15
