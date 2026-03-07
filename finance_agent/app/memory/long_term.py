from __future__ import annotations

import json
import os
from abc import ABC, abstractmethod


class BaseLongTermMemory(ABC):
    @abstractmethod
    def store(self, key: str, value: str) -> None: ...

    @abstractmethod
    def retrieve(self, query: str) -> list[str]: ...

    @abstractmethod
    def clear(self) -> None: ...


class JsonLongTermMemory(BaseLongTermMemory):
    """File-backed long-term memory using simple JSON storage."""

    def __init__(self, path: str = "./data/long_term_memory.json") -> None:
        self._path = path
        self._data: dict[str, str] = {}
        self._load()

    def _load(self) -> None:
        if os.path.exists(self._path):
            with open(self._path, "r") as f:
                self._data = json.load(f)

    def _save(self) -> None:
        os.makedirs(os.path.dirname(self._path) or ".", exist_ok=True)
        with open(self._path, "w") as f:
            json.dump(self._data, f, indent=2)

    def store(self, key: str, value: str) -> None:
        self._data[key] = value
        self._save()

    def retrieve(self, query: str) -> list[str]:
        query_lower = query.lower()
        return [
            f"{k}: {v}"
            for k, v in self._data.items()
            if query_lower in k.lower() or query_lower in v.lower()
        ]

    def clear(self) -> None:
        self._data.clear()
        self._save()
