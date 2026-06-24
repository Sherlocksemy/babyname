def test_generate_lunar_api(api_client, api_payload) -> None:
    payload = dict(api_payload)
    payload.update({"calendar_type": "lunar", "birth_year": 2025, "birth_month": 2, "birth_day": 2, "is_leap_month": False, "generation_seed": 20260624})
    response = api_client.post("/api/v1/names/generate", json=payload)
    assert response.status_code == 202
    result = api_client.get(f"/api/v1/names/{response.json()['request_id']}").json()
    assert result["status"] == "COMPLETED"
    assert result["top3"]
