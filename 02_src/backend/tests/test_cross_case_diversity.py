from __future__ import annotations

from app.cli.run_milestone_1_2 import run_matrix


def test_cross_case_top20_overlap_under_threshold() -> None:
    matrix = run_matrix()

    assert all(rate <= 0.25 for rate in matrix["top20_overlap_matrix"].values())
    assert matrix["max_top20_overlap"] <= 0.25
