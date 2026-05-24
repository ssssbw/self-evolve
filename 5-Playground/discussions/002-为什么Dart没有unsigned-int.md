# 讨论题 #002 — 为什么 Dart 没有 unsigned int？

> 没有标准答案，写你的真实想法。

---

## 背景

Dart 只有 `int`（64 位有符号），没有 `unsigned int`。但 CSAPP 第 2 章花了大量篇幅讲 unsigned。

C 有 unsigned，Go 有 uint，Rust 有 u32/u64，Java 和 Dart 没有。

## 思考方向

- Dart 为什么做这个设计决策？好处和坏处分别是什么？
- 什么时候你真的需要 unsigned？不需要的时候，没有它是不是更安全？
- 你在做 Flutter 开发时，有没有遇到过因为"没有 unsigned"导致的问题？
- 这反映了编程语言设计中的什么权衡？

## 规则

- 写你真实的想法，2-3 句话也行
- 写完后跟 AI 讨论，我会挑战你的观点
