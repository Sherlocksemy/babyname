def test_composed_name_returns_two_evidences(api_client, api_generated) -> None:
    request_id = api_generated["accepted"]["request_id"]
    candidate_id = api_generated["result"]["top3"][0]["candidate_id"]
    detail = api_client.get(f"/api/v1/names/{request_id}/candidates/{candidate_id}").json()
    assert len(detail["origin"]["component_evidences"]) == 2
    assert {item["position"] for item in detail["origin"]["component_evidences"]} == {"FIRST", "SECOND"}
