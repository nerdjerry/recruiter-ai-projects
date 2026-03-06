from __future__ import annotations

from app.memory.long_term import BaseLongTermMemory
from app.memory.short_term import ShortTermMemory


class MemoryManager:
    """Single coordinator for both short-term and long-term memory (SRP)."""

    def __init__(
        self, short_term: ShortTermMemory, long_term: BaseLongTermMemory
    ) -> None:
        self._short_term = short_term
        self._long_term = long_term

    def add_conversation(self, role: str, content: str) -> None:
        self._short_term.add_message(role, content)

    def store_fact(self, key: str, value: str) -> None:
        self._long_term.store(key, value)

    def get_context(self, query: str) -> dict:
        return {
            "conversation": self._short_term.get_history(),
            "facts": self._long_term.retrieve(query),
        }

    def clear_all(self) -> None:
        self._short_term.clear()
        self._long_term.clear()
