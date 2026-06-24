from __future__ import annotations


def test_backup7_is_returned_and_quality_guard_passed(alpha_result) -> None:
    assert alpha_result["top3"]
    assert alpha_result["backup7"]
    combined = alpha_result["top3"] + alpha_result["backup7"]
    assert len(combined) <= 10
    assert all(not item["quality_guard"]["hard_failures"] for item in combined)
    assert len({item["given_name"] for item in combined}) == len(combined)

