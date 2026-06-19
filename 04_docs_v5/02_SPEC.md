# 易元命名 Pro｜AI易经命名顾问系统

## System Specification

### Version 3.1 Final

---

# 文档信息

| 项目   | 内容                                                   |
| ---- | ---------------------------------------------------- |
| 文档名称 | 02_SPEC.md                                           |
| 所属项目 | 易元命名 Pro                                             |
| 文档版本 | V3.1 Final                                           |
| 文档定位 | 系统架构设计说明书                                            |
| 上游文档 | 01_PRD.md、02A_NAMING_PHILOSOPHY.md、03_DATA_SCHEMA.md |
| 下游文档 | 04_DEV_PLAN.md、05_TEST_PLAN.md、06_API_SCHEMA.md      |
| 核心目标 | 定义系统架构、模块职责、引擎协作机制与生成流程                              |

---

# 第一章 系统设计目标

## 1.1 系统定位

易元命名不是：

```text
起名工具
```

而是：

```text
AI命名顾问系统
```

---

系统输出的不是：

```text
20个名字
```

而是：

```text
一组经过命理分析、
文化考据、
人格建模、
质量审查后的姓名方案
```

---

## 1.2 V1核心目标

V1阶段只解决一个问题：

```text
稳定生成高质量姓名
```

---

不做：

* 会员体系
* 支付体系
* 海报生成
* 分享裂变
* AI聊天
* Agent协作

---

只专注：

```text
名字质量
```

---

# 第二章 架构设计原则

## 原则一

Knowledge First

---

知识库优先。

系统所有事实来源于：

```text
knowledge_base
```

---

包括：

* 康熙字典
* 五行
* 诗经
* 楚辞
* 唐诗
* 宋词
* 四书五经
* 潮汕话
* 重名库
* 八字规则

---

AI不得编造。

---

## 原则二

Rule Driven

---

规则驱动。

---

所有结论：

必须来自：

```text
Rule Engine
```

---

例如：

八字分析。

五格分析。

生肖分析。

谐音分析。

---

禁止：

AI直接生成结论。

---

## 原则三

AI Assisted

---

AI仅负责：

### 解释

---

### 总结

---

### 顾问报告

---

不负责：

### 决策

---

## 原则四

Plugin Architecture

---

所有模块插件化。

---

支持未来增加：

```text
紫微斗数

奇门遁甲

企业命名

品牌命名

家谱辈分
```

无需重构。

---

# 第三章 总体架构

## 3.1 六层架构

系统采用：

```text
Presentation Layer

↓

API Layer

↓

Orchestrator Layer

↓

Engine Layer

↓

Knowledge Layer

↓

Storage Layer
```

---

## 3.2 架构图

```text
Frontend
│
├── Baby Form
├── Name List
├── Name Detail
└── Compare

        ↓

FastAPI

        ↓

NameGenerationOrchestrator

        ↓

ArchetypeEngine
ImageryEngine
BaziEngine
WugeEngine
ZodiacEngine
CultureRetriever
NameComposer
NameScorer
QualityGuard

        ↓

Knowledge Base

        ↓

SQLite/PostgreSQL
```

---

# 第四章 系统模块划分

## 一级模块

### User Module

用户输入模块

---

### Profile Module

宝宝画像模块

---

### Fortune Module

命理分析模块

---

### Archetype Module

人格原型模块

---

### Imagery Module

文化意象模块

---

### Culture Module

出处召回模块

---

### Generation Module

姓名生成模块

---

### Scoring Module

评分模块

---

### Quality Module

质量审查模块

---

### Report Module

顾问报告模块

---

# 第五章 核心调度器

## NameGenerationOrchestrator

### 定位

系统总调度器。

---

负责：

```text
统一管理所有引擎
```

---

避免：

```text
Engine互相调用
```

导致耦合。

---

## 调度流程

```text
UserInput

↓

BabyProfile

↓

ArchetypeEngine

↓

ImageryEngine

↓

BaziEngine

↓

ZodiacEngine

↓

WugeEngine

↓

CultureRetriever

↓

CharPoolBuilder

↓

NameComposer

↓

NameScorer

↓

QualityGuard

↓

ConsultantReport
```

---

# 第六章 引擎协作原则

## Engine禁止

直接依赖其他Engine。

---

例如：

```text
BaziEngine
不能调用
NameComposer
```

---

所有协作：

统一通过：

```text
ModuleResult
```

完成。

---

## 好处

支持：

* 独立测试
* 独立替换
* 独立升级
* 回退机制

---

# 第七章 失败回退机制

