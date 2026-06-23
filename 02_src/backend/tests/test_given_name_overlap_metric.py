from __future__ import annotations


def test_overlap_metrics_use_given_name_not_full_name(milestone_1_3_results) -> None:
    rows = milestone_1_3_results["matrix_b_overlap"]
    assert rows
    assert all("given_name_overlap" in row for row in rows)
    assert all("top20_given_name_jaccard" in row for row in rows)
    assert any(row["full_name_overlap"] == 0 and row["given_name_overlap"] > 0 for row in rows)

