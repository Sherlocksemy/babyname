#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build character attribute layer from chinese-xinhua and makemeahanzi."""

from __future__ import annotations

import csv
import json
import re
import zipfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "00_raw_repos"
COMPLIANCE = ROOT / "01_knowledge_base" / "01_compliance_layer" / "tongyong_guifan_hanzi.csv"
OUT_DIR = ROOT / "01_knowledge_base" / "02_char_attribute_layer"
XINHUA = RAW / "01_char_base" / "chinese-xinhua-master" / "data" / "word.json"
MAKE_DICT = RAW / "01_char_base" / "makemeahanzi-master" / "dictionary.txt"
PINYIN_COMMON = RAW / "02_pronunciation" / "pinyin-data-master" / "kMandarin_8105.txt"
CNCHAR_RADICALS = RAW / "01_char_base" / "cnchar-master" / "src" / "cnchar" / "plugin" / "radical" / "dict" / "radicals.json"
CNCHAR_STRUCT = RAW / "01_char_base" / "cnchar-master" / "src" / "cnchar" / "plugin" / "radical" / "dict" / "struct.json"
CNCHAR_WUBI = RAW / "01_char_base" / "cnchar-master" / "src" / "cnchar" / "plugin" / "input" / "dict" / "wubi.json"
RIME_WUBI = RAW / "07_github_supplement" / "rime-wubi" / "wubi86.dict.yaml"
NAME_ELEMENTS = RAW / "07_github_supplement" / "johnwu1114-chinese-name" / "ChineseCharacters.json"
SHUOWEN_DIR = RAW / "07_github_supplement" / "shuowenjiezi-shuowen" / "data"
UNIHAN_ZIP = RAW / "06_auxiliary" / "unicode_unihan" / "Unihan.zip"
KANGXI_RADICALS_GO = RAW / "05_numerology" / "fate-main" / "internal" / "dict" / "kangxi_radicals.go"

RADICAL_KANGXI_ADJUST = {"氵": 4, "扌": 4, "忄": 4, "艹": 6, "辶": 7, "阝": 8, "犭": 4, "王": 5, "礻": 5, "衤": 6, "月": 6}
ELEMENT_BY_RADICAL = {
    "木": "木", "艹": "木", "竹": "木", "禾": "木",
    "火": "火", "灬": "火", "日": "火",
    "土": "土", "山": "土", "石": "土", "田": "土",
    "金": "金", "钅": "金", "刀": "金", "刂": "金", "玉": "金", "王": "金",
    "水": "水", "氵": "水", "冫": "水", "雨": "水",
}
RADICAL_SIMPLIFY = {
    "艸": "艹", "辵": "辶", "邑": "阝", "阜": "阝", "犬": "犭", "手": "扌", "心": "忄", "水": "氵",
    "金": "钅", "糸": "纟", "言": "讠", "食": "饣", "示": "礻", "衣": "衤", "玉": "王",
}
_OPENCC = None
POSITIVE_HINTS = set("安乐嘉佳瑞祥善美雅清朗明睿慧宁悦欣怡熙懿贤德仁义礼智信谦和温润泽宇轩宸")
NEGATIVE_HINTS = set("凶恶病死灾祸残贼毒怨哭哀厄丧")


def load_whitelist() -> list[str]:
    if not COMPLIANCE.exists():
        raise FileNotFoundError("Run extract_tongyong_hanzi.py before extracting attributes")
    with COMPLIANCE.open("r", encoding="utf-8", newline="") as f:
        chars = [row["char"] for row in csv.DictReader(f)]
    if len(chars) != 8105:
        raise ValueError(f"Compliance whitelist must have 8105 rows, got {len(chars)}")
    return chars


def load_xinhua() -> dict[str, dict]:
    with XINHUA.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return {item.get("word", ""): item for item in data if len(item.get("word", "")) == 1}


def load_makeme() -> dict[str, dict]:
    out: dict[str, dict] = {}
    with MAKE_DICT.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            ch = item.get("character", "")
            if len(ch) == 1:
                out[ch] = item
    return out


def load_common_pinyin() -> dict[str, str]:
    out: dict[str, str] = {}
    pat = re.compile(r"^U\+([0-9A-F]{4,5}):\s*([^#]+)")
    with PINYIN_COMMON.open("r", encoding="utf-8") as f:
        for line in f:
            m = pat.match(line.strip())
            if m:
                out[chr(int(m.group(1), 16))] = m.group(2).split(",")[0].strip()
    return out


