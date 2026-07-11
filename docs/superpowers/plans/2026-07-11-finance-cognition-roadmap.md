# 理财与认知学习路线重构实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将理财与认知路线改造成无固定期限、按知识依赖推进、以实践产出和通关条件验收的长期学习系统，并清理会误导当前执行的过时文档。

**Architecture:** 两份领域 roadmap 是现行路线的唯一权威来源；资源计划只保留历史状态并链接回 roadmap；索引和上下文只描述当前事实；历史日志与已发生的复盘不回写。所有修改均为 Markdown 内容变更，通过关键词扫描、路径检查和 `git diff --check` 验证一致性。

**Tech Stack:** Markdown、PARA 知识库、Git、`rg`

---

### Task 1: 重写理财学习路线

**Files:**
- Modify: `1-Areas/A2-理财/roadmap.md`

- [ ] **Step 1: 建立无期限执行规则**

将学习原则改为：每周安排一次理财学习、同时只推进一本主线书、继续上次进度、不设置页数和完成日期、实践产出优先于读完。

- [ ] **Step 2: 按依赖顺序重建阶段**

使用以下固定顺序：财务底盘、财富行为、长期投资、经济金融基础、基础财报、投资决策、主动研究分支、宏观选修。每阶段必须包含“学习目标、顺序资源、必做实践、通关条件”。

- [ ] **Step 3: 明确主线与选修边界**

把《置身事内》移出理财路线；把《纳瓦尔宝典》降为选读；长期配置者完成个人投资政策后可停止扩展，主动研究个股时才进入财报估值分支。

- [ ] **Step 4: 删除冲突排期**

删除“四层学习计划”和“前 12 周学习计划”，保留简洁笔记模板与资产实践要求。

- [ ] **Step 5: 验证理财路线**

Run: `rg -n "前 12 周|W[0-9]+|置身事内|一周一本" '1-Areas/A2-理财/roadmap.md'`

Expected: 不出现周次和《置身事内》；“一周一本”只允许出现在否定性说明中，否则无输出。

### Task 2: 重写认知学习路线

**Files:**
- Modify: `1-Areas/A3-认知/roadmap.md`

- [ ] **Step 1: 建立无期限执行规则**

将学习原则改为：每周安排一次认知学习、同时只推进一本主线书、每次记录现实案例、按通关条件推进而不是按日期推进。

- [ ] **Step 2: 按依赖顺序重建阶段**

使用以下固定顺序：学习与执行、逻辑与批判思维、数据判断、心理与偏差、决策与不确定性、博弈与权力、制度与现实、历史与政治经济学。每阶段必须包含“学习目标、顺序资源、必做实践、通关条件”。

- [ ] **Step 3: 处理跨领域重复**

《置身事内》只在制度与现实阶段出现；所有财报、估值和投资工具书从认知路线移除；《穷查理宝典》和《纳瓦尔宝典》不在认知主线重复。

- [ ] **Step 4: 删除冲突排期**

删除“第一层/第二层/第三层”和“前 12 周学习计划”，保留认知笔记模板与现实案例要求。

- [ ] **Step 5: 验证认知路线**

Run: `rg -n "前 12 周|W[0-9]+|财务报表|一周一本" '1-Areas/A3-认知/roadmap.md'`

Expected: 不出现周次、财务报表书籍和强制的一周一本安排。

### Task 3: 统一资源索引和执行状态

**Files:**
- Modify: `2-Resources/100天读书计划.md`
- Modify: `2-Resources/reading-list.md`
- Modify: `1-Areas/_index.md`

- [ ] **Step 1: 将 100 天计划标为历史计划**

在标题下增加醒目说明：该计划创建于早期阶段，已停止执行；理财和认知以两份新版 roadmap 为准；保留正文仅用于回顾。

- [ ] **Step 2: 把 reading-list 改为当前状态追踪器**

保留已读《富爸爸穷爸爸》，为理财和认知各增加一行“当前主线：未选择”，并说明完整顺序不在此重复维护。

