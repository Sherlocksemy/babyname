# 易元命名 Pro

# PROMPT ARCHITECTURE

Version 1.0

---

# 文档定位

本文件定义：

```text id="u8m4q2"
Prompt Layer
```

架构。

---

作用：

建立：

```text id="p5m7q4"
命名生成体系
```

---

解决：

```text id="x2m8q1"
只有评分

没有生成
```

问题。

---

# 第一章 Prompt Layer定位

## 1.1 系统架构

最终架构：

```text id="n7v3m5"
Knowledge Layer

↓

Structure Layer

↓

Archetype Layer

↓

Prompt Layer

↓

Generation Layer

↓

NES Layer
```

---

# 1.2 Prompt Layer职责

负责：

```text id="h4m8q3"
生成名字

生成解释

生成报告
```

---

不负责：

```text id="r8m1q5"
最终评分
```

---

评分：

属于：

```text id="m5v7q2"
NES
```

职责。

---

# 1.3 Prompt Layer原则

原则一：

```text id="u9m2q4"
先结构

后名字
```

---

原则二：

```text id="k7m8q3"
先人格

后文字
```

---

原则三：

```text id="r3v7m2"
先文化

后表达
```

---

# 第二章 Prompt体系总览

V1建立：

```text id="x5m8q2"
六大Prompt
```

---

分别：

```text id="n2v7m4"
P01 Structure Prompt

P02 Archetype Prompt

P03 Culture Prompt

P04 Generation Prompt

P05 Evaluation Prompt

P06 Report Prompt
```

---

# 第三章 P01 Structure Prompt

## 定位

负责：

```text id="j4m8q5"
生成结构
```

---

输入：

```json id="h7v2m1"
{
  "gender":"male",

  "region":"teochew",

  "style":"scholar"
}
```

---

输出：

```json id="u3m7q4"
{
  "primary_structure":"S06",

  "secondary_structure":"S08"
}
```

---

# Prompt模板

```text id="p8v4m2"
你是一位顶级命名顾问。

请根据以下条件：

性别：
{{gender}}

地域：
{{region}}

风格：
{{style}}

从Structure Library中选择：

1个Primary Structure

1个Secondary Structure

要求：

结构清晰

人格明确

符合地域文化

输出JSON。
```

---

# 第四章 P02 Archetype Prompt

## 定位

负责：

```text id="m5q8v1"
生成人格原型
```

---

输入：

```json id="n8m3q2"
{
  "primary_structure":"S06",

  "secondary_structure":"S08"
}
```

---

输出：

```json id="r4v7m5"
{
  "primary_archetype":"书卷学者"
}
```

---

# Prompt模板

```text id="u7m1q8"
根据以下结构：

Primary：
S06

Secondary：
S08

从Archetype Matrix中：

选择最匹配人格原型。

禁止发明新人格。

输出JSON。
```

---

# 第五章 P03 Culture Prompt

## 定位

负责：

```text id="x2m8q4"
选择文化路径
```

---

输入：

```json id="k5v7m2"
{
  "structure":"S06",

  "archetype":"书卷学者"
}
```

---

输出：

```json id="j8m4q1"
{
  "culture_path":"论语"
}
```

---

# Prompt模板

```text id="w4v8m2"
根据：

Structure

Archetype

选择最匹配文化路径。

候选：

论语

大学

中庸

诗经

楚辞

庄子

禁止随机选择。

必须解释原因。
```

---

# 第六章 Prompt Pipeline

## 标准流程

```text id="h2m7q5"
用户资料

↓

Structure Prompt

↓

Archetype Prompt

↓

Culture Prompt

↓

Generation Prompt

↓

NES

↓

Top3
```

---

# 第七章 Prompt Guardrails

禁止：

```text id="u8v3m1"
直接生成名字
```

---

必须：

```text id="r8m2q4"
先结构
```

---

然后：

```text id="k7v4m1"
先人格
```

---

然后：

```text id="n5m8q2"
先文化
```

---

最后：

```text id="m7q4v1"
生成名字
```

---

# 第八章 Prompt Philosophy

生成名字：

不是：

```text id="p3m8q4"
猜名字
```

---

而是：

```text id="h5v7m2"
推导名字
```

---

因此：

```text id="u4m8q5"
Prompt Layer

是整个命名引擎的大脑
```

---

# 文档状态

```text id="p9v2m1"
Draft Complete
```

---

# Part 1 End

# 第九章 P04 Generation Prompt

## 9.1 定位

负责：

```text id="u8m4q2"
真正生成名字
```

---

这是：

```text id="p5m7q4"
全系统最重要Prompt
```

---

因为：

```text id="x2m8q1"
Structure

Archetype

Culture
```

最终都要落地为：

```text id="n7v3m5"
名字
```

---

# 9.2 Generation Layer原则

必须遵循：

```text id="h4m8q3"
Structure First
```

---

禁止：

```text id="r8m1q5"
随机组字
```

---

禁止：

```text id="m5v7q2"
词库抽签
```

---

禁止：

```text id="u9m2q4"
好听优先
```

---

必须：

```text id="k7m8q3"
人格优先
```

---

# 第十章 Name Generation Formula

## 标准公式

```text id="r3v7m2"
Structure

+

Archetype

+

Culture

+

Imagery

↓

Name
```

---

# 示例

输入：

```text id="x5m8q2"
Structure：
书卷型

Archetype：
书卷学者

Culture：
论语
```

---

推导：

```text id="n2v7m4"
学问

↓

洞察

↓

知微
```

