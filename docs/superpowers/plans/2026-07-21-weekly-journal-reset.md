# Weekly Journal Reset Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 重置 `4-Journal/weekly/`，从 `2026-W30` 开始使用新的周模板并清理旧周文件。

**Architecture:** 直接改写周模板，新增本周周复盘文件，并删除不再保留的旧周文件。保持其它目录不动，只校验目录结果和 Markdown 格式。

**Tech Stack:** Markdown、Git、ripgrep。

---

### Task 1: 改写周模板

**Files:**
- Modify: `4-Journal/weekly/_template.md`

- [x] 按当前学习工作流重写模板结构。
- [x] 加入每日记录区与周日复盘区。

### Task 2: 创建本周周复盘

**Files:**
- Create: `4-Journal/weekly/2026-W30.md`

- [x] 以新模板为基线创建本周文件。
- [x] 只预填真实日期和活跃项目，不伪造完成记录。

### Task 3: 清理旧文件

**Files:**
- Delete: `4-Journal/weekly/2026-W28.md`
- Delete: `4-Journal/weekly/2026-W29.md`
- Delete: `4-Journal/weekly/example-weekly-review.md`

- [x] 删除用户明确要求清理的旧周文件和示例文件。

### Task 4: 验证

**Files:**
- Verify: `4-Journal/weekly/`

- [x] 运行 `find 4-Journal/weekly -maxdepth 1 -type f | sort`，确认最终只保留两个文件。
- [x] 运行 `git diff --check`，确认 Markdown 格式无误。
