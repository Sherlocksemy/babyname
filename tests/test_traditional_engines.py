from backend.app.engines.bazi_engine import BaziEngine
from backend.app.engines.wuge_engine import WugeEngine
from backend.app.engines.zodiac_engine import ZodiacEngine
from backend.app.services.char_service import CharService


def test_bazi_zodiac_wuge_are_structured_references():
    bazi = BaziEngine().analyze("2026-06-18 09:30")
    assert bazi["calendar_accuracy"] == "approximate"
    chars = [CharService().lookup("清"), CharService().lookup("宁")]
    zodiac = ZodiacEngine().analyze("马", chars)
    assert "传统文化参考" in zodiac["notes"]
    wuge = WugeEngine().analyze("陈", "清宁")
    assert wuge["grids"]["总格"] > 0
    assert "传统文化参考" in wuge["notes"]

