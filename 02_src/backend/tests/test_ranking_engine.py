from __future__ import annotations


def test_ranking_engine_top3_diversity(alpha_result) -> None:
    top3 = alpha_result["top3"]
    chars = "".join(item["given_name"] for item in top3)

    assert len(top3) == 3
    assert len({item["structure_id"] for item in top3}) >= 2
    assert len({item["archetype_id"] for item in top3}) >= 2
    assert len(chars) == len(set(chars))
    assert len({item["evidences"][0]["record_id"] for item in top3}) >= 2
