# Playground Numbering Unification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 Playground 的题目编号统一为各叶子目录独立连续编号，并修正相关引用。

**Architecture:** 仅调整 Markdown 文件名和少量文本引用，不改变目录层级与题目内容。优先用 Git 重命名保留历史，再修正文内编号、答案文件提示和入口文档引用。

**Tech Stack:** Markdown、Git、ripgrep、路径校验。

---

### Task 1: 重命名题目文件

**Files:**
- Modify: `5-Playground/P001-基础重建/CSAPP/homework/*`
- Modify: `5-Playground/P001-基础重建/CSAPP/discussions/*`
- Modify: `5-Playground/P001-基础重建/设计模式与架构/homework/*`
- Modify: `5-Playground/P001-基础重建/设计模式与架构/discussions/*`
- Modify: `5-Playground/P002-财务底盘与财富行为/01-金钱心理学/discussions/*`

- [x] 将各叶子目录内的题目文件按 `001` 开始连续重命名。
- [x] 保持题目标题文字不变，只调整编号前缀。

### Task 2: 修正文内引用

**Files:**
- Modify: `5-Playground/P001-基础重建/CSAPP/homework/*.md`
- Modify: `5-Playground/P001-基础重建/CSAPP/discussions/*.md`
- Modify: `5-Playground/P001-基础重建/设计模式与架构/homework/*.md`
- Modify: `5-Playground/P001-基础重建/设计模式与架构/discussions/*.md`
- Modify: `5-Playground/P002-财务底盘与财富行为/01-金钱心理学/discussions/*.md`

- [x] 更新题目标题中的编号。
- [x] 更新题目内部 `answer.md` 文件名提示，使其与新编号一致。

### Task 3: 修正入口文档

**Files:**
- Modify: `0-Projects/P001-基础重建/first-month-calendar.md`
- Modify: `docs/superpowers/plans/2026-07-15-project-scoped-playground.md`

- [x] 把旧日历中的全局编号改为“轨道名 + 轨道内编号”。
- [x] 更新计划文档中的路径与编号示例，避免留下失效路径。

### Task 4: 验证

**Files:**
- Verify: 上述所有文件

- [x] 运行 `find 5-Playground -type f | sort`，确认每个叶子目录内编号连续。
- [x] 运行 `rg` 复查旧编号和旧路径残留。
- [x] 运行 `git diff --check`，确认格式无误。