- [ ] **Step 3: 更新领域总览状态**

将 A1 改为 P001 进行中；将 A2、A3 改为路线已重构、按每周一次的节奏顺序推进。

- [ ] **Step 4: 验证唯一权威来源**

Run: `rg -n "等待启动第一个学习项目|100 天内读完|当前主线" '1-Areas/_index.md' '2-Resources/100天读书计划.md' '2-Resources/reading-list.md'`

Expected: 领域索引不再出现“等待启动”；100 天计划明确停止执行；阅读清单包含两条当前主线记录。

### Task 4: 标记历史执行材料并修正文档事实

**Files:**
- Modify: `0-Projects/P001-软件开发能力提升/first-month-calendar.md`
- Modify: `4-Journal/weekly/example-weekly-review.md`
- Modify: `1-Areas/A1-技术/roadmap.md`
- Modify: `.ai/CONTEXT.md`
- Modify: `1-Areas/A2-理财/practice/理财实操模板.md`

- [ ] **Step 1: 标记首月日历为旧基线**

在标题下说明日期已结束，原计划保留用于比较，当前执行以 P001 计划、阶段作战表和最新周复盘为准。

- [ ] **Step 2: 标记早期周复盘示例**

说明示例中的书籍和启动安排仅反映 2026-W18，不是当前任务；新周复盘应复制 `_template.md`。

- [ ] **Step 3: 限定技术 roadmap 的执行优先级**

增加说明：路线图描述长期方向，当前节奏以活跃项目和最新周计划为准，避免每日 1.5-2 小时建议覆盖 `2121` 安排。

- [ ] **Step 4: 修正 AI 上下文**

把示例路径改为 `guideline/一五计划/第一个五年计划.md`；删除每个领域必有 `reflections/` 的陈述，改为实际存在的 roadmap 和主题子目录。

- [ ] **Step 5: 修正理财模板路径**

把复制目标改为 `1-Areas/A2-理财/practice/2026-MM.md`。

- [ ] **Step 6: 验证过时事实已消除**

Run: `rg -n "guideline/第一五年|包含 roadmap.md、子分类与 reflections|复制到 .*A2-理财" .ai/CONTEXT.md '1-Areas/A2-理财/practice/理财实操模板.md'`

Expected: 无输出。

### Task 5: 更新交接记忆并完成全库验证

**Files:**
- Modify: `.ai/SESSION-LOG.md`
- Modify: `.serena/memories/project_decisions/2026-07-11-live-open-loops.md`

- [ ] **Step 1: 追加本次会话记录**

在 SESSION-LOG 末尾追加新会话：记录两条路线取消时间限制、采用阶段闸门、旧 100 天计划停止执行、历史文件只加标识不删除。

- [ ] **Step 2: 更新稳定项目决策记忆**

在 live open loops 中记录当前理财和认知学习规则：每周各一次、每个领域同时一本主线、无固定完成时间、以实践通关。

- [ ] **Step 3: 执行全库关键词检查**

Run: `rg -n "前 12 周学习计划|等待启动第一个学习项目|guideline/第一五年|包含 roadmap.md、子分类与 reflections" --glob '*.md' --glob '!docs/superpowers/**' --glob '!.ai/SESSION-LOG.md'`

Expected: 无输出；历史会话日志被明确排除。

- [ ] **Step 4: 执行格式和范围检查**

Run: `git diff --check`

Expected: 无输出。

Run: `git status --short`

Expected: 仅列出本计划中的 Markdown 文件，以及属于另一任务且未暂存的脚本/测试变更。

- [ ] **Step 5: 提交本任务文件**

只暂存本计划列出的 Markdown 文件，明确排除 `scripts/`、`tests/` 和同步脚本相关文件。

Run: `git diff --cached --name-only`

Expected: 仅出现本计划列出的 Markdown 文件。

Commit: `docs: 重构理财认知学习路线`
