from __future__ import annotations

from datetime import datetime


class BaziEngine:
    STEMS = "甲乙丙丁戊己庚辛壬癸"
    BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
    ELEMENTS = {"甲": "木", "乙": "木", "寅": "木", "卯": "木", "丙": "火", "丁": "火", "巳": "火", "午": "火", "戊": "土", "己": "土", "辰": "土", "戌": "土", "丑": "土", "未": "土", "庚": "金", "辛": "金", "申": "金", "酉": "金", "壬": "水", "癸": "水", "子": "水", "亥": "水"}

    def analyze(self, birth_datetime: str | None) -> dict:
        dt = self._parse(birth_datetime)
        if not dt:
            return {"calendar_accuracy": "missing", "bazi": {}, "five_elements_count": {}, "preferred_elements": ["木", "水"], "explanation": "出生时间缺失，八字仅作降级参考。"}
        year = self._ganzhi(dt.year - 4)
        month = self._ganzhi(dt.month + dt.year)
        day = self._ganzhi(dt.toordinal())
        hour = self._ganzhi(dt.hour // 2 + dt.toordinal())
        pillars = {"year": year, "month": month, "day": day, "hour": hour}
        counts = {item: 0 for item in "金木水火土"}
        for pillar in pillars.values():
            for ch in pillar:
                element = self.ELEMENTS.get(ch)
                if element:
                    counts[element] += 1
        preferred = sorted(counts, key=lambda k: counts[k])[:2]
        return {
            "calendar_accuracy": "approximate",
            "bazi": pillars,
            "five_elements_count": counts,
            "preferred_elements": preferred,
            "explanation": f"按公历近似排盘，五行较弱项为{'、'.join(preferred)}；仅作传统文化参考。",
        }

    def _ganzhi(self, index: int) -> str:
        return self.STEMS[index % 10] + self.BRANCHES[index % 12]

    def _parse(self, value: str | None) -> datetime | None:
        if not value:
            return None
        for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d", "%Y/%m/%d %H:%M", "%Y/%m/%d"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        return None

