from backend.app.engines.wuge_engine import WugeEngine


def test_wuge_engine_calculates_all_grids():
    result = WugeEngine().analyze("陈", "清宁")
    assert set(result["grids"]) == {"天格", "人格", "地格", "外格", "总格"}
    assert result["detail"]["总格"]["luck"] in {"吉", "凶", "平"}
    assert "传统文化参考" in result["notes"]
