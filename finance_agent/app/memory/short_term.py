from __future__ import annotations


class ShortTermMemory:
    """In-memory conversation buffer with a fixed max size."""

    MAX_MESSAGES = 20

    def __init__(self) -> None:
        self._history: list[dict[str, str]] = []

    def add_message(self, role: str, content: str) -> None:
        self._history.append({"role": role, "content": content})
        if len(self._history) > self.MAX_MESSAGES:
            self._history = self._history[-self.MAX_MESSAGES :]

    def get_history(self) -> list[dict[str, str]]:
        return list(self._history)

    def clear(self) -> None:
        self._history.clear()
