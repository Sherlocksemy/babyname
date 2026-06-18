# 04_DEV_PLAN.md｜易元命名分模块开发计划

## 1. 开发原则

1. 从 0 到 1 开发，不在旧项目上修补。
2. 当前只有知识库数据源，项目还没有正式开始开发。
3. 先做知识库加载与审计，再做名字生成。
4. 先做后端规则引擎，再做前端页面。
5. 每个模块必须独立测试。
6. 每个开发阶段必须可回退。
7. 不允许一次性开发完整系统。
8. 不允许随机拼字。
9. 不允许直接让 AI 生成最终名字。
10. 所有名字必须由知识库和规则引擎筛选生成。
11. 所有诗词出处必须来自本地知识库，不能编造。
12. 八字、五格、生肖只作为传统文化参考，不能做绝对化承诺。
13. 不要一开始做复杂 UI、支付、会员、海报功能。
14. 第一阶段只追求名字质量稳定。

## 2. 项目阶段总览

本项目按 Step 1 至 Step 17 执行，并映射为 phase-0 至 phase-12。每个阶段必须具备：明确输入、明确输出、明确文件范围、明确测试文件、明确验收标准、明确回退点。

## 3. Phase 0：初始化项目结构

对应 Step 1。

### 目标

创建标准项目目录，形成后续模块化开发基础。

### 目录

```text
baby-name-system/
├── backend/
├── frontend/
├── knowledge_base/
├── docs/
├── scripts/
└── tests/
```

### 技术要求

1. 后端使用 Python + FastAPI。
2. 前端使用 Next.js / React。
3. 测试使用 pytest。

### 验收标准

1. 项目目录创建完成。
2. pytest 可运行。
3. 不开发名字生成。
4. 不开发前端页面。
5. 不改动原始知识库。

### 提交名

`phase-0-init`

## 4. Phase 1：迁移知识库、创建文档、开发 KnowledgeLoader

对应 Step 2、Step 3、Step 4。

### 目标

接入知识库，完成知识库加载和审计能力。

### 知识库目录

```text
knowledge_base/
├── compliance/
├── char_attribute/
├── pronunciation/
├── culture_origin/
├── popularity/
└── numerology/
```

### 当前知识库包含

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

### 创建文档

在 docs/ 下创建：

1. PRD.md
2. SPEC.md
3. DEV_PLAN.md
4. TEST_PLAN.md
5. DATA_SCHEMA.md
6. API_SCHEMA.md

### 模块文件

```text
backend/app/core/knowledge_loader.py
```

### 要求

1. 能加载所有知识库文件。
2. 能检查文件是否存在。
3. 能检查字段是否完整。
4. 能输出知识库审计报告。
5. 缺失字段不能导致系统崩溃，必须有 warning。

### 测试文件

```text
tests/test_knowledge_loader.py
```

### 提交名

`phase-1-knowledge-loader`

## 5. Phase 2：开发单字查询模块 CharService

对应 Step 5。

### 模块文件

```text
backend/app/services/char_service.py
```

### 输入

一个汉字。

### 输出

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

### 测试文件

```text
tests/test_char_service.py
```

### 提交名

`phase-2-char-service`

## 6. Phase 3：开发宝宝档案模块 BabyProfileService

对应 Step 6。

### 模块文件

```text
backend/app/services/baby_profile_service.py
```

### 输入

1. 姓氏
2. 性别
3. 出生时间
4. 出生地
5. 日历类型
6. 风格偏好
7. 禁用字
8. 喜欢字

### 输出

1. 标准化宝宝档案
2. 生肖
3. 八字
4. 五行分布
5. 建议补益五行
6. 方言检查需求
7. 取名偏好权重

### 测试文件

```text
tests/test_baby_profile_service.py
```

### 提交名

`phase-3-baby-profile`

## 7. Phase 4：开发八字与传统规则模块

对应 Step 7。

### 模块文件

```text
backend/app/engines/bazi_engine.py
backend/app/engines/zodiac_engine.py
backend/app/engines/wuge_engine.py
```

### 要求

1. 八字计算必须可解释。
2. 五行分析必须返回过程。
3. 生肖喜忌必须来自知识库。
4. 五格只做参考，不作为唯一标准。

### 测试文件

```text
tests/test_bazi_engine.py
tests/test_zodiac_engine.py
tests/test_wuge_engine.py
```

### 提交名

`phase-4-bazi-engine`

## 8. Phase 5：开发候选字池模块 CharPoolBuilder

对应 Step 8。

### 模块文件

```text
backend/app/engines/char_pool_builder.py
```

### 候选字池分为

