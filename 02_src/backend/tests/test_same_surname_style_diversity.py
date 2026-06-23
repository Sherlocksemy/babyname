from __future__ import annotations

from collections import Counter


def test_same_surname_different_styles_top3_are_diverse(milestone_1_3_results) -> None:
    matrix = milestone_1_3_results["matrix_a"]
    top3_names = [item["given_name"] for case in matrix.values() for item in case["top3"]]
    counts = Counter(top3_names)
    assert len(top3_names) == 15
    assert len(counts) >= 12
    assert len(counts) / len(top3_names) >= 0.8
    assert max(counts.values()) <= 2
    assert max(row["top3_given_name_overlap_count"] for row in milestone_1_3_results["matrix_a_overlap"]) <= 1
    assert max(row["top20_given_name_jaccard"] for row in milestone_1_3_results["matrix_a_overlap"]) <= 0.25