---

而不是：

```text id="j4m8q5"
随机挑两个字
```

---

# 第十一章 Generation Prompt模板

## Master Prompt

```text id="h7v2m1"
你是一位大师级中文命名顾问。

你的任务不是组合汉字。

而是根据：

Structure

Archetype

Culture

推导名字。

规则：

1 禁止网红名

2 禁止AI模板名

3 禁止随机组字

4 禁止仅解释名字

5 必须先形成结构

6 必须形成人格

7 必须有文化出处

8 名字必须自然

9 名字必须像真人会取的名字

10 输出JSON
```

---

# 输入模板

```json id="u3m7q4"
{
  "surname":"林",

  "structure":"S06",

  "archetype":"书卷学者",

  "culture":"论语"
}
```

---

# 输出模板

```json id="p8v4m2"
{
  "name":"知微",

  "structure_pattern":"学问+洞察",

  "archetype":"书卷学者",

  "culture_source":"论语"
}
```

---

# 第十二章 AI Name Blacklist

## 12.1 定位

建立：

```text id="m5q8v1"
Prompt黑名单
```

---

防止：

```text id="n8m3q2"
AI味
```

---

# 第一类

若X

---

例如：

```text id="r4v7m5"
若汐

若宁

若棠

若兮
```

---

默认：

```text id="u7m1q8"
拒绝
```

---

# 第二类

梓X

---

例如：

```text id="x2m8q4"
梓宸

梓轩

梓熙
```

---

默认：

```text id="k5v7m2"
拒绝
```

---

# 第三类

XX轩

---

例如：

```text id="j8m4q1"
皓轩

浩轩

宇轩
```

---

默认：

```text id="w4v8m2"
拒绝
```

---

# 第四类

XX宸

---

例如：

```text id="h2m7q5"
子宸

梓宸

宇宸
```

---

默认：

```text id="u8v3m1"
拒绝
```

---

# 第十三章 AI Template Detection Prompt

## Prompt

```text id="r8m2q4"
检查以下名字：

是否属于：

AI模板名

网红名

小说主角名

古偶名

言情名

若是：

返回FAIL
```

---

# 示例

输入：

```text id="k7v4m1"
若汐
```

---

输出：

```json id="n5m8q2"
{
  "template":true,

  "reason":"若X模板"
}
```

---

# 第十四章 Name Diversity Prompt

## 定位

用于：

```text id="m7q4v1"
候选池生成
```

---

# 规则

禁止：

```text id="p3m8q4"
同结构重复
```

---

例如：

```text id="h5v7m2"
知微

知远

知行

知止
```

---

FAIL。

---

# 要求

200个候选名：

至少：

```text id="u4m8q5"
6种结构
```

---

至少：

```text id="p9v2m1"
8种人格
```

---

# 第十五章 Candidate Pool Prompt

## 目标

生成：

```text id="m5q8v4"
200候选名
```

---

组成：

| 类型  | 数量 |
| --- | -- |
| S级  | 20 |
| A级  | 60 |
| B级  | 80 |
| 实验型 | 40 |

---

总计：

```text id="h2v7m3"
200
```

---

# 原则

不是：

```text id="n8m4q2"
200个好名字
```

---

而是：

```text id="j7m3q5"
200个不同方向
```

---

# 第十六章 Generation Quality Gate

生成后：

必须：

```text id="r4v8m1"
Template Check
```

---

```text id="u5m7q2"
Structure Check
```

---

```text id="k8v2m4"
Archetype Check
```

---

```text id="x3m8q1"
Culture Check
```

---

否则：

```text id="p6m7q5"
丢弃
```

---

# 第十七章 Generation Philosophy

优秀名字：

不是：

```text id="h8v4m2"
好听
```

---

而是：

```text id="u2v7m1"
有人格
```

---

不是：

```text id="m8v4q5"
有出处
```

---

而是：

```text id="n5m8q4"
出处支撑人格
```

---

因此：

```text id="u3v7m2"
Generation Prompt

本质上是人格生成器
```

---

# 文档状态

```text id="r7m2q5"
Draft Complete
```

---

# Part 2 End

# 第十八章 P05 Evaluation Prompt

## 18.1 定位

负责：

```text id="u8m4q2"
LLM评审
```

---

作用：

不是替代：

```text id="p5m7q4"
NES
```

---

而是：

```text id="x2m8q1"
辅助NES
```

---

最终原则：

```text id="n7v3m5"
NES决定分数

LLM决定解释
```

---

# 18.2 Evaluation Layer职责

负责：

### 人格解释

---

### 文化解释

---

### 美学解释

---

### 风险提示

---

不负责：

```text id="h4m8q3"
最终定分
```

---

# 第十九章 Dual Review System

## 19.1 定位

建立：

```text id="r8m1q5"
双评审机制
```

---

组成：

```text id="m5v7q2"
Rule Engine

+

LLM Review
```

---

# 第一层

Rule Engine

即：

```text id="u9m2q4"
NES
```

---

输出：

```json id="k7m8q3"
{
  "nes_score":91
}
```

---

# 第二层

LLM Review

输出：

```json id="r3v7m2"
{
  "aesthetic_level":"S",
  "comment":"人格鲜明"
}
```

---

# 19.2 优先级

发生冲突时：

```text id="x5m8q2"
NES优先
```

---

例如：

```text id="n2v7m4"
NES = 62

LLM = 很喜欢
```

---

结果：

```text id="j4m8q5"
62
```

---

不能：

```text id="h7v2m1"
人工加分
```

