# 作业 001 — Python Markdown 元数据提取

> 所属项目：P004 第二份工作准备\
> 所属层级：L1 工程基础底座\
> 练习类型：Python coding 能力验收\
> 作业说明位置：`self-evolve/5-Playground/P004-第二份工作准备/L1-工程基础底座/homework/`\
> 代码实现位置：`self-evolve-ai-assistant`\
> 状态：⬜ 未开始

## 目标

验证 Python 基础 coding 能力是否能支撑 Self-Evolve AI 助手的第一步：从 Markdown 知识库中提取笔记元数据。

这不是设计模式练习，也不是完整项目实现。重点是验证：

- 函数拆分是否清晰。
- 数据结构是否合理。
- 字符串和文件处理是否可靠。
- 边界情况是否有处理。
- 是否能写基础测试。
- 是否能把小练习迁移到后续笔记元数据 API。

## 背景

Self-Evolve AI 助手后续需要读取 `self-evolve` 中的 Markdown 文件，建立笔记索引，再进一步支持搜索、RAG、学习状态读取和引用来源。

本作业只做最小闭环：输入 Markdown 内容或文件路径，输出结构化的 `NoteMetadata`。

## 任务

在 `self-evolve-ai-assistant` 中手写 Python 代码，完成一个 Markdown 元数据提取器。

建议文件位置由你自己决定，但需要能清楚说明模块职责。可以参考：

```text
src/
  note_parser/
    metadata.py
    markdown_parser.py
tests/
  test_markdown_parser.py
```

必须实现：

1. 输入一个 Markdown 字符串，提取元数据。
2. 输入一个 Markdown 文件路径，读取文件并提取元数据。
3. 提取标题：优先使用第一个 `# 标题`。
4. 提取一级标题和二级标题列表。
5. 统计字符数。
6. 返回结构化结果。
7. 至少写 3 个测试。

## 建议数据结构

可以使用 `dataclass`，也可以先用普通 `dict`。推荐先尝试 `dataclass`。

字段至少包含：

```text
path
title
headings
char_count
has_title
```

`headings` 至少要能区分一级标题和二级标题。

## 边界情况

至少考虑：

- 空 Markdown 内容。
- 没有 `# 标题` 的 Markdown。
- 只有二级标题，没有一级标题。
- 文件路径不存在。
- 文件内容不是 UTF-8 时如何处理，先写出你的处理策略即可。

## 测试要求

至少 3 个测试：

1. 正常 Markdown：包含标题、一级标题、二级标题。
2. 无标题 Markdown：能返回默认标题或空标题，并标记 `has_title = false`。
3. 空内容或不存在路径：能给出明确行为。

如果使用 pytest，测试命名建议：

```text
test_parse_normal_markdown
test_parse_markdown_without_title
test_parse_empty_content_or_missing_file
```

## 手写要求

- 先自己写第一版代码。
- 可以查 Python 官方文档、pytest 文档和已有项目结构。
- AI 只能用于解释、提示、debug 和 code review。
- 不让 AI 直接生成完整实现照抄。

## 提交格式

完成后把下面信息发给 AI review：

```text
实际投入：
代码位置：
运行命令：
测试结果：

核心代码：

我自己的理解：
1. 我如何拆分函数：
2. 我如何设计 NoteMetadata：
3. 我处理了哪些边界情况：
4. 这段代码后续如何迁移到笔记元数据 API：

我不确定的地方：
```

## 验收标准

| 掌握度  | 标准                                           |
| ---- | -------------------------------------------- |
| 20%  | 能看懂题目，知道要用字符串处理、文件读取和数据结构                    |
| 40%  | 能跟着资料写出基本函数，但边界处理和测试不完整                      |
| 60%  | 能独立完成字符串解析、文件读取和结构化返回                        |
| 80%  | 能补齐边界处理和 pytest，并说明代码如何迁移到 Self-Evolve AI 助手 |
| 100% | 能解释模块拆分、异常处理、测试覆盖和后续 API 集成取舍                |

## 复盘区

- 作答日期：
- 实际用时：
- 代码位置：
- 运行 / 测试证据：
- AI 参与了什么：
- 遇到的问题：
- 采用的方案：
- 最终掌握度：
- 可迁移到项目的点：

