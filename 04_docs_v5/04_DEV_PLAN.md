# 易元命名 Pro

# DEVELOPMENT PLAN

Version 1.0

---

# 文档定位

本文件定义：

```text
从架构到产品落地路线
```

---

连接：

```text
02A Philosophy

↓

02D Structure

↓

02C Archetype

↓

02E Prompt

↓

02F Orchestration

↓

02B NES

↓

03 Data Schema
```

---

目标：

```text
指导开发团队

从0到1实现系统
```

---

# 第一章 Development Philosophy

## 核心原则

先验证：

```text
架构正确
```

---

再验证：

```text
产品可用
```

---

最后验证：

```text
商业成立
```

---

禁止：

```text
先做UI

后补逻辑
```

---

禁止：

```text
先做Agent

后补数据
```

---

正确顺序：

```text
Data

↓

Engine

↓

Orchestration

↓

API

↓

Frontend
```

---

# 第二章 技术架构总览

## Backend

推荐：

```text
Python 3.12
```

---

框架：

```text
FastAPI
```

---

原因：

```text
异步

高性能

AI生态成熟
```

---

# Database

主库：

```text
PostgreSQL
```

---

缓存：

```text
Redis
```

---

文件：

```text
S3 / MinIO
```

---

# AI Layer

推荐：

```text
LangGraph
```

---

原因：

```text
天然支持

State

Workflow

Multi Agent
```

---

不推荐：

```text
CrewAI
```

作为主架构。

---

仅用于：

```text
实验Agent
```

---

# 第三章 Repository Structure

```text
yiyuan-naming/

├── apps/
│
├── backend/
│
├── frontend/
│
├── prompts/
│
├── datasets/
│
├── tests/
│
├── docs/
│
└── infra/
```

---

# Backend结构

```text
backend/

├── api/
├── core/
├── engines/
├── agents/
├── schemas/
├── repositories/
├── services/
├── workers/
├── orchestration/
└── tests/
```

---

# 第四章 Engine Development Order

## 为什么

当前项目最大风险：

```text
Agent太复杂
```

---

因此：

必须：

```text
Engine优先
```

---

不是：

```text
Prompt优先
```

---

# 开发顺序

```text
Structure Engine

↓

Archetype Engine

↓

Culture Engine

↓

Generator Engine

↓

Critique Engine

↓

NES Engine

↓

Ranking Engine

↓

Report Engine
```

---

# 第五章 Sprint 0

## 目标

建立基础设施。

---

周期：

```text
3天
```

---

# 任务

## PostgreSQL

建库

---

## Redis

搭建

---

## FastAPI

初始化

---

## Docker

初始化

---

## CI/CD

初始化

---

# 验收标准

```text
本地一键启动
```

---

```text
Docker运行
```

---

```text
数据库连接成功
```

---

# 第六章 Sprint 1

## Structure Engine

---

周期：

```text
5天
```

---

# 输入

```json
{
  "profile":{}
}
```

---

# 输出

```json
{
  "structure":"S06"
}
```

---

# 实现内容

## Structure Library

导入。

---

## Structure Matcher

实现。

---

## Structure Ranking

实现。

---

# 验收

```text
Top3 Structure
```

正确输出。

---

准确率：

```text
>90%
```

---

# 第七章 Sprint 2

## Archetype Engine

---

周期：

```text
5天
```

---

# 输入

```json
{
  "structure":"S06"
}
```

---

# 输出

```json
{
  "archetype":"A01"
}
```

---

# 功能

## Archetype Mapping

---

## Confidence

---

## Archetype Ranking

---

# 验收

```text
Structure→Archetype
```

链路跑通。

---

# 第八章 Sprint 3

## Culture Engine

---

周期：

```text
7天
```

---

# 输入

```json
{
  "archetype":"A01"
}
```

---

# 输出

```json
{
  "culture":"论语"
}
```

---

# 功能

## Culture Library

---

## Culture Retrieval

---

## Quote Retrieval

---

## Evidence Builder

---

# 验收

```text
Archetype

↓

Culture
```

正确率：

```text
>90%
```

---

# 第九章 Sprint 4

## Generator Engine

---

周期：

```text
10天
```

---

# 目标

生成：

```text
200 Candidate
```

---

# 功能

## Character Pool

---

## Semantic Composer

---

## Structure Constraint

---

## Culture Constraint

---

## Diversity Generator

---

# 验收

生成：

```text
200个候选
```

---

重复率：

```text
<5%
```

---

模板率：

```text
<10%
```

---

# 第十章 MVP定义

MVP必须具备：

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
Generation
```

---

# MVP暂不包含

```text
家庭偏好学习
```

---

```text
用户画像学习
```

---

```text
长期记忆
```

---

```text
自动优化
```

---

# 文档状态

```text
Draft Complete
```

---

# Part 1 End

# 第十一章 Sprint 5

# Critique Engine

---

## 周期

```text id="a1m8q2"
10天
```

---

## 开发目标

建立：

```text id="b2v7m4"
名字质量过滤层
```

---

解决：

```text id="c3m8q5"
AI模板名
```

---

```text id="d4v7m1"
小说主角名
```

---

```text id="e5m8q3"
网红宝宝名
```

---

问题。

---

# 子模块

## Self Critique

---

## Red Team

---

## Template Detector

---

## Human Detector

---

## Aesthetic Engine

---

## Diversity Guard

---

# 第十二章 Self Critique Engine

## 输入

```json id="f6v7m2"
{
  "candidate":"知微"
}
```

---

## 输出

```json id="g7m8q4"
{
  "passed":true
}
```

---

## 功能

自动检查：

### 结构成立性

---

### 人格一致性

---

### 文化一致性

---

### 语义完整性

---

# 验收

误判率：

```text id="h8v3m5"
<5%
```

---

# 第十三章 Red Team Engine

## 目标

建立：

```text id="i9m7q1"
反对者模型
```

---

## 检查项

### 小说男主感

---

### 古偶女主感

---

### 网络爆款感

---

### AI味

---

### 中二感

---

# 输出

```json id="j1v8m2"
{
  "risk":"LOW"
}
```

---

# 验收

高风险名字：

识别率：

```text id="k2m7q4"
>90%
```

---

# 第十四章 Template Detector

## 建立

```text id="l3v8m5"
AI模板库
```

---

## 第一批

至少：

```text id="m4v7m1"
10000
```

个名字。

---

# 来源

### 新生儿榜单

---

### 小红书热门名

---

### 起名网站

---

### AI生成样本

---

# 输出

```json id="n5m8q2"
{
  "template":true
}
```

---

# 验收

命中率：

```text id="o6v7m4"
>95%
```

---

# 第十五章 Human Detector

## 目标

判断：

```text id="p7m8q5"
像不像真人大师取名
```

---

# 输入

```text id="q8v7m1"
林知微
```

---

# 输出

```json id="r9m8q3"
{
  "human_score":91
}
```

---

# 评分区间

```text id="s1v7m2"
95+
```

大师级。

---

```text id="t2m8q4"
90+
```

优秀。

---

```text id="u3v8m5"
80+
```

合格。

---

```text id="v4m7q1"
80-
```

淘汰。

---

# 第十六章 Aesthetic Engine

## 定位

建立：

```text id="w5m8q2"
高级感评分系统
```

---

# 五维模型

### Structure

---

### Archetype

---

### Culture

---

### Reality

---

### Beauty

---

# 输出

```json id="x6v7m4"
{
  "aesthetic_score":92
}
```

---

# 验收

专家一致率：

```text id="y7m8q5"
>85%
```

---

# 第十七章 Diversity Guard

## 定位

防止：

```text id="z8v7m1"
名字越来越像
```

---

## 检查

### 字重复

---

### 结构重复

---

### 人格重复

---

### 文化重复

---

# 输出

```json id="a9m8q3"
{
  "diversity_passed":true
}
```

---

# 第十八章 Sprint 6

# NES Engine

---

## 周期

```text id="b1v7m2"
5天
```

---

## 来源

```text id="c2m8q4"
02B_NES
```

---

# 实现模块

### Structure Score

---

### Archetype Score

---

### Culture Score

---

### Meaning Score

---

### Sound Score

---

### Fortune Score

---

### Unique Score

---

### Bonus Score

---

# 输出

```json id="d3v8m5"
{
  "nes_score":91
}
```

---

# 第十九章 NES Validator

## 目标

验证：

```text id="e4m7q1"
评分正确
```

---

# 检查

总分：

```text id="f5m8q2"
=
```

各项分数之和。

---

# 禁止

```text id="g6v7m4"
黑盒评分
```

---

# 第二十章 Sprint 7

# Ranking Engine

---

## 周期

```text id="h7m8q5"
5天
```

---

# 输入

```text id="i8v7m1"
200 Candidate
```

---

# 输出

```text id="j9m8q3"
Top3
```

---

# 模块

### Ranking

---

### Tie Break

---

### Diversity Selection

---

### Top1 Selection

---

# 第二十一章 Ranking Logic

## 第一层

按：

```text id="k1v7m2"
NES
```

排序。

---

# 第二层

按：

```text id="l2m8q4"
Aesthetic
```

排序。

---

# 第三层

按：

```text id="m3v8m5"
Human Score
```

排序。

---

# 第四层

按：

```text id="n4m7q1"
Culture Depth
```

排序。

---

# 第二十二章 Sprint 8

# Report Engine

---

## 周期

```text id="o5m8q2"
7天
```

---

# 输入

```text id="p6v7m4"
Top3
```

---

# 输出

```text id="q7m8q5"
命名报告
```

---

# 模块

### Evidence Builder

---

### Explainability Builder

---

### Top3 Comparison

---

### Risk Analysis

---

### PDF Builder

---

# 第二十三章 Explainability Engine

## 用户提问

```text id="r8v7m1"
为什么是林知微？
```

---

# 系统回答

```text id="s9m8q3"
S06 书卷型

