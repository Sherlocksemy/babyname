from __future__ import annotations

from app.engines.char_pool_builder import CharPoolBuilder
from app.schemas.naming_input import NamingInput


def test_rejected_chars_do_not_enter_char_pool() -> None:
    naming_input = NamingInput(surname="林", gender="male")
    pools = CharPoolBuilder().build(naming_input, [], [], [])
    chars = {item.char for item in pools["first_pool"] + pools["second_pool"]}

    assert "乂" not in chars
    assert "罪" not in chars

