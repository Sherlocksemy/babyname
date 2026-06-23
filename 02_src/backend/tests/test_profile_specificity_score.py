from __future__ import annotations


def test_profile_specificity_fields_present_and_thresholded(alpha_result) -> None:
    assert alpha_result["profile"]["profile_signature"]
    assert alpha_result["profile"]["preferred_structures"]
    assert alpha_result["profile"]["preferred_archetypes"]
    assert alpha_result["profile"]["preferred_imagery"]
    for item in alpha_result["top20"]:
        assert item["profile_specificity_score"] >= 70
        assert item["profile_fit_reasons"]
    for item in alpha_result["top10"]:
        assert item["profile_specificity_score"] >= 80
    for item in alpha_result["top3"]:
        assert item["profile_specificity_score"] >= 88

