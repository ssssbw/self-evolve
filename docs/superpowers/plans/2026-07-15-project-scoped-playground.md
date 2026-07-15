# 学习项目化 Playground 迁移计划

> **供执行代理使用：** 逐项执行并在每一步核对路径、链接与 Markdown 格式。

**目标：** 让练习、讨论和挑战按活跃项目及其书本或学习主题归档，并把题目类型规则固化到学习工作流。

**结构：** `0-Projects/` 维护 P001-P003 的目标与通关条件；`5-Playground/` 按项目建立目录，技术项目再按技术轨道拆分，理财和认知项目按阶段或书本拆分。

**技术栈：** Markdown、Git 路径重命名与仓库链接检查。

---

### 任务 1：建立项目边界

**文件：**
- 重命名：`0-Projects/P001-软件开发能力提升/` 至 `0-Projects/P001-基础重建/`
- 创建：`0-Projects/P002-财务底盘与财富行为/plan.md`
- 创建：`0-Projects/P003-学习与执行/plan.md`
- 修改：`0-Projects/_index.md`

- [x] 将 P001 更名为“基础重建”，保留 CSAPP 与设计模式/架构双轨内容。
- [x] 为 P002 写明先完成财务底盘，再进入《金钱心理学》财富行为阶段。
- [x] 为 P003 写明以《刻意练习》为首本主线，将方法用于当前技术学习。
- [x] 在活跃项目索引中登记三个项目，项目上限为三个。

### 任务 2：按项目迁移既有题目

**文件：**
- 移动：`5-Playground/homework/001、003、005、007` 至 `5-Playground/P001-基础重建/CSAPP/homework/`
- 移动：`5-Playground/discussions/001、002、004` 至 `5-Playground/P001-基础重建/CSAPP/discussions/`
- 移动：`5-Playground/homework/002、004、006、008` 至 `5-Playground/P001-基础重建/设计模式与架构/homework/`
- 移动：`5-Playground/discussions/003、005` 至 `5-Playground/P001-基础重建/设计模式与架构/discussions/`
- 创建：`5-Playground/README.md` 与各项目 README
- 修改：`0-Projects/P001-基础重建/first-month-calendar.md`

- [x] 保留全部文件名、题号与正文，使用 Git 移动保留历史。
- [x] 更新旧日历中的三个实际路径，保证历史链接仍可打开。
- [x] 删除迁移后为空的旧题型目录及其失效说明。

### 任务 3：建立书本级入口与当前讨论

**文件：**
- 创建：`5-Playground/P002-财务底盘与财富行为/00-财务底盘/README.md`
- 创建：`5-Playground/P002-财务底盘与财富行为/01-金钱心理学/README.md`
- 创建：`5-Playground/P002-财务底盘与财富行为/01-金钱心理学/discussions/006-不同经历能否导出相同的金钱原则.md`
- 创建：`5-Playground/P003-学习与执行/01-刻意练习/README.md`

- [x] 财务底盘按阶段归档，因为它没有单一主线书；书本内容按书名独立归档。
- [x] 为当前《金钱心理学》创建一题开放讨论，不附带买卖或财务数据要求。
- [x] 为认知的首本主线书创建入口，不提前创建未开始书本的题目。

### 任务 4：固化题目分流规则

**文件：**
- 修改：`.ai/LEARNING-WORKFLOW.md`

- [x] 技术学习优先指向教材或课程自带练习；AI 仅补充不重复的进阶作业。
- [x] 理财与认知的日常输出仅为开放讨论；挑战只用于连续多天的实践产出。
- [x] 新题必须按“项目 -> 技术轨道或阶段/书本 -> 题型”保存。
- [x] 将最多三个活跃项目写为学习工作流约束。

### 任务 5：验证

**文件：**
- 验证：上述所有移动与创建文件

- [x] 运行 `git diff --check`，确认无 Markdown 空白错误。
- [x] 运行 `find 5-Playground -type f -name '*.md' | sort`，确认所有题目均处于项目目录。
- [x] 运行 `rg -n '5-Playground/(homework|discussions|challenges)'`，确认旧日历链接已更新且不存在废弃路径。
- [x] 查看 `git diff --stat` 与 `git status --short`，确认只有本次结构调整和原有 W29 改动。
