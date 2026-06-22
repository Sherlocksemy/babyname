from __future__ import annotations

from backend.app.indexes.popularity_index import PopularityIndex


def test_popularity_index_reads_hot_chars() -> None:
    index = PopularityIndex()

    assert index.hot_chars()
    assert index.get_char("英")["heat_level"] == "爆款"


def test_popularity_index_blacklist_query() -> None:
    index = PopularityIndex()

    assert index.is_blacklisted("秀英") is True
    assert index.get_name("秀英") is not None
