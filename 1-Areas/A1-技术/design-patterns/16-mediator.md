# 中介者模式（Mediator）

## 一句话

用一个中介对象封装一系列对象间的交互，使对象之间不需要显式相互引用。

## Dart 代码

```dart
// 中介者
class ChatRoom {
  static void showMessage(User user, String message) {
    print('${DateTime.now()} [${user.name}]: $message');
  }
}

class User {
  final String name;
  User(this.name);

  void send(String message) => ChatRoom.showMessage(this, message);
}

void main() {
  final alice = User('Alice');
  final bob = User('Bob');
  alice.send('你好 Bob!');
  bob.send('你好 Alice!');
  // User 之间不直接引用，通过 ChatRoom 中介
}
```

## Go 代码

```go
package mediator

import "fmt"
import "time"

type ChatRoom struct{}
func (c *ChatRoom) ShowMessage(name, message string) {
	fmt.Printf("%v [%s]: %s\n", time.Now().Format("15:04:05"), name, message)
}

type User struct {
	name     string
	chatRoom *ChatRoom
}

func (u *User) Send(message string) { u.chatRoom.ShowMessage(u.name, message) }

// 使用
// room := &ChatRoom{}
// alice := &User{name: "Alice", chatRoom: room}
// bob := &User{name: "Bob", chatRoom: room}
// alice.Send("你好!")
```

## Flutter 中的真实应用

- **InheritedWidget**：中介 Widget 树中祖先和后代之间的通信
- **EventBus**：事件总线就是中介者——发布者和订阅者不直接引用

## 什么时候用 / 不用

- 用：多个对象之间有复杂的引用关系（网状变星状）
- 不用：对象交互简单，引入中介者反而增加复杂度
