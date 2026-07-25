# AI 全栈能力金字塔

> 用途：下一份工作的技术栈路线。  
> 所属项目：P004 下一份工作准备。  
> 定位：这不是 P001 的基础学习计划，而是 P004 的职业转型路线；P001 只提供其中一部分工程地基。

## 总结

下一份工作的目标不是继续把自己限制在 Flutter 工程师，而是转向 AI 应用工程师 / AI 全栈工程师。技术路线可以设计成一座能力金字塔，从底层工程基础到 AI 应用、生产工程化、系统设计和求职表达逐层点亮。

每一层不是“看过教程”就算完成，至少要同时满足：

1. 能解释核心原理。
2. 能独立编码实现。
3. 能集成进真实项目。
4. 能部署并解决问题。
5. 能在面试中讲清取舍。

最终技术定位：

> Python + Next.js 是主轴，AI 应用工程是核心，Go 是后端增强，Flutter 是跨端差异化，Vue 是兼容能力。

## 能力金字塔

```text
                         L7：求职与个人品牌
                         简历 / 作品 / 面试
                    L6：系统设计与差异化能力
                    Go / Flutter / 云原生 / 架构
               L5：AI 生产工程化
               评测 / 安全 / 监控 / 成本 / 稳定性
          L4：AI 应用核心
          RAG / Agent / Tool Calling / 多模态
     L3：LLM 基础与模型接入
     Transformer / Prompt / Embedding / 流式输出
L2：Web 全栈产品能力
FastAPI / Next.js / 鉴权 / 数据库 / 缓存 / 异步任务
L1：工程基础底座
Python / TypeScript / 网络 / SQL / Linux / Git / Docker / 测试
```

## L1：工程基础底座

目标：从 Flutter 客户端工程师升级为具备后端、数据库、部署和测试意识的工程师。

必须掌握：

- Python：类型、模块化、异常、`async/await`、依赖管理、pytest、基础工程规范。
- TypeScript：类型、接口、泛型、异步编程、React 基础、浏览器与 Node.js 差异。
- PostgreSQL：表设计、约束、JOIN、索引、事务、慢查询、ORM 与原生 SQL 边界。
- Web 基础：HTTP、REST、Cookie、Session、JWT、CORS、SSE、WebSocket、文件上传、流式响应。
- 工程工具：Git、Linux、Docker、Docker Compose、环境变量、日志、单元测试、API 集成测试。

点亮条件：

- 完成一个非 AI 后端服务：FastAPI + PostgreSQL + Redis + 登录鉴权 + CRUD + 分页搜索 + Docker Compose + 测试 + 部署。
- 能讲清索引、事务、JWT 与 Session、Redis、同步异步、SSE 与 WebSocket 的基本取舍。

## L2：Web 全栈产品能力

目标：具备从数据库、后端 API 到 Web UI 的完整产品交付能力。

必须掌握：

- FastAPI：路由、依赖注入、Pydantic、Middleware、异常处理、异步接口、文件上传、Background Task、OpenAPI、权限校验。
- Next.js：React、TypeScript、App Router、Server Component、Client Component、Route Handler、Server Action、SSR/CSR/SSG、表单校验、加载/错误/空状态、鉴权和部署。
- 常规业务能力：用户系统、RBAC、分页筛选、文件上传、对象存储、限流、审计日志、管理后台。

点亮条件：

- 完成一个真正可用的 SaaS Web 产品，而不是单纯 Demo。
- 能从浏览器出发讲清一次请求如何经过 Next.js、FastAPI、PostgreSQL/Redis，再返回前端更新状态。

## L3：LLM 基础与模型接入

目标：从传统全栈工程师升级为能正确使用大模型的 AI 应用工程师。

必须掌握：

- 模型概念：Token、Context Window、Temperature、Top P、System/User/Assistant Message、Transformer 直觉、Attention 直觉、训练/推理/微调区别、幻觉、Embedding、余弦相似度。
- 模型 API：普通对话、流式输出、Structured Output、JSON Schema、Function Calling、多轮上下文、超时重试、Token 统计、模型切换、错误处理。
- Prompt 工程：指令边界、Few-shot、结构化输出、上下文组织、Prompt 模板、版本管理。

点亮条件：

