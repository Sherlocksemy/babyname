from app.services.evidence_excerpt_builder import EvidenceExcerptBuilder


def test_evidence_excerpt_exact_match_contains_matched_text() -> None:
    evidence = {"original_text": "求之不得，寤寐思服。悠哉悠哉，辗转反侧。", "evidence_level": "E2"}
    excerpt = EvidenceExcerptBuilder().build(evidence, "思")
    assert excerpt["exact_match"] is True
    assert excerpt["match_start"] is not None
    assert "思" in excerpt["display_excerpt"]
