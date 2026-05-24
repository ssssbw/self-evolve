# 责任链模式（Chain of Responsibility）

## 一句话

将请求沿处理者链传递，每个处理者决定是否处理或传递给下一个。

## Dart 代码

```dart
abstract class Handler {
  Handler? next;
  Handler setNext(Handler h) { next = h; return h; }
  void handle(String request);
}

class AuthHandler extends Handler {
  @override
  void handle(String request) {
    if (request == 'auth') {
      print('AuthHandler: 处理认证');
    } else {
      print('AuthHandler: 传递给下一个');
      next?.handle(request);
    }
  }
}

class LogHandler extends Handler {
  @override
  void handle(String request) {
    if (request == 'log') {
      print('LogHandler: 处理日志');
    } else {
      next?.handle(request);
    }
  }
}

class ErrorHandler extends Handler {
  @override
  void handle(String request) {
    print('ErrorHandler: 兜底处理 [$request]');
  }
}

// 使用
void main() {
  final auth = AuthHandler();
  final log = LogHandler();
  final error = ErrorHandler();
  auth.setNext(log)..setNext(error);
  auth.handle('log');    // LogHandler 处理
  auth.handle('unknown'); // ErrorHandler 兜底
}
```

## Go 代码

```go
package chain

type Handler interface {
	SetNext(Handler) Handler
	Handle(request string)
}

type BaseHandler struct{ next Handler }
func (h *BaseHandler) SetNext(n Handler) Handler { h.next = n; return n }
func (h *BaseHandler) Next(request string)       { h.next.Handle(request) }

type AuthHandler struct{ BaseHandler }
func (h *AuthHandler) Handle(request string) {
	if request == "auth" {
		println("AuthHandler: 处理认证")
	} else {
		println("AuthHandler: 传递")
		h.Next(request)
	}
}

type ErrorHandler struct{ BaseHandler }
func (h *ErrorHandler) Handle(request string) {
	println("ErrorHandler: 兜底处理", request)
}
```

## Flutter 中的真实应用

- **手势识别的 Hit Test**：事件从外到内逐层传递，每一层决定是否消费
- **中间件链**：Dart Shelf / Express 风格的中间件就是责任链

## 什么时候用 / 不用

- 用：多个处理者可能处理同一请求；处理顺序重要
- 不用：请求只有一个明确的处理者
