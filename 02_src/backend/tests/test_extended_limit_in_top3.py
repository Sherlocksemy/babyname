from __future__ import annotations

import json
from pathlib import Path


def test_top3_extended_char_limit_is_reported_and_respected() -> None:
    payload = json.loads(Path("reports/milestone_3_2a_generation_matrix.json").read_text(encoding="utf-8"))

    assert payload["cases"]["case_a_lin_male_teochew"]["metrics"]["top3_extended_char_count"] <= 2
    assert payload["cases"]["case_e_ouyang_neutral"]["metrics"]["top3_extended_char_count"] <= 2
    assert payload["quality_gates"]["case_d_zheng_female"]["top3_extended_limit"] is False
