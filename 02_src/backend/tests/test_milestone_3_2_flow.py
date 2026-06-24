from __future__ import annotations


def test_milestone_3_2_flow_returns_catalog_driven_top3(alpha_result) -> None:
    assert alpha_result["result_status"] == "OK"
    assert alpha_result["top3"]
    for item in alpha_result["top3"]:
        assert item["first_char"]["catalog_level"] in {"CORE", "EXTENDED"}
        assert item["second_char"]["catalog_level"] in {"CORE", "EXTENDED"}

