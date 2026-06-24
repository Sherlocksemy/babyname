def test_regenerate_api_returns_new_completed_run(api_client, api_generated) -> None:
    request_id = api_generated["accepted"]["request_id"]
    response = api_client.post(f"/api/v1/names/{request_id}/regenerate", json={"generation_seed": 20270701})
    assert response.status_code == 202
    assert response.json()["status"] == "COMPLETED"
