from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CultureEvidence:
    evidence_id: str
    source_type: str
    book: str
    title: str | None
    author: str | None
    original_text: str
    matched_chars: list[str] = field(default_factory=list)
    matched_keywords: list[str] = field(default_factory=list)
    match_type: str = ""
    confidence: float = 0.0
    record_id: str | None = None
    evidence_level: str = "E3"
    suitability: dict | None = None

    def to_dict(self) -> dict:
        return {
            "evidence_id": self.evidence_id,
            "source_type": self.source_type,
            "book": self.book,
            "title": self.title,
            "author": self.author,
            "original_text": self.original_text,
            "matched_chars": self.matched_chars,
            "matched_keywords": self.matched_keywords,
            "match_type": self.match_type,
            "confidence": self.confidence,
            "record_id": self.record_id,
            "evidence_level": self.evidence_level,
            "suitability": self.suitability,
        }


@dataclass
class CandidateChar:
    char: str
    semantic_roles: list[str] = field(default_factory=list)
    structure_scores: dict[str, float] = field(default_factory=dict)
    archetype_scores: dict[str, float] = field(default_factory=dict)
    culture_evidence_ids: list[str] = field(default_factory=list)
    mandarin: list[dict] = field(default_factory=list)
    teochew: list[dict] = field(default_factory=list)
    popularity_penalty: float = 0.0
    risk_flags: list[str] = field(default_factory=list)
    final_score: float = 0.0

    def to_dict(self) -> dict:
        return {
            "char": self.char,
            "semantic_roles": self.semantic_roles,
            "structure_scores": self.structure_scores,
            "archetype_scores": self.archetype_scores,
            "culture_evidence_ids": self.culture_evidence_ids,
            "mandarin": self.mandarin,
            "teochew": self.teochew,
            "popularity_penalty": self.popularity_penalty,
            "risk_flags": self.risk_flags,
            "final_score": self.final_score,
        }


@dataclass
class NameCandidate:
    candidate_id: str
    surname: str
    given_name: str
    full_name: str
    structure_id: str
    archetype_id: str
    semantic_pattern: str
    culture_evidence_ids: list[str]
    generation_reason_codes: list[str]
    generation_seed: int
    first_char: CandidateChar | None = None
    second_char: CandidateChar | None = None
    quality_guard: dict | None = None
    score: dict | None = None
    evidences: list[CultureEvidence] = field(default_factory=list)
    semantic_role_first: str = ""
    semantic_role_second: str = ""
    combined_meaning: str = ""
    meaning_completeness: float = 0.0
    evidence_level: str = "E3"
    evidence_suitability_score: float = 0.0
    naturalness_score: float = 0.0
    structure_archetype_compatibility: float = 0.0
    compatibility_level: str = ""
    compatibility_reason_codes: list[str] = field(default_factory=list)
    semantic_validation: dict | None = None
    naturalness: dict | None = None
    generation_mode: str = ""
    first_char_source: list[str] = field(default_factory=list)
    second_char_source: list[str] = field(default_factory=list)
    structure_rule_ids: list[str] = field(default_factory=list)
    archetype_rule_ids: list[str] = field(default_factory=list)
    was_example_name: bool = False
    was_golden_fixture: bool = False
    was_direct_name_candidate: bool = False
    reconstruction: dict | None = None
    classic_expression_score: float = 0.0
    derivation_originality_score: float = 0.0
    corpus_copy_risk: float = 0.0
    historical_name_collision: str = "UNKNOWN"
    style_affinity_score: float = 0.0
    style_fit_score: float = 0.0
    gender_tone_fit_score: float = 0.0
    surname_fit_score: float = 0.0
    imagery_fit_score: float = 0.0
    profile_specificity_score: float = 0.0
    profile_fit_reasons: list[str] = field(default_factory=list)
    profile_conflicts: list[str] = field(default_factory=list)
    gender_tone_reason_codes: list[str] = field(default_factory=list)
    surname_fit: dict | None = None
    universal_candidate_risk: float = 0.0
    cross_profile_dominance_risk: float = 0.0

    def to_dict(self) -> dict:
        return {
            "candidate_id": self.candidate_id,
            "surname": self.surname,
            "given_name": self.given_name,
            "full_name": self.full_name,
            "structure_id": self.structure_id,
            "archetype_id": self.archetype_id,
            "semantic_pattern": self.semantic_pattern,
            "culture_evidence_ids": self.culture_evidence_ids,
            "generation_reason_codes": self.generation_reason_codes,
            "generation_seed": self.generation_seed,
            "quality_guard": self.quality_guard,
            "score": self.score,
            "evidences": [item.to_dict() for item in self.evidences],
            "semantic_role_first": self.semantic_role_first,
            "semantic_role_second": self.semantic_role_second,
            "combined_meaning": self.combined_meaning,
            "meaning_completeness": self.meaning_completeness,
            "evidence_level": self.evidence_level,
            "evidence_suitability_score": self.evidence_suitability_score,
            "naturalness_score": self.naturalness_score,
            "structure_archetype_compatibility": self.structure_archetype_compatibility,
            "compatibility_level": self.compatibility_level,
            "compatibility_reason_codes": self.compatibility_reason_codes,
            "semantic_validation": self.semantic_validation,
            "naturalness": self.naturalness,
            "generation_mode": self.generation_mode,
            "first_char_source": self.first_char_source,
            "second_char_source": self.second_char_source,
            "structure_rule_ids": self.structure_rule_ids,
            "archetype_rule_ids": self.archetype_rule_ids,
            "was_example_name": self.was_example_name,
            "was_golden_fixture": self.was_golden_fixture,
            "was_direct_name_candidate": self.was_direct_name_candidate,
            "reconstruction": self.reconstruction,
            "classic_expression_score": self.classic_expression_score,
            "derivation_originality_score": self.derivation_originality_score,
            "corpus_copy_risk": self.corpus_copy_risk,
            "historical_name_collision": self.historical_name_collision,
            "style_affinity_score": self.style_affinity_score,
            "style_fit_score": self.style_fit_score,
            "gender_tone_fit_score": self.gender_tone_fit_score,
            "surname_fit_score": self.surname_fit_score,
            "imagery_fit_score": self.imagery_fit_score,
            "profile_specificity_score": self.profile_specificity_score,
            "profile_fit_reasons": self.profile_fit_reasons,
            "profile_conflicts": self.profile_conflicts,
            "gender_tone_reason_codes": self.gender_tone_reason_codes,
            "surname_fit": self.surname_fit,
            "universal_candidate_risk": self.universal_candidate_risk,
            "cross_profile_dominance_risk": self.cross_profile_dominance_risk,
        }
