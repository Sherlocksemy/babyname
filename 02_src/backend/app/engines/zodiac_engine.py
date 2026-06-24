from __future__ import annotations

import csv
from pathlib import Path

from app.core.config import KNOWLEDGE_BASE_DIR


ZODIAC_BY_BRANCH = {
    "子": "鼠",
    "丑": "牛",
    "寅": "虎",
    "卯": "兔",
    "辰": "龙",
    "巳": "蛇",
    "午": "马",
    "未": "羊",
    "申": "猴",
    "酉": "鸡",
    "戌": "狗",
    "亥": "猪",
}


class ZodiacEngine:
    def __init__(self, rules_path: str | Path | None = None) -> None:
        self.rules_path = Path(rules_path) if rules_path else KNOWLEDGE_BASE_DIR / "06_numerology_layer" / "zodiac_taboo.csv"
        self.rules = self._load_rules()

    def analyze(self, four_pillars: dict, lunar_date: dict) -> dict:
        bazi = ZODIAC_BY_BRANCH.get(four_pillars["year_pillar"]["branch"], "")
        folk = str(lunar_date.get("zodiac") or "")
        row = self.rules.get(bazi, {})
        return {
            "bazi_zodiac": bazi,
            "folk_zodiac": folk,
            "boundary_difference": bool(bazi and folk and bazi != folk),
            "preferred_radicals": self._split(row.get("good_radicals", "")),
            "avoid_radicals": self._split(row.get("bad_radicals", "")),
            "matched_rules": [row.get("good_meaning", ""), row.get("bad_meaning", "")] if row else [],
            "status": "COMPLETE" if row else "PARTIAL",
            "rule_version": "zodiac_taboo.csv:2026-06-18",
            "warnings": [] if row else ["ZODIAC_RULE_MISSING"],
        }

    def _load_rules(self) -> dict[str, dict[str, str]]:
        with self.rules_path.open("r", encoding="utf-8-sig", newline="") as handle:
            return {row["zodiac"]: row for row in csv.DictReader(handle)}

    @staticmethod
    def _split(value: str) -> list[str]:
        return [item for item in value.split(",") if item]

