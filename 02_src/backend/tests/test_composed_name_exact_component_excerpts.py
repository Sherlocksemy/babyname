from app.services.candidate_detail_service import CandidateDetailService


def test_composed_name_returns_two_exact_component_excerpts() -> None:
    payload = {
        "generation_mode": "semantic_role_composition",
        "given_name": "思敬",
        "first_char": {"char": "思"},
        "second_char": {"char": "敬"},
        "evidences": [
            {"book": "诗经", "title": "关雎", "original_text": "求之不得，寤寐思服。", "evidence_level": "E2"},
            {"book": "诗经", "title": "沔水", "original_text": "我友敬矣，谗言其兴。", "evidence_level": "E2"},
        ],
    }
    origin = CandidateDetailService()._origin(payload)
    assert origin["mode"] == "SEMANTIC_ROLE_COMPOSITION"
    assert [item["char"] for item in origin["component_evidences"]] == ["思", "敬"]
    assert all(item["exact_match"] for item in origin["component_evidences"])
    assert all(item["char"] in item["display_excerpt"] for item in origin["component_evidences"])
