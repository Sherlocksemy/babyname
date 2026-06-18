# 文化出处层

本目录按诗经、楚辞、唐诗、宋词、四书五经分层保存可追溯文化出处。

## 统一字段

`id` 唯一编号；`title` 篇名；`author` 作者；`dynasty` 朝代；`chapter` 章节/分类；`content` 原文；`translation` 白话译文，源缺失时留空；`keywords` 取名意象关键词；`name_candidates` 从原文启发式提取的 2-3 个双字词组。

## 处理规范

使用 OpenCC 将繁体尽量转为简体；无 OpenCC 环境时保留原文。唐诗、宋词源数据体量极大，本层输出取前 3000 条作为“精选”基础集，后续可按评分策略扩展。唐诗来源限定为 `poet.tang.*.json`，避免误读同目录宋诗文件。
非译文字段采用规则兜底：关键词缺失时使用文学出处/清雅等通用标签，候选名缺失时从合规白名单汉字组成的双字窗口补齐，唐诗无章节时统一标注为“全唐诗精选”。译文字段仅使用可追溯来源，不做机器生成；真实来源缺失时保留空值并由审计报告统计。

## 数据来源

- `00_raw_repos/03_culture/chinese-poetry-master/诗经/shijing.json`
- `00_raw_repos/03_culture/chinese-poetry-master/楚辞/chuci.json`
- `00_raw_repos/03_culture/chinese-poetry-master/全唐诗/`
- `00_raw_repos/03_culture/chinese-poetry-master/宋词/`
- `00_raw_repos/03_culture/chinese-poetry-master/四书五经/`、`论语/`
- 译文补充源：`00_raw_repos/07_github_supplement/yht050511-gushiwen/gushiwen.json.gz`，按标题/作者匹配，字段来自 `sons.译文及注释`。
- 四书译文补充源：GitHub `NiuTrans/Classical-Modern` 的 `双语数据/大学章句集注`、`双语数据/中庸`、`双语数据/孟子`、`双语数据/论语`，本地缓存于 `00_raw_repos/07_github_supplement/NiuTrans-Classical-Modern-bilingual/`。
- 提取时间：2026-06-18T15:57:06.
