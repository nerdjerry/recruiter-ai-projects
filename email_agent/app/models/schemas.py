"""Pydantic v2 schemas for the email intelligence agent."""

from datetime import datetime

from pydantic import BaseModel, Field


class EmailMessage(BaseModel):
    id: str
    sender: str
    subject: str
    body: str
    received_at: datetime


class Classification(BaseModel):
    intent: str = Field(pattern=r"^(inquiry|complaint|scheduling|spam|other)$")
    urgency: str = Field(pattern=r"^(high|medium|low)$")
    confidence: float = Field(ge=0.0, le=1.0)


class DraftReply(BaseModel):
    email_id: str
    subject: str
    body: str
    tone: str


class ProcessedEmail(BaseModel):
    email: EmailMessage
    classification: Classification
    draft_reply: DraftReply
    status: str = Field(
        default="pending", pattern=r"^(pending|approved|rejected)$"
    )


class HealthResponse(BaseModel):
    status: str
