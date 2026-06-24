from __future__ import annotations

from app.catalogs.name_char_catalog_builder import ensure_name_char_catalog


def test_catalog_order_is_deterministic() -> None:
    first = [record["char"] for record in ensure_name_char_catalog()["records"][:20]]
    second = [record["char"] for record in ensure_name_char_catalog()["records"][:20]]

    assert first == second

