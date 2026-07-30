# 作业 002 — Python 聊天记录数据建模与脱敏

> 所属项目：P004 第二份工作准备  
> 所属层级：L1 工程基础底座  
> 练习类型：Python coding 能力验收 / 公司 AI 项目牵引  
> 作业说明位置：`self-evolve/5-Playground/P004-第二份工作准备/L1-工程基础底座/homework/`  
> 代码实现位置：`/Users/xw.zhu/customer-feedback-analytics`  
> 状态：⬜ 未开始

## 目标

用公司用户反馈评估系统作为练习场，验证 Python 基础 coding 能力是否能支撑聊天记录分析链路的第一步：会话 / 消息数据建模与敏感信息脱敏。

这不是完整业务实现，也不要求接入真实接口。重点是验证：

- 能用 Python 表达业务数据结构。
- 能把聊天记录拆成会话、消息、分析任务等对象。
- 能处理手机号、邮箱、订单号等敏感信息。
- 能写基础测试验证边界情况。
- 能说明这段能力后续如何接入 FastAPI、PostgreSQL 和 LLM 分析链路。

## 合规边界

- 不使用公司真实聊天记录。
- 不记录客户、客服、销售或内部人员个人信息。
- 不记录公司接口地址、账号、密钥、内部字段全量结构或私有 Prompt。
- 只使用人工构造样例和脱敏字段名。
- 本作业复盘只记录通用代码结构、测试结果和个人理解。

## 背景

用户反馈评估系统需要把用户与客服聊天记录整理为可分析的结构化输入。LLM 分析前必须先完成：

1. 会话和消息建模。
2. 角色归一化。
3. 基础脱敏。
4. 构造可传给后续分析模块的安全输入。

## 任务

在 `/Users/xw.zhu/customer-feedback-analytics` 中手写 Python 代码，完成一个最小聊天记录数据建模与脱敏模块。

建议文件位置由你自己根据项目结构决定。可以参考：

```text
src/
  feedback_analytics/
    models.py
    sanitizer.py
tests/
  test_sanitizer.py
```

必须实现：

1. 定义 `ChatMessage` 数据结构。
2. 定义 `ChatSession` 数据结构。
3. 定义一个脱敏函数，处理人工构造消息中的手机号、邮箱和订单号。
4. 定义一个函数，将 `ChatSession` 转换为 LLM 分析前的安全输入文本。
5. 至少写 4 个测试。

## 建议数据结构

可以使用 `dataclass` 或 Pydantic。当前 L1 阶段优先建议先用 `dataclass`，后续再迁移到 Pydantic / FastAPI。

字段建议：

```text
ChatMessage
- message_id
- role
- content
- created_at

ChatSession
- session_id
- messages
- source
```

角色建议先归一化为：

```text
user
support
system
unknown
```

## 脱敏规则

至少处理：

- 手机号：替换为 `[PHONE]`
- 邮箱：替换为 `[EMAIL]`
- 订单号：替换为 `[ORDER_ID]`

订单号可以先使用人工约定规则，例如：

```text
ORD-20260729-001
```

不要把公司真实订单号格式写入本作业。

## 测试要求

至少 4 个测试：

1. 普通消息不包含敏感信息时，内容保持不变。
2. 包含手机号时能替换为 `[PHONE]`。
3. 包含邮箱和订单号时都能替换。
4. `ChatSession` 能转换为安全输入文本，并保留角色和消息顺序。

如果使用 pytest，测试命名建议：

```text
test_sanitize_plain_text
test_sanitize_phone_number
test_sanitize_email_and_order_id
test_build_safe_llm_input_keeps_role_and_order
```

## 手写要求

- 先自己写第一版代码。
- 可以查 Python 官方文档、正则表达式和 pytest 文档。
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
1. 我如何设计 ChatMessage / ChatSession：
2. 我如何设计脱敏规则：
3. 我处理了哪些边界情况：
4. 这段代码后续如何迁移到 FastAPI / PostgreSQL / LLM 分析链路：

我不确定的地方：
```

## 验收标准

| 掌握度 | 标准 |
| ------ | ---- |
| 20% | 能看懂题目，知道要做数据建模、字符串处理和测试 |
| 40% | 能跟着资料写出 dataclass 和基础脱敏函数 |
| 60% | 能独立完成会话 / 消息建模、脱敏和安全输入构造 |
| 80% | 能补齐测试和边界处理，并说明如何接入用户反馈评估系统 |
| 100% | 能讲清数据建模、隐私边界、测试覆盖和后续 FastAPI / PostgreSQL / LLM 集成取舍 |

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
- 可用于面试表达的点：