---

# 第二十章 Evaluation Prompt模板

## Master Prompt

```text id="u3m7q4"
你是一位大师级中文姓名评审专家。

你的职责：

解释名字。

不是给名字打分。

评分由NES完成。

请从以下角度分析：

1 人格原型

2 结构完整性

3 文化出处

4 审美高度

5 风险提示

输出JSON。
```

---

# 输入模板

```json id="p8v4m2"
{
  "name":"知微",

  "structure":"书卷型",

  "archetype":"书卷学者",

  "culture":"论语",

  "nes_score":92
}
```

---

# 输出模板

```json id="m5q8v1"
{
  "personality":"书卷学者",

  "structure_comment":"完整",

  "culture_comment":"论语体系",

  "aesthetic_comment":"高级",

  "risk":"LOW"
}
```

---

# 第二十一章 Aesthetic Evaluation Prompt

## 定位

负责：

```text id="n8m3q2"
高级感评估
```

---

# 核心问题

判断：

```text id="r4v7m5"
像大师取的

还是AI编的
```

---

# Prompt

```text id="u7m1q8"
评估以下名字：

是否具有：

高级感

人格感

文化感

真实感

若存在：

网红感

模板感

AI感

请指出原因。
```

---

# 第二十二章 AI Smell Detection

## 检测项

### 模板感

---

### 网红感

---

### 小说感

---

### 古偶感

---

### 言情感

---

### 玄幻感

---

# 示例

输入：

```text id="x2m8q4"
若汐
```

---

输出：

```json id="k5v7m2"
{
  "ai_smell":95,

  "reason":"若X模板"
}
```

---

# 第二十三章 Explainability Prompt

## 定位

负责：

```text id="j8m4q1"
解释为什么好
```

---

不是：

```text id="w4v8m2"
硬编故事
```

---

# Prompt

```text id="h2m7q5"
解释名字时：

必须引用：

Structure

Archetype

Culture

禁止：

先有名字

再编出处
```

---

# 错误示例

```text id="u8v3m1"
名字生成后

临时找诗词
```

---

FAIL。

---

# 正确示例

```text id="r8m2q4"
论语

↓

书卷学者

↓

知微
```

---

PASS。

---

# 第二十四章 Risk Evaluation Prompt

## 定位

负责：

```text id="k7v4m1"
风险识别
```

---

# 检测项

### 谐音风险

---

### 潮汕读音风险

---

### 生僻字风险

---

### 重名风险

---

### AI模板风险

---

# 输出

```json id="n5m8q2"
{
  "risk_level":"LOW",

  "risks":[]
}
```

---

# 第二十五章 LLM禁止行为

禁止：

```text id="m7q4v1"
直接修改NES
```

---

禁止：

```text id="p3m8q4"
跳过Structure
```

---

禁止：

```text id="h5v7m2"
发明人格
```

---

禁止：

```text id="u4m8q5"
发明出处
```

---

禁止：

```text id="p9v2m1"
自创诗句
```

---

# 第二十六章 Evaluation Confidence

## 输出

```json id="m5q8v4"
{
  "confidence":95
}
```

---

# 标准

| Confidence | 说明  |
| ---------- | --- |
| 95+        | 极稳定 |
| 90-94      | 稳定  |
| 80-89      | 可接受 |
| <80        | 需复核 |

---

# 第二十七章 Evaluation Quality Gate

发布前：

必须：

```text id="h2v7m3"
Explanation PASS
```

---

```text id="n8m4q2"
Risk PASS
```

---

```text id="j7m3q5"
Aesthetic PASS
```

---

```text id="r4v8m1"
AI Smell PASS
```

---

否则：

```text id="u5m7q2"
退回重生成
```

---

# 第二十八章 Evaluation Philosophy

评估名字：

不是问：

```text id="k8v2m4"
喜不喜欢
```

---

而是问：

```text id="x3m8q1"
人格是否成立

结构是否成立

文化是否成立
```

---

因此：

```text id="p6m7q5"
Evaluation Prompt

负责解释

NES负责裁决
```

---

# 文档状态

```text id="h8v4m2"
Draft Complete
```

---

# Part 3 End

# 第二十九章 P06 Report Prompt

## 29.1 定位

负责：

```text id="u8m4q2"
生成命名报告
```

---

作用：

把：

```text id="p5m7q4"
NES

Structure

Archetype

Culture
```

转化为：

```text id="x2m8q1"
用户可理解报告
```

---

# 29.2 Report原则

报告不是：

```text id="n7v3m5"
算命报告
```

---

不是：

```text id="h4m8q3"
诗词堆砌
```

---

更不是：

```text id="r8m1q5"
硬凑故事
```

---

而是：

```text id="m5v7q2"
命名决策解释书
```

---

# 第三十章 Report Layer Architecture

## 输入

```json id="u9m2q4"
{
  "name":"知微",

  "structure":"S06",

  "archetype":"A01",

  "culture":"论语",

  "nes_score":92
}
```

---

# 输出

```text id="k7m8q3"
Top1报告
```

---

包含：

```text id="r3v7m2"
名字

↓

人格

↓

结构

↓

文化

↓

命理

↓

风险

↓

结论
```

---

# 第三十一章 Top1 Report Prompt

## Prompt模板

```text id="x5m8q2"
你是一位顶级命名顾问。

请解释：

为什么Top1是这个名字。

必须按照：

结构

人格

文化

命理

审美

五个维度展开。

禁止：

空洞赞美。

禁止：

诗词堆砌。

禁止：

营销话术。
```