↓

A01 书卷学者

↓

论语

↓

见微知著

↓

知微
```

---

# 禁止

```text id="t1v7m2"
因为好听
```

---

# 第二十四章 MVP Alpha验收

## Alpha完成条件

```text id="u2m8q4"
Structure Engine
```

PASS

---

```text id="v3v8m5"
Archetype Engine
```

PASS

---

```text id="w4m7q1"
Culture Engine
```

PASS

---

```text id="x5m8q2"
Generator Engine
```

PASS

---

```text id="y6v7m4"
Critique Engine
```

PASS

---

```text id="z7m8q5"
NES Engine
```

PASS

---

```text id="a8v7m1"
Ranking Engine
```

PASS

---

```text id="b9m8q3"
Report Engine
```

PASS

---

# 第二十五章 Alpha目标

实现：

```text id="c1v7m2"
200

↓

20

↓

10

↓

3

↓

1
```

---

完整闭环。

---

# 文档状态

```text id="d2m8q4"
Draft Complete
```

---

# Part 2 End

# 第二十六章 Sprint 9

# Orchestration Engine

---

## 周期

```text id="a1m8q2"
10天
```

---

## 目标

实现：

```text id="b2v7m4"
02F_ORCHESTRATION_ENGINE
```

---

建立：

```text id="c3m8q5"
系统中枢
```

---

# 核心职责

### State Management

---

### Agent Scheduling

---

### Context Propagation

---

### Error Recovery

---

### Workflow Control

---

# 第二十七章 LangGraph Architecture

## 为什么选LangGraph

因为系统本质：

```text id="d4v7m1"
State Machine
```

---

而不是：

```text id="e5m8q3"
ChatBot
```

---

# 状态流

```text id="f6v7m2"
INIT

↓

PROFILE

↓

FORTUNE

↓

STRUCTURE

↓

ARCHETYPE

↓

CULTURE

↓

GENERATION

↓

CRITIQUE

↓

NES

↓

RANKING

↓

REPORT

↓

DONE
```

---

# LangGraph Node Mapping

## Node01

```text id="g7m8q4"
Profile Node
```

---

## Node02

```text id="h8v3m5"
Fortune Node
```

---

## Node03

```text id="i9m7q1"
Structure Node
```

---

## Node04

```text id="j1v8m2"
Archetype Node
```

---

## Node05

```text id="k2m7q4"
Culture Node
```

---

## Node06

```text id="l3v8m5"
Generation Node
```

---

## Node07

```text id="m4v7m1"
Critique Node
```

---

## Node08

```text id="n5m8q2"
NES Node
```

---

## Node09

```text id="o6v7m4"
Ranking Node
```

---

## Node10

```text id="p7m8q5"
Report Node
```

---

# 第二十八章 State Schema

## LangGraph State

```python
class NamingState:
    session_id: str

    profile: dict

    fortune: dict

    structure: dict

    archetype: dict

    culture: dict

    candidates: list

    critique: dict

    ranking: dict

    report: dict
```

---

# 原则

所有Node：

共享：

```text id="q8v7m1"
NamingState
```

---

# 第二十九章 Context Bus

## 定位

统一上下文总线。

---

# 禁止

```text id="r9m8q3"
Node互相调用
```

---

例如：

禁止：

```text id="s1v7m2"
Structure

↓

直接调用Culture
```

---

# 必须

```text id="t2m8q4"
State

↓

Graph
```

传递。

---

# 第三十章 Multi-Agent Architecture

## Agent分类

### Structure Agent

---

### Archetype Agent

---

### Culture Agent

---

### Generator Agent

---

### Critique Agent

---

### NES Agent

---

### Report Agent

---

# 原则

Agent：

负责：

```text id="u3v8m5"
推理
```

---

Graph：

负责：

```text id="v4m7q1"
流程
```

---

# 第三十一章 Agent Contract

## 输入

统一：

```python
InputContext
```

---

## 输出

统一：

```python
OutputContext
```

---

# 示例

```python
{
   "structure":"S06"
}
```

---

# 禁止

```text id="w5m8q2"
返回自由文本
```

---

# 必须

```text id="x6v7m4"
结构化JSON
```

---

# 第三十二章 Database Repository Layer

## Repository模式

建立：

```text id="y7m8q5"
Data Access Layer
```

---

# Repository

### SessionRepository

---

### CandidateRepository

---

### ScoreRepository

---

### ReportRepository

---

### AuditRepository

---

# 禁止

Agent直接访问数据库。

---

# 第三十三章 Service Layer

## 定位

业务逻辑层。

---

# Services

### StructureService

---

### ArchetypeService

---

### CultureService

---

### GenerationService

---

### RankingService

---

### ReportService

---

# 调用链

```text id="z8v7m1"
API

↓

Service

↓

