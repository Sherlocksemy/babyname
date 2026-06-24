from __future__ import annotations

import pytest

from app.engines.calendar_engine import CalendarEngine
from app.schemas.baby_profile import BabyProfile


def test_valid_lunar_leap_month() -> None:
    result = CalendarEngine().normalize(BabyProfile.from_dict({"surname": "黄", "calendar_type": "lunar", "birth_year": 2025, "birth_month": 6, "birth_day": 1, "is_leap_month": True}))
    assert result.is_leap_month is True
    assert result.solar_datetime.strftime("%Y-%m-%d") == "2025-07-25"


def test_invalid_lunar_leap_month_rejected() -> None:
    with pytest.raises(ValueError):
        CalendarEngine().normalize(BabyProfile.from_dict({"surname": "黄", "calendar_type": "lunar", "birth_year": 2025, "birth_month": 2, "birth_day": 1, "is_leap_month": True}))

