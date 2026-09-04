# Flutter 栈学习清单

> 定位：工作刚需 + Flutter 开发岗退路 + AI 移动端差异化。  
> 归属：A1-技术 / frontend。  
> 执行原则：不和 AI 全栈主线抢资源；优先解决工作中会遇到的真实问题，再沉淀为面试表达和作品能力。

## 学习目标

这份清单不是从零入门 Flutter，而是把已有 Flutter 工作经验升级为可解释、可排查、可架构、可面试的能力。

最终目标：

1. 能稳定完成工作中的 Flutter 业务开发。
2. 能解释 Flutter 的核心机制，而不是只会套组件。
3. 能排查生命周期、异步、状态、性能、内存和平台接入问题。
4. 能形成“Flutter + AI 移动端应用开发”的求职差异化。

## L1：Dart 语言进阶与异步模型

目标：理解 Flutter 代码运行的语言地基，尤其是异步、事件循环和并行计算边界。

- [ ] `Future`：一次性异步结果，成功或失败只完成一次。
- [ ] `Stream`：连续异步事件，适合 WebSocket、下载进度、输入变化等场景。
- [ ] `async / await`：把异步流程写成顺序代码，但不等于新线程。
- [ ] `unawaited`：明确标记故意不等待的 Future，并处理错误。
- [ ] microtask queue 与 event queue：理解任务调度顺序。
- [ ] `isolate` / `compute`：CPU 密集任务如何避免阻塞 main isolate。
- [ ] `extension`、`mixin`、泛型、`factory constructor`、`late`、null safety。

验收：

- 能讲清 `Future`、`Stream`、`isolate` 的区别。
- 能判断一个问题应该用 `Future` 等待、`Stream` 监听，还是用 isolate 搬走 CPU 任务。
- 能写出异步回来后检查 `mounted` 再更新 UI 的代码。

## L2：Flutter 三棵树与构建机制

目标：理解 Flutter UI 从配置到屏幕像素的过程。

- [ ] Widget Tree：Widget 是 immutable 的 UI 配置。
- [ ] Element Tree：Element 是 Widget 在树中的实例位置，负责生命周期和复用。
- [ ] RenderObject Tree：RenderObject 负责 layout、paint、hit test。
- [ ] `BuildContext` 本质上关联 Element。
- [ ] `setState`：标记对应 Element dirty，等待下一帧 rebuild。
- [ ] `Key`：控制 Element 复用和状态保留。
- [ ] `InheritedWidget` / `InheritedModel`：跨子树传递依赖的底层机制。

验收：

- 能解释为什么 Widget 本身没有 `mounted`。
- 能解释为什么 build 会频繁执行，以及为什么不要在 build 中做副作用。
- 能用 `Key` 解决列表状态错乱或组件复用问题。

## L3：生命周期与状态管理

目标：能把页面状态、业务状态和资源生命周期管理清楚。

- [ ] `initState`：初始化 controller、订阅、首屏请求入口。
- [ ] `didChangeDependencies`：依赖 InheritedWidget 的初始化或刷新。
- [ ] `didUpdateWidget`：父组件传入配置变化后的处理。
- [ ] `deactivate` / `dispose`：释放 controller、listener、subscription、animation。
- [ ] `mounted` / `context.mounted`：异步回来后判断 UI 节点是否还存在。
- [ ] 局部状态：`setState` 的适用边界。
- [ ] 页面状态：loading / success / empty / error。
- [ ] 跨页面状态：Provider / Riverpod / Bloc 的取舍。
- [ ] 状态归属判断：状态属于谁、生命周期多长、谁能修改、谁需要监听。

验收：

- 能设计一个页面的状态模型，而不是把所有变量堆在 State 里。
- 能解释 `TextEditingController`、`AnimationController`、`StreamSubscription` 为什么要释放。
- 能说明 Provider / Riverpod / Bloc 的适用场景和取舍。

## L4：渲染、布局与性能优化

目标：能定位和优化常见卡顿、重建、重绘、内存问题。

- [ ] Flutter 一帧流程：build → layout → paint → composite → raster。
- [ ] 16ms / 8ms 帧预算：理解 60 FPS / 120 FPS 的性能边界。
- [ ] build、layout、paint 的职责和优化方向。
- [ ] `const`：减少不必要对象创建和 rebuild 成本。
- [ ] 拆小 Widget：缩小 dirty Element 影响范围。
- [ ] `ListView.builder` / sliver：长列表按需构建。
- [ ] `RepaintBoundary`：隔离重绘边界。
- [ ] 图片优化：尺寸、解码、缓存、内存占用。
- [ ] Flutter DevTools：查看 rebuild、timeline、memory、CPU profile。
- [ ] main isolate 卡顿：识别 CPU 密集任务并用 isolate / compute 处理。

验收：

- 能解释列表卡顿、页面首帧慢、图片占内存、点击后 UI 冻住的常见原因。
- 能用 DevTools 找到至少一个性能证据，而不是靠猜。
- 能写出一个长列表优化方案。

