# 讨论题 #003 — Flutter 的 Widget 为什么是 immutable 的？

> 没有标准答案，写你的真实想法。

---

## 背景

Flutter 的 Widget 是 immutable 的——一旦创建就不能修改。每次 `setState` 都创建新的 Widget 实例。这在直觉上似乎很浪费。

## 思考方向

- 从 CSAPP 的内存管理角度，不断创建新对象是不是浪费？Dart GC 能高效处理吗？
- immutability 和并发安全有什么关系？如果 Widget 是 mutable 的，多线程渲染会出什么问题？
- React、SwiftUI、Jetpack Compose 都采用了类似设计——为什么现代 UI 框架都选 immutable？
- immutable Widget + mutable State 的分离设计，本质上是解决了什么问题？

## 规则

- 写你真实的想法
- 写完后跟 AI 讨论
