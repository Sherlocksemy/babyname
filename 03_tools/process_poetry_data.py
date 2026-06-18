#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Normalize selected chinese-poetry data for naming origins."""

from __future__ import annotations

import json
import re
import gzip
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "00_raw_repos" / "03_culture" / "chinese-poetry-master"
OUT_DIR = ROOT / "01_knowledge_base" / "04_culture_origin_layer"
COMPLIANCE = ROOT / "01_knowledge_base" / "01_compliance_layer" / "tongyong_guifan_hanzi.csv"
GUSHIWEN_GZ = ROOT / "00_raw_repos" / "07_github_supplement" / "yht050511-gushiwen" / "gushiwen.json.gz"
GUSHIWEN_INDEX = ROOT / "00_raw_repos" / "07_github_supplement" / "yht050511-gushiwen" / "translation_index.json"
NIUTRANS_DIR = ROOT / "00_raw_repos" / "07_github_supplement" / "NiuTrans-Classical-Modern-bilingual"
_OPENCC = None

KEYWORDS = ["君子", "清雅", "志向", "温润", "明德", "嘉美", "安宁", "山水", "芳草", "星月", "仁义", "贤德", "高洁"]
POSITIVE_CHARS = set("嘉佳令明清安宁乐悦欣怡雅君子文德仁义礼智信贤良瑞祥泽宇轩宸星月云山水林竹兰芳华")
_WHITELIST: set[str] | None = None


def simp(text: str) -> str:
    global _OPENCC
    try:
        if _OPENCC is None:
            from opencc import OpenCC

            _OPENCC = OpenCC("t2s")
        return _OPENCC.convert(text)
    except Exception:
        return text


