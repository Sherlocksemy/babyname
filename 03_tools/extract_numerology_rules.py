#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build numerology and bazi rule layer."""

from __future__ import annotations

import ast
import csv
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "00_raw_repos" / "05_numerology"
OUT_DIR = ROOT / "01_knowledge_base" / "06_numerology_layer"
BAZI_DATAS = RAW / "bazi-master" / "datas.py"
ZODIAC_SHU = RAW / "fate-main" / "docs" / "zodiac_shu.md"
GITHUB_ZODIAC_DIR = ROOT / "00_raw_repos" / "07_github_supplement" / "johnwu1114-chinese-name"
COMPLIANCE = ROOT / "01_knowledge_base" / "01_compliance_layer" / "tongyong_guifan_hanzi.csv"

TEN_GODS = {
    "比肩": "与日主同五行同阴阳，代表自我、同辈、竞争。",
    "劫财": "与日主同五行异阴阳，代表竞争、分财、行动力。",
    "食神": "日主所生且同阴阳，代表表达、才艺、福气。",
    "伤官": "日主所生且异阴阳，代表才华、突破、反叛。",
    "偏财": "日主所克且同阴阳，代表机会财、经营。",
    "正财": "日主所克且异阴阳，代表稳定财、责任。",
    "七杀": "克日主且同阴阳，代表压力、权威、挑战。",
    "正官": "克日主且异阴阳，代表规则、职位、名誉。",
    "偏印": "生日主且同阴阳，代表偏门知识、保护。",
    "正印": "生日主且异阴阳，代表学业、贵人、资源。",
}

PATTERNS = {
    "正官格": {"condition": "月令主气为正官，且官星清透有根", "notes": "忌伤官强破，宜印星护官。"},
    "七杀格": {"condition": "月令主气为七杀，杀星有制或化", "notes": "有食神制杀或印化杀为佳。"},
    "正财格": {"condition": "月令主气为正财，财星得令不混杂", "notes": "宜身旺能任财。"},
    "食神格": {"condition": "月令主气为食神，食神清透", "notes": "忌偏印夺食。"},
}
ELEMENT_RULES = {
    "旺衰": "以月令为核心，结合天干透出、地支通根、季节得令综合判定。",
    "通根": "天干五行在地支藏干中出现同类或生扶，即视为有根。",
    "透干": "地支藏干对应五行在天干出现，视为透出。",
}
USHEN_RULES = {
    "basic": "先判日主强弱，再取扶抑、调候、通关为主要用神方向。",
    "avoid": "忌神为破坏平衡、加重偏枯或冲克关键用神的五行与十神。",
}
ELEMENT_BY_RADICAL = {
    "木": "木", "艹": "木", "竹": "木", "禾": "木",
    "火": "火", "灬": "火", "日": "火",
    "土": "土", "山": "土", "石": "土", "田": "土",
    "金": "金", "钅": "金", "刀": "金", "刂": "金", "玉": "金", "王": "金",
    "水": "水", "氵": "水", "冫": "水", "雨": "水",
}


def simplify(text: str) -> str:
    try:
        from opencc import OpenCC

        return OpenCC("t2s").convert(text)
    except Exception:
        return text


def load_char_radicals() -> dict[str, str]:
    if not COMPLIANCE.exists():
        return {}
    with COMPLIANCE.open("r", encoding="utf-8", newline="") as f:
        return {row["char"]: row.get("radical", "") for row in csv.DictReader(f)}


def flatten_stroke_groups(groups: dict) -> list[str]:
    chars: list[str] = []
    for key in sorted(groups.keys(), key=lambda k: int(k.strip("_")) if k.strip("_").isdigit() else 999):
        for ch in groups.get(key) or []:
            sch = simplify(str(ch))
            if len(sch) == 1 and sch not in chars:
                chars.append(sch)
    return chars


def top_radicals(chars: list[str], radical_map: dict[str, str]) -> list[str]:
    counts: dict[str, int] = {}
    for ch in chars:
        radical = radical_map.get(ch, "")
        if radical:
            counts[radical] = counts.get(radical, 0) + 1
    return [r for r, _ in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:24]]


def safe_literal_dict(name: str) -> dict:
    text = BAZI_DATAS.read_text(encoding="utf-8")
    m = re.search(rf"^{name}\s*=\s*(\{{.*?\n\}})", text, flags=re.S | re.M)
    if not m:
        return {}
    try:
        return ast.literal_eval(m.group(1))
    except Exception:
        return {}