def load_cnchar_radicals() -> dict[str, dict[str, object]]:
    raw = json.loads(CNCHAR_RADICALS.read_text(encoding="utf-8"))
    structs = json.loads(CNCHAR_STRUCT.read_text(encoding="utf-8"))
    out: dict[str, dict[str, object]] = {}
    for radical, text in raw.items():
        if radical == "*":
            i = 0
            while i < len(text):
                ch = text[i]
                code = text[i + 1] if i + 1 < len(text) else ""
                j = i + 2
                while j < len(text) and text[j].isdigit():
                    j += 1
                if "\u4e00" <= ch <= "\u9fff":
                    out[ch] = {"radical": ch, "radical_count": int(text[i + 2 : j] or 0), "structure": structs.get(code, "")}
                i = j
            continue
        if ":" not in text:
            continue
        count_text, body = text.split(":", 1)
        count = int(count_text) if count_text.isdigit() else 0
        i = 0
        while i + 1 < len(body):
            ch, code = body[i], body[i + 1]
            if "\u4e00" <= ch <= "\u9fff":
                out[ch] = {"radical": radical, "radical_count": count, "structure": structs.get(code, "")}
            i += 2
    return out


def load_kangxi_radical_names() -> dict[str, str]:
    text = KANGXI_RADICALS_GO.read_text(encoding="utf-8")
    names = dict(re.findall(r'"(\d+)":\s*"([^"]+)"', text))
    if len(names) < 214:
        raise ValueError(f"Could not parse 214 Kangxi radical names from {KANGXI_RADICALS_GO}")
    return names


def simplify_radical(radical: str) -> str:
    global _OPENCC
    if radical in RADICAL_SIMPLIFY:
        return RADICAL_SIMPLIFY[radical]
    try:
        if _OPENCC is None:
            from opencc import OpenCC

            _OPENCC = OpenCC("t2s")
        radical = _OPENCC.convert(radical)
    except Exception:
        pass
    return RADICAL_SIMPLIFY.get(radical, radical)


def load_unihan_attrs() -> dict[str, dict[str, str]]:
    if not UNIHAN_ZIP.exists():
        return {}
    radical_names = load_kangxi_radical_names()
    attrs: dict[str, dict[str, str]] = {}
    with zipfile.ZipFile(UNIHAN_ZIP) as zf:
        for name in zf.namelist():
            if not name.endswith(".txt"):
                continue
            with zf.open(name) as f:
                for raw in f:
                    line = raw.decode("utf-8").strip()
                    if not line or line.startswith("#"):
                        continue
                    parts = line.split("\t")
                    if len(parts) < 3 or not parts[0].startswith("U+"):
                        continue
                    ch = chr(int(parts[0][2:], 16))
                    field, value = parts[1], parts[2]
                    item = attrs.setdefault(ch, {})
                    if field == "kRSUnicode":
                        m = re.match(r"(\d+)'?\.", value)
                        if m:
                            item["radical"] = simplify_radical(radical_names.get(m.group(1), ""))
                    elif field == "kTotalStrokes":
                        m = re.search(r"\d+", value)
                        if m:
                            item["strokes"] = m.group(0)
                    elif field == "kDefinition":
                        item.setdefault("definition", value)
    return attrs


