from __future__ import annotations

from app.engines.semantic_composition_validator import SemanticCompositionValidator


def test_virtue_stacking_is_blocked() -> None:
    result = SemanticCompositionValidator().validate("仁贤")

    assert "SEMANTIC_REDUNDANCY" in result["issues"]
    assert result["passed"] is False