Repository
```

---

# 第三十四章 API Development Order

## 第一阶段

```text id="a9m8q3"
POST /naming/create
```

---

## 第二阶段

```text id="b1v7m2"
GET /session
```

---

## 第三阶段

```text id="c2m8q4"
GET /ranking
```

---

## 第四阶段

```text id="d3v8m5"
GET /report
```

---

## 第五阶段

```text id="e4m7q1"
GET /audit
```

---

# 第三十五章 Async Job Architecture

## 为什么

生成：

```text id="f5m8q2"
200 Candidate
```

耗时较长。

---

# 方案

用户：

```text id="g6v7m4"
创建Session
```

---

系统：

```text id="h7m8q5"
异步执行
```

---

用户：

```text id="i8v7m1"
轮询状态
```

---

# 第三十六章 Queue Worker Design

## Worker Pool

### Structure Worker

---

### Generator Worker

---

### Critique Worker

---

### NES Worker

---

### Report Worker

---

# 并发

```text id="j9m8q3"
可水平扩容
```

---

# 第三十七章 Error Recovery Integration

## 对接

```text id="k1v7m2"
Recovery Engine
```

---

# 流程

```text id="l2m8q4"
Fail

↓

Retry

↓

Fallback

↓

DLQ
```

---

# 第三十八章 Audit Integration

## 每个Node

产生：

```text id="m3v8m5"
Audit Event
```

---

例如：

```text id="n4m7q1"
STRUCTURE_SELECTED
```

---

```text id="o5m8q2"
ARCHETYPE_SELECTED
```

---

```text id="p6v7m4"
TOP1_SELECTED
```

---

# 第三十九章 MVP Beta

## Beta标准

支持：

```text id="q7m8q5"
100 Session/Day
```

---

支持：

```text id="r8v7m1"
Top3生成
```

---

支持：

```text id="s9m8q3"
完整报告
```

---

# 性能

平均：

```text id="t1v7m2"
<30秒
```

完成一次命名。

---

# 第四十章 Sprint 9验收

## 验收项

### LangGraph运行

PASS

---

### State管理

PASS

---

### Agent编排

PASS

---

### Error Recovery

PASS

---

### Audit

PASS

---

### API

PASS

---

# 文档状态

```text id="u2m8q4"
Draft Complete
```

---

# Part 3 End

# 第四十一章 Knowledge Base Development Plan

## 定位

建立：

```text
Naming Intelligence Layer
```

---

原因：

系统真正的护城河：

不是：

```text
Prompt
```

---

不是：

```text
Agent
```

---

而是：

```text
Knowledge Base
```

---

# 核心公式

```text
普通起名系统

=
Prompt
```

---

```text
易元命名

=

Knowledge Base

+

Prompt

+

Orchestration
```

---

# 第四十二章 Knowledge Architecture

## V1知识体系

```text
Structure Library

↓

Archetype Library

↓

Culture Library

↓

Character Library

↓

Template Blacklist

↓

Human Naming Corpus
```

---

# 目标规模

```text
Structure
50+
```

---

```text
Archetype
100+
```

---

```text
Culture
3000+
```

---

```text
Character
5000+
```

---

```text
Human Corpus
100000+
```

---

# 第四十三章 Structure Library Construction

## 来源

### 历代名人

---

### 地域文化

---

### 儒释道文化

---

### 企业家案例

---

### 现代精英人格

---

# 第一阶段

建立：

```text
50个Structure
```

---

例如：

```text
君子型
```

---

```text
书卷型
```

---

```text
将帅型
```

---

```text
修行型
```

---

```text
开拓型
```

---

# 数据结构

```json
{
  "structure_id":"S06",

  "structure_name":"书卷型",

  "description":"..."
}
```

---

# 第四十四章 Archetype Library Construction

## 来源

### 荣格原型

---

### 中国历史人物

---

### 企业家人格

---

### 文学人格

---

### 宗教人格

---

# 第一阶段

建立：

```text
100 Archetype
```

---

# 示例

```text
书卷学者
```

---

```text
温润君子
```

---

```text
远见领袖
```

---

```text
修行者
```

---

```text
战略家
```

---

# 验收

每个Archetype：

必须：

```text
绑定Structure
```

---

# 第四十五章 Culture Library Construction

## 项目价值核心

---

决定：

```text
名字深度
```

---

# 文化来源

## 经部

### 论语

### 孟子

### 大学

### 中庸

---

## 子部

### 庄子

### 老子

### 韩非子

---

## 集部

### 唐诗

### 宋词

### 楚辞

---

## 史部

### 史记

### 汉书

### 资治通鉴

---

# 第一阶段目标

```text
3000+
文化片段
```

---

# Schema

```json
{
  "culture_id":"C001",

  "source":"论语",

  "quote":"见微知著",

  "meaning":"..."
}
```

---

# 第四十六章 Culture Quality Rules

## 禁止

直接存：

```text
整段古文
```

---

必须拆解：

```text
文化意象
```

---

例如：

```text
见微知著
```

拆成：

```text
洞察
```

---

```text
远见
```

---

```text
认知
```

---

```text
审慎
```

---

# 第四十七章 Character Library Construction

## 定位

建立：

```text
汉字语义库
```

---

# 第一阶段

```text
5000字
```

---

# 每个字

记录：

### 本义

---

### 引申义

---

### 文化义

---

### 使用频率

---

### 姓名适配度

---

# Schema

```json
{
  "char":"知",

  "meaning":"认知",

  "culture_tags":[]
}
```

---

# 第四十八章 Character Risk Library

## 建立

风险字库

---

记录：

### 生僻字

---

### 多音字

---

### 谐音风险

---

### 负面语义

---

# 示例

```text
玥
```

高频。

---

```text
梓
```

过热。

---

```text
汐
```

模板化。

---

# 第四十九章 Template Blacklist

## 项目成败关键

---

建立：

```text
Template Blacklist
```

---

# 第一阶段目标

```text
10000+
```

名字。

---

# 来源

### 公安姓名数据

---

### 新生儿榜单

---

### 起名网站

---

### AI生成结果

---

# 分类

### 高频名

---

### AI名

---

### 小说名

---

### 网红名

---

# 示例

```text
若汐
```

---

```text
沐辰
```

---

```text
梓涵
```

---

```text
子墨
```

---

```text
一诺
```

---

# 第五十章 Template Detector Training

## 输入

```text
林若汐
```

---

# 输出

```json
{
  "template":true,

  "confidence":98
}
```

---

# 验收

准确率：

```text
>95%
```

---

# 第五十一章 Human Naming Corpus

## 项目最大护城河

---

建立：

```text
Human Naming Corpus
```

---

目标：

```text
100000+
真实姓名
```

---

来源：

### 历史人物

---

### 企业家

---

### 学者

---

### 作家

---

### 近代名人

---

### 地域优秀姓名

---

# 第五十二章 Human Detector Dataset

## 正样本

```text
优秀真实姓名
```

---

## 负样本

```text
AI姓名
```

---

```text
模板姓名
```

---

```text
小说姓名
```

---

# 数据量

```text
200000+
```

---

# 第五十三章 Human Detector Training

## 输出

```json
{
  "human_score":91
}
```

---

# 目标

优秀姓名：

```text
>90
```

---

模板姓名：

```text
<70
```

---

# 第五十四章 Knowledge Base Versioning

## 所有知识库

必须：

```text
版本管理
```

---

例如：

```text
structure_v1
```

---

```text
culture_v3
```

---

```text
template_v5
```

---

# 第五十五章 Knowledge Audit

## 每条知识

必须记录：

```text
来源
```

---

```text
作者
```

---

```text
时间
```

---

```text
版本
```

---

禁止：

```text
来源不明
```

---

# 第五十六章 Knowledge Philosophy

系统最终差异：

不是：

```text
模型差异
```

---

而是：

```text
知识差异
```

---

未来竞争对手：

复制：

```text
Prompt
```

容易。

---

复制：

```text
Agent
```

容易。

---

复制：

```text
10万条命名知识库
```

极难。

---

因此：

```text
Knowledge Base