如果：

```text
CultureRetriever失败
```

---

系统：

降级：

```text
核心出处
↓
辅助出处
```

---

如果：

```text
QualityGuard失败
```

---

系统：

自动重新生成。

---

最大重试：

```text
3次
```

---

# 本章结论

系统核心不是：

```text
NameComposer
```

而是：

```text
NameGenerationOrchestrator
```

它负责把：

人格

文化

命理

出处

质量

统一编排。

---

# 第八章 Knowledge Layer（知识库层）

## 8.1 设计目标

Knowledge Layer 是整个系统的事实层（Fact Layer）。

---

职责：

统一管理：

```text
raw 数据源
↓
知识清洗
↓
标准知识库
↓
索引
↓
引擎调用
```

---

系统所有事实：

必须来自：

```text
knowledge_base
```

---

禁止：

```text
AI直接编造
```

---

# 第九章 KnowledgeLoader

## 9.1 定位

统一知识库加载器。

---

路径：

```text
backend/app/core/knowledge_loader.py
```

---

## 9.2 职责

负责：

### 加载知识库

---

### 字段校验

---

### 版本检查

---

### 缓存构建

---

### 审计报告

---

# 9.3 加载顺序

```text
01_compliance_layer

↓

02_char_attribute_layer

↓

03_pronunciation_layer

↓

04_culture_origin_layer

↓

05_name_popularity_layer

↓

06_numerology_layer

↓

07_zodiac_layer

↓

08_surname_layer

↓

09_teochew_layer

↓

10_real_name_layer

↓

11_archetype_layer

↓

12_imagery_layer

↓

13_quality_rules_layer
```

---

## 9.4 启动策略

系统启动时：

一次加载。

---

运行期间：

内存缓存。

---

避免：

频繁读文件。

---

# 第十章 KnowledgeAudit

## 10.1 设计目标

知识库健康检查。

---

避免：

```text
字段缺失

数据损坏

索引失效
```

---

## 10.2 输出

```json
{
  "status":"warning",
  "missing_files":[],
  "missing_fields":[],
  "record_count":0
}
```

---

## 10.3 检查内容

### 文件是否存在

---

### 字段是否齐全

---

### 主键是否重复

---

### 诗词出处是否完整

---

### 潮汕话字段是否缺失

---

### 五行字段是否缺失

---

# 第十一章 CultureIndex

## 11.1 定位

文化出处索引。

---

负责：

快速召回：

```text
诗经

楚辞

唐诗

宋词

四书五经

古文
```

---

## 11.2 目标

避免：

每次生成都遍历全库。

---

# 11.3 索引结构

```json
{
  "char":"棠",
  "origins":[]
}
```

---

### 单字索引

---

### 双字索引

---

### 同句索引

---

### 意象索引

---

### 关键词索引

---

# 第十二章 CultureKnowledgeStore

## 数据结构

```json
{
  "origin_id":"",
  "source":"",
  "title":"",
  "author":"",
  "original_text":"",
  "translation":"",
  "keywords":[],
  "imagery_tags":[]
}
```

---

# 第十三章 TeochewIndex

## 13.1 定位

潮汕话索引库。

---

V1重点支持：

```text
汕头

潮州

揭阳
```

---

## 13.2 功能

支持：

### 单字读音

---

### 双字连读

---

### 姓名整体连读

---

### 风险检测

---

## 13.3 数据结构

```json
{
  "char":"棠",
  "romanization":"",
  "tone":"",
  "ipa":""
}
```

---

# 第十四章 TeochewRiskIndex

## 功能

检测：

```text
不雅谐音

方言禁忌

负面联想
```

---

## 风险等级

```text
LOW

MEDIUM

HIGH

CRITICAL
```

---

## 示例

```json
{
  "phrase":"",
  "risk":"HIGH",
  "reason":"潮汕地区存在明显负面联想"
}
```

---

# 第十五章 NameFrequencyIndex

## 15.1 定位

全国姓名热度库。

---

你的知识库优势之一：

拥有：

```text
全国姓名库

全国重名库
```

---

这是很多GitHub项目没有的。

---

必须充分利用。

---

# 15.2 功能

查询：

### 全国重名人数

---

### 同年龄段热度

---

### 爆款趋势

---

### 风险等级

---

## 示例

```json
{
  "name":"陈梓轩",
  "count":15672,
  "risk":"HIGH"
}
```

---

# 第十六章 CharacterKnowledgeStore

## 设计目标

统一所有汉字属性。

---

## Schema