---

# Top1输出结构

## 第一部分

名字结论

---

## 第二部分

人格解析

---

## 第三部分

结构解析

---

## 第四部分

文化出处

---

## 第五部分

NES评分解释

---

## 第六部分

顾问建议

---

# 第三十二章 Top3 Report Prompt

## 定位

负责：

```text id="n2v7m4"
Top3推荐
```

---

# Prompt

```text id="j4m8q5"
请比较：

Top1

Top2

Top3

三者区别。

不要说谁更好。

而要说明：

适合什么家庭。

适合什么人格期待。

适合什么命名方向。
```

---

# 输出示例

```json id="h7v2m1"
{
  "top1":"书卷学者",

  "top2":"君子人格",

  "top3":"修行者"
}
```

---

# 第三十三章 顾问式解释体系

## 错误解释

```text id="u3m7q4"
知微

寓意聪明智慧
```

---

FAIL。

---

原因：

```text id="p8v4m2"
太浅
```

---

# 正确解释

```text id="m5q8v1"
知微

来源于：

见微知著

体现：

书卷学者人格

对应：

学问+洞察结构

最终形成：

认知型人格方向
```

---

PASS。

---

# 第三十四章 Evidence Chain Prompt

## 定位

建立：

```text id="n8m3q2"
证据链
```

---

# 原则

所有结论：

必须：

```text id="r4v7m5"
有来源
```

---

例如：

```text id="u7m1q8"
知微
```

---

必须提供：

### 来源

---

### 原文

---

### 解释

---

### 与人格关系

---

# 输出结构

```json id="x2m8q4"
{
  "source":"论语",

  "quote":"见微知著",

  "reason":"体现洞察力"
}
```

---

# 第三十五章 Naming Recommendation Prompt

## 定位

负责：

```text id="k5v7m2"
顾问建议
```

---

# Prompt

```text id="j8m4q1"
根据：

名字

人格

结构

文化

给出命名建议。

重点：

解释为什么适合。

不要夸大。
```

---

# 示例

```text id="w4v8m2"
如果家庭希望：

孩子未来成为：

认知型人才

研究型人才

长期主义者

则知微是非常匹配的选择。
```

---

# 第三十六章 Anti-Marketing Rule

## 禁止

```text id="h2m7q5"
这是最好的名字
```

---

禁止：

```text id="u8v3m1"
保证成功
```

---

禁止：

```text id="r8m2q4"
大富大贵
```

---

禁止：

```text id="k7v4m1"
改变命运
```

---

# 原因

报告定位：

```text id="n5m8q2"
命名建议
```

---

不是：

```text id="m7q4v1"
神秘学宣传
```

---

# 第三十七章 Report Style Guide

## 风格

要求：

```text id="p3m8q4"
专业

克制

有依据
```

---

禁止：

```text id="h5v7m2"
玄学腔
```

---

禁止：

```text id="u4m8q5"
营销腔
```

---

禁止：

```text id="p9v2m1"
AI腔
```

---

# 示例

禁止：

```text id="m5q8v4"
此名天降祥瑞
```

---

推荐：

```text id="h2v7m3"
此名在人格表达和文化来源上具有较高一致性。
```

---

# 第三十八章 Report Quality Gate

生成报告后：

必须验证：

```text id="n8m4q2"
Evidence PASS
```

---

```text id="j7m3q5"
Explanation PASS
```

---

```text id="r4v8m1"
Risk PASS
```

---

```text id="u5m7q2"
Consistency PASS
```

---

否则：

```text id="k8v2m4"
重新生成
```

---

# 第三十九章 Report Philosophy

报告的价值：

不是：

```text id="x3m8q1"
告诉用户名字好
```

---

而是：

```text id="p6m7q5"
告诉用户

为什么这个名字成立
```

---

因此：

```text id="h8v4m2"
Report Prompt

本质上是：

决策解释器
```

---

# 文档状态

```text id="u2v7m1"
Draft Complete
```

---

# Part 4 End

# 第四十章 Multi-Agent Prompt Architecture

## 40.1 定位

V1开始：

系统不再采用：

```text id="u8m4q2"
单Prompt
```

模式。

---

升级为：

```text id="p5m7q4"
Multi-Agent
```

模式。

---

原因：

```text id="x2m8q1"
一个Agent

无法同时做好：

生成

评分

审计

排序
```

---

# 40.2 Agent架构

```text id="n7v3m5"
Orchestrator Agent

↓

Structure Agent

↓

Archetype Agent

↓

Culture Agent

↓

Generator Agent

↓

Evaluator Agent

↓

Quality Agent

↓

Ranking Agent

↓

Report Agent
```

---

# 第四十一章 Orchestrator Agent

## 定位

系统总控Agent。

---

职责：

```text id="h4m8q3"
任务拆解

流程编排

结果聚合
```

---

不负责：

```text id="r8m1q5"
生成名字
```

---

# 输入

```json id="m5v7q2"
{
  "surname":"林",

  "gender":"male",

  "region":"teochew"
}
```

---

# 输出

```json id="u9m2q4"
{
  "workflow":"naming_v1"
}
```

---

# 第四十二章 Structure Agent

## 定位

负责：

```text id="k7m8q3"
结构决策
```

---

调用：

```text id="r3v7m2"
02D_STRUCTURE_LIBRARY
```

---

输出：

```json id="x5m8q2"
{
  "primary_structure":"S06",

  "secondary_structure":"S08"
}
```

---

# Agent Prompt

