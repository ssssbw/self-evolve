# 备忘录模式（Memento）

## 一句话

在不破坏封装的前提下，捕获对象的内部状态，以便之后恢复。

## Dart 代码

```dart
class Memento {
  final String state;
  Memento(this.state);
}

class Originator {
  String state;
  Originator(this.state);

  Memento save() => Memento(state);
  void restore(Memento m) => state = m.state;
}

class CareTaker {
  final List<Memento> _history = [];
  void save(Memento m) => _history.add(m);
  Memento? undo() => _history.isNotEmpty ? _history.removeLast() : null;
}

void main() {
  final origin = Originator('状态A');
  final care = CareTaker();

  care.save(origin.save()); // 保存 A
  origin.state = '状态B';
  care.save(origin.save()); // 保存 B
  origin.state = '状态C';

  print(origin.state); // 状态C
  origin.restore(care.undo()!);
  print(origin.state); // 状态B
  origin.restore(care.undo()!);
  print(origin.state); // 状态A
}
```

## Go 代码

```go
package memento

type Memento struct{ State string }
type Originator struct{ State string }
func (o *Originator) Save() *Memento       { return &Memento{State: o.State} }
func (o *Originator) Restore(m *Memento)   { o.State = m.State }

type CareTaker struct{ history []*Memento }
func (c *CareTaker) Save(m *Memento)        { c.history = append(c.history, m) }
func (c *CareTaker) Undo() *Memento {
	if len(c.history) == 0 { return nil }
	m := c.history[len(c.history)-1]
	c.history = c.history[:len(c.history)-1]
	return m
}
```

## Flutter 中的真实应用

- **表单保存草稿**：用户填到一半离开，下次恢复
- **State Restoration**：Android 的状态恢复机制（Activity 被系统销毁后恢复）
- **Ctrl+Z**：文本编辑器的撤销功能

## 什么时候用 / 不用

- 用：需要保存/恢复状态、实现撤销功能
- 不用：状态很简单，直接保存变量即可
