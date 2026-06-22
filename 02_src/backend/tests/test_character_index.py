from __future__ import annotations

from backend.app.indexes.character_index import CharacterIndex


def test_character_index_returns_zhi_profile() -> None:
    index = CharacterIndex()
    profile = index.get("知")

    assert profile["is_compliant"] is True
    assert profile["semantic"]["definition"]
    assert profile["kangxi"]["kangxi_strokes"]
    assert profile["mandarin"]


def test_character_index_can_query_unsuitable_rare_char() -> None:
    index = CharacterIndex()
    profile = index.get("乂")

    assert profile["char"] == "乂"
    assert "is_compliant" in profile
    assert profile["popularity"] is None or isinstance(profile["popularity"], dict)
