from __future__ import annotations

from datetime import datetime

from app.engines.four_pillars_engine import FourPillarsEngine


def test_jieqi_month_boundary_changes_month_pillar() -> None:
    engine = FourPillarsEngine()
    before = engine.calculate(datetime(2025, 3, 5, 16, 0))
    after = engine.calculate(datetime(2025, 3, 5, 23, 30))
    assert before["month_pillar"]["text"] != after["month_pillar"]["text"]

