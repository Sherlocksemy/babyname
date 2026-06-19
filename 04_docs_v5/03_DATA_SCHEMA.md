# 易元命名 Pro

# DATA SCHEMA

Version 1.0

---

# 文档定位

本文件定义：

```text
全系统数据模型
```

---

作用：

连接：

```text
02A Philosophy

02D Structure

02C Archetype

02E Prompt

02F Orchestration

02B NES
```

---

目标：

实现：

```text
可存储

可追踪

可审计

可回归
```

---

# 第一章 Data Architecture

## 1.1 数据原则

系统中的任何结果：

必须：

```text
有来源
```

---

任何评分：

必须：

```text
可追溯
```

---

任何名字：

必须：

```text
可重建
```

---

# 1.2 数据层级

```text
User

↓

Session

↓

Context

↓

Candidate

↓

Score

↓

Ranking

↓

Report
```

---

# 第二章 Core Entity Model

## 核心实体

系统包含：

```text
User
```

---

```text
NamingSession
```

---

```text
NamingContext
```

---

```text
Structure
```

---

```text
Archetype
```

---

```text
Culture
```

---

```text
Candidate
```

---

```text
NESScore
```

---

```text
Ranking
```

---

```text
Report
```

---

# 第三章 Naming Session

## 定义

一次完整命名过程：

称为：

```text
Naming Session
```

---

# Schema

```json
{
  "session_id":"SID_001",

  "status":"RUNNING",

  "created_at":"2026-06-20",

  "completed_at":null,

  "version":"v1.0.0"
}
```

---

# Status

允许：

```text
INIT
```

---

```text
RUNNING
```

---

```text
FAILED
```

---

```text
COMPLETED
```

---

```text
ARCHIVED
```

---

# 第四章 User Profile Schema

## 定位

用户输入层。

---

# Schema

```json
{
  "surname":"林",

  "gender":"male",

  "birth_date":"2025-03-01",

  "birth_time":"08:30",

  "birth_location":"广东汕头",

  "region":"teochew"
}
```

---

# 字段定义

## surname

姓氏。

---

## gender

```text
male

female
```

---

## region

支持：

```text
teochew

hakka

cantonese

minnan

general
```

---

# 第五章 Fortune Context Schema

## 定位

命理分析结果。

---

# Schema

```json
{
  "fortune_id":"FORTUNE_001",

  "favorable_elements":[
    "木",
    "水"
  ],

  "avoid_elements":[
    "火"
  ]
}
```

---

# 说明

该层：

```text
不直接生成名字
```

---

只提供：

```text
约束条件
```

---

# 第六章 Structure Schema

## 来源

```text
02D_STRUCTURE_LIBRARY
```

---

# Schema

```json
{
  "structure_id":"S06",

  "structure_name":"书卷型",

  "confidence":92,

  "reason":"..."
}
```

---

# 字段

## structure_id

唯一ID。

---

例如：

```text
S01

S02

S03

...
```

---

# 第七章 Archetype Schema

## 来源

```text
02C_ARCHETYPE_MATRIX
```

---

# Schema

```json
{
  "archetype_id":"A01",

  "archetype_name":"书卷学者",

  "confidence":94
}
```

---

# 关系

```text
Structure

↓

Archetype
```

---

# 示例

```text
S06

↓

A01
```

---

# 第八章 Culture Schema

## 来源

```text
02A_NAMING_PHILOSOPHY
```

---

# Schema

```json
{
  "culture_id":"C01",

  "culture_name":"论语",

  "source_quote":"见微知著",

  "culture_depth":91
}
```

---

# 原则

Culture：

必须来自：

```text
文化路径库
```

---

禁止：

```text
AI即时创造
```

---

# 第九章 Naming Context

## 定位

统一上下文对象。

---

# Schema

```json
{
  "session_id":"SID001",

  "profile":{},

  "fortune":{},

  "structure":{},

  "archetype":{},

  "culture":{}
}
```

---

# 原则

所有Agent：

读取：

```text
Naming Context
```

---

禁止：

```text
直接访问数据库
```

---

# 第十章 Context Versioning

## Schema

```json
{
  "context_version":"v1.0.0",

  "updated_at":"..."
}
```

---

# 用途

支持：

```text
回归测试
```

---

```text
版本追踪
```

---

```text
审计
```

---

# 文档状态

```text
Draft Complete
```

---

# Part 1 End

# 第十一章 Candidate Schema

## 11.1 定位

定义：

```text id="a1m8q2"
候选名字对象
```

---

来源：

```text id="b2v7m4"
Generator Engine
```

---

作用：

作为：

```text id="c3m8q5"
全流程核心实体
```

---

# 11.2 Schema

```json id="d4v7m1"
{
  "candidate_id":"CID_001",

  "name":"知微",

  "surname":"林",

  "full_name":"林知微",

  "generation_batch":"B001",

  "status":"GENERATED"
}
```

---

# Candidate ID规则

格式：

```text id="e5m8q3"
CID_000001
```

---

全局唯一。

---

禁止：

```text id="f6v7m2"
重复ID
```

---

# 第十二章 Candidate Metadata

## 定位

记录：

```text id="g7m8q4"
候选生成信息
```

---

# Schema

```json id="h8v3m5"
{
  "candidate_id":"CID_001",

  "generator_version":"v1.0.0",

  "prompt_version":"v1.0.0",

  "generated_at":"..."
}
```

---

# 用途

支持：

```text id="i9m7q1"
回归测试
```

---

```text id="j1v8m2"
问题追踪
```

---

```text id="k2m7q4"
Prompt审计
```

---

# 第十三章 Candidate Semantic Schema

## 定位

记录：

```text id="l3v8m5"
名字语义结构
```

---

# Schema

```json id="m4v7m1"
{
  "candidate_id":"CID_001",

  "structure_id":"S06",

  "archetype_id":"A01",

  "culture_id":"C01"
}
```

---

# 原则

任何名字：

必须绑定：

```text id="n5m8q2"
Structure
```

---

```text id="o6v7m4"
Archetype
```

---

```text id="p7m8q5"
Culture
```

---

# 禁止

```text id="q8v7m1"
孤立名字
```

---

# 第十四章 Candidate Pool Schema

