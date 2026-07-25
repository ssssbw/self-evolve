# Challenge 001 — Self-Evolve 笔记结构化总结

## 目标

验证 L3 LLM 基础与模型接入：Prompt、Structured Output、JSON schema、超时重试和错误处理。

## 任务

选择 `self-evolve` 中的若干 Markdown 笔记，让大模型输出结构化总结结果。

输出字段至少包含：

- 笔记主题。
- 所属项目或领域。
- 核心结论。
- 行动项。
- 未解决问题。
- 可关联的 challenge。
- 置信度。
- 引用段落。

## 手写要求

- 自己设计 Prompt、schema、错误处理和测试样本。
- AI 可以解释 Structured Output 和 review schema，不能直接生成最终 Prompt 和完整代码照抄。

## 验收

- 输出必须是可解析 JSON。
- 至少准备 10 篇 Markdown 笔记作为样本。
- 记录成功、失败和误判案例。
- 能解释为什么使用 Structured Output，而不是只在 Prompt 中要求“返回 JSON”。
- 能说明这个能力后续如何接入 RAG 和学习计划助手。

## 复盘

- 查阅资料：
- 自己的设计：
- 手写实现：
- 运行 / 测试证据：
- AI 参与了什么：
- 遇到的问题：
- 采用的方案：
- 结果证据：
- 可写进简历的表达：
