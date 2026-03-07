from __future__ import annotations

import re

from langchain_openai import ChatOpenAI

from app.core.config import Settings
from app.core.prompts import FINANCE_CHAT_PROMPT
from app.memory.memory_manager import MemoryManager
from app.models.schemas import ChatResponse, WeeklyInsight
from app.tools.budget_tool import BudgetTool
from app.tools.insight_tool import InsightTool
from app.tools.spending_tool import SpendingTool


class FinanceAgent:
    """Conversational finance agent with memory injection (DI), powered by LangChain."""

    def __init__(
        self,
        memory_manager: MemoryManager,
        spending_tool: SpendingTool,
        budget_tool: BudgetTool,
        insight_tool: InsightTool,
        config: Settings,
    ) -> None:
        self._memory = memory_manager
        self._spending = spending_tool
        self._budget = budget_tool
        self._insight = insight_tool
        self._llm = ChatOpenAI(
            model=config.chat_model,
            api_key=config.openai_api_key,
            max_tokens=500,
            temperature=0.7,
        )

    def chat(self, message: str) -> ChatResponse:
        self._memory.add_conversation("user", message)

        # Extract budget goals before computing context so new goals are included
        self._extract_and_store_goals(message)

        context = self._memory.get_context(message)

        tool_results = self._route_tools(message)

        memory_text = "\n".join(context["facts"]) if context["facts"] else "No stored facts."
        system_prompt = FINANCE_CHAT_PROMPT.format(
            memory_context=memory_text,
            tool_results=tool_results or "No tool results.",
        )

        messages = [("system", system_prompt)]
        for msg in context["conversation"]:
            if msg["role"] == "user":
                role = "human"
            elif msg["role"] == "assistant":
                role = "ai"
            else:
                role = msg["role"]
            messages.append((role, msg["content"]))

        try:
            response = self._llm.invoke(messages)
            reply = response.content.strip()
        except Exception as e:
            reply = f"I encountered an error: {e}. Please check your API key."

        self._memory.add_conversation("assistant", reply)
        return ChatResponse(reply=reply, memory_context=context["facts"] or None)

    def get_weekly_insight(self) -> WeeklyInsight:
        return self._insight.run()

    def clear_memory(self) -> None:
        self._memory.clear_all()

    def _route_tools(self, message: str) -> str:
        msg_lower = message.lower()
        results: list[str] = []
        if any(w in msg_lower for w in ("spend", "transaction", "spent", "expense")):
            days = self._extract_days(msg_lower)
            results.append(self._spending.run(days=days))
        if any(w in msg_lower for w in ("budget", "goal", "limit", "target")):
            results.append(self._budget.run())
        return "\n\n".join(results)

    def _extract_and_store_goals(self, message: str) -> None:
        msg_lower = message.lower()
        if any(phrase in msg_lower for phrase in ("my budget", "my goal", "i want to spend", "limit of")):
            self._memory.store_fact("budget_goal", message)

    @staticmethod
    def _extract_days(text: str) -> int:
        match = re.search(r"(\d+)\s*days?", text)
        if match:
            return int(match.group(1))
        if "week" in text:
            return 7
        if "year" in text:
            return 365
        return 30
