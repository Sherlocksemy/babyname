from __future__ import annotations

import json
from pathlib import Path

from app.engines.semantic_composition_validator import SemanticCompositionValidator


def test_golden_names_are_semantic_anchors_not_generation_source() -> None:
    fixture = json.loads((Path(__file__).parent / "fixtures" / "golden_names.v1.json").read_text(encoding="utf-8"))
    validator = SemanticCompositionValidator()
    results = []
    for item in fixture:
        scored = validator.validate(item["given_name"], item["expected_structures"][0], item["expected_archetypes"][0])
        results.append(scored["meaning_completeness"])
    assert sum(results) / len(results) >= 68
