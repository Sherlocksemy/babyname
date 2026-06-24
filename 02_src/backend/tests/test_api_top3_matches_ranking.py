from app.orchestration.naming_alpha_orchestrator import NamingAlphaOrchestrator


def test_api_top3_matches_ranking_engine_order(api_client, api_payload) -> None:
    expected = NamingAlphaOrchestrator().run(api_payload)
    accepted = api_client.post("/api/v1/names/generate", json={**api_payload, "generation_seed": 20260623}).json()
    result = api_client.get(f"/api/v1/names/{accepted['request_id']}").json()
    assert [item["full_name"] for item in result["top3"]] == [item["full_name"] for item in expected["top3"]]
    assert [item["engine_candidate_id"] for item in result["top3"]] == [item["candidate_id"] for item in expected["top3"]]
