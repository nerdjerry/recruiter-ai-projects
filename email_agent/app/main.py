"""FastAPI application entry point."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.agents.email_agent import EmailAgent
from app.core.config import get_settings
from app.models.schemas import HealthResponse
from app.routers.emails import router as emails_router, set_agent
from app.services.gmail_client import MockEmailClient
from app.tools.classify_tool import ClassifyTool
from app.tools.draft_tool import DraftTool

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI):
    settings = get_settings()
    client = MockEmailClient()
    classify_tool = ClassifyTool(settings)
    draft_tool = DraftTool(settings)
    agent = EmailAgent(
        email_client=client,
        classify_tool=classify_tool,
        draft_tool=draft_tool,
        max_emails=settings.max_emails_per_run,
    )
    set_agent(agent)
    logger.info("Email agent initialised with MockEmailClient")
    yield


app = FastAPI(title="Email Intelligence Agent API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(emails_router)


@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="ok")
