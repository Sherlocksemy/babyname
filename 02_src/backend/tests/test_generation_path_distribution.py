from __future__ import annotations


def test_top20_generation_path_distribution(milestone_1_3_results) -> None:
    for matrix in [milestone_1_3_results["matrix_a"], milestone_1_3_results["matrix_b"]]:
        for case in matrix.values():
            dist = case["path_distribution"]
            assert dist["total"] == 20
            assert dist["ratios"].get("direct_expression", 0) <= 0.50
            assert dist["ratios"].get("semantic_role_composition", 0) >= 0.30
            assert dist["ratios"].get("imagery_transformation", 0) >= 0.15

