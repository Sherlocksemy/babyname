def test_invalid_leap_month_returns_contract_error(api_client, api_payload) -> None:
    payload = dict(api_payload)
    payload.update({"calendar_type": "lunar", "birth_month": 2, "is_leap_month": True, "generation_seed": 20260625})
    response = api_client.post("/api/v1/names/generate", json=payload)
    assert response.status_code == 422
    assert response.json()["error"]["code"] in {"INVALID_LEAP_MONTH", "INVALID_LUNAR_DATE", "GENERATION_FAILED"}
