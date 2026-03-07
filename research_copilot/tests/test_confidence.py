"""Tests for the confidence scoring heuristic."""

from app.models.schemas import ToolResult
from app.services.confidence import ConfidenceService

svc = ConfidenceService()


def _make_results(n: int, names: list[str] | None = None) -> list[ToolResult]:
    names = names or ["web_search"]
    return [
        ToolResult(content=f"Source content {i}", source_name=names[i % len(names)])
        for i in range(n)
    ]


def test_no_sources_low_confidence():
    score = svc.compute_confidence("Some answer text here.", [])
    assert score <= 0.15


def test_more_sources_higher_confidence():
    few = svc.compute_confidence("A good answer.", _make_results(1))
    many = svc.compute_confidence("A good answer.", _make_results(5))
    assert many > few


def test_diverse_sources_higher_confidence():
    same = svc.compute_confidence(
        "A good answer.", _make_results(3, ["web_search"])
    )
    diverse = svc.compute_confidence(
        "A good answer.",
        _make_results(3, ["web_search", "wikipedia", "knowledge_base"]),
    )
    assert diverse > same


def test_empty_answer_low_length_score():
    score = svc.compute_confidence("short", _make_results(3))
    full = svc.compute_confidence("A " * 50, _make_results(3))
    assert full >= score


def test_single_source():
    score = svc.compute_confidence("Reasonable answer text.", _make_results(1))
    assert 0.0 <= score <= 1.0


def test_score_bounded():
    score = svc.compute_confidence("x " * 300, _make_results(10, ["a", "b", "c"]))
    assert 0.0 <= score <= 1.0