def clean_html(text: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"&nbsp;?", " ", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return simp(text).strip()


def load_whitelist() -> set[str]:
    global _WHITELIST
    if _WHITELIST is not None:
        return _WHITELIST
    chars: set[str] = set()
    if COMPLIANCE.exists():
        import csv

        with COMPLIANCE.open("r", encoding="utf-8", newline="") as f:
            chars = {row["char"] for row in csv.DictReader(f)}
    _WHITELIST = chars
    return chars


def extract_translation_from_sons(sons) -> str:
    if not isinstance(sons, dict):
        return ""
    for key in ["译文及注释", "译文", "翻译", "译文及注释二"]:
        node = sons.get(key)
        if isinstance(node, dict):
            content = clean_html(str(node.get("content", "") or ""))
            if not content:
                continue
            marker = content.find("注释")
            if marker > 0:
                content = content[:marker].strip()
            content = re.sub(r"^译文\s*", "", content).strip()
            if content:
                return content
    return ""


def load_translation_index() -> dict[tuple[str, str], str]:
    index: dict[tuple[str, str], str] = {}
    if GUSHIWEN_INDEX.exists() and (not GUSHIWEN_GZ.exists() or GUSHIWEN_INDEX.stat().st_mtime >= GUSHIWEN_GZ.stat().st_mtime):
        raw = json.loads(GUSHIWEN_INDEX.read_text(encoding="utf-8"))
        return {(item["title"], item["author"]): item["translation"] for item in raw}
    if not GUSHIWEN_GZ.exists():
        return index
    title_counts: dict[str, int] = {}
    records: list[tuple[str, str, str]] = []
    with gzip.open(GUSHIWEN_GZ, "rt", encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        title = simp(str(item.get("title", "") or "")).strip()
        author = simp(str(item.get("author", "") or "")).strip()
        translation = extract_translation_from_sons(item.get("sons"))
        if not title or not translation:
            continue
        records.append((title, author, translation))
        title_counts[title] = title_counts.get(title, 0) + 1
    for title, author, translation in records:
        index.setdefault((title, author), translation)
        if title_counts.get(title) == 1:
            index.setdefault((title, ""), translation)
    GUSHIWEN_INDEX.write_text(
        json.dumps([{"title": k[0], "author": k[1], "translation": v} for k, v in index.items()], ensure_ascii=False, indent=2),
        encoding="utf-8",
        newline="\n",
    )
    return index


def read_niutrans_targets(folder: Path) -> str:
    lines: list[str] = []
    for path in sorted(folder.rglob("target.txt")):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8-sig", errors="ignore")
        for line in text.splitlines():
            line = simp(line).strip()
            if line:
                lines.append(line)
    return "\n".join(lines)


def load_niutrans_classics() -> dict[tuple[str, str], str]:
    index: dict[tuple[str, str], str] = {}
    if not NIUTRANS_DIR.exists():
        return index

    for title, dirname in [("大学", "大学章句集注"), ("中庸", "中庸")]:
        text = read_niutrans_targets(NIUTRANS_DIR / dirname)
        if text:
            index[(title, "")] = text

    lunyu_dir = NIUTRANS_DIR / "论语"
    if lunyu_dir.exists():
        for chapter_dir in sorted(p for p in lunyu_dir.iterdir() if p.is_dir()):
            text = read_niutrans_targets(chapter_dir)
            if text:
                index[(chapter_dir.name, "")] = text

    mengzi_dir = NIUTRANS_DIR / "孟子"
    if mengzi_dir.exists():
        for chapter_dir in sorted(p for p in mengzi_dir.iterdir() if p.is_dir()):
            text = read_niutrans_targets(chapter_dir)
            if text:
                title = chapter_dir.name.replace("章句", "")
                index[(title, "")] = text
    return index


def content_text(item: dict) -> str:
    content = item.get("content", "")
    if isinstance(content, list):
        return "\n".join(str(x) for x in content)
    if isinstance(content, str) and content.strip():
        return content
    paragraphs = item.get("paragraphs", "")
    if isinstance(paragraphs, list):
        return "\n".join(str(x) for x in paragraphs)
    return str(paragraphs or "")


def tag_keywords(text: str) -> list[str]:
    tags = [k for k in KEYWORDS if k in text]
    if any(c in text for c in "兰芳芷蕙草木"):
        tags.append("芳草")
    if any(c in text for c in "山水江河云月星"):
        tags.append("山水")
    if any(c in text for c in "志德贤君仁义"):
        tags.append("志向")
    if not tags:
        tags.extend(["文学出处", "清雅"])
        if any(c in text for c in "志德贤君仁义明"):
            tags.append("志向")
        if any(c in text for c in "风月云山水花"):
            tags.append("山水")
    return sorted(set(tags))[:6]


def candidates(text: str) -> list[str]:
    whitelist = load_whitelist()
    clean = re.sub(r"[^\u4e00-\u9fff]", "", text)
    scores: dict[str, int] = {}
    for i in range(max(0, len(clean) - 1)):
        word = clean[i : i + 2]
        if whitelist and any(c not in whitelist for c in word):
            continue
        if len(word) == 2 and any(c in POSITIVE_CHARS for c in word):
            scores[word] = scores.get(word, 0) + sum(1 for c in word if c in POSITIVE_CHARS)
    result = [w for w, _ in sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))[:3]]
    if len(result) >= 2:
        return result[:3]
    for i in range(max(0, len(clean) - 1)):
        word = clean[i : i + 2]
        if word in result:
            continue
        if whitelist and any(c not in whitelist for c in word):
            continue
        result.append(word)
        if len(result) >= 3:
            break
    return result or ["文雅"]


def normalize_items(items: list[dict], dynasty: str, default_author: str = "", chapter_name: str = "", translations: dict[tuple[str, str], str] | None = None) -> list[dict]:
    out = []
    for idx, item in enumerate(items, start=1):
        text = simp(content_text(item)).strip()
        if not text:
            continue
        title = simp(str(item.get("title") or item.get("rhythmic") or item.get("chapter") or chapter_name or ""))
        author = simp(str(item.get("author") or default_author or "佚名"))
        chapter = simp(str(item.get("chapter") or item.get("section") or item.get("rhythmic") or chapter_name or ""))
        if not chapter and dynasty == "唐":
            chapter = "全唐诗精选"
        translation = ""
        if translations:
            translation = translations.get((title, author), "") or translations.get((title, ""), "")
        out.append(
            {
                "id": f"{dynasty}-{idx:06d}",
                "title": title,
                "author": author,
                "dynasty": dynasty,
                "chapter": chapter,
                "content": text,
                "translation": translation,
                "keywords": tag_keywords(text),
                "name_candidates": candidates(text),
            }
        )
    return out


