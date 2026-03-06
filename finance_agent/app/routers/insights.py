from __future__ import annotations

from fastapi import APIRouter, Request

from app.models.schemas import WeeklyInsight

router = APIRouter(tags=["insights"])


@router.get("/insights/weekly", response_model=WeeklyInsight)
async def weekly_insight(request: Request) -> WeeklyInsight:
    agent = request.app.state.agent
    return agent.get_weekly_insight()
