# 桥接模式（Bridge）

## 一句话

将抽象部分与实现部分分离，使它们都可以独立变化。

## 问题场景

你有一个消息通知系统，需要支持多种通知类型（邮件、短信、推送）和多种紧急程度（普通、重要、紧急）。如果用继承，需要 3×3=9 个子类。加一种通知类型就要加 3 个子类。

## 解决方案

把"通知方式"和"紧急程度"拆成两个独立的维度，通过组合而非继承关联。

## Dart 代码

```dart
// 实现接口——通知渠道
abstract class NotificationSender {
  void send(String message);
}

class EmailSender implements NotificationSender {
  @override
  void send(String message) => print('邮件发送: $message');
}

class SmsSender implements NotificationSender {
  @override
  void send(String message) => print('短信发送: $message');
}

class PushSender implements NotificationSender {
  @override
  void send(String message) => print('推送发送: $message');
}

// 抽象——通知类型（持有 Sender 引用）
abstract class Notification {
  final NotificationSender sender;
  Notification(this.sender);

  void notify(String message);
}

class NormalNotification extends Notification {
  NormalNotification(NotificationSender sender) : super(sender);

  @override
  void notify(String message) {
    sender.send('[普通] $message');
  }
}

class UrgentNotification extends Notification {
  UrgentNotification(NotificationSender sender) : super(sender);

  @override
  void notify(String message) {
    sender.send('[紧急] $message');
  }
}

// 使用：任意组合，不需要 9 个子类
void main() {
  Notification n1 = NormalNotification(EmailSender());
  n1.notify('系统更新完成');

  Notification n2 = UrgentNotification(SmsSender());
  n2.notify('服务器异常！');
}
```

## Go 代码

```go
package bridge

import "fmt"

// 实现接口
type Sender interface {
	Send(message string)
}

type EmailSender struct{}
func (s *EmailSender) Send(message string) { fmt.Printf("邮件发送: %s\n", message) }

type SmsSender struct{}
func (s *SmsSender) Send(message string) { fmt.Printf("短信发送: %s\n", message) }

// 抽象
type Notification struct {
	sender Sender
}

func (n *Notification) Notify(message, level string) {
	fullMessage := fmt.Sprintf("[%s] %s", level, message)
	n.sender.Send(fullMessage)
}

// 使用
// n := &Notification{sender: &EmailSender{}}
// n.Notify("系统更新", "普通")
```

## Flutter 中的真实应用

- Flutter 的 `RenderObject` 体系：Widget（抽象）和 RenderObject（实现）是桥接关系
- 平台插件中，Dart 层（抽象）和 Native 层（实现）通过 MethodChannel 桥接

## 什么时候用

- 两个维度独立变化（如通知方式 × 紧急程度）
- 继承导致类爆炸
- 需要在运行时切换实现

## 什么时候不用

- 只有一个变化维度
- 类的数量可控

## 与其他模式的关系

- 桥接在设计初期使用（结构设计），**适配器**在后期使用（兼容已有代码）
- 桥接强调"分离维度"，**策略**强调"替换算法"
