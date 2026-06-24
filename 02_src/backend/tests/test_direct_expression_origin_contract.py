from app.services.candidate_detail_service import CandidateDetailService


def test_direct_expression_origin_contract() -> None:
    payload = {
        "generation_mode": "direct_expression",
        "given_name": "怀瑾",
        "combined_meaning": "怀瑾握瑜，取其美德。",
        "evidences": [
            {
                "source_type": "chuci",
                "book": "楚辞",
                "title": "九章",
                "author": "屈原",
                "original_text": "怀瑾握瑜兮，穷不知所示。",
                "evidence_level": "E1",
            }
        ],
    }
    origin = CandidateDetailService()._origin(payload)
    assert origin["mode"] == "DIRECT_EXPRESSION"
    assert origin["name_level_evidence"]["matched_text"] == "怀瑾"
    assert origin["name_level_evidence"]["exact_match"] is True
    assert origin["component_evidences"] == []
