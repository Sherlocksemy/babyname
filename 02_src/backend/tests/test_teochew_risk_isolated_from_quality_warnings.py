from app.services.candidate_detail_service import CandidateDetailService


def test_teochew_risk_isolated_from_quality_warnings() -> None:
    payload = {
        "first_char": {"char": "思", "teochew": [{"pinyin_teochew": "si"}]},
        "second_char": {"char": "敬", "teochew": [{"pinyin_teochew": "gêng"}]},
        "quality_guard": {"passed": True, "hard_failures": [], "soft_warnings": ["GENERIC_NOTICE"]},
    }
    contract = CandidateDetailService()._teochew_contract(payload)
    assert contract["risk_level"] == "UNKNOWN"
    assert contract["full_name_reading_status"] == "PARTIAL"
