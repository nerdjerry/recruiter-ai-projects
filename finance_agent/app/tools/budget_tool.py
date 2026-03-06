from __future__ import annotations

from collections import defaultdict

from app.memory.memory_manager import MemoryManager
from app.services.plaid_client import BaseTransactionSource


class BudgetTool:
    """Checks budget status against goals stored in long-term memory (SRP)."""

    def __init__(
        self, memory_manager: MemoryManager, transaction_source: BaseTransactionSource
    ) -> None:
        self._memory = memory_manager
        self._source = transaction_source

    def run(self) -> str:
        facts = self._memory.get_context("budget")["facts"]
        transactions = self._source.fetch(days=30)

        total_spent = sum(t.amount for t in transactions)
        by_category: dict[str, float] = defaultdict(float)
        for t in transactions:
            by_category[t.category] += t.amount

        lines = [f"Monthly spending: ${total_spent:,.2f}"]
        if facts:
            lines.append("Budget goals from memory:")
            for fact in facts:
                lines.append(f"  - {fact}")
        else:
            lines.append("No budget goals set. Tell me your goals and I'll remember them!")

        lines.append("Category breakdown:")
        for cat, amt in sorted(by_category.items(), key=lambda x: -x[1]):
            lines.append(f"  {cat}: ${amt:,.2f}")
        return "\n".join(lines)
