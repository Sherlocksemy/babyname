from __future__ import annotations

import json
from pathlib import Path

from app.engines.evidence_suitability_evaluator import EvidenceSuitabilityEvaluator
from app.engines.semantic_composition_validator import SemanticCompositionValidator


def test_weak_names_do_not_get_master_level_semantics() -> None:
    fixture = json.loads((Path(__file__).parent / "fixtures" / "weak_names.v1.json").read_text(encoding="utf-8"))
    validator = SemanticCompositionValidator()
    weak_scores = [validator.validate(item["given_name"], "S06", "A01")["meaning_completeness"] for item in fixture]

    assert max(weak_scores) < 90
    assert validator.validate("仁贤", "S02", "A03")["passed"] is False


def test_yiyan_and_yuan_do_not_become_e1_from_adjacent_context() -> None:
    evaluator = EvidenceSuitabilityEvaluator()

    assert evaluator.evaluate("宜言", {"original_text": "宜言饮酒，与子偕老", "match_type": "direct_bigram_same_sentence"}, "S02", "A03")["evidence_level"] != "E1"
    assert evaluator.evaluate("宇安", {"original_text": "万宇安人", "match_type": "direct_bigram_same_sentence"}, "S10", "A02")["evidence_level"] != "E1"
