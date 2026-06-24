from app.services.candidate_detail_service import CandidateDetailService


def test_dechu_is_not_direct_when_not_contiguous_in_binzhichuyan() -> None:
    payload = {
        "generation_mode": "direct_expression",
        "given_name": "德初",
        "first_char": {"char": "德"},
        "second_char": {"char": "初"},
        "evidences": [
            {
                "book": "诗经",
                "title": "宾之初筵",
                "original_text": "宾之初筵，左右秩秩。既醉以酒，既饱以德。",
                "evidence_level": "E1",
            }
        ],
    }
    origin = CandidateDetailService()._origin(payload)
    assert origin["mode"] != "DIRECT_EXPRESSION"
    assert origin["name_level_evidence"] is None
