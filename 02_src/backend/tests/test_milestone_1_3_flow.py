from __future__ import annotations

from app.cli.run_milestone_1_3 import matrix_a_summary, matrix_b_summary


def test_milestone_1_3_matrix_flow_passes(milestone_1_3_results) -> None:
    assert matrix_a_summary(milestone_1_3_results["matrix_a"])["meets_threshold"] is True
    assert matrix_b_summary(milestone_1_3_results["matrix_b"])["meets_threshold"] is True
    for matrix in [milestone_1_3_results["matrix_a"], milestone_1_3_results["matrix_b"]]:
        for case in matrix.values():
            assert len(case["top20"]) == 20
            assert len(case["top10"]) == 10
            assert len(case["top3"]) == 3
            assert case["top1"] is not None
