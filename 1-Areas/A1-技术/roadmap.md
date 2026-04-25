# Flutter开发者到顶尖全栈工程师的技术学习路线图（中文版）

以下路线图面向在 Flutter/Dart 具备一定工作经验、目标成为具备深厚 CS 基础和 AI 能力的全栈工程师的开发者。路线分为三个阶段：阶段 1 重建根基、阶段 2 深耕全栈、阶段 3 拓展前沿。每个主题给出简要描述、为何重要、1-2 条优质资源以及明确的进度标记，用以跟踪学习进度。

Phase 1 — 重建根基 (6-12 个月)
- 计算机体系结构
  - WHAT & WHY：理解计算机硬件如何执行指令、缓存与内存层次结构的工作原理。掌握这些原理有助于理解软件性能瓶颈、优化机会以及系统级思考。
  - 推荐资源：
    - 深入理解计算机系统（CSAPP 中文版） — 当前项目中 🔄
    - Nand2Tetris（From NAND to Tetris!）课程与实验
    - Patterson & Hennessy 的 Computer Architecture 经典讲义/中文译本（选读）
  - 进度：🔄
- 操作系统原理
  - WHAT & WHY：掌握进程/线程、内存管理、调度、文件系统、I/O、并发模型等，为并发编程和后端服务稳定性打底。
  - 推荐资源：
    - 操作系统概念（Operating System Concepts）中文/英文
    - 鸟哥的 Linux 私房菜（面向实操的 Linux/系统知识）
  - 进度：⬜
- 计算机网络与网络编程
  - WHAT & WHY：理解网络分层、协议、路由、流控、TLS/安全等，支撑 API 设计、分布式系统与安全性。
  - 推荐资源：
    - Computer Networking: A Top-Down Approach（Kurose & Ross）中文
    - TCP/IP Illustrated（Stevens）选读
  - 进度：⬜
- 数据结构与算法
  - WHAT & WHY：数据组织、常用算法、复杂度分析是高效编码、面试和系统设计的基础。
  - 推荐资源：
    - 算法导论（CLRS）中文版/英文版
    - LeetCode 刷题攻略与数据结构专题
  - 进度：⬜
- 编译原理
  - WHAT & WHY：理解从源码到可执行文件的过程，掌握语言实现与性能边界，提升调试和优化能力。
  - 推荐资源：
    - 龙书（Compilers: Principles, Techniques, Tools）中文版
    - 现代编译原理相关课程/讲义（Coursera、edX 等）
  - 进度：⬜
- 软件设计基础
  - WHAT & WHY：掌握面向对象设计原则（S.O.L.I.D）和常用设计模式，写出可维护、可扩展的代码。是提升代码质量的最快路径。
  - 推荐资源：
    - 《Head First 设计模式》
    - 《设计模式》- GoF（经典）
    - Refactoring.Guru（在线图解）
  - 进度：⬜
- 软件架构
  - WHAT & WHY：理解分层架构、MVVM、Clean Architecture 等架构模式，提升系统设计能力和代码组织能力。
  - 推荐资源：
    - 《架构整洁之道》- Robert C. Martin
    - Flutter 官方架构示例（BLoC、Riverpod）
  - 进度：⬜

Phase 2 — 深耕全栈 (ongoing, parallel with Phase 1)
- Frontend mastery: Flutter 深入与 Dart 语言特性
  - WHAT & WHY：深入理解 Flutter 的渲染管线、状态管理内部原理、以及自定义渲染能力，结合 Dart 的语言特性提升开发效率与性能。
  - 推荐资源：
    - Flutter 官方文档（flutter.dev）
    - Dart 官方语言指南与 Effective Dart（dart.dev）
    - 与 Flutter 渲染与性能优化相关的专著/高质量文章
  - 进度：⬜
- Backend: Go 为主语言的全栈后端
  - WHAT & WHY：掌握 Go 进行 REST/gRPC API 的设计与实现，结合数据库、缓存和消息队列构建高可用后端。
  - 推荐资源：
    - The Go Programming Language（Kernighan & Donovan）
    - Go by Example / Go In Action
    - Designing Data-Intensive Applications（Kleppmann）
    - REST API Design Rulebook、gRPC Up & Running
    - SQL Antipatterns、Redis in Action / Redis 快速入门
  - 进度：⬜
- DevOps 基础
  - WHAT & WHY：容器化、持续集成/持续部署、基础部署能力，是将本地开发落地到实际环境的关键。
  - 推荐资源：
    - Docker 官方文档 / Docker Deep Dive
    - GitHub Actions / CI/CD 实践
    - 常见部署场景的脚本与配置范例
  - 进度：⬜

Phase 3 — 拓展前沿 (在 Phase 1 基础扎实后推进)
- AI/ML 基础
  - WHAT & WHY：理解神经网络、LLM 基本原理、提示工程和 AI 辅助开发的思路，提升产品的智能化能力与开发效率。
  - 推荐资源：
    - Deep Learning（Ian Goodfellow 等著，中英文对照版）
    - Coursera 的 Deep Learning Specialization（Andrew Ng）
    - Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow（Aurélien Géron）
    - Prompt Engineering Guides / OpenAI Cookbook
  - 进度：⬜
- 系统设计与分布式架构
  - WHAT & WHY：理解分布式系统的基本模式、容量规划、弹性设计、微服务与数据一致性等，提升大规模系统的设计思考能力。
  - 推荐资源：
    - Designing Data-Intensive Applications（Kleppmann）
    - Building Microservices（Sam Newman） / Designing Distributed Systems（Brendan Burns）
  - 进度：⬜
- 开源贡献
  - WHAT & WHY：通过参与开源提升代码质量、协作能力和对技术生态的理解。
  - 推荐资源：
    - Pro Git（书籍） / GitHub 的贡献指南
    - How to Contribute to Open Source（Open Source Guides）
  - 进度：⬜

学习建议
- 平衡工作与学习的节奏：建议每日固定 1.5-2 小时学习，工作日分散安排，周末进行深度学习和小项目实践。总目标是保持持续性，而非短期冲刺。
- 理论与实践的比例：阶段 1 偏理论理解，阶段 2 向落地项目靠拢，阶段 3 将理论能力与系统设计、开源实践结合。
- 知识巩固方法：采用间隔重复、讲解/教学他人、定期写作（技术博客）来巩固；用小型落地项目把知识落地。
- 每周学习节奏示例：
 1) 周二/周四：2 小时理论与阅读
 2) 周末：3-5 小时编码与实践（构建小型练手项目或参与开源）
 3) 每周末留出 15-30 分钟回顾总结，更新学习计划。

备注
- 该路线图以“从 Flutter/ Dart 到全栈”为主线，强调建立扎实 CS 基础与系统设计能力，同时维持在 Flutter / Go 生态中的实践能力。
