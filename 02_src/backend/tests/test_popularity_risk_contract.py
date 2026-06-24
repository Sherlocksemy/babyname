from app.services.candidate_detail_service import CandidateDetailService


def test_popularity_risk_contract_uses_template_label_not_duplicate_rate() -> None:
    payload = {"score": {"breakdown": {"uniqueness": 8.5}}, "historical_name_collision": "UNKNOWN"}
    contract = CandidateDetailService._popularity_template_risk(payload)
    assert contract["level"] == "LOW"
    assert contract["label"] == "低"
    assert "重名" not in str(contract)
