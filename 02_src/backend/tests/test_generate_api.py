def test_generate_api_returns_completed_real_result(api_generated) -> None:
    accepted = api_generated["accepted"]
    result = api_generated["result"]
    assert accepted["status"] == "COMPLETED"
    assert result["status"] == "COMPLETED"
    assert len(result["top3"]) == 3
    assert len(result["backup7"]) == 7
    assert all(item["quality_guard"]["passed"] for item in result["top3"])