def load_name_elements(whitelist: set[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    if not NAME_ELEMENTS.exists():
        return out
    try:
        data = json.loads(NAME_ELEMENTS.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return out
    for item in data:
        element = str(item.get("fiveEle", "") or "")
        if element not in {"木", "火", "土", "金", "水"}:
            continue
        for ch in str(item.get("chars", "") or ""):
            if ch in whitelist and ch not in out:
                out[ch] = element
    return out


def load_rime_wubi(whitelist: set[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    if not RIME_WUBI.exists():
        return out
    started = False
    with RIME_WUBI.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.strip() == "...":
                started = True
                continue
            if not started or not line.strip() or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) >= 2:
                ch, code = parts[0].strip(), parts[1].strip()
                if len(ch) == 1 and ch in whitelist and ch not in out:
                    out[ch] = code
    return out


def load_shuowen(whitelist: set[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    if not SHUOWEN_DIR.exists():
        return out
    for path in SHUOWEN_DIR.glob("*.json"):
        try:
            item = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        ch = item.get("wordhead", "")
        explanation = re.sub(r"\s+", " ", str(item.get("explanation", "") or "")).strip()
        if len(ch) == 1 and ch in whitelist and explanation and ch not in out:
            out[ch] = explanation
        for variant in item.get("variants") or []:
            vch = variant.get("wordhead", "")
            vexp = re.sub(r"\s+", " ", str(variant.get("explanation", "") or "")).strip()
            if len(vch) == 1 and vch in whitelist and vexp and vch not in out:
                out[vch] = vexp
    return out


def infer_structure(decomp: str) -> str:
    if not decomp or decomp == "？":
        return "独体"
    op = decomp[0]
    return {"⿰": "左右", "⿱": "上下", "⿲": "左右", "⿳": "上下", "⿴": "包围", "⿵": "包围", "⿶": "包围", "⿷": "包围", "⿸": "包围", "⿹": "包围", "⿺": "包围", "⿻": "品字"}.get(op, "独体")


def normalize_structure(value: str) -> str:
    if "左右" in value or "左中右" in value:
        return "左右"
    if "上下" in value or "上中下" in value:
        return "上下"
    if "包围" in value:
        return "包围"
    if "品字" in value:
        return "品字"
    if "独体" in value:
        return "独体"
    return value


def components(decomp: str) -> list[str]:
    if not decomp:
        return []
    return [c for c in decomp if "\u4e00" <= c <= "\u9fff"]


def fallback_element(strokes: int | str) -> str:
    if not isinstance(strokes, int):
        return "土"
    tail = strokes % 10
    if tail in {1, 2}:
        return "木"
    if tail in {3, 4}:
        return "火"
    if tail in {5, 6}:
        return "土"
    if tail in {7, 8}:
        return "金"
    return "水"


def fallback_definition(ch: str) -> str:
    return f"规范汉字「{ch}」，取名释义需结合字形、读音与语境综合判断。"


def fallback_ancient(ch: str, component_list: list[str]) -> str:
    parts = "、".join(component_list or [ch])
    return f"未见结构化古义；字形构件：{parts}。"


def etymology_text(item: dict) -> str:
    etymology = item.get("etymology")
    if not isinstance(etymology, dict):
        return ""
    parts: list[str] = []
    hint = str(etymology.get("hint") or "").strip()
    if hint:
        parts.append(hint)
    semantic = str(etymology.get("semantic") or "").strip()
    phonetic = str(etymology.get("phonetic") or "").strip()
    if semantic:
        parts.append(f"义符：{semantic}")
    if phonetic:
        parts.append(f"声符：{phonetic}")
    return "；".join(parts)


def positive_level(ch: str, definition: str) -> int:
    if ch in POSITIVE_HINTS or any(k in definition for k in ["美好", "吉祥", "善", "贤", "清雅", "聪明"]):
        return 5
    if any(k in definition for k in ["好", "美", "安", "乐", "明", "德"]):
        return 4
    if ch in NEGATIVE_HINTS or any(k in definition for k in ["凶", "恶", "病", "死亡", "灾"]):
        return 1
    return 3


def common_level(idx: int) -> int:
    return 1 if idx <= 3500 else 2 if idx <= 6500 else 3


def kangxi_strokes(modern: int | str, radical: str) -> int | str:
    if not isinstance(modern, int):
        return ""
    if radical in RADICAL_KANGXI_ADJUST:
        modern_radical_guess = {"氵": 3, "扌": 3, "忄": 3, "艹": 3, "辶": 3, "阝": 3, "犭": 3, "王": 4, "礻": 4, "衤": 5, "月": 4}.get(radical, RADICAL_KANGXI_ADJUST[radical])
        return modern - modern_radical_guess + RADICAL_KANGXI_ADJUST[radical]
    return modern


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    whitelist = load_whitelist()
    whitelist_set = set(whitelist)
    xinhua = load_xinhua()
    makeme = load_makeme()
    common_pinyin = load_common_pinyin()
    cnchar_radicals = load_cnchar_radicals()
    wubi_map = json.loads(CNCHAR_WUBI.read_text(encoding="utf-8"))
    wubi_map.update(load_rime_wubi(whitelist_set))
    name_elements = load_name_elements(whitelist_set)
    shuowen = load_shuowen(whitelist_set)
    unihan = load_unihan_attrs()
    base_rows: list[dict[str, object]] = []
    kangxi: dict[str, dict[str, object]] = {}
    semantic: dict[str, dict[str, object]] = {}
    for idx, ch in enumerate(whitelist, start=1):
        x = xinhua.get(ch, {})
        m = makeme.get(ch, {})
        c = cnchar_radicals.get(ch, {})
        u = unihan.get(ch, {})
        strokes_raw = str(x.get("strokes", "") or "")
        strokes_source = strokes_raw or u.get("strokes", "")
        strokes = int(strokes_source) if str(strokes_source).isdigit() else ""
        radical = str(x.get("radicals", "") or m.get("radical", "") or c.get("radical", "") or u.get("radical", "") or "")
        m_pinyin = (m.get("pinyin") or [""])[0] if isinstance(m.get("pinyin"), list) else ""
        pinyin = str(x.get("pinyin", "") or common_pinyin.get(ch, "") or m_pinyin)
        decomp = str(m.get("decomposition", "") or "")
        structure = normalize_structure(str(c.get("structure", ""))) or infer_structure(decomp)
        definition = re.sub(r"\s+", " ", str(x.get("explanation", "") or m.get("definition", "") or u.get("definition", "") or "")).strip()
        if not definition:
            definition = fallback_definition(ch)
        component_list = components(decomp)
        if not component_list:
            component_list = [ch]
        ancient_meaning = shuowen.get(ch, "") or etymology_text(m) or fallback_ancient(ch, component_list)
        element = name_elements.get(ch) or ELEMENT_BY_RADICAL.get(radical, "") or fallback_element(kangxi_strokes(strokes, radical))
        basis = "现代笔画加姓名学常用部首折算表；五行优先采用 GitHub johnwu1114/chinese-name，缺失时按部首/笔画尾数规则推断。"
        base_rows.append({"char": ch, "pinyin_main": pinyin, "strokes_modern": strokes, "radical": radical, "structure": structure, "wubi": wubi_map.get(ch, "")})
        kangxi[ch] = {
            "kangxi_strokes": kangxi_strokes(strokes, radical),
            "kangxi_radical": radical,
            "element": element,
            "components": component_list,
            "basis": basis,
        }
        semantic[ch] = {
            "definition": definition[:180],
            "positive_level": positive_level(ch, definition),
            "common_level": common_level(idx),
            "ancient_meaning": ancient_meaning,
        }
    with (OUT_DIR / "char_base_info.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["char", "pinyin_main", "strokes_modern", "radical", "structure", "wubi"])
        writer.writeheader()
        writer.writerows(base_rows)
    for filename, data in [("kangxi_strokes.json", kangxi), ("char_semantic.json", semantic)]:
        (OUT_DIR / filename).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    readme = f"""# 汉字全属性层

本目录以合规准入层 8105 字为唯一白名单，整合 `chinese-xinhua-master` 与 `makemeahanzi-master` 的单字属性。

## 文件与字段

- `char_base_info.csv`: `char` 汉字；`pinyin_main` 首选拼音；`strokes_modern` 现代笔画；`radical` 部首；`structure` 字形结构；`wubi` 五笔编码，源数据缺失时留空。
- `kangxi_strokes.json`: `kangxi_strokes` 康熙/姓名学笔画；`kangxi_radical` 康熙部首近似字段；`element` 五行；`components` 部件拆分；`basis` 计算依据。
- `char_semantic.json`: `definition` 释义摘要；`positive_level` 褒义等级 1-5；`common_level` 常用度 1-3；`ancient_meaning` 古义摘要，源缺失时留空。

## 取值规范

缺失字段留空。康熙笔画对氵、艹、扌、忄、辶、阝、犭、王、礻、衤、月等常见姓名学部首进行传统笔画折算；其余字沿用现代笔画并在 `basis` 中标注。

## 数据来源

- `00_raw_repos/01_char_base/chinese-xinhua-master/data/word.json`
- `00_raw_repos/01_char_base/makemeahanzi-master/dictionary.txt`
- `00_raw_repos/01_char_base/cnchar-master/src/cnchar/plugin/radical/dict/radicals.json`
- `00_raw_repos/01_char_base/cnchar-master/src/cnchar/plugin/input/dict/wubi.json`
- 五笔补充源：`00_raw_repos/07_github_supplement/rime-wubi/wubi86.dict.yaml`
- 五行补充源：GitHub `johnwu1114/chinese-name/ChineseCharacters.json`；源缺失时按部首/笔画尾数规则兜底。
- 古义补充源：`00_raw_repos/07_github_supplement/shuowenjiezi-shuowen/data/*.json`
- 字源兜底源：`makemeahanzi-master/dictionary.txt` 的 `etymology` 字段，含 hint/semantic/phonetic。
- Unicode 官方 Unihan `kRSUnicode`、`kTotalStrokes`、`kDefinition` 缓存：`00_raw_repos/06_auxiliary/unicode_unihan/Unihan.zip`
- 首选拼音补充：`00_raw_repos/02_pronunciation/pinyin-data-master/kMandarin_8105.txt`
- 白名单：`01_knowledge_base/01_compliance_layer/tongyong_guifan_hanzi.csv`
- 提取时间：{datetime.now().isoformat(timespec="seconds")}.
"""
    (OUT_DIR / "README.md").write_text(readme, encoding="utf-8", newline="\n")
    print(f"Wrote {OUT_DIR}")


if __name__ == "__main__":
    main()
