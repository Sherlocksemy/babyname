def test_regenerate_failure_preserves_previous_success(api_client, api_generated) -> None:
    request_id = api_generated["accepted"]["request_id"]
    before = api_client.get(f"/api/v1/names/{request_id}").json()

    class FailingOrchestrator:
        def run(self, payload):
            raise RuntimeError("forced regenerate failure")

    original = api_client.app.state.orchestrator
    api_client.app.state.orchestrator = FailingOrchestrator()
    try:
        api_client.post(f"/api/v1/names/{request_id}/regenerate", json={})
    finally:
        api_client.app.state.orchestrator = original
    after = api_client.get(f"/api/v1/names/{request_id}").json()
    assert after["top3"] == before["top3"]
    assert after["backup7"] == before["backup7"]
    assert after["status"] in {"COMPLETED", "PARTIAL"}
