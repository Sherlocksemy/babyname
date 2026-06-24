from __future__ import annotations

import json
from pathlib import Path


def test_real_name_quality_matrix_contains_five_cases_and_manual_fields() -> None:
    payload = json.loads(Path("reports/milestone_3_2a_generation_matrix.json").read_text(encoding="utf-8"))

    assert set(payload["cases"]) == {
        "case_a_lin_male_teochew",
        "case_b_chen_female",
        "case_c_huang_male",
        "case_d_zheng_female",
        "case_e_ouyang_neutral",
    }
    for case in payload["cases"].values():
        assert case["top3"]
        assert case["backup7"]
        for item in case["top3"]:
            assert item["combined_meaning"]
            assert item["culture_evidence"]
    for gates in payload["quality_gates"].values():
        assert gates["top3_naturalness"] is True
