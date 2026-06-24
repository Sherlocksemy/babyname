def test_regenerate_does_not_repeat_previous_names(api_client, api_payload) -> None:
    first = api_client.post("/api/v1/names/generate", json={**api_payload, "generation_seed": 20270702}).json()
    first_result = api_client.get(f"/api/v1/names/{first['request_id']}").json()
    first_names = {item["full_name"] for item in first_result["top3"] + first_result["backup7"]}
    regen = api_client.post(f"/api/v1/names/{first['request_id']}/regenerate", json={"generation_seed": 20270703})
    assert regen.status_code == 202
    second_result = api_client.get(f"/api/v1/names/{first['request_id']}").json()
    second_names = {item["full_name"] for item in second_result["top3"] + second_result["backup7"]}
    assert first_names.isdisjoint(second_names)
