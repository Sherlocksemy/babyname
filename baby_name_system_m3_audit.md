# 易元命名 Pro｜Milestone 3 源码审计报告

审计对象：`baby-name-system-m3.7z`  
审计方式：实际解压、源码检查、关键流程复现、前端重新安装与构建。  
审计日期：2026-06-23

---

## 一、结论

| 层级 | 结论 |
|---|---|
| 本地工程演示 | 通过 |
| API / SQLite / 前端链路 | 基本通过 |
| 核心命名结果可信度 | 不通过 |
| 付费产品发布 | 不通过 |
| 公开部署与安全 | 不通过 |

当前项目已经是一个可以运行的技术 MVP，但还不是一个可以对外收费、承诺“文化出处、潮汕读音、个性化命名”的产品 MVP。

阻塞发布的根因不是页面数量不足，而是以下四项：

1. API 层重新筛选候选，覆盖了 RankingEngine 的真实 Top3。
2. 组合名的文化出处展示存在误导，只显示第一个字的出处，却包装成整个名字的出处。
3. 8105 字知识库并未真正驱动生成，生产语义核心仍是约百字的硬编码小字典。
4. 分数、自然度、潮汕风险、重名风险等字段的产品含义明显大于实际算法能力。

---

## 二、已独立复现的事实

### 2.1 直接运行命名引擎

固定案例：林姓、男、汕头、公历 2025-03-01 08:30、书卷清雅＋君子品格。

直接调用 Orchestrator 得到的 Top3：

1. 林思敬
2. 林承仁
3. 林谦正

### 2.2 通过 API 运行相同案例

API 返回 Top3：

1. 林思敬
2. 林思弘
3. 林敬谦

这证明 API 层没有忠实使用 RankingEngine 已选出的 Top3。

### 2.3 换一批

独立复现结果：

- 第二批只返回 Top3＋5 个备选，仍标记完成。
- 再连续换批后，出现 Top3＋4、Top3＋0。
- 最终一次返回 HTTP 409 后，Session 状态残留为 `RUNNING`。

### 2.4 前端

删除压缩包内 Windows 版 `node_modules`，执行干净安装后：

- `npm run lint`：通过
- `npm run test`：通过，4 tests
- `npm run build`：通过

压缩包自带的 `node_modules` 在 Linux 环境执行失败，说明归档包含平台相关产物，不应随源码交付。

### 2.5 依赖安全

重新执行 `npm audit`：

- 2 个 moderate 漏洞
- 主要涉及 Next.js 间接依赖 PostCSS

本地演示可暂缓，公开部署前必须处理。

### 2.6 后端全量测试

在本审计环境中，两次尝试完整运行后端测试，分别在 5 分钟和 10 分钟超时，未能独立复现“105 passed”。

因此：

- 用户提交的 105 passed 记录可以保留；
- 本报告不声称已独立复现全部后端测试；
- 关键 API、生成、换批和前端流程已独立执行。

---

## 三、P0 阻塞问题

### P0-1：API 覆盖 RankingEngine 的 Top3

文件：

`02_src/backend/app/services/naming_application_service.py`

关键位置：

- 135–149 行：执行 Orchestrator 后，再调用 `_select_visible_candidates`。
- 159–176 行：从 `top20` 或 `top10` 顺序扫描，重新取前 10 个，再切成前 3 和后 7。

问题：

```python
for item in result.get("top20") or result.get("top10") or []:
    ...
return selected[:3], selected[3:10]
```

这一步绕开了 RankingEngine 已经完成的：

- Top3 多样性选择；
- 路径配额；
- Structure / Archetype 差异；
- Tie Break；
- 个性化排序。

影响：

- API 页面显示结果与核心引擎结果不一致；
- 所有前面 Milestone 1.1–1.3 建立的 Top3 规则可能在应用层失效；
- 测试通过也不能证明最终用户看到的是正确排序。

修复：

- 首批结果直接使用 `result["top3"]` 与 `result["backup7"]`。
- 换一批时，将排除集传入 RankingEngine，由 RankingEngine 重新选择，而不是应用层扫描 `top20`。
- 新增测试：API Top3 必须与 RankingEngine Top3 一致。

---

### P0-2：换一批数量和事务状态错误

文件：

`02_src/backend/app/services/naming_application_service.py`

关键位置：

- 42–65 行：`regenerate` 没有异常状态回写。
- 146–149 行：只检查 `len(top3) == 3`，不检查是否有 7 个备选。

问题：

