from __future__ import annotations

from app.engines.char_pool_builder import CharPoolBuilder
from app.schemas.naming_input import NamingInput


def test_char_pool_contains_catalog_chars_beyond_legacy_anchor_set() -> None:
    legacy_anchor = set("知思明德仁义礼信文书闻清雅安宁和温润远行景云泽川山怀修诚敬正嘉乐新承彦辰星月华光")
    pools = CharPoolBuilder().build(NamingInput(surname="林", gender="male"), [], [], [])
    chars = {item.char for item in pools["first_pool"] + pools["second_pool"]}
    new_chars = chars - legacy_anchor

    assert len(chars) >= 80
    assert len(new_chars) / len(chars) >= 0.2

