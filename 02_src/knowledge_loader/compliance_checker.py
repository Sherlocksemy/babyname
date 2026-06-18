#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""合规准入层加载器。

本模块只读取 01_compliance_layer，不访问其他知识库分层。
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


class ComplianceChecker:
    """通用规范汉字表白名单校验工具。"""

    def __init__(self, project_root: str | Path | None = None) -> None:
        self.project_root = Path(project_root) if project_root else Path(__file__).resolve().parents[2]
        self.data_path = self.project_root / "01_knowledge_base" / "01_compliance_layer" / "tongyong_guifan_hanzi.csv"
        self._loaded = False
        self._chars: dict[str, dict] = {}

    def reload(self) -> dict:
        """清空缓存并重新加载。"""
        self._loaded = False
        self._chars = {}
        return self._load()

    def _load(self) -> dict:
        """懒加载合规白名单。"""
        if self._loaded:
            return {"ok": True, "count": len(self._chars)}
        try:
            if not self.data_path.exists():
                return {"ok": False, "error": f"合规数据文件不存在: {self.data_path}"}
            with self.data_path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                required = {"char", "level", "strokes_modern", "radical", "unicode"}
                if not required.issubset(set(reader.fieldnames or [])):
                    return {"ok": False, "error": f"合规数据字段缺失，应包含: {sorted(required)}"}
                for row in reader:
                    ch = row.get("char", "").strip()
                    if len(ch) != 1:
                        continue
                    self._chars[ch] = {
                        "char": ch,
                        "level": int(row["level"]) if row.get("level", "").isdigit() else None,
                        "strokes_modern": int(row["strokes_modern"]) if row.get("strokes_modern", "").isdigit() else None,
                        "radical": row.get("radical", ""),
                        "unicode": row.get("unicode", ""),
                    }
            self._loaded = True
            return {"ok": True, "count": len(self._chars)}
        except Exception as exc:
            return {"ok": False, "error": f"加载合规数据失败: {exc}"}

    def health_check(self) -> dict:
        """返回模块健康状态。"""
        result = self._load()
        result.update({"layer": "01_compliance_layer", "path": str(self.data_path)})
        return result

    def is_allowed_char(self, char: str) -> dict:
        """判断单字是否可用于户籍登记。"""
        try:
            if not char or len(char) != 1:
                return {"ok": False, "allowed": False, "error": "请输入单个汉字"}
            loaded = self._load()
            if not loaded["ok"]:
                return {**loaded, "allowed": False}
            info = self._chars.get(char)
            return {"ok": True, "char": char, "allowed": info is not None, "info": info}
        except Exception as exc:
            return {"ok": False, "allowed": False, "error": f"合规校验失败: {exc}"}

    def get_level(self, char: str) -> dict:
        """查询规范等级，返回 1/2/3 或 None。"""
        result = self.is_allowed_char(char)
        if not result.get("ok") or not result.get("allowed"):
            return {**result, "level": None}
        return {"ok": True, "char": char, "level": result["info"].get("level"), "info": result["info"]}

    def filter_allowed_chars(self, chars: Iterable[str]) -> dict:
        """批量过滤违规字。"""
        try:
            loaded = self._load()
            if not loaded["ok"]:
                return {**loaded, "allowed_chars": [], "blocked_chars": []}
            allowed, blocked = [], []
            for ch in chars:
                if ch in self._chars:
                    allowed.append(ch)
                else:
                    blocked.append(ch)
            return {"ok": True, "allowed_chars": allowed, "blocked_chars": blocked}
        except Exception as exc:
            return {"ok": False, "allowed_chars": [], "blocked_chars": [], "error": f"批量过滤失败: {exc}"}

    def validate_name(self, name: str) -> dict:
        """校验姓名中所有汉字是否都在白名单内。"""
        if not name:
            return {"ok": False, "valid": False, "error": "姓名不能为空"}
        result = self.filter_allowed_chars([ch for ch in name if "\u4e00" <= ch <= "\u9fff"])
        if not result.get("ok"):
            return {**result, "valid": False}
        return {
            "ok": True,
            "valid": len(result["blocked_chars"]) == 0,
            "name": name,
            "blocked_chars": result["blocked_chars"],
        }

    def all_chars(self) -> list[str]:
        """返回全部合规字。"""
        self._load()
        return list(self._chars.keys())


if __name__ == "__main__":
    checker = ComplianceChecker()
    print(checker.health_check())
    print(checker.is_allowed_char("明"))
    print(checker.validate_name("张明泽"))