- Top3 满 3 个、Backup 只有 0–6 个，也会返回 COMPLETED。
- `_execute_run` 失败后 Session 可能停留在 RUNNING。
- 已创建的 run 缺少失败状态和回滚语义。

独立复现：

- 第二批：3＋5，仍 COMPLETED。
- 后续：3＋4、3＋0。
- 409 后 Session 保持 RUNNING。

修复：

- 明确接口契约：必须 3＋7，或返回 `INSUFFICIENT_QUALIFIED_CANDIDATES` 并附实际数量。
- `regenerate` 增加与 `generate` 同等级的 try/except。
- Session 和 Run 同时记录 FAILED。
- 保存候选、完成 Run、更新 Session 使用一个事务。

---

### P0-3：组合名文化出处展示失真

文件：

- `02_src/backend/app/engines/name_composer.py`
- `02_src/backend/app/engines/culture_retriever.py`
- `02_src/backend/app/services/candidate_detail_service.py`

关键位置：

- NameComposer：分别查首字、次字出处后组合。
- CultureRetriever 68–88 行：单字出处直接标为 E2。
- CandidateDetailService 17 行、49 行：只取 `evidences[0]`。
- CandidateDetailService 84–93 行：将第一条证据作为整个名字的文化来源展示。

例子：`林思敬`

实际证据：

- “思”来自《诗经·关雎》中的“寤寐思服”；
- “敬”来自《诗经·沔水》中的“我友敬矣”。

但 API 卡片只展示第一条，容易让用户理解成“思敬”整体出自《关雎》。这是文化出处的事实性误导。

修复：

- Direct Expression：可以展示一个完整双字出处。
- Composed Name：必须分别展示“首字出处”和“次字出处”。
- 页面文案明确标注“组合推导”，不得写成“姓名出自某篇”。
- 不得把两条单字证据合并为一个双字经典出处。

---

### P0-4：知识库没有真正驱动命名语义

文件：

- `02_src/backend/app/engines/char_pool_builder.py`
- `02_src/backend/app/engines/semantic_composition_validator.py`

事实：

- 知识库有 8105 个规范字、字义、拼音、康熙笔画。
- 但 CharPoolBuilder 使用硬编码 `NAME_FRIENDLY_CHARS`，约 113 字。
- SemanticCompositionValidator 使用硬编码 `CHAR_INFO`，约 96 字。
- 不在小字典中的字通常无法进入有效组合。

影响：

- 生成引擎实际不是从 8105 字知识库中进行规则筛选；
- 它主要是在约百字范围内反复组合；
- “仁、贤、承、谦、敬、信、德”等字频繁出现，是结构性必然；
- 项目宣称的 Knowledge First 目前只完成了“加载数据”，没有完成“以数据替代硬编码”。

修复：

建立可审计的派生命名语义库：

```text
8105规范字
→ 字义清洗
→ 词性/语义标签
→ 可命名性
→ 性别气质
→ 年龄稳定性
→ 结构位置适配
→ 风险等级
→ 人工审核状态
```

生产代码只能读取该 Catalog，不再维护 96 字的代码常量。

---

## 四、P1 重大质量问题

### P1-1：组合义模板化，未真正验证语义

文件：`semantic_composition_validator.py`

组合义基本采用：

```text
A取某意，B取某意，组合为A与B相成
```

这不是词义、语法或姓名自然度验证，只是把两个正面标签拼成一句解释。

同时，类别矩阵中存在逻辑冲突，同一类别对既可能被判为互补，也可能被判为弱关系或强行解释。

修复：

- 引入固定词语/典故词典；
- 引入真实姓名语料；
- 区分：词语义、典故义、组合推导义；
- 无法形成自然组合义时直接淘汰，不生成套话解释。

---

### P1-2：Naturalness 与 NES 分数虚高且循环

文件：

- `naturalness_guard.py`
- `candidate_quality_scorer.py`

问题：

- Naturalness 以高基础分起步，再做少量扣分，容易普遍超过 90。
- Structure 和 Archetype 先由系统选中，评分时又因“匹配已选中的 Structure/Archetype”获得高分，存在循环自证。
- Profile adjustment 最高可额外加 12 分。
- 结果中的 94.9、92.08 看起来像精密测量，实际上是启发式公式。

修复：

- 在完成人工标注校准前，前端改成等级或区间，不展示两位小数的“权威分”。
- 建立人工评分集：至少 500 个正负样本，由多人评分。
- 使用排序一致率、Top-K 命中率、专家一致性进行校准。
- 分数用于排序，不用于制造“科学精确”的印象。

---

