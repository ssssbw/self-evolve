# 技术面试准备指南

> 1-2 年后跳槽/晋升时用。现在先了解，学习过程中持续积累。

---

## 面试考察维度

| 维度 | 权重 | 你现在的准备 |
|------|------|-------------|
| 算法与数据结构 | 30% | LeetCode 路线图已规划 |
| 系统设计 | 20% | 系统设计入门已写 |
| 计算机基础 | 20% | CSAPP 正在学习 |
| 项目经验 | 20% | 工作中持续积累 |
| 框架深度 | 10% | Flutter/Dart + 设计模式 |

---

## Flutter/Dart 面试高频题

### Dart 语言

1. **Dart 的 Isolate 和线程的区别？**
   - Isolate 有独立堆内存，线程共享堆
   - Isolate 通过消息通信，线程通过共享内存+锁
   - Dart 的 async/await 是单线程事件循环，不是多线程

2. **Dart 的 Future 和 Stream 的区别？**
   - Future：一次性的异步结果
   - Stream：异步数据流（多个值）
   - 类比：Future 是函数调用，Stream 是事件监听

3. **Dart 的 Extension Method 是什么？给个实际应用**
   - 给现有类添加方法，不修改源码
   - 例子：给 BuildContext 添加 context.theme 快捷访问

4. **Dart 3 的 sealed class 有什么用？**
   - 限制子类在同一文件，编译器穷举检查
   - 用于状态管理：Loading/Success/Failure

### Flutter 框架

1. **Widget、Element、RenderObject 的关系？**
   - Widget 是描述（immutable），Element 管理生命周期，RenderObject 执行布局/绘制
   - 你已经学过了（见 `flutter-rendering-pipeline.md`）

2. **StatefulWidget 的生命周期？**
   - createState → initState → build → didUpdateWidget → deactivate → dispose
   - 你已经学过了（模板方法模式）

3. **Flutter 的渲染管线？**
   - build → layout → paint → composite
   - 你已经学过了（CSAPP 流水线类比）

4. **Keys 的作用？**
   - 帮助 Element 区分同类型的 Widget
   - 列表中增删元素时，避免状态错乱

5. **InheritedWidget 的原理？**
   - 代理模式 + 观察者模式
   - 子树中的 Widget 通过 context 向上查找最近的 InheritedWidget
   - 你已经学过了（见 `flutter-design-patterns.md`）

### 状态管理

1. **Provider vs Bloc vs Riverpod 的区别？**
   - 你已经学过了（见 `state-management-comparison.md`）

2. **BLoC 的 Event 和 State 的关系？**
   - Event 是命令（用户操作），State 是结果（UI 状态）
   - 一对多：一个 Event 可能触发多个 State 变化（Loading → Success）

---

## Go 后端面试高频题

### 语言基础

1. **Go 的 Goroutine 和线程的区别？**
   - Goroutine 初始栈 2KB，线程通常 1MB+
   - Goroutine 由 Go runtime 调度，线程由 OS 调度
   - Goroutine 通过 channel 通信，不共享内存

2. **Go 的 interface 是隐式的？什么意思？**
   - 不需要 `implements` 关键字
   - 只要 struct 实现了 interface 的所有方法，就自动满足
   - 鸭子类型

3. **Go 的错误处理为什么不用 try-catch？**
   - 显式处理每个错误，不隐藏问题
   - if err != nil 模式虽然啰嗦但清晰

### 并发

1. **Channel 的方向？**
   - 只读 `<-chan T`，只写 `chan<- T`
   - 编译时检查，防止误用

2. **select 的作用？**
   - 同时等待多个 channel 操作
   - 类似于 I/O 多路复用（CSAPP 第 12 章）

---

## 面试准备节奏

```
当前阶段（第 1-4 月）：专注学习，不做面试准备
    ↓
第 5-8 月：开始 LeetCode 刷题（每天 1 题）
    ↓
第 9-12 月：
  - LeetCode 刷到 100 题
  - 整理 3-5 个项目亮点（工作中做了什么、解决了什么问题）
  - 模拟面试 2-3 次
    ↓
准备跳槽/晋升
```

---

## 推荐面试资源

| 资源 | 类型 | 说明 |
|------|------|------|
| LeetCode（力扣） | 刷题 | 按知识点分类刷 |
| 《剑指 Offer》 | 书 | 经典面试题 |
| ByteByteGo | 网站 | 系统设计 |
| Flutter 面试题合集 | GitHub | 搜 "flutter interview" |
