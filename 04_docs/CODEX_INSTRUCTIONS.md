# CODEX_INSTRUCTIONS.md｜从 0 到 1 构建新生儿智能取名系统

你现在要从 0 到 1 开发一个“新生儿智能取名系统”。

注意：

这是一个新项目，不是在旧项目上修补。当前只有知识库数据源，项目还没有正式开始开发。

项目目标：

为新生儿父母提供一个简洁、清晰、实用的取名系统。用户输入宝宝的姓氏、性别、出生日期时间、出生地、名字字数、风格偏好、禁用字、喜欢字等信息后，系统输出一组候选名字，并为每个名字提供完整解释，包括寓意、普通话读音、潮汕话读音、诗词典籍出处、八字五行参考、生肖参考、重名热度和风险提示。

请严格按以下开发原则执行：

1. 不要随机拼字。
2. 不要直接让 AI 生成最终名字。
3. 所有名字必须由知识库和规则引擎筛选生成。
4. 所有诗词出处必须来自本地知识库，不能编造。
5. 八字、五格、生肖只作为传统文化参考，不能做绝对化承诺。
6. 项目必须模块化开发。
7. 每个模块必须支持独立测试。
8. 每个开发阶段必须可回退。
9. 不要一开始做复杂 UI、支付、会员、海报功能。
10. 第一阶段只追求名字质量稳定。

请按以下步骤执行：

## Step 1：初始化项目结构

创建项目目录：

```text
baby-name-system/
├── backend/
├── frontend/
├── knowledge_base/
├── docs/
├── scripts/
└── tests/
```

后端使用 Python + FastAPI。
前端使用 Next.js / React。
测试使用 pytest。

## Step 2：迁移知识库

将现有知识库放入：

```text
knowledge_base/
├── compliance/
├── char_attribute/
├── pronunciation/
├── culture_origin/
├── popularity/
└── numerology/
```

当前知识库包含：

1. 通用规范汉字表
2. 字义语义
3. 康熙笔画
4. 五行属性
5. 普通话拼音
6. 潮汕话读音
7. 谐音黑名单
8. 诗经
9. 楚辞
10. 唐诗
11. 宋词
12. 四书五经
13. 字频
14. 热名黑名单
15. 八字规则
16. 五格规则
17. 生肖喜忌

## Step 3：创建文档

在 docs/ 下创建：

1. PRD.md
2. SPEC.md
3. DEV_PLAN.md
4. TEST_PLAN.md
5. DATA_SCHEMA.md
6. API_SCHEMA.md

## Step 4：开发 KnowledgeLoader

创建：

```text
backend/app/core/knowledge_loader.py
```

要求：

1. 能加载所有知识库文件。
2. 能检查文件是否存在。
3. 能检查字段是否完整。
4. 能输出知识库审计报告。
5. 缺失字段不能导致系统崩溃，必须有 warning。

测试文件：

```text
tests/test_knowledge_loader.py
```

## Step 5：开发单字查询模块

创建：

```text
backend/app/services/char_service.py
```

输入一个汉字，输出：

1. 是否合规
2. 普通话拼音
3. 潮汕话读音
4. 康熙笔画
5. 五行
6. 字义
7. 古义
8. 常用度
9. 热度
10. 相关出处

测试文件：

```text
tests/test_char_service.py
```

## Step 6：开发宝宝档案模块

创建：

```text
backend/app/services/baby_profile_service.py
```

输入：

1. 姓氏
2. 性别
3. 出生时间
4. 出生地
5. 日历类型
6. 风格偏好
7. 禁用字
8. 喜欢字

输出：

1. 标准化宝宝档案
2. 生肖
3. 八字
4. 五行分布
5. 建议补益五行
6. 方言检查需求
7. 取名偏好权重

测试文件：

```text
tests/test_baby_profile_service.py
```

## Step 7：开发八字与传统规则模块

创建：

```text
backend/app/engines/bazi_engine.py
backend/app/engines/zodiac_engine.py
backend/app/engines/wuge_engine.py
```

要求：

1. 八字计算必须可解释。
2. 五行分析必须返回过程。
3. 生肖喜忌必须来自知识库。
4. 五格只做参考，不作为唯一标准。

测试文件：

```text
tests/test_bazi_engine.py
tests/test_zodiac_engine.py
tests/test_wuge_engine.py
```

## Step 8：开发候选字池模块

创建：

```text
backend/app/engines/char_pool_builder.py
```

候选字池分为：

1. 合规字池
2. 五行补益字池
3. 文化出处字池
4. 风格偏好字池
5. 用户喜欢字池
6. 辈分字池
7. 备用字池

