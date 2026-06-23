from __future__ import annotations

from dataclasses import dataclass, field

from app.schemas.candidate import CandidateChar, CultureEvidence, NameCandidate
from app.schemas.naming_input import NamingInput


@dataclass
class NamingContext:
    naming_input: NamingInput
    structures: list[dict] = field(default_factory=list)
    archetypes: list[dict] = field(default_factory=list)
    culture_evidences: list[CultureEvidence] = field(default_factory=list)
    first_char_pool: list[CandidateChar] = field(default_factory=list)
    second_char_pool: list[CandidateChar] = field(default_factory=list)
    candidates: list[NameCandidate] = field(default_factory=list)
    passed_candidates: list[NameCandidate] = field(default_factory=list)
    filtered_count: int = 0
    filter_reasons: dict[str, int] = field(default_factory=dict)
    top20: list[NameCandidate] = field(default_factory=list)
    top10: list[NameCandidate] = field(default_factory=list)
    top3: list[NameCandidate] = field(default_factory=list)
    diversity_status: str = "OK"
    diversity_reason: str = ""
    fortune_status: str = "NOT_EVALUATED"
    fortune_reason: str = "当前bazi_rules不足以支持可靠计算"
