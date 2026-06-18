from backend.app.engines.bazi_engine import BaziEngine


def test_bazi_engine_returns_explainable_reference():
    result = BaziEngine().analyze("2026-06-18 09:30")
    assert result["calendar_accuracy"] == "approximate"
    assert set(result["bazi"]) == {"year", "month", "day", "hour"}
    assert set(result["five_elements_count"]) == {"金", "木", "水", "火", "土"}
    assert result["preferred_elements"]
    assert "仅作传统文化参考" in result["explanation"]


def test_bazi_engine_handles_missing_birth_time():
    result = BaziEngine().analyze(None)
    assert result["calendar_accuracy"] == "missing"
    assert result["preferred_elements"]