1. 合规字池
2. 五行补益字池
3. 文化出处字池
4. 风格偏好字池
5. 用户喜欢字池
6. 辈分字池
7. 备用字池

### 过滤规则

1. 禁用字过滤
2. 负面字过滤
3. 热名字过滤
4. 生僻字过滤
5. 谐音风险过滤

### 测试文件

```text
tests/test_char_pool_builder.py
```

### 提交名

`phase-5-char-pool`

## 9. Phase 6：开发文化出处召回模块 CultureRetriever

对应 Step 9。

### 模块文件

```text
backend/app/engines/culture_retriever.py
```

### 支持

1. 单字直接召回
2. 双字直接召回
3. 意象关联召回
4. 风格召回
5. 五行意象召回

### 返回字段

1. source
2. title
3. author
4. original_text
5. matched_chars
6. match_type
7. confidence
8. explanation

### 要求

1. 直接出处优先。
2. 意象关联必须明确标注。
3. 没有出处不能伪装有出处。
4. 置信度低于 0.6 不作为核心出处展示。

### 测试文件

```text
tests/test_culture_retriever.py
```

### 提交名

`phase-6-culture-retriever`

## 10. Phase 7：开发读音与谐音模块 PronunciationEngine

对应 Step 10。

### 模块文件

```text
backend/app/engines/pronunciation_engine.py
```

### 检查

1. 普通话拼音
2. 声调组合
3. 声母韵母搭配
4. 普通话谐音风险
5. 潮汕话读音
6. 潮汕话谐音风险
7. 姓名连读顺口度

### 测试文件

```text
tests/test_pronunciation_engine.py
```

### 提交名

`phase-7-pronunciation-engine`

## 11. Phase 8：开发名字组合模块 NameComposer

对应 Step 11。

### 模块文件

```text
backend/app/engines/name_composer.py
```

### 支持

1. 单字名
2. 双字名
3. 固定辈分字
4. 固定喜欢字
5. 锁定某个字继续生成
6. 排除某个字重新生成

### 组合限制

1. 两个名用字不能相同。
2. 不能高频重复同一批字。
3. 不能三连同声调。
4. 不能连续同声母导致拗口。
5. 不能爆款字堆叠。

### 测试文件

```text
tests/test_name_composer.py
```

### 提交名

`phase-8-name-composer`

## 12. Phase 9：开发评分模块 NameScorer

对应 Step 12。

### 模块文件

```text
backend/app/engines/name_scorer.py
```

### 评分维度

1. 合规安全：15
2. 普通话音律：15
3. 潮汕话读音：10
4. 字义寓意：15
5. 诗词典籍出处：15
6. 八字五行参考：10
7. 生肖喜忌参考：5
8. 重名热度控制：10
9. 性别与风格匹配：5

### 测试文件

```text
tests/test_name_scorer.py
```

### 提交名

`phase-9-name-scorer`

## 13. Phase 10：开发质量审查模块 QualityGuard

对应 Step 13。

### 模块文件

```text
backend/app/quality/quality_guard.py
```

### 检查

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

### 测试文件

```text
tests/test_quality_guard.py
```

### 提交名

`phase-10-quality-guard`

## 14. Phase 11：开发 API

对应 Step 14。

### 模块文件

```text
backend/app/api/name_routes.py
```

### 接口

1. POST /api/names/generate
2. GET /api/names/{request_id}/{name}
3. POST /api/names/regenerate
4. POST /api/favorites
5. GET /api/favorites

### 提交名

`phase-11-api`

## 15. Phase 12：开发前端 MVP

对应 Step 15。

### 只做 4 个页面

1. 宝宝信息填写页
2. 候选名字列表页
3. 名字详情页
4. 收藏对比页

### 设计原则

1. 简洁
2. 清晰
3. 卡片化
4. 每个名字一眼能看懂
5. 不堆砌玄学术语
6. 不做复杂营销包装

### 提交名

`phase-12-frontend-mvp`

## 16. Golden Cases

对应 Step 16。

### 文件

```text
tests/golden_cases.json
```

### 至少包含 10 个测试案例

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

## 17. 开发阶段提交

对应 Step 17。

### 每个阶段单独提交

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

## 18. 每阶段完成标准

1. 代码完成。
2. 单元测试完成。
3. pytest 通过。
4. 文档更新。
5. 输出修改文件清单。
6. 输出风险点。
7. 输出下一阶段建议。

## 19. 最终目标

用户输入宝宝信息后，系统稳定输出 20 个高质量候选名字。每个名字都必须有完整解释、普通话读音、潮汕话读音、文化出处、八字参考、热度风险和推荐理由。
