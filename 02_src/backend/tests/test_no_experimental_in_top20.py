from __future__ import annotations

import json
from pathlib import Path


def test_no_experimental_chars_in_top20_reports() -> None:
    payload = json.loads(Path("reports/milestone_3_2a_generation_matrix.json").read_text(encoding="utf-8"))

    for case in payload["cases"].values():
        assert case["metrics"]["experimental_char_count"] == 0