## L5：网络、缓存与异步业务架构

目标：能处理真实业务 App 中的接口、异常、缓存和弱网问题。

- [ ] HTTP 请求生命周期、超时、取消、重试。
- [ ] Dio / http 的封装边界。
- [ ] 统一错误模型：网络错误、服务端错误、业务错误、解析错误。
- [ ] loading / empty / error / success 状态统一表达。
- [ ] 防重复提交和并发请求控制。
- [ ] Token 存储、过期刷新、请求重放。
- [ ] 本地缓存：内存缓存、文件缓存、本地数据库。
- [ ] 弱网策略：重试、降级、离线兜底。
- [ ] WebSocket / SSE：实时消息与 AI 流式响应。

验收：

- 能设计一个不会到处散落 try/catch 的接口层。
- 能解释 token 过期刷新时如何避免多个请求同时刷新。
- 能实现一个支持 loading / error / retry 的页面请求闭环。

## L6：Flutter 工程架构与可维护性

目标：让项目变大后仍然能维护、测试和定位问题。

- [ ] feature-first 目录结构。
- [ ] presentation / domain / data 分层。
- [ ] Repository Pattern。
- [ ] Dependency Injection。
- [ ] ViewModel / Controller / Notifier 的职责边界。
- [ ] 路由管理和页面参数规范。
- [ ] 主题系统、暗色模式、国际化。
- [ ] 日志、埋点、异常上报。
- [ ] 单元测试、Widget 测试、集成测试。
- [ ] 多环境配置：dev / staging / prod。

验收：

- 能把一个业务功能拆成 UI、状态、接口、模型、错误处理和测试。
- 能解释为什么 UI 层不应该直接依赖 Dio 细节。
- 能给出一个中型 Flutter 项目的目录结构和依赖方向。

## L7：平台能力与 Flutter + AI 差异化

目标：形成“客户端工程能力 + AI 应用落地能力”的组合标签。

- [ ] Platform Channel 与插件机制。
- [ ] Android / iOS 权限模型。
- [ ] 相机、相册、文件选择、麦克风。
- [ ] 音频录制与播放、TTS / STT 接入。
- [ ] 本地数据库与 secure storage。
- [ ] 推送通知、后台任务、Deep Link。
- [ ] WebView 与原生页面协作。
- [ ] AI Chat UI：消息列表、输入框、生成中状态、中断生成。
- [ ] Markdown 增量渲染。
- [ ] LLM 流式响应：SSE / WebSocket。
- [ ] 图片输入、多模态消息、本地会话缓存。
- [ ] Token 安全存储与日志隐私。

验收：

- 完成一个 Flutter 多模态 AI 助手原型。
- 至少支持流式回答、Markdown 展示、本地会话缓存、图片或语音输入中的一项。
- 能在面试中讲清为什么选择 SSE 或 WebSocket，以及如何处理弱网和安全问题。

## 面试表达清单

- [ ] Flutter 三棵树是什么？
- [ ] Widget 为什么是 immutable？
- [ ] `setState` 做了什么？
- [ ] `BuildContext` 是什么？
- [ ] `mounted` 是什么，什么时候检查？
- [ ] `Key` 有什么作用？
- [ ] `Future` 和 `Stream` 区别？
- [ ] Dart event loop 怎么工作？
- [ ] microtask queue 和 event queue 区别？
- [ ] `isolate` 和 thread 区别？
- [ ] Flutter 一帧渲染流程是什么？
- [ ] build、layout、paint 分别是什么？
- [ ] ListView 怎么优化？
- [ ] 图片加载怎么优化？
- [ ] 如何减少 rebuild？
- [ ] Provider / Riverpod / Bloc 怎么选？
- [ ] 网络异常和 token 过期怎么处理？
- [ ] 页面销毁后请求回来怎么办？
- [ ] 如何做本地缓存？
- [ ] Flutter 如何接入原生能力？
- [ ] Platform Channel 原理是什么？
- [ ] Flutter 如何接入 AI 流式响应？
- [ ] SSE 和 WebSocket 在客户端怎么选？
- [ ] 如何设计一个 AI Chat 页面？
- [ ] 如何定位 Flutter 卡顿？

## 推荐学习顺序

1. Dart 异步模型与生命周期安全：`Future`、`Stream`、`mounted`、`unawaited`、`isolate`。
2. Flutter 三棵树与 build 机制。
3. 状态管理与页面状态建模。
4. 网络、缓存、错误处理和弱网策略。
5. 渲染性能、列表性能和 DevTools 排查。
6. 工程架构、测试和多环境配置。
7. Flutter + AI 客户端能力。

## 执行规则

- 工作中遇到的问题优先进入本清单对应层级。
- 每次只补一个最小知识点，不追求一次学完整层。
- 能用工作问题验证的，不只看教程。
- 能沉淀为面试表达的，记录到 P004 面试准备。
- 涉及公司数据、接口、客户信息时，只记录脱敏后的通用问题、方案和结果。
