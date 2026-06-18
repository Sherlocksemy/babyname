# 姓名流行度层

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
- 提取时间：2026-06-18T15:57:06.
