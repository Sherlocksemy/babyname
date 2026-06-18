from backend.app.services.char_service import CharService


def test_char_lookup_uses_local_knowledge_base():
    item = CharService().lookup("清")
    assert item["is_compliant"] is True
    assert item["pinyin"]
    assert item["kangxi_strokes"]
    assert item["element"] in {"木", "火", "土", "金", "水"}
    assert item["definition"]

