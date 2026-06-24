from __future__ import annotations


def test_catalog_quality_regression_top3_has_reasons_and_no_rejected_chars(alpha_result) -> None:
    rejected_chars = {"乂", "罪", "徒", "届"}
    top3 = alpha_result["top3"]

    assert len(top3) == 3
    assert not any(any(char in rejected_chars for char in item["given_name"]) for item in top3)
    assert all(item["combined_meaning"] for item in top3)

