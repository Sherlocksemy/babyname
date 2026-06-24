from app.services.naming_application_service import NamingApplicationService


def test_partial_result_contract_for_3_plus_less_than_7() -> None:
    contract = NamingApplicationService._result_contract({"qualified_count": 8}, [{}] * 3, [{}] * 5)
    assert contract["status"] == "PARTIAL"
    assert contract["result_status"] == "INSUFFICIENT_QUALIFIED_CANDIDATES"
    assert contract["counts"] == {"top3": 3, "backup": 5, "qualified": 8, "required": 10}


def test_top3_under_3_is_failed_contract() -> None:
    contract = NamingApplicationService._result_contract({"qualified_count": 2}, [{}] * 2, [])
    assert contract["status"] == "FAILED"
    assert contract["result_status"] == "INSUFFICIENT_QUALIFIED_CANDIDATES"
