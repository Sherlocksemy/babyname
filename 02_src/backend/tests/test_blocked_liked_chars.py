from __future__ import annotations

from app.cli.run_milestone_1_2 import run_matrix


def test_blocked_chars_do_not_appear_and_liked_chars_participate() -> None:
    case_d = run_matrix()["cases"]["D"]

    assert case_d["blocked_char_hits"] == []
    assert case_d["liked_char_appearances"]
    assert len(case_d["liked_char_appearances"]) < len(case_d["top20"])
