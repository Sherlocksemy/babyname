#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""命理规则层加载器与近似计算工具。

本模块只读取 06_numerology_layer，不访问其他知识库分层。
八字排盘为标准库近似算法，结果会标注 calendar_accuracy=approximate。
"""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path


class NumerologyCalculator:
    """八字、生肖宜忌和五格数理计算工具。"""

    STEMS = "甲乙丙丁戊己庚辛壬癸"
    BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
    ZODIACS = "鼠牛虎兔龙蛇马羊猴鸡狗猪"
    STEM_ELEMENTS = {
        "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
        "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水",
    }
    BRANCH_ELEMENTS = {
        "子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火",
        "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水",
    }
    HOUR_BRANCHES = ["子", "丑", "丑", "寅", "寅", "卯", "卯", "辰", "辰", "巳", "巳", "午",
                     "午", "未", "未", "申", "申", "酉", "酉", "戌", "戌", "亥", "亥", "子"]
    ELEMENTS = ["木", "火", "土", "金", "水"]

    def __init__(self, project_root: str | Path | None = None) -> None:
        self.project_root = Path(project_root) if project_root else Path(__file__).resolve().parents[2]
        self.layer_dir = self.project_root / "01_knowledge_base" / "06_numerology_layer"
        self.bazi_path = self.layer_dir / "bazi_rules.json"
        self.zodiac_path = self.layer_dir / "zodiac_taboo.csv"
        self.wuge_path = self.layer_dir / "wuge_rules.json"
        self._loaded = False
        self._bazi_rules: dict = {}
        self._zodiac_rules: dict[str, dict] = {}
        self._wuge_rules: dict = {}

    def reload(self) -> dict:
        """清空缓存并重新加载。"""
        self._loaded = False
        self._bazi_rules = {}
        self._zodiac_rules = {}
        self._wuge_rules = {}
        return self._load()

    def _load(self) -> dict:
        """懒加载命理规则。"""
        if self._loaded:
            return {"ok": True, "zodiac_count": len(self._zodiac_rules)}
        try:
            for path in [self.bazi_path, self.zodiac_path, self.wuge_path]:
                if not path.exists():
                    return {"ok": False, "error": f"命理规则文件不存在: {path}"}
            self._bazi_rules = json.loads(self.bazi_path.read_text(encoding="utf-8"))
            self._wuge_rules = json.loads(self.wuge_path.read_text(encoding="utf-8"))
            with self.zodiac_path.open("r", encoding="utf-8", newline="") as f:
                for row in csv.DictReader(f):
                    zodiac = row.get("zodiac", "")
                    if zodiac:
                        row["good_radicals"] = [x for x in row.get("good_radicals", "").split(",") if x]
                        row["bad_radicals"] = [x for x in row.get("bad_radicals", "").split(",") if x]
                        row["lucky_elements"] = [x for x in row.get("lucky_elements", "").split(",") if x]
                        self._zodiac_rules[zodiac] = row
            self._loaded = True
            return {"ok": True, "zodiac_count": len(self._zodiac_rules)}
        except Exception as exc:
            return {"ok": False, "error": f"加载命理规则失败: {exc}"}

    def health_check(self) -> dict:
        """返回模块健康状态。"""
        result = self._load()
        result.update({"layer": "06_numerology_layer", "path": str(self.layer_dir)})
        return result

    def parse_birth_time(self, birth_time: str | datetime) -> dict:
        """解析出生时间，支持 datetime 或常见字符串格式。"""
        if isinstance(birth_time, datetime):
            return {"ok": True, "datetime": birth_time}
        if not isinstance(birth_time, str):
            return {"ok": False, "error": "出生时间必须是 datetime 或字符串"}
        for fmt in ["%Y-%m-%d %H:%M", "%Y-%m-%d %H", "%Y-%m-%d", "%Y/%m/%d %H:%M", "%Y/%m/%d"]:
            try:
                return {"ok": True, "datetime": datetime.strptime(birth_time, fmt)}
            except ValueError:
                continue
        return {"ok": False, "error": "Invalid birth datetime format，示例: 2024-05-20 09:30"}

    def calculate_bazi(self, birth_time: str | datetime) -> dict:
        """近似计算四柱八字。"""
        parsed = self.parse_birth_time(birth_time)
        if not parsed["ok"]:
            return {**parsed, "bazi": None}
        dt = parsed["datetime"]
        try:
            year_gz = self._ganzhi((dt.year - 4) % 60)
            month_gz = self._ganzhi(((dt.year - 4) * 12 + dt.month + 1) % 60)
            base = datetime(1900, 1, 31)
            day_gz = self._ganzhi((dt - base).days % 60)
            hour_branch = self.HOUR_BRANCHES[dt.hour]
            day_stem_index = self.STEMS.index(day_gz[0])
            hour_stem = self.STEMS[((day_stem_index % 5) * 2 + self.BRANCHES.index(hour_branch)) % 10]
            hour_gz = hour_stem + hour_branch
            pillars = {"year": year_gz, "month": month_gz, "day": day_gz, "hour": hour_gz}
            element_counts = self._count_elements(pillars)
            zodiac = self.ZODIACS[(dt.year - 4) % 12]
            return {
                "ok": True,
                "birth_time": dt.isoformat(sep=" ", timespec="minutes"),
                "bazi": pillars,
                "zodiac": zodiac,
                "element_counts": element_counts,
                "calendar_accuracy": "approximate",
                "warning": "标准库近似排盘，未按节气精确换年换月。",
            }
        except Exception as exc:
            return {"ok": False, "bazi": None, "error": f"八字计算失败: {exc}"}

    def _ganzhi(self, index: int) -> str:
        return self.STEMS[index % 10] + self.BRANCHES[index % 12]

    def _count_elements(self, pillars: dict[str, str]) -> dict[str, int]:
        counts = {e: 0 for e in self.ELEMENTS}
        for pillar in pillars.values():
            counts[self.STEM_ELEMENTS.get(pillar[0], "土")] += 1
            counts[self.BRANCH_ELEMENTS.get(pillar[1], "土")] += 1
        return counts

    def infer_favorable_elements(self, bazi_result: dict) -> dict:
        """根据五行计数粗略推断喜用五行。"""
        if not bazi_result.get("ok"):
            return {"ok": False, "elements": [], "error": bazi_result.get("error", "八字无效")}
        counts = bazi_result.get("element_counts", {})
        min_count = min(counts.values()) if counts else 0
        elements = [e for e, count in counts.items() if count == min_count]
        return {"ok": True, "elements": elements, "basis": "五行数量偏少者作为近似补益方向"}

    def match_zodiac(self, name_chars: list[dict], zodiac: str) -> dict:
        """根据生肖宜忌部首和五行匹配候选字。"""
        try:
            loaded = self._load()
            if not loaded["ok"]:
                return {**loaded, "score": 0}
            rule = self._zodiac_rules.get(zodiac)
            if not rule:
                return {"ok": True, "zodiac": zodiac, "score": 60, "details": [], "warning": "未找到生肖规则"}
            score = 70
            details = []
            for item in name_chars:
                radical = item.get("radical", "")
                element = item.get("element", "")
                if radical in rule["good_radicals"] or element in rule["lucky_elements"]:
                    score += 8
                    details.append(f"{item.get('char')} 匹配生肖宜用")
                if radical in rule["bad_radicals"]:
                    score -= 10
                    details.append(f"{item.get('char')} 命中生肖忌用部首")
            return {"ok": True, "zodiac": zodiac, "score": max(0, min(score, 100)), "details": details, "rule": rule}
        except Exception as exc:
            return {"ok": False, "score": 0, "error": f"生肖匹配失败: {exc}"}

    def calculate_wuge(self, surname: str, given_name: str, stroke_lookup: dict[str, int]) -> dict:
        """按单姓双字名为主计算五格数理。"""
        try:
            loaded = self._load()
            if not loaded["ok"]:
                return {**loaded, "score": 0}
            if not surname or not given_name:
                return {"ok": False, "score": 0, "error": "姓氏和名字不能为空"}
            surname_strokes = sum(stroke_lookup.get(ch, 1) for ch in surname)
            given_strokes = [stroke_lookup.get(ch, 1) for ch in given_name]
            first = given_strokes[0]
            second = given_strokes[1] if len(given_strokes) > 1 else 1
            tiange = surname_strokes + 1 if len(surname) == 1 else surname_strokes
            renge = stroke_lookup.get(surname[-1], 1) + first
            dige = sum(given_strokes) if len(given_name) > 1 else first + 1
            waige = second + 1 if len(surname) == 1 and len(given_name) > 1 else 1
            zongge = surname_strokes + sum(given_strokes)
            grids = {"天格": tiange, "人格": renge, "地格": dige, "外格": waige, "总格": zongge}
            math = self._wuge_rules.get("stroke_math", {})
            details = {k: math.get(str(v if v <= 81 else ((v - 1) % 81 + 1)), {}) for k, v in grids.items()}
            score = 50 + sum(10 for item in details.values() if item.get("luck") == "吉")
            score += sum(4 for item in details.values() if item.get("luck") == "半吉")
            return {"ok": True, "score": min(score, 100), "grids": grids, "details": details}
        except Exception as exc:
            return {"ok": False, "score": 0, "error": f"五格计算失败: {exc}"}

    def score_numerology(self, surname: str, given_name: str, birth_time: str | datetime, name_chars: list[dict]) -> dict:
        """综合八字、生肖和五格进行命理评分。"""
        bazi = self.calculate_bazi(birth_time)
        if not bazi.get("ok"):
            return {"ok": False, "score": 0, "error": bazi.get("error"), "bazi": bazi}
        favorable = self.infer_favorable_elements(bazi)
        zodiac = self.match_zodiac(name_chars, bazi["zodiac"])
        stroke_lookup = {item["char"]: item.get("kangxi_strokes") or item.get("strokes_modern") or 1 for item in name_chars}
        for ch in surname:
            stroke_lookup.setdefault(ch, 1)
        wuge = self.calculate_wuge(surname, given_name, stroke_lookup)
        element_hits = sum(1 for item in name_chars if item.get("element") in favorable.get("elements", []))
        score = 50 + element_hits * 10 + zodiac.get("score", 60) * 0.2 + wuge.get("score", 60) * 0.2
        return {
            "ok": True,
            "score": round(min(score, 100), 2),
            "bazi": bazi,
            "favorable_elements": favorable,
            "zodiac_match": zodiac,
            "wuge": wuge,
        }


if __name__ == "__main__":
    calc = NumerologyCalculator()
    print(calc.health_check())
    print(calc.calculate_bazi("2024-05-20 09:30"))
