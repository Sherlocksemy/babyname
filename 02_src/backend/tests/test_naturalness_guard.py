from __future__ import annotations

from app.engines.naturalness_guard import NaturalnessGuard
from app.engines.semantic_composition_validator import SemanticCompositionValidator


def test_naturalness_rejects_low_real_name_feel() -> None:
    semantic = SemanticCompositionValidator().validate("墨书", "S06", "A01")
    result = NaturalnessGuard().evaluate("林墨书", "墨书", semantic)

    assert result["naturalness_score"] < 70
    assert result["passed"] is False


def test_naturalness_allows_strong_nameable_phrase() -> None:
    semantic = SemanticCompositionValidator().validate("修远", "S03", "A05")
    result = NaturalnessGuard().evaluate("林修远", "修远", semantic)

    assert result["naturalness_score"] >= 90
    assert result["top3_allowed"] is True