## 定位

定义：

```text id="r9m8q3"
候选池
```

---

# Schema

```json id="s1v7m2"
{
  "pool_id":"POOL_001",

  "session_id":"SID_001",

  "candidate_count":200
}
```

---

# 组成

```text id="t2m8q4"
200 Candidate
```

---

# 生命周期

```text id="u3v8m5"
Generated

↓

Filtered

↓

Scored

↓

Ranked
```

---

# 第十五章 Generation Batch Schema

## 定位

定义：

```text id="v4m7q1"
批次生成
```

---

# Schema

```json id="w5m8q2"
{
  "batch_id":"B001",

  "generated_count":200,

  "generator_version":"v1.0.0"
}
```

---

# 作用

支持：

```text id="x6v7m4"
批量追踪
```

---

```text id="y7m8q5"
批量回归
```

---

# 第十六章 Candidate Lifecycle Schema

## 生命周期状态

```text id="z8v7m1"
GENERATED
```

---

```text id="a9m8q3"
VALIDATED
```

---

```text id="b1v7m2"
CRITIQUED
```

---

```text id="c2m8q4"
SCORED
```

---

```text id="d3v8m5"
TOP20
```

---

```text id="e4m7q1"
TOP10
```

---

```text id="f5m8q2"
TOP3
```

---

```text id="g6v7m4"
TOP1
```

---

```text id="h7m8q5"
REJECTED
```

---

# 第十七章 Lifecycle Audit Schema

## 定位

记录：

```text id="i8v7m1"
每一次状态变化
```

---

# Schema

```json id="j9m8q3"
{
  "candidate_id":"CID_001",

  "from":"GENERATED",

  "to":"VALIDATED",

  "timestamp":"..."
}
```

---

# 原则

任何状态变化：

必须记录。

---

禁止：

```text id="k1v7m2"
无日志变更
```

---

# 第十八章 Rejection Schema

## 定位

记录：

```text id="l2m8q4"
淘汰原因
```

---

# Schema

```json id="m3v8m5"
{
  "candidate_id":"CID_001",

  "rejected":true,

  "reason":"AI_TEMPLATE"
}
```

---

# 枚举

```text id="n4m7q1"
AI_TEMPLATE
```

---

```text id="o5m8q2"
LOW_AESTHETIC
```

---

```text id="p6v7m4"
LOW_HUMAN_SCORE
```

---

```text id="q7m8q5"
LOW_NES
```

---

```text id="r8v7m1"
STRUCTURE_FAIL
```

---

```text id="s9m8q3"
ARCHETYPE_FAIL
```

---

```text id="t1v7m2"
CULTURE_FAIL
```

---

# 第十九章 Candidate Diversity Schema

## 定位

记录：

```text id="u2m8q4"
多样性分析
```

---

# Schema

```json id="v3v8m5"
{
  "candidate_id":"CID_001",

  "structure_group":"S06",

  "archetype_group":"A01",

  "culture_group":"C01"
}
```

---

# 用途

支持：

```text id="w4m7q1"
Diversity Guard
```

---

# 第二十章 Candidate Provenance Schema

## 定位

记录：

```text id="x5m8q2"
名字来源链
```

---

# Schema

```json id="y6v7m4"
{
  "candidate_id":"CID_001",

  "structure_id":"S06",

  "archetype_id":"A01",

  "culture_id":"C01",

  "generation_batch":"B001"
}
```

---

# 用途

回答：

```text id="z7m8q5"
为什么生成这个名字？
```

---

支持：

```text id="a8v7m1"
Explainability
```

---

# 文档状态

```text id="b9m8q3"
Draft Complete
```

---

# Part 2 End

# 第二十一章 Critique Schema

## 21.1 定位

定义：

```text id="a1m8q2"
Critique Layer数据结构
```

---

来源：

```text id="b2v7m4"
02E Prompt Architecture
```

↓

```text id="c3m8q5"
Critique Engine
```

---

作用：

记录：

```text id="d4v7m1"
名字被如何审查
```

---

# 21.2 Schema

```json id="e5m8q3"
{
  "candidate_id":"CID_001",

  "critique_id":"CRI_001",

  "passed":true,

  "created_at":"..."
}
```

---

# 第二十二章 Self Critique Schema

## 定位

记录：

```text id="f6v7m2"
自我批判结果
```

---

# Schema

```json id="g7m8q4"
{
  "candidate_id":"CID_001",

  "self_critique_passed":true,

  "issues":[]
}
```

---

# Issues

允许：

```text id="h8v3m5"
STRUCTURE_WEAK
```

---

```text id="i9m7q1"
ARCHETYPE_WEAK
```

---

```text id="j1v8m2"
CULTURE_WEAK
```

---

```text id="k2m7q4"
MEANING_WEAK
```

---

# 第二十三章 Red Team Schema

## 定位

记录：

```text id="l3v8m5"
反方审查
```

---

# Schema

```json id="m4v7m1"
{
  "candidate_id":"CID_001",

  "novel_risk":10,

  "idol_drama_risk":5,

  "marketing_risk":0,

  "overall_risk":"LOW"
}
```

---

# 风险等级

```text id="n5m8q2"
LOW
```

---

```text id="o6v7m4"
MEDIUM
```

---

```text id="p7m8q5"
HIGH
```

---

# 第二十四章 Template Detection Schema

## 定位

记录：

```text id="q8v7m1"
模板命中情况
```

---

# Schema

```json id="r9m8q3"
{
  "candidate_id":"CID_001",

  "template_detected":false,

  "template_type":null
}
```

---

# Template Type

允许：

```text id="s1v7m2"
PREFIX
```

---

```text id="t2m8q4"
SUFFIX
```

---

```text id="u3v8m5"
SEMANTIC
```

---

```text id="v4m7q1"
STYLE
```

---

# 第二十五章 Aesthetic Schema

## 定位

记录：

```text id="w5m8q2"
高级感评分
```

---

# Schema

```json id="x6v7m4"
{
  "candidate_id":"CID_001",

  "aesthetic_score":92
}
```

---

# 五维评分

```json id="y7m8q5"
{
  "personality":19,

  "culture":19,

  "structure":18,

  "reality":18,

  "aesthetic":18
}
```

