# 第 10 章 — 系统级 I/O

## 本章概览

讲解 Unix I/O 的基本接口：打开、读、写、关闭文件。所有高级 I/O 库（C 的 stdio、Dart 的 dart:io）都建立在这些系统调用之上。本章相对简单，是连接底层系统调用和高级 API 的桥梁。

## 核心概念

### 概念 1：文件描述符（File Descriptor）
- 一句话定义：内核为每个打开的文件分配的一个非负整数，作为后续操作的标识。
- 为什么重要：所有 I/O 操作都通过文件描述符——"一切皆文件"。
- 关键特性：
  - 0 = stdin, 1 = stdout, 2 = stderr（默认打开）
  - 每个进程有独立的文件描述符表
  - 文件描述符可以被子进程继承（fork 后）

### 概念 2：Unix I/O 基本操作
- 一句话定义：open/read/write/close 四个系统调用构成最基本的文件操作。
- 关键函数：
  - open(path, flags, mode)：打开文件，返回 fd
  - read(fd, buf, n)：从 fd 读取最多 n 字节到 buf，返回实际读取的字节数
  - write(fd, buf, n)：将 buf 中 n 字节写入 fd，返回实际写入的字节数
  - close(fd)：关闭文件描述符
- 关键特性：read/write 返回值可能小于请求的字节数（short count），必须处理

### 概念 3：标准 I/O vs Unix I/O
- 一句话定义：标准 I/O（fopen/fread/fwrite）在 Unix I/O 之上封装了缓冲区，减少系统调用次数。
- 关键区别：
  - Unix I/O：每次 read/write 都是一次系统调用（开销大）
  - 标准 I/O：数据先进入用户空间缓冲区，满时才调用一次 read/write
  - 标准 I/O 的缓冲对程序员透明
- 何时用哪个：
  - 一般情况用标准 I/O（方便、高效）
  - 需要精细控制（如网络编程、文件锁）时用 Unix I/O

### 概念 4：文件元数据（Metadata）
- 一句话定义：文件的附加信息，存储在 stat 结构体中。
- 关键字段：文件大小、inode 号、权限、所有者、修改时间、文件类型
- 文件类型：普通文件、目录、套接字、管道、设备文件

### 概念 5：RIO 包（Robust I/O）
- 一句话定义：CSAPP 提供的一个封装库，自动处理 short count 和缓冲。
- 为什么重要：在实际网络编程中，你永远不能假设一次 read 就能读够需要的字节数。

## 难点预警

本章整体难度较低。唯一需要注意的是：
- short count 的处理——不要假设 read/write 能一次性完成
- 标准 I/O 和 Unix I/O 的区别和选择

## 必做练习

- 用 Unix I/O 实现一个文件复制程序（处理 short count）
- 用 stat 查看文件元数据

## 与 Flutter/Dart 的关联

- **dart:io**：Dart 的 `File` 类本质上是对 Unix I/O 的高级封装。`File.readAsString()` 内部调用了 `open → read → close`。
- **Flutter 的 Asset 系统**：Flutter 读取 assets（图片、配置文件）时，底层通过操作系统的文件 I/O 实现。理解 I/O 模型有助于优化大量小文件读取的性能。
- **网络请求**：Dart 的 `HttpClient` 底层是 socket（也是一种 fd），每个 HTTP 请求涉及 open → write（请求）→ read（响应）→ close 的完整 I/O 流程。
- **Stream**：Dart 的 `Stream` 概念来源于 Unix 的流式 I/O。`Stream<List<int>>` 就是异步版本的 `read(fd, buf, n)` 循环。

## 关键术语对照

| 英文 | 中文 | 一句话解释 |
|------|------|-----------|
| file descriptor | 文件描述符 | 打开文件的标识符 |
| short count | 短计数 | read/write 实际处理字节数小于请求数 |
| buffer | 缓冲区 | 减少系统调用的中间存储 |
| inode | inode | 文件在磁盘上的元数据结构 |
| stat | stat | 获取文件元数据的系统调用 |

## 学习检查清单

- [ ] 能说出文件描述符 0/1/2 分别是什么
- [ ] 能处理 read 的 short count 情况
- [ ] 理解标准 I/O 和 Unix I/O 的区别
- [ ] 能解释为什么缓冲能提升 I/O 性能