### P1-3：普通话音律和姓氏适配算法不可靠

文件：`surname_fit_evaluator.py`

关键问题：

- 只硬编码 5 个姓氏：林、陈、黄、郑、欧阳。
- 未知姓氏音调为 0。
- 拼音声母只取首字母，韵母只取最后两个字符。
- `zh/ch/sh`、`iang/uang/ong` 等全部不能正确解析。
- 欧阳被记录为一个音调，不符合复姓两音节实际情况。
- `SURNAME_CHAR_AFFINITY` 直接为特定姓氏与特定字加分，容易产生新的人工偏置。

修复：

- 使用真实拼音音节解析器；
- 单独建姓氏拼音与康熙笔画数据；
- 复姓按多音节处理；
- 姓氏适配只评价音律、字形和语义冲突，不使用主观“某姓偏爱某字”的硬编码加分。

---

### P1-4：潮汕话能力未达到产品宣称

当前实现主要是：

- 单字潮汕读音查询；
- 单字风险表查询。

尚未实现：

- 全名连读；
- 变调；
- 汕头/潮州/揭阳口音差异的完整组合；
- 姓名级谐音；
- 负面短语匹配。

此外，`CandidateDetailService._risk_level` 将任何 QualityGuard warning 都映射为 `NOTICE`，因此页面中的“潮汕话风险 NOTICE”可能只是 E2_COMPOSED 等普通警告，不是潮汕话风险。

修复：

- 将 `teochew_risk` 与通用 `quality_warning` 完全分离；
- 没有姓名级方言判断时显示“单字读音已覆盖，连读风险未评估”；
- 不得用 NOTICE 暗示已完成潮汕话分析。

---

### P1-5：“重名风险”名不副实

现有数据：

- 字频 180 条；
- 热门名字黑名单 500 条。

这不足以计算：

- 全国重名人数；
- 全国重名率；
- 同年龄段热度。

当前 UI 将 `uniqueness` 展示为“重名风险”，容易让用户误解为有全国重名数据支撑。

修复：

在补齐真实数据前，统一改名为：

```text
热门字 / 模板名风险
```

不得展示“预计重名人数”或“全国重名率”。

---

### P1-6：命理分多数是基础保底分

文件：

- `five_elements_engine.py`
- `fortune_fusion_engine.py`

现状：

- 五行支持方向主要取权重最低的两个元素，本质接近“缺什么补什么”的启发式。
- 没命中也有五行、生肖、五格基础分。
- 五格没有81数理解读，却仍因“数值可计算”获得一部分分值。

影响：

- Fortune Score 不是严格意义上的个体适配；
- 分数可能轻度改变排序，却没有足够理论和数据解释力。

修复：

- 将 Fortune 标注为 Foundation / Heuristic。
- 没有可靠适配依据的模块不计分，只显示计算结果。
- 五格只有数值、没有解释时不得贡献“吉利适配分”。

---

### P1-7：索引和知识库重复加载

文件：

- `app/api/main.py`
- `naming_alpha_orchestrator.py`
- `culture_retriever.py`
- `char_pool_builder.py`
- `quality_guard.py`

API lifespan 已构建索引，但 Orchestrator 内部的各组件仍各自创建新索引并重新加载知识库。

影响：

- 启动耗时和内存浪费；
- “只初始化一次”的测试结论并不完整；
- 后续并发时成本更高。

修复：

统一依赖注入：

```text
lifespan 构建一次 KnowledgeContext
→ 注入 Orchestrator
→ 注入全部 Engine
```

所有 Engine 禁止自行 new KnowledgeLoader。

---

## 五、P2 工程与产品问题

### P2-1：CORS 本地地址不一致

`.env.example` 允许：

```text
http://localhost:3000
```

实际用户访问：

```text
http://127.0.0.1:3000
```

独立预检结果：

- localhost：允许
- 127.0.0.1：返回 400 Disallowed CORS origin

修复：开发环境明确允许两个地址，或者启动脚本统一只输出 localhost。

---

### P2-2：SQLite 外键没有显式启用

虽然模型声明了 ForeignKey，但 SQLite 默认关闭外键约束。当前代码没有执行：

```sql
PRAGMA foreign_keys=ON;
```

影响：可能产生孤立 run、candidate、favorite。

修复：引擎连接事件中开启外键；增加级联和孤儿数据测试。

---

### P2-3：没有数据库迁移

目前主要依赖 `create_all`。

本地演示可以接受，进入持续迭代后必须引入 Alembic 或明确版本迁移机制。

---

### P2-4：旧版随机/笛卡尔积生成器仍可执行

