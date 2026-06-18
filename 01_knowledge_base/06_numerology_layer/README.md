# 命理规则层

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
- 提取时间：2026-06-18T15:58:40.
