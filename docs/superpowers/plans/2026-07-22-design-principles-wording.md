# Design Principles Wording Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 统一仓库中当前执行面与路线图里对 `SOLID` 和 `DRY / KISS / YAGNI` 的表述口径。

**Architecture:** 仅修改三份 Markdown 文案：项目计划、当前作业和长期路线图。保持学习路径与内容结构不变，只修正概念层级和说明文字。

**Tech Stack:** Markdown、ripgrep、Git。

---

### Task 1: 修正 P001 计划

**Files:**
- Modify: `0-Projects/P001-基础重建/plan.md`

- [x] 将 B1 阶段表述改为 `SOLID + DRY / KISS / YAGNI` 的分层说明。

### Task 2: 修正当前设计原则作业

**Files:**
- Modify: `5-Playground/P001-基础重建/设计模式与架构/homework/001-设计模式单例练习.md`

- [x] 将前置阅读和题目要求中的原则集合改成分层表述。

### Task 3: 修正 A1 技术路线图

**Files:**
- Modify: `1-Areas/A1-技术/roadmap.md`

- [x] 将软件设计基础中的 WHAT & WHY 改成更严谨的原则分层表述。

### Task 4: 验证

**Files:**
- Verify: 上述三份文件

- [x] 运行 `rg` 复查旧表述残留。
- [x] 运行 `git diff --check`，确认 Markdown 格式无误。
