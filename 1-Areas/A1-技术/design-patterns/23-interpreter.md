# 解释器模式（Interpreter）

## 一句话

定义一种语言的文法表示，并定义一个解释器来解释该语言中的句子。

## Dart 代码

```dart
// 简单的表达式解释器：支持 "5 + 3 - 2" 这样的算术表达式
abstract class Expression {
  int interpret();
}

class Number implements Expression {
  final int value;
  Number(this.value);
  @override
  int interpret() => value;
}

class Add implements Expression {
  final Expression left, right;
  Add(this.left, this.right);
  @override
  int interpret() => left.interpret() + right.interpret();
}

class Subtract implements Expression {
  final Expression left, right;
  Subtract(this.left, this.right);
  @override
  int interpret() => left.interpret() - right.interpret();
}

void main() {
  // (5 + 3) - 2
  final expr = Subtract(Add(Number(5), Number(3)), Number(2));
  print(expr.interpret()); // 6
}
```

## Go 代码

```go
package interpreter

type Expression interface {
	Interpret() int
}

type Number struct{ Value int }
func (n *Number) Interpret() int { return n.Value }

type Add struct{ Left, Right Expression }
func (a *Add) Interpret() int { return a.Left.Interpret() + a.Right.Interpret() }

type Subtract struct{ Left, Right Expression }
func (s *Subtract) Interpret() int { return s.Left.Interpret() - s.Right.Interpret() }

// 使用
// expr := &Subtract{Left: &Add{Left: &Number{5}, Right: &Number{3}}, Right: &Number{2}}
// fmt.Println(expr.Interpret()) // 6
```

## Flutter/Dart 中的真实应用

- **Dart 的表达式求值**：debugger 中的表达式求值
- **正则表达式**：RegExp 就是解释器模式
- **SQL 解析**、**配置文件解析**：任何需要解析"小语言"的场景

## 什么时候用 / 不用

- 用：需要解析和执行特定格式的表达式/命令；简单的 DSL
- 不用：语法复杂（用解析器生成器如 ANTLR）；性能敏感场景
