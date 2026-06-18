from __future__ import annotations

from pydantic import BaseModel, Field


class ScoreBreakdown(BaseModel):
    compliance: int
    mandarin: int
    teochew: int
    meaning: int
    culture: int
    bazi: int
    zodiac: int
    popularity: int
    style: int
    total: int
    reasons: list[str] = Field(default_factory=list)


class NameCandidate(BaseModel):
    name: str
    given_name: str
    group: str = ""
    score: int
    pinyin: str
    summary: str
    meaning: dict
    culture_origin: dict
    pronunciation: dict
    teochew: dict
    bazi: dict
    zodiac: dict
    wuge: dict
    popularity: dict
    score_breakdown: ScoreBreakdown
    warnings: list[str] = Field(default_factory=list)
    recommendation_reason: str

