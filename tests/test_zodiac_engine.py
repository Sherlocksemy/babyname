from backend.app.engines.zodiac_engine import ZodiacEngine
from backend.app.services.char_service import CharService


def test_zodiac_engine_uses_knowledge_base_rules():
    chars = [CharService().lookup("清"), CharService().lookup("宁")]
    result = ZodiacEngine().analyze("马", chars)
    assert result["zodiac"] == "马"
    assert result["rule"]["good_radicals"]
    assert 0 <= result["score"] <= 5
    assert "传统文化参考" in result["notes"]
