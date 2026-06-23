from __future__ import annotations


def test_gender_tone_fit_has_scores_and_reason_codes(milestone_1_3_results) -> None:
    matrix = milestone_1_3_results["matrix_a"]
    for case in matrix.values():
        for item in case["top3"]:
            assert item["gender_tone_fit_score"] > 0
            assert item["gender_tone_reason_codes"]
    female_cases = [case for case in matrix.values() if case["input"]["gender"] == "female"]
    assert female_cases
    assert all(item["gender_tone_fit_score"] >= 70 for case in female_cases for item in case["top3"])

