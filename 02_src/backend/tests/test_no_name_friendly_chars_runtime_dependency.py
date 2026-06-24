from __future__ import annotations

from pathlib import Path


def test_char_pool_has_no_legacy_name_friendly_runtime_dependency() -> None:
    text = Path("02_src/backend/app/engines/char_pool_builder.py").read_text(encoding="utf-8")

    assert "NAME_FRIENDLY_CHARS" not in text