def parse_zodiac() -> list[dict[str, str]]:
    animals = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
    if GITHUB_ZODIAC_DIR.exists():
        radical_map = load_char_radicals()
        rows = []
        for path in sorted(GITHUB_ZODIAC_DIR.glob("*_*.json")):
            if path.name in {"ChineseCharacters.json", "EightyOne.json", "Sancai.json"}:
                continue
            data = json.loads(path.read_text(encoding="utf-8-sig"))
            zodiac = simplify(str(data.get("type", "")))
            if zodiac not in animals:
                continue
            good_chars = flatten_stroke_groups(data.get("better") or {})
            bad_chars = flatten_stroke_groups(data.get("worse") or {})
            good_radicals = top_radicals(good_chars, radical_map)
            bad_radicals = top_radicals(bad_chars, radical_map)
            lucky_elements = sorted({ELEMENT_BY_RADICAL[r] for r in good_radicals if r in ELEMENT_BY_RADICAL})
            rows.append(
                {
                    "zodiac": zodiac,
                    "good_radicals": ",".join(good_radicals),
                    "bad_radicals": ",".join(bad_radicals),
                    "good_meaning": "由 johnwu1114/chinese-name 十二生肖 better 字库派生；原仓库按笔画列宜用字，本字段汇总部首。",
                    "bad_meaning": "由 johnwu1114/chinese-name 十二生肖 worse 字库派生；原仓库按笔画列忌用字，本字段汇总部首。",
                    "lucky_elements": ",".join(lucky_elements),
                }
            )
        rows.sort(key=lambda row: animals.index(row["zodiac"]))
        if len(rows) == 12:
            return rows
    text = ZODIAC_SHU.read_text(encoding="utf-8") if ZODIAC_SHU.exists() else ""
    rows = []
    for animal in animals:
        good_radicals = []
        bad_radicals = []
        if animal == "鼠":
            good_radicals = re.findall(r"「([^」]{1,4})」", text.split("属鼠的人不适合的字")[0])[:20]
            bad_radicals = re.findall(r"「([^」]{1,4})」", text.split("属鼠的人不适合的字")[-1])[:20]
        rows.append(
            {
                "zodiac": animal,
                "good_radicals": ",".join(good_radicals),
                "bad_radicals": ",".join(bad_radicals),
                "good_meaning": "按 fate-main 生肖姓名学文档抽取；源文档未覆盖的生肖留空待补。",
                "bad_meaning": "按 fate-main 生肖姓名学文档抽取；源文档未覆盖的生肖留空待补。",
                "lucky_elements": "",
            }
        )
    return rows


def stroke_math() -> dict[str, dict[str, str]]:
    lucky = {1, 3, 5, 6, 7, 8, 11, 13, 15, 16, 17, 18, 21, 23, 24, 25, 29, 31, 32, 33, 35, 37, 39, 41, 45, 47, 48, 52, 57, 61, 63, 65, 67, 68, 81}
    half = {26, 27, 30, 38, 40, 42, 43, 49, 50, 51, 53, 55, 58, 71, 73, 75, 77, 78, 80}
    out = {}
    for i in range(1, 82):
        level = "吉" if i in lucky else "半吉" if i in half else "凶"
        out[str(i)] = {"luck": level, "meaning": f"五格 81 数理第 {i} 数，{level}。"}
    return out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    bazi = {
        "ten_gods": TEN_GODS,
        "patterns": PATTERNS,
        "element_rules": ELEMENT_RULES,
        "ushen_rules": USHEN_RULES,
        "source_tables": {
            "nayins": {str(k): v for k, v in safe_literal_dict("nayins").items()},
            "empties": {str(k): v for k, v in safe_literal_dict("empties").items()},
        },
    }
    (OUT_DIR / "bazi_rules.json").write_text(json.dumps(bazi, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    with (OUT_DIR / "zodiac_taboo.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["zodiac", "good_radicals", "bad_radicals", "good_meaning", "bad_meaning", "lucky_elements"])
        writer.writeheader()
        writer.writerows(parse_zodiac())
    wuge = {
        "stroke_math": stroke_math(),
        "sancai_config": {"rule": "三才按天格、人格、地格个位数映射五行，再判断生克关系；具体流派差异保留为可配置表。"},
        "calculate_rules": {
            "single_surname_single_given": "天格=姓氏康熙笔画+1；人格=姓+名；地格=名+1；外格=2；总格=姓+名。",
            "single_surname_double_given": "天格=姓+1；人格=姓+名一；地格=名一+名二；外格=名二+1；总格=全名。",
            "double_surname_single_given": "天格=复姓两字；人格=复姓第二字+名；地格=名+1；外格=复姓第一字+1；总格=全名。",
            "double_surname_double_given": "天格=复姓两字；人格=复姓第二字+名一；地格=名一+名二；外格=复姓第一字+名二；总格=全名。",
        },
    }
    (OUT_DIR / "wuge_rules.json").write_text(json.dumps(wuge, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    readme = f"""# 命理规则层

本目录保存八字、生肖、五格规则的结构化配置。规则只做数据化存储，不写死业务计算逻辑，便于后续按流派调整。

## 文件说明

- `bazi_rules.json`: 十神定义、常见格局、五行旺衰/通根/透干、用神忌神基础判定，以及 bazi-master 中纳音、空亡等源表。
- `zodiac_taboo.csv`: 12 生肖全覆盖；当前 `fate-main/docs/zodiac_shu.md` 仅明确提供鼠的详细宜忌，其余生肖保留空字段待补源。
- `zodiac_taboo.csv`: 12 生肖全覆盖；优先使用 `johnwu1114/chinese-name` 的 12 个生肖 JSON，将 better/worse 宜忌字库派生为部首与五行；若缺源则回退到 `fate-main/docs/zodiac_shu.md`。
- `wuge_rules.json`: 81 数理、三才配置占位规则、天格/人格/地格/外格/总格计算规则。

## 数据来源

- `00_raw_repos/05_numerology/bazi-master/datas.py`
- `00_raw_repos/05_numerology/pyLunarCalendar-master/`
- `00_raw_repos/05_numerology/fate-main/docs/zodiac_shu.md`
- `00_raw_repos/07_github_supplement/johnwu1114-chinese-name/*_*.json`
- 提取时间：{datetime.now().isoformat(timespec="seconds")}.
"""
    (OUT_DIR / "README.md").write_text(readme, encoding="utf-8", newline="\n")
    print(f"Wrote {OUT_DIR}")


if __name__ == "__main__":
    main()
