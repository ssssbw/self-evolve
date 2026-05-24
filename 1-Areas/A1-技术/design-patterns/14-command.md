# 命令模式（Command）

## 一句话

将请求封装为对象，支持参数化、排队、记录日志和撤销操作。

## Dart 代码

```dart
abstract class Command {
  void execute();
  void undo();
}

class Light {
  void on() => print('灯开了');
  void off() => print('灯关了');
}

class LightOnCommand implements Command {
  final Light light;
  LightOnCommand(this.light);
  @override void execute() => light.on();
  @override void undo() => light.off();
}

class LightOffCommand implements Command {
  final Light light;
  LightOffCommand(this.light);
  @override void execute() => light.off();
  @override void undo() => light.on();
}

class RemoteControl {
  final List<Command> _history = [];
  void execute(Command cmd) { cmd.execute(); _history.add(cmd); }
  void undo() { if (_history.isNotEmpty) _history.removeLast().undo(); }
}

void main() {
  final remote = RemoteControl();
  final light = Light();
  remote.execute(LightOnCommand(light));  // 灯开了
  remote.execute(LightOffCommand(light)); // 灯关了
  remote.undo(); // 灯开了（撤销关灯）
}
```

## Go 代码

```go
package command

type Command interface {
	Execute()
	Undo()
}

type Light struct{}
func (l *Light) On()  { println("灯开了") }
func (l *Light) Off() { println("灯关了") }

type LightOnCommand struct{ light *Light }
func (c *LightOnCommand) Execute() { c.light.On() }
func (c *LightOnCommand) Undo()    { c.light.Off() }

type LightOffCommand struct{ light *Light }
func (c *LightOffCommand) Execute() { c.light.Off() }
func (c *LightOffCommand) Undo()    { c.light.On() }

type RemoteControl struct{ history []Command }
func (r *RemoteControl) Execute(cmd Command) { cmd.Execute(); r.history = append(r.history, cmd) }
func (r *RemoteControl) Undo() {
	if len(r.history) > 0 {
		cmd := r.history[len(r.history)-1]
		r.history = r.history[:len(r.history)-1]
		cmd.Undo()
	}
}
```

## Flutter 中的真实应用

- **Actions/Intents** 系统：将用户操作（Intent）封装为可执行对象（Action）
- **undo/redo** 功能：文本编辑器的撤销重做

## 什么时候用 / 不用

- 用：需要撤销/重做、排队执行、记录日志
- 不用：操作简单且不需要撤销
