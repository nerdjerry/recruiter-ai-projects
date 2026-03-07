"""FastAPI application entry-point for the Research Copilot."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.models.schemas import HealthResponse
from app.routers.research import router as research_router
from app.agents.research_agent import ResearchAgent
from app.services.confidence import ConfidenceService
from app.services.vectorstore import VectorStoreService
from app.tools.web_search_tool import WebSearchTool
from app.tools.retriever_tool import RetrieverTool
from app.tools.wikipedia_tool import WikipediaTool

_agent: ResearchAgent | None = None
_vectorstore: VectorStoreService | None = None


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    global _agent, _vectorstore
    settings = get_settings()
    _vectorstore = VectorStoreService(
        embedding_model=settings.embedding_model,
        vectorstore_path=settings.vectorstore_path,
        openai_api_key=settings.openai_api_key,
    )
    tools = [
        WebSearchTool(api_key=settings.tavily_api_key),
        RetrieverTool(vectorstore=_vectorstore),
        WikipediaTool(),
    ]
    _agent = ResearchAgent(
        tools=tools,
        chat_model=settings.chat_model,
        openai_api_key=settings.openai_api_key,
        confidence_service=ConfidenceService(),
    )
    yield


app = FastAPI(title="Research Copilot API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(research_router)


def get_agent() -> ResearchAgent:
    assert _agent is not None, "Agent not initialised"
    return _agent


def get_vectorstore() -> VectorStoreService:
    assert _vectorstore is not None, "VectorStore not initialised"
    return _vectorstore


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok")
