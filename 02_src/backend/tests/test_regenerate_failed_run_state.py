def test_regenerate_failed_run_state(api_client, api_generated) -> None:
    class FailingOrchestrator:
        def run(self, payload):
            raise RuntimeError("forced regenerate failure")

    original = api_client.app.state.orchestrator
    api_client.app.state.orchestrator = FailingOrchestrator()
    try:
        request_id = api_generated["accepted"]["request_id"]
        response = api_client.post(f"/api/v1/names/{request_id}/regenerate", json={})
        assert response.status_code == 500
    finally:
        api_client.app.state.orchestrator = original