---

总分：

```text id="z8v7m1"
92
```

---

# 第二十六章 Human Detector Schema

## 定位

记录：

```text id="a9m8q3"
真人命名概率
```

---

# Schema

```json id="b1v7m2"
{
  "candidate_id":"CID_001",

  "human_score":91
}
```

---

# 等级

| 分数    | 说明 |
| ----- | -- |
| 95+   | 极高 |
| 90-94 | 高  |
| 80-89 | 中  |
| <80   | 低  |

---

# 第二十七章 Diversity Schema

## 定位

记录：

```text id="c2m8q4"
多样性结果
```

---

# Schema

```json id="d3v8m5"
{
  "candidate_id":"CID_001",

  "diversity_score":93
}
```

---

# 子项

```json id="e4m7q1"
{
  "structure_diversity":95,

  "archetype_diversity":92,

  "culture_diversity":90
}
```

---

# 第二十八章 NES Schema

## 定位

连接：

```text id="f5m8q2"
02B_NAMING_EVALUATION_SYSTEM
```

---

# Schema

```json id="g6v7m4"
{
  "candidate_id":"CID_001",

  "nes_score":91
}
```

---

# 第二十九章 NES Breakdown Schema

## 定位

记录：

```text id="h7m8q5"
评分明细
```

---

# Schema

```json id="i8v7m1"
{
  "culture_score":23,

  "structure_score":18,

  "archetype_score":14,

  "meaning_score":14,

  "phonetic_score":9,

  "fortune_score":5,

  "uniqueness_score":4,

  "bonus_score":4
}
```

---

# 第三十章 NES Version Schema

## 定位

记录：

```text id="j9m8q3"
评分版本
```

---

# Schema

```json id="k1v7m2"
{
  "nes_version":"v1.0.0"
}
```

---

# 用途

支持：

```text id="l2m8q4"
版本回归
```

---

# 第三十一章 Elite Score Schema

## 定位

记录：

```text id="m3v8m5"
大师级评分
```

---

# Schema

```json id="n4m7q1"
{
  "candidate_id":"CID_001",

  "elite_score":90
}
```

---

# 判定

```text id="o5m8q2"
≥90
```

---

标记：

```text id="p6v7m4"
ELITE
```

---

# 第三十二章 Critique Result Schema

## 汇总对象

```json id="q7m8q5"
{
  "candidate_id":"CID_001",

  "self_critique_passed":true,

  "red_team_passed":true,

  "template_passed":true,

  "aesthetic_score":92,

  "human_score":91,

  "diversity_score":93
}
```

---

# 输出

```text id="r8v7m1"
Qualified
```

---

# 第三十三章 Scoring Audit Schema

## 定位

记录：

```text id="s9m8q3"
评分全过程
```

---

# Schema

```json id="t1v7m2"
{
  "candidate_id":"CID_001",

  "scored_at":"...",

  "scoring_version":"v1.0.0"
}
```

---

# 用途

支持：

```text id="u2m8q4"
审计
```

---

```text id="v3v8m5"
回归
```

---

```text id="w4m7q1"
问题追踪
```

---

# 第三十四章 Scoring Philosophy

评分对象：

不是：

```text id="x5m8q2"
名字本身
```

---

而是：

```text id="y6v7m4"
Structure

+

Archetype

+

Culture

↓

名字
```

---

因此：

```text id="z7m8q5"
NES

必须绑定

Structure

Archetype

Culture
```

---

# 文档状态

```text id="a8v7m1"
Draft Complete
```

---

# Part 3 End

# 第三十五章 Ranking Schema

## 35.1 定位

定义：

```text id="a1m8q2"
排序层数据模型
```

---

作用：

连接：

```text id="b2v7m4"
Candidate

↓

NES

↓

Top20

↓

Top10

↓

Top3

↓

Top1
```

---

# 35.2 Ranking Object

## Schema

```json id="c3m8q5"
{
  "ranking_id":"RANK_001",

  "session_id":"SID_001",

  "ranking_version":"v1.0.0",

  "created_at":"..."
}
```

---

# 第三十六章 Ranking Result Schema

## 定位

记录：

```text id="d4v7m1"
排序结果
```

---

# Schema

```json id="e5m8q3"
{
  "candidate_id":"CID_001",

  "rank":1,

  "nes_score":91
}
```

---

# 原则

排序依据：

```text id="f6v7m2"
NES优先
```

---

禁止：

```text id="g7m8q4"
LLM主观喜好
```

---

# 第三十七章 Top20 Schema

## 定位

记录：

```text id="h8v3m5"
Top20结果
```

---

# Schema

```json id="i9m7q1"
{
  "session_id":"SID_001",

  "stage":"TOP20",

  "candidate_ids":[]
}
```

---

# 数量限制

```text id="j1v8m2"
≤20
```

---

# 晋升条件

```text id="k2m7q4"
NES ≥75
```

---

```text id="l3v8m5"
Structure ≥14
```

---

```text id="m4v7m1"
Archetype ≥12
```

---

```text id="n5m8q2"
Culture ≥18
```

---

# 第三十八章 Top10 Schema

## 定位

记录：

```text id="o6v7m4"
Top10结果
```

---

# Schema

```json id="p7m8q5"
{
  "session_id":"SID_001",

  "stage":"TOP10",

  "candidate_ids":[]
}
```

---

# 晋升条件

```text id="q8v7m1"
NES ≥82
```

---

```text id="r9m8q3"
Aesthetic ≥85
```

---

```text id="s1v7m2"
Human ≥88
```

---

# 第三十九章 Top3 Schema

## 定位

最终推荐层。

---

# Schema

```json id="t2m8q4"
{
  "session_id":"SID_001",

  "top3":[
    "CID_001",
    "CID_002",
    "CID_003"
  ]
}
```

---

# 数据结构

```json id="u3v8m5"
{
  "top1":"CID_001",

  "top2":"CID_002",

  "top3":"CID_003"
}
```

---

# 第四十章 Top3 Diversity Schema

## 定位

记录：

```text id="v4m7q1"
Top3多样性
```

---

# Schema

