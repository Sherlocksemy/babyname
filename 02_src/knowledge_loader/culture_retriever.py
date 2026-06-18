#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文化出处层加载器。

本模块只读取 04_culture_origin_layer，不访问其他知识库分层。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


class CultureRetriever:
    """诗经、楚辞、唐诗、宋词、四书五经出处检索工具。"""

    CATEGORY_FILES = {
        "shijing": "shijing/shijing_full.json",
        "chuci": "chuci/chuci_full.json",
        "tang_poetry": "tang_poetry/tang_poetry.json",
        "song_ci": "song_ci/song_ci.json",
        "sishuwujing": "sishuwujing/sishuwujing.json",
    }

    def __init__(self, project_root: str | Path | None = None) -> None:
        self.project_root = Path(project_root) if project_root else Path(__file__).resolve().parents[2]
        self.layer_dir = self.project_root / "01_knowledge_base" / "04_culture_origin_layer"
        self._loaded = False
        self._items: list[dict] = []
        self._by_category: dict[str, list[dict]] = {}
        self._char_index: dict[str, list[dict]] = {}

    def reload(self) -> dict:
        """清空缓存并重新加载。"""
        self._loaded = False
        self._items = []
        self._by_category = {}
        self._char_index = {}
        return self._load()

    def _load(self) -> dict:
        """懒加载所有文化出处文件并建立单字倒排索引。"""
        if self._loaded:
            return {"ok": True, "count": len(self._items)}
        try:
            if not self.layer_dir.exists():
                return {"ok": False, "error": f"文化出处目录不存在: {self.layer_dir}"}
            for category, rel_path in self.CATEGORY_FILES.items():
                path = self.layer_dir / rel_path
                if not path.exists():
                    return {"ok": False, "error": f"文化出处文件不存在: {path}"}
                data = json.loads(path.read_text(encoding="utf-8"))
                rows = []
                for item in data:
                    normalized = dict(item)
                    normalized["category"] = category
                    rows.append(normalized)
                    self._items.append(normalized)
                    for ch in set(normalized.get("content", "") + "".join(normalized.get("name_candidates", []))):
                        if "\u4e00" <= ch <= "\u9fff":
                            self._char_index.setdefault(ch, []).append(normalized)
                self._by_category[category] = rows
            self._loaded = True
            return {"ok": True, "count": len(self._items)}
        except Exception as exc:
            return {"ok": False, "error": f"加载文化出处失败: {exc}"}

    def health_check(self) -> dict:
        """返回模块健康状态。"""
        result = self._load()
        result.update({"layer": "04_culture_origin_layer", "path": str(self.layer_dir)})
        return result

    def search_by_char(self, char: str, categories: Iterable[str] | None = None, limit: int = 20) -> dict:
        """通过汉字反向匹配诗词原文和候选名。"""
        try:
            loaded = self._load()
            if not loaded["ok"]:
                return {**loaded, "items": []}
            category_set = set(categories or [])
            rows = self._char_index.get(char, [])
            if category_set:
                rows = [row for row in rows if row.get("category") in category_set]
            return {"ok": True, "char": char, "count": len(rows[:limit]), "items": rows[:limit]}
        except Exception as exc:
            return {"ok": False, "items": [], "error": f"文化检索失败: {exc}"}

    def get_keywords(self, chars: Iterable[str]) -> dict:
        """汇总一组汉字相关的意象标签。"""
        try:
            loaded = self._load()
            if not loaded["ok"]:
                return {**loaded, "keywords": []}
            scores: dict[str, int] = {}
            for ch in chars:
                for item in self._char_index.get(ch, [])[:50]:
                    for keyword in item.get("keywords", []):
                        scores[keyword] = scores.get(keyword, 0) + 1
            keywords = [k for k, _ in sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))[:10]]
            return {"ok": True, "keywords": keywords}
        except Exception as exc:
            return {"ok": False, "keywords": [], "error": f"意象提取失败: {exc}"}

    def get_name_origins(self, name: str, preference: str | None = None, limit: int = 5) -> dict:
        """为姓名生成出处文案，优先匹配完整名字，其次匹配单字。"""
        try:
            loaded = self._load()
            if not loaded["ok"]:
                return {**loaded, "origins": [], "score": 0}
            given = name[-2:] if len(name) >= 2 else name
            scored = []
            for item in self._items:
                if preference and item.get("category") != preference:
                    continue
                content = item.get("content", "")
                candidates = item.get("name_candidates", [])
                hit = 0
                if given in content or given in candidates:
                    hit += 5
                hit += sum(1 for ch in given if ch in content)
                if hit <= 0:
                    continue
                scored.append((hit, item))
            scored.sort(key=lambda pair: (-pair[0], pair[1].get("id", "")))
            origins = [self._format_origin(item, hit) for hit, item in scored[:limit]]
            score = min(100, 55 + (scored[0][0] * 8 if scored else 0))
            return {"ok": True, "name": name, "score": score if origins else 45, "origins": origins}
        except Exception as exc:
            return {"ok": False, "origins": [], "score": 0, "error": f"出处生成失败: {exc}"}

    @staticmethod
    def _format_origin(item: dict, hit: int) -> dict:
        text = item.get("content", "").replace("\n", " ")
        return {
            "title": item.get("title", ""),
            "author": item.get("author", ""),
            "dynasty": item.get("dynasty", ""),
            "category": item.get("category", ""),
            "chapter": item.get("chapter", ""),
            "keywords": item.get("keywords", []),
            "quote": text[:120],
            "translation": item.get("translation", "")[:160],
            "match_strength": hit,
        }


if __name__ == "__main__":
    retriever = CultureRetriever()
    print(retriever.health_check())
    print(retriever.search_by_char("明", categories=["shijing"], limit=2))
    print(retriever.get_name_origins("明泽", preference="shijing"))
