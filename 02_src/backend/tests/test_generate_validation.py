def test_generate_rejects_invalid_input(api_client, api_payload) -> None:
    payload = dict(api_payload)
    payload["surname"] = ""
    response = api_client.post("/api/v1/names/generate", json=payload)
    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "INVALID_INPUT"
    assert "error" in body
