"""FastAPI router for email endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.agents.email_agent import EmailAgent
from app.models.schemas import ProcessedEmail

router = APIRouter(prefix="/emails", tags=["emails"])

_agent_instance: EmailAgent | None = None


def set_agent(agent: EmailAgent) -> None:
    global _agent_instance
    _agent_instance = agent


def get_agent() -> EmailAgent:
    if _agent_instance is None:
        raise HTTPException(status_code=503, detail="Agent not initialised")
    return _agent_instance


@router.get("", response_model=list[ProcessedEmail])
def fetch_emails(agent: EmailAgent = Depends(get_agent)):
    return agent.process_emails()


@router.post("/{email_id}/approve")
def approve_email(
    email_id: str, agent: EmailAgent = Depends(get_agent)
):
    if not agent.approve(email_id):
        raise HTTPException(status_code=404, detail="Email not found")
    return {"detail": "approved", "email_id": email_id}


@router.post("/{email_id}/reject")
def reject_email(
    email_id: str, agent: EmailAgent = Depends(get_agent)
):
    if not agent.reject(email_id):
        raise HTTPException(status_code=404, detail="Email not found")
    return {"detail": "rejected", "email_id": email_id}
