def test_generate_rejects_unsupported_city(api_client, api_payload) -> None:
    payload = dict(api_payload)
    payload["birth_city"] = "广州市"
    response = api_client.post("/api/v1/names/generate", json=payload)
    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "LOCATION_DATA_MISSING"
    assert body["error"]["field"] == "birth_city"
