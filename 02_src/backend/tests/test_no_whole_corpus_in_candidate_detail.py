from app.services.evidence_excerpt_builder import EvidenceExcerptBuilder


def test_no_whole_corpus_in_candidate_detail_excerpt() -> None:
    original = "关关雎鸠，在河之洲。" * 80 + "求之不得，寤寐思服。" + "悠哉悠哉，辗转反侧。" * 80
    excerpt = EvidenceExcerptBuilder().build({"original_text": original, "evidence_level": "E2"}, "思")
    assert len(excerpt["display_excerpt"]) <= 240
    assert len(excerpt["display_excerpt"]) < len(original)