```json
{
  "char":"棠",

  "stroke":12,

  "wuxing":"木",

  "pinyin":"tang",

  "tone":2,

  "meaning":"海棠",

  "classical_meaning":"棠梨",

  "frequency":0,

  "hot_score":0
}
```

---

# 第十七章 RealNameKnowledgeStore

## 设计目标

整个系统最重要的知识库之一。

---

来源：

```text
历史人物

文学人物

企业家

学者

艺术家
```

---

而不是：

```text
爆款名字
```

---

## 功能

学习：

### 人格结构

---

### 名字结构

---

### 文化结构

---

### 意象结构

---

# 第十八章 ArchetypeKnowledgeStore

## 数据来源

来自：

```text
真实优秀姓名
```

抽象而来。

---

## 数据结构

```json
{
  "archetype":"大家闺秀",

  "imagery":[
    "书卷",
    "草木"
  ],

  "preferred_chars":[],
  "avoid_chars":[]
}
```

---

# 第十九章 ImageryKnowledgeStore

## 设计目标

支持：

意象生成。

---

## 数据结构

```json
{
  "imagery":"书卷",

  "description":"知性、理性、书香",

  "chars":[],

  "related_origins":[]
}
```

---

# 第二十章 MetadataStore

## 功能

管理：

知识库版本。

---

## 数据结构

```json
{
  "dataset":"",
  "version":"",
  "updated_at":"",
  "record_count":0
}
```

---

# 第二十一章 知识库更新机制

## 数据流

```text
Raw Source

↓

Cleaning

↓

Normalize

↓

Validate

↓

Knowledge Base

↓

Index Build

↓

Production
```

---

## 原则

禁止：

```text
AI直接写入知识库
```

---

必须：

```text
人工审核
```

后才能进入正式库。

---

# 第二十二章 Knowledge Layer 总结

Knowledge Layer 提供：

```text
事实

知识

出处

读音

规则
```

---

它不负责：

```text
推理
```

---

推理交给：

```text
Engine Layer
```

完成。

---

# 本章结论

Knowledge Layer 是：

```text
系统大脑中的长期记忆
```

---

而：

Engine Layer 是：

```text
系统的大脑
```

---

下一层：

```text
Intelligence Layer
```

将负责：

```text
人格推理

命理推理

文化推理

名字生成
```

---

# 第二十三章 Intelligence Layer（智能决策层）

## 23.1 设计目标

Intelligence Layer 是整个系统的核心竞争力。

---

Knowledge Layer 提供：

```text id="f1d8am"
事实
```

---

Intelligence Layer 负责：

```text id="2m6lhf"
推理
```

---

例如：

Knowledge Layer 只知道：

```text id="4w7wgh"
棠

五行=木

意象=草木
```

---

但：

Intelligence Layer 要判断：

```text id="dr7ihf"
这个宝宝
适不适合棠
```

---

# 第二十四章 Engine Bus 架构

## 24.1 设计原则

所有引擎：

统一接入：

```text id="3m9sso"
EngineBus
```

---

禁止：

```text id="n4fh9l"
Engine A
直接调用
Engine B
```

---

统一：

```text id="jl6gso"
Input

↓

Engine

↓

ModuleResult

↓

EngineBus
```

---

# 第二十五章 ArchetypeEngine

## 25.1 定位

人格原型推理引擎。

---

整个系统第一决策引擎。

---

负责回答：

```text id="s0h64u"
孩子未来更适合什么人格气质？
```

---

而不是：

```text id="1ztm3r"
缺什么五行？
```

---

## 25.2 输入

```json id="08vk94"
{
  "gender":"female",

  "birth_place":"汕头",

  "style_preferences":[
    "知性",
    "诗意",
    "高级"
  ]
}
```

---

## 25.3 输出

```json id="2fclj4"
{
  "大家闺秀":48,

  "书卷学者":30,

  "温柔坚定":12,

  "现代高级":10
}
```

---

## 25.4 计算维度

### 用户偏好

---

### 性别

---

### 地域文化

---

### 家族偏好

---

### 风格标签

---

# 第二十六章 ImageryEngine

## 26.1 定位

意象推理引擎。

---

职责：

将人格原型转换为：

文化意象。

---

例如：

```text id="i0xjv0"
大家闺秀
```

↓

```text id="7xx7yj"
书卷
草木
明月
```

---

## 26.2 输入

```json id="7qrrhf"
{
  "大家闺秀":48,

  "书卷学者":30
}
```

---

## 26.3 输出

```json id="yjlwmv"
{
  "书卷":42,

  "草木":33,

  "明月":15,

  "清风":10
}
```

