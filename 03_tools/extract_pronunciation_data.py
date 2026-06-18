#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build Mandarin and Teochew pronunciation data."""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "00_raw_repos"
COMPLIANCE = ROOT / "01_knowledge_base" / "01_compliance_layer" / "tongyong_guifan_hanzi.csv"
OUT_DIR = ROOT / "01_knowledge_base" / "03_pronunciation_layer"
PINYIN_ALL = RAW / "02_pronunciation" / "pinyin-data-master" / "pinyin.txt"
PINYIN_COMMON = RAW / "02_pronunciation" / "pinyin-data-master" / "kMandarin_8105.txt"
DIEGHV = RAW / "02_pronunciation" / "dieghv-master"

ACCENTS = {
    "dieziu": "潮州",
    "suantau": "汕头",
    "dioion": "潮阳",
    "gekion": "揭阳",
    "tenghai": "澄海",
    "riaupeng": "饶平",
}
TONE_RE = re.compile(r"[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]")
TONE_MAP = {c: n for n, chars in enumerate(["", "āēīōūǖ", "áéíóúǘ", "ǎěǐǒǔǚ", "àèìòùǜ"], start=0) for c in chars}
BAD_CHARS = set("病死亡丧凶恶灾祸孤寡穷苦哭毒残贼仇怨鬼")
BAD_MEANING = {ch: "常见负面语义字，取名谐音需避让" for ch in BAD_CHARS}
RHYME_GROUPS = [
    ("一啊", set("aiauanian")),
    ("二喔", set("oouongiong")),
    ("三鹅", set("eieer")),
    ("四衣", set("iyuü")),
    ("五乌", set("u")),
    ("六迂", set("vü")),
    ("七哀", set("aiuai")),
    ("八欸", set("eiui")),
    ("九熬", set("aoiao")),
    ("十欧", set("ouiu")),
    ("十一安", set("aneninunün")),
    ("十二恩", set("en")),
    ("十三昂", set("angengiingong")),
]


def load_whitelist() -> set[str]:
    with COMPLIANCE.open("r", encoding="utf-8", newline="") as f:
        return {row["char"] for row in csv.DictReader(f)}


def tone_of(pinyin: str) -> int:
    for ch in pinyin:
        if ch in TONE_MAP:
            return TONE_MAP[ch]
    return 0


def rhyme_of(pinyin: str) -> str:
    plain = (
        pinyin.translate(str.maketrans("āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü", "aaaaeeeeiiiioooouuuuvvvvv"))
        .replace("zh", "")
        .replace("ch", "")
        .replace("sh", "")
    )
    plain = re.sub(r"^[bpmfdtnlgkhjqxrzcsyw]+", "", plain)
    for name, finals in RHYME_GROUPS:
        if plain in finals or any(plain.endswith(x) for x in finals):
            return name
    return ""


