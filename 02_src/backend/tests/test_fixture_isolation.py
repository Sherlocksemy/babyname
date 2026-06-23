from __future__ import annotations

from pathlib import Path


def test_production_code_does_not_read_test_fixtures() -> None:
    app_dir = Path(__file__).resolve().parents[1] / "app"
    forbidden = ["golden_names.v1.json", "weak_names.v1.json", "GOLDEN_MEANINGS"]
    offenders = []
    for path in app_dir.rglob("*.py"):
        if path.name == "run_milestone_1_2.py":
            continue
        text = path.read_text(encoding="utf-8")
        if any(token in text for token in forbidden):
            offenders.append(str(path))

    assert offenders == []


def test_name_composer_has_no_fixed_candidate_array() -> None:
    composer = Path(__file__).resolve().parents[1] / "app" / "engines" / "name_composer.py"
    text = composer.read_text(encoding="utf-8")

    assert "preferred =" not in text
    assert "was_golden_fixture=True" not in text