---

## 26.4 原则

意象优先。

汉字次之。

---

禁止：

```text id="j0v3vk"
先选字
再解释
```

---

# 第二十七章 BaziEngine

## 27.1 定位

八字分析引擎。

---

项目核心引擎之一。

---

权重默认：

```text id="7cbp1g"
35%
```

---

允许用户自定义。

---

## 27.2 输入

```json id="z5xzk9"
{
  "birth_datetime":"",
  "calendar_type":"solar",
  "birth_place":"汕头"
}
```

---

## 27.3 输出

```json id="5ykfw6"
{
  "day_master":"乙木",

  "five_elements":{},

  "yongshen":[],

  "xishen":[],

  "jishen":[],

  "analysis":""
}
```

---

## 27.4 设计原则

必须：

展示过程。

---

禁止：

```text id="ghkln0"
只给结果
```

---

必须解释：

```text id="4s0h5q"
为什么缺木

为什么喜火

为什么忌金
```

---

# 第二十八章 ZodiacEngine

## 定位

生肖分析引擎。

---

## 功能

支持：

### 生肖喜用

---

### 生肖忌用

---

### 偏旁过滤

---

### 生肖评分

---

## 输出

```json id="h9jv6f"
{
  "animal":"马",

  "preferred_radicals":[],

  "avoid_radicals":[],

  "score":92
}
```

---

# 第二十九章 WugeEngine

## 定位

三才五格分析引擎。

---

默认权重：

```text id="yg1bcs"
25%
```

---

允许：

用户调整。

---

## 输出

```json id="oqkqwy"
{
  "tiange":0,

  "renge":0,

  "dige":0,

  "waige":0,

  "zongge":0,

  "sancai":""
}
```

---

## 输出要求

必须解释：

### 什么是五格

---

### 为什么这样算

---

### 对应什么意义

---

# 第三十章 FortuneFusionEngine

## 定位

命理融合引擎。

---

职责：

统一：

```text id="u4esvd"
八字

生肖

五格
```

---

避免：

三个引擎互相冲突。

---

## 输出

```json id="0m5t3r"
{
  "recommended_elements":[],

  "avoid_elements":[],

  "preferred_chars":[],

  "avoid_chars":[]
}
```

---

# 第三十一章 CultureRetriever

## 定位

出处召回引擎。

---

职责：

寻找：

最契合当前人格原型的出处。

---

## 检索顺序

### 双字直接出处

---

### 同句出处

---

### 同篇出处

---

### 意象出处

---

### 关联出处

---

## 输出

```json id="itx0j8"
{
  "origins":[]
}
```

---

# 第三十二章 CharPoolBuilder

## 定位

候选字池构建器。

---

系统核心模块。

---

## 输入来源

### ArchetypeEngine

---

### ImageryEngine

---

### BaziEngine

---

### ZodiacEngine

---

### WugeEngine

---

### User Preference

---

## 字池结构

```text id="0obx40"
合规字池

↓

命理字池

↓

意象字池

↓

出处字池

↓

偏好字池

↓

最终字池
```

---

# 第三十三章 字池过滤规则

## 一级过滤

强制淘汰

---

### 禁用字

---

### 违法违规字

---

### 谐音高风险

---

### 潮汕话高风险

---

## 二级过滤

降权

---

### 爆款字

---

### 高频字

---

### 网红字

---

## 三级过滤

审美过滤

---

### 结构重复

---

### 意象重复

---

### 人格冲突

---

# 第三十四章 ModuleResult统一协议

所有引擎输出：

统一格式。

---

```json id="7r3j2q"
{
  "module_id":"",

  "score":0,

  "weight":0,

  "analysis":"",

  "warnings":[],

  "metadata":{}
}
```

---

# 第三十五章 Intelligence Layer 总结

这一层负责：

```text id="h5h68i"
人格推理

文化推理

命理推理

出处推理
```

---

这是：

```text id="e6j7g8"
博士级命名系统
```

与：

```text id="m7k5xw"
GitHub起名脚本
```

最大的区别。

---

# 第三十六章 Name Generation Layer（姓名生成层）

## 36.1 设计目标

这是系统最终产生名字的核心层。

---

职责：

将：

```text id="0ep4lq"
人格原型

文化意象

命理分析

出处系统

候选字池
```

转换为：

```text id="gwjtr7"
高质量姓名方案
```

---

## 设计原则

禁止：

```text id="i5kpfd"
随机组合
```

---

禁止：

```text id="ok97zb"
高分字+高分字
```

---

