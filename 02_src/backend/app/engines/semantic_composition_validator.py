from __future__ import annotations

from app.catalogs.nameability_classifier import HIGH_RISK_POLYPHONE_CHARS
from app.catalogs.name_char_catalog_builder import ensure_name_char_catalog


COMPLEMENTARY_CATEGORY_PAIRS: set[tuple[str, str]] = {
    ("WISDOM", "ASPIRATION"),
    ("WISDOM", "AESTHETIC"),
    ("WISDOM", "CULTIVATION"),
    ("WISDOM", "WISDOM"),
    ("WISDOM", "VIRTUE"),
    ("LEARNING", "VIRTUE"),
    ("LEARNING", "WISDOM"),
    ("CULTIVATION", "WISDOM"),
    ("CULTIVATION", "ASPIRATION"),
    ("CULTIVATION", "VIRTUE"),
    ("VIRTUE", "BRIGHTNESS"),
    ("VIRTUE", "CULTIVATION"),
    ("VIRTUE", "ORDER"),
    ("VIRTUE", "WISDOM"),
    ("VIRTUE", "ASPIRATION"),
    ("ASPIRATION", "CAPABILITY"),
    ("ASPIRATION", "BRIGHTNESS"),
    ("ASPIRATION", "AESTHETIC"),
    ("CAPABILITY", "ASPIRATION"),
    ("PEACE", "AESTHETIC"),
    ("AESTHETIC", "PEACE"),
    ("AESTHETIC", "VIRTUE"),
    ("AESTHETIC", "ASPIRATION"),
    ("BRIGHTNESS", "ASPIRATION"),
    ("BRIGHTNESS", "VIRTUE"),
    ("LANDSCAPE", "WISDOM"),
    ("LANDSCAPE", "AESTHETIC"),
    ("WATER", "AESTHETIC"),
    ("WATER", "PEACE"),
    ("SPACE", "ASPIRATION"),
    ("GROWTH", "VIRTUE"),
    ("ORDER", "VIRTUE"),
    ("CULTURE", "VIRTUE"),
    ("CULTURE", "WISDOM"),
}

WEAK_CATEGORY_COMBINATIONS: dict[tuple[str, str], str] = {
    ("VIRTUE", "VIRTUE"): "SEMANTIC_REDUNDANCY",
    ("OBJECT", "OBJECT"): "OBJECT_OBJECT_PAIR",
    ("OBJECT", "CULTURE"): "OBJECT_OBJECT_PAIR",
    ("CULTURE", "OBJECT"): "OBJECT_OBJECT_PAIR",
    ("LANDSCAPE", "LANDSCAPE"): "LANDSCAPE_DUPLICATION",
    ("WATER", "WATER"): "LANDSCAPE_DUPLICATION",
    ("WATER", "BRIGHTNESS"): "SEMANTIC_DISCONNECT",
    ("SPACE", "PEACE"): "FORCED_INTERPRETATION",
    ("BRIGHTNESS", "ORDER"): "SEMANTIC_DISCONNECT",
    ("LANDSCAPE", "WATER"): "LANDSCAPE_DUPLICATION",
    ("FUNCTION", "FUNCTION"): "LOW_NAMEABILITY",
    ("UNKNOWN", "UNKNOWN"): "SEMANTIC_DISCONNECT",
}

BLOCKING_ISSUES = {
    "LOW_NAMEABILITY",
    "FORCED_INTERPRETATION",
    "INCOMPLETE_PHRASE",
    "SEMANTIC_REDUNDANCY",
    "LANDSCAPE_DUPLICATION",
    "OBJECT_OBJECT_PAIR",
    "LOW_NAMEABILITY_PRIMARY_CATEGORY",
    "HIGH_RISK_POLYPHONE",
}


