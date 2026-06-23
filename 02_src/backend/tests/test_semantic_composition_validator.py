from __future__ import annotations

from app.engines.semantic_composition_validator import SemanticCompositionValidator


def test_semantic_redundancy_is_detected() -> None:
    result = SemanticCompositionValidator().validate("仁贤", "S02", "A03")

    assert "SEMANTIC_REDUNDANCY" in result["issues"]
    assert result["meaning_completeness"] < 72


def test_object_stack_and_landscape_duplication_are_detected() -> None:
    validator = SemanticCompositionValidator()

    assert "OBJECT_OBJECT_PAIR" in validator.validate("墨书", "S06", "A01")["issues"]
    assert "LANDSCAPE_DUPLICATION" in validator.validate("川洲", "S05", "A09")["issues"]


def test_golden_semantic_unit_has_complete_meaning() -> None:
    result = SemanticCompositionValidator().validate("知微", "S01", "A01")

    assert result["passed"] is True
    assert result["meaning_completeness"] >= 90
