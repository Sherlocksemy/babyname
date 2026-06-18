#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""汉字全属性层加载器。

本模块只读取 02_char_attribute_layer，不访问其他知识库分层。
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable


class CharQuery:
    """汉字基础属性、语义、康熙笔画和五行查询工具。"""

    def __init__(self, project_root: str | Path | None = None) -> None:
        self.project_root = Path(project_root) if project_root else Path(__file__).resolve().parents[2]
        self.layer_dir = self.project_root / "01_knowledge_base" / "02_char_attribute_layer"
        self.base_path = self.layer_dir / "char_base_info.csv"
        self.kangxi_path = self.layer_dir / "kangxi_strokes.json"
        self.semantic_path = self.layer_dir / "char_semantic.json"
        self._loaded = False
        self._chars: dict[str, dict] = {}

    def reload(self) -> dict:
        """清空缓存并重新加载。"""
        self._loaded = False
        self._chars = {}
        return self._load()

    def _load(self) -> dict:
        """懒加载并合并三份汉字属性数据。"""
        if self._loaded:
            return {"ok": True, "count": len(self._chars)}
        try:
            for path in [self.base_path, self.kangxi_path, self.semantic_path]:
                if not path.exists():
                    return {"ok": False, "error": f"汉字属性数据文件不存在: {path}"}

            with self.kangxi_path.open("r", encoding="utf-8") as f:
                kangxi = json.load(f)
            with self.semantic_path.open("r", encoding="utf-8") as f:
                semantic = json.load(f)
            with self.base_path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                required = {"char", "pinyin_main", "strokes_modern", "radical", "structure", "wubi"}
                if not required.issubset(set(reader.fieldnames or [])):
                    return {"ok": False, "error": f"char_base_info.csv 字段缺失，应包含: {sorted(required)}"}
                for row in reader:
                    ch = row.get("char", "").strip()
                    if len(ch) != 1:
                        continue
                    k = kangxi.get(ch, {})
                    s = semantic.get(ch, {})
                    self._chars[ch] = {
                        "char": ch,
                        "pinyin_main": row.get("pinyin_main", ""),
                        "strokes_modern": self._to_int(row.get("strokes_modern")),
                        "radical": row.get("radical", ""),
                        "structure": row.get("structure", ""),
                        "wubi": row.get("wubi", ""),
                        "kangxi_strokes": self._to_int(k.get("kangxi_strokes")),
                        "kangxi_radical": k.get("kangxi_radical", ""),
                        "element": k.get("element", ""),
                        "components": k.get("components", []),
                        "definition": s.get("definition", ""),
                        "positive_level": self._to_int(s.get("positive_level")) or 0,
                        "common_level": self._to_int(s.get("common_level")) or 3,
                        "ancient_meaning": s.get("ancient_meaning", ""),
                    }
            self._loaded = True
            return {"ok": True, "count": len(self._chars)}
        except Exception as exc:
            return {"ok": False, "error": f"加载汉字属性失败: {exc}"}

    @staticmethod
    def _to_int(value) -> int | None:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def health_check(self) -> dict:
        """返回模块健康状态。"""
        result = self._load()
        result.update({"layer": "02_char_attribute_layer", "path": str(self.layer_dir)})
        return result

    def get_char(self, char: str) -> dict:
        """查询单字完整属性。"""
        try:
            if not char or len(char) != 1:
                return {"ok": False, "exists": False, "error": "请输入单个汉字"}
            loaded = self._load()
            if not loaded["ok"]:
                return {**loaded, "exists": False}
            info = self._chars.get(char)
            return {"ok": True, "exists": info is not None, "char": char, "data": info}
        except Exception as exc:
            return {"ok": False, "exists": False, "error": f"查询汉字失败: {exc}"}

    def filter_chars(
        self,
        elements: Iterable[str] | None = None,
        strokes: Iterable[int] | None = None,
        radicals: Iterable[str] | None = None,
        positive_min: int = 1,
        common_max: int = 3,
        limit: int | None = None,
    ) -> dict:
        """按五行、笔画、部首、褒义等级批量筛选汉字。"""
        try:
            loaded = self._load()
            if not loaded["ok"]:
                return {**loaded, "chars": []}
            element_set = set(elements or [])
            stroke_set = set(strokes or [])
            radical_set = set(radicals or [])
            result = []
            for item in self._chars.values():
                if element_set and item["element"] not in element_set:
                    continue
                if stroke_set and item["kangxi_strokes"] not in stroke_set and item["strokes_modern"] not in stroke_set:
                    continue
                if radical_set and item["radical"] not in radical_set and item["kangxi_radical"] not in radical_set:
                    continue
                if item["positive_level"] < positive_min or item["common_level"] > common_max:
                    continue
                result.append(item)
                if limit and len(result) >= limit:
                    break
            return {"ok": True, "count": len(result), "chars": result}
        except Exception as exc:
            return {"ok": False, "chars": [], "error": f"筛选汉字失败: {exc}"}

    def score_char(self, char: str, preferred_elements: Iterable[str] | None = None) -> dict:
        """按褒义、常用度、五行偏好给单字评分。"""
        result = self.get_char(char)
        if not result.get("ok") or not result.get("exists"):
            return {**result, "score": 0}
        data = result["data"]
        score = data["positive_level"] * 12 + (4 - data["common_level"]) * 8
        reasons = [f"褒义等级 {data['positive_level']}", f"常用度 {data['common_level']}"]
        if preferred_elements and data["element"] in set(preferred_elements):
            score += 20
            reasons.append(f"五行匹配 {data['element']}")
        return {"ok": True, "char": char, "score": min(score, 100), "reasons": reasons, "data": data}

    def all_chars(self) -> list[str]:
        """返回全部可查询字。"""
        self._load()
        return list(self._chars.keys())


if __name__ == "__main__":
    query = CharQuery()
    print(query.health_check())
    print(query.get_char("明"))
    print(query.filter_chars(elements=["水"], positive_min=4, limit=3))
