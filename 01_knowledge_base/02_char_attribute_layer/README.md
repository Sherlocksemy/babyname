# 汉字全属性层

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
- 提取时间：2026-06-18T15:56:59.
