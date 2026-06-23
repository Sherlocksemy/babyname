from __future__ import annotations

from app.engines.structure_archetype_compatibility import evaluate_compatibility


def test_s09_a03_is_conflict() -> None:
    result = evaluate_compatibility("S09", "A03")

    assert result["compatibility_level"] == "CONFLICT"
    assert result["passed"] is False


def test_documented_high_compatibility_pairs() -> None:
    assert evaluate_compatibility("S01", "A01")["compatibility_level"] == "HIGH"
    assert evaluate_compatibility("S10", "A04")["compatibility_level"] == "HIGH"
