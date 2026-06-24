from __future__ import annotations


def test_fortune_score_is_capped_and_traceable(alpha_result) -> None:
    top = alpha_result["top3"][0]
    assert top["fortune_evaluation"]
    assert 0 <= (top["fortune_score"] or 0) <= 10
    assert top["fortune_evaluation"]["available_score"] <= 10
    assert top["fortune_evaluation"]["metadata"]


def test_no_precise_yongshen_is_fabricated(alpha_result) -> None:
    limitations = " ".join(alpha_result["fortune"]["five_elements"]["limitations"])
    assert "专家级喜用神" in limitations