```json id="w5m8q2"
{
  "diversity_score":93,

  "structure_diversity":true,

  "archetype_diversity":true,

  "culture_diversity":true
}
```

---

# 最低要求

至少：

```text id="x6v7m4"
2种Structure
```

---

至少：

```text id="y7m8q5"
2种Archetype
```

---

推荐：

```text id="z8v7m1"
3种Archetype
```

---

# 第四十一章 Top1 Schema

## 定位

最终答案。

---

# Schema

```json id="a9m8q3"
{
  "candidate_id":"CID_001",

  "full_name":"林知微",

  "rank":1
}
```

---

# 关系

```text id="b1v7m2"
Top1

属于

Top3
```

---

禁止：

```text id="c2m8q4"
绕过Top3
```

---

# 第四十二章 Tie Break Schema

## 定位

记录：

```text id="d3v8m5"
平分决策
```

---

# Schema

```json id="e4m7q1"
{
  "candidate_a":"CID_001",

  "candidate_b":"CID_002",

  "winner":"CID_001",

  "reason":"AESTHETIC"
}
```

---

# 允许值

```text id="f5m8q2"
AESTHETIC
```

---

```text id="g6v7m4"
ARCHETYPE
```

---

```text id="h7m8q5"
CULTURE
```

---

```text id="i8v7m1"
REGIONAL_FIT
```

---

# 第四十三章 Ranking Audit Schema

## 定位

记录：

```text id="j9m8q3"
排序审计日志
```

---

# Schema

```json id="k1v7m2"
{
  "ranking_id":"RANK001",

  "candidate_count":20,

  "selected_count":10,

  "timestamp":"..."
}
```

---

# 第四十四章 Promotion Audit Schema

## 定位

记录：

```text id="l2m8q4"
晋升过程
```

---

# Schema

```json id="m3v8m5"
{
  "candidate_id":"CID_001",

  "from_stage":"TOP20",

  "to_stage":"TOP10",

  "reason":"NES_PASS"
}
```

---

# 第四十五章 Selection Reason Schema

## 定位

解释：

```text id="n4m7q1"
为什么进入Top3
```

---

# Schema

```json id="o5m8q2"
{
  "candidate_id":"CID_001",

  "reason":"HIGH_NES"
}
```

---

# 枚举

```text id="p6v7m4"
HIGH_NES
```

---

```text id="q7m8q5"
HIGH_AESTHETIC
```

---

```text id="r8v7m1"
HIGH_HUMAN_SCORE
```

---

```text id="s9m8q3"
HIGH_DIVERSITY
```

---

# 第四十六章 Ranking Snapshot Schema

## 定位

支持：

```text id="t1v7m2"
回归测试
```

---

# Schema

```json id="u2m8q4"
{
  "session_id":"SID001",

  "snapshot_version":"v1.0.0",

  "top3":[]
}
```

---

# 用途

支持：

```text id="v3v8m5"
升级前后对比
```

---

```text id="w4m7q1"
结果漂移检测
```

---

# 第四十七章 Ranking Metrics Schema

## 监控

```json id="x5m8q2"
{
  "top1_stability":96,

  "top3_diversity":92,

  "ranking_accuracy":95
}
```

---

# 目标

```text id="y6v7m4"
Top1 Stability >95%
```

---

```text id="z7m8q5"
Top3 Diversity >90%
```

---

# 第四十八章 Ranking Philosophy

排序：

不是：

```text id="a8v7m1"
选最好听
```

---

而是：

```text id="b9m8q3"
选最成立
```

---

因此：

```text id="c1v7m2"
Ranking Layer

本质是：

证据排序器
```

---

# 文档状态

```text id="d2m8q4"
Draft Complete
```

---

# Part 4 End

# 第四十九章 Report Schema

## 49.1 定位

定义：

```text id="a1m8q2"
命名报告数据模型
```

---

作用：

连接：

```text id="b2v7m4"
Top3

↓

Top1

↓

Evidence

↓

Explainability
```

---

最终输出：

```text id="c3m8q5"
用户报告
```

---

# 49.2 Report Object

## Schema

```json id="d4v7m1"
{
  "report_id":"REP_001",

  "session_id":"SID_001",

  "report_version":"v1.0.0",

  "created_at":"..."
}
```

---

# 第五十章 Top1 Report Schema

## 定位

记录：

```text id="e5m8q3"
Top1完整分析
```

---

# Schema

```json id="f6v7m2"
{
  "candidate_id":"CID_001",

  "full_name":"林知微",

  "nes_score":91
}
```

---

# 包含

### Name Analysis

---

### Structure Analysis

---

### Archetype Analysis

---

### Culture Analysis

---

### Fortune Analysis

---

### Risk Analysis

---

# 第五十一章 Top3 Report Schema

## 定位

记录：

```text id="g7m8q4"
Top3对比
```

---

# Schema

```json id="h8v3m5"
{
  "top1":"CID_001",

  "top2":"CID_002",

  "top3":"CID_003"
}
```

---

# 用途

向用户解释：

```text id="i9m7q1"
为什么推荐这三个
```

---

# 第五十二章 Name Analysis Schema

## 定位

记录：

```text id="j1v8m2"
名字本身分析
```

---

# Schema

```json id="k2m7q4"
{
  "candidate_id":"CID_001",

  "full_name":"林知微",

  "character_analysis":[]
}
```

---

# 示例

```json id="l3v8m5"
{
  "character":"知",

  "meaning":"认知与洞察"
}
```

---

# 第五十三章 Structure Analysis Schema

## 来源

```text id="m4v7m1"
02D_STRUCTURE_LIBRARY
```

---

# Schema

```json id="n5m8q2"
{
  "structure_id":"S06",

  "structure_name":"书卷型",

  "structure_comment":"..."
}
```

---

# 用途

解释：

```text id="o6v7m4"
为什么采用该结构
```

---

# 第五十四章 Archetype Analysis Schema

## 来源

```text id="p7m8q5"
02C_ARCHETYPE_MATRIX
```

---

# Schema

```json id="q8v7m1"
{
  "archetype_id":"A01",

  "archetype_name":"书卷学者",

  "archetype_comment":"..."
}
```

---

# 用途

解释：

```text id="r9m8q3"
人格方向
```

---

