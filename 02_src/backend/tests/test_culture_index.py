from __future__ import annotations

from backend.app.indexes.culture_index import CultureIndex


def test_culture_index_reads_records_and_titles() -> None:
    index = CultureIndex()

    assert index.records
    assert index.by_title("关雎")
    assert index.by_source("shijing")


def test_culture_index_supports_char_keyword_and_bigram_queries() -> None:
    index = CultureIndex()

    assert index.by_char("知")
    assert index.by_keyword("君子")
    assert index.by_bigram("君子")