禁止：

```text id="bvdk17"
模板化批量输出
```

---

必须：

```text id="mkk7nd"
结构优先

意象优先

人格优先

命理校验
```

---

# 第三十七章 CandidateGenerator

## 37.1 定位

候选方案生成器。

---

职责：

生成：

```text id="4h6r7x"
100~300个
初始姓名候选
```

---

供后续：

```text id="gnrf6k"
Scorer

QualityGuard
```

筛选。

---

## 37.2 输入

```json id="js2mgi"
{
  "archetype": {},
  "imagery": {},
  "char_pool": {}
}
```

---

## 37.3 输出

```json id="n5m8ow"
{
  "candidate_names": []
}
```

---

# 第三十八章 NameComposer

## 38.1 定位

姓名结构生成器。

---

系统最重要模块之一。

---

职责：

生成：

```text id="vudc2y"
姓名结构
```

而不是：

```text id="s7uj4m"
汉字组合
```

---

# 38.2 结构优先原则

系统先生成：

```text id="4ejv9v"
书卷+草木

君子+光明

山水+书卷
```

---

再映射：

汉字。

---

例如：

```text id="0mpsje"
书卷+草木
```

↓

```text id="qzzh9r"
知
+
棠
```

↓

```text id="3wuv9l"
知棠
```

---

# 38.3 禁止行为

禁止：

```text id="jjz3wy"
棠
+
宁
```

因为：

两字高分。

直接组合。

---

系统必须知道：

```text id="b1fklz"
为什么组合
```

---

# 第三十九章 StructureTemplate Engine

## 39.1 定位

名字结构模板引擎。

---

来源：

```text id="8tt9y2"
Naming Philosophy
```

---

## V1支持结构

### 书卷+草木

---

### 书卷+山水

---

### 君子+光明

---

### 山水+光明

---

### 书卷+时间

---

### 草木+光明

---

### 君子+山水

---

## 输出格式

```json id="uhqg4g"
{
  "template":"书卷+草木",

  "weight":95
}
```

---

# 第四十章 DiversityEngine

## 40.1 定位

多样性控制引擎。

---

这是防止：

```text id="t4z9bh"
知棠

知兰

知芷

知若
```

出现的核心模块。

---

## 40.2 规则

同批结果：

禁止：

### 同首字过多

---

### 同尾字过多

---

### 同结构过多

---

### 同意象过多

---

### 同人格过多

---

# 40.3 输出要求

Top10结果：

至少覆盖：

```text id="jlwmgc"
3种以上人格原型

4种以上意象结构

3种以上结构模板
```

---

# 第四十一章 CandidateDeduplicator

## 定位

候选去重引擎。

---

职责：

消除：

```text id="6uv6vu"
知棠

知堂

知唐
```

---

这种：

语义高度重复。

---

## 去重维度

### 字面重复

---

### 读音重复

---

### 意象重复

---

### 人格重复

---

# 第四十二章 NameScorer

## 42.1 定位

姓名评分引擎。

---

职责：

排序。

---

不是：

决定好坏。

---

## 42.2 默认评分体系

支持：

用户自定义。

---

默认：

```text id="euj8oo"
八字：35

五格：25

文化：15

审美：10

普通话：5

潮汕话：5

重名：5
```

---

总计：

```text id="f8jmln"
100
```

---

# 42.3 一级评分

硬规则

---

例如：

```text id="cc54an"
违法违规

不良谐音

高风险方言
```

---

直接淘汰。

---

# 42.4 二级评分

命理评分

---

来自：

```text id="z3zhcl"
BaziEngine

ZodiacEngine

WugeEngine
```

---

# 42.5 三级评分

文化评分

---

来自：

```text id="z9lbxn"
出处质量

出处匹配度

意象质量
```

---

# 42.6 四级评分

审美评分

---

来自：

```text id="uk3s38"
结构质量

人格匹配

自然度
```

---

# 第四十三章 Naturalness Engine

## 43.1 定位

自然度引擎。

---

整个系统隐藏核心。

---

因为：

很多名字：

合规。

有出处。

有五格。

---

但：

不像真人名字。

---

# 43.2 学习来源

来自：

```text id="4q1o2g"
全国姓名库

历史人物库

学者姓名库

企业家姓名库
```

---

不是：

爆款名字库。

---

# 43.3 输出

```json id="djgojs"
{
  "naturalness":92
}
```

---

# 第四十四章 Top3精品机制

## 定位

最终核心结果。

---

系统最终展示：

```text id="n55jbi"
3个精品名字
```

---

每个名字：

