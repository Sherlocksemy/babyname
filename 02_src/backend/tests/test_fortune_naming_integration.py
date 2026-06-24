from __future__ import annotations

def test_fortune_is_integrated_into_nes(alpha_result) -> None:
    top = alpha_result["top3"][0]
    assert top["score"]["score_version"] == "NES_MVP_2.0"
    assert top["score"]["max_score"] == 100
    assert top["score"]["breakdown"]["fortune"] is not None
    assert top["score"]["fortune_status"] in {"COMPLETE", "PARTIAL"}


def test_fortune_cannot_rescue_quality_guard_failure(alpha_result) -> None:
    top3_names = {item["full_name"] for item in alpha_result["top3"]}
    failed_names = {
        item["full_name"]
        for item in alpha_result["rejected_candidates"]
        if item.get("quality_guard") and item["quality_guard"].get("hard_failures")
    }
    assert top3_names.isdisjoint(failed_names)