过滤规则：

1. 禁用字过滤
2. 负面字过滤
3. 热名字过滤
4. 生僻字过滤
5. 谐音风险过滤

测试文件：

```text
tests/test_char_pool_builder.py
```

## Step 9：开发文化出处召回模块

创建：

```text
backend/app/engines/culture_retriever.py
```

支持：

1. 单字直接召回
2. 双字直接召回
3. 意象关联召回
4. 风格召回
5. 五行意象召回

返回字段：

1. source
2. title
3. author
4. original_text
5. matched_chars
6. match_type
7. confidence
8. explanation

要求：

1. 直接出处优先。
2. 意象关联必须明确标注。
3. 没有出处不能伪装有出处。
4. 置信度低于 0.6 不作为核心出处展示。

测试文件：

```text
tests/test_culture_retriever.py
```

## Step 10：开发读音与谐音模块

创建：

```text
backend/app/engines/pronunciation_engine.py
```

检查：

1. 普通话拼音
2. 声调组合
3. 声母韵母搭配
4. 普通话谐音风险
5. 潮汕话读音
6. 潮汕话谐音风险
7. 姓名连读顺口度

测试文件：

```text
tests/test_pronunciation_engine.py
```

## Step 11：开发名字组合模块

创建：

```text
backend/app/engines/name_composer.py
```

支持：

1. 单字名
2. 双字名
3. 固定辈分字
4. 固定喜欢字
5. 锁定某个字继续生成
6. 排除某个字重新生成

组合限制：

1. 两个名用字不能相同。
2. 不能高频重复同一批字。
3. 不能三连同声调。
4. 不能连续同声母导致拗口。
5. 不能爆款字堆叠。

测试文件：

```text
tests/test_name_composer.py
```

## Step 12：开发评分模块

创建：

```text
backend/app/engines/name_scorer.py
```

评分维度：

1. 合规安全：15
2. 普通话音律：15
3. 潮汕话读音：10
4. 字义寓意：15
5. 诗词典籍出处：15
6. 八字五行参考：10
7. 生肖喜忌参考：5
8. 重名热度控制：10
9. 性别与风格匹配：5

测试文件：

```text
tests/test_name_scorer.py
```

## Step 13：开发质量审查模块

创建：

```text
backend/app/quality/quality_guard.py
```

检查：

1. 名字是否重复
2. 单字是否重复过多
3. 出处是否真实相关
4. 解释是否空泛
5. 谐音是否安全
6. 潮汕话读音是否安全
7. 是否爆款字堆叠
8. 是否性别气质不匹配
9. 是否命理表述过度

如果不通过，返回失败原因，并触发重新生成。

测试文件：

```text
tests/test_quality_guard.py
```

## Step 14：开发 API

创建：

```text
backend/app/api/name_routes.py
```

接口：

1. POST /api/names/generate
2. GET /api/names/{request_id}/{name}
3. POST /api/names/regenerate
4. POST /api/favorites
5. GET /api/favorites

## Step 15：开发前端 MVP

只做 4 个页面：

1. 宝宝信息填写页
2. 候选名字列表页
3. 名字详情页
4. 收藏对比页

设计原则：

1. 简洁
2. 清晰
3. 卡片化
4. 每个名字一眼能看懂
5. 不堆砌玄学术语
6. 不做复杂营销包装

## Step 16：建立 Golden Cases

创建：

```text
tests/golden_cases.json
```

至少包含 10 个测试案例：

1. 男宝双字名
2. 女宝双字名
3. 潮汕地区宝宝
4. 带辈分字
5. 禁用爆款字
6. 喜欢固定字
7. 单字名
8. 复姓
9. 出生时间缺失
10. 出生地缺失

## Step 17：开发阶段提交

每个阶段单独提交：

1. phase-0-init
2. phase-1-knowledge-loader
3. phase-2-char-service
4. phase-3-baby-profile
5. phase-4-bazi-engine
6. phase-5-char-pool
7. phase-6-culture-retriever
8. phase-7-pronunciation-engine
9. phase-8-name-composer
10. phase-9-name-scorer
11. phase-10-quality-guard
12. phase-11-api
13. phase-12-frontend-mvp

每次提交前必须运行：

```bash
pytest
```

如果测试失败，不允许进入下一阶段。

最终目标：

用户输入宝宝信息后，系统稳定输出 20 个高质量候选名字。每个名字都必须有完整解释、普通话读音、潮汕话读音、文化出处、八字参考、热度风险和推荐理由。