class SemanticCompositionValidator:
    def __init__(self) -> None:
        catalog = ensure_name_char_catalog()
        self.records_by_char = catalog["records_by_char"]
        self.culture_links = catalog["culture_links"]

    def validate(self, given_name: str, structure_id: str = "", archetype_id: str = "") -> dict:
        if len(given_name) != 2:
            return self._result(given_name, "", "", "", 0, ["INCOMPLETE_PHRASE", "LOW_NAMEABILITY"], False)

        first, second = given_name[0], given_name[1]
        first_record = self.records_by_char.get(first)
        second_record = self.records_by_char.get(second)
        issues: list[str] = []
        risk_codes: list[str] = []
        if not first_record or not second_record:
            issues.append("SEMANTIC_DISCONNECT")
            return self._result(given_name, "", "", "", 42, issues, False, risk_codes=["MISSING_CATALOG_RECORD"])
        if first_record["nameability_level"] == "REJECTED" or second_record["nameability_level"] == "REJECTED":
            issues.append("LOW_NAMEABILITY")
            risk_codes.append("CATALOG_REJECTED_CHAR")
        if self._primary_raw_category(first_record) in {"OBJECT", "FUNCTION", "UNKNOWN"} or self._primary_raw_category(second_record) in {"OBJECT", "FUNCTION", "UNKNOWN"}:
            issues.append("LOW_NAMEABILITY_PRIMARY_CATEGORY")
            risk_codes.append("LOW_NAMEABILITY_CATEGORY")
        if first in HIGH_RISK_POLYPHONE_CHARS or second in HIGH_RISK_POLYPHONE_CHARS:
            issues.append("HIGH_RISK_POLYPHONE")
            risk_codes.append("HIGH_RISK_POLYPHONE")

        first_cat, second_cat, relation_type = self._best_category_pair(first_record, second_record)
        pair = (first_cat, second_cat)
        if pair in WEAK_CATEGORY_COMBINATIONS:
            issues.append(WEAK_CATEGORY_COMBINATIONS[pair])
        if first_cat == second_cat and first_cat in {"VIRTUE", "LANDSCAPE", "WATER", "OBJECT"}:
            issues.append("SEMANTIC_REDUNDANCY" if first_cat == "VIRTUE" else WEAK_CATEGORY_COMBINATIONS.get(pair, "ABSTRACT_LABEL_PAIR"))
        if first in {"书", "墨"} and second in {"书", "墨"}:
            issues.append("OBJECT_OBJECT_PAIR")
        if first in {"川", "洲", "山", "岳", "峰"} and second in {"川", "洲", "山", "岳", "峰"}:
            issues.append("LANDSCAPE_DUPLICATION")

        complementary = relation_type == "COMPLEMENTARY"
        reverse_complementary = relation_type == "REVERSE_COMPLEMENTARY"
        base_quality = (float(first_record["nameability_score"]) + float(second_record["nameability_score"])) / 2
        completeness = base_quality
        if complementary:
            completeness += 6
            if pair == ("WISDOM", "WISDOM"):
                completeness += 8
        elif reverse_complementary:
            completeness += 3
        else:
            completeness -= 10
            if "SEMANTIC_DISCONNECT" not in issues and not set(issues) & {"OBJECT_OBJECT_PAIR", "LANDSCAPE_DUPLICATION"}:
                issues.append("SEMANTIC_DISCONNECT")

        if issues:
            completeness -= min(30, len(set(issues)) * 8)
        if "SEMANTIC_REDUNDANCY" in issues:
            completeness -= 8
        if any(category in {"OBJECT", "FUNCTION"} for category in (first_cat, second_cat)):
            completeness -= 8
            risk_codes.append("LOW_NAMEABILITY_CATEGORY")

        completeness = max(0, min(96, completeness))
        passed = completeness >= 72 and not set(issues) & BLOCKING_ISSUES
        first_role = self._primary_role(first_record)
        second_role = self._primary_role(second_record)
        meaning = self._derive_meaning(first, second, first_role, second_role, first_cat, second_cat) if passed else ""
        return self._result(
            first + second,
            first_role,
            second_role,
            meaning,
            round(completeness, 2),
            sorted(set(issues)),
            passed,
            first_category=first_cat,
            second_category=second_cat,
            relation_type=relation_type,
            risk_codes=sorted(set(risk_codes + first_record.get("risk_codes", []) + second_record.get("risk_codes", []))),
            catalog_evidence={
                first: self.culture_links.get(first, [])[:2],
                second: self.culture_links.get(second, [])[:2],
            },
        )

    @staticmethod
    def _primary_category(record: dict) -> str:
        for category in record.get("semantic_categories") or []:
            if category not in {"UNKNOWN", "OBJECT", "FUNCTION"}:
                return category
        return (record.get("semantic_categories") or ["UNKNOWN"])[0]

    @staticmethod
    def _primary_raw_category(record: dict) -> str:
        return (record.get("semantic_categories") or ["UNKNOWN"])[0]

    @classmethod
    def _best_category_pair(cls, first_record: dict, second_record: dict) -> tuple[str, str, str]:
        first_categories = [item for item in first_record.get("semantic_categories", []) if item not in {"UNKNOWN", "OBJECT", "FUNCTION"}]
        second_categories = [item for item in second_record.get("semantic_categories", []) if item not in {"UNKNOWN", "OBJECT", "FUNCTION"}]
        first_categories = first_categories or [cls._primary_category(first_record)]
        second_categories = second_categories or [cls._primary_category(second_record)]
        primary_pair = (cls._primary_category(first_record), cls._primary_category(second_record))
        if primary_pair in WEAK_CATEGORY_COMBINATIONS:
            return primary_pair[0], primary_pair[1], "WEAK"
        if primary_pair[0] == primary_pair[1] and primary_pair[0] in {"VIRTUE", "LANDSCAPE", "WATER", "OBJECT"}:
            return primary_pair[0], primary_pair[1], "WEAK"
        for first in first_categories[:4]:
            for second in second_categories[:4]:
                if (first, second) in COMPLEMENTARY_CATEGORY_PAIRS:
                    return first, second, "COMPLEMENTARY"
        for first in first_categories[:4]:
            for second in second_categories[:4]:
                if (second, first) in COMPLEMENTARY_CATEGORY_PAIRS:
                    return first, second, "REVERSE_COMPLEMENTARY"
        return first_categories[0], second_categories[0], "WEAK"

    @staticmethod
    def _primary_role(record: dict) -> str:
        roles = record.get("semantic_roles") or []
        return roles[0] if roles else "语义待审"

    @staticmethod
    def _derive_meaning(first: str, second: str, first_role: str, second_role: str, first_cat: str, second_cat: str) -> str:
        return f"{first}取{first_role}之意，{second}取{second_role}之意，组合为{first_cat}/{second_cat}相成。"

    @staticmethod
    def _result(
        given_name: str,
        role_first: str,
        role_second: str,
        meaning: str,
        completeness: float,
        issues: list[str],
        passed: bool,
        first_category: str = "",
        second_category: str = "",
        relation_type: str = "",
        risk_codes: list[str] | None = None,
        catalog_evidence: dict | None = None,
    ) -> dict:
        return {
            "given_name": given_name,
            "semantic_role_first": role_first,
            "semantic_role_second": role_second,
            "first_role": role_first,
            "second_role": role_second,
            "first_category": first_category,
            "second_category": second_category,
            "relation_type": relation_type,
            "combined_meaning": meaning,
            "meaning_completeness": completeness,
            "issues": issues,
            "risk_codes": risk_codes or [],
            "catalog_evidence": catalog_evidence or {},
            "passed": passed,
        }
