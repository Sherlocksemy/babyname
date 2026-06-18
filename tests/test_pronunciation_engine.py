from backend.app.engines.pronunciation_engine import PronunciationEngine


def test_pronunciation_engine_checks_mandarin_teochew_and_risk():
    result = PronunciationEngine().analyze("陈", "清宁", True)
    assert result["pinyin"].startswith("chén")
    assert set(result["teochew"]) == {"清", "宁"}
    assert isinstance(result["homophone_issues"], list)
    assert 0 <= result["score"] <= 100
