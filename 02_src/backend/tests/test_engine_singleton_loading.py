def test_engine_singleton_loading(api_client) -> None:
    first = api_client.get("/ready").json()
    second = api_client.get("/ready").json()
    assert first["knowledge_loaded"] is True
    assert second["knowledge_loaded"] is True
    assert first["datasets"] == second["datasets"]
