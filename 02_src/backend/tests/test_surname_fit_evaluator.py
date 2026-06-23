from __future__ import annotations

def test_surname_fit_evaluator_outputs_required_fields(alpha_result) -> None:
    item = alpha_result["top20"][0]
    fit = item["surname_fit"]
    assert set(["surname", "given_name", "tone_pattern", "initial_conflicts", "final_conflicts", "rhythm_score", "visual_balance_score", "surname_fit_score"]).issubset(fit)
    assert 0 <= fit["surname_fit_score"] <= 100


def test_surname_fit_varies_by_surname(milestone_1_3_results) -> None:
    values_by_name: dict[str, set[float]] = {}
    for case in milestone_1_3_results["matrix_b"].values():
        for item in case["top20"]:
            values_by_name.setdefault(item["given_name"], set()).add(round(item["surname_fit_score"], 2))
    assert any(len(values) >= 2 for values in values_by_name.values())
