def test_candidate_detail_api(api_client, api_generated) -> None:
    request_id = api_generated["accepted"]["request_id"]
    candidate_id = api_generated["result"]["top3"][0]["candidate_id"]
    response = api_client.get(f"/api/v1/names/{request_id}/candidates/{candidate_id}")
    body = response.json()
    assert response.status_code == 200
    assert body["name"]["full_name"]
    origin = body["origin"]
    if origin["name_level_evidence"]:
        assert origin["name_level_evidence"]["original_text"]
    else:
        assert origin["component_evidences"][0]["original_text"]
    assert body["fortune"]["wuge"]["interpretation_status"] == "DATA_INCOMPLETE"
    assert "免责声明" not in body["disclaimer"]
