from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class NamingGenerateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    surname: str = Field(min_length=1, max_length=2)
    gender: str = Field(pattern="^(male|female|neutral|unknown)$")
    calendar_type: str = Field(default="solar", pattern="^(solar|lunar)$")
    birth_year: int = Field(ge=1900, le=2100)
    birth_month: int = Field(ge=1, le=12)
    birth_day: int = Field(ge=1, le=31)
    birth_hour: int = Field(ge=0, le=23)
    birth_minute: int = Field(ge=0, le=59)
    is_leap_month: bool = False
    birth_province: str = "广东省"
    birth_city: str
    timezone: str = "Asia/Shanghai"
    region: str = "teochew"
    style_preferences: list[str] = Field(default_factory=list)
    liked_chars: list[str] = Field(default_factory=list)
    blocked_chars: list[str] = Field(default_factory=list)
    generation_seed: int | None = None

    @field_validator("surname", "birth_city", "birth_province", "timezone", "region")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()

    @field_validator("liked_chars", "blocked_chars")
    @classmethod
    def normalize_chars(cls, value: list[str]) -> list[str]:
        chars: list[str] = []
        for item in value:
            chars.extend(char for char in str(item).strip() if char.strip())
        return list(dict.fromkeys(chars))

    @field_validator("style_preferences")
    @classmethod
    def normalize_styles(cls, value: list[str]) -> list[str]:
        return [str(item).strip() for item in value if str(item).strip()]

    @model_validator(mode="after")
    def check_conflicts(self) -> "NamingGenerateRequest":
        conflict = set(self.liked_chars) & set(self.blocked_chars)
        if conflict:
            raise ValueError(f"liked_chars and blocked_chars conflict: {''.join(sorted(conflict))}")
        if self.timezone != "Asia/Shanghai":
            raise ValueError("timezone must be Asia/Shanghai")
        return self


class RegenerateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    generation_seed: int | None = None
    liked_chars: list[str] = Field(default_factory=list)
    blocked_chars: list[str] = Field(default_factory=list)


class FavoriteCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str
    candidate_id: str
