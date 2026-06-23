from __future__ import annotations


def test_top20_candidates_are_reconstructable(alpha_result) -> None:
    assert alpha_result["top20"]
    for item in alpha_result["top20"]:
        reconstruction = item["reconstruction"]
        assert reconstruction["reconstructable"] is True
        assert reconstruction["source_independent"] is True
        assert reconstruction["reconstruction_steps"]
