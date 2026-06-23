from __future__ import annotations


def test_universal_candidate_risk_is_reported(alpha_result) -> None:
    for item in alpha_result["top20"]:
        assert "universal_candidate_risk" in item
        assert "cross_profile_dominance_risk" in item
        assert item["universal_candidate_risk"] >= 0
    assert all(item["profile_specificity_score"] >= 88 for item in alpha_result["top3"])

