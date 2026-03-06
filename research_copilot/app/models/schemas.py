"""Pydantic v2 schemas for the research copilot API."""

from datetime import datetime

from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    question: str
    document_ids: list[str] = Field(default_factory=list)


class Citation(BaseModel):
    source: str
    title: str
    snippet: str


class ResearchResponse(BaseModel):
    answer: str
    citations: list[Citation]
    confidence_score: float = Field(ge=0.0, le=1.0)
    reasoning_trace: list[str]


class DocumentInfo(BaseModel):
    id: str
    filename: str
    chunk_count: int
    uploaded_at: datetime


class DocumentListResponse(BaseModel):
    documents: list[DocumentInfo]


class ToolResult(BaseModel):
    content: str
    source_name: str
    source_url: str | None = None


class HealthResponse(BaseModel):
    status: str
