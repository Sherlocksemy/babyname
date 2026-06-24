from __future__ import annotations

CONCEPTUAL_SUFFIXES = {"序", "洲", "泽", "星"}


class NaturalnessGuard:
    def evaluate(self, full_name: str, given_name: str, semantic_validation: dict | None = None) -> dict:
        issues: list[str] = []
        completeness = (semantic_validation or {}).get("meaning_completeness", 72)
        score = 70 + min(24, completeness * 0.24)
        if semantic_validation:
            for issue in semantic_validation.get("issues", []):
                if issue in {"OBJECT_OBJECT_PAIR", "LANDSCAPE_DUPLICATION", "ABSTRACT_LABEL_PAIR", "SLOGAN_LIKE"}:
                    score -= 10
                    issues.append(issue)
                elif issue in {"FORCED_INTERPRETATION", "INCOMPLETE_PHRASE", "SEMANTIC_DISCONNECT"}:
                    score -= 14
                    issues.append(issue)
            if semantic_validation.get("meaning_completeness", 0) < 72:
                score -= 12
                issues.append("LOW_REAL_NAME_FEEL")
        if given_name[1] in CONCEPTUAL_SUFFIXES and completeness < 86:
            score -= 5
            issues.append("CONCEPTUALIZATION_RISK")
        if full_name[0] == given_name[0]:
            score -= 8
            issues.append("FULL_NAME_REPETITION")
        score += (sum(ord(char) for char in given_name) % 5) - 2
        score = max(0, min(100, score))
        return {
            "naturalness_score": score,
            "adult_usability": max(0, score - (5 if "CONCEPTUALIZATION_RISK" in issues else 0)),
            "spoken_usability": max(0, score - (8 if "LOW_REAL_NAME_FEEL" in issues else 0)),
            "full_name_fit": max(0, score - (10 if "FULL_NAME_REPETITION" in issues else 0)),
            "conceptualization_risk": max(0, 100 - score),
            "issues": sorted(set(issues)),
            "passed": score >= 70,
            "top20_allowed": score >= 80,
            "top10_allowed": score >= 85,
            "top3_allowed": score >= 90,
        }
