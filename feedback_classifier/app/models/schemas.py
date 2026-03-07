"""Pydantic v2 request / response schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class FeedbackIn(BaseModel):
    text: str
    source: str = "manual"
    submitted_at: datetime = Field(default_factory=datetime.utcnow)


class FeedbackOut(BaseModel):
    id: int
    text: str
    sentiment: str
    topic: str
    summary: str
    severity: int
    priority_score: float
    source: str
    submitted_at: datetime
    classified_at: datetime


class FeedbackSummary(BaseModel):
    """Lightweight view used by the dashboard (ISP)."""

    id: int
    sentiment: str
    topic: str
    priority_score: float
    submitted_at: datetime


class PaginatedResults(BaseModel):
    items: list[FeedbackOut]
    total: int
    page: int
    page_size: int


class HealthResponse(BaseModel):
    status: str