=

系统核心资产
```

---

# 文档状态

```text
Draft Complete
```

---

# Part 4 End

# 第五十七章 Frontend Development Plan

## 定位

构建：

```text id="a1m8q2"
用户可感知产品层
```

---

原则：

用户看到的：

不是：

```text id="b2v7m4"
Agent
```

---

不是：

```text id="c3m8q5"
NES
```

---

而是：

```text id="d4v7m1"
专业命名顾问
```

体验。

---

# 产品定位

```text id="e5m8q3"
AI命名顾问
```

---

而非：

```text id="f6v7m2"
AI名字生成器
```

---

# 第五十八章 Frontend Technology Stack

## Web

推荐：

```text id="g7m8q4"
Next.js 15
```

---

UI：

```text id="h8v3m5"
Shadcn UI
```

---

样式：

```text id="i9m7q1"
TailwindCSS
```

---

状态管理：

```text id="j1v8m2"
Zustand
```

---

图表：

```text id="k2m7q4"
Recharts
```

---

PDF预览：

```text id="l3v8m5"
React PDF
```

---

# 第五十九章 页面架构

## 用户端

```text id="m4v7m1"
Home
```

---

```text id="n5m8q2"
Naming Wizard
```

---

```text id="o6v7m4"
Processing
```

---

```text id="p7m8q5"
Top3 Result
```

---

```text id="q8v7m1"
Full Report
```

---

```text id="r9m8q3"
History
```

---

# 管理端

```text id="s1v7m2"
Dashboard
```

---

```text id="t2m8q4"
Knowledge Base
```

---

```text id="u3v8m5"
Audit Center
```

---

```text id="v4m7q1"
Prompt Center
```

---

```text id="w5m8q2"
System Metrics
```

---

# 第六十章 Home Page

## 定位

成交页。

---

不是：

```text id="x6v7m4"
功能页
```

---

# 页面结构

## Hero

---

## 命名理念

---

## 命名案例

---

## 命名流程

---

## 开始命名

---

# CTA

```text id="y7m8q5"
立即生成专属名字
```

---

# 第六十一章 Naming Wizard

## Step 1

姓氏。

---

## Step 2

性别。

---

## Step 3

出生日期。

---

## Step 4

出生时间。

---

## Step 5

出生地。

---

## Step 6

家庭偏好（可选）。

---

# 输出

```text id="z8v7m1"
Create Session
```

---

# 第六十二章 Processing Page

## 定位

等待页。

---

# 实时显示

```text id="a9m8q3"
Profile分析中
```

---

```text id="b1v7m2"
Structure分析中
```

---

```text id="c2m8q4"
Archetype分析中
```

---

```text id="d3v8m5"
Culture分析中
```

---

```text id="e4m7q1"
生成候选名
```

---

```text id="f5m8q2"
质量审查中
```

---

```text id="g6v7m4"
生成最终报告
```

---

# 用户感知

增强：

```text id="h7m8q5"
专业度
```

---

# 第六十三章 Top3 Result Page

## 项目核心页面

---

# 展示

```text id="i8v7m1"
Top1
```

---

```text id="j9m8q3"
Top2
```

---

```text id="k1v7m2"
Top3
```

---

# 每个名字展示

### 姓名

---

### NES评分

---

### 人格标签

---

### 文化出处

---

### 一句话解释

---

# 示例

```text id="l2m8q4"
林知微

NES 91

书卷学者

见微知著

洞察细微而见未来
```

---

# 第六十四章 Explainability UI

## 项目差异化核心

---

展示：

```text id="m3v8m5"
证据链
```

---

# UI

```text id="n4m7q1"
Structure
```

↓

```text id="o5m8q2"
Archetype
```

↓

```text id="p6v7m4"
Culture
```

↓

```text id="q7m8q5"
Name
```

---

# 示例

```text id="r8v7m1"
书卷型

↓

书卷学者

↓

论语

↓

知微
```

---

# 用户一眼看懂

为什么成立。

---

# 第六十五章 Top3 Compare UI

## 展示方式

表格对比。

---

| 项目  | Top1 | Top2 | Top3 |
| --- | ---- | ---- | ---- |
| NES | 91   | 89   | 88   |
| 人格  | 学者   | 君子   | 修行者  |
| 文化  | 论语   | 大学   | 庄子   |
| 风格  | 沉稳   | 大气   | 灵动   |

---

# 用户价值

增强：

```text id="s9m8q3"
决策感
```

---

# 第六十六章 Full Report Page

## 内容

### 命名摘要

---

### Top1解析

---

### Structure解析

---

### Archetype解析

---

### Culture解析

---

### Top3对比

---

### 风险分析

---

### 成长建议

---

# 输出

```text id="t1v7m2"
网页版
```

*

```text id="u2m8q4"
PDF版
```

---

# 第六十七章 PDF Builder

## 技术

推荐：

```text id="v3v8m5"
Playwright
```

---

生成：

```text id="w4m7q1"
高质量PDF
```

---

# 风格

参考：

```text id="x5m8q2"
高端咨询报告
```

---

而不是：

```text id="y6v7m4"
普通起名报告
```

---

# 第六十八章 Dashboard

## 管理后台首页

---

展示：

### Session数量

---

### Top1通过率

---

### NES均值

---

### Human Score均值

---

### Top模板命中

---

# 第六十九章 Knowledge Base CMS

## 管理

### Structure

---

### Archetype

---

### Culture

---

### Character

---

### Template

---

# 功能

增删改查。

---

# 第七十章 Audit Center

## 查看

### Session

---

### Candidate

---

### Ranking

---

### Report

---

### Event

---

# 支持

```text id="z7m8q5"
全链路追踪
```

---

# 第七十一章 Product KPI

## MVP阶段

### Session完成率

> 80%

---

### Top1满意度

> 70%

---

### 报告打开率

> 90%

---

### 平均生成时间

<30秒

---

# 第七十二章 Frontend Philosophy

用户最终购买的：

不是：

```text id="a8v7m1"
名字
```

---

而是：

```text id="b9m8q3"
被理解感
```

---

因此：

```text id="c1v7m2"
Explainability UI
```

优先级：

高于：

```text id="d2m8q4"
名字展示UI
```

---

# 文档状态

```text id="e3v8m5"
Draft Complete
```

---

# Part 5 End

# 第七十三章 Prompt Engineering Development Plan

## 定位

建立：

```text
Prompt Layer
```

---

作用：

连接：

```text
Knowledge Base

↓

Generator

↓

Critique

↓

