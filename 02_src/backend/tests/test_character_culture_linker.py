from __future__ import annotations

from app.catalogs.name_char_catalog_builder import ensure_name_char_catalog


def test_character_culture_linker_records_traceable_evidence() -> None:
    catalog = ensure_name_char_catalog()
    links = catalog["culture_links"]["知"]

    assert links
    assert links[0]["source_record_id"]
    assert links[0]["matched_text"]
    assert links[0]["exact_match"] is True

