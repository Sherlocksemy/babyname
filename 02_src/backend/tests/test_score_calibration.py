from __future__ import annotations


def test_top3_all_meet_alpha_admission(alpha_result) -> None:
    assert alpha_result["top3"]
    for item in alpha_result["top3"]:
        score = item["score"]
        breakdown = score["breakdown"]
        assert score["top3_eligible"] is True
        assert score["raw_score"] >= 72
        assert breakdown["structure"] >= 15
        assert breakdown["culture"] >= 11
        assert breakdown["meaning"] >= 12
        assert breakdown["aesthetic"] >= 8
        assert item["naturalness_score"] >= 90
        assert item["evidence_level"] in {"E1", "E2", "E2_COMPOSED", "E2_IMAGERY"}


def test_top1_status_is_explicit(alpha_result) -> None:
    assert alpha_result["top1_status"] in {"OK", "NO_S_LEVEL_CANDIDATE"}
    if alpha_result["top1_status"] == "NO_S_LEVEL_CANDIDATE":
        assert alpha_result["top1"] is None