# 第五十五章 Culture Analysis Schema

## 来源

```text id="s1v7m2"
02A_NAMING_PHILOSOPHY
```

---

# Schema

```json id="t2m8q4"
{
  "culture_id":"C01",

  "culture_name":"论语",

  "source_quote":"见微知著"
}
```

---

# 输出

解释：

```text id="u3v8m5"
文化来源
```

---

# 第五十六章 Evidence Chain Schema

## 定位

系统核心解释链。

---

# Schema

```json id="v4m7q1"
{
  "candidate_id":"CID_001",

  "structure_id":"S06",

  "archetype_id":"A01",

  "culture_id":"C01"
}
```

---

# 关系

```text id="w5m8q2"
Structure

↓

Archetype

↓

Culture

↓

Name
```

---

# 示例

```text id="x6v7m4"
书卷型

↓

书卷学者

↓

论语

↓

知微
```

---

# 第五十七章 Explainability Schema

## 定位

回答：

```text id="y7m8q5"
为什么是这个名字？
```

---

# Schema

```json id="z8v7m1"
{
  "candidate_id":"CID_001",

  "explanation":"..."
}
```

---

# 原则

解释：

必须来源于：

```text id="a9m8q3"
Evidence Chain
```

---

禁止：

```text id="b1v7m2"
事后编故事
```

---

# 第五十八章 Recommendation Schema

## 定位

记录：

```text id="c2m8q4"
顾问建议
```

---

# Schema

```json id="d3v8m5"
{
  "candidate_id":"CID_001",

  "recommendation":"..."
}
```

---

# 示例

```text id="e4m7q1"
适合认知型成长路径
```

---

# 第五十九章 Risk Analysis Schema

## 定位

记录：

```text id="f5m8q2"
风险分析
```

---

# Schema

```json id="g6v7m4"
{
  "candidate_id":"CID_001",

  "homophone_risk":"LOW",

  "template_risk":"LOW",

  "rare_character_risk":"LOW"
}
```

---

# 第六十章 Report Section Schema

## 定位

定义：

```text id="h7m8q5"
报告章节
```

---

# Schema

```json id="i8v7m1"
{
  "section_id":"SEC001",

  "section_type":"STRUCTURE"
}
```

---

# 枚举

```text id="j9m8q3"
SUMMARY
```

---

```text id="k1v7m2"
STRUCTURE
```

---

```text id="l2m8q4"
ARCHETYPE
```

---

```text id="m3v8m5"
CULTURE
```

---

```text id="n4m7q1"
RISK
```

---

```text id="o5m8q2"
TOP3_COMPARE
```

---

# 第六十一章 Report Snapshot Schema

## 定位

支持：

```text id="p6v7m4"
版本回归
```

---

# Schema

```json id="q7m8q5"
{
  "report_id":"REP001",

  "report_version":"v1.0.0"
}
```

---

# 用途

支持：

```text id="r8v7m1"
升级前后比较
```

---

# 第六十二章 Report Audit Schema

## 定位

记录：

```text id="s9m8q3"
报告生成过程
```

---

# Schema

```json id="t1v7m2"
{
  "report_id":"REP001",

  "generated_at":"...",

  "report_agent_version":"v1.0.0"
}
```

---

# 第六十三章 Explainability Score Schema

## 定位

衡量：

```text id="u2m8q4"
解释质量
```

---

# Schema

```json id="v3v8m5"
{
  "candidate_id":"CID001",

  "explainability_score":95
}
```

---

# 要求

```text id="w4m7q1"
≥90
```

---

# 第六十四章 Report Philosophy

报告：

不是：

```text id="x5m8q2"
夸名字
```

---

不是：

```text id="y6v7m4"
讲故事
```

---

而是：

```text id="z7m8q5"
展示证据链
```

---

因此：

```text id="a8v7m1"
Report Schema

本质是：

Explainability Schema
```

---

# 文档状态

```text id="b9m8q3"
Draft Complete
```

---

# Part 5 End

# 第六十五章 Session Schema

## 65.1 定位

定义：

```text id="a1m8q2"
命名会话
```

---

作用：

管理：

```text id="b2v7m4"
一次完整命名任务
```

---

对应：

```text id="c3m8q5"
02F Session Engine
```

---

# 65.2 Schema

```json id="d4v7m1"
{
  "session_id":"SID001",

  "user_id":"USER001",

  "status":"RUNNING",

  "current_stage":"STRUCTURE",

  "created_at":"...",

  "completed_at":null
}
```

---

# Status枚举

```text id="e5m8q3"
INIT
```

---

```text id="f6v7m2"
RUNNING
```

---

```text id="g7m8q4"
FAILED
```

---

```text id="h8v3m5"
COMPLETED
```

---

```text id="i9m7q1"
ARCHIVED
```

---

# 第六十六章 Session State Schema

## 定位

记录：

```text id="j1v8m2"
当前执行状态
```

---

# Schema

```json id="k2m7q4"
{
  "session_id":"SID001",

  "current_stage":"ARCHETYPE_READY"
}
```

---

# 枚举

```text id="l3v8m5"
PROFILE_READY
```

---

```text id="m4v7m1"
FORTUNE_READY
```

---

```text id="n5m8q2"
STRUCTURE_READY
```

---

```text id="o6v7m4"
ARCHETYPE_READY
```

---

```text id="p7m8q5"
CULTURE_READY
```

---

```text id="q8v7m1"
GENERATION_READY
```

---

```text id="r9m8q3"
TOP3_READY
```

---

```text id="s1v7m2"
REPORT_READY
```

---

# 第六十七章 Job Schema

## 定位

定义：

```text id="t2m8q4"
执行任务
```

---

# Schema

```json id="u3v8m5"
{
  "job_id":"JOB001",

  "session_id":"SID001",

  "job_type":"STRUCTURE",

  "status":"RUNNING"
}
```

---

# Job Type

```text id="v4m7q1"
PROFILE
```

---

```text id="w5m8q2"
FORTUNE
```

---

```text id="x6v7m4"
STRUCTURE
```

---

```text id="y7m8q5"
ARCHETYPE
```

---

```text id="z8v7m1"
CULTURE
```

---

