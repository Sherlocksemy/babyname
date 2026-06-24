def test_api_error_contract_hides_internal_paths(api_client) -> None:
    response = api_client.get("/api/v1/names/not-a-real-session")
    body = response.json()
    assert response.status_code == 404
    assert set(body.keys()) == {"error"}
    assert body["error"]["code"] == "SESSION_NOT_FOUND"
    assert "G:\\" not in str(body)
