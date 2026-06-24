def test_ready_api_reports_loaded_knowledge(api_client) -> None:
    response = api_client.get("/ready")
    body = response.json()
    assert response.status_code == 200
    assert body["status"] == "ready"
    assert body["knowledge_loaded"] is True
    assert body["datasets"]["compliance_hanzi"] == 8105
    assert body["nes_version"] == "NES_MVP_2.0"
