def test_result_api_returns_profile_fortune_and_candidates(api_client, api_generated) -> None:
    request_id = api_generated["accepted"]["request_id"]
    response = api_client.get(f"/api/v1/names/{request_id}")
    body = response.json()
    assert response.status_code == 200
    assert body["profile_summary"]["surname"] == "林"
    assert body["fortune_summary"]["calculation_status"] in {"COMPLETE", "PARTIAL"}
    assert body["result_status"] == "COMPLETE"
