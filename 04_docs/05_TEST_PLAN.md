# 05_TEST_PLAN.md｜易元命名测试计划

## 1. 测试目标

确保系统按模块稳定开发，避免修修补补导致项目失控。测试重点不是覆盖率数字，而是确保名字生成结果合规、可解释、可追溯、低重复、无明显风险。

## 2. 测试类型

1. 知识库加载测试。
2. 单字查询测试。
3. 宝宝档案测试。
4. 八字/生肖/五格测试。
5. 候选字池测试。
6. 文化出处召回测试。
7. 读音与谐音测试。
8. 名字组合测试。
9. 评分测试。
10. QualityGuard 测试。
11. API 集成测试。
12. 前端基础交互测试。

## 3. 测试文件规划

```text
tests/
├── golden_cases.json
├── test_knowledge_loader.py
├── test_char_service.py
├── test_baby_profile_service.py
├── test_bazi_engine.py
├── test_zodiac_engine.py
├── test_wuge_engine.py
├── test_char_pool_builder.py
├── test_culture_retriever.py
├── test_pronunciation_engine.py
├── test_name_composer.py
├── test_name_scorer.py
├── test_quality_guard.py
└── test_name_api.py
```

## 4. Golden Cases

至少 10 个案例：

1. 男宝双字名。
2. 女宝双字名。
3. 潮汕地区宝宝。
4. 带辈分字。
5. 禁用爆款字。
6. 喜欢固定字。
7. 单字名。
8. 复姓。
9. 出生时间缺失。
10. 出生地缺失。

## 5. 模块验收标准

### 5.1 KnowledgeLoader

1. 所有知识库文件可读取。
2. 缺失字段有 warning。
3. 审计报告可生成。
4. 不改写原始知识库。

### 5.2 CharService

输入一个汉字，必须返回合规、拼音、潮汕话读音、康熙笔画、五行、字义、古义、热度、出处与风险。

### 5.3 CultureRetriever

1. 直接出处必须来自 content。
2. name_candidates 必须来自本地 JSON。
3. 意象关联必须标注。
4. 无出处不得伪造。
5. confidence 低于 0.6 不展示为核心出处。

### 5.4 PronunciationEngine

1. 能返回普通话拼音与声调。
2. 能返回潮汕话读音。
3. 能识别谐音黑名单。
4. 能给出顺口度评分。

### 5.5 NameComposer

1. 能生成单字名和双字名。
2. 不重复。
3. 不三连同声调。
4. 不爆款字堆叠。
5. 支持辈分字、喜欢字、禁用字。

### 5.6 NameScorer

1. 输出 9 个维度分项分数。
2. 总分等于分项和。
3. 扣分原因明确。

### 5.7 QualityGuard

必须拦截：重复名、重复字过多、出处不相关、解释空泛、谐音风险、潮汕话风险、爆款堆叠、性别风格不匹配、命理表述过度。

## 6. 最终验收

输入宝宝信息后，系统必须稳定输出 20 个高质量候选名字。每个名字必须包含完整解释、普通话读音、潮汕话读音、文化出处、八字参考、热度风险和推荐理由。

## 7. 回归测试

每次修改必须运行：

```bash
pytest
```

如果测试失败，不允许进入下一阶段。