文件：

- `02_src/main.py`
- `02_src/name_generator.py`

旧入口仍然存在，并使用与当前 Structure First 不一致的旧逻辑。开发人员若运行错误入口，可能重新得到最初那套低质量结果。

修复：

- 移至 `legacy/`；
- 禁止作为默认入口；
- 根 README 只保留新 FastAPI 与新 CLI 启动方式。

---

### P2-5：前端仍是技术演示界面

主要问题：

- 日期和时间使用原始数字输入，而非日期/时间选择器；
- 风格选项不足；
- 生成中页面并未绑定真实阶段；
- 结果页展示 S06、A02 等内部ID；
- 四柱、含义、发音、生肖、五格、NES 多处直接展示 JSON；
- 收藏缺少完整取消和状态同步；
- 换一批失败会让结果页整体切换成错误状态；
- 表单可访问性不足。

结论：功能可用，但还不是“高端命名顾问”的交付体验。

---

### P2-6：当前 E2E 不是浏览器级 E2E

项目中没有 Playwright、Cypress 等浏览器自动化依赖和脚本。

现有前端测试只有 4 项，报告中的 HTTP smoke 不能证明：

- 浏览器真实填写；
- 页面跳转；
- 收藏交互；
- 换一批交互；
- 移动端布局。

修复：增加 Playwright，覆盖一条完整用户旅程。

---

### P2-7：测试耗时过长，且遗漏关键断言

当前测试将大量矩阵生成、报告生成混在默认测试中，导致全量测试在本审计环境 10 分钟仍未完成。

缺失的关键测试：

- API Top3 等于 RankingEngine Top3；
- Backup 必须为 7 或明确不足；
- regenerate 失败后 Session/Run 为 FAILED；
- 组合名详情展示两条出处；
- 127.0.0.1 CORS；
- 潮汕风险与通用 warning 分离。

建议拆分：

```text
unit
integration
slow_matrix
browser_e2e
```

CI 默认跑 unit＋integration，矩阵和浏览器测试单独执行。

---

### P2-8：归档不干净

压缩包包含：

- `node_modules`，约 495MB；
- `__pycache__`；
- `.pyc`；
- `tsconfig.tsbuildinfo`。

结果：

- 压缩包 78MB；
- 解压后约 518MB；
- Windows 版 node_modules 在 Linux 中出现执行权限问题。

修复：归档只保留源码和 lockfile，使用 `npm ci` 重建依赖。

---

## 六、必须先修的发布门槛

### Gate A：结果正确性

1. API 不得覆盖 RankingEngine Top3。
2. 换一批必须事务化，并正确处理候选不足。
3. Composed Name 必须展示双证据，不得伪装成完整双字出处。
4. Top3、Backup7、详情页的数据定义一致。

### Gate B：命名引擎真实性

1. 去除生产代码中的小型硬编码语义字库。
2. 建立派生 Character Naming Catalog。
3. 建立真实短语/典故词典与姓名语料。
4. 分数通过人工样本校准前，不展示“94.90”式权威精度。
5. 潮汕、重名、命理三类结果按实际能力降级展示。

### Gate C：工程稳定性

1. 索引单例化与依赖注入。
2. CORS 修复。
3. SQLite 外键启用和迁移机制。
4. 清理旧版入口和归档产物。
5. 修复 npm moderate 漏洞。
6. 增加真实浏览器 E2E。

---

## 七、建议的修复顺序

### 第一批：P0 正确性修复

预计目标：保证用户看到的就是核心引擎真正选出的结果，并保证出处不误导。

### 第二批：命名知识层重构

预计目标：把“8105 字已加载”升级为“8105 字真正可被结构化筛选”，解决德行字循环组合。

### 第三批：前端产品化与发布安全

预计目标：让页面成为命名顾问产品，而不是 JSON 调试台，并达到可外部测试水平。

在以上三批完成前，不建议进入支付、会员、PDF和公开部署。

---

## 八、最终评级

| 项目 | 评级 |
|---|---|
| 知识库资产 | B+ |
| 文档体系 | A- |
| 后端模块化 | B |
| API/持久化 | B- |
| 前端工程可运行性 | B |
| 命名语义引擎 | C- |
| 文化出处可信展示 | D+ |
| 潮汕能力 | D+ |
| 重名风险能力 | D |
| 命理适配可信度 | C- |
| 付费产品成熟度 | D+ |
| 本地技术Demo | B+ |

**最终状态：技术 MVP 已完成；产品 MVP 未通过发布审计。**
