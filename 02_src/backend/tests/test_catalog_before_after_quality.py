from __future__ import annotations

import json
from pathlib import Path


def test_before_after_quality_report_is_traceable_and_flags_known_case_d_gap() -> None:
    before_after = json.loads(Path("reports/milestone_3_2a_before_after.json").read_text(encoding="utf-8"))
    matrix = json.loads(Path("reports/milestone_3_2a_generation_matrix.json").read_text(encoding="utf-8"))

    assert before_after["before"]["available"] is True
    assert before_after["after"]["metrics"]["name_count"] > 0
    assert matrix["quality_gates"]["case_a_lin_male_teochew"]["top20_unique_chars"] is True
    assert matrix["quality_gates"]["case_d_zheng_female"]["top20_unique_chars"] is False
