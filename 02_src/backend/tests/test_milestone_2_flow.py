from __future__ import annotations

from app.cli.run_milestone_1_3 import matrix_a_summary, matrix_b_summary


def test_milestone_2_reports_generated(milestone_2_reports) -> None:
    assert milestone_2_reports["milestone_2_data_audit.json"]["calendar_dependency"]["name"] == "lunar-python"
    assert milestone_2_reports["milestone_2_naming_integration.json"]["sample_top3"]


def test_milestone_1_3_matrix_still_passes(milestone_1_3_results) -> None:
    assert matrix_a_summary(milestone_1_3_results["matrix_a"])["meets_threshold"] is True
    assert matrix_b_summary(milestone_1_3_results["matrix_b"])["meets_threshold"] is True
