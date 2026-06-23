from __future__ import annotations

from app.engines.culture_retriever import CultureRetriever
from app.engines.evidence_suitability_evaluator import EvidenceSuitabilityEvaluator


def test_adjacent_chars_do_not_automatically_become_e1() -> None:
    evaluator = EvidenceSuitabilityEvaluator()
    result = evaluator.evaluate(
        "宜言",
        {"original_text": "宜言饮酒，与子偕老", "match_type": "direct_bigram_same_sentence"},
        "S02",
        "A03",
    )

    assert result["evidence_level"] in {"E0", "E2"}
    assert result["evidence_level"] != "E1"
    assert result["passed"] is False


def test_wan_yu_an_ren_does_not_make_yu_an_e1() -> None:
    result = EvidenceSuitabilityEvaluator().evaluate(
        "宇安",
        {"original_text": "五方降帝，万宇安人。", "match_type": "direct_bigram_same_sentence"},
        "S10",
        "A02",
    )

    assert result["evidence_level"] != "E1"
    assert "FORCED_INTERPRETATION" in result["reason_codes"]


def test_top_flow_can_produce_e1_with_real_evidence(alpha_result) -> None:
    candidates = alpha_result["top20"]

    assert any(candidate["evidence_level"] == "E1" for candidate in candidates)
    assert any(any(evidence["evidence_level"] == "E1" for evidence in candidate["evidences"]) for candidate in candidates)
