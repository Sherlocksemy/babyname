from __future__ import annotations

from datetime import datetime

from app.engines.true_solar_time_engine import TrueSolarTimeEngine


def test_missing_location_is_not_guessed() -> None:
    result = TrueSolarTimeEngine().calculate(datetime(2025, 3, 1, 8, 30), "不存在城市")
    assert result.status == "LOCATION_DATA_MISSING"
    assert result.longitude is None


def test_longitude_and_equation_of_time_are_used() -> None:
    result = TrueSolarTimeEngine().calculate(datetime(2025, 3, 1, 8, 30), "汕头市")
    assert result.status == "COMPLETE"
    assert result.longitude_correction_minutes < 0
    assert result.equation_of_time_minutes is not None
    assert result.true_solar_time < result.standard_time


def test_true_solar_time_crosses_day_boundary() -> None:
    result = TrueSolarTimeEngine().calculate(datetime(2025, 3, 1, 0, 5), "揭阳市")
    assert result.date_shift == -1

