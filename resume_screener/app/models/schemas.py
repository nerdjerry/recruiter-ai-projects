from __future__ import annotations

from pydantic import BaseModel, Field


class CandidateResult(BaseModel):
    name: str
    score: float = Field(ge=0, le=1)
    explanation: str
    skill_gaps: list[str] = Field(default_factory=list)


class ScreeningResponse(BaseModel):
    job_description: str
    candidates: list[CandidateResult]


class HealthResponse(BaseModel):
    status: str = "ok"
