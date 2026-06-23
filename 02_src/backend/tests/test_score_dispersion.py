from __future__ import annotations


def test_top10_score_dispersion(alpha_result) -> None:
    raw_scores = [item["score"]["raw_score"] for item in alpha_result["top10"]]
    naturalness = [item["naturalness_score"] for item in alpha_result["top10"]]
    top3_raw = [item["score"]["raw_score"] for item in alpha_result["top3"]]

    assert len(set(raw_scores)) >= 5
    assert len(set(top3_raw)) == len(top3_raw)
    assert len(set(naturalness)) >= 3
    assert all(item["score"]["sub_breakdown"] for item in alpha_result["top10"])
