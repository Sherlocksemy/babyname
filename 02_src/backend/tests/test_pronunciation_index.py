from __future__ import annotations

from backend.app.indexes.pronunciation_index import PronunciationIndex


def test_pronunciation_index_returns_mandarin_polyphone() -> None:
    index = PronunciationIndex()
    readings = index.get("行")["mandarin"]

    assert len(readings) >= 2
    assert {item["tone"] for item in readings}


def test_pronunciation_index_has_teochew_multi_reading_data() -> None:
    index = PronunciationIndex()
    multi_rows = next(rows for rows in index.teochew.values() if len(rows) > 1)

    assert multi_rows
    assert {"accent", "is_colloquial", "is_literary"}.issubset(multi_rows[0].keys())
