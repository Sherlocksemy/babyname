from __future__ import annotations

from app.catalogs.character_risk_classifier import CharacterRiskClassifier


LEVEL_ORDER = {"CORE": 3, "EXTENDED": 2, "EXPERIMENTAL": 1, "REJECTED": 0}

POSITIVE_CATEGORY_BONUS = {
    "WISDOM": 10,
    "LEARNING": 7,
    "VIRTUE": 10,
    "CULTIVATION": 8,
    "ASPIRATION": 8,
    "CAPABILITY": 6,
    "PEACE": 7,
    "AESTHETIC": 8,
    "BRIGHTNESS": 7,
    "LANDSCAPE": 4,
    "WATER": 4,
    "SPACE": 4,
    "GROWTH": 5,
    "ORDER": 5,
    "CULTURE": 6,
}


class NameabilityClassifier:
    def __init__(self, risk_classifier: CharacterRiskClassifier | None = None) -> None:
        self.risk_classifier = risk_classifier or CharacterRiskClassifier()

    def classify(
        self,
        profile: dict,
        categories: list[str],
        culture_links: list[dict],
        homophone_risks: list[dict] | None = None,
    ) -> dict:
        char = str(profile.get("char") or "")
        semantic = profile.get("semantic") or {}
        definition = str(semantic.get("definition") or "")
        positive_level = int(semantic.get("positive_level") or 0)
        common_level = int(semantic.get("common_level") or 3)
        mandarin = profile.get("mandarin") or []
        risk_codes, rejection_reasons = self.risk_classifier.classify(char, definition, homophone_risks)

        if not profile.get("is_compliant"):
            rejection_reasons.append("not_in_compliance_whitelist")
        if not definition:
            rejection_reasons.append("missing_definition")
        if not mandarin:
            rejection_reasons.append("missing_mandarin")
        if positive_level <= 1:
            risk_codes.append("LOW_SOURCE_POSITIVE_LEVEL")

        hard_reject = {
            "obvious_non_name_character",
            "negative_definition_hint",
            "function_word_semantic",
            "homophone_blacklist",
            "not_in_compliance_whitelist",
            "missing_definition",
            "missing_mandarin",
            "low_nameability_definition",
        }
        if hard_reject & set(rejection_reasons):
            return {
                "level": "REJECTED",
                "score": 0,
                "risk_codes": list(dict.fromkeys(risk_codes)),
                "rejection_reasons": list(dict.fromkeys(rejection_reasons)),
                "reason_codes": ["REJECTED_BY_RISK_OR_SOURCE"],
            }

        score = positive_level * 14 + (4 - common_level) * 8
        if positive_level <= 1:
            score -= 10
        score += min(14, len(culture_links) * 3)
        for category in categories:
            score += POSITIVE_CATEGORY_BONUS.get(category, 0)
        if "OBJECT_OR_TOOL_SEMANTIC" in risk_codes:
            score -= 18
        if "FUNCTION" in categories:
            score -= 12
        if "OBJECT" in categories:
            score -= 8
        if "LOW_SOURCE_POSITIVE_LEVEL" in risk_codes:
            score -= 8
        if len(mandarin) > 1:
            score -= 4
            risk_codes.append("POLYPHONE")
        if "UNKNOWN" in categories:
            score -= 8
        score = max(0, min(100, score))

        if score >= 78 and not (set(categories) & {"OBJECT", "FUNCTION"}):
            level = "CORE"
        elif score >= 58:
            level = "EXTENDED"
        else:
            level = "EXPERIMENTAL"
        return {
            "level": level,
            "score": round(score, 2),
            "risk_codes": list(dict.fromkeys(risk_codes)),
            "rejection_reasons": list(dict.fromkeys(rejection_reasons)),
            "reason_codes": [f"NAMEABILITY_{level}", "KNOWLEDGE_DERIVED_CLASSIFICATION"],
        }
