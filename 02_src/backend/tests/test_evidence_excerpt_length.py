from app.services.evidence_excerpt_builder import EvidenceExcerptBuilder


def test_evidence_excerpt_length_never_exceeds_240_chars() -> None:
    long_text = "序言" * 100 + "我友敬矣，谗言其兴。" + "余文" * 100
    excerpt = EvidenceExcerptBuilder().build({"original_text": long_text, "evidence_level": "E2"}, "敬")
    assert "敬" in excerpt["display_excerpt"]
    assert len(excerpt["display_excerpt"]) <= 240