Report
```

---

原则：

Prompt：

不是：

```text
业务逻辑
```

---

而是：

```text
推理接口
```

---

# 第七十四章 Prompt Architecture

## 分层

```text
System Prompt
```

↓

```text
Role Prompt
```

↓

```text
Task Prompt
```

↓

```text
Output Schema
```

---

禁止：

```text
超级长Prompt
```

---

必须：

```text
模块化Prompt
```

---

# 第七十五章 Structure Prompt

## 输入

```json
{
  "profile":{}
}
```

---

## 输出

```json
{
  "structure":"S06"
}
```

---

# Prompt职责

负责：

```text
Structure匹配
```

---

不负责：

```text
生成名字
```

---

# 第七十六章 Archetype Prompt

## 输入

```json
{
  "structure":"S06"
}
```

---

## 输出

```json
{
  "archetype":"A01"
}
```

---

# Prompt职责

负责：

```text
人格推理
```

---

不负责：

```text
名字推理
```

---

# 第七十七章 Culture Prompt

## 输入

```json
{
  "archetype":"A01"
}
```

---

## 输出

```json
{
  "culture":"论语"
}
```

---

# Prompt职责

负责：

```text
文化匹配
```

---

# 第七十八章 Generator Prompt

## 系统核心Prompt

---

输入：

```json
{
  "structure":"S06",

  "archetype":"A01",

  "culture":"论语"
}
```

---

输出：

```json
{
  "candidates":[]
}
```

---

# 约束

必须：

```text
人格优先
```

---

必须：

```text
文化优先
```

---

禁止：

```text
高频模板名
```

---

禁止：

```text
网红宝宝名
```

---

# 第七十九章 Critique Prompt

## 输入

```json
{
  "candidate":"知微"
}
```

---

## 输出

```json
{
  "passed":true
}
```

---

# 检查项

### 结构一致

---

### 人格一致

---

### 文化一致

---

### 审美一致

---

# 第八十章 Prompt Registry

## 定位

统一管理Prompt

---

# Schema

```json
{
  "prompt_id":"GENERATOR_V1",

  "version":"1.0.0"
}
```

---

# 功能

### 版本管理

---

### 灰度发布

---

### 回滚

---

# 第八十一章 RAG Architecture

## 定位

知识库检索层

---

# 流程

```text
Query

↓

Retriever

↓

Knowledge Chunk

↓

Prompt

↓

LLM
```

---

# 数据源

### Structure

---

### Archetype

---

### Culture

---

### Character

---

# 第八十二章 Embedding Strategy

## 推荐

```text
bge-m3
```

---

或：

```text
text-embedding-3-large
```

---

# Chunk Size

```text
300~500 Token
```

---

# Overlap

```text
50 Token
```

---

# 第八十三章 Vector Database

## 推荐

```text
Qdrant
```

---

原因：

```text
简单

稳定

便宜
```

---

# 不推荐

```text
Pinecone
```

作为V1。

---

# 第八十四章 Generator Training Plan

## 目标

解决：

```text
名字同质化
```

---

# 第一阶段

建立：

```text
5000优质名字样本
```

---

# 第二阶段

建立：

```text
Structure→Name
```

映射。

---

# 第三阶段

建立：

```text
Archetype→Name
```

映射。

---

# 第四阶段

建立：

```text
Culture→Name
```

映射。

---

# 第八十五章 Human Detector Development

## V1

规则评分。

---

# V2

Embedding相似度。

---

# V3

分类模型。

---

# 输入

```text
林知微
```

---

# 输出

```json
{
  "human_score":91
}
```

---

# 第八十六章 Human Detector Dataset

## 正样本

```text
历史名人姓名
```

---

```text
企业家姓名
```

---

```text
学者姓名
```

---

```text
优秀真实姓名
```

---

## 负样本

```text
AI生成姓名
```

---

```text
模板姓名
```

---

```text
小说姓名
```

---

# 第八十七章 Template Detector Development

## 第一阶段

规则库。

---

## 第二阶段

向量相似度。

---

## 第三阶段

分类模型。

---

# 输入

```text
林若汐
```

---

# 输出

```json
{
  "template":true,

  "confidence":98
}
```

---

# 第八十八章 Knowledge Retrieval Pipeline

## 流程

```text
Archetype

↓

Culture Search

↓

Quote Search

↓

Character Search

↓

Generation
```

---

# 目标

保证：

```text
名字来源于知识
```

---

而不是：

```text
来源于幻觉
```

---

# 第八十九章 Prompt Evaluation Framework

## 评估指标

### Diversity

---

### Human Score

---

### Aesthetic

---

### NES

---

### Template Rate

---

# 发布条件

```text
Template Rate

<5%
```

---

```text
Human Score

>90
```

---

# 第九十章 AI Layer Acceptance

## 验收标准

### Prompt Registry

PASS

---

### RAG

PASS

---

### Generator

PASS

---

### Human Detector

PASS

---

### Template Detector

PASS

---

### Knowledge Retrieval

PASS

---

# 第九十一章 AI Philosophy

真正优秀的命名系统：

不是：

```text
让模型更聪明
```

---

而是：

```text
让模型受到约束
```

---

因此：

```text
Knowledge

>

Prompt

>

Model
```

---

优先级排序成立。

---

# 文档状态

```text
Draft Complete
```

---

# Part 6 End

# 第九十二章 Quality Assurance Strategy

## 定位

建立：

```text id="a1m8q2"
命名质量保障体系
```

---

目标：

确保：

```text id="b2v7m4"
每次发布

不会让系统退化
```

---

避免：

```text id="c3m8q5"
修一个Bug

新增十个Bug
```

---

# QA原则

任何升级：

必须通过：

```text id="d4v7m1"
自动化测试
```

---

```text id="e5m8q3"
回归测试
```

---

```text id="f6v7m2"
命名质量测试
```

---

才能发布。

---

# 第九十三章 Test Environment

## 环境规划

### DEV

开发环境

---

### QA

测试环境

---

### STAGING

预发布环境

---

### PROD

生产环境

---

# 原则

禁止：

```text id="g7m8q4"
直接在生产环境验证
```

---

# 第九十四章 Benchmark Dataset

## 定位

建立：

```text id="h8v3m5"
黄金测试集
```

---

作用：

验证：

```text id="i9m7q1"
系统升级后
```

结果是否变化。

---

# 第一阶段

建立：

```text id="j1v8m2"
1000 Case
```

---

# 第二阶段

建立：

```text id="k2m7q4"
5000 Case
```

---

# 第三阶段

建立：

```text id="l3v8m5"
10000 Case
```

---

# 第九十五章 Benchmark Structure

## 每个Case

包含：

```json id="m4v7m1"
{
  "input":{},

  "expected_structure":"S06",

  "expected_archetype":"A01"
}
```

---

# 扩展

```json id="n5m8q2"
{
  "expected_culture":"C01",

  "expected_quality":"HIGH"
}
```

---

# 第九十六章 Structure Test

## 测试目标

验证：

```text id="o6v7m4"
Structure Engine
```

---

# 输入

固定：

```text id="p7m8q5"
Benchmark Case
```

---

# 输出

```text id="q8v7m1"
Structure
```

---

# 验收

准确率：

```text id="r9m8q3"
≥90%
```

---

# 第九十七章 Archetype Test

## 验证

```text id="s1v7m2"
Structure

↓

Archetype
```

映射。

---

# 验收

准确率：

```text id="t2m8q4"
≥90%
```

---

# 第九十八章 Culture Test

## 验证

```text id="u3v8m5"
Archetype

↓

