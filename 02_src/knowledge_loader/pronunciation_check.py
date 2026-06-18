#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""读音音律层加载器。

本模块只读取 03_pronunciation_layer，不访问其他知识库分层。
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


class PronunciationChecker:
    """普通话、潮汕话、平仄和谐音风险检测工具。"""

    PING_TONES = {1, 2}
    ZE_TONES = {3, 4}

    def __init__(self, project_root: str | Path | None = None) -> None:
        self.project_root = Path(project_root) if project_root else Path(__file__).resolve().parents[2]
        self.layer_dir = self.project_root / "01_knowledge_base" / "03_pronunciation_layer"
        self.mandarin_path = self.layer_dir / "mandarin_pinyin.json"
        self.teochew_path = self.layer_dir / "teochew_pronunciation.csv"
        self.blacklist_path = self.layer_dir / "homophone_blacklist.csv"
        self._loaded = False
        self._mandarin: dict[str, list[dict]] = {}
        self._teochew: dict[str, list[dict]] = {}
        self._blacklist: dict[str, list[dict]] = {}

    def reload(self) -> dict:
        """清空缓存并重新加载。"""
        self._loaded = False
        self._mandarin = {}
        self._teochew = {}
        self._blacklist = {}
        return self._load()

    def _load(self) -> dict:
        """懒加载读音层三份数据。"""
        if self._loaded:
            return {"ok": True, "mandarin": len(self._mandarin), "teochew": len(self._teochew)}
        try:
            for path in [self.mandarin_path, self.teochew_path, self.blacklist_path]:
                if not path.exists():
                    return {"ok": False, "error": f"读音数据文件不存在: {path}"}
            self._mandarin = json.loads(self.mandarin_path.read_text(encoding="utf-8"))

            with self.teochew_path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ch = row.get("char", "")
                    if len(ch) == 1:
                        self._teochew.setdefault(ch, []).append(row)

            with self.blacklist_path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ch = row.get("char", "")
                    if len(ch) == 1:
                        self._blacklist.setdefault(ch, []).append(row)

            self._loaded = True
            return {"ok": True, "mandarin": len(self._mandarin), "teochew": len(self._teochew)}
        except Exception as exc:
            return {"ok": False, "error": f"加载读音数据失败: {exc}"}

    def health_check(self) -> dict:
        """返回模块健康状态。"""
        result = self._load()
        result.update({"layer": "03_pronunciation_layer", "path": str(self.layer_dir)})
        return result

    def get_mandarin(self, char: str) -> dict:
        """获取单字普通话读音列表。"""
        try:
            loaded = self._load()
            if not loaded["ok"]:
                return {**loaded, "readings": []}
            return {"ok": True, "char": char, "readings": self._mandarin.get(char, [])}
        except Exception as exc:
            return {"ok": False, "readings": [], "error": f"查询普通话读音失败: {exc}"}

    def get_teochew(self, char: str, accent: str | None = None) -> dict:
        """获取单字潮汕话读音，可按口音过滤。"""
        try:
            loaded = self._load()
            if not loaded["ok"]:
                return {**loaded, "readings": []}
            rows = self._teochew.get(char, [])
            if accent:
                rows = [row for row in rows if row.get("accent") == accent]
            return {"ok": True, "char": char, "accent": accent, "readings": rows}
        except Exception as exc:
            return {"ok": False, "readings": [], "error": f"查询潮汕话读音失败: {exc}"}

    def get_tone_pattern(self, name: str) -> dict:
        """返回普通话平仄结构。"""
        try:
            loaded = self._load()
            if not loaded["ok"]:
                return {**loaded, "pattern": []}
            pattern = []
            for ch in name:
                readings = self._mandarin.get(ch, [])
                tone = readings[0].get("tone") if readings else 0
                if tone in self.PING_TONES:
                    label = "平"
                elif tone in self.ZE_TONES:
                    label = "仄"
                else:
                    label = "轻"
                pattern.append({"char": ch, "tone": tone, "label": label})
            return {"ok": True, "name": name, "pattern": pattern}
        except Exception as exc:
            return {"ok": False, "pattern": [], "error": f"平仄判断失败: {exc}"}

    def check_homophone(self, name: str, include_teochew: bool = True) -> dict:
        """检查普通话和潮汕话谐音黑名单。"""
        try:
            loaded = self._load()
            if not loaded["ok"]:
                return {**loaded, "safe": False, "issues": []}
            issues = []
            for ch in name:
                for item in self._blacklist.get(ch, []):
                    if include_teochew or item.get("language_type") == "mandarin":
                        issues.append(item)
            return {"ok": True, "name": name, "safe": len(issues) == 0, "issues": issues}
        except Exception as exc:
            return {"ok": False, "safe": False, "issues": [], "error": f"谐音检测失败: {exc}"}

    def score_pronunciation(self, name: str, include_teochew: bool = True) -> dict:
        """根据平仄变化和谐音风险给读音评分。"""
        tone_result = self.get_tone_pattern(name)
        homo_result = self.check_homophone(name, include_teochew=include_teochew)
        if not tone_result.get("ok") or not homo_result.get("ok"):
            return {"ok": False, "score": 0, "error": tone_result.get("error") or homo_result.get("error")}

        labels = [item["label"] for item in tone_result["pattern"]]
        score = 80
        reasons = []
        if len(set(labels)) > 1:
            score += 10
            reasons.append("平仄有变化")
        else:
            score -= 8
            reasons.append("平仄略单一")
        if not homo_result["safe"]:
            score -= min(40, len(homo_result["issues"]) * 15)
            reasons.append("存在谐音风险")
        else:
            reasons.append("未命中谐音黑名单")
        return {
            "ok": True,
            "name": name,
            "score": max(0, min(score, 100)),
            "tone_pattern": tone_result["pattern"],
            "homophone": homo_result,
            "reasons": reasons,
        }


if __name__ == "__main__":
    checker = PronunciationChecker()
    print(checker.health_check())
    print(checker.get_mandarin("明"))
    print(checker.score_pronunciation("明泽"))
