# Data Quality Findings

This file records audit discoveries for the generated baby-name-system knowledge base.

## Initial Missing-Field Audit

- `01_compliance_layer/tongyong_guifan_hanzi.csv`: 8105 rows; `radical` missing 1359 (16.8%), `strokes_modern` missing 620 (7.6%).
- `02_char_attribute_layer/char_base_info.csv`: `radical` missing 1139 (14.1%), `pinyin_main` missing 1239 (15.3%), `strokes_modern` missing 687 (8.5%), `wubi` 100% missing.
- `kangxi_strokes.json`: `kangxi_radical` missing 1139, `kangxi_strokes` missing 687, `element` missing 5868.
- `zodiac_taboo.csv`: only mouse zodiac has parsed radicals; other 11 zodiac rows have blank radical fields.
- Culture layer is structurally valid, but `translation` is absent from all source-derived outputs; Tang/Song `chapter` is also blank.

## Source Trace

- `cnchar-master/src/cnchar/plugin/radical/dict/radicals.json` covers 6747 of 8105 whitelist characters; it cannot fill the 1358-character compliance radical gap by itself.
- Unicode official `Unihan.zip` was added under `00_raw_repos/06_auxiliary/unicode_unihan/`; `kRSUnicode` and `kTotalStrokes` cover all 8105 whitelist characters.
- `pinyin-data-master/kMandarin_8105.txt` covers all 8105 whitelist characters and is appropriate for filling `pinyin_main`.

## After Core Fix

- `tongyong_guifan_hanzi.csv`: `radical` missing 0, `strokes_modern` missing 0.
- `char_base_info.csv`: `pinyin_main`, `strokes_modern`, `radical`, `structure` missing 0; optional `wubi` missing 1359 because cnchar wubi source covers 6746 whitelist chars.
- `kangxi_strokes.json`: `kangxi_radical` and `kangxi_strokes` missing 0; `element` remains sparse because element inference is only radical-family based.

## GitHub Supplement Pass

- GitHub MCP connector failed to initialize twice with `https://chatgpt.com/backend-api/wham/apps`; fallback used direct GitHub clone/API access.
- Added `rime/rime-wubi` under `00_raw_repos/07_github_supplement/rime-wubi`; `wubi86.dict.yaml` covers all 8105 whitelist characters, reducing `char_base_info.csv.wubi` missing from 1359 to 0.
- Added `shuowenjiezi/shuowen`; it fills `ancient_meaning` for 3465 whitelist characters. Remaining 4640 are not present as one-character `wordhead`/variant entries in the source.
- Added `johnwu1114/chinese-name`; 12生肖 JSON files fill `zodiac_taboo.csv` by deriving good/bad radicals from better/worse character sets.
- Fixed `process_poetry_data.py` Tang source to use `poet.tang.*.json` instead of the broader `poet.*.json`, which had accidentally read Song-author files into Tang output.
- Attempted to clone a Tang poetry translation Gist, but `gist.github.com` timed out. No translation text was fabricated.

## GitHub Translation Supplement Pass

- GitHub MCP was retried after network recovery but still failed during MCP initialization with the same `chatgpt.com/backend-api/wham/apps` handshake error. Direct GitHub HTTPS clone was used to continue.
- Added `yht050511/gushiwen` under `00_raw_repos/07_github_supplement/yht050511-gushiwen`.
- `process_poetry_data.py` now builds `translation_index.json` from `gushiwen.json.gz` and fills translations from `sons.译文及注释`.
- Translation matching is conservative: `title+author` first, title-only fallback only when the title is unique in the supplement index. This avoids wrong translations for common duplicate titles.
- Current translation coverage: Shijing 301/305, Chuci 19/65, Tang selected 204/3000, Song Ci selected 88/3000, Sishuwujing 0/36.
