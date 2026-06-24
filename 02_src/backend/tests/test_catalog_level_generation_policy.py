from __future__ import annotations

from app.catalogs.character_risk_classifier import LOW_NAMEABILITY_CHARS
from app.engines.char_pool_builder import CharPoolBuilder
from app.schemas.naming_input import NamingInput


def test_generation_pool_excludes_low_nameability_chars() -> None:
    pools = CharPoolBuilder().build(NamingInput(surname="林", gender="male"), [], [], [])
    chars = {item.char for item in pools["first_pool"] + pools["second_pool"]}

    assert not (chars & LOW_NAMEABILITY_CHARS)