```text id="n2v7m4"
根据：

性别

地域

家庭偏好

选择：

Primary Structure

Secondary Structure

禁止直接生成名字。
```

---

# 第四十三章 Archetype Agent

## 定位

负责：

```text id="j4m8q5"
人格决策
```

---

调用：

```text id="h7v2m1"
02C_ARCHETYPE_MATRIX
```

---

输出：

```json id="u3m7q4"
{
  "archetype":"书卷学者"
}
```

---

# Agent Prompt

```text id="p8v4m2"
根据：

Structure

选择：

最匹配人格原型。

禁止发明新人格。
```

---

# 第四十四章 Culture Agent

## 定位

负责：

```text id="m5q8v1"
文化路径决策
```

---

调用：

```text id="n8m3q2"
02A_NAMING_PHILOSOPHY
```

---

输出：

```json id="r4v7m5"
{
  "culture":"论语"
}
```

---

# Agent Prompt

```text id="u7m1q8"
根据：

Structure

Archetype

选择：

文化路径。

必须有出处依据。
```

---

# 第四十五章 Generator Agent

## 定位

负责：

```text id="x2m8q4"
生成候选名
```

---

这是：

```text id="k5v7m2"
唯一允许生成名字的Agent
```

---

输入：

```json id="j8m4q1"
{
  "structure":"S06",

  "archetype":"书卷学者",

  "culture":"论语"
}
```

---

输出：

```json id="w4v8m2"
{
  "candidate_names":[]
}
```

---

# 生成目标

```text id="h2m7q5"
200个候选名
```

---

要求：

```text id="u8v3m1"
高多样性
```

---

# 第四十六章 Evaluator Agent

## 定位

负责：

```text id="r8m2q4"
名字解释
```

---

不负责：

```text id="k7v4m1"
最终评分
```

---

职责：

```text id="n5m8q2"
人格解释

文化解释

审美解释
```

---

# 输入

```json id="m7q4v1"
{
  "name":"知微"
}
```

---

# 输出

```json id="p3m8q4"
{
  "comment":"..."
}
```

---

# 第四十七章 Quality Agent

## 定位

负责：

```text id="h5v7m2"
质量审计
```

---

这是：

```text id="u4m8q5"
全系统最重要Agent
```

---

因为：

```text id="p9v2m1"
决定是否淘汰
```

---

# 检查项

### Template

---

### AI Smell

---

### Structure

---

### Archetype

---

### Culture

---

### Risk

---

# 输出

```json id="m5q8v4"
{
  "passed":true
}
```

---

# 第四十八章 Ranking Agent

## 定位

负责：

```text id="h2v7m3"
Top3排序
```

---

调用：

```text id="n8m4q2"
NES
```

---

排序规则：

```text id="j7m3q5"
NES优先
```

---

不是：

```text id="r4v8m1"
LLM喜欢优先
```

---

# 输入

```json id="u5m7q2"
{
  "candidates":[]
}
```

---

# 输出

```json id="k8v2m4"
{
  "top1":"知微",

  "top2":"景行",

  "top3":"若谷"
}
```

---

# 第四十九章 Report Agent

## 定位

负责：

```text id="x3m8q1"
生成最终报告
```

---

调用：

```text id="p6m7q5"
P06 Report Prompt
```

---

输出：

```text id="h8v4m2"
完整命名报告
```

---

# 第五十章 Agent Communication Protocol

## 统一格式

所有Agent：

输入：

```json id="u2v7m1"
{
  "input":{}
}
```

---

输出：

```json id="m8v4q5"
{
  "output":{}
}
```

---

禁止：

```text id="n5m8q4"
自由文本
```

---

原因：

```text id="u3v7m2"
方便编排
```

---

# 第五十一章 Agent Failure Recovery

## Structure失败

重新调用：

```text id="r7m2q5"
Structure Agent
```

---

# Archetype失败

重新调用：

```text id="k4m8q1"
Archetype Agent
```

---

# Generator失败

重新生成：

```text id="p8v3m4"
候选池
```

---

# Quality失败

直接：

```text id="x2m7q1"
淘汰
```

---

# 第五十二章 Multi-Agent Philosophy

优秀命名系统：

不是：

```text id="h7v4m2"
一个超级Prompt
```

---

而是：

```text id="u6m8q5"
多个专家Agent
```

---

协同完成：

```text id="j3m8q2"
结构

人格

文化

生成

评分

报告
```

---

# 文档状态

```text id="m8v4q1"
Draft Complete
```

---

# Part 5 End

# 第五十三章 Self-Critique Agent

## 53.1 定位

负责：

```text id="u8m4q2"
自我批判
```

---

作用：

解决：

```text id="p5m7q4"
模型自嗨
```

问题。

---

# 53.2 核心原则

Generator Agent：

负责：

```text id="x2m8q1"
创造
```

---

Self-Critique Agent：

负责：

```text id="n7v3m5"
怀疑
```

---

# 53.3 Prompt

```text id="h4m8q3"
请站在最苛刻命名顾问角度。

检查以下名字：

是否存在：

模板化

AI味

结构缺失

文化牵强

人格模糊

如果发现问题：

直接淘汰。
```

---

# 输入

```json id="r8m1q5"
{
  "name":"若汐"
}
```

---

# 输出

```json id="m5v7q2"
{
  "passed":false,

  "reason":"若X模板"
}
```

---

# 第五十四章 Red Team Agent

## 54.1 定位

负责：

```text id="u9m2q4"
攻击名字
```

---

作用：

不是证明：

