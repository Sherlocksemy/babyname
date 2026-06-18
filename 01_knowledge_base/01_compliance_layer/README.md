# 合规准入层

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
- PDF 解析状态：PDF 为扫描版或无文本层，pdfplumber 未抽取到文字；已回退使用 pinyin-data 的 8105 官方码位顺序辅助源。
- 提取时间：2026-06-18T15:56:43.
