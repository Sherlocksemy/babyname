from __future__ import annotations

from datetime import datetime

from app.engines.five_elements_engine import FiveElementsEngine
from app.engines.four_pillars_engine import FourPillarsEngine


def test_five_elements_counts_from_pillars_and_hidden_stems() -> None:
    pillars = FourPillarsEngine().calculate(datetime(2025, 3, 1, 8, 30))
    result = FiveElementsEngine().analyze(pillars)
    assert sum(result["element_counts"].values()) == 8
    assert sum(result["weighted_elements"].values()) > 8
    assert result["recommendation_status"] == "HEURISTIC"
    assert "喜用神" not in result["balance_summary"]

