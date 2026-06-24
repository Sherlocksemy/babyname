def test_favorite_api_is_idempotent(api_client, api_generated) -> None:
    request_id = api_generated["accepted"]["request_id"]
    candidate_id = api_generated["result"]["top3"][0]["candidate_id"]
    first = api_client.post("/api/v1/favorites", json={"request_id": request_id, "candidate_id": candidate_id})
    second = api_client.post("/api/v1/favorites", json={"request_id": request_id, "candidate_id": candidate_id})
    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["favorite_id"] == second.json()["favorite_id"]
    listed = api_client.get(f"/api/v1/favorites?request_id={request_id}")
    assert listed.status_code == 200
    assert listed.json()["favorites"]