```text id="a9m8q3"
GENERATION
```

---

```text id="b1v7m2"
CRITIQUE
```

---

```text id="c2m8q4"
NES
```

---

```text id="d3v8m5"
RANKING
```

---

```text id="e4m7q1"
REPORT
```

---

# 第六十八章 Job Lifecycle Schema

## 生命周期

```text id="f5m8q2"
PENDING
```

↓

```text id="g6v7m4"
RUNNING
```

↓

```text id="h7m8q5"
SUCCESS
```

---

失败：

```text id="i8v7m1"
FAILED
```

---

恢复：

```text id="j9m8q3"
RETRYING
```

---

最终：

```text id="k1v7m2"
COMPLETED
```

---

# Schema

```json id="l2m8q4"
{
  "job_id":"JOB001",

  "from_status":"RUNNING",

  "to_status":"SUCCESS",

  "timestamp":"..."
}
```

---

# 第六十九章 Queue Schema

## 定位

定义：

```text id="m3v8m5"
任务队列
```

---

# Schema

```json id="n4m7q1"
{
  "queue_id":"QUEUE001",

  "queue_type":"GENERATION"
}
```

---

# Queue Type

```text id="o5m8q2"
PROFILE_QUEUE
```

---

```text id="p6v7m4"
STRUCTURE_QUEUE
```

---

```text id="q7m8q5"
ARCHETYPE_QUEUE
```

---

```text id="r8v7m1"
CULTURE_QUEUE
```

---

```text id="s9m8q3"
GENERATION_QUEUE
```

---

```text id="t1v7m2"
SCORING_QUEUE
```

---

```text id="u2m8q4"
REPORT_QUEUE
```

---

# 第七十章 Queue Item Schema

## 定位

记录：

```text id="v3v8m5"
队列任务
```

---

# Schema

```json id="w4m7q1"
{
  "queue_id":"QUEUE001",

  "job_id":"JOB001",

  "priority":1
}
```

---

# 优先级

```text id="x5m8q2"
1
```

最高。

---

```text id="y6v7m4"
5
```

最低。

---

# 第七十一章 Worker Schema

## 定位

定义：

```text id="z7m8q5"
执行器
```

---

# Schema

```json id="a8v7m1"
{
  "worker_id":"WORKER001",

  "worker_type":"GENERATOR"
}
```

---

# Worker Type

```text id="b9m8q3"
STRUCTURE_WORKER
```

---

```text id="c1v7m2"
ARCHETYPE_WORKER
```

---

```text id="d2m8q4"
GENERATOR_WORKER
```

---

```text id="e3v8m5"
NES_WORKER
```

---

```text id="f4m7q1"
REPORT_WORKER
```

---

# 第七十二章 Scheduler Schema

## 定位

定义：

```text id="g5m8q2"
调度器
```

---

# Schema

```json id="h6v7m4"
{
  "scheduler_id":"SCH001",

  "active_jobs":15
}
```

---

# 功能

负责：

```text id="i7m8q5"
任务分配
```

---

```text id="j8v7m1"
执行顺序控制
```

---

# 第七十三章 Event Schema

## 定位

记录：

```text id="k9m8q3"
系统事件
```

---

# Schema

```json id="l1v7m2"
{
  "event_id":"EVT001",

  "event_type":"JOB_STARTED",

  "session_id":"SID001",

  "timestamp":"..."
}
```

---

# Event Type

```text id="m2m8q4"
JOB_CREATED
```

---

```text id="n3v8m5"
JOB_STARTED
```

---

```text id="o4m7q1"
JOB_COMPLETED
```

---

```text id="p5m8q2"
JOB_FAILED
```

---

```text id="q6v7m4"
RETRY_TRIGGERED
```

---

# 第七十四章 Audit Log Schema

## 定位

系统级审计。

---

# Schema

```json id="r7m8q5"
{
  "audit_id":"AUD001",

  "entity_type":"Candidate",

  "entity_id":"CID001",

  "action":"UPDATE"
}
```

---

# 用途

支持：

```text id="s8v7m1"
全链路追踪
```

---

```text id="t9m8q3"
问题定位
```

---

```text id="u1v7m2"
版本回溯
```

---

# 第七十五章 Error Event Schema

## 定位

记录：

```text id="v2m8q4"
系统错误
```

---

# Schema

```json id="w3v8m5"
{
  "error_id":"ERR001",

  "job_id":"JOB001",

  "error_type":"STRUCTURE_FAIL",

  "retry_count":2
}
```

---

# 第七十六章 DLQ Schema

## Dead Letter Queue

---

# Schema

```json id="x4m7q1"
{
  "dlq_id":"DLQ001",

  "job_id":"JOB001",

  "reason":"CONTEXT_CORRUPTED"
}
```

---

# 作用

存放：

```text id="y5m8q2"
无法恢复任务
```

---

# 第七十七章 Event Sourcing Philosophy

所有重要状态：

必须：

```text id="z6v7m4"
事件驱动
```

---

任何变化：

必须：

```text id="a7m8q5"
留下事件
```

---

因此：

```text id="b8v7m1"
Session

Job

Queue

Event

Audit
```

---

共同构成：

```text id="c9m8q3"
Execution Data Layer
```

---

# 文档状态

```text id="d1v7m2"
Draft Complete
```

---

# Part 6 End

# 第七十八章 API Schema

## 78.1 定位

定义：

```text id="a1m8q2"
系统接口数据模型
```

---

作用：

连接：

```text id="b2v7m4"
Frontend

↓

API

↓

Orchestration

↓

Database
```

---

# 78.2 API原则

所有接口：

必须：

```text id="c3m8q5"
版本化
```

---

必须：

```text id="d4v7m1"
可追踪
```

---

必须：

```text id="e5m8q3"
可审计
```

---

# 第七十九章 API Request Schema

## 通用请求

```json id="f6v7m2"
{
  "request_id":"REQ001",

  "api_version":"v1",

  "timestamp":"..."
}
```

---

# 命名请求

```json id="g7m8q4"
{
  "surname":"林",

  "gender":"male",

  "birth_date":"2025-03-01",

  "birth_time":"08:30",

  "birth_location":"广东汕头"
}
```

---

# 第八十章 API Response Schema

