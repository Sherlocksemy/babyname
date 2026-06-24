from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class NamingInput:
    surname: str
    gender: str = "male"
    birth_date: str = ""
    birth_time: str = ""
    birth_location: str = ""
    region: str = "mandarin"
    style_preferences: list[str] = field(default_factory=list)
    liked_chars: list[str] = field(default_factory=list)
    blocked_chars: list[str] = field(default_factory=list)
    exclude_given_names: list[str] = field(default_factory=list)
    generation_seed: int = 20260622

    @classmethod
    def from_dict(cls, payload: dict) -> "NamingInput":
        return cls(
            surname=str(payload.get("surname", "")).strip(),
            gender=str(payload.get("gender", "male")).strip() or "male",
            birth_date=str(payload.get("birth_date", "")).strip(),
            birth_time=str(payload.get("birth_time", "")).strip(),
            birth_location=str(payload.get("birth_location", "")).strip(),
            region=str(payload.get("region", "mandarin")).strip() or "mandarin",
            style_preferences=list(payload.get("style_preferences") or []),
            liked_chars=list(payload.get("liked_chars") or []),
            blocked_chars=list(payload.get("blocked_chars") or []),
            exclude_given_names=list(payload.get("exclude_given_names") or []),
            generation_seed=int(payload.get("generation_seed", 20260622)),
        )

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.surname:
            errors.append("surname is required")
        if len(self.surname) > 2:
            errors.append("surname currently supports one or two Chinese characters")
        if self.gender not in {"male", "female", "neutral", "unknown"}:
            errors.append("gender must be male, female, neutral, or unknown")
        return errors
