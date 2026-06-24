from __future__ import annotations

from pathlib import Path


def test_semantic_validator_has_no_legacy_char_info_table() -> None:
    text = Path("02_src/backend/app/engines/semantic_composition_validator.py").read_text(encoding="utf-8")

    assert "CHAR_INFO" not in text

