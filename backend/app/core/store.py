from __future__ import annotations

from threading import Lock
from typing import Any


class MemoryStore:
    def __init__(self) -> None:
        self._requests: dict[str, dict[str, Any]] = {}
        self._favorites: list[dict[str, Any]] = []
        self._lock = Lock()

    def save_request(self, request_id: str, payload: dict[str, Any]) -> None:
        with self._lock:
            self._requests[request_id] = payload

    def get_request(self, request_id: str) -> dict[str, Any] | None:
        return self._requests.get(request_id)

    def add_favorite(self, favorite: dict[str, Any]) -> None:
        with self._lock:
            if favorite not in self._favorites:
                self._favorites.append(favorite)

    def favorites(self) -> list[dict[str, Any]]:
        return list(self._favorites)


store = MemoryStore()

