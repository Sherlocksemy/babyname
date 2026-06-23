from __future__ import annotations


def test_candidate_quality_scorer_reports_nes_alpha_not_fortune(alpha_result) -> None:
    top = alpha_result["top3"][0]
    score = top["score"]

    assert score["score_version"] in {"NES_ALPHA_1.0", "NES_ALPHA_1.2", "NES_ALPHA_1.3"}
    assert score["available_max_score"] == 90
    assert score["fortune_score"] is None
    assert score["fortune_status"] == "NOT_EVALUATED"
    assert 0 < score["raw_score"] <= 90
    assert 0 < score["normalized_score"] <= 100