必须满足：

### 高命理适配

---

### 高文化质量

---

### 高自然度

---

### 高解释质量

---

## 输出

```json id="qvhb22"
{
  "top_names":[]
}
```

---

# 第四十五章 Backup7机制

## 定位

备用候选。

---

如果：

用户不满意。

---

可快速切换。

---

## 输出

```json id="dqtq8j"
{
  "backup_names":[]
}
```

---

# 第四十六章 Regeneration机制

## 支持

用户点击：

```text id="0u9h6f"
换一批
```

---

系统：

不允许：

```text id="t7xhll"
重复生成
```

---

必须：

锁定：

```text id="jl9j86"
已展示结构

已展示字

已展示意象
```

---

重新生成。

---

# 第四十七章 Name Generation Layer 总结

这一层负责：

```text id="qgkzwm"
生成名字
```

---

但生成依据不是：

```text id="7aok7l"
字
```

---

而是：

```text id="rmc9zm"
人格

意象

结构

命理

文化
```

---

因此：

系统输出的是：

```text id="gm4f6r"
姓名方案
```

而不是：

```text id="i7ps9k"
姓名字符串
```

---

# 第四十八章 Quality Layer（质量审查层）

## 48.1 设计目标

Quality Layer 是整个系统的最终裁判。

---

职责：

确保：

```text id="4n0i4t"
所有展示给用户的名字
都符合易元命名标准
```

---

如果：

```text id="hr4c1v"
NameComposer
生成100个名字
```

---

Quality Layer 有权：

```text id="3m0f4u"
淘汰95个
```

---

只保留：

真正符合标准的姓名方案。

---

# 第四十九章 QualityGuard

## 49.1 定位

系统最终守门员。

---

职责：

检查：

```text id="m6f72z"
名字是否真的合格
```

---

而不是：

```text id="3ylhhy"
评分是否高
```

---

## 49.2 审查顺序

```text id="0ydw6z"
合规审查

↓

命理审查

↓

读音审查

↓

文化审查

↓

结构审查

↓

自然度审查

↓

解释质量审查
```

---

# 第五十章 Compliance Guard

## 检查内容

### 国家规范汉字

---

### 禁用字

---

### 生僻字

---

### 敏感字

---

### 违规字

---

## 输出

```json id="v0tzca"
{
  "passed": true,
  "issues": []
}
```

---

# 第五十一章 Pronunciation Guard

## 普通话检查

检查：

### 声母重复

---

### 韵母重复

---

### 三连同调

---

### 绕口

---

### 不雅谐音

---

## 潮汕话检查

检查：

### 单字读音

---

### 连读读音

---

### 地域禁忌

---

### 不雅联想

---

## 示例

```text id="ynz8ig"
陈诗诗
```

---

可能出现：

```text id="7v58f6"
连续发音过密
```

---

降权。

---

# 第五十二章 Culture Guard

## 设计目标

确保：

出处真实。

---

## 检查内容

### 是否存在出处

---

### 是否直接出处

---

### 是否同句出处

---

### 是否意象关联

---

### 是否伪出处

---

## 禁止

```text id="5azg8f"
AI编造出处
```

---

## 输出

```json id="tq7m8e"
{
  "origin_quality": 92
}
```

---

# 第五十三章 Structure Guard

## 设计目标

确保：

名字结构成立。

---

## 检查内容

### 人格结构

---

### 意象结构

---

### 文化结构

---

### 组合合理性

---

## 示例

允许：

```text id="h6u8t3"
知棠

修舟

允昭
```

---

不推荐：

```text id="d7o4z0"
棠兰

仁德

昭曜
```

---

原因：

结构重复。

---

# 第五十四章 Naturalness Guard

## 设计目标

防止：

机器名。

---

## 判断依据

### 全国姓名库

---

### 历史人物库

---

### 学者姓名库

---

### 企业家姓名库

---

## 输出

```json id="c2r9xq"
{
  "naturalness": 91
}
```

---

## 低于阈值

```text id="4t4xzu"
80
```

---

自动淘汰。

---

# 第五十五章 HotName Guard

## 设计目标

避免：

爆款名字堆叠。

---

## 检查内容

### 爆款字

---

### 高频字

---

### 热门组合

---

## 原则

不禁止。

---

降权。

---

例如：

```text id="4b65jw"
梓
轩
宸
熙
诺
```

---

参与评分。

但降低优先级。

---

# 第五十六章 ExplainEngine

## 设计目标

生成：

用户能看懂的解释。

---

不是：

命理师术语。

---

## 输入

