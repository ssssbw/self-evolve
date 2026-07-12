# Fixed Learning Companion Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将已确认的固定学习陪练规则固化到仓库，使任意 Codex 任务都能恢复每日学习闭环和每周复盘流程。

**Architecture:** `.ai/LEARNING-WORKFLOW.md` 是完整工作流的唯一来源；`.ai/CONTEXT.md` 和 `AGENTS.md` 只保存触发入口；`.ai/SESSION-LOG.md` 记录本次决策。当前周复盘继续承担每日学习状态的持久化，不新增每日 Journal。

**Tech Stack:** Markdown、Git、Codex App 本地项目任务

---

### Task 1: 创建学习工作流唯一来源

**Files:**
- Create: `.ai/LEARNING-WORKFLOW.md`

- [x] **Step 1: 创建工作流文件**

文件必须包含以下章节和规则：

```markdown
# 学习陪练工作流

> 本文件是每日学习闭环、作业批改、开放讨论和每周复盘的唯一现行规则。

## 使用入口

- 长期使用一个固定的 Codex 项目任务，建议命名为“学习陪练”。
- 每日触发语：`开始今日学习闭环`。
- 每周触发语：`开始本周复盘`。
- 手机、Windows 时钟或日历负责时间提醒，不创建每日或每周 Codex cron 自动任务。

## 每日学习闭环

### 时间边界

- 周一至周六在 22:30 前完成当天主要学习。
- 每天投入 60-90 分钟，阅读和作业都包含在该时间内。
- 不固定阅读与作业比例，根据内容和难度调整。
- 大型实验单独规划，不计入日常 60-90 分钟。
- 22:30-23:00 用于提交、批改、开放讨论和确定下一步。

### 提交内容

1. 实际投入时间。
2. 阅读或练习内容。
3. 自己的理解、笔记或作业答案。
4. 当前疑问或卡点。

### AI 处理流程

1. 读取当前周复盘、活跃项目、读书清单和相关作业。
2. 核对用户提交的信息，不推测未说明的完成情况。
3. 根据内容选择小作业、概念复述、现实案例、开放讨论或补充练习。
4. 从正确性、理解深度、应用能力和表达清晰度进行反馈。
5. 在 23:00 前收束讨论，生成下一天 60-90 分钟任务。
6. 生成一条简短学习记录，用户确认后写入当前周复盘。

### 输出与批改原则

- 不强制每天都有传统作业，只选择能验证理解的输出。
- 反馈必须指出具体证据、错误和改进方向，不使用空泛评价。
- 作业错误较多时，下一次优先纠错，减少新内容。
- 讨论超过 23:00 时，记录未解决问题，后续继续。

## 每周复盘

### 时间边界

- 每周日 20:30 开始，控制在 30-45 分钟。
- 周日不再执行每日 22:30 闭环。

### AI 处理流程

1. 读取当前周每日记录、P001、读书清单和本周 Git 变化。
2. 对缺失信息先询问用户，不根据文件变化推测掌握情况。
3. 复盘技术、理财、认知、职业资产、资产记录和健康执行。
4. 将结果区分为“已掌握”“接触过”“未执行”。
5. 汇总完成情况、关键收获、主要阻塞和未解决问题。
6. 保留 `2121` 节奏，只确定下周最重要的 1-3 件事。
7. 大型实验单独列入候选，不自动塞入普通学习时段。
8. 生成本周复盘和下一周计划草稿。
9. 用户确认后更新本周文件并创建下一周复盘文件。

## 状态与写入边界

- Markdown 仓库是事实来源，对话上下文不是长期状态来源。
- 每日记录写入当前周复盘，不创建每日 Journal 文件。
- 用户没有明确提供的信息保持空白。
- 个人完成情况、评分、资产和健康数据必须经用户确认。
- P001、读书清单和路线图仅在达到明确通关条件并再次确认后更新。
- 不自动执行 Git commit、Trilium 同步或长期路线调整。

## 中断处理

- 当天未学习：如实记录原因，只安排下一次最低恢复任务。
- 未在 22:30 提交：之后仍可继续，不生成虚假记录。
- 学习中断：不补历史欠账，从当前节奏恢复。
- 固定任务不可用：在项目下新建任务并使用相同触发语，从仓库恢复状态。
```

- [x] **Step 2: 验证工作流章节完整**

Run:

```powershell
rg -n '^## |^### ' .ai/LEARNING-WORKFLOW.md
```

Expected: 输出“使用入口、每日学习闭环、每周复盘、状态与写入边界、中断处理”等章节。

### Task 2: 添加稳定入口和路由规则

**Files:**
- Modify: `.ai/CONTEXT.md`
- Modify: `AGENTS.md`

- [x] **Step 1: 更新 `.ai/CONTEXT.md`**

在“互动偏好与工作方式”后新增：

