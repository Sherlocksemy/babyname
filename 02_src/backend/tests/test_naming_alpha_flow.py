from __future__ import annotations


def test_naming_alpha_flow_returns_real_top3(alpha_result) -> None:
    assert alpha_result["ok"] is True
    assert alpha_result["fortune_status"] in {"COMPLETE", "PARTIAL"}
    assert alpha_result["top3"]
    assert alpha_result["generated_candidates_count"] >= 60
    assert alpha_result["filtered_count"] >= 1


def test_top3_has_complete_evidence_chain(alpha_result) -> None:
    for item in alpha_result["top3"]:
        assert item["full_name"].startswith("林")
        assert item["culture_evidence_ids"]
        assert item["score"]["fortune_status"] in {"COMPLETE", "PARTIAL"}
        evidence_text = "".join(evidence["original_text"] for evidence in item["evidences"])
        if item["generation_mode"] in {"semantic_role_composition", "imagery_transformation"}:
            assert all(char in evidence_text for char in item["given_name"])
            continue
        for evidence in item["evidences"]:
            assert evidence["original_text"]
            assert all(char in evidence["original_text"] for char in item["given_name"]) or evidence["match_type"] == "two_chars_same_record"
