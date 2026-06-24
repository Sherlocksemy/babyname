from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.schemas.naming_input import NamingInput


@dataclass(frozen=True)
class BabyProfile:
    surname: str
    gender: str = "male"
    calendar_type: str = "solar"
    birth_year: int = 2025
    birth_month: int = 1
    birth_day: int = 1
    birth_hour: int = 0
    birth_minute: int = 0
    is_leap_month: bool = False
    birth_province: str = ""
    birth_city: str = ""
    timezone: str = "Asia/Shanghai"
    region: str = "mandarin"
    style_preferences: list[str] = field(default_factory=list)
    liked_chars: list[str] = field(default_factory=list)
    blocked_chars: list[str] = field(default_factory=list)
    exclude_given_names: list[str] = field(default_factory=list)
    generation_seed: int = 20260623

    @classmethod
    def from_dict(cls, payload: dict) -> "BabyProfile":
        if "birth_year" not in payload and "birth_date" in payload:
            year, month, day = [int(part) for part in str(payload.get("birth_date")).split("-")]
            hour, minute = [int(part) for part in str(payload.get("birth_time") or "00:00").split(":")[:2]]
            location = str(payload.get("birth_location") or "")
            return cls(
                surname=str(payload.get("surname", "")).strip(),
                gender=str(payload.get("gender", "male")).strip() or "male",
                calendar_type="solar",
                birth_year=year,
                birth_month=month,
                birth_day=day,
                birth_hour=hour,
                birth_minute=minute,
                birth_province="",
                birth_city=location.replace("广东", "").replace("省", "").strip() or location,
                timezone=str(payload.get("timezone", "Asia/Shanghai")).strip() or "Asia/Shanghai",
                region=str(payload.get("region", "mandarin")).strip() or "mandarin",
                style_preferences=list(payload.get("style_preferences") or []),
                liked_chars=list(payload.get("liked_chars") or []),
                blocked_chars=list(payload.get("blocked_chars") or []),
                exclude_given_names=list(payload.get("exclude_given_names") or []),
                generation_seed=int(payload.get("generation_seed", 20260623)),
            )
        return cls(
            surname=str(payload.get("surname", "")).strip(),
            gender=str(payload.get("gender", "male")).strip() or "male",
            calendar_type=str(payload.get("calendar_type", "solar")).strip() or "solar",
            birth_year=int(payload.get("birth_year", 2025)),
            birth_month=int(payload.get("birth_month", 1)),
            birth_day=int(payload.get("birth_day", 1)),
            birth_hour=int(payload.get("birth_hour", 0)),
            birth_minute=int(payload.get("birth_minute", 0)),
            is_leap_month=bool(payload.get("is_leap_month", False)),
            birth_province=str(payload.get("birth_province", "")).strip(),
            birth_city=str(payload.get("birth_city", "")).strip(),
            timezone=str(payload.get("timezone", "Asia/Shanghai")).strip() or "Asia/Shanghai",
            region=str(payload.get("region", "mandarin")).strip() or "mandarin",
            style_preferences=list(payload.get("style_preferences") or []),
            liked_chars=list(payload.get("liked_chars") or []),
            blocked_chars=list(payload.get("blocked_chars") or []),
            exclude_given_names=list(payload.get("exclude_given_names") or []),
            generation_seed=int(payload.get("generation_seed", 20260623)),
        )

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.surname:
            errors.append("surname is required")
        if len(self.surname) > 2:
            errors.append("surname currently supports one or two Chinese characters")
        if self.gender not in {"male", "female", "neutral", "unknown"}:
            errors.append("gender must be male, female, neutral, or unknown")
        if self.calendar_type not in {"solar", "lunar"}:
            errors.append("calendar_type must be solar or lunar")
        if self.timezone != "Asia/Shanghai":
            errors.append("Milestone 2 only supports timezone Asia/Shanghai")
        if not (1900 <= self.birth_year <= 2100):
            errors.append("birth_year must be within 1900-2100")
        if not (1 <= self.birth_month <= 12):
            errors.append("birth_month must be within 1-12")
        if not (1 <= self.birth_day <= 31):
            errors.append("birth_day must be within 1-31")
        if not (0 <= self.birth_hour <= 23):
            errors.append("birth_hour must be within 0-23")
        if not (0 <= self.birth_minute <= 59):
            errors.append("birth_minute must be within 0-59")
        if self.calendar_type == "solar":
            try:
                datetime(self.birth_year, self.birth_month, self.birth_day, self.birth_hour, self.birth_minute)
            except ValueError as exc:
                errors.append(f"invalid solar datetime: {exc}")
        return errors

    def to_naming_input(self) -> NamingInput:
        return NamingInput(
            surname=self.surname,
            gender=self.gender,
            birth_date=f"{self.birth_year:04d}-{self.birth_month:02d}-{self.birth_day:02d}",
            birth_time=f"{self.birth_hour:02d}:{self.birth_minute:02d}",
            birth_location=f"{self.birth_province}{self.birth_city}",
            region=self.region,
            style_preferences=self.style_preferences,
            liked_chars=self.liked_chars,
            blocked_chars=self.blocked_chars,
            exclude_given_names=self.exclude_given_names,
            generation_seed=self.generation_seed,
        )

    def to_dict(self) -> dict:
        return self.__dict__.copy()
