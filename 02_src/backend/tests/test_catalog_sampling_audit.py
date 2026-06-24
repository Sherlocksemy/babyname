from __future__ import annotations

import json
from pathlib import Path


def test_catalog_sampling_audit_uses_required_seed_and_sample_sizes() -> None:
    payload = json.loads(Path("reports/milestone_3_2a_catalog_sample_audit.json").read_text(encoding="utf-8"))

    assert payload["seed"] == 20260623
    assert payload["levels"]["CORE"]["sample_size"] == 200
    assert payload["levels"]["EXTENDED"]["sample_size"] == 200
    assert payload["levels"]["EXPERIMENTAL"]["sample_size"] == 100
    assert payload["levels"]["REJECTED"]["sample_size"] == 100
    assert payload["quality_gates"]["core_correct_rate_passed"] is True
    assert payload["quality_gates"]["extended_obvious_error_passed"] is True
    assert payload["quality_gates"]["rejected_false_kill_passed"] is True

