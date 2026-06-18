# 读音音律层

本目录保存普通话、潮汕话和谐音风险数据，所有单字均按合规层 8105 字过滤。

## 字段说明

- `mandarin_pinyin.json`: 键为汉字；`pinyin` 为带声调拼音；`tone` 为 1/2/3/4/0；`is_common` 标注 `kMandarin_8105.txt` 首选读音；`rhyme` 为中华通韵近似韵部。
- `teochew_pronunciation.csv`: `char` 汉字；`pinyin_teochew` 潮罗/字典读音；`tone` 调号；`accent` 潮阳/汕头/潮州/揭阳/澄海/饶平；文白读标记按源文件标注推断，源缺失则为 False。
- `homophone_blacklist.csv`: 由普通话与潮汕话同音分组生成，覆盖常见负面语义字的谐音风险。

## 数据来源

- `00_raw_repos/02_pronunciation/pinyin-data-master/pinyin.txt`
- `00_raw_repos/02_pronunciation/pinyin-data-master/kMandarin_8105.txt`
- `00_raw_repos/02_pronunciation/dieghv-master/*.dict.yaml`
- 提取时间：2026-06-18T15:57:01.