```json id="f3e6lo"
{
  "name":"陈知棠"
}
```

---

## 输出

```json id="4bq4hj"
{
  "summary":""
}
```

---

# 解释原则

必须：

### 有依据

---

### 可验证

---

### 可理解

---

禁止：

```text id="i2e3wv"
命格极佳

福禄双全

大富大贵
```

---

# 第五十七章 ConsultantReport Engine

## 定位

顾问报告生成器。

---

付费产品核心。

---

## 报告组成

### 姓名总览

---

### 八字分析

---

### 五行分析

---

### 生肖分析

---

### 五格分析

---

### 人格原型分析

---

### 文化出处分析

---

### 普通话分析

---

### 潮汕话分析

---

### 重名分析

---

### 顾问建议

---

## 报告目标

用户读完后：

能够理解：

```text id="3gw9v5"
为什么推荐这个名字
```

---

而不是：

```text id="9v8i53"
只看到一个分数
```

---

# 第五十八章 Retry Engine

## 设计目标

失败自动重试。

---

## 触发条件

### QualityGuard失败

---

### 出处不足

---

### 潮汕话高风险

---

### 自然度不足

---

### 解释质量不足

---

## 重试策略

```text id="2k5n1j"
重新选结构

↓

重新选意象

↓

重新选字

↓

重新评分
```

---

## 最大次数

```text id="m1j5u4"
3次
```

---

# 第五十九章 Golden Cases

## 设计目标

保证系统长期稳定。

---

每次发布前：

必须跑：

```text id="x4d7b3"
Golden Cases
```

---

## V1测试集

### 男宝

---

### 女宝

---

### 潮汕地区

---

### 双胞胎

---

### 龙凤胎

---

### 农历

---

### 闰月

---

### 复姓

---

### 喜欢字

---

### 禁用字

---

## 校验项

### 是否生成名字

---

### 是否有出处

---

### 是否有八字分析

---

### 是否有潮汕话分析

---

### 是否通过QualityGuard

---

# 第六十章 Quality Layer 总结

Quality Layer 是：

```text id="9m2d0l"
系统最后一道防线
```

---

它保证：

系统不会因为：

```text id="97wzkr"
新增知识库

新增规则

新增功能
```

而退化。

---

# 本章结论

易元命名最终交付的：

不是：

```text id="5l7m1z"
生成结果
```

---

而是：

```text id="m7j4vp"
经过严格审查的姓名方案
```

---

因此：

```text id="j4h3tn"
QualityGuard
```

的重要性：

不低于：

```text id="s8m4kp"
BaziEngine
```

---

# 第六十一章 Presentation Layer（前端展示层）

## 61.1 设计目标

前端不是算命工具界面。

---

不是：

```text id="8a3e21"
复杂
神神叨叨
充满玄学
```

---

而是：

```text id="7b2f19"
专业
清晰
顾问式
```

---

用户打开后应该感觉：

```text id="6e4c55"
正在咨询一位专业命名顾问
```

而不是：

```text id="2f6d84"
正在使用一个算命网站
```

---

# 第六十二章 MVP 页面规划

## Page 1

宝宝信息填写页

---

路径：

```text id="8f8c32"
/
```

---

输入项：

### 姓氏

---

### 性别

---

### 出生日期

---

### 出生时间

---

### 出生城市

---

### 阳历/农历

---

### 闰月

---

### 名字字数

---

### 喜欢字

---

### 禁用字

---

### 风格偏好

---

### 命名侧重

---

# Page 2

分析过程页

---

路径：

```text id="4c0d55"
/analysis
```

---

展示：

```text id="7a7e01"
正在分析八字

正在构建人格画像

正在召回文化出处

正在生成姓名方案
```

---

增强专业感。

---

# Page 3

姓名结果页

---

路径：

```text id="5d5c78"
/result
```

---

展示：

### Top3精品方案

---

### Backup7备选方案

---

### 综合评分

---

### 一句话推荐

---

### 重名风险

---

### 潮汕话风险

---

### 点击查看详情

---

# Page 4

姓名详情页

---

路径：

```text id="9b0b22"
/name/[id]
```

---

展示：

### 名字释义

---

### 出处解析

---

### 八字适配

---

### 五格分析

---

### 生肖分析

---

### 普通话分析

---

### 潮汕话分析

---

### 顾问建议

---

# Page 5

收藏对比页

---

路径：

```text id="4e7c91"
/compare
```

---

支持：

### 多名字对比

---

### 导出PDF

---

### 收藏

---

# 第六十三章 UX设计原则

## 原则一

