# Challenge 001 — Self-Evolve 笔记元数据 API

## 目标

验证 L1 工程基础底座：Python、FastAPI、PostgreSQL、基础鉴权、CRUD、分页、Docker 和测试。

这是 Self-Evolve AI 助手的第一块积木，后续 L2-L5 都要继续复用和改造它。

## 任务

实现一个最小笔记元数据 API，用于管理 `self-evolve` Markdown 知识库中的笔记索引。先不做 AI，只做稳定的后端基础。

必须包含：

- 笔记记录创建、查询、分页、更新和状态标记。
- 字段至少包含：路径、标题、所属项目/领域、标签、摘要、最后更新时间、是否已索引。
- 基础鉴权，可以先使用简单 token。
- PostgreSQL 数据表。
- Docker Compose 启动服务和数据库。
- 至少 4 个测试：创建记录、分页查询、更新记录、状态标记。

## 手写要求

- 先查 FastAPI、Pydantic、PostgreSQL、pytest、Docker Compose 资料。
- 自己写数据模型、接口设计和第一版代码。
- AI 可以解释概念、检查报错和做 code review，不能直接生成完整实现照抄。

## 验收

- 能独立启动服务和数据库。
- 能通过 API 创建、查询、更新笔记元数据。
- 测试可重复运行。
- 能解释索引、分页、鉴权、Docker Compose 各自解决什么问题。
- 能说明这个 API 后续如何支撑 RAG：文档解析、chunk、embedding 和引用来源。

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
