from __future__ import annotations

from collections import Counter

from app.engines.char_pool_builder import NEGATIVE_HINTS, UNSUITABLE_CHARS
from app.engines.evidence_suitability_evaluator import EvidenceSuitabilityEvaluator
from app.engines.naturalness_guard import NaturalnessGuard
from app.engines.semantic_composition_validator import SemanticCompositionValidator
from app.engines.structure_archetype_compatibility import evaluate_compatibility
from app.indexes.character_index import CharacterIndex
from app.indexes.popularity_index import PopularityIndex
from app.indexes.pronunciation_index import PronunciationIndex
from app.schemas.candidate import NameCandidate
from app.schemas.naming_input import NamingInput


TEMPLATE_NAMES = {"梓涵", "梓轩", "若汐", "若兮", "沐辰", "子墨", "一诺", "雨桐", "梓萱", "浩轩", "宇轩", "子轩"}
TEMPLATE_PREFIXES = ("若", "梓", "沐")
TEMPLATE_SUFFIXES = ("轩", "宸", "涵", "萱")
COMMON_NOUN_NAMES = {"书信", "文书", "书卷", "山川", "江山", "云山", "川泽", "山信"}


class QualityGuard:
    def __init__(
        self,
        character_index: CharacterIndex | None = None,
        pronunciation_index: PronunciationIndex | None = None,
        popularity_index: PopularityIndex | None = None,
    ) -> None:
        self.character_index = character_index or CharacterIndex()
        self.pronunciation_index = pronunciation_index or PronunciationIndex()
        self.popularity_index = popularity_index or PopularityIndex()
        self.semantic_validator = SemanticCompositionValidator()
        self.naturalness_guard = NaturalnessGuard()
        self.evidence_evaluator = EvidenceSuitabilityEvaluator()

    def evaluate(self, candidate: NameCandidate, naming_input: NamingInput) -> dict:
        hard_failures: list[str] = []
        soft_warnings: list[str] = []
        penalties: dict[str, float] = {}
        given = candidate.given_name

        if len(given) != 2 or not all("\u4e00" <= char <= "\u9fff" for char in given):
            hard_failures.append("ILLEGAL_NAME_CHAR")
        for char in given:
            if not self.character_index.is_compliant(char):
                hard_failures.append("NON_COMPLIANT_CHAR")
            if char in naming_input.blocked_chars:
                hard_failures.append("USER_BLOCKED_CHAR")
            if char in UNSUITABLE_CHARS:
                hard_failures.append("UNSUITABLE_FUNCTION_CHAR")
        if given[0] == given[1]:
            hard_failures.append("DUPLICATED_INTERNAL_CHAR")
        if any(char in naming_input.surname for char in given):
            hard_failures.append("SURNAME_GIVEN_DUPLICATION")
        if self.popularity_index.is_blacklisted(given) or self.popularity_index.is_blacklisted(candidate.full_name):
            hard_failures.append("TOP_NAME_BLACKLIST")
        if self._is_template_name(given):
            hard_failures.append("TEMPLATE_NAME_PATTERN")
        if given in COMMON_NOUN_NAMES:
            hard_failures.append("COMMON_NOUN_OR_OBJECT_NAME")
        for char in given:
            if self.pronunciation_index.risks(char):
                hard_failures.append("HIGH_RISK_HOMOPHONE")
            profile = self.character_index.get(char)
            definition = str((profile.get("semantic") or {}).get("definition") or "")
            if any(hint in definition for hint in NEGATIVE_HINTS):
                hard_failures.append("NEGATIVE_SEMANTIC")
        if not candidate.evidences:
            hard_failures.append("MISSING_CULTURE_EVIDENCE")
        elif not self._evidence_supports_candidate(candidate):
            hard_failures.append("EVIDENCE_NOT_RELATED")
        if not candidate.structure_id:
            hard_failures.append("INCOMPLETE_STRUCTURE")
        if not candidate.archetype_id:
            hard_failures.append("INCOMPLETE_ARCHETYPE")

        semantic = candidate.semantic_validation or self.semantic_validator.validate(given, candidate.structure_id, candidate.archetype_id)
        candidate.semantic_validation = semantic
        candidate.semantic_role_first = semantic.get("semantic_role_first", "")
        candidate.semantic_role_second = semantic.get("semantic_role_second", "")
        candidate.combined_meaning = candidate.combined_meaning or semantic.get("combined_meaning", "")
        candidate.meaning_completeness = max(candidate.meaning_completeness, semantic.get("meaning_completeness", 0))
        for issue in semantic.get("issues", []):
            soft_warnings.append(issue)
        if not semantic.get("combined_meaning"):
            hard_failures.append("MISSING_COMBINED_MEANING")
        if not semantic.get("passed"):
            hard_failures.append("SEMANTIC_COMPOSITION_FAILED")

        compatibility = evaluate_compatibility(candidate.structure_id, candidate.archetype_id)
        candidate.structure_archetype_compatibility = compatibility["structure_archetype_compatibility"]
        candidate.compatibility_level = compatibility["compatibility_level"]
        candidate.compatibility_reason_codes = compatibility["compatibility_reason_codes"]
        if candidate.compatibility_level == "CONFLICT":
            hard_failures.append("STRUCTURE_ARCHETYPE_CONFLICT")
        elif candidate.compatibility_level == "LOW":
            penalties["LOW_STRUCTURE_ARCHETYPE_COMPATIBILITY"] = 8
            soft_warnings.append("LOW_STRUCTURE_ARCHETYPE_COMPATIBILITY")

        naturalness = candidate.naturalness or self.naturalness_guard.evaluate(candidate.full_name, given, semantic)
        candidate.naturalness = naturalness
        candidate.naturalness_score = naturalness["naturalness_score"]
        if not naturalness["passed"]:
            hard_failures.append("LOW_NATURALNESS")
        for issue in naturalness["issues"]:
            soft_warnings.append(issue)

        if candidate.evidences and candidate.evidence_level not in {"E2_COMPOSED", "E2_IMAGERY"}:
            best_suitability = None
            for evidence in candidate.evidences:
                result = evidence.suitability or self.evidence_evaluator.evaluate(given, evidence.to_dict(), candidate.structure_id, candidate.archetype_id)
                evidence.suitability = result
                evidence.evidence_level = result["evidence_level"]
                if best_suitability is None or result["evidence_suitability_score"] > best_suitability["evidence_suitability_score"]:
                    best_suitability = result
            if best_suitability:
                candidate.evidence_level = best_suitability["evidence_level"]
                candidate.evidence_suitability_score = best_suitability["evidence_suitability_score"]
                if candidate.evidence_level in {"E0", "E3"}:
                    hard_failures.append("INSUFFICIENT_CORE_EVIDENCE")
                for reason in best_suitability.get("reason_codes", []):
                    soft_warnings.append(reason)
        elif candidate.evidences:
            candidate.evidence_suitability_score = max(candidate.evidence_suitability_score, 82 if candidate.evidence_level == "E2_COMPOSED" else 80)
            soft_warnings.append(candidate.evidence_level)

        candidate.classic_expression_score = round(candidate.evidence_suitability_score * (1.0 if candidate.evidence_level == "E1" else 0.65), 2)
        candidate.corpus_copy_risk = 0.65 if candidate.evidence_level == "E1" and any(e.match_type == "direct_bigram_same_sentence" for e in candidate.evidences) else 0.18
        candidate.derivation_originality_score = round(max(0, 100 - candidate.corpus_copy_risk * 55 - candidate.classic_expression_score * 0.15), 2)
        candidate.historical_name_collision = "UNKNOWN"

        heat_penalty = 0.0
        for char in given:
            popularity = self.popularity_index.get_char(char)
            if not popularity:
                continue
            if popularity.get("heat_level") == "爆款":
                heat_penalty += 4
            elif popularity.get("heat_level") == "高":
                heat_penalty += 2
        if heat_penalty:
            penalties["POPULARITY"] = heat_penalty
            soft_warnings.append("POPULAR_CHAR_USED")

        counts = Counter(hard_failures)
        hard_failures = [key for key, count in counts.items() for _ in range(count)]
        return {
            "passed": not hard_failures,
            "hard_failures": hard_failures,
            "soft_warnings": soft_warnings,
            "penalties": penalties,
        }

    @staticmethod
    def _is_template_name(given_name: str) -> bool:
        return (
            given_name in TEMPLATE_NAMES
            or any(given_name.startswith(prefix) for prefix in TEMPLATE_PREFIXES)
            or any(given_name.endswith(suffix) for suffix in TEMPLATE_SUFFIXES)
        )

    @staticmethod
    def _evidence_supports_candidate(candidate: NameCandidate) -> bool:
        if any(all(char in evidence.original_text for char in candidate.given_name) for evidence in candidate.evidences):
            return True
        if candidate.evidence_level in {"E2_COMPOSED", "E2_IMAGERY"}:
            evidence_text = "".join(evidence.original_text for evidence in candidate.evidences)
            return all(char in evidence_text for char in candidate.given_name)
        return False
