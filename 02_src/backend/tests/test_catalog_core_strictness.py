from __future__ import annotations

import json
from pathlib import Path


def test_catalog_core_strictness_report_passes_required_empty_field_gates() -> None:
    payload = json.loads(Path("reports/milestone_3_2a_core_strictness.json").read_text(encoding="utf-8"))

    assert payload["counts"]["core_total"] > 0
    assert payload["counts"]["empty_semantic_roles_count"] == 0
    assert payload["counts"]["empty_naming_meaning_count"] == 0
    assert payload["counts"]["nonempty_risk_count"] == 0

