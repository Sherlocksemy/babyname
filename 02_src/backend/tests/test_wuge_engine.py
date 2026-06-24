from __future__ import annotations

from app.engines.wuge_engine import WugeEngine


def test_single_surname_double_given_wuge() -> None:
    result = WugeEngine().calculate("林", "思敬")
    assert result["tiange"] == 9
    assert result["renge"] == 17
    assert result["dige"] == 21
    assert result["zongge"] == 29
    assert result["interpretation_status"] == "DATA_INCOMPLETE"
    assert result["numerology_interpretation"] is None


def test_double_surname_double_given_wuge() -> None:
    result = WugeEngine().calculate("欧阳", "贤庭")
    assert result["surname_strokes"] == [8, 11]
    assert result["given_name_strokes"]
    assert result["status"] == "COMPLETE"

