# 访问者模式（Visitor）

## 一句话

在不改变各元素类的前提下，定义作用于这些元素的新操作。

## Dart 代码

```dart
// 元素接口
abstract class Shape {
  void accept(ShapeVisitor visitor);
}

class Circle implements Shape {
  final double radius;
  Circle(this.radius);
  @override
  void accept(ShapeVisitor visitor) => visitor.visitCircle(this);
}

class Rectangle implements Shape {
  final double width, height;
  Rectangle(this.width, this.height);
  @override
  void accept(ShapeVisitor visitor) => visitor.visitRectangle(this);
}

// 访问者接口
abstract class ShapeVisitor {
  void visitCircle(Circle circle);
  void visitRectangle(Rectangle rect);
}

// 具体访问者：计算面积
class AreaCalculator implements ShapeVisitor {
  @override
  void visitCircle(Circle c) => print('圆面积: ${3.14 * c.radius * c.radius}');

  @override
  void visitRectangle(Rectangle r) => print('矩形面积: ${r.width * r.height}');
}

// 具体访问者：绘制
class ShapeDrawer implements ShapeVisitor {
  @override
  void visitCircle(Circle c) => print('画一个半径 ${c.radius} 的圆');

  @override
  void visitRectangle(Rectangle r) => print('画一个 ${r.width}x${r.height} 的矩形');
}

void main() {
  final shapes = <Shape>[Circle(5), Rectangle(3, 4)];

  print('计算面积:');
  for (final s in shapes) { s.accept(AreaCalculator()); }

  print('绘制:');
  for (final s in shapes) { s.accept(ShapeDrawer()); }
}
```

## Go 代码

```go
package visitor

import "fmt"

type Visitor interface {
	VisitCircle(c *Circle)
	VisitRectangle(r *Rectangle)
}

type Shape interface {
	Accept(v Visitor)
}

type Circle struct{ Radius float64 }
func (c *Circle) Accept(v Visitor) { v.VisitCircle(c) }

type Rectangle struct{ Width, Height float64 }
func (r *Rectangle) Accept(v Visitor) { v.VisitRectangle(r) }

type AreaCalculator struct{}
func (a *AreaCalculator) VisitCircle(c *Circle) {
	fmt.Printf("圆面积: %.2f\n", 3.14*c.Radius*c.Radius)
}
func (a *AreaCalculator) VisitRectangle(r *Rectangle) {
	fmt.Printf("矩形面积: %.2f\n", r.Width*r.Height)
}
```

## Flutter 中的真实应用

- **Widget 树遍历**：`context.findAncestorWidgetOfExactType<T>()` 类似于在树中做访问
- **AST 遍历**：Dart 的代码分析工具（analyzer）用访问者模式遍历语法树

## 什么时候用 / 不用

- 用：需要对一组不同类型的对象执行多种不同操作；操作经常新增但类型稳定
- 不用：类型经常变化；操作简单且稳定
