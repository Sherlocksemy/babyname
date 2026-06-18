# 02_SPEC.md｜易元命名系统技术规格说明

## 1. 技术目标

构建一个知识库驱动、规则引擎驱动、可测试、可回退的新生儿智能取名系统。系统必须避免随机拼字，所有候选名必须经过合规、字义、读音、文化出处、八字五行、生肖、热度与质量审查。

## 2. 推荐技术栈

后端：Python + FastAPI。

前端：Next.js / React。

测试：pytest。

数据：本地 CSV/JSON 知识库，MVP 可使用 SQLite 存储收藏、生成记录和请求历史。

## 3. 项目目录

```text
baby-name-system/
├── 00_raw_repos/
├── 01_knowledge_base/
├── 02_src/
├── 03_tools/
├── 04_docs/
├── backend/
├── frontend/
├── scripts/
└── tests/
```

说明：当前已有 `01_knowledge_base`、`02_src`、`03_tools`。正式开发可以在不破坏原目录的情况下新增 `backend/`、`frontend/`、`tests/`，也可逐步迁移 `02_src` 中已有能力。

## 4. 后端模块架构

```text
backend/app/
├── api/
│   └── name_routes.py
├── core/
│   ├── config.py
│   └── knowledge_loader.py
├── schemas/
│   ├── baby_profile.py
│   ├── name_candidate.py
│   └── response.py
├── services/
│   ├── char_service.py
│   └── baby_profile_service.py
├── engines/
│   ├── bazi_engine.py
│   ├── zodiac_engine.py
│   ├── wuge_engine.py
│   ├── char_pool_builder.py
│   ├── culture_retriever.py
│   ├── pronunciation_engine.py
│   ├── name_composer.py
│   └── name_scorer.py
└── quality/
    └── quality_guard.py
```

## 5. 数据流设计

用户输入 → BabyProfileService → BaziEngine/ZodiacEngine/WugeEngine → CharPoolBuilder → CultureRetriever → PronunciationEngine → NameComposer → NameScorer → QualityGuard → API Response。

所有模块输入输出必须结构化，禁止用自然语言字符串作为模块之间的主要数据接口。

## 6. KnowledgeLoader

职责：加载 `01_knowledge_base` 中所有 CSV/JSON 文件，完成字段校验、缺失检测和审计报告输出。

要求：

1. 支持懒加载和一次性加载。
2. 文件缺失输出 warning。
3. 字段缺失输出 warning。
4. 关键知识库无法读取时返回明确错误。
5. 不改写原始知识库。

输出：KnowledgeBundle，包含 compliance、char_attribute、pronunciation、culture_origin、popularity、numerology 六层数据。

## 7. CharService

职责：输入一个汉字，返回其完整属性。

输出字段：是否合规、普通话拼音、潮汕话读音、现代笔画、康熙笔画、部首、结构、五行、字义、古义、正向等级、常用等级、热度、相关出处、风险。

## 8. BabyProfileService

职责：将用户输入标准化为 BabyProfile，并生成取名上下文。

包括：姓氏校验、性别规范化、出生时间规范化、出生地规范化、风格偏好、禁用字、喜欢字、是否需要潮汕话检查。

## 9. BaziEngine / ZodiacEngine / WugeEngine

BaziEngine：根据出生时间计算八字与五行分布。算法必须可解释，不能由 AI 自由生成。

ZodiacEngine：根据年份识别生肖，基于 zodiac_taboo.csv 给出喜忌部首参考。

WugeEngine：基于康熙笔画计算天格、人格、地格、外格、总格，并查 wuge_rules.json。

统一约束：三者只作为传统文化参考，不作为绝对判断。

## 10. CharPoolBuilder

职责：构建候选字池。

输入：BabyProfile、BaziProfile、用户偏好、知识库。

输出：core_chars、culture_chars、style_chars、liked_chars、generation_chars、blocked_chars。

过滤顺序：合规 → 禁用字 → 负面字义 → 谐音风险 → 热名风险 → 五行/风格/文化召回 → 排序。

## 11. CultureRetriever

职责：从诗经、楚辞、唐诗、宋词、四书五经中召回出处。

支持：单字直接召回、双字直接召回、name_candidates 召回、keywords 意象召回、五行意象召回。

match_type：direct_char、direct_phrase、candidate_source、imagery_related、element_related。

置信度规则：低于 0.6 不作为核心出处展示。

## 12. PronunciationEngine

职责：普通话和潮汕话读音检查。

普通话检查：拼音、声调、声母、韵母、连读顺口度、谐音黑名单。

潮汕话检查：多 accent 读音、声调、是否口语/文读、不良谐音风险。

## 13. NameComposer

职责：组合姓名。

支持：单字名、双字名、辈分字固定、喜欢字固定、锁定字继续生成、排除字重新生成。

限制：两个名用字不能相同，不得三连同声调，不得连续同声母严重拗口，不得爆款字堆叠，不得同批字重复过高。

## 14. NameScorer

总分 100 分，维度：合规安全 15、普通话音律 15、潮汕话读音 10、字义寓意 15、诗词典籍出处 15、八字五行参考 10、生肖喜忌参考 5、重名热度控制 10、性别风格匹配 5。

NameScorer 必须返回分项分数与扣分原因。

## 15. QualityGuard

职责：最终质量审查。

检查：重复名、重复字过多、出处不相关、解释空泛、谐音风险、潮汕话风险、爆款字堆叠、性别气质不匹配、命理表述过度。

失败处理：返回失败原因，并通知生成流程重新生成或降级补位。

## 16. API 设计概览

1. POST /api/names/generate
2. GET /api/names/{request_id}/{name}
3. POST /api/names/regenerate
4. POST /api/favorites
5. GET /api/favorites

详细字段见 `06_API_SCHEMA.md`。

## 17. 前端 MVP

页面：宝宝信息填写页、候选名字列表页、名字详情页、收藏对比页。

设计原则：简洁、清晰、卡片化、不堆玄学术语、不做复杂营销包装。

## 18. 回退与版本控制

每个阶段单独提交；每次提交前必须运行 pytest；失败不得进入下一阶段。
