from __future__ import annotations


def test_profile_conflicts_do_not_enter_top3(milestone_1_3_results) -> None:
    for matrix in [milestone_1_3_results["matrix_a"], milestone_1_3_results["matrix_b"]]:
        for case in matrix.values():
            assert all(not item["profile_conflicts"] for item in case["top3"])

