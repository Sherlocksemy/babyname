from __future__ import annotations

from datetime import datetime

from app.engines.calendar_engine import CalendarEngine
from app.engines.four_pillars_engine import FourPillarsEngine
from app.engines.zodiac_engine import ZodiacEngine
from app.schemas.baby_profile import BabyProfile


def test_bazi_and_folk_zodiac_boundaries_are_distinct() -> None:
    profile = BabyProfile.from_dict({"surname": "林", "calendar_type": "solar", "birth_year": 2025, "birth_month": 1, "birth_day": 30})
    calendar = CalendarEngine().normalize(profile)
    pillars = FourPillarsEngine().calculate(calendar.solar_datetime)
    result = ZodiacEngine().analyze(pillars, calendar.lunar_date)
    assert result["bazi_zodiac"]
    assert result["folk_zodiac"]
    assert result["boundary_difference"] is True

