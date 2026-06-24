from __future__ import annotations

from app.catalogs.name_char_catalog_builder import ensure_name_char_catalog


def test_catalog_core_extended_exceeds_legacy_whitelist_fourfold() -> None:
    stats = ensure_name_char_catalog()["statistics"]

    assert stats["total_records"] == 8105
    assert stats["core_extended_count"] >= 113 * 4