def parse_pinyin_file(path: Path, whitelist: set[str]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = defaultdict(list)
    pat = re.compile(r"^U\+([0-9A-F]{4,5}):\s*([^#]+)")
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            m = pat.match(line.strip())
            if not m:
                continue
            ch = chr(int(m.group(1), 16))
            if ch not in whitelist:
                continue
            for py in [x.strip() for x in m.group(2).split(",") if x.strip()]:
                if py not in out[ch]:
                    out[ch].append(py)
    return out


def parse_teochew(whitelist: set[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for key, accent in ACCENTS.items():
        path = DIEGHV / f"{key}.dict.yaml"
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "\t" not in line:
                    continue
                parts = line.split("\t")
                if len(parts) < 2:
                    continue
                ch, reading = parts[0].strip(), parts[1].strip()
                if len(ch) != 1 or ch not in whitelist:
                    continue
                tone = "".join(re.findall(r"\d+", reading))
                rows.append(
                    {
                        "char": ch,
                        "pinyin_teochew": reading,
                        "tone": tone,
                        "accent": accent,
                        "is_colloquial": any(mark in line for mark in ["白", "colloquial"]),
                        "is_literary": any(mark in line for mark in ["文", "literary"]),
                    }
                )
    rows.sort(key=lambda r: (r["char"], r["accent"], r["pinyin_teochew"]))
    dedup = []
    seen = set()
    for row in rows:
        key = tuple(row.items())
        if key not in seen:
            seen.add(key)
            dedup.append(row)
    return dedup


def build_blacklist(mandarin: dict[str, list[dict]], teochew_rows: list[dict[str, object]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    by_py: dict[str, list[str]] = defaultdict(list)
    for ch, readings in mandarin.items():
        for item in readings:
            by_py[item["pinyin"]].append(ch)
    for chars in by_py.values():
        bad = [c for c in chars if c in BAD_CHARS]
        for b in bad:
            for c in chars:
                if c != b:
                    rows.append({"char": c, "homophone_char": b, "bad_meaning": BAD_MEANING[b], "language_type": "mandarin"})
    by_tc: dict[tuple[str, str], list[str]] = defaultdict(list)
    for row in teochew_rows:
        by_tc[(str(row["accent"]), str(row["pinyin_teochew"]))].append(str(row["char"]))
    for chars in by_tc.values():
        bad = [c for c in chars if c in BAD_CHARS]
        for b in bad:
            for c in chars:
                if c != b:
                    rows.append({"char": c, "homophone_char": b, "bad_meaning": BAD_MEANING[b], "language_type": "teochew"})
    seen = set()
    uniq = []
    for row in rows:
        key = (row["char"], row["homophone_char"], row["language_type"])
        if key not in seen:
            seen.add(key)
            uniq.append(row)
    uniq.sort(key=lambda r: (r["language_type"], r["char"], r["homophone_char"]))
    return uniq


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    whitelist = load_whitelist()
    all_py = parse_pinyin_file(PINYIN_ALL, whitelist)
    common_py = parse_pinyin_file(PINYIN_COMMON, whitelist)
    mandarin: dict[str, list[dict[str, object]]] = {}
    for ch in sorted(whitelist):
        readings = all_py.get(ch) or common_py.get(ch) or []
        common = set(common_py.get(ch, readings[:1]))
        mandarin[ch] = [{"pinyin": py, "tone": tone_of(py), "is_common": py in common, "rhyme": rhyme_of(py)} for py in readings]
    (OUT_DIR / "mandarin_pinyin.json").write_text(json.dumps(mandarin, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    tc_rows = parse_teochew(whitelist)
    with (OUT_DIR / "teochew_pronunciation.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["char", "pinyin_teochew", "tone", "accent", "is_colloquial", "is_literary"])
        writer.writeheader()
        writer.writerows(tc_rows)
    blacklist = build_blacklist(mandarin, tc_rows)
    with (OUT_DIR / "homophone_blacklist.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["char", "homophone_char", "bad_meaning", "language_type"])
        writer.writeheader()
        writer.writerows(blacklist)
    readme = f"""# 读音音律层

本目录保存普通话、潮汕话和谐音风险数据，所有单字均按合规层 8105 字过滤。

## 字段说明

- `mandarin_pinyin.json`: 键为汉字；`pinyin` 为带声调拼音；`tone` 为 1/2/3/4/0；`is_common` 标注 `kMandarin_8105.txt` 首选读音；`rhyme` 为中华通韵近似韵部。
- `teochew_pronunciation.csv`: `char` 汉字；`pinyin_teochew` 潮罗/字典读音；`tone` 调号；`accent` 潮阳/汕头/潮州/揭阳/澄海/饶平；文白读标记按源文件标注推断，源缺失则为 False。
- `homophone_blacklist.csv`: 由普通话与潮汕话同音分组生成，覆盖常见负面语义字的谐音风险。

## 数据来源

- `00_raw_repos/02_pronunciation/pinyin-data-master/pinyin.txt`
- `00_raw_repos/02_pronunciation/pinyin-data-master/kMandarin_8105.txt`
- `00_raw_repos/02_pronunciation/dieghv-master/*.dict.yaml`
- 提取时间：{datetime.now().isoformat(timespec="seconds")}.
"""
    (OUT_DIR / "README.md").write_text(readme, encoding="utf-8", newline="\n")
    print(f"Wrote {OUT_DIR}")


if __name__ == "__main__":
    main()
