from __future__ import annotations


def test_top20_candidate_provenance_is_clean(alpha_result) -> None:
    for item in alpha_result["top20"]:
        assert item["generation_mode"] in {"direct_expression", "semantic_role_composition", "imagery_transformation"}
        assert item["first_char_source"]
        assert item["second_char_source"]
        assert item["structure_rule_ids"]
        assert item["archetype_rule_ids"]
        assert item["was_example_name"] is False
        assert item["was_golden_fixture"] is False
        assert item["was_direct_name_candidate"] is False
