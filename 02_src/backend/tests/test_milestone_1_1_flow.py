from __future__ import annotations


def test_milestone_1_1_flow_replaces_old_top3(alpha_result) -> None:
    top3 = [item["full_name"] for item in alpha_result["top3"]]

    assert "林仁贤" not in top3
    assert "林宜言" not in top3
    assert "林宇安" not in top3
    assert alpha_result["fortune_status"] in {"COMPLETE", "PARTIAL"}


def test_top3_has_no_repeated_chars_and_real_evidence(alpha_result) -> None:
    chars = "".join(item["given_name"] for item in alpha_result["top3"])

    assert len(chars) == len(set(chars))
    for item in alpha_result["top3"]:
        assert item["combined_meaning"]
        assert item["evidence_level"] in {"E1", "E2", "E2_COMPOSED", "E2_IMAGERY"}
        assert item["compatibility_level"] == "HIGH"
        assert item["naturalness_score"] >= 90
        assert item["evidences"][0]["original_text"]
