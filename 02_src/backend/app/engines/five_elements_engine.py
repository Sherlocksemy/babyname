from __future__ import annotations

from collections import Counter

from app.engines.four_pillars_engine import HIDDEN_STEMS


ELEMENT_BY_STEM = {
    "甲": "wood",
    "乙": "wood",
    "丙": "fire",
    "丁": "fire",
    "戊": "earth",
    "己": "earth",
    "庚": "metal",
    "辛": "metal",
    "壬": "water",
    "癸": "water",
}
ELEMENT_BY_BRANCH = {
    "寅": "wood",
    "卯": "wood",
    "巳": "fire",
    "午": "fire",
    "辰": "earth",
    "戌": "earth",
    "丑": "earth",
    "未": "earth",
    "申": "metal",
    "酉": "metal",
    "亥": "water",
    "子": "water",
}
SEASON_BY_MONTH_BRANCH = {
    "寅": "spring",
    "卯": "spring",
    "辰": "spring_transition",
    "巳": "summer",
    "午": "summer",
    "未": "summer_transition",
    "申": "autumn",
    "酉": "autumn",
    "戌": "autumn_transition",
    "亥": "winter",
    "子": "winter",
    "丑": "winter_transition",
}


class FiveElementsEngine:
    def analyze(self, four_pillars: dict) -> dict:
        counts = Counter({"wood": 0, "fire": 0, "earth": 0, "metal": 0, "water": 0})
        weighted = Counter({"wood": 0.0, "fire": 0.0, "earth": 0.0, "metal": 0.0, "water": 0.0})
        pillars = [four_pillars[key] for key in ["year_pillar", "month_pillar", "day_pillar", "hour_pillar"]]
        for pillar in pillars:
            stem_el = ELEMENT_BY_STEM.get(pillar["stem"])
            branch_el = ELEMENT_BY_BRANCH.get(pillar["branch"])
            if stem_el:
                counts[stem_el] += 1
                weighted[stem_el] += 1.0
            if branch_el:
                counts[branch_el] += 1
                weighted[branch_el] += 0.8
            for hidden_stem in HIDDEN_STEMS.get(pillar["branch"], []):
                hidden_el = ELEMENT_BY_STEM.get(hidden_stem)
                if hidden_el:
                    weighted[hidden_el] += 0.25
        month_branch = four_pillars["month_pillar"]["branch"]
        season = SEASON_BY_MONTH_BRANCH.get(month_branch, "unknown")
        day_master_stem = four_pillars["day_pillar"]["stem"]
        day_master_element = ELEMENT_BY_STEM.get(day_master_stem, "")
        sorted_elements = sorted(weighted.items(), key=lambda item: item[1])
        supportive = [item[0] for item in sorted_elements[:2]]
        caution = [item[0] for item in sorted(weighted.items(), key=lambda item: -item[1])[:1]]
        return {
            "day_master": {"stem": day_master_stem, "element": day_master_element},
            "element_counts": dict(counts),
            "weighted_elements": {key: round(value, 2) for key, value in weighted.items()},
            "seasonal_context": season,
            "balance_summary": self._summary(weighted),
            "analysis_level": "FOUNDATION_V1",
            "status": "COMPLETE",
            "limitations": [
                "仅做天干、地支、藏干的基础五行统计。",
                "不输出完整旺衰、精确格局、调候或专家级喜用神。",
            ],
            "recommendation_status": "HEURISTIC",
            "supportive_elements": supportive,
            "caution_elements": caution,
            "confidence": 0.68,
        }

    @staticmethod
    def _summary(weighted: Counter) -> str:
        max_el, max_value = max(weighted.items(), key=lambda item: item[1])
        min_el, min_value = min(weighted.items(), key=lambda item: item[1])
        return f"基础统计显示 {max_el} 相对较多（{max_value:.2f}），{min_el} 相对较少（{min_value:.2f}）；仅作为启发式参考。"

