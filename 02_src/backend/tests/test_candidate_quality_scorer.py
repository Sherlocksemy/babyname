from __future__ import annotations


def test_candidate_quality_scorer_reports_nes_mvp_with_fortune(alpha_result) -> None:
    top = alpha_result["top3"][0]
    score = top["score"]

    assert score["score_version"] == "NES_MVP_2.0"
    assert score["available_max_score"] == 100
    assert score["fortune_score"] is not None
    assert score["fortune_status"] in {"COMPLETE", "PARTIAL"}
    assert 0 < score["raw_score"] <= 100
    assert 0 < score["normalized_score"] <= 100
