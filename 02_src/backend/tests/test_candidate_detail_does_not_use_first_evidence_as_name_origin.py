def test_candidate_detail_does_not_use_first_evidence_as_name_origin(api_client, api_generated) -> None:
    request_id = api_generated["accepted"]["request_id"]
    candidate_id = api_generated["result"]["top3"][0]["candidate_id"]
    detail = api_client.get(f"/api/v1/names/{request_id}/candidates/{candidate_id}").json()
    origin = detail["origin"]
    assert origin["name_level_evidence"] is None
    assert "整体出处" not in origin["display_label"]
    assert "固定双字姓名表达" in origin["disclaimer"]