- 完成一个 AI Chat SaaS：多会话、流式回答、Markdown 渲染、结构化输出、Tool Calling、对话历史、Token/成本记录、中止生成、超时重试、模型切换。
- 能说明为什么不能无限保存对话历史，为什么结构化输出比普通 JSON 提示更可靠，模型超时和重复工具执行如何处理。

## L4：AI 应用核心

目标：从“API 调用工程师”进入真正 AI 应用工程。

最高优先级是 RAG：

- 数据处理：PDF、Word、HTML、Markdown 解析，文档清洗，Metadata，Chunk，表格和图片处理边界。
- 检索：Embedding、pgvector、Top-K、阈值、Metadata Filter、BM25、混合检索、Rerank。
- 生成：检索内容注入、引用来源、无答案拒答、上下文去重排序、长文档压缩、降低幻觉。

Agent 与 Tool Calling：

- 工具参数校验、执行权限、最大执行步数、超时、人工确认、幂等性、工具错误反馈、状态持久化。
- 真实产品优先使用受约束的工作流，不追求无限自主循环。

多模态方向：

- 图片理解、OCR、语音转文字、文字转语音、实时语音交互、相机和文件输入。
- 这一层可以结合 Flutter 形成差异化。

点亮条件：

- 完成一个企业知识库、研究助手或专业领域助手。
- 至少包含文档上传、异步解析、Chunk、Embedding、混合检索、Rerank、引用溯源、无答案拒答、Tool Calling、用户知识库隔离和管理后台。
- 建立测试集，而不是只靠手动体验判断效果。

## L5：AI 生产工程化

目标：把 AI Demo 升级为能进入生产环境的 AI 产品。

必须掌握：

- Evaluation：测试数据集、检索召回率、Context Relevance、Answer Relevance、Faithfulness、引用准确率、无答案识别率、工具选择准确率、回归测试。
- 可观测性：请求日志、Trace ID、Prompt 和模型版本、Token、模型耗时、首 Token 延迟、总响应时间、工具调用记录、检索结果、错误率、用户反馈。
- 稳定性：超时、重试、指数退避、限流、熔断、降级、幂等性、队列、死信处理、模型故障切换。
- 安全：Prompt Injection、越权访问、租户隔离、敏感信息脱敏、文件上传安全、工具权限、SQL/命令注入、API Key 管理、日志隐私。
- 成本：Token 预算、上下文压缩、Embedding 缓存、Prompt 缓存、模型路由、用户配额、并发控制、成本告警。

点亮条件：

- 项目能展示真实指标：测试问题数量、Recall@5、引用准确率、无答案识别率、首 Token P95、总响应 P95、单次请求成本、API 错误率。
- 数字不必漂亮，但必须有测试方法、真实测量、优化前后对比和解释过程。

## L6：系统设计与差异化能力

目标：在主线 AI 全栈之外，用 Go 和 Flutter 形成差异化，而不是过早分散精力。

Go 的定位：

- 用于后端增强，例如 API Gateway、高并发 SSE/WebSocket、鉴权限流、实时通信、任务分发、爬虫采集、基础设施工具。
- 重点掌握 Goroutine、Channel、Context、Mutex、Race Condition、HTTP Server、Middleware、连接池、Graceful Shutdown、Profiling、测试和错误处理。
- 不要为了展示 Go 强拆微服务。

Flutter 的定位：

- 不是重新学习 Flutter，而是把 Flutter 接入 AI 产品。
- 重点补 SSE/WebSocket 流式响应、Markdown 增量渲染、音频录制与播放、相机与图片输入、本地缓存、对话状态管理、弱网重试、后台任务、推送通知和 Token 安全存储。

系统设计：

- 掌握单体与微服务取舍、水平扩容、无状态服务、负载均衡、缓存、消息队列、数据一致性、幂等性、多租户、限流配额、灾备和容量估算。
- 能解释为什么 AI 服务用 Python，为什么某个模块用 Go，为什么选择 SSE 而不是 WebSocket，如何隔离企业数据，模型不可用时如何降级，如何估算模型成本。

## L7：求职与个人品牌

目标：把能力转成 Offer，而不是只停留在学习。

推荐准备两个旗舰项目：

1. AI 企业知识库：证明 AI + Web 全栈深度。
2. Flutter 多模态 AI 助手：证明移动端和跨端差异化。