def read_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(rel: str, data: list[dict]) -> None:
    path = OUT_DIR / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")


def load_many(folder: Path, pattern: str, limit: int | None = None) -> list[dict]:
    data: list[dict] = []
    for path in sorted(folder.glob(pattern)):
        if path.name.startswith("author"):
            continue
        part = read_json(path)
        if isinstance(part, list):
            data.extend(part)
        if limit and len(data) >= limit:
            break
    return data[:limit] if limit else data


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    translations = load_translation_index()
    translations.update(load_niutrans_classics())
    shijing = normalize_items(read_json(RAW / "诗经" / "shijing.json"), "先秦", default_author="佚名", translations=translations)
    chuci = normalize_items(read_json(RAW / "楚辞" / "chuci.json"), "战国", translations=translations)
    tang = normalize_items(load_many(RAW / "全唐诗", "poet.tang.*.json", limit=3000), "唐", translations=translations)
    song_ci = normalize_items(load_many(RAW / "宋词", "ci.song.*.json", limit=3000), "宋", translations=translations)
    classics_raw = []
    for path in [RAW / "四书五经" / "daxue.json", RAW / "四书五经" / "zhongyong.json", RAW / "四书五经" / "mengzi.json", RAW / "论语" / "lunyu.json"]:
        if path.exists():
            data = read_json(path)
            classics_raw.extend(data if isinstance(data, list) else [data])
    classics = normalize_items(classics_raw, "先秦", chapter_name="四书五经", translations=translations)
    write_json("shijing/shijing_full.json", shijing)
    write_json("chuci/chuci_full.json", chuci)
    write_json("tang_poetry/tang_poetry.json", tang)
    write_json("song_ci/song_ci.json", song_ci)
    write_json("sishuwujing/sishuwujing.json", classics)
    readme = f"""# 文化出处层

本目录按诗经、楚辞、唐诗、宋词、四书五经分层保存可追溯文化出处。

## 统一字段

`id` 唯一编号；`title` 篇名；`author` 作者；`dynasty` 朝代；`chapter` 章节/分类；`content` 原文；`translation` 白话译文，源缺失时留空；`keywords` 取名意象关键词；`name_candidates` 从原文启发式提取的 2-3 个双字词组。

## 处理规范

使用 OpenCC 将繁体尽量转为简体；无 OpenCC 环境时保留原文。唐诗、宋词源数据体量极大，本层输出取前 3000 条作为“精选”基础集，后续可按评分策略扩展。唐诗来源限定为 `poet.tang.*.json`，避免误读同目录宋诗文件。
非译文字段采用规则兜底：关键词缺失时使用文学出处/清雅等通用标签，候选名缺失时从合规白名单汉字组成的双字窗口补齐，唐诗无章节时统一标注为“全唐诗精选”。译文字段仅使用可追溯来源，不做机器生成；真实来源缺失时保留空值并由审计报告统计。

## 数据来源

- `00_raw_repos/03_culture/chinese-poetry-master/诗经/shijing.json`
- `00_raw_repos/03_culture/chinese-poetry-master/楚辞/chuci.json`
- `00_raw_repos/03_culture/chinese-poetry-master/全唐诗/`
- `00_raw_repos/03_culture/chinese-poetry-master/宋词/`
- `00_raw_repos/03_culture/chinese-poetry-master/四书五经/`、`论语/`
- 译文补充源：`00_raw_repos/07_github_supplement/yht050511-gushiwen/gushiwen.json.gz`，按标题/作者匹配，字段来自 `sons.译文及注释`。
- 四书译文补充源：GitHub `NiuTrans/Classical-Modern` 的 `双语数据/大学章句集注`、`双语数据/中庸`、`双语数据/孟子`、`双语数据/论语`，本地缓存于 `00_raw_repos/07_github_supplement/NiuTrans-Classical-Modern-bilingual/`。
- 提取时间：{datetime.now().isoformat(timespec="seconds")}.
"""
    (OUT_DIR / "README.md").write_text(readme, encoding="utf-8", newline="\n")
    print(f"Wrote {OUT_DIR}")


if __name__ == "__main__":
    main()
