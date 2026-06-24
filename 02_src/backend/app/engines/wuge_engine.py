from __future__ import annotations

import json
from pathlib import Path

from app.core.config import KNOWLEDGE_BASE_DIR


class WugeEngine:
    def __init__(self, knowledge_base_dir: str | Path = KNOWLEDGE_BASE_DIR) -> None:
        base = Path(knowledge_base_dir)
        self.kangxi = json.loads((base / "02_char_attribute_layer" / "kangxi_strokes.json").read_text(encoding="utf-8"))
        self.rules = json.loads((base / "06_numerology_layer" / "wuge_rules.json").read_text(encoding="utf-8"))

    def calculate(self, surname: str, given_name: str) -> dict:
        surname_strokes = [self._stroke(char) for char in surname]
        given_strokes = [self._stroke(char) for char in given_name]
        warnings = []
        if any(value is None for value in surname_strokes + given_strokes):
            warnings.append("KANGXI_STROKE_MISSING")
            return {
                "surname_strokes": surname_strokes,
                "given_name_strokes": given_strokes,
                "status": "PARTIAL",
                "warnings": warnings,
            }
        s = surname_strokes
        g = given_strokes
        if len(s) == 1 and len(g) == 1:
            tiange, renge, dige, waige, zongge = s[0] + 1, s[0] + g[0], g[0] + 1, 2, s[0] + g[0]
        elif len(s) == 1:
            tiange, renge, dige, waige, zongge = s[0] + 1, s[0] + g[0], g[0] + g[1], g[1] + 1, s[0] + sum(g)
        elif len(g) == 1:
            tiange, renge, dige, waige, zongge = sum(s), s[-1] + g[0], g[0] + 1, s[0] + 1, sum(s) + g[0]
        else:
            tiange, renge, dige, waige, zongge = sum(s), s[-1] + g[0], sum(g), s[0] + g[-1], sum(s) + sum(g)
        sancai = "".join(self._sancai_element(value) for value in [tiange, renge, dige])
        return {
            "surname_strokes": s,
            "given_name_strokes": g,
            "tiange": tiange,
            "renge": renge,
            "dige": dige,
            "waige": waige,
            "zongge": zongge,
            "sancai": sancai,
            "stroke_source": "KANGXI",
            "numerology_interpretation": None,
            "interpretation_status": "DATA_INCOMPLETE",
            "status": "COMPLETE",
            "warnings": ["WUGE_INTERPRETATION_DATA_INCOMPLETE"],
        }

    def _stroke(self, char: str) -> int | None:
        item = self.kangxi.get(char)
        if not item:
            return None
        return int(item.get("kangxi_strokes") or 0) or None

    @staticmethod
    def _sancai_element(value: int) -> str:
        return {1: "木", 2: "木", 3: "火", 4: "火", 5: "土", 6: "土", 7: "金", 8: "金", 9: "水", 0: "水"}[value % 10]

