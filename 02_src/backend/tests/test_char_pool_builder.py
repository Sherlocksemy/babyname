from __future__ import annotations

from app.engines.char_pool_builder import UNSUITABLE_CHARS


def test_char_pool_builder_excludes_obvious_unsuitable_chars(alpha_result) -> None:
    pools = alpha_result["char_pool_counts"]

    assert pools["first_pool"] <= 80
    assert pools["second_pool"] <= 80
    assert "乂" in UNSUITABLE_CHARS


def test_generated_names_do_not_use_unsuitable_chars(alpha_result) -> None:
    names = [item["given_name"] for item in alpha_result["top20"]]
    hard_unsuitable = set("乂乜儿几卜么乎哉矣焉")

    assert names
    assert not any(any(char in hard_unsuitable for char in name) for name in names)
