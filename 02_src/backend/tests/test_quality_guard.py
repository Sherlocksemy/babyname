from __future__ import annotations

from app.engines.quality_guard import QualityGuard
from app.schemas.candidate import CultureEvidence, NameCandidate
from app.schemas.naming_input import NamingInput


def _candidate(given_name: str) -> NameCandidate:
    evidence = CultureEvidence(
        evidence_id="EV-test",
        source_type="sishuwujing",
        book="四书五经",
        title="测试",
        author=None,
        original_text=f"测试原文包含{given_name}",
        matched_chars=list(given_name),
        match_type="direct_bigram_same_sentence",
        confidence=0.9,
    )
    return NameCandidate(
        candidate_id="NC-test",
        surname="林",
        given_name=given_name,
        full_name="林" + given_name,
        structure_id="S06",
        archetype_id="A01",
        semantic_pattern="学问/文气",
        culture_evidence_ids=["EV-test"],
        generation_reason_codes=[],
        generation_seed=1,
        evidences=[evidence],
    )


def test_quality_guard_blocks_template_names() -> None:
    result = QualityGuard().evaluate(_candidate("梓轩"), NamingInput(surname="林"))

    assert result["passed"] is False
    assert "TEMPLATE_NAME_PATTERN" in result["hard_failures"]


def test_quality_guard_blocks_blacklisted_names() -> None:
    result = QualityGuard().evaluate(_candidate("秀英"), NamingInput(surname="林"))

    assert result["passed"] is False
    assert "TOP_NAME_BLACKLIST" in result["hard_failures"]
