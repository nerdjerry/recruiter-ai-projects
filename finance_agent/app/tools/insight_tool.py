from __future__ import annotations

from collections import defaultdict
from datetime import date, timedelta

from langchain_openai import ChatOpenAI

from app.core.config import Settings
from app.core.prompts import INSIGHT_PROMPT
from app.memory.memory_manager import MemoryManager
from app.models.schemas import WeeklyInsight
from app.services.plaid_client import BaseTransactionSource


class InsightTool:
    """Generates proactive weekly spending insights (SRP)."""

    def __init__(
        self,
        config: Settings,
        transaction_source: BaseTransactionSource,
        memory_manager: MemoryManager,
    ) -> None:
        self._llm = ChatOpenAI(
            model=config.chat_model,
            api_key=config.openai_api_key,
            max_tokens=300,
            temperature=0.7,
        )
        self._source = transaction_source
        self._memory = memory_manager

    def run(self) -> WeeklyInsight:
        transactions = self._source.fetch(days=7)
        total_spent = sum(t.amount for t in transactions)

        by_category: dict[str, float] = defaultdict(float)
        for t in transactions:
            by_category[t.category] += t.amount

        top_categories = [
            {"category": cat, "amount": round(amt, 2)}
            for cat, amt in sorted(by_category.items(), key=lambda x: -x[1])[:5]
        ]

        today = date.today()
        period = f"{(today - timedelta(days=7)).isoformat()} to {today.isoformat()}"

        txn_summary = "\n".join(
            f"  {cat}: ${amt:,.2f}" for cat, amt in sorted(by_category.items(), key=lambda x: -x[1])
        )
        goals = self._memory.get_context("budget")["facts"]
        goal_text = "\n".join(goals) if goals else "No goals set."

        try:
            response = self._llm.invoke([
                ("human", INSIGHT_PROMPT.format(
                    transaction_summary=txn_summary or "No transactions this week.",
                    user_goals=goal_text,
                )),
            ])
            summary = response.content.strip()
        except Exception:
            summary = f"You spent ${total_spent:,.2f} this week across {len(by_category)} categories."

        return WeeklyInsight(
            summary=summary,
            top_categories=top_categories,
            total_spent=round(total_spent, 2),
            period=period,
        )
