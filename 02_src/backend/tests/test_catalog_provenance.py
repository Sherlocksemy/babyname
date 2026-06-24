from __future__ import annotations

from app.catalogs.name_char_catalog_builder import ensure_name_char_catalog


def test_catalog_records_keep_source_fields() -> None:
    record = ensure_name_char_catalog()["records_by_char"]["知"]

    assert record["source_fields"]["compliance"].endswith("tongyong_guifan_hanzi.csv")
    assert record["source_fields"]["semantic"].endswith("char_semantic.json")