Culture
```

链路。

---

# 检查

### 文化匹配

---

### 文化深度

---

### 文化来源

---

# 验收

```text id="v4m7q1"
≥90%
```

---

# 第九十九章 Generator Test

## 核心测试

验证：

```text id="w5m8q2"
200 Candidate
```

---

# 指标

### 重复率

---

### 模板率

---

### Human Score

---

### Diversity

---

# 验收

重复率：

```text id="x6v7m4"
<5%
```

---

模板率：

```text id="y7m8q5"
<5%
```

---

# 第一百章 Critique Test

## 验证

### Self Critique

---

### Red Team

---

### Template Detector

---

### Human Detector

---

# 输入

```text id="z8v7m1"
已知模板姓名
```

---

# 输出

必须：

```text id="a9m8q3"
Reject
```

---

# 第一百零一章 NES Test

## 验证

评分正确性。

---

# 检查

```text id="b1v7m2"
总分
=
子项分数之和
```

---

# 禁止

```text id="c2m8q4"
隐藏加分
```

---

# 第一百零二章 Ranking Test

## 验证

```text id="d3v8m5"
Top3选择
```

---

# 检查

### NES排序

---

### Tie Break

---

### Diversity

---

# 验收

```text id="e4m7q1"
Top3稳定率

>95%
```

---

# 第一百零三章 Report Test

## 验证

报告生成。

---

# 检查

### Evidence Chain

---

### Explainability

---

### Risk Analysis

---

# 验收

解释链完整率：

```text id="f5m8q2"
100%
```

---

# 第一百零四章 End-to-End Test

## E2E流程

```text id="g6v7m4"
Input

↓

Structure

↓

Archetype

↓

Culture

↓

Generation

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

# 验证

全链路通过。

---

# 第一百零五章 Regression Test

## 定位

系统升级后：

自动执行。

---

# 检查

```text id="h7m8q5"
Top1变化率
```

---

```text id="i8v7m1"
Top3变化率
```

---

```text id="j9m8q3"
NES变化率
```

---

# 阈值

```text id="k1v7m2"
<5%
```

---

# 第一百零六章 Prompt Regression Test

## 验证

Prompt升级。

---

# 检查

### Template Rate

---

### Human Score

---

### Diversity

---

### Top1 Stability

---

# 发布条件

全部通过。

---

# 第一百零七章 Knowledge Regression Test

## 验证

知识库升级。

---

# 检查

### Structure变化

---

### Archetype变化

---

### Culture变化

---

# 防止

```text id="l2m8q4"
知识污染
```

---

# 第一百零八章 Performance Test

## 验证

性能指标。

---

# 目标

单次命名：

```text id="m3v8m5"
<30秒
```

---

Top3生成：

```text id="n4m7q1"
<20秒
```

---

报告生成：

```text id="o5m8q2"
<10秒
```

---

# 第一百零九章 Load Test

## 并发

V1目标：

```text id="p6v7m4"
100 Session/Day
```

---

V2目标：

```text id="q7m8q5"
1000 Session/Day
```

---

# 压测

### 50并发

---

### 100并发

---

### 500并发

---

# 第一百一十章 Human Evaluation Program

## 项目核心

机器测试不够。

---

必须建立：

```text id="r8v7m1"
专家评审团
```

---

# 组成

### 起名师

---

### 中文系老师

---

### 国学研究者

---

### 普通家长

---

# 第一百一十一章 Human Scorecard

## 评分维度

### 高级感

---

### 文化感

---

### 独特性

---

### 记忆点

---

### 真实感

---

# 满分

```text id="s9m8q3"
100
```

---

# 第一百一十二章 Release Gate

## 发布前

必须通过：

### Unit Test

PASS

---

### Integration Test

PASS

---

### E2E Test

PASS

---

### Regression Test

PASS

---

### Human Evaluation

PASS

---

# 否则

```text id="t1v7m2"
禁止发布
```

---

# 第一百一十三章 QA Philosophy

系统真正目标：

不是：

```text id="u2m8q4"
生成名字
```

---

而是：

```text id="v3v8m5"
持续生成高质量名字
```

---

因此：

```text id="w4m7q1"
QA

不是附属模块
```

---

而是：

```text id="x5m8q2"
产品核心能力
```

---

# 文档状态

```text id="y6v7m4"
Draft Complete
```

---

# Part 7 End

# 第一百一十四章 Continuous Improvement Plan

## 定位

建立：

```text id="a1m8q2"
系统进化机制
```

---

目标：

解决：

```text id="b2v7m4"
知识老化
```

---

```text id="c3m8q5"
审美老化
```

---

```text id="d4v7m1"
名字同质化
```

---

问题。

---

# 核心原则

系统：

不是：

```text id="e5m8q3"
一次开发完成
```

---

而是：

```text id="f6v7m2"
持续成长
```

---

# 第一百一十五章 Feedback Loop

## 用户反馈闭环

---

用户行为：

```text id="g7m8q4"
查看Top3
```

↓

```text id="h8v3m5"
选择Top1
```

↓

```text id="i9m7q1"
保存报告
```

↓

```text id="j1v8m2"
购买命名服务
```

↓

```text id="k2m7q4"
反馈满意度
```

---

形成：

```text id="l3v8m5"
Feedback Dataset
```

---

# 第一百一十六章 Feedback Schema

## Schema

```json id="m4v7m1"
{
  "session_id":"SID001",

  "selected_name":"CID001",

  "rating":5,

  "comment":"..."
}
```

---

# 评分

```text id="n5m8q2"
1
```

差。

---

```text id="o6v7m4"
5
```

优秀。

---

# 第一百一十七章 Selection Tracking

## 定位

记录：

```text id="p7m8q5"
用户最终选择
```

---

# Schema

```json id="q8v7m1"
{
  "session_id":"SID001",

  "selected_rank":"TOP2"
}
```

---

# 作用

发现：

```text id="r9m8q3"
系统判断

与

用户偏好

差异
```

---

# 第一百一十八章 Naming Memory

## 定位

建立：

```text id="s1v7m2"
命名记忆层
```

---

# 记录

### 用户偏好

---

### 家族偏好

---

### 风格偏好

---

### 地域偏好

---

# 示例

```json id="t2m8q4"
{
  "prefer_style":"书卷",

  "avoid_style":"网红"
}
```

---

# 第一百一十九章 Preference Learning

## V1

规则学习。

---

# V2

统计学习。

---

# V3

Embedding学习。

---

# 输入

```text id="u3v8m5"
用户选择记录
```

---

# 输出

```text id="v4m7q1"
偏好画像
```

---

# 第一百二十章 Family Naming Graph

## 定位

建立：

```text id="w5m8q2"
家族命名图谱
```

---

# 记录

### 父母姓名

---

### 兄弟姐妹姓名

---

### 家族字辈

---

### 家族文化偏好

---

# 用途

避免：

```text id="x6v7m4"
风格冲突
```

---

# 第一百二十一章 Knowledge Evolution Engine

## 定位

知识库进化系统。

---

# 输入

```text id="y7m8q5"
用户反馈
```

---

```text id="z8v7m1"
专家反馈
```

---

```text id="a9m8q3"
运营反馈
```

---

# 输出

```text id="b1v7m2"
知识更新建议
```

---

# 第一百二十二章 Culture Expansion Plan

## 每月新增

```text id="c2m8q4"
100+
```

文化片段。

---

# 来源

### 古籍

---

### 地方文化

---

### 历史人物

---

### 现代优秀人物

---

# 原则

禁止：

```text id="d3v8m5"
只新增诗词
```

---

必须：

```text id="e4m7q1"
新增人格文化
```

---

# 第一百二十三章 Character Evolution

## 每月审计

### 高频字

---

### 过热字

---

### 模板字

---

# 示例

