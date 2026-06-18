# 03_DATA_SCHEMA.md｜易元命名知识库与数据结构设计

## 1. 文档目标

本文档定义新生儿智能取名系统的数据标准。当前项目已有知识库位于 `01_knowledge_base/`，包含合规字库、字属性、读音、文化出处、热度、传统数理等层级。系统开发时必须以本文档为准，不得在业务代码中随意猜字段、改字段、临时拼接数据。

## 2. 知识库总目录

```text
01_knowledge_base/
├── 01_compliance_layer/
├── 02_char_attribute_layer/
├── 03_pronunciation_layer/
├── 04_culture_origin_layer/
├── 05_name_popularity_layer/
├── 06_numerology_layer/
└── build_audit_report.json
```

## 3. compliance_layer

### 3.1 tongyong_guifan_hanzi.csv

用途：合规汉字白名单，是所有候选字的第一层过滤来源。

字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| char | string | 汉字 |
| level | int | 通用规范汉字等级 |
| strokes_modern | int | 现代笔画 |
| radical | string | 部首 |
| unicode | string | Unicode 编码 |

规则：

1. 候选名用字必须优先来自该文件。
2. 不在该文件中的字默认不可作为 V1.0 推荐字。
3. level 越低越常用，排序时可加权。

## 4. char_attribute_layer

### 4.1 char_base_info.csv

用途：提供单字基础属性。

字段：char、pinyin_main、strokes_modern、radical、structure、wubi。

### 4.2 char_semantic.json

用途：提供字义、古义、正向等级、常用等级。

结构：

```json
{
  "一": {
    "definition": "...",
    "positive_level": 4,
    "common_level": 1,
    "ancient_meaning": "..."
  }
}
```

规则：

1. positive_level 用于过滤负面字义。
2. common_level 用于控制常用度。
3. ancient_meaning 可用于文化解释，但不得强行用于每个字。

### 4.3 kangxi_strokes.json

用途：提供康熙笔画、姓名学部首、五行、构件。

结构：

```json
{
  "一": {
    "kangxi_strokes": 1,
    "kangxi_radical": "一",
    "element": "土",
    "components": ["一"],
    "basis": "..."
  }
}
```

规则：

1. 五格计算使用 kangxi_strokes。
2. 五行适配使用 element，但只作为传统文化参考。
3. basis 字段用于解释数据来源与推断依据。

## 5. pronunciation_layer

### 5.1 mandarin_pinyin.json

用途：普通话拼音、声调、韵部。

结构：

```json
{
  "㑇": [
    {"pinyin": "zhòu", "tone": 4, "is_common": true, "rhyme": "一啊"}
  ]
}
```

规则：

1. 多音字必须显式处理。
2. 姓氏多音时必须由用户或系统规则确定读音。
3. 名字组合需要检查声调结构。

### 5.2 teochew_pronunciation.csv

用途：潮汕话读音检查。

字段：char、pinyin_teochew、tone、accent、is_colloquial、is_literary。

规则：

1. 同一字可能有多个地区口音记录。
2. 默认支持汕头、揭阳等 accent。
3. 若用户出生地或方言偏好为潮汕地区，需提高该层权重。

### 5.3 homophone_blacklist.csv

用途：谐音风险过滤。

字段：char、homophone_char、bad_meaning、language_type。

规则：

1. language_type 支持 mandarin 等类型。
2. 命中严重负面谐音时直接淘汰。
3. 轻微风险可作为 warning 输出。

## 6. culture_origin_layer

文化出处层包含：

1. shijing/shijing_full.json
2. chuci/chuci_full.json
3. tang_poetry/tang_poetry.json
4. song_ci/song_ci.json
5. sishuwujing/sishuwujing.json

统一字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| id | string | 条目 ID |
| title | string | 篇名 |
| author | string | 作者 |
| dynasty | string | 朝代 |
| chapter | string | 章节 |
| content | string | 原文 |
| translation | string | 译文，可为空 |
| keywords | list | 意象/主题标签 |
| name_candidates | list | 候选名字片段 |

