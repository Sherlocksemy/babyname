from types import SimpleNamespace

from app.services.candidate_detail_service import CandidateDetailService


def test_ranking_score_contract_separates_nes_and_ranking_score() -> None:
    row = SimpleNamespace(score=94.04, rank_type="BACKUP7", rank_position=1)
    payload = {"score": {"normalized_score": 94.04, "alpha_grade": "卓越"}}
    contract = CandidateDetailService._score_contract(row, payload)
    assert contract["nes_score"] == 94.0
    assert "ranking_score" in contract
    assert contract["diversity_reasons"]
