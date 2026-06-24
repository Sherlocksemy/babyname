from __future__ import annotations

from datetime import datetime, timedelta

from app.adapters.lunar_calendar_adapter import LunarCalendarAdapter


STEMS = list("甲乙丙丁戊己庚辛壬癸")
BRANCHES = list("子丑寅卯辰巳午未申酉戌亥")
HIDDEN_STEMS = {
    "子": ["癸"],
    "丑": ["己", "癸", "辛"],
    "寅": ["甲", "丙", "戊"],
    "卯": ["乙"],
    "辰": ["戊", "乙", "癸"],
    "巳": ["丙", "庚", "戊"],
    "午": ["丁", "己"],
    "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "戊"],
    "酉": ["辛"],
    "戌": ["戊", "辛", "丁"],
    "亥": ["壬", "甲"],
}


class FourPillarsEngine:
    def __init__(self, adapter: LunarCalendarAdapter | None = None) -> None:
        self.adapter = adapter or LunarCalendarAdapter()

    def calculate(self, solar_datetime: datetime, true_solar_time: datetime | None = None, zi_hour_rule: str = "SAME_DAY") -> dict:
        basis_time = true_solar_time or solar_datetime
        adjusted = self._apply_zi_rule(basis_time, zi_hour_rule)
        eight = self.adapter.eight_char(adjusted)
        cross_day = self._day_ganzhi_by_anchor(adjusted)
        warnings = []
        if cross_day != eight["day"]:
            warnings.append("DAY_PILLAR_CROSS_CHECK_MISMATCH")
        pillars = {
            "year_pillar": self._pillar(eight["year"]),
            "month_pillar": self._pillar(eight["month"]),
            "day_pillar": self._pillar(eight["day"]),
            "hour_pillar": self._pillar(eight["time"]),
        }
        hidden = {key: HIDDEN_STEMS.get(value["branch"], []) for key, value in pillars.items()}
        return {
            **pillars,
            "day_master": eight["day_gan"],
            "hidden_stems": hidden,
            "method": {
                "year_boundary": "LICHUN",
                "month_boundary": "JIEQI",
                "time_basis": "TRUE_SOLAR_TIME" if true_solar_time else "STANDARD_TIME",
                "zi_hour_rule": zi_hour_rule,
                "timezone": "Asia/Shanghai",
            },
            "cross_validation": {
                "day_pillar_anchor_method": cross_day,
                "library_day_pillar": eight["day"],
                "passed": cross_day == eight["day"],
                "anchor": "2000-01-01 戊午",
            },
            "status": "COMPLETE" if not warnings else "PARTIAL",
            "confidence": 0.88 if not warnings else 0.72,
            "warnings": warnings,
        }

    @staticmethod
    def _pillar(text: str) -> dict:
        return {"stem": text[:1], "branch": text[1:2], "text": text}

    @staticmethod
    def _apply_zi_rule(dt: datetime, zi_hour_rule: str) -> datetime:
        if zi_hour_rule == "NEXT_DAY_AT_23" and dt.hour >= 23:
            return dt + timedelta(days=1)
        return dt

    @staticmethod
    def _day_ganzhi_by_anchor(dt: datetime) -> str:
        anchor = datetime(2000, 1, 1)
        anchor_index = STEMS.index("戊") % 10
        anchor_branch = BRANCHES.index("午") % 12
        offset = (dt.date() - anchor.date()).days
        return STEMS[(anchor_index + offset) % 10] + BRANCHES[(anchor_branch + offset) % 12]
