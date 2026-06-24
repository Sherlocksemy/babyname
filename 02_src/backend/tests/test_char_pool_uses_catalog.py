from __future__ import annotations

from app.engines.char_pool_builder import CharPoolBuilder
from app.schemas.naming_input import NamingInput


def test_char_pool_exposes_catalog_fields() -> None:
    pools = CharPoolBuilder().build(NamingInput(surname="林", gender="male"), [], [], [])
    first = pools["first_pool"][0]

    assert first.catalog_level in {"CORE", "EXTENDED"}
    assert first.catalog_score > 0
    assert first.reason_codes

