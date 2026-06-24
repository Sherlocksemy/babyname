from __future__ import annotations

from app.catalogs.name_char_catalog_builder import ensure_name_char_catalog


def test_core_records_have_semantic_roles() -> None:
    records = ensure_name_char_catalog()["records"]
    missing = [record["char"] for record in records if record["nameability_level"] == "CORE" and not record.get("semantic_roles")]

    assert missing == []

