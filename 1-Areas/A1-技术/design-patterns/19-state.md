# 状态模式（State）

## 一句话

允许对象在内部状态改变时改变行为，看起来像改变了类。

## Dart 代码

```dart
abstract class ConnectionState {
  void connect(Context ctx);
  void disconnect(Context ctx);
  void send(Context ctx, String data);
}

class Disconnected implements ConnectionState {
  @override
  void connect(Context ctx) {
    print('连接中...');
    ctx.state = Connected();
  }
  @override
  void disconnect(Context ctx) => print('已经断开了');
  @override
  void send(Context ctx, String data) => print('错误: 未连接');
}

class Connected implements ConnectionState {
  @override
  void connect(Context ctx) => print('已经连接了');
  @override
  void disconnect(Context ctx) {
    print('断开连接');
    ctx.state = Disconnected();
  }
  @override
  void send(Context ctx, String data) => print('发送: $data');
}

class Context {
  ConnectionState state;
  Context() : state = Disconnected();
  void connect() => state.connect(this);
  void disconnect() => state.disconnect(this);
  void send(String data) => state.send(this, data);
}

void main() {
  final conn = Context();
  conn.send('hello');   // 错误: 未连接
  conn.connect();        // 连接中...
  conn.send('hello');   // 发送: hello
  conn.disconnect();     // 断开连接
}
```

## Go 代码

```go
package state

import "fmt"

type Context struct{ state ConnectionState }

type ConnectionState interface {
	Connect(ctx *Context)
	Disconnect(ctx *Context)
	Send(ctx *Context, data string)
}

type Disconnected struct{}
func (s *Disconnected) Connect(ctx *Context)    { fmt.Println("连接中..."); ctx.state = &Connected{} }
func (s *Disconnected) Disconnect(ctx *Context) { fmt.Println("已经断开了") }
func (s *Disconnected) Send(ctx *Context, data string) { fmt.Println("错误: 未连接") }

type Connected struct{}
func (s *Connected) Connect(ctx *Context)    { fmt.Println("已经连接了") }
func (s *Connected) Disconnect(ctx *Context) { fmt.Println("断开连接"); ctx.state = &Disconnected{} }
func (s *Connected) Send(ctx *Context, data string) { fmt.Println("发送:", data) }
```

## Flutter 中的真实应用

- **StatefulWidget + State** — 名字直白。State 对象持有状态，状态变化改变渲染输出
- **网络请求状态**：Loading / Success / Error 三种状态切换不同的 UI

## 什么时候用 / 不用

- 用：对象行为随状态变化，且状态种类多；用大量 if-else 判断状态
- 不用：只有 1-2 种状态，if-else 更清晰