每个项目至少准备：

- 在线体验地址。
- GitHub 仓库。
- README。
- 架构图。
- 数据模型图。
- API 文档。
- 部署说明。
- 测试说明。
- AI 评测报告。
- 性能和成本指标。
- 2-3 分钟演示视频。
- 技术难点复盘。

面试中要能 15 分钟讲清：

- 解决什么问题。
- 为什么使用 AI。
- 整体架构是什么。
- RAG 或 Agent 如何设计。
- 遇到了什么问题。
- 如何评测。
- 如何优化延迟和成本。
- 为什么使用 Python / Go / Flutter。
- 用户增长十倍如何扩展。
- 自己具体负责什么。

## 技术优先级

### P0：现在必须投入

```text
Python
FastAPI
TypeScript
React + Next.js
PostgreSQL
Redis
Docker
HTTP / SSE
LLM API
Structured Output
Tool Calling
RAG
Embedding
pgvector
混合检索
Rerank
Evaluation
AI 安全
日志与监控
```

### P1：完成主线后加强

```text
Go
Flutter AI 客户端
异步任务
消息队列
LangGraph
MCP
多模态
OpenTelemetry
云部署
系统设计
```

### P2：根据岗位选择

```text
Kubernetes
本地大模型部署
LoRA / QLoRA
Milvus
Kafka
复杂微服务
模型推理优化
GPU 基础设施
```

### 暂不深挖

```text
Vue / Nuxt 深度生态
多 Agent 炫技
从零训练大模型
同时学习多个向量数据库
为了技术栈丰富强拆微服务
复杂 Kubernetes 集群
大量低完成度 AI Demo
```

Vue 保留已有经验即可，除非目标职位明确要求 Vue / Nuxt。

## 推荐点亮顺序

```text
第 1 步：Python + FastAPI
第 2 步：PostgreSQL + Redis + Docker
第 3 步：TypeScript + Next.js
第 4 步：LLM API + 流式输出 + Structured Output
第 5 步：RAG + pgvector + 混合检索 + Rerank
第 6 步：Agent + Tool Calling + 工作流
第 7 步：Evaluation + 安全 + 监控 + 成本控制
第 8 步：Flutter 多模态客户端
第 9 步：Go 网关或高并发模块
第 10 步：整理旗舰项目并准备求职
```

## 统一验收标准

| 状态 | 含义 |
| ---- | ---- |
| 20% | 看过课程，理解基本概念 |
| 40% | 能跟着教程实现 |
| 60% | 能脱离教程独立实现 |
| 80% | 能集成进项目并部署 |
| 100% | 能讲原理、做取舍、测指标、解决线上问题 |

只有到 80% 才算点亮，达到 100% 才算面试级能力。

## Challenge 入口

每一层都要通过 `5-Playground/P004-下一份工作准备/` 下的 challenge 验收，不把“看过教程”当作完成。

| 层级 | Challenge 入口 | 验收重点 |
| ---- | -------------- | -------- |
| L1 | `L1-工程基础底座/challenges/` | FastAPI、数据库、鉴权、Docker、测试 |
| L2 | `L2-Web全栈产品能力/challenges/` | Next.js + FastAPI 的完整产品闭环 |
| L3 | `L3-LLM基础与模型接入/challenges/` | LLM API、流式输出、Structured Output、Tool Calling |
| L4 | `L4-AI应用核心/challenges/` | RAG、Agent、检索、引用、拒答 |
| L5 | `L5-AI生产工程化/challenges/` | Evaluation、日志、监控、成本、安全 |
| L6 | `L6-系统设计与差异化/challenges/` | Go / Flutter / 系统设计取舍 |
| L7 | `L7-求职与个人品牌/challenges/` | 简历、项目讲述、面试表达、作品展示 |

## 与 P001 的关系

P001 是工程地基，继续承担 CSAPP、设计模式和架构基础重建，不适合塞入完整 AI 全栈路线。AI 全栈能力金字塔属于 P004，因为它直接服务下一份工作、技术栈选择、项目组合、简历表达和面试准备。

后续执行时：

- P001 解决“工程基础是否扎实”。
- P004 解决“下一份工作需要什么能力、如何展示、如何拿 Offer”。
- 当前公司用户反馈评估系统是 P004 的第一条现实 AI 项目资产。
