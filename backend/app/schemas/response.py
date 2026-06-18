from __future__ import annotations

from pydantic import BaseModel, Field

from backend.app.schemas.baby_profile import BabyProfile, BabyProfileRequest
from backend.app.schemas.name_candidate import NameCandidate


class GenerateNamesResponse(BaseModel):
    request_id: str
    profile: BabyProfile
    results: list[NameCandidate]


class RegenerateRequest(BaseModel):
    request_id: str
    locked_chars: list[str] = Field(default_factory=list)
    excluded_chars: list[str] = Field(default_factory=list)
    excluded_names: list[str] = Field(default_factory=list)


class FavoriteRequest(BaseModel):
    request_id: str
    name: str


class ErrorResponse(BaseModel):
    request_id: str | None = None
    code: str
    message: str
    details: dict | None = None


__all__ = [
    "BabyProfile",
    "BabyProfileRequest",
    "GenerateNamesResponse",
    "RegenerateRequest",
    "FavoriteRequest",
    "NameCandidate",
]

