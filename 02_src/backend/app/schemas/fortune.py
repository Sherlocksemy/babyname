from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ModuleResult:
    module_id: str
    status: str = "NOT_EVALUATED"
    score: float | None = None
    available_score: float = 0.0
    max_score: float = 10.0
    recommended_elements: list[str] = field(default_factory=list)
    caution_elements: list[str] = field(default_factory=list)
    preferred_char_features: list[str] = field(default_factory=list)
    avoid_char_features: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "module_id": self.module_id,
            "status": self.status,
            "score": self.score,
            "available_score": self.available_score,
            "max_score": self.max_score,
            "recommended_elements": self.recommended_elements,
            "caution_elements": self.caution_elements,
            "preferred_char_features": self.preferred_char_features,
            "avoid_char_features": self.avoid_char_features,
            "warnings": self.warnings,
            "limitations": self.limitations,
            "metadata": self.metadata,
        }


@dataclass
class FortuneContext:
    calendar: dict
    true_solar_time: dict
    four_pillars: dict
    five_elements: dict
    zodiac: dict
    fusion: dict
    status: str = "PARTIAL"

    def to_dict(self) -> dict:
        return self.__dict__.copy()