```text id="k7m8q3"
名字有多好
```

---

而是寻找：

```text id="r3v7m2"
名字为什么不好
```

---

# 54.2 检测维度

### 是否像小说主角

---

### 是否像古偶角色

---

### 是否像AI生成

---

### 是否像网红名

---

### 是否像营销包装

---

# Prompt

```text id="x5m8q2"
请扮演最严格的反对者。

寻找这个名字的所有缺点。

不要解释优点。

只寻找缺点。
```

---

# 第五十五章 Anti-Template Agent

## 55.1 定位

负责：

```text id="n2v7m4"
模板检测
```

---

# V1模板库

## Prefix模板

```text id="j4m8q5"
若X

子X

梓X

沐X

可X
```

---

## Suffix模板

```text id="h7v2m1"
XX轩

XX宸

XX熙

XX涵

XX萱
```

---

## Semantic模板

```text id="u3m7q4"
仙气

治愈

温柔

高级感
```

---

# 55.2 Prompt

```text id="p8v4m2"
检测以下名字：

是否命中：

Prefix

Suffix

Semantic

Template

若命中：

直接FAIL
```

---

# 输出

```json id="m5q8v1"
{
  "template":true,

  "type":"Prefix"
}
```

---

# 第五十六章 AestheticGuard Agent

## 56.1 定位

负责：

```text id="n8m3q2"
高级感守门
```

---

这是：

```text id="r4v7m5"
易元命名核心Agent
```

---

# 判断标准

核心问题：

```text id="u7m1q8"
像大师取的

还是AI取的
```

---

# 五维评估

| 项目  | 分值 |
| --- | -- |
| 人格感 | 20 |
| 文化感 | 20 |
| 结构感 | 20 |
| 真实感 | 20 |
| 审美感 | 20 |

---

总分：

```text id="x2m8q4"
100
```

---

# 第五十七章 Aesthetic Score

## S+

```text id="k5v7m2"
95+
```

---

## S

```text id="j8m4q1"
90~94
```

---

## A

```text id="w4v8m2"
80~89
```

---

## B

```text id="h2m7q5"
70~79
```

---

## FAIL

```text id="u8v3m1"
<70
```

---

# 第五十八章 Human Name Detector

## 定位

判断：

```text id="r8m2q4"
真人概率
```

---

# Prompt

```text id="k7v4m1"
请判断：

这个名字是否像：

真实家庭会取的名字。

而不是：

AI生成的名字。

输出：

0~100。
```

---

# 示例

```text id="n5m8q2"
知微
```

---

输出：

```text id="m7q4v1"
92
```

---

# 示例

```text id="p3m8q4"
若汐
```

---

输出：

```text id="h5v7m2"
45
```

---

# 第五十九章 Repetition Detector

## 定位

解决：

```text id="u4m8q5"
名字反复重复
```

问题。

---

# 检查项

统计：

```text id="p9v2m1"
候选池200名
```

---

出现频率。

---

# 规则

同字：

```text id="m5q8v4"
>3次
```

---

扣分。

---

例如：

```text id="h2v7m3"
知微

知远

知行

知止
```

---

触发：

```text id="n8m4q2"
重复告警
```

---

# 第六十章 DiversityGuard Agent

## 定位

负责：

```text id="j7m3q5"
多样性审计
```

---

# 检查

### Structure Diversity

---

### Archetype Diversity

---

### Culture Diversity

---

### Character Diversity

---

# 输出

```json id="r4v8m1"
{
  "passed":true,

  "diversity_score":94
}
```

---

# 第六十一章 Elite Name Detector

## 定位

检测：

```text id="u5m7q2"
大师级名字
```

---

# 条件

同时满足：

```text id="k8v2m4"
Structure ≥18
```

---

```text id="x3m8q1"
Archetype ≥14
```

---

```text id="p6m7q5"
Culture ≥22
```

---

```text id="h8v4m2"
Aesthetic ≥90
```

---

判定：

```text id="u2v7m1"
Elite
```

---

# 第六十二章 Critique Layer Workflow

```text id="m8v4q5"
Generator

↓

Self-Critique

↓

Red Team

↓

Anti-Template

↓

AestheticGuard

↓

Human Detector

↓

DiversityGuard

↓

Quality Agent
```

---

# 第六十三章 Critique Philosophy

优秀系统：

不是：

```text id="n5m8q4"
不断生成
```

---

而是：

```text id="u3v7m2"
不断淘汰
```

---

真正的大师级名字：

不是：

```text id="r7m2q5"
生成出来
```

---

而是：

```text id="k4m8q1"
筛选出来
```

---

# 文档状态

```text id="p8v3m4"
Draft Complete
```

---

# Part 6 End

# 第六十四章 Candidate Generation Strategy

## 64.1 定位

建立：

```text id="u8m4q2"
候选名漏斗体系
```

---

目的：

解决：

```text id="p5m7q4"
直接生成Top1
```

问题。

---

因为：

```text id="x2m8q1"
大师级名字

不是生成出来的
```

---

而是：

```text id="n7v3m5"
筛选出来的
```

---

# 64.2 核心原则

禁止：

```text id="h4m8q3"
一次生成3个名字
```

---

禁止：

```text id="r8m1q5"
一次生成10个名字
```

---

原因：

```text id="m5v7q2"
搜索空间太小
```

---

必须：

```text id="u9m2q4"
大规模生成

小规模筛选
```

---

# 第六十五章 Naming Funnel

## V1标准漏斗

