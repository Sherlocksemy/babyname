#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract the 8105-character Tongyong Guifan Hanzi whitelist."""

from __future__ import annotations

import csv
import re
import zipfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "00_raw_repos"
OUT_DIR = ROOT / "01_knowledge_base" / "01_compliance_layer"
PDF_PATH = RAW / "01_char_base" / "通用规范汉字表.pdf"
ORDER_PATH = RAW / "02_pronunciation" / "pinyin-data-master" / "tools" / "china-8105-06062014.txt"
XINHUA_PATH = RAW / "01_char_base" / "chinese-xinhua-master" / "data" / "word.json"
CNCHAR_STROKES = RAW / "01_char_base" / "cnchar-master" / "src" / "cnchar" / "main" / "dict" / "stroke-count-jian.json"
UNIHAN_ZIP = RAW / "06_auxiliary" / "unicode_unihan" / "Unihan.zip"
KANGXI_RADICALS_GO = RAW / "05_numerology" / "fate-main" / "internal" / "dict" / "kangxi_radicals.go"
RADICAL_SIMPLIFY = {
    "艸": "艹", "辵": "辶", "邑": "阝", "阜": "阝", "犬": "犭", "手": "扌", "心": "忄", "水": "氵",
    "金": "钅", "糸": "纟", "言": "讠", "食": "饣", "示": "礻", "衣": "衤", "玉": "王",
}
_OPENCC = None


def read_json(path: Path):
    import json

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_order_file() -> list[str]:
    chars: list[str] = []
    pattern = re.compile(r"^U\+([0-9A-F]{4,5})\s+")
    with ORDER_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            m = pattern.match(line.strip())
            if m:
                chars.append(chr(int(m.group(1), 16)))
    if len(chars) != 8105:
        raise ValueError(f"{ORDER_PATH} did not contain 8105 codepoints, got {len(chars)}")
    if len(set(chars)) != 8105:
        raise ValueError(f"{ORDER_PATH} contains duplicate codepoints")
    return chars


def smoke_check_pdf() -> str:
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"Official PDF not found: {PDF_PATH}")
    try:
        import pdfplumber
    except ImportError as exc:
        raise RuntimeError("PDF parsing dependency missing: install pdfplumber from requirements.txt") from exc
    failed: list[int] = []
    seen = 0
    with pdfplumber.open(str(PDF_PATH)) as pdf:
        for idx, page in enumerate(pdf.pages, start=1):
            try:
                text = page.extract_text() or ""
                seen += len(text)
            except Exception:
                failed.append(idx)
    if failed:
        raise RuntimeError(f"PDF parsing failed on page(s): {', '.join(map(str, failed))}")
    if seen == 0:
        return "PDF 为扫描版或无文本层，pdfplumber 未抽取到文字；已回退使用 pinyin-data 的 8105 官方码位顺序辅助源。"
    return "PDF 文本层可解析，未发现页码级解析异常。"


def load_xinhua_attrs() -> dict[str, dict[str, str]]:
    data = read_json(XINHUA_PATH)
    attrs: dict[str, dict[str, str]] = {}
    for item in data:
        ch = item.get("word", "")
        if len(ch) == 1:
            attrs[ch] = {
                "strokes": str(item.get("strokes", "") or ""),
                "radical": str(item.get("radicals", "") or ""),
            }
    return attrs


def load_cnchar_strokes() -> dict[str, int]:
    raw = read_json(CNCHAR_STROKES)
    strokes: dict[str, int] = {}
    for stroke, chars in raw.items():
        if not str(stroke).isdigit():
            continue
        for ch in chars:
            strokes[ch] = int(stroke)
    return strokes


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
    return attrs


def build_rows() -> tuple[list[dict[str, object]], str]:
    pdf_status = smoke_check_pdf()
    chars = parse_order_file()
    xinhua = load_xinhua_attrs()
    cnchar = load_cnchar_strokes()
    unihan = load_unihan_attrs()
    rows: list[dict[str, object]] = []
    for idx, ch in enumerate(chars, start=1):
        level = 1 if idx <= 3500 else 2 if idx <= 6500 else 3
        attr = xinhua.get(ch, {})
        u = unihan.get(ch, {})
        strokes = attr.get("strokes") or cnchar.get(ch) or u.get("strokes", "")
        radical = attr.get("radical") or u.get("radical", "")
        rows.append(
            {
                "char": ch,
                "level": level,
                "strokes_modern": int(strokes) if str(strokes).isdigit() else "",
                "radical": radical,
                "unicode": f"U+{ord(ch):04X}",
            }
        )
    rows.sort(key=lambda r: (r["level"], r["strokes_modern"] if r["strokes_modern"] != "" else 999, ord(str(r["char"]))))
    if len(rows) != 8105 or len({r["char"] for r in rows}) != 8105:
        raise ValueError("Tongyong whitelist must contain exactly 8105 unique characters")
    return rows, pdf_status


def write_readme(pdf_status: str) -> None:
    text = f"""# 合规准入层

本目录保存新生儿取名系统的唯一单字准入白名单。所有后续单字知识库均必须以 `tongyong_guifan_hanzi.csv` 为过滤依据。

## 字段说明

- `char`: 规范汉字。
- `level`: 《通用规范汉字表》字级，1/2/3；按官方 3500/3000/1605 分级。
- `strokes_modern`: 现代规范笔画数，优先取 chinese-xinhua，缺失时用 cnchar 笔画表补齐。
- `radical`: 部首，优先取 chinese-xinhua。
- `unicode`: Unicode 十六进制编码。

## 户籍登记注意事项

公安户籍登记通常以国家通用规范汉字为准。取名业务应优先使用一级、二级常用字；三级字虽在规范表内，但存在输入法、证件系统、跨系统显示兼容风险，需谨慎使用。

## 数据来源

- 原始底本：国务院 2013 年发布《通用规范汉字表》PDF：`00_raw_repos/01_char_base/通用规范汉字表.pdf`。
- 8105 字官方顺序辅助源：`pinyin-data-master/tools/china-8105-06062014.txt`。
- 笔画与部首补充源：`chinese-xinhua-master/data/word.json`、`cnchar-master/stroke-count-jian.json`。
- 部首与总笔画补充源：Unicode 官方 Unihan `kRSUnicode`、`kTotalStrokes`，本地缓存 `00_raw_repos/06_auxiliary/unicode_unihan/Unihan.zip`。
- PDF 解析状态：{pdf_status}
- 提取时间：{datetime.now().isoformat(timespec="seconds")}.
"""
    (OUT_DIR / "README.md").write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows, pdf_status = build_rows()
    out = OUT_DIR / "tongyong_guifan_hanzi.csv"
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["char", "level", "strokes_modern", "radical", "unicode"])
        writer.writeheader()
        writer.writerows(rows)
    write_readme(pdf_status)
    print(f"Wrote {out} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
