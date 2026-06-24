from __future__ import annotations

from app.engines.semantic_composition_validator import SemanticCompositionValidator


def test_landscape_duplication_is_blocked() -> None:
    result = SemanticCompositionValidator().validate("峰山")

    assert "LANDSCAPE_DUPLICATION" in result["issues"]
    assert result["passed"] is False

