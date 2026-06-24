from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class GenerateAcceptedResponse(BaseModel):
    request_id: str
    status: str
    created_at: str


class NamingResultResponse(BaseModel):
    request_id: str
    status: str
    progress: dict[str, Any] | None = None
    profile_summary: dict[str, Any] | None = None
    fortune_summary: dict[str, Any] | None = None
    top3: list[dict[str, Any]] = []
    backup7: list[dict[str, Any]] = []
    result_status: str | None = None
    limitations: list[str] = []
    warnings: list[str] = []


class FavoriteResponse(BaseModel):
    favorite_id: str
    request_id: str
    candidate_id: str
    created_at: str
    candidate: dict[str, Any] | None = None