规则：

1. 直接命中：名字中的字或双字直接出现在 content 中。
2. 候选命中：名字来自 name_candidates。
3. 意象关联：名字不直接出现，但语义与 keywords 相关，必须标注 match_type=imagery_related。
4. translation 为空时不得生成伪译文。
5. 文化解释必须引用 content 字段，不得凭空造句。

## 7. popularity_layer

### 7.1 char_frequency.csv

字段：char、gender_tendency、frequency_rank、heat_level、era_tag。

用途：控制用字热度、性别倾向、时代感。

### 7.2 top_names_blacklist.csv

字段：name、gender、estimated_count、heat_level。

用途：过滤或降权爆款名。

规则：

1. 命中爆款全名，默认降权或淘汰。
2. 命中高频单字，不一定淘汰，但不得堆叠。
3. 用户主动禁用爆款字时，严格过滤。

## 8. numerology_layer

### 8.1 bazi_rules.json

用途：八字、十神、五行解释规则。

### 8.2 wuge_rules.json

用途：五格 81 数理解释。

### 8.3 zodiac_taboo.csv

字段：zodiac、good_radicals、bad_radicals、good_meaning、bad_meaning、lucky_elements。

规则：

1. 生肖喜忌仅作为参考维度。
2. 生肖规则不得直接决定名字淘汰，除非与其他风险叠加。
3. 对用户展示时必须使用“传统文化参考”口径。

## 9. 核心业务 Schema

### 9.1 BabyProfile

```json
{
  "surname": "陈",
  "gender": "female",
  "birth_datetime": "2026-06-18 09:30",
  "calendar_type": "solar",
  "birth_place": "广东省汕头市",
  "name_length": 2,
  "style_preferences": ["温润", "诗意"],
  "banned_chars": ["梓", "轩"],
  "liked_chars": ["清"],
  "avoid_hot_names": true,
  "need_teochew_check": true
}
```

### 9.2 BaziProfile

```json
{
  "zodiac": "马",
  "bazi": {"year": "...", "month": "...", "day": "...", "hour": "..."},
  "five_elements_count": {"金": 1, "木": 2, "水": 0, "火": 2, "土": 3},
  "preferred_elements": ["水", "木"],
  "explanation": "五行水偏弱，取名可参考水、木意象。"
}
```

### 9.3 CultureOrigin

```json
{
  "source": "诗经",
  "title": "关雎",
  "author": "佚名",
  "original_text": "...",
  "matched_chars": ["清"],
  "match_type": "direct_char",
  "confidence": 0.92,
  "explanation": "..."
}
```

### 9.4 NameCandidate

```json
{
  "name": "陈清宁",
  "given_name": "清宁",
  "score": 91,
  "pinyin": "chén qīng níng",
  "summary": "清澈安宁，温润明朗。",
  "meaning": {},
  "culture_origin": {},
  "pronunciation": {},
  "teochew": {},
  "bazi": {},
  "zodiac": {},
  "popularity": {},
  "warnings": [],
  "recommendation_reason": "..."
}
```

### 9.5 NameScore

```json
{
  "compliance": 15,
  "mandarin": 14,
  "teochew": 9,
  "meaning": 14,
  "culture": 13,
  "bazi": 8,
  "zodiac": 4,
  "popularity": 8,
  "gender_style": 5,
  "total": 90
}
```

### 9.6 QualityGuardResult

```json
{
  "passed": true,
  "issues": [],
  "warnings": [],
  "action": "accept"
}
```

## 10. 数据治理规则

1. 原始知识库不得被业务代码直接改写。
2. 所有派生结果放入 scripts 或缓存目录。
3. 每次构建必须输出 build_audit_report.json。
4. 字段缺失必须 warning，不允许静默失败。
5. 所有候选名字必须能回溯到数据来源。
