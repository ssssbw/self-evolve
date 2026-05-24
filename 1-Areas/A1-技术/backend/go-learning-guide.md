# Go 语言学习指南 — 从 Flutter 开发者到 Go 后端

> 你已经会 Dart，Go 和 Dart 有很多相似之处。这份指南帮你快速跨越。

---

## 为什么 Go 适合你

| 特性 | Dart | Go |
|------|------|-----|
| 类型系统 | 静态类型 + 空安全 | 静态类型 + 简洁 |
| 并发模型 | Isolate（重量级） | Goroutine（轻量级） |
| 包管理 | pub | go mod |
| 编译 | JIT + AOT | 原生编译 |
| 垃圾回收 | 有 | 有 |
| 接口 | 显式 implements | 隐式满足（鸭子类型） |
| 适用领域 | 前端/UI | 后端/基础设施/微服务 |

**Dart 给你的优势：** 你已经理解了静态类型、异步编程、包管理。Go 的学习曲线会比从零开始平缓很多。

---

## 学习路线（4 周）

### 第 1 周：Go 基础 + 和 Dart 的对比

**目标：能用 Go 写简单程序**

**必须掌握：**
- 变量声明：`var x int` vs `x := 1`（Go 有短变量声明）
- 基本类型：int, float64, string, bool, byte
- 控制流：if/for/switch（Go 的 if 可以带初始化语句，for 没有 while）
- 函数：多返回值 `func div(a, b int) (int, error)`
- 数组 vs 切片：`[5]int`（固定）vs `[]int`（动态，类似 Dart List）
- Map：`map[string]int`（类似 Dart Map）
- Struct：Go 没有 class，用 struct + 方法

**和 Dart 的关键区别：**
```go
// Dart: 用 class 和 interface
class Animal {
  String name;
  Animal(this.name);
  void speak() => print('$name speaks');
}

// Go: 用 struct 和方法
type Animal struct {
    Name string
}
func (a *Animal) Speak() {
    fmt.Printf("%s speaks\n", a.Name)
}
```

**练习：** 用 Go 实现一个 TODO List CLI 程序

### 第 2 周：Go 的接口 + 错误处理 + 并发

**目标：理解 Go 的核心哲学**

**接口（最关键的差异）：**
```go
// Go 的接口是隐式满足的——不需要 implements
type Writer interface {
    Write([]byte) (int, error)
}

type FileWriter struct {
    file *os.File
}

// 只要 FileWriter 有 Write 方法，它就自动满足 Writer 接口
func (fw *FileWriter) Write(data []byte) (int, error) {
    return fw.file.Write(data)
}

// Dart 需要 class FileWriter implements Writer
// Go 不需要！这叫"鸭子类型"——如果它走起来像鸭子，那它就是鸭子
```

**错误处理（Go 没有 try-catch）：**
```go
// Dart: try { ... } catch (e) { ... }
// Go: 显式检查每个错误
file, err := os.Open("config.json")
if err != nil {
    return fmt.Errorf("failed to open config: %w", err)
}
defer file.Close() // defer 类似 Dart 的 finally

// 习惯这种模式：if err != nil { ... }
// Go 社区认为显式错误处理比 try-catch 更清晰
```

**Goroutine + Channel（Go 的杀手级特性）：**
```go
// Goroutine — 轻量级线程
go func() {
    fmt.Println("在另一个 goroutine 中运行")
}()

// Channel — goroutine 之间通信
ch := make(chan string)

go func() {
    ch <- "hello" // 发送到 channel
}()

msg := <-ch // 从 channel 接收
fmt.Println(msg)

// 对比 Dart：
// Dart 的 Isolate 很重（每个 isolate 独立堆）
// Go 的 Goroutine 很轻（初始栈只有 2KB，共享堆）
// Dart 用 SendPort/ReceivePort 通信
// Go 用 channel 通信（更优雅）
```

**练习：** 用 goroutine + channel 实现一个并发网页爬虫

### 第 3 周：Go Web 开发基础

**目标：能写一个 REST API 服务**

**核心知识点：**
- `net/http` 标准库（Go 的标准库极其强大）
- 路由（标准库或 chi/gorilla mux）
- JSON 处理：`encoding/json`
- 数据库操作：`database/sql` + 驱动
- 中间件模式

**一个最简 REST API：**
```go
package main

import (
    "encoding/json"
    "log"
    "net/http"
)

type Todo struct {
    ID    int    `json:"id"`
    Title string `json:"title"`
    Done  bool   `json:"done"`
}

var todos = []Todo{
    {ID: 1, Title: "学 Go", Done: false},
    {ID: 2, Title: "写 API", Done: false},
}

func getTodos(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(todos)
}

func main() {
    http.HandleFunc("/todos", getTodos)
    log.Println("Server running on :8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
```

**练习：** 完整实现一个 TODO REST API（CRUD + SQLite）

### 第 4 周：Go + Flutter 联通

**目标：用 Go 后端 + Flutter 前端构建一个完整应用**

- Flutter 用 `http` 包或 `dio` 调用 Go 后端 API
- Go 后端提供 RESTful JSON API
- 学习 gRPC（Google 的高性能 RPC 框架，Go 和 Flutter 都支持）

---

## 推荐资源

| 资源 | 类型 | 说明 |
|------|------|------|
| [A Tour of Go](https://go.dev/tour/) | 互动教程 | 官方出品，1-2 小时搞定 |
| [Go by Example](https://gobyexample.com/) | 代码示例 | 每个概念一个示例，适合速查 |
| [Effective Go](https://go.dev/doc/effective_go) | 文档 | Go 的最佳实践 |
| 《Go 程序设计语言》 | 书 | Go 界的 CSAPP |
| [Go 语言圣经（中文版）](https://gopl-zh.github.io/) | 书 | 上面的中文翻译 |

---

## Flutter 开发者学 Go 的常见陷阱

1. **Go 没有 class** — 用 struct + 方法替代，不需要 Dart 的 class
2. **Go 没有 try-catch** — 必须显式处理每个 error
3. **Go 的 Map/Channel 不是类** — 内置类型，不是对象
4. **Go 没有泛型（直到 1.18）** — 现在有了，但社区代码还有很多不用泛型的
5. **Go 的首字母大小写决定可见性** — 大写 = public，小写 = private（Dart 用下划线 _）
6. **Go 没有 constructor** — 用 `NewXxx()` 工厂函数
7. **defer 不是 finally** — defer 在函数返回时执行，不是在代码块结束时

---

## 学习检查清单

- [ ] 完成 A Tour of Go
- [ ] 能用 Go 写一个 CLI 程序
- [ ] 理解 interface 的隐式满足
- [ ] 能用 goroutine + channel 写并发程序
- [ ] 能写一个 REST API（CRUD）
- [ ] 能连接数据库
- [ ] Flutter 前端 + Go 后端联调成功
