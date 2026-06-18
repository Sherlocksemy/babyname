from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class BabyProfileRequest(BaseModel):
    surname: str = Field(min_length=1, max_length=2)
    gender: str = "neutral"
    birth_datetime: str | None = None
    calendar_type: str = "solar"
    birth_place: str | None = None
    name_length: int = Field(default=2, ge=1, le=2)
    style_preferences: list[str] = Field(default_factory=list)
    generation_char: str | None = None
    banned_chars: list[str] = Field(default_factory=list)
    liked_chars: list[str] = Field(default_factory=list)
    expectations: list[str] = Field(default_factory=list)
    avoid_hot_names: bool = True
    need_teochew_check: bool = True
    need_culture_origin: bool = True
    weight_preference: str | None = None

    @field_validator("gender")
    @classmethod
    def normalize_gender(cls, value: str) -> str:
        mapping = {"男": "male", "女": "female", "中性": "neutral", "M": "male", "F": "female", "N": "neutral"}
        return mapping.get(value, value)


class BabyProfile(BaseModel):
    surname: str
    gender: str
    birth_datetime: str | None
    calendar_type: str
    birth_place: str | None
    name_length: int
    style_preferences: list[str]
    generation_char: str | None
    banned_chars: list[str]
    liked_chars: list[str]
    expectations: list[str]
    avoid_hot_names: bool
    need_teochew_check: bool
    need_culture_origin: bool
    zodiac: str | None
    preferred_elements: list[str]
    dialect_region: str | None
    preference_weights: dict[str, float]
    warnings: list[str] = Field(default_factory=list)

