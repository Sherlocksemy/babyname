from __future__ import annotations

from app.catalogs.name_char_catalog_builder import ensure_name_char_catalog


def test_name_char_catalog_builder_outputs_8105_records() -> None:
    catalog = ensure_name_char_catalog()

    assert catalog["statistics"]["total_records"] == 8105
    assert "知" in catalog["records_by_char"]
    assert catalog["records_by_char"]["知"]["nameability_level"] in {"CORE", "EXTENDED", "EXPERIMENTAL"}