```text id="k7m8q3"
200

↓

50

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

# 阶段一

Generator Agent

---

输出：

```text id="r3v7m2"
200候选名
```

---

目标：

```text id="x5m8q2"
覆盖尽可能多方向
```

---

# 阶段二

Quality Filter

---

淘汰：

```text id="n2v7m4"
模板名

网红名

结构弱名
```

---

保留：

```text id="j4m8q5"
50
```

---

# 阶段三

NES Filter

---

保留：

```text id="h7v2m1"
NES Top20
```

---

# 阶段四

Elite Filter

---

保留：

```text id="u3m7q4"
Top10
```

---

# 阶段五

Diversity Filter

---

保留：

```text id="p8v4m2"
Top3
```

---

# 阶段六

Final Ranking

---

输出：

```text id="m5q8v1"
Top1
```

---

# 第六十六章 Stage 1 Prompt

## 目标

生成：

```text id="n8m3q2"
200候选名
```

---

# Prompt

```text id="r4v7m5"
根据：

Structure

Archetype

Culture

生成200个候选名。

要求：

结构成立

人格成立

文化成立

不要排序。

不要评分。

不要推荐。
```

---

# 生成策略

### 40% 主结构

---

### 30% 邻近结构

---

### 20% 实验结构

---

### 10% 创新结构

---

# 第六十七章 Stage 2 Filter

## Template Filter

淘汰：

```text id="u7m1q8"
若X

梓X

XX轩

XX宸
```

---

# AI Smell Filter

淘汰：

```text id="x2m8q4"
AI味
```

---

# Empty Meaning Filter

淘汰：

```text id="k5v7m2"
空洞名字
```

---

# 输出

```text id="j8m4q1"
50
```

---

# 第六十八章 Stage 3 NES Ranking

## 输入

```text id="w4v8m2"
50名
```

---

# 输出

```text id="h2m7q5"
Top20
```

---

# 排序

依据：

```text id="u8v3m1"
NES
```

---

不是：

```text id="r8m2q4"
LLM喜好
```

---

# 第六十九章 Stage 4 Elite Filter

## 条件

Structure：

```text id="k7v4m1"
≥16
```

---

Archetype：

```text id="n5m8q2"
≥13
```

---

Culture：

```text id="m7q4v1"
≥20
```

---

Aesthetic：

```text id="p3m8q4"
≥85
```

---

保留：

```text id="h5v7m2"
Top10
```

---

# 第七十章 Stage 5 Diversity Filter

## 定位

防止：

```text id="u4m8q5"
Top10长得一样
```

---

# 检查项

### Structure

---

### Archetype

---

### Culture

---

### 高频字

---

# 示例

淘汰：

```text id="p9v2m1"
知微

知远

知行

知止
```

---

原因：

```text id="m5q8v4"
同质化
```

---

# 输出

```text id="h2v7m3"
Top3
```

---

# 第七十一章 Top3 Strategy

## Top1

定位：

```text id="n8m4q2"
最平衡
```

---

## Top2

定位：

```text id="j7m3q5"
更传统
```

---

## Top3

定位：

```text id="r4v8m1"
更独特
```

---

# 示例

```text id="u5m7q2"
Top1

知微
```

---

```text id="k8v2m4"
Top2

景行
```

---

```text id="x3m8q1"
Top3

若谷
```

---

# 第七十二章 Final Decision Tree

```text id="p6m7q5"
200

↓

Template Filter

↓

50

↓

NES

↓

20

↓

Elite Filter

↓

10

↓

Diversity Filter

↓

3

↓

Top1 Ranking

↓

1
```

---

# 第七十三章 Tie Break Rules

## NES相同

比较：

```text id="h8v4m2"
Aesthetic
```

---

仍相同：

比较：

```text id="u2v7m1"
Archetype Clarity
```

---

仍相同：

比较：

```text id="m8v4q5"
Culture Depth
```

---

仍相同：

比较：

```text id="n5m8q4"
Regional Fit
```

---

# 第七十四章 Top1 Selection Prompt

## Prompt

```text id="u3v7m2"
请从Top3中选择Top1。

依据：

NES

Structure

Archetype

Culture

Aesthetic

不要依据：

个人偏好。

不要依据：

模型喜好。
```

---

# 输出

```json id="r7m2q5"
{
  "top1":"知微",

  "reason":"NES最高且人格最清晰"
}
```

---

# 第七十五章 Funnel Philosophy

错误方法：

```text id="k4m8q1"
生成3个

选1个
```

---

正确方法：

```text id="p8v3m4"
生成200个

淘汰197个

留下3个

选1个
```

---

原因：

```text id="x2m7q1"
顶级名字

来自筛选

不是灵感
```

---

# 文档状态

```text id="h7v4m2"
Draft Complete
```

---

# Part 7 End

# 第七十六章 Prompt Dataset

## 76.1 定位

建立：

```text id="u8m4q2"
Prompt Dataset
```

统一数据集。

---

作用：

用于：

```text id="p5m7q4"
训练

测试

回归

升级
```

---

# 76.2 Dataset分类

包含：

```text id="x2m8q1"
Generation Dataset

Evaluation Dataset

Report Dataset

Failure Dataset
```

---

# Generation Dataset

记录：

```text id="n7v3m5"
输入

↓

候选名

↓

最终结果
```

---

# Evaluation Dataset

记录：

```text id="h4m8q3"
NES

↓

解释结果
```

---

# Failure Dataset

记录：

```text id="r8m1q5"
失败案例
```

---

例如：

```text id="m5v7q2"
若汐

