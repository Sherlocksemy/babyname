from __future__ import annotations

from app.catalogs.name_char_catalog_builder import ensure_name_char_catalog


def test_semantic_role_mapper_assigns_expected_categories() -> None:
    records = ensure_name_char_catalog()["records_by_char"]

    assert "WISDOM" in records["知"]["semantic_categories"]
    assert "WISDOM" in records["微"]["semantic_categories"]
    assert records["知"]["semantic_roles"]