## 通用响应

```json id="h8v3m5"
{
  "success":true,

  "request_id":"REQ001",

  "data":{}
}
```

---

# 错误响应

```json id="i9m7q1"
{
  "success":false,

  "error_code":"INVALID_INPUT",

  "message":"..."
}
```

---

# 第八十一章 Naming API Schema

## POST

```text id="j1v8m2"
/api/v1/naming/create
```

---

# Response

```json id="k2m7q4"
{
  "session_id":"SID001",

  "status":"RUNNING"
}
```

---

# GET

```text id="l3v8m5"
/api/v1/naming/status
```

---

# Response

```json id="m4v7m1"
{
  "session_id":"SID001",

  "current_stage":"ARCHETYPE_READY"
}
```

---

# 第八十二章 Candidate API Schema

## GET

```text id="n5m8q2"
/api/v1/candidates
```

---

# Response

```json id="o6v7m4"
{
  "session_id":"SID001",

  "candidates":[]
}
```

---

# Candidate Object

```json id="p7m8q5"
{
  "candidate_id":"CID001",

  "name":"知微"
}
```

---

# 第八十三章 Ranking API Schema

## GET

```text id="q8v7m1"
/api/v1/ranking
```

---

# Response

```json id="r9m8q3"
{
  "top1":"CID001",

  "top2":"CID002",

  "top3":"CID003"
}
```

---

# 第八十四章 Report API Schema

## GET

```text id="s1v7m2"
/api/v1/report
```

---

# Response

```json id="t2m8q4"
{
  "report_id":"REP001"
}
```

---

# 第八十五章 Version Schema

## 定位

统一版本控制。

---

# Schema

```json id="u3v8m5"
{
  "version":"v1.0.0",

  "released_at":"..."
}
```

---

# 分类

```text id="v4m7q1"
Schema Version
```

---

```text id="w5m8q2"
API Version
```

---

```text id="x6v7m4"
Prompt Version
```

---

```text id="y7m8q5"
NES Version
```

---

# 第八十六章 Entity Version Schema

## 定位

记录：

```text id="z8v7m1"
实体版本
```

---

# Schema

```json id="a9m8q3"
{
  "entity_id":"CID001",

  "entity_version":"v1.0.0"
}
```

---

# 用途

支持：

```text id="b1v7m2"
回归测试
```

---

```text id="c2m8q4"
历史恢复
```

---

# 第八十七章 Migration Schema

## 定位

数据库迁移。

---

# Schema

```json id="d3v8m5"
{
  "migration_id":"MIG001",

  "from_version":"v1.0.0",

  "to_version":"v1.1.0"
}
```

---

# 状态

```text id="e4m7q1"
PENDING
```

---

```text id="f5m8q2"
RUNNING
```

---

```text id="g6v7m4"
SUCCESS
```

---

```text id="h7m8q5"
FAILED
```

---

# 第八十八章 Schema Compatibility

## 定位

兼容性管理。

---

# 原则

升级后：

必须保证：

```text id="i8v7m1"
旧数据可读取
```

---

# 禁止

```text id="j9m8q3"
直接删除字段
```

---

# 必须

```text id="k1v7m2"
Deprecated
```

↓

```text id="l2m8q4"
Migration
```

↓

```text id="m3v8m5"
Removal
```

---

# 第八十九章 Backward Compatibility Schema

## Schema

```json id="n4m7q1"
{
  "schema_version":"v1.0.0",

  "compatible_versions":[
    "v0.9.0"
  ]
}
```

---

# 用途

支持：

```text id="o5m8q2"
旧Session恢复
```

---

```text id="p6v7m4"
历史报告恢复
```

---

# 第九十章 Database Table Mapping

## NamingSession

```text id="q7m8q5"
naming_sessions
```

---

## Candidate

```text id="r8v7m1"
candidates
```

---

## NESScore

```text id="s9m8q3"
nes_scores
```

---

## Report

```text id="t1v7m2"
reports
```

---

## Audit

```text id="u2m8q4"
audit_logs
```

---

# 第九十一章 Storage Strategy

## PostgreSQL

存储：

```text id="v3v8m5"
Session
```

---

```text id="w4m7q1"
Candidate
```

---

```text id="x5m8q2"
NES
```

---

```text id="y6v7m4"
Report
```

---

# Redis

存储：

```text id="z7m8q5"
Queue
```

---

```text id="a8v7m1"
Job
```

---

```text id="b9m8q3"
Cache
```

---

# Object Storage

存储：

```text id="c1v7m2"
Report Snapshot
```

---

```text id="d2m8q4"
Audit Export
```

---

# 第九十二章 Data Governance Philosophy

数据：

不是：

```text id="e3v8m5"
存起来
```

---

而是：

```text id="f4m7q1"
支持解释
```

---

支持：

```text id="g5m8q2"
审计
```

---

支持：

```text id="h6v7m4"
回归
```

---

支持：

```text id="i7m8q5"
重建
```

---

因此：

```text id="j8v7m1"
Data Schema

是系统的事实来源（Source of Truth）
```

---

# 文档状态

```text id="k9m8q3"
Draft Complete
```

---

# Part 7 End

# 第九十三章 Architecture Mapping

## 93.1 定位

建立：

```text id="a1m8q2"
数据架构映射
```

---

连接：

```text id="b2v7m4"
02A

↓

02D

↓

02C

↓

02E

↓

02F

↓

02B
```

---

与：

```text id="c3m8q5"
03 Data Schema
```

建立对应关系。

---

# 93.2 Mapping

## Naming Philosophy

对应：

```text id="d4v7m1"
Culture Schema
```

---

## Structure Library

对应：

```text id="e5m8q3"
Structure Schema
```

---

## Archetype Matrix

对应：

```text id="f6v7m2"
Archetype Schema
```

---

## Prompt Architecture

对应：

```text id="g7m8q4"
Candidate Schema
```

---

## Orchestration Engine

对应：

```text id="h8v3m5"
Session

Job

Queue

Event
```

---

## NES

对应：

```text id="i9m7q1"
NES Schema
```

---

# 第九十四章 Entity Relationship Model

## 核心关系图

