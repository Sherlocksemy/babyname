from __future__ import annotations

from app.catalogs.name_char_catalog_builder import ensure_name_char_catalog


def test_core_records_do_not_carry_polyphonic_risk() -> None:
    records = ensure_name_char_catalog()["records"]
    risky = [
        record["char"]
        for record in records
        if record["nameability_level"] == "CORE"
        and ("POLYPHONE" in record.get("risk_codes", []) or len(record.get("mandarin") or []) > 1)
    ]

    assert risky == []

