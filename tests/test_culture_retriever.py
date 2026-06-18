from backend.app.engines.culture_retriever import CultureRetriever


def test_culture_retriever_uses_local_candidates_and_content():
    retriever = CultureRetriever()
    result = retriever.find_origin("清柔", ["温润"])
    assert result["has_core_origin"] is True
    assert result["core"]["match_type"] in {"candidate_source", "direct_phrase"}
    assert result["core"]["original_text"]


def test_culture_retriever_does_not_fake_origin():
    result = CultureRetriever().find_origin("不存在")
    assert result["has_core_origin"] is False
    assert result["core"] == {}
