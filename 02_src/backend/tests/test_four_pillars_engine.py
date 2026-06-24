from __future__ import annotations

from datetime import datetime

from app.engines.four_pillars_engine import FourPillarsEngine


def test_lichun_year_boundary_changes_year_pillar() -> None:
    engine = FourPillarsEngine()
    before = engine.calculate(datetime(2025, 2, 3, 20, 0))
    after = engine.calculate(datetime(2025, 2, 4, 12, 0))
    assert before["year_pillar"]["text"] == "甲辰"
    assert after["year_pillar"]["text"] == "乙巳"


def test_zi_hour_rule_is_configurable() -> None:
    engine = FourPillarsEngine()
    same = engine.calculate(datetime(2025, 3, 1, 23, 10), zi_hour_rule="SAME_DAY")
    next_day = engine.calculate(datetime(2025, 3, 1, 23, 10), zi_hour_rule="NEXT_DAY_AT_23")
    assert same["day_pillar"]["text"] != next_day["day_pillar"]["text"]


def test_four_pillars_cross_validation_present() -> None:
    result = FourPillarsEngine().calculate(datetime(2025, 3, 1, 8, 30))
    assert result["cross_validation"]["passed"] is True
    assert result["method"]["month_boundary"] == "JIEQI"

