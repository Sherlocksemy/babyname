from __future__ import annotations

from app.cli.run_milestone_1_2 import run_matrix


def test_golden_overlap_limit() -> None:
    matrix = run_matrix()

    for case in matrix["cases"].values():
        assert case["golden_overlap_rate"] <= 0.2
        assert case["document_example_overlap_rate"] <= 0.2