```markdown

**9. 固定学习陪练工作流**
- 日常学习、作业批改、开放讨论和周复盘统一使用固定的“学习陪练”任务。
- 用户说“开始今日学习闭环”或“开始本周复盘”时，先完整读取 `.ai/LEARNING-WORKFLOW.md`。
- 当前周复盘文件是每日学习进度和跨任务恢复状态的事实来源。
- 时间提醒由外部日历、手机或 Windows 时钟负责，不使用每日或每周 Codex cron 自动任务。
```

- [x] **Step 2: 更新 `AGENTS.md`**

在“Agent-Specific Instructions”末尾新增：

```markdown

For learning coaching, homework review, open discussion, or weekly review requests, read `.ai/LEARNING-WORKFLOW.md` completely before responding. Treat that file as the single source of truth for the learning workflow.
```

- [x] **Step 3: 验证入口引用**

Run:

```powershell
rg -n 'LEARNING-WORKFLOW|开始今日学习闭环|开始本周复盘' AGENTS.md .ai/CONTEXT.md
```

Expected: 两个文件均引用 `.ai/LEARNING-WORKFLOW.md`，`CONTEXT` 包含两个触发语。

### Task 3: 记录本次会话决策

**Files:**
- Modify: `.ai/SESSION-LOG.md`

- [x] **Step 1: 追加会话 #005**

在文件末尾追加：

```markdown

---

## 会话 #005 — 固定学习陪练工作流（2026-07-12 ~ 2026-07-13）

**本次完成：**

1. **确定每日学习闭环**
   - 周一至周六每天学习 60-90 分钟，阅读和作业都包含在内。
   - 大型实验单独安排，不计入日常时段。
   - 22:30-23:00 提交学习结果、批改作业、开放讨论并确定下一步。
   - 不强制每天布置传统作业，根据内容选择小作业、复述、案例或讨论题。

2. **确定周复盘流程**
   - 每周日 20:30 开始，控制在 30-45 分钟。
   - 根据每日记录复盘六个维度，区分“已掌握”“接触过”“未执行”。
   - 先生成本周复盘和下周计划草稿，用户确认后再写入。

3. **调整 Codex 使用方式**
   - 不使用每日、每周 Codex cron 自动任务，避免持续创建独立任务。
   - 长期使用一个固定的“学习陪练”任务。
   - 时间提醒交给手机、Windows 时钟或日历。
   - 工作流固化在 `.ai/LEARNING-WORKFLOW.md`，仓库是跨任务恢复状态的事实来源。

**现行触发方式：**

- 每日：`开始今日学习闭环`
- 每周：`开始本周复盘`

**下一步：**

- 从 2026-W29 开始执行固定学习陪练工作流。
- 每日结果确认后写入当前周复盘。
- 周日确认复盘草稿后更新本周文件并创建下一周文件。

**下一个 AI 需要知道：**

- 学习工作流的唯一现行来源是 `.ai/LEARNING-WORKFLOW.md`。
- 不要重新创建每日或每周 Codex cron 自动任务，除非用户明确改变决定。
- 不得根据 Git 变化或计划文件推测用户已经学习或掌握。
```

- [x] **Step 2: 验证会话编号和日期**

Run:

```powershell
rg -n '^## 会话 #' .ai/SESSION-LOG.md
```

Expected: 会话编号从 `#001` 到 `#005`，最后一项日期为 `2026-07-12 ~ 2026-07-13`。

### Task 4: 完整验证与提交

**Files:**
- Verify: `.ai/LEARNING-WORKFLOW.md`
- Verify: `.ai/CONTEXT.md`
- Verify: `.ai/SESSION-LOG.md`
- Verify: `AGENTS.md`

- [x] **Step 1: 检查 Markdown 和链接**

Run:

```powershell
git diff --check
rg -n 'LEARNING-WORKFLOW.md' AGENTS.md .ai/CONTEXT.md .ai/SESSION-LOG.md
Test-Path .ai/LEARNING-WORKFLOW.md
```

Expected: `git diff --check` 无输出；三个入口文件均引用工作流；`Test-Path` 返回 `True`。

- [x] **Step 2: 检查改动范围**

Run:

```powershell
git status --short
git diff --stat
```

Expected: 只出现 `.ai/LEARNING-WORKFLOW.md`、`.ai/CONTEXT.md`、`.ai/SESSION-LOG.md`、`AGENTS.md` 和本实施计划文件。

- [x] **Step 3: 提交实现**

```powershell
git add -- .ai/LEARNING-WORKFLOW.md .ai/CONTEXT.md .ai/SESSION-LOG.md AGENTS.md docs/superpowers/plans/2026-07-13-learning-companion-workflow.md
git commit -m "docs: 固化学习陪练工作流"
```

Expected: 创建一个只包含学习工作流文档变更的提交。
