# 观察者模式（Observer）

## 一句话

定义对象间一对多的依赖关系，当一个对象状态改变时，所有依赖者自动收到通知。

## Dart 代码

```dart
// 不依赖 Flutter SDK 的纯 Dart 实现
abstract class Observer {
  void update(String message);
}

class Subject {
  final List<Observer> _observers = [];

  void attach(Observer o) => _observers.add(o);
  void detach(Observer o) => _observers.remove(o);
  void notify(String message) {
    for (final o in _observers) {
      o.update(message);
    }
  }
}

class EmailNotifier implements Observer {
  @override
  void update(String message) => print('邮件通知: $message');
}

class PushNotifier implements Observer {
  @override
  void update(String message) => print('推送通知: $message');
}

void main() {
  final subject = Subject();
  subject.attach(EmailNotifier());
  subject.attach(PushNotifier());
  subject.notify('CSAPP 第 1 章学完了！');
  // 邮件通知: CSAPP 第 1 章学完了！
  // 推送通知: CSAPP 第 1 章学完了！
}
```

## Go 代码

```go
package observer

import "fmt"

type Observer interface {
	Update(message string)
}

type Subject struct {
	observers []Observer
}

func (s *Subject) Attach(o Observer)   { s.observers = append(s.observers, o) }
func (s *Subject) Detach(o Observer) {
	for i, obs := range s.observers {
		if obs == o {
			s.observers = append(s.observers[:i], s.observers[i+1:]...)
			break
		}
	}
}
func (s *Subject) Notify(message string) {
	for _, o := range s.observers {
		o.Update(message)
	}
}

type EmailNotifier struct{}
func (e *EmailNotifier) Update(message string) { fmt.Printf("邮件通知: %s\n", message) }

type PushNotifier struct{}
func (p *PushNotifier) Update(message string) { fmt.Printf("推送通知: %s\n", message) }
```

## Flutter 中的真实应用

- **ChangeNotifier** + **ValueNotifier** — Flutter 状态管理的根基
- **Stream** / **StreamController** — Dart 的异步观察者
- **Provider/Riverpod/Bloc** — 都基于观察者模式构建

## 什么时候用 / 不用

- 用：一个对象变化需要通知多个其他对象；事件驱动架构
- 不用：一对一的简单依赖，直接调用即可

## 与其他模式的关系

- 观察者是 Flutter 开发者**最需要掌握**的模式
- 和**中介者**的区别：观察者是"一对多通知"，中介者是"多对多协调"
- Go 中常用 channel 替代观察者