小白友好

---

用户不需要懂：

```text id="8a7f66"
天格

人格

地格

喜用神
```

---

系统必须解释：

```text id="5b4d91"
是什么

为什么

有什么影响
```

---

## 原则二

顾问式输出

---

禁止：

```text id="1a6e44"
分数堆砌
```

---

必须：

```text id="3f6d73"
解释
建议
原因
```

---

## 原则三

结果优先

---

用户先看到：

```text id="2c7b66"
名字
```

---

再深入查看：

```text id="6e5f81"
命理
文化
出处
```

---

# 第六十四章 API Layer

## 64.1 设计目标

统一API入口。

---

技术栈：

```text id="8d7c11"
FastAPI
```

---

# 64.2 核心接口

## POST

```text id="4a1e88"
/api/names/generate
```

---

功能：

生成姓名。

---

## GET

```text id="7d3c02"
/api/names/{request_id}
```

---

获取结果。

---

## POST

```text id="2e5f47"
/api/names/regenerate
```

---

换一批。

---

## POST

```text id="9f1b65"
/api/favorites
```

---

收藏姓名。

---

## GET

```text id="1b4f38"
/api/favorites
```

---

读取收藏。

---

# 第六十五章 Storage Layer

## V1

SQLite

---

理由：

```text id="3d8c27"
简单

稳定

开发快
```

---

# V2

PostgreSQL

---

支持：

```text id="5c9d14"
用户系统

支付

报告系统
```

---

# 第六十六章 Deployment Architecture

## 本地开发

```text id="4b6e82"
Next.js

FastAPI

SQLite
```

---

## 测试环境

```text id="2f1d90"
Docker Compose
```

---

## 生产环境

```text id="6d5f11"
Nginx

Next.js

FastAPI

PostgreSQL

Redis
```

---

# 第六十七章 数据流总图

```text id="8c4d53"
UserInput

↓

BabyProfile

↓

ArchetypeEngine

↓

ImageryEngine

↓

BaziEngine

↓

ZodiacEngine

↓

WugeEngine

↓

FortuneFusionEngine

↓

CultureRetriever

↓

CharPoolBuilder

↓

NameComposer

↓

NameScorer

↓

QualityGuard

↓

ConsultantReport

↓

Frontend
```

---

# 第六十八章 开发阶段规划

## Phase 0

项目初始化

---

## Phase 1

Knowledge Loader

---

## Phase 2

Character Service

---

## Phase 3

Baby Profile

---

## Phase 4

Bazi Engine

---

## Phase 5

Archetype Engine

---

## Phase 6

Imagery Engine

---

## Phase 7

Culture Retriever

---

## Phase 8

Char Pool Builder

---

## Phase 9

Name Composer

---

## Phase 10

Name Scorer

---

## Phase 11

Quality Guard

---

## Phase 12

API

---

## Phase 13

Frontend MVP

---

# 第六十九章 MVP边界

## V1必须完成

### 八字

---

### 生肖

---

### 五格

---

### 潮汕话

---

### 诗词出处

---

### 人格原型

---

### 文化意象

---

### Top3精品名字

---

### Backup7名字

---

# V1禁止新增

### AI聊天

---

### Agent系统

---

### 支付

---

### 会员

---

### 海报

---

### 分享裂变

---

# 第七十章 V2规划

## 增加

### 双胞胎命名

---

### 龙凤胎命名

---

### 预产期命名

---

### 成人改名

---

### 企业命名

---

### 品牌命名

---

# 第七十一章 V3规划

## 增加

### 紫微斗数

---

### 奇门遁甲

---

### 家谱辈分系统

---

### 多方言系统

---

### 海外华人命名

---

# 第七十二章 系统架构总结

易元命名采用：

```text id="1d8a52"
Knowledge First

Rule Driven

AI Assisted
```

---

系统核心公式：

```text id="7c5f34"
人格原型

+

文化意象

+

名字结构

+

命理校验

+

质量审查

=

高质量姓名方案
```

---

与传统起名系统最大的区别：

传统系统：

```text id="9e2b44"
八字

↓

选字

↓

组合
```

---

易元命名：

```text id="3b7d51"
宝宝画像

↓

人格原型

↓

文化意象

↓

名字结构

↓

出处召回

↓

命理校验

↓

质量审查

↓

顾问报告
```

---

因此：

系统最终输出的不是：

```text id="5d9f63"
名字
```

---

而是：

```text id="8c1b29"
姓名决策方案
```

---

# 文档状态

```text id="2f7d85"
Approved For Development Planning
```
