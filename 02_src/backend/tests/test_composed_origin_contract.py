def test_composed_origin_contract(api_generated) -> None:
    composed = api_generated["result"]["top3"][0]
    origin = composed["origin"]
    assert origin["mode"] in {"SEMANTIC_ROLE_COMPOSITION", "IMAGERY_TRANSFORMATION"}
    assert origin["name_level_evidence"] is None
    assert origin["disclaimer"]