```text id="f5m8q2"
梓
```

---

```text id="g6v7m4"
汐
```

---

```text id="h7m8q5"
玥
```

---

# 动态调整

权重。

---

# 第一百二十四章 Template Blacklist Evolution

## 每周更新

新增：

```text id="i8v7m1"
热门模板名
```

---

来源：

### 新生儿榜单

---

### 社交平台

---

### AI生成结果

---

# 目标

保持：

```text id="j9m8q3"
领先市场
```

---

# 第一百二十五章 Human Corpus Evolution

## 每月新增

```text id="k1v7m2"
1000+
```

优秀姓名。

---

# 来源

### 学者

---

### 企业家

---

### 科学家

---

### 艺术家

---

# 作用

提升：

```text id="l2m8q4"
Human Detector
```

---

# 第一百二十六章 Expert Review Program

## 建立

```text id="m3v8m5"
专家委员会
```

---

# 组成

### 命名顾问

---

### 中文学者

---

### 国学研究者

---

### 品牌顾问

---

# 职责

审计：

### Top1

---

### 新知识

---

### 新规则

---

# 第一百二十七章 Monthly Audit

## 每月审计

### Template Rate

---

### Human Score

---

### Diversity

---

### Top1满意度

---

### 报告满意度

---

# 输出

```text id="n4m7q1"
Monthly Review
```

---

# 第一百二十八章 Naming Intelligence Dashboard

## 展示

### 本月Session

---

### 用户满意度

---

### Top1选择率

---

### Top3选择率

---

### Human Score趋势

---

### Template Rate趋势

---

# 第一百二十九章 Self Evolution Roadmap

## V1

规则系统。

---

## V2

知识驱动系统。

---

## V3

反馈驱动系统。

---

## V4

偏好驱动系统。

---

## V5

命名智能体。

---

# 第一百三十章 Long-Term Moat

未来竞争：

不会输给：

```text id="o5m8q2"
模型能力
```

---

会输给：

```text id="p6v7m4"
知识积累速度
```

---

```text id="q7m8q5"
反馈积累速度
```

---

```text id="r8v7m1"
命名数据积累速度
```

---

# 第一百三十一章 Continuous Improvement Philosophy

系统价值：

不是：

```text id="s9m8q3"
今天生成一个好名字
```

---

而是：

```text id="t1v7m2"
三年后

依然持续生成好名字
```

---

因此：

```text id="u2m8q4"
Feedback

+

Knowledge

+

Evolution
```

---

共同构成：

```text id="v3v8m5"
Naming Intelligence Flywheel
```

---

# 文档状态

```text id="w4m7q1"
Draft Complete
```

---

# Part 8 End

# 第一百三十二章 MVP Scope & Roadmap

## 定位

定义：

```text
什么必须做
```

---

定义：

```text
什么延后做
```

---

定义：

```text
什么不做
```

---

目标：

防止：

```text
无限开发
```

---

防止：

```text
永远无法上线
```

---

# 第一百三十三章 当前项目风险

## 风险一

过度架构。

---

现状：

```text
架构完成度

95%
```

---

开发完成度：

```text
0%
```

---

风险：

```text
继续设计

继续补文档

继续补理论
```

---

结果：

```text
产品永远不上线
```

---

# 风险二

知识库过大

---

当前规划：

```text
Culture

3000+
```

---

```text
Character

5000+
```

---

```text
Human Corpus

100000+
```

---

实际：

```text
V1根本不需要
```

---

# 风险三

Agent过多

---

当前：

```text
Structure Agent

Archetype Agent

Culture Agent

Generator Agent

Critique Agent

NES Agent

Report Agent
```

---

实际：

```text
V1

只需要：

4个Agent
```

---

# 第一百三十四章 MVP目标

## 核心目标

证明：

```text
易元命名

比普通AI起名

明显更好
```

---

不是证明：

```text
全世界最强命名系统
```

---

# MVP成功标准

用户看到结果后：

说：

```text
这个名字

确实不一样
```

---

即可。

---

# 第一百三十五章 V1必须做

## Module 1

Structure Engine

---

必须。

---

## Module 2

Archetype Engine

---

必须。

---

## Module 3

Culture Engine

---

必须。

---

## Module 4

Generator Engine

---

必须。

---

## Module 5

Critique Engine

---

必须。

---

## Module 6

NES Engine

---

必须。

---

## Module 7

Ranking Engine

---

必须。

---

## Module 8

Report Engine

---

必须。

---

# 第一百三十六章 V1必须砍掉

## Family Graph

删除。

---

## Preference Learning

删除。

---

## Evolution Engine

删除。

---

## Expert Committee

删除。

---

## CMS后台

删除。

---

## 多租户

删除。

---

## 自动知识进化

删除。

---

## 用户长期记忆

删除。

---

# 原因

这些：

```text
不影响命名质量
```

---

# 第一百三十七章 V1知识库规模

## Structure

目标：

```text
20
```

即可。

---

不是：

```text
50
```

---

## Archetype

目标：

```text
40
```

即可。

---

不是：

```text
100
```

---

## Culture

目标：

```text
500
```

即可。

---

不是：

```text
3000
```

---

## Character

目标：

```text
1500
```

即可。

---

不是：

```text
5000
```

---

## Human Corpus

目标：

```text
10000
```

即可。

---

不是：

```text
100000
```

---

# 第一百三十八章 V1 Agent Architecture

## 保留

### Structure Agent

---

### Generator Agent

---

### Critique Agent

---

### Report Agent

---

# 合并

Archetype

*

Culture

↓

Structure Agent内部完成

---

NES

*

Ranking

↓

Critique Agent内部完成

---

# 结果

从：

```text
7 Agent
```

---

变成：

```text
4 Agent
```

---

# 第一百三十九章 V1数据库

## 仅保留

### sessions

---

### candidates

---

### scores

---

### reports

---

### audits

---

# 暂不建立

### family_graph

---

### user_memory

---

### preference_profile

---

### evolution_history

---

# 第一百四十章 V1 UI

## 页面

仅保留：

### Home

---

### Naming Form

---

### Processing

---

### Result

---

### Report

---

# 删除

### Dashboard

---

### CMS

---

### Audit Center

---

### Prompt Center

---

# 原因

用户看不到。

---

# 第一百四十一章 V1技术栈

## Backend

```text
FastAPI
```

---

## DB

```text
PostgreSQL
```

---

## Cache

```text
Redis
```

---

## AI

```text
LangGraph
```

---

## Frontend

```text
Next.js
```

---

禁止新增：

```text
Kafka
```

---

```text
Elasticsearch
```

---

```text
ClickHouse
```

---

```text
Milvus
```

---

# 第一百四十二章 V1开发时间

## Sprint 0

基础设施

3天

---

## Sprint 1

Structure

5天

---

## Sprint 2

Generator

7天

---

## Sprint 3

Critique

7天

---

## Sprint 4

Report

5天

---

## Sprint 5

UI

5天

---

## Sprint 6

联调

5天

---

# 合计

```text
37天
```

---

# 第一百四十三章 上线标准

满足：

```text
Top3可生成
```

---

满足：

```text
解释链成立
```

---

满足：

```text
模板率<10%
```

---

满足：

```text
Human Score>85
```

---

即可上线。

---

# 第一百四十四章 V2路线图

## 增加

### Family Graph

---

### Preference Learning

---

### CMS

---

### Knowledge Editor

---

### Expert Review

---

