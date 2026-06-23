from __future__ import annotations

from app.cli.run_milestone_1_2 import run_matrix


def test_personalization_matrix_cases_vary() -> None:
    matrix = run_matrix()
    top3_sets = [tuple(case["top3"]) for case in matrix["cases"].values()]
    primary_structures = {case["primary_structure"] for case in matrix["cases"].values()}
    primary_archetypes = {case["primary_archetype"] for case in matrix["cases"].values()}

    assert len(set(top3_sets)) == len(top3_sets)
    assert len(primary_structures) >= 3
    assert len(primary_archetypes) >= 3
    assert matrix["max_top20_overlap"] <= 0.25
