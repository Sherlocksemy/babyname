from __future__ import annotations

from app.cli.run_milestone_1_2 import run_matrix


def test_compound_surname_is_preserved() -> None:
    case_e = run_matrix()["cases"]["E"]

    assert case_e["top3"]
    assert all(name.startswith("欧阳") for name in case_e["top20"])
