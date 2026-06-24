from __future__ import annotations

from app.engines.semantic_composition_validator import SemanticCompositionValidator


def test_semantic_validator_returns_catalog_evidence() -> None:
    result = SemanticCompositionValidator().validate("知微")

    assert result["passed"] is True
    assert result["first_role"]
    assert result["catalog_evidence"]["知"]

