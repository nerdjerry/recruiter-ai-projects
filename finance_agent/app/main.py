from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.agents.finance_agent import FinanceAgent
from app.core.config import get_settings
from app.memory.long_term import JsonLongTermMemory
from app.memory.memory_manager import MemoryManager
from app.memory.short_term import ShortTermMemory
from app.models.schemas import HealthResponse
from app.routers import chat, insights, transactions
from app.services.categorizer import CategorizationService
from app.services.csv_importer import CsvImporter
from app.tools.budget_tool import BudgetTool
from app.tools.insight_tool import InsightTool
from app.tools.spending_tool import SpendingTool


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    csv_importer = CsvImporter(db_path=settings.db_path)
    categorizer = CategorizationService(config=settings)

    short_term = ShortTermMemory()
    long_term = JsonLongTermMemory()
    memory_manager = MemoryManager(short_term=short_term, long_term=long_term)

    spending_tool = SpendingTool(transaction_source=csv_importer)
    budget_tool = BudgetTool(memory_manager=memory_manager, transaction_source=csv_importer)
    insight_tool = InsightTool(config=settings, transaction_source=csv_importer, memory_manager=memory_manager)

    agent = FinanceAgent(
        memory_manager=memory_manager,
        spending_tool=spending_tool,
        budget_tool=budget_tool,
        insight_tool=insight_tool,
        config=settings,
    )

    app.state.agent = agent
    app.state.csv_importer = csv_importer
    app.state.categorizer = categorizer
    yield


app = FastAPI(title="Personal Finance Agent API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(transactions.router)
app.include_router(insights.router)


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")
