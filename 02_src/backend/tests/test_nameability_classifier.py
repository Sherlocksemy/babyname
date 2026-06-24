from __future__ import annotations

from app.catalogs.name_char_catalog_builder import ensure_name_char_catalog


def test_nameability_classifier_rejects_obvious_unsuitable_char() -> None:
    record = ensure_name_char_catalog()["records_by_char"]["乂"]

    assert record["nameability_level"] == "REJECTED"
    assert "UNSUITABLE_FUNCTION_CHAR" in record["risk_codes"]

