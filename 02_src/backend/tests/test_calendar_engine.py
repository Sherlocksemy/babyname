from __future__ import annotations

from app.engines.calendar_engine import CalendarEngine
from app.schemas.baby_profile import BabyProfile


def test_solar_to_lunar_vector() -> None:
    result = CalendarEngine().normalize(BabyProfile.from_dict({"surname": "林", "calendar_type": "solar", "birth_year": 2025, "birth_month": 3, "birth_day": 1}))
    assert result.lunar_date["month"] == 2
    assert result.lunar_date["day"] == 2
    assert result.calendar_library == "lunar-python"
    assert result.calendar_library_version == "1.4.8"


def test_lunar_to_solar_vector() -> None:
    result = CalendarEngine().normalize(BabyProfile.from_dict({"surname": "林", "calendar_type": "lunar", "birth_year": 2025, "birth_month": 2, "birth_day": 2}))
    assert result.solar_datetime.strftime("%Y-%m-%d") == "2025-03-01"

