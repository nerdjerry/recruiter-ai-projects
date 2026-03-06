"""Tests for PriorityService — no external dependencies."""

from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from app.services.prioritizer import PriorityService


@pytest.fixture
def svc() -> PriorityService:
    return PriorityService()


def test_higher_severity_means_higher_priority(svc: PriorityService) -> None:
    now = datetime.utcnow()
    low = svc.compute_priority(1, now)
    high = svc.compute_priority(5, now)
    assert high > low


def test_recent_items_score_higher(svc: PriorityService) -> None:
    recent = datetime.utcnow()
    old = datetime.utcnow() - timedelta(days=30)
    assert svc.compute_priority(3, recent) > svc.compute_priority(3, old)


def test_boundary_severity_1_today(svc: PriorityService) -> None:
    score = svc.compute_priority(1, datetime.utcnow())
    assert 0.9 <= score <= 1.1  # ~1.0


def test_boundary_severity_5_today(svc: PriorityService) -> None:
    score = svc.compute_priority(5, datetime.utcnow())
    assert 4.5 <= score <= 5.1  # ~5.0


def test_boundary_severity_5_old(svc: PriorityService) -> None:
    old = datetime.utcnow() - timedelta(days=60)
    score = svc.compute_priority(5, old)
    assert score == 2.5  # severity 5 * floor weight 0.5


def test_recency_weight_floor(svc: PriorityService) -> None:
    ancient = datetime.utcnow() - timedelta(days=365)
    score = svc.compute_priority(2, ancient)
    assert score == 1.0  # 2 * 0.5
