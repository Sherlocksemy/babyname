from __future__ import annotations

from app.engines.semantic_composition_validator import SemanticCompositionValidator


class EvidenceSuitabilityEvaluator:
    def __init__(self) -> None:
        self.semantic_validator = SemanticCompositionValidator()

    def evaluate(self, given_name: str, evidence: dict, structure_id: str, archetype_id: str) -> dict:
        original_text = str(evidence.get("original_text") or "")
        match_type = str(evidence.get("match_type") or "")
        semantic = self.semantic_validator.validate(given_name, structure_id, archetype_id)
        direct = given_name in original_text and match_type == "direct_bigram_same_sentence"
        context_support = semantic["passed"] and (direct or match_type == "two_chars_same_record")
        semantic_dependency = direct and self._has_surrounding_dependency(given_name, original_text)
        phrase_complete = semantic["passed"] and semantic["meaning_completeness"] >= 84 and not semantic_dependency
        nameability = semantic["passed"] and semantic["meaning_completeness"] >= 78

        if phrase_complete and context_support:
            level = "E1"
            passed = True
            score = min(96, 84 + semantic["meaning_completeness"] * 0.12)
        elif context_support and nameability and not semantic_dependency:
            level = "E2"
            passed = True
            score = 78
        elif match_type in {"single_char", "keyword", "source_priority", "two_chars_same_record"}:
            level = "E3"
            passed = False
            score = 52
        else:
            level = "E0"
            passed = False
            score = 20
        if "FORCED_INTERPRETATION" in semantic["issues"] or "INCOMPLETE_PHRASE" in semantic["issues"]:
            level = "E0" if direct else "E3"
            passed = False
            score = min(score, 35)

        reason_codes = []
        if direct and not phrase_complete:
            reason_codes.append("DIRECT_ADJACENT_NOT_AUTOMATIC_E1")
        if semantic_dependency:
            reason_codes.append("CONTEXT_DEPENDENT_PHRASE")
        reason_codes.extend(semantic["issues"])
        return {
            "evidence_level": level,
            "phrase_complete": phrase_complete,
            "semantic_dependency": semantic_dependency,
            "context_support": context_support,
            "nameability": nameability,
            "reason_codes": sorted(set(reason_codes)),
            "passed": passed,
            "evidence_suitability_score": score,
            "semantic": semantic,
        }

    @staticmethod
    def _has_surrounding_dependency(given_name: str, text: str) -> bool:
        index = text.find(given_name)
        if index < 0:
            return False
        before = text[index - 1] if index > 0 else ""
        after_index = index + len(given_name)
        after = text[after_index] if after_index < len(text) else ""
        punctuation = set("，。！？；、 \n\r：：“”")
        return bool(before and before not in punctuation) or bool(after and after not in punctuation)
