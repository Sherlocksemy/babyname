from app.services.candidate_detail_service import CandidateDetailService


def test_direct_expression_requires_contiguous_given_name() -> None:
    payload = {
        "generation_mode": "direct_expression",
        "given_name": "思敬",
        "first_char": {"char": "思"},
        "second_char": {"char": "敬"},
        "evidences": [
            {
                "book": "诗经",
                "title": "关雎",
                "original_text": "求之不得，寤寐思服。我友敬矣，谗言其兴。",
                "evidence_level": "E1",
            }
        ],
    }
    origin = CandidateDetailService()._origin(payload)
    assert origin["mode"] == "SEMANTIC_ROLE_COMPOSITION"
    assert origin["name_level_evidence"] is None