梓宸

浩轩
```

---

# 第七十七章 Prompt Versioning

## 定位

建立：

```text id="u9m2q4"
Prompt版本体系
```

---

# Version格式

```text id="k7m8q3"
v1.0.0
```

---

结构：

```text id="r3v7m2"
Major

Minor

Patch
```

---

# Major

变化：

```text id="x5m8q2"
架构升级
```

---

例如：

```text id="n2v7m4"
单Agent

↓

Multi-Agent
```

---

# Minor

变化：

```text id="j4m8q5"
Prompt优化
```

---

# Patch

变化：

```text id="h7v2m1"
Bug修复
```

---

# 第七十八章 Prompt Regression Test

## 定位

防止：

```text id="u3m7q4"
Prompt升级

导致质量下降
```

---

# Golden Cases

固定：

```text id="p8v4m2"
知微

景行

守仁

若谷

怀瑾

弘毅
```

---

# 测试

升级前：

```text id="m5q8v1"
输出A
```

---

升级后：

```text id="n8m3q2"
输出B
```

---

要求：

```text id="r4v7m5"
质量不得下降
```

---

# Case 1

输入：

```json id="u7m1q8"
{
  "surname":"林",

  "gender":"male"
}
```

---

要求：

```text id="x2m8q4"
Top3质量稳定
```

---

# 第七十九章 Prompt Benchmark Suite

## 定位

建立：

```text id="k5v7m2"
Prompt基准测试
```

---

# Benchmark 1

结构生成。

---

验证：

```text id="j8m4q1"
Structure Agent
```

---

# Benchmark 2

人格生成。

---

验证：

```text id="w4v8m2"
Archetype Agent
```

---

# Benchmark 3

文化选择。

---

验证：

```text id="h2m7q5"
Culture Agent
```

---

# Benchmark 4

候选生成。

---

验证：

```text id="u8v3m1"
Generator Agent
```

---

# Benchmark 5

最终排序。

---

验证：

```text id="r8m2q4"
Ranking Agent
```

---

# 第八十章 Prompt Release Gate

## 发布前

必须：

```text id="k7v4m1"
Regression PASS
```

---

```text id="n5m8q2"
Benchmark PASS
```

---

```text id="m7q4v1"
Golden PASS
```

---

```text id="p3m8q4"
Top3 PASS
```

---

```text id="h5v7m2"
Top1 PASS
```

---

```text id="u4m8q5"
Aesthetic PASS
```

---

否则：

```text id="p9v2m1"
禁止上线
```

---

# 第八十一章 Prompt Failure Library

## 定位

建立：

```text id="m5q8v4"
失败案例库
```

---

# 类型一

模板名

---

例如：

```text id="h2v7m3"
若汐

若宁

若棠
```

---

# 类型二

网红名

---

例如：

```text id="n8m4q2"
梓宸

梓轩

梓熙
```

---

# 类型三

结构失效

---

例如：

```text id="j7m3q5"
山川

海涛
```

---

原因：

```text id="r4v8m1"
只有景物
```

---

# 类型四

人格失效

---

例如：

```text id="u5m7q2"
成功

奋斗
```

---

原因：

```text id="k8v2m4"
口号感
```

---

# 第八十二章 Prompt Admin Rules

## 新Prompt准入

必须：

```text id="x3m8q1"
可解释
```

---

```text id="p6m7q5"
可测试
```

---

```text id="h8v4m2"
可回归
```

---

```text id="u2v7m1"
可审计
```

---

# 禁止

禁止：

```text id="m8v4q5"
黑盒Prompt
```

---

例如：

```text id="n5m8q4"
生成100个好名字
```

---

原因：

```text id="u3v7m2"
不可验证
```

---

# 第八十三章 Prompt Architecture Final Mapping

## 最终关系

```text id="r7m2q5"
02A

命名哲学
```

↓

```text id="k4m8q1"
02D

Structure
```

↓

```text id="p8v3m4"
02C

Archetype
```

↓

```text id="x2m7q1"
02E

Prompt
```

↓

```text id="h7v4m2"
02B

NES
```

↓

```text id="u6m8q5"
Top3
```

↓

```text id="j3m8q2"
Top1
```

---

# 第八十四章 Prompt Layer最终审计

## 审计问题

第一轮审计发现：

```text id="m8v4q1"
只有评分

没有生成
```

---

导致：

```text id="f4m8q2"
名字重复

人格失效

文化失效
```

---

# 修复后

建立：

```text id="u5m7q3"
Prompt Layer
```

---

获得：

```text id="p7m8q4"
生成能力
```

---

```text id="n3v7m2"
批判能力
```

---

```text id="r8m4q1"
审计能力
```

---

```text id="k5m7q2"
回归能力
```

---

# 第八十五章 Prompt Philosophy

真正的大师命名：

不是：

```text id="j8m3q5"
想到一个名字
```

---

而是：

```text id="u4m8q1"
设计一个人格
```

---

不是：

```text id="p5v7m4"
找到一句诗
```

---

而是：

```text id="x2m8q3"
建立一套文化逻辑
```

---

不是：

```text id="n7m4q2"
解释名字
```

---

而是：

```text id="h8v3m1"
证明名字成立
```

---

因此：

```text id="r5m8q4"
Prompt Layer

是命名系统的创造引擎
```

---

# 文档状态

```text id="u1v7m5"
Approved
```

---

版本：

```text id="m4q8v2"
02E_PROMPT_ARCHITECTURE.md

Version 1.0 Final
```

---

# End Of File
