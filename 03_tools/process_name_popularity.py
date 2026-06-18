#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build name popularity layer."""

from __future__ import annotations

import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "00_raw_repos" / "04_name_bigdata"
COMPLIANCE = ROOT / "01_knowledge_base" / "01_compliance_layer" / "tongyong_guifan_hanzi.csv"
OUT_DIR = ROOT / "01_knowledge_base" / "05_name_popularity_layer"
CHAR_YEAR = RAW / "ChineseNames-main" / "data-csv" / "top50char.year.csv"
NAME_YEAR = RAW / "ChineseNames-main" / "data-csv" / "top100name.year.csv"


def load_whitelist() -> set[str]:
    with COMPLIANCE.open("r", encoding="utf-8", newline="") as f:
        return {row["char"] for row in csv.DictReader(f)}


def heat(rank: int) -> str:
    if rank <= 20:
        return "爆款"
    if rank <= 100:
        return "高"
    if rank <= 300:
        return "中"
    if rank <= 1000:
        return "低"
    return "极低"


def era_from_col(col: str) -> str:
    year = col.rsplit(".", 1)[-1]
    return f"{year}后" if year.isdigit() else ""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    whitelist = load_whitelist()
    stats: dict[str, dict[str, object]] = defaultdict(lambda: {"count": 0, "m": 0, "f": 0, "eras": set()})
    with CHAR_YEAR.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            for key, value in row.items():
                if not key.startswith("char.") or not value or len(value) != 1 or value not in whitelist:
                    continue
                suffix = key.replace("char.", "")
                n_key = "n." + suffix
                n = int(float(row.get(n_key, "0") or 0))
                stats[value]["count"] = int(stats[value]["count"]) + n
                if ".m." in key:
                    stats[value]["m"] = int(stats[value]["m"]) + n
                elif ".f." in key:
                    stats[value]["f"] = int(stats[value]["f"]) + n
                stats[value]["eras"].add(era_from_col(key))
    ordered = sorted(stats.items(), key=lambda kv: (-int(kv[1]["count"]), kv[0]))
    char_rows = []
    for rank, (ch, item) in enumerate(ordered, start=1):
        m, f = int(item["m"]), int(item["f"])
        gender = "M" if m > f * 1.2 else "F" if f > m * 1.2 else "N"
        eras = sorted(e for e in item["eras"] if e)
        char_rows.append({"char": ch, "gender_tendency": gender, "frequency_rank": rank, "heat_level": heat(rank), "era_tag": "/".join(eras[-3:])})
    with (OUT_DIR / "char_frequency.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["char", "gender_tendency", "frequency_rank", "heat_level", "era_tag"])
        writer.writeheader()
        writer.writerows(char_rows)
    name_stats: dict[tuple[str, str], int] = defaultdict(int)
    with NAME_YEAR.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            for key, name in row.items():
                if not key.startswith("name.") or not name or len(name) > 3:
                    continue
                given = str(name)
                if not all(ch in whitelist for ch in given):
                    continue
                suffix = key.replace("name.", "")
                n = int(float(row.get("n." + suffix, "0") or 0))
                gender = "M" if ".m." in key else "F" if ".f." in key else "N"
                name_stats[(given, gender)] += n
    top_rows = []
    for rank, ((name, gender), count) in enumerate(sorted(name_stats.items(), key=lambda kv: (-kv[1], kv[0]))[:500], start=1):
        top_rows.append({"name": name, "gender": gender, "estimated_count": count, "heat_level": heat(rank)})
    with (OUT_DIR / "top_names_blacklist.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "gender", "estimated_count", "heat_level"])
        writer.writeheader()
        writer.writerows(top_rows)
    readme = f"""# 姓名流行度层

本目录基于公开姓名频次数据生成取名热度与爆款预警，所有单字均按通用规范汉字白名单过滤。

## 字段说明

- `char_frequency.csv`: `char` 单字；`gender_tendency` 性别倾向 M/F/N；`frequency_rank` 全国取名频次排名；`heat_level` 极低/低/中/高/爆款；`era_tag` 年代流行标签。
- `top_names_blacklist.csv`: `name` 高频名；`gender` 性别；`estimated_count` 源数据汇总估算人数级；`heat_level` 热度等级。

## 分级规范

排名 1-20 为爆款，21-100 为高，101-300 为中，301-1000 为低，其余为极低。性别倾向以男女频次 1.2 倍差异判定，未达到阈值为中性。

## 数据来源

- `00_raw_repos/04_name_bigdata/ChineseNames-main/data-csv/top50char.year.csv`
- `00_raw_repos/04_name_bigdata/ChineseNames-main/data-csv/top100name.year.csv`
- `00_raw_repos/04_name_bigdata/Chinese-Names-Corpus-master/` 作为辅助语料来源目录保留。
- 提取时间：{datetime.now().isoformat(timespec="seconds")}.
"""
    (OUT_DIR / "README.md").write_text(readme, encoding="utf-8", newline="\n")
    print(f"Wrote {OUT_DIR}")


if __name__ == "__main__":
    main()
