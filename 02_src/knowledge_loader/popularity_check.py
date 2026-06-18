#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""姓名流行度层加载器。

本模块只读取 05_name_popularity_layer，不访问其他知识库分层。
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


class PopularityChecker:
    """单字热度、爆款姓名和重名风险检测工具。"""

    HEAT_SCORE = {"极低": 100, "低": 88, "中": 72, "高": 52, "爆款": 20}
    HEAT_ORDER = {"极低": 0, "低": 1, "中": 2, "高": 3, "爆款": 4}

    def __init__(self, project_root: str | Path | None = None) -> None:
        self.project_root = Path(project_root) if project_root else Path(__file__).resolve().parents[2]
        self.layer_dir = self.project_root / "01_knowledge_base" / "05_name_popularity_layer"
        self.char_path = self.layer_dir / "char_frequency.csv"
        self.name_path = self.layer_dir / "top_names_blacklist.csv"
        self._loaded = False
        self._char_freq: dict[str, dict] = {}
        self._hot_names: dict[str, dict] = {}

    def reload(self) -> dict:
        """清空缓存并重新加载。"""
        self._loaded = False
        self._char_freq = {}
        self._hot_names = {}
        return self._load()

    def _load(self) -> dict:
        """懒加载热度数据。"""
        if self._loaded:
            return {"ok": True, "chars": len(self._char_freq), "names": len(self._hot_names)}
        try:
            for path in [self.char_path, self.name_path]:
                if not path.exists():
                    return {"ok": False, "error": f"流行度数据文件不存在: {path}"}
            with self.char_path.open("r", encoding="utf-8", newline="") as f:
                for row in csv.DictReader(f):
                    ch = row.get("char", "")
                    if len(ch) == 1:
                        row["frequency_rank"] = self._to_int(row.get("frequency_rank")) or 999999
                        self._char_freq[ch] = row
            with self.name_path.open("r", encoding="utf-8", newline="") as f:
                for row in csv.DictReader(f):
                    name = row.get("name", "")
                    if name:
                        row["estimated_count"] = self._to_int(row.get("estimated_count")) or 0
                        self._hot_names[name] = row
            self._loaded = True
            return {"ok": True, "chars": len(self._char_freq), "names": len(self._hot_names)}
        except Exception as exc:
            return {"ok": False, "error": f"加载流行度数据失败: {exc}"}

    @staticmethod
    def _to_int(value) -> int | None:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def health_check(self) -> dict:
        """返回模块健康状态。"""
        result = self._load()
        result.update({"layer": "05_name_popularity_layer", "path": str(self.layer_dir)})
        return result

    def get_char_heat(self, char: str) -> dict:
        """查询单字取名热度。"""
        try:
            loaded = self._load()
            if not loaded["ok"]:
                return {**loaded, "data": None}
            data = self._char_freq.get(char)
            if not data:
                return {"ok": True, "exists": False, "char": char, "heat_level": "低", "score": 88, "data": None}
            score = self.HEAT_SCORE.get(data.get("heat_level", "中"), 72)
            return {"ok": True, "exists": True, "char": char, "heat_level": data.get("heat_level"), "score": score, "data": data}
        except Exception as exc:
            return {"ok": False, "data": None, "error": f"查询单字热度失败: {exc}"}

    def is_hot_name(self, name: str) -> dict:
        """判断名字是否在爆款黑名单内。"""
        try:
            loaded = self._load()
            if not loaded["ok"]:
                return {**loaded, "is_hot": False}
            data = self._hot_names.get(name)
            return {"ok": True, "name": name, "is_hot": data is not None, "data": data}
        except Exception as exc:
            return {"ok": False, "is_hot": False, "error": f"爆款姓名判断失败: {exc}"}

    def filter_by_heat(self, chars: Iterable[str], max_heat: str = "高") -> dict:
        """过滤超过热度上限的候选字。"""
        try:
            allowed, blocked = [], []
            max_order = self.HEAT_ORDER.get(max_heat, 3)
            for ch in chars:
                heat = self.get_char_heat(ch)
                level = heat.get("heat_level", "低")
                if self.HEAT_ORDER.get(level, 1) <= max_order:
                    allowed.append(ch)
                else:
                    blocked.append({"char": ch, "heat_level": level})
            return {"ok": True, "allowed_chars": allowed, "blocked": blocked}
        except Exception as exc:
            return {"ok": False, "allowed_chars": [], "blocked": [], "error": f"热度过滤失败: {exc}"}

    def score_name(self, name: str, max_heat: str = "高") -> dict:
        """根据单字热度和爆款黑名单给姓名评分。"""
        hot = self.is_hot_name(name)
        if not hot.get("ok"):
            return {"ok": False, "score": 0, "error": hot.get("error")}
        score = 90
        reasons = []
        if hot["is_hot"]:
            score -= 45
            reasons.append("命中爆款姓名黑名单")
        for ch in name:
            heat = self.get_char_heat(ch)
            score = min(score, heat.get("score", 88))
            reasons.append(f"{ch} 热度 {heat.get('heat_level', '低')}")
        if self.HEAT_ORDER.get(max_heat, 3) < 4 and hot["is_hot"]:
            reasons.append(f"超过热度限制 {max_heat}")
        return {"ok": True, "name": name, "score": max(0, score), "is_hot": hot["is_hot"], "reasons": reasons}


if __name__ == "__main__":
    checker = PopularityChecker()
    print(checker.health_check())
    print(checker.get_char_heat("英"))
    print(checker.score_name("明泽"))
