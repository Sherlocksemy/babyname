from __future__ import annotations

from backend.app.core.knowledge_loader import KnowledgeLoader


class ZodiacEngine:
    def __init__(self, loader: KnowledgeLoader | None = None) -> None:
        self.data = (loader or KnowledgeLoader()).load()
        self.rules = {row["zodiac"]: row for row in self.data["zodiac_taboo"]}

    def analyze(self, zodiac: str | None, chars: list[dict] | None = None) -> dict:
        if not zodiac:
            return {"zodiac": None, "score": 3, "notes": "未提供可判定生肖的出生年份。"}
        rule = self.rules.get(zodiac, {})
        good = self._split(rule.get("good_radicals", ""))
        bad = self._split(rule.get("bad_radicals", ""))
        matched_good = []
        matched_bad = []
        for item in chars or []:
            radical = item.get("radical", "")
            if radical in good:
                matched_good.append(item.get("char"))
            if radical in bad:
                matched_bad.append(item.get("char"))
        score = max(0, min(5, 3 + len(matched_good) - len(matched_bad)))
        return {"zodiac": zodiac, "score": score, "rule": rule, "matched_good": matched_good, "matched_bad": matched_bad, "notes": "生肖喜忌仅作传统文化参考。"}

    def _split(self, value: str) -> set[str]:
        return {item.strip() for item in value.split(",") if item.strip()}

