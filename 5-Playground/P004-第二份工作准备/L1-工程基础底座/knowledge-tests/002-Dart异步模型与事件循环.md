# 知识验收 002 — Dart 异步模型与事件循环

> 所属项目：P004 第二份工作准备  
> 所属层级：L1 工程基础底座  
> 创建日期：2026-09-04  
> 状态：⬜ 未作答

## 目标

验证自己是否真正理解 Dart / Flutter 的异步模型，尤其是 `Future`、`Stream`、`await`、`unawaited`、`mounted`、`isolate` 和 `event loop`。

这不是背定义。验收重点是：

- 能解释异步和并发的差别。
- 能解释 microtask queue 和 event queue 的执行顺序。
- 能判断什么时候该用 `await`，什么时候该用 `unawaited`。
- 能判断什么时候要检查 `mounted`。
- 能判断什么时候该用 `isolate` 或 `compute`。
- 能把这些知识放回 Flutter 页面生命周期和 UI 更新里理解。

## 学习笔记卡片

先用自己的话补完下面内容。不要复制教程原文。

| 知识点 | 我的理解 | 例子 |
| ------ | -------- | ---- |
| Future |  |  |
| Stream |  |  |
| await |  |  |
| unawaited |  |  |
| mounted |  |  |
| isolate |  |  |
| event loop |  |  |
| microtask queue |  |  |
| event queue |  |  |

## 自测题

### A. 基础解释

1. `Future<T>` 和 `Stream<T>` 的核心区别是什么？
2. `await` 为什么不是“阻塞线程”？它到底做了什么？
3. `unawaited(...)` 的作用是什么？它解决的是哪类问题？
4. `mounted` 为什么要在异步回来后检查？
5. Dart 的 event loop 主要负责什么？
6. microtask queue 和 event queue 的区别是什么？
7. `Future.microtask(...)`、`Future(() {})`、`Future.delayed(Duration.zero, ...)` 分别更接近哪个队列？
8. `isolate` 解决的主要是什么问题？为什么普通网络请求通常不需要丢到 isolate？

### B. 顺序判断

9. 下面代码的输出顺序是什么？为什么？

```dart
import 'dart:async';

void main() {
  print('A');
  scheduleMicrotask(() => print('B'));
  Future(() => print('C'));
  Future.microtask(() => print('D'));
  Future.delayed(Duration.zero, () => print('E'));
  print('F');
}
```

10. 下面代码里，`print('2')` 为什么会在 `await` 后才执行？

```dart
Future<void> foo() async {
  print('1');
  await Future.delayed(const Duration(seconds: 1));
  print('2');
}
```

### C. Flutter 场景题

11. 一个页面发起请求后，用户在请求结束前退出页面。为什么这时要先检查 `mounted` 再 `setState`？
12. 哪些工作适合放进 isolate？哪些不适合？请各举 3 个例子。
13. 如果一个按钮点击后页面卡顿，你会先怀疑 `Future`、`Stream`、`event loop` 还是 `isolate`？为什么？
14. 如果你需要一边流式接收 AI 输出，一边更新 UI，应该优先理解哪几个概念？

### D. 排错题

15. 为什么“我用了 async/await，但页面还是卡”不一定是 async 的问题？
16. 为什么“我把请求放到 Future 里”并不等于“我用了并行计算”？
17. 为什么不断塞 microtask 可能会让 UI 事件被延迟？
18. 为什么后台 isolate 不能直接 `setState` 或 `Navigator.push`？

## 代码理解题

请直接写出你对下面每段代码的判断。

### 题 1

```dart
void main() {
  print('start');
  Future(() => print('future'));
  print('end');
}
```

- 输出顺序：
- 原因：

### 题 2

```dart
class DemoState extends State<DemoPage> {
  Future<void> load() async {
    final data = await api.fetchData();
    if (!mounted) return;
    setState(() {
      value = data;
    });
  }
}
```

- 为什么要检查 `mounted`：
- 如果不检查会怎样：

### 题 3

```dart
unawaited(sendLog());
```

- 这段代码适合什么场景：
- 有什么风险：

## 表达题

用 2 分钟讲清楚：

> Dart 的 event loop、Future、await、mounted 和 isolate 为什么是一套连起来的知识？

回答必须包含：

- 哪些概念解决“等待”问题。
- 哪些概念解决“页面还在不在”问题。
- 哪些概念解决“CPU 太重”问题。
- 这些知识为什么对 Flutter 开发重要。

## 验收标准

| 掌握度 | 标准 |
| ------ | ---- |
| 20% | 能说出 Future、Stream、await、mounted、isolate 这些词的基本含义 |
| 40% | 能解释 microtask queue、event queue 和 event loop 的大致关系 |
| 60% | 能独立预测简单异步代码的输出顺序，并解释 `await` 的作用 |
| 80% | 能把异步、mounted、isolate 放到真实 Flutter 页面场景里做判断 |
| 100% | 能在面试里讲清异步模型、事件循环和生命周期安全的取舍 |

## 手写答案区

### 第一轮独立作答

- 作答日期：
- 实际用时：
- 是否查资料：
- 自评掌握度：

#### A. 基础解释答案

1.
2.
3.
4.
5.
6.
7.
8.

#### B. 顺序判断答案

9.
10.

#### C. Flutter 场景题答案

11.
12.
13.
14.

#### D. 排错题答案

15.
16.
17.
18.

#### E. 代码理解题答案

题 1：
题 2：
题 3：

#### F. 表达题草稿


## Review 记录

- AI review 日期：
- 主要问题：
- 修正动作：
- 最终掌握度：
- 可迁移到项目的点：
- 可用于面试表达的点：
