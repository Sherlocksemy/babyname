from __future__ import annotations


def test_same_style_different_surnames_are_not_identical(milestone_1_3_results) -> None:
    matrix = milestone_1_3_results["matrix_b"]
    top3_sets = [tuple(item["given_name"] for item in case["top3"]) for case in matrix.values()]
    top1_names = [case["top1"]["given_name"] for case in matrix.values() if case["top1"]]
    assert len(top1_names) == 5
    assert len(set(top1_names)) / len(top1_names) >= 0.6
    for index, left in enumerate(top3_sets):
        for right in top3_sets[index + 1 :]:
            assert left != right


def test_same_given_name_has_surname_fit_variation(milestone_1_3_results) -> None:
    values_by_name: dict[str, set[float]] = {}
    for case in milestone_1_3_results["matrix_b"].values():
        for item in case["top20"]:
            values_by_name.setdefault(item["given_name"], set()).add(round(item["surname_fit_score"], 2))
    assert any(len(values) >= 2 for values in values_by_name.values())

