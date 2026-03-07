from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class Transaction(BaseModel):
    id: str
    date: date
    description: str
    amount: float
    category: str = "other"
    source: str = "csv"


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    memory_context: Optional[list[str]] = Field(default=None)


class TransactionFilter(BaseModel):
    days: Optional[int] = None
    category: Optional[str] = None
    min_amount: Optional[float] = None


class WeeklyInsight(BaseModel):
    summary: str
    top_categories: list[dict]
    total_spent: float
    period: str


class SyncResponse(BaseModel):
    imported_count: int
    message: str


class HealthResponse(BaseModel):
    status: str
