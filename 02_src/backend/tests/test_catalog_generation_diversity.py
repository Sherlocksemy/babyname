from __future__ import annotations


def test_catalog_generation_has_multiple_paths(alpha_result) -> None:
    modes = {item["generation_mode"] for item in alpha_result["top20"]}

    assert len(alpha_result["top20"]) >= 10
    assert {"semantic_role_composition", "imagery_transformation"} & modes

