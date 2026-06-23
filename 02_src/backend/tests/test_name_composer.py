from __future__ import annotations


def test_name_composer_generates_at_least_sixty_unique_candidates(alpha_result) -> None:
    assert alpha_result["generated_candidates_count"] >= 60
    names = [item["given_name"] for item in alpha_result["top20"]]
    assert len(names) == len(set(names))


def test_generated_candidates_have_culture_evidence(alpha_result) -> None:
    assert alpha_result["top20"]
    assert all(item["culture_evidence_ids"] for item in alpha_result["top20"])
    assert all(item["evidences"] for item in alpha_result["top20"])