# 时间

V1上线后。

---

# 第一百四十五章 V3路线图

## 增加

### Evolution Engine

---

### Feedback Learning

---

### Human Detector Model

---

### Auto Knowledge Growth

---

# 时间

获得真实用户后。

---

# 第一百四十六章 Final MVP Verdict

当前项目：

真正应该做的：

```text
让系统跑起来
```

---

不是：

```text
继续扩文档
```

---

不是：

```text
继续扩知识库
```

---

不是：

```text
继续扩Agent
```

---

# 第一百四十七章 Product Manager Decision

从本章开始：

```text
停止新增架构文档
```

---

优先级切换：

```text
文档阶段
↓
开发阶段
```

---

# 文档状态

```text
Approved
```

---

# Part 9 End

# 第一百四十八章 Launch Plan

## 定位

定义：

```text id="a1m8q2"
项目上线计划
```

---

目标：

```text id="b2v7m4"
从开发完成

到真实用户使用
```

---

# 上线原则

先：

```text id="c3m8q5"
小规模验证
```

---

再：

```text id="d4v7m1"
逐步放量
```

---

禁止：

```text id="e5m8q3"
开发完成

立即大规模推广
```

---

# 第一百四十九章 Development Milestone

## M0

架构完成

---

状态：

```text id="f6v7m2"
已完成
```

---

包含：

```text id="g7m8q4"
02A~02F
```

---

```text id="h8v3m5"
03_DATA_SCHEMA
```

---

```text id="i9m7q1"
04_DEV_PLAN
```

---

# M1

知识库V1

---

内容：

```text id="j1v8m2"
20 Structure
```

---

```text id="k2m7q4"
40 Archetype
```

---

```text id="l3v8m5"
500 Culture
```

---

```text id="m4v7m1"
1500 Character
```

---

# M2

Engine完成

---

完成：

```text id="n5m8q2"
Structure
```

---

```text id="o6v7m4"
Generator
```

---

```text id="p7m8q5"
Critique
```

---

```text id="q8v7m1"
Report
```

---

# M3

Beta上线

---

支持：

```text id="r9m8q3"
真实用户测试
```

---

# M4

正式发布

---

开放：

```text id="s1v7m2"
商业收费
```

---

# 第一百五十章 Timeline

## Week 1

基础设施。

---

## Week 2

Structure Engine。

---

## Week 3

Generator Engine。

---

## Week 4

Critique Engine。

---

## Week 5

Report Engine。

---

## Week 6

Frontend。

---

## Week 7

联调。

---

## Week 8

Beta测试。

---

# 总周期

```text id="t2m8q4"
8周
```

---

# 第一百五十一章 Team Structure

## 单人开发模式

推荐。

---

角色：

### Product Owner

你自己

---

### AI Architect

ChatGPT

---

### Developer

Codex

---

### QA

ChatGPT + 人工

---

# 优势

```text id="u3v8m5"
成本最低
```

---

# 第一百五十二章 双人团队模式

## 成员

### 产品负责人

你

---

### 全栈开发

1人

---

# 周期

```text id="v4m7q1"
6~10周
```

---

# 第一百五十三章 Cost Estimate

## V1

最低成本。

---

# AI成本

```text id="w5m8q2"
OpenAI API
```

---

预计：

```text id="x6v7m4"
100~500 USD/月
```

---

# 服务器

```text id="y7m8q5"
2C4G
```

即可。

---

预计：

```text id="z8v7m1"
20~50 USD/月
```

---

# 数据库

```text id="a9m8q3"
PostgreSQL
```

---

```text id="b1v7m2"
Redis
```

---

可同机部署。

---

# 第一百五十四章 Risk Register

## R1

知识库质量不足。

---

风险：

```text id="c2m8q4"
名字质量下降
```

---

解决：

```text id="d3v8m5"
先做小而精
```

---

# R2

Prompt漂移。

---

风险：

```text id="e4m7q1"
结果不稳定
```

---

解决：

```text id="f5m8q2"
Prompt Registry
```

---

# R3

模板名回归。

---

风险：

```text id="g6v7m4"
再次变成

梓涵生成器
```

---

解决：

```text id="h7m8q5"
Template Blacklist
```

---

```text id="i8v7m1"
Critique Layer
```

---

# R4

开发周期失控。

---

风险：

```text id="j9m8q3"
一年都做不完
```

---

解决：

```text id="k1v7m2"
严格执行V1范围
```

---

# 第一百五十五章 Success Metrics

## 产品指标

### Top1满意度

```text id="l2m8q4"
>80%
```

---

### 报告阅读率

```text id="m3v8m5"
>90%
```

---

### Top3选择率

```text id="n4m7q1"
>95%
```

---

# 技术指标

### Template Rate

```text id="o5m8q2"
<10%
```

---

### Human Score

```text id="p6v7m4"
>85
```

---

### 平均耗时

```text id="q7m8q5"
<30秒
```

---

# 第一百五十六章 Commercial Validation

## 第一阶段

50个真实案例。

---

目标：

```text id="r8v7m1"
验证命名质量
```

---

# 第二阶段

200个真实案例。

---

目标：

```text id="s9m8q3"
验证用户满意度
```

---

# 第三阶段

500个真实案例。

---

目标：

```text id="t1v7m2"
验证商业模式
```

---

# 第一百五十七章 Final Delivery Checklist

## 文档

### PRD

PASS

---

### Data Schema

PASS

---

### Dev Plan

PASS

---

# 架构

### Structure

PASS

---

### Archetype

PASS

---

### Culture

PASS

---

### Generator

PASS

---

### Critique

PASS

---

### NES

PASS

---

### Ranking

PASS

---

### Report

PASS

---

# 产品

### Web UI

READY

---

### API

READY

---

### Database

READY

---

# 第一百五十八章 Project Closure Review

当前阶段：

```text id="u2m8q4"
架构设计完成
```

---

下一阶段：

```text id="v3v8m5"
开发实现
```

---

禁止：

```text id="w4m7q1"
继续无限扩文档
```

---

建议：

```text id="x5m8q2"
开始建立知识库V1
```

---

同时：

```text id="y6v7m4"
启动Codex开发
```

---

# 第一百五十九章 Final Verdict

项目当前成熟度：

## 产品设计

```text id="z7m8q5"
95/100
```

---

## 数据架构

```text id="a8v7m1"
95/100
```

---

## 开发规划

```text id="b9m8q3"
95/100
```

---

## 可开发性

```text id="c1v7m2"
90/100
```

---

## 可上线性

```text id="d2m8q4"
85/100
```

---

剩余最大工作：

不是写文档。

而是：

```text id="e3v8m5"
知识库建设
```

*

```text id="f4m7q1"
工程实现
```

---

# 第一百六十章 Development Handoff

从此刻开始：

```text id="g5m8q2"
产品负责人
```

任务结束。

---

进入：

```text id="h6v7m4"
技术负责人阶段
```

---

后续优先级：

```text id="i7m8q5"
05_TEST_PLAN.md
```

↓

```text id="j8v7m1"
06_KNOWLEDGE_BASE_PLAN.md
```

↓

```text id="k9m8q3"
07_IMPLEMENTATION_GUIDE.md
```

↓

```text id="l1v7m2"
Codex开发
```

---

# 文档状态

```text id="m2m8q4"
Approved
```

---

版本：

```text id="n3v8m5"
04_DEV_PLAN.md

Version 1.0 Final
```

---

# End Of File
