from app.services.naming_application_service import NamingApplicationService


def test_complete_result_requires_exact_3_plus_7() -> None:
    contract = NamingApplicationService._result_contract({"qualified_count": 10}, [{}] * 3, [{}] * 7)
    assert contract["status"] == "COMPLETED"
    assert contract["result_status"] == "COMPLETE"
    assert contract["counts"] == {"top3": 3, "backup": 7, "qualified": 10, "required": 10}