```text id="j1v8m2"
User

1

↓

N

Session

1

↓

1

Context

1

↓

N

Candidate

1

↓

1

NES

1

↓

1

Ranking

1

↓

1

Report
```

---

# Candidate扩展关系

```text id="k2m7q4"
Candidate

↓

Structure

↓

Archetype

↓

Culture
```

---

# Critique扩展关系

```text id="l3v8m5"
Candidate

↓

Critique

↓

Aesthetic

↓

Human

↓

Diversity
```

---

# 第九十五章 Physical Database Design

## PostgreSQL Tables

### users

---

### naming_sessions

---

### naming_contexts

---

### structures

---

### archetypes

---

### cultures

---

### candidates

---

### critique_results

---

### nes_scores

---

### rankings

---

### reports

---

### jobs

---

### events

---

### audit_logs

---

# 第九十六章 Primary Key Design

## User

```text id="m4v7m1"
user_id
```

---

## Session

```text id="n5m8q2"
session_id
```

---

## Candidate

```text id="o6v7m4"
candidate_id
```

---

## Report

```text id="p7m8q5"
report_id
```

---

## Job

```text id="q8v7m1"
job_id
```

---

# 原则

统一：

```text id="r9m8q3"
UUID
```

---

# 第九十七章 Index Strategy

## 高频查询

### Session

```text id="s1v7m2"
session_id
```

---

### Candidate

```text id="t2m8q4"
candidate_id
```

---

### Ranking

```text id="u3v8m5"
rank
```

---

### Report

```text id="v4m7q1"
report_id
```

---

# 复合索引

```text id="w5m8q2"
session_id

+

candidate_id
```

---

# 第九十八章 Cache Strategy

## Redis缓存

缓存：

```text id="x6v7m4"
Session State
```

---

```text id="y7m8q5"
Candidate Pool
```

---

```text id="z8v7m1"
Top3
```

---

```text id="a9m8q3"
Report Preview
```

---

# TTL

默认：

```text id="b1v7m2"
24小时
```

---

# 第九十九章 Event Sourcing Model

## 原则

重要状态：

全部事件化。

---

例如：

```text id="c2m8q4"
Candidate Generated
```

---

```text id="d3v8m5"
Candidate Rejected
```

---

```text id="e4m7q1"
NES Calculated
```

---

```text id="f5m8q2"
Top3 Selected
```

---

# Event Schema

```json id="g6v7m4"
{
  "event_id":"EVT001",

  "event_type":"TOP3_SELECTED",

  "session_id":"SID001"
}
```

---

# 第一百章 Audit Governance

## 审计原则

任何名字：

必须回答：

```text id="h7m8q5"
为什么生成？
```

---

任何评分：

必须回答：

```text id="i8v7m1"
为什么得分？
```

---

任何淘汰：

必须回答：

```text id="j9m8q3"
为什么淘汰？
```

---

# 审计链

```text id="k1v7m2"
Candidate

↓

Critique

↓

NES

↓

Ranking

↓

Report
```

---

# 第一百零一章 Data Quality Rules

## 必填字段

### session_id

---

### candidate_id

---

### structure_id

---

### archetype_id

---

### culture_id

---

### nes_score

---

# 缺失

直接：

```text id="l2m8q4"
Reject
```

---

# 第一百零二章 Data Integrity Rules

## Candidate

必须绑定：

```text id="m3v8m5"
Structure
```

---

```text id="n4m7q1"
Archetype
```

---

```text id="o5m8q2"
Culture
```

---

禁止：

```text id="p6v7m4"
孤立Candidate
```

---

# NES

必须绑定：

```text id="q7m8q5"
Candidate
```

---

禁止：

```text id="r8v7m1"
孤立Score
```

---

# 第一百零三章 Data Lifecycle

## Session

```text id="s9m8q3"
90天
```

在线。

---

## Report

```text id="t1v7m2"
永久保存
```

---

## Audit

```text id="u2m8q4"
永久保存
```

---

## Event

```text id="v3v8m5"
180天
```

---

# 第一百零四章 Governance Metrics

## 数据质量指标

### Data Completeness

---

### Data Consistency

---

### Audit Coverage

---

### Explainability Coverage

---

### Traceability Coverage

---

# 目标

```text id="w4m7q1"
≥95%
```

---

# 第一百零五章 Final Data Audit

## 第一轮审计发现

缺：

```text id="x5m8q2"
Structure Schema
```

---

修复：

```text id="y6v7m4"
Part 1
```

---

缺：

```text id="z7m8q5"
Archetype Schema
```

---

修复：

```text id="a8v7m1"
Part 1
```

---

缺：

```text id="b9m8q3"
Candidate Lifecycle
```

---

修复：

```text id="c1v7m2"
Part 2
```

---

缺：

```text id="d2m8q4"
Critique Schema
```

---

修复：

```text id="e3v8m5"
Part 3
```

---

缺：

```text id="f4m7q1"
Ranking Schema
```

---

修复：

```text id="g5m8q2"
Part 4
```

---

缺：

```text id="h6v7m4"
Report Schema
```

---

修复：

```text id="i7m8q5"
Part 5
```

---

缺：

```text id="j8v7m1"
Execution Schema
```

---

修复：

```text id="k9m8q3"
Part 6
```

---

# 第一百零六章 Data Layer Closure

至此：

```text id="l1v7m2"
Philosophy
```

↓

```text id="m2m8q4"
Structure
```

↓

```text id="n3v8m5"
Archetype
```

↓

```text id="o4m7q1"
Prompt
```

↓

```text id="p5m8q2"
Orchestration
```

↓

```text id="q6v7m4"
NES
```

↓

```text id="r7m8q5"
Data Schema
```

全部打通。

---

# 第一百零七章 Final Verdict

Data Layer已具备：

```text id="s8v7m1"
可解释
```

---

```text id="t9m8q3"
可审计
```

---

```text id="u1v7m2"
可回归
```

---

```text id="v2m8q4"
可扩展
```

---

```text id="w3v8m5"
可开发
```

---

能力。

---

# 文档状态

```text id="x4m7q1"
Approved
```

---

版本：

```text id="y5m8q2"
03_DATA_SCHEMA.md

Version 1.0 Final
```

---

# End Of File
