#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate generated knowledge-base files."""

from __future__ import annotations

import csv
import json
import argparse
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "01_knowledge_base"

REQUIRED = [
    KB / "01_compliance_layer" / "tongyong_guifan_hanzi.csv",
    KB / "01_compliance_layer" / "README.md",
    KB / "02_char_attribute_layer" / "char_base_info.csv",
    KB / "02_char_attribute_layer" / "kangxi_strokes.json",
    KB / "02_char_attribute_layer" / "char_semantic.json",
    KB / "02_char_attribute_layer" / "README.md",
    KB / "03_pronunciation_layer" / "mandarin_pinyin.json",
    KB / "03_pronunciation_layer" / "teochew_pronunciation.csv",
    KB / "03_pronunciation_layer" / "homophone_blacklist.csv",
    KB / "03_pronunciation_layer" / "README.md",
    KB / "04_culture_origin_layer" / "shijing" / "shijing_full.json",
    KB / "04_culture_origin_layer" / "chuci" / "chuci_full.json",
    KB / "04_culture_origin_layer" / "tang_poetry" / "tang_poetry.json",
    KB / "04_culture_origin_layer" / "song_ci" / "song_ci.json",
    KB / "04_culture_origin_layer" / "sishuwujing" / "sishuwujing.json",
    KB / "04_culture_origin_layer" / "README.md",
    KB / "05_name_popularity_layer" / "char_frequency.csv",
    KB / "05_name_popularity_layer" / "top_names_blacklist.csv",
    KB / "05_name_popularity_layer" / "README.md",
    KB / "06_numerology_layer" / "bazi_rules.json",
    KB / "06_numerology_layer" / "zodiac_taboo.csv",
    KB / "06_numerology_layer" / "wuge_rules.json",
    KB / "06_numerology_layer" / "README.md",
]
AUDIT_REPORT = KB / "build_audit_report.json"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def assert_unique(rows: list[dict[str, str]], keys: list[str], path: Path) -> None:
    seen = set()
    for idx, row in enumerate(rows, start=2):
        key = tuple(row.get(k, "") for k in keys)
        if key in seen:
            raise ValueError(f"Duplicate key {key} in {path} line {idx}")
        seen.add(key)


def blank(value) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict, tuple, set)):
        return len(value) == 0
    return False


def count_blank_mapping(data: dict, fields: list[str]) -> dict[str, int]:
    return {field: sum(1 for item in data.values() if blank(item.get(field))) for field in fields}


def count_blank_items(data: list[dict], fields: list[str]) -> dict[str, int]:
    return {field: sum(1 for item in data if blank(item.get(field))) for field in fields}


def write_audit(report: dict) -> None:
    AUDIT_REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="Require all non-translation business fields to be complete.")
    args = parser.parse_args(argv)

    report: dict[str, object] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "strict": args.strict,
        "missing_counts": {},
    }
    missing = [p for p in REQUIRED if not p.exists()]
    if missing:
        raise FileNotFoundError("Missing required outputs:\n" + "\n".join(str(p) for p in missing))
    whitelist_rows = read_csv(KB / "01_compliance_layer" / "tongyong_guifan_hanzi.csv")
    whitelist = {row["char"] for row in whitelist_rows}
    if len(whitelist_rows) != 8105 or len(whitelist) != 8105:
        raise ValueError("Compliance CSV must contain exactly 8105 unique characters")
    for row in whitelist_rows:
        if len(row["char"]) != 1 or row["unicode"] != f"U+{ord(row['char']):04X}":
            raise ValueError(f"Invalid compliance row: {row}")
        for field in ["radical", "strokes_modern"]:
            if not row.get(field, "").strip():
                raise ValueError(f"Compliance row has blank {field}: {row}")
    char_base = read_csv(KB / "02_char_attribute_layer" / "char_base_info.csv")
    if len(char_base) != 8105 or any(row["char"] not in whitelist for row in char_base):
        raise ValueError("char_base_info.csv must contain only and all whitelist characters")
    assert_unique(char_base, ["char"], KB / "02_char_attribute_layer" / "char_base_info.csv")
    for row in char_base:
        for field in ["pinyin_main", "strokes_modern", "radical", "structure"]:
            if not row.get(field, "").strip():
                raise ValueError(f"char_base_info.csv has blank {field}: {row}")
    for json_path in [
        KB / "02_char_attribute_layer" / "kangxi_strokes.json",
        KB / "02_char_attribute_layer" / "char_semantic.json",
        KB / "03_pronunciation_layer" / "mandarin_pinyin.json",
    ]:
        data = json.loads(json_path.read_text(encoding="utf-8"))
        if set(data.keys()) != whitelist:
            raise ValueError(f"{json_path} keys must equal compliance whitelist")

    kangxi = json.loads((KB / "02_char_attribute_layer" / "kangxi_strokes.json").read_text(encoding="utf-8"))
    semantic = json.loads((KB / "02_char_attribute_layer" / "char_semantic.json").read_text(encoding="utf-8"))
    report["missing_counts"]["kangxi_strokes.json"] = count_blank_mapping(kangxi, ["kangxi_strokes", "kangxi_radical", "element", "components"])
    report["missing_counts"]["char_semantic.json"] = count_blank_mapping(semantic, ["definition", "ancient_meaning", "positive_level", "common_level"])
    for filename, counts in report["missing_counts"].items():
        if filename in {"kangxi_strokes.json", "char_semantic.json"}:
            nonzero = {k: v for k, v in counts.items() if v}
            if nonzero:
                raise ValueError(f"{filename} has blank required fields: {nonzero}")
    for csv_path, keys in [
        (KB / "03_pronunciation_layer" / "teochew_pronunciation.csv", ["char", "pinyin_teochew", "accent"]),
        (KB / "03_pronunciation_layer" / "homophone_blacklist.csv", ["char", "homophone_char", "language_type"]),
        (KB / "05_name_popularity_layer" / "char_frequency.csv", ["char"]),
        (KB / "05_name_popularity_layer" / "top_names_blacklist.csv", ["name", "gender"]),
    ]:
        rows = read_csv(csv_path)
        assert_unique(rows, keys, csv_path)
        for row in rows:
            chars = row.get("char", "") or row.get("name", "")
            for ch in chars:
                if "\u4e00" <= ch <= "\u9fff" and ch not in whitelist:
                    raise ValueError(f"{csv_path} contains non-whitelist character {ch}: {row}")
    for json_path in [p for p in REQUIRED if p.suffix == ".json"]:
        data = json.loads(json_path.read_text(encoding="utf-8"))
        if "04_culture_origin_layer" in str(json_path) and not data:
            raise ValueError(f"{json_path} must not be empty")
        if "04_culture_origin_layer" in str(json_path):
            counts = count_blank_items(data, ["translation", "keywords", "name_candidates", "chapter"])
            report["missing_counts"][str(json_path.relative_to(KB))] = counts
            non_translation = {k: v for k, v in counts.items() if k != "translation" and v}
            if non_translation:
                raise ValueError(f"{json_path} has blank non-translation fields: {non_translation}")
            if args.strict:
                for item in data:
                    for field in ["id", "title", "author", "dynasty", "chapter", "content", "keywords", "name_candidates"]:
                        if blank(item.get(field)):
                            raise ValueError(f"{json_path} has blank strict field {field}: {item.get('id', '')}")
    write_audit(report)
    print("Validation passed.")


if __name__ == "__main__":
    main()
