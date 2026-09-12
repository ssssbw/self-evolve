# 知识验收 002 — Dart 异步模型与事件循环

> 所属项目：P004 第二份工作准备\
> 所属层级：L1 工程基础底座\
> 创建日期：2026-09-04\
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

| 知识点             | 我的理解                                                                                                                       | 例子                                                                                        |
| --------------- | -------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Future          | 一个异步执行的事件                                                                                                                  | 例如获取一个网络数据的时候，使用 Future 不卡 ui，让请求在后台执行                                                    |
| Stream          | 一串异步执行的事件流                                                                                                                 | 例如在网络上获取一个大文件的下载进度，订阅文件的下载进度，不卡 ui，等待进度回来后显示在界面上                                          |
| await           | 相当于是同步执行时的暂停键，等待异步执行的结果回来                                                                                                  | 例如 userData = await Future\<User>.getUserData,同步代码执行到这里是会等待异步数据给 userData 赋值              |
| unawaited       | 承诺这个 Future 的结果一定不会影响 ui                                                                                                   | <br />                                                                                    |
| mounted         | 是 Element 和 BuildContext 的属性，表示这个ui有没有加载或者渲染，利用这个属性可以预防一些异步数据回来但是界面已经被销毁的问题                                                |  例如有一个 Future还在请求异步数据，但是这个时候我们退出了界面，就需要用到 mounted 属性来检查这个界面是否已加载，否则在已销毁的页面上使用异步返回的数据会造成错误 |
| isolate         | 相当于 dart 里面的多线程，dart 只有一个主线程，如果想实现其他编程语言的多线程的并行效果，就需要使用 isolate，但是使用 isolate 需要注意，尽量把需要占用高 cpu 的操作放到 isolate，否则尽量用 Future。 | 例如，一些计算量大，高计算任务比较占用 cpu 的操作，我们需要用到 isolate，避免其卡住 ui                                       |
| event loop      |  event loop 是 dart 里面一个线程里面的事件执行顺序，按同步代码，微任务队列，事件队列的执行优先级排序                                                                | <br />                                                                                    |
| microtask queue | 位于同步代码优先级下面的事件队列，需要单独声明 microtask 来插队，内部按事件声明顺序排队，先来先服务，但是里面也不能放计算量大的任务，防止卡 UI                                             | <br />                                                                                    |
| event queue     | 优先级最低的事件队列，异步执行的操作都会在这里排队执行                                                                                                | <br />                                                                                    |

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

1. 下面代码的输出顺序是什么？为什么？

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

1. 下面代码里，`print('2')` 为什么会在 `await` 后才执行？

```dart
Future<void> foo() async {
  print('1');
  await Future.delayed(const Duration(seconds: 1));
  print('2');
}
```

### C. Flutter 场景题

1. 一个页面发起请求后，用户在请求结束前退出页面。为什么这时要先检查 `mounted` 再 `setState`？
2. 哪些工作适合放进 isolate？哪些不适合？请各举 3 个例子。
3. 如果一个按钮点击后页面卡顿，你会先怀疑 `Future`、`Stream`、`event loop` 还是 `isolate`？为什么？
4. 如果你需要一边流式接收 AI 输出，一边更新 UI，应该优先理解哪几个概念？

### D. 排错题

1. 为什么“我用了 async/await，但页面还是卡”不一定是 async 的问题？
2. 为什么“我把请求放到 Future 里”并不等于“我用了并行计算”？
3. 为什么不断塞 microtask 可能会让 UI 事件被延迟？
4. 为什么后台 isolate 不能直接 `setState` 或 `Navigator.push`？

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

| 掌握度  | 标准                                                 |
| ---- | -------------------------------------------------- |
| 20%  | 能说出 Future、Stream、await、mounted、isolate 这些词的基本含义   |
| 40%  | 能解释 microtask queue、event queue 和 event loop 的大致关系 |
| 60%  | 能独立预测简单异步代码的输出顺序，并解释 `await` 的作用                   |
| 80%  | 能把异步、mounted、isolate 放到真实 Flutter 页面场景里做判断         |
| 100% | 能在面试里讲清异步模型、事件循环和生命周期安全的取舍                         |

## 手写答案区

### 第一轮独立作答

- 作答日期： 9.12
- 实际用时：2h
- 是否查资料：无
- 自评掌握度：60%

#### A. 基础解释答案

1. 核心区别在于 Future 只返回一个结果，而 stream 会返回一串异步结果
2. 不知道，我的理解 await 是暂停了同步代码的执行顺序，等待异步操作的结果回来继续往下面执行
3. 给dart 一个承诺，保证这个异步请求的结果不会影响到正常代码的执行
4. 防止发生异步数据回来后页面销毁的情况，所以要先检查一下也没是否已加载
5. 主要负责在这个线程内代码的执行顺序，按同步顺序、microtask queue、event queue 的优先级来执行代码
6. microtask queue 需要特意声明，执行快，event queue 里面的都是异步操作
7. microtask，event queue，event queue
8. isolate 主要解决多线程的问题，可以让事件并行执行。普通网络请求不需要占用很多 cpu，放在主线程即可，如果使用 isolate 反而会增加代码的复杂度和通信难度

#### B. 顺序判断答案

1. AFBDCE

   两个 print 是同步操作，优先级在 event loop 中最高，所以优先执行，而 B 和 D 是 microtask 任务 C 和 F 是 Future 任务，前者会在 microtask queue 中排队，后者会在 event queue 中排队，所以执行顺序是AFBDCE
2. 1 ，延迟 1s，2

   await 操作会暂停当前的同步代码，等待异步操作结果回来后继续往下执行

#### C. Flutter 场景题答案

1. 这个时候请求还没有结束，用户退出界面导致界面销毁，资源被释放，如果不先检查 mounted，判断界面是否加载就直接 setState，就会报空指针，因为你的界面资源已经被释放了，这个时候根本就刷新不了界面
2. 重复大量计算型任务，占用 cpu 高的任务，例如对音视频的处理，这些就需要用 isolate\
   不占用大量 cpu 的任务，简单网络请求，普通操作
3. event loop，普通异步操作不会卡 ui，isolate 是另一个线程不会影响当前线程的 ui，但是如果在 event loop 中有一个事件是需要大量计算的可能就会卡 ui 了
4. stream，mounted，setstate

#### D. 排错题答案

1. <br />
2. <br />
3. <br />
4. <br />

#### E. 代码理解题答案

题 1：start->end->future\
因为 start 和 end 的 print 都是同步代码，在 event loop 中优先执行，而 future 是异步代码，会防止 event queue 中按序执行

题 2：防止请求结束前退出界面时界面销毁，先检查是否被加载，没有加载的话就直接返回。如果不检查 mounted，在请求结束前退出界面导致界面被销毁，此时 setState 就会报空指针

题 3：这个 Future 请求我们不关心结果就可以用 unawaited

#### F. 表达题草稿

## Review 记录

- AI review 日期：
- 主要问题：
- 修正动作：
- 最终掌握度：
- 可迁移到项目的点：
- 可用于面试表达的点：

