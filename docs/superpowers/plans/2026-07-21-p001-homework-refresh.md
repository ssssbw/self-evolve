# P001 Homework Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 P001 当前的 CSAPP 与设计模式题目更新到真实学习进度，并同步本周周记录。

**Architecture:** 仅修改已有 `001` 题目与 `2026-W30.md`，不新增文件编号。CSAPP 题目改为覆盖第 1 章与 2.1，设计模式题目改为覆盖设计原则，周记录只更新周二当天计划项。

**Tech Stack:** Markdown、ripgrep、Git。

---

### Task 1: 更新 CSAPP 题目

**Files:**
- Modify: `5-Playground/P001-基础重建/CSAPP/homework/001-你写的代码计算机在做什么.md`
- Modify: `5-Playground/P001-基础重建/CSAPP/discussions/001-AI时代学底层还有意义吗.md`

- [x] 将作业改为覆盖第 1 章与 2.1 的进阶理解任务。
- [x] 将讨论改为围绕位模式、上下文和应用层工程判断展开。

### Task 2: 更新设计模式题目

**Files:**
- Modify: `5-Playground/P001-基础重建/设计模式与架构/homework/001-设计模式单例练习.md`
- Modify: `5-Playground/P001-基础重建/设计模式与架构/discussions/001-Flutter的Widget为什么是immutable的.md`

- [x] 将作业改为设计原则识别与应用。
- [x] 将讨论改为“原则先于模式”的开放讨论。

### Task 3: 更新本周记录

**Files:**
- Modify: `4-Journal/weekly/2026-W30.md`

- [x] 只更新周二记录行。
- [x] 不填写未发生的时长或结果。

### Task 4: 验证

**Files:**
- Verify: 上述 5 个文件

- [x] 运行 `rg` 复查题目主题是否已经切换到当前进度。
- [x] 运行 `git diff --check`，确认 Markdown 格式无误。
