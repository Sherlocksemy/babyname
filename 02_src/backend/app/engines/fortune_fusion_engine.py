from __future__ import annotations

from app.schemas.fortune import ModuleResult


ELEMENT_CN_TO_EN = {"木": "wood", "火": "fire", "土": "earth", "金": "metal", "水": "water"}


class FortuneFusionEngine:
    def evaluate(self, candidate, five_elements: dict, zodiac: dict, wuge: dict) -> ModuleResult:
        limitations = []
        warnings = []
        score = 0.0
        available = 0.0
        recommended = list(five_elements.get("supportive_elements") or [])
        caution = list(five_elements.get("caution_elements") or [])
        char_elements = [self._char_element(candidate.first_char), self._char_element(candidate.second_char)]
        char_elements = [item for item in char_elements if item]
        if five_elements.get("recommendation_status") == "HEURISTIC":
            available += 4
            support_hits = sum(1 for item in char_elements if item in recommended)
            caution_hits = sum(1 for item in char_elements if item in caution)
            score += min(4, 2 + support_hits * 0.8 - caution_hits * 0.5)
            if support_hits >= 2:
                warnings.append("OVERCOMPENSATION_RISK")
                score -= 0.4
            limitations.extend(five_elements.get("limitations") or [])
        if zodiac.get("status") in {"COMPLETE", "PARTIAL"}:
            available += 2
            radicals = [self._char_radical(candidate.first_char), self._char_radical(candidate.second_char)]
            good = set(zodiac.get("preferred_radicals") or [])
            bad = set(zodiac.get("avoid_radicals") or [])
            score += max(0, min(2, 1 + 0.4 * sum(radical in good for radical in radicals) - 0.3 * sum(radical in bad for radical in radicals)))
        if wuge.get("status") == "COMPLETE":
            available += 1.5
            score += 1.0
            if wuge.get("interpretation_status") == "DATA_INCOMPLETE":
                limitations.append("五格仅计算数值，不使用占位81数理吉凶解释。")
        status = "COMPLETE" if available >= 7.5 else "PARTIAL" if available else "NOT_EVALUATED"
        return ModuleResult(
            module_id="fortune_fusion",
            status=status,
            score=round(max(0, min(10, score)), 2) if available else None,
            available_score=round(available, 2),
            max_score=10,
            recommended_elements=recommended,
            caution_elements=caution,
            preferred_char_features=[f"element:{item}" for item in recommended],
            avoid_char_features=[f"element:{item}" for item in caution],
            warnings=warnings,
            limitations=limitations,
            metadata={
                "char_elements": char_elements,
                "wuge": wuge,
                "zodiac": {"bazi_zodiac": zodiac.get("bazi_zodiac"), "folk_zodiac": zodiac.get("folk_zodiac")},
            },
        )

    @staticmethod
    def _char_element(char_obj) -> str:
        if not char_obj:
            return ""
        # CandidateChar does not carry element; filled by orchestration before scoring when possible.
        return getattr(char_obj, "element", "")

    @staticmethod
    def _char_radical(char_obj) -> str:
        if not char_obj:
            return ""
        return getattr(char_obj, "radical", "")
