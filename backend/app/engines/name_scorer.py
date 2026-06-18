from __future__ import annotations

from backend.app.schemas.name_candidate import ScoreBreakdown


class NameScorer:
    def score(self, char_items: list[dict], pronunciation: dict, culture: dict, bazi: dict, zodiac: dict, wuge: dict, popularity: dict, style_hit: bool) -> ScoreBreakdown:
        compliance = 15 if all(item.get("is_compliant") for item in char_items) else 0
        mandarin = round(15 * pronunciation.get("score", 0) / 100)
        teochew = 10 if pronunciation.get("safe") else 2
        meaning = min(15, sum((item.get("positive_level") or 3) for item in char_items) + 6)
        culture_score = 15 if culture.get("has_core_origin") else 6
        bazi_score = 10 if any(item.get("element") in bazi.get("preferred_elements", []) for item in char_items) else 6
        zodiac_score = int(zodiac.get("score", 3))
        heat = popularity.get("heat_level", "低")
        popularity_score = {"极低": 10, "低": 9, "中": 7, "高": 4, "爆款": 0}.get(heat, 7)
        style = 5 if style_hit else 3
        reasons = []
        if not culture.get("has_core_origin"):
            reasons.append("未找到高置信度核心出处，文化分降级。")
        if heat in ("高", "爆款"):
            reasons.append("热度偏高，已降权。")
        if pronunciation.get("homophone_issues"):
            reasons.append("存在谐音风险。")
        total = compliance + mandarin + teochew + meaning + culture_score + bazi_score + zodiac_score + popularity_score + style
        return ScoreBreakdown(compliance=compliance, mandarin=mandarin, teochew=teochew, meaning=meaning, culture=culture_score, bazi=bazi_score, zodiac=zodiac_score, popularity=popularity_score, style=style, total=total, reasons=reasons)

