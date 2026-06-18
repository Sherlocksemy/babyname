from __future__ import annotations

from backend.app.core.knowledge_loader import KnowledgeLoader


class CharService:
    def __init__(self, loader: KnowledgeLoader | None = None) -> None:
        self.loader = loader or KnowledgeLoader()
        self.data = self.loader.load()
        self.compliance = {row["char"]: row for row in self.data["compliance"]}
        self.base = {row["char"]: row for row in self.data["char_base"]}
        self.semantic = self.data["char_semantic"]
        self.kangxi = self.data["kangxi"]
        self.mandarin = self.data["mandarin"]
        self.teochew: dict[str, list[dict]] = {}
        for row in self.data["teochew"]:
            self.teochew.setdefault(row.get("char", ""), []).append(row)
        self.frequency = {row["char"]: row for row in self.data["char_frequency"]}

    def is_compliant(self, char: str) -> bool:
        return char in self.compliance

    def lookup(self, char: str) -> dict:
        compliant = self.is_compliant(char)
        base = self.base.get(char, {})
        semantic = self.semantic.get(char, {})
        kangxi = self.kangxi.get(char, {})
        frequency = self.frequency.get(char, {})
        return {
            "char": char,
            "is_compliant": compliant,
            "pinyin": self.mandarin.get(char, []),
            "teochew": self.teochew.get(char, []),
            "modern_strokes": self._int(base.get("strokes_modern") or self.compliance.get(char, {}).get("strokes_modern")),
            "kangxi_strokes": self._int(kangxi.get("kangxi_strokes")),
            "radical": base.get("radical") or self.compliance.get(char, {}).get("radical", ""),
            "structure": base.get("structure", ""),
            "wubi": base.get("wubi", ""),
            "element": kangxi.get("element", ""),
            "components": kangxi.get("components", []),
            "definition": semantic.get("definition", ""),
            "ancient_meaning": semantic.get("ancient_meaning", ""),
            "positive_level": self._int(semantic.get("positive_level"), 3),
            "common_level": self._int(semantic.get("common_level"), 3),
            "heat_level": frequency.get("heat_level", "低"),
            "gender_tendency": frequency.get("gender_tendency", "N"),
            "frequency_rank": self._int(frequency.get("frequency_rank")),
            "era_tag": frequency.get("era_tag", ""),
        }

    def score_char(self, char: str, preferred_elements: list[str] | None = None) -> int:
        item = self.lookup(char)
        if not item["is_compliant"]:
            return 0
        score = 50
        score += max(0, item["positive_level"] - 2) * 10
        score += max(0, 4 - item["common_level"]) * 8
        if preferred_elements and item["element"] in preferred_elements:
            score += 12
        if item["heat_level"] == "爆款":
            score -= 20
        elif item["heat_level"] == "高":
            score -= 8
        return max(0, min(100, score))

    def iter_nameable_chars(self) -> list[dict]:
        rows = []
        for char in self.compliance:
            item = self.lookup(char)
            if item["positive_level"] >= 3 and item["common_level"] <= 2:
                rows.append(item)
        return rows

    @staticmethod
    def _int(value, default: int | None = None) -> int | None:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

