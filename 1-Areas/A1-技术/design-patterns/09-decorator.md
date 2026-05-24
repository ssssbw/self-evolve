# 装饰器模式（Decorator）

## 一句话

动态地给对象添加额外职责，而不改变其结构。比继承更灵活的扩展方式。

## 问题场景

一个咖啡订单系统：基础咖啡可以加牛奶、摩卡、奶油等。如果用继承，每种组合都是一个子类（EspressoWithMilk、EspressoWithMocha、EspressoWithMilkAndMocha...），类爆炸。

## Dart 代码

```dart
// 组件接口
abstract class Coffee {
  String getDescription();
  double getCost();
}

// 基础组件
class Espresso implements Coffee {
  @override
  String getDescription() => 'Espresso';
  @override
  double getCost() => 15.0;
}

class HouseBlend implements Coffee {
  @override
  String getDescription() => 'House Blend';
  @override
  double getCost() => 12.0;
}

// 装饰器基类
abstract class CoffeeDecorator implements Coffee {
  final Coffee _coffee;
  CoffeeDecorator(this._coffee);
}

// 具体装饰器
class Milk extends CoffeeDecorator {
  Milk(Coffee coffee) : super(coffee);

  @override
  String getDescription() => '${_coffee.getDescription()}, Milk';
  @override
  double getCost() => _coffee.getCost() + 3.0;
}

class Mocha extends CoffeeDecorator {
  Mocha(Coffee coffee) : super(coffee);

  @override
  String getDescription() => '${_coffee.getDescription()}, Mocha';
  @override
  double getCost() => _coffee.getCost() + 4.0;
}

class Whip extends CoffeeDecorator {
  Whip(Coffee coffee) : super(coffee);

  @override
  String getDescription() => '${_coffee.getDescription()}, Whip';
  @override
  double getCost() => _coffee.getCost() + 2.0;
}

// 使用：层层包装
void main() {
  Coffee coffee = Espresso();
  coffee = Milk(coffee);
  coffee = Mocha(coffee);
  coffee = Whip(coffee);

  print('${coffee.getDescription()} = ${coffee.getCost()}元');
  // Espresso, Milk, Mocha, Whip = 24.0元
}
```

## Go 代码

```go
package decorator

import "fmt"

// 组件接口
type Coffee interface {
	GetDescription() string
	GetCost() float64
}

// 基础组件
type Espresso struct{}

func (e *Espresso) GetDescription() string { return "Espresso" }
func (e *Espresso) GetCost() float64       { return 15.0 }

type HouseBlend struct{}

func (h *HouseBlend) GetDescription() string { return "House Blend" }
func (h *HouseBlend) GetCost() float64       { return 12.0 }

// 装饰器
type MilkDecorator struct {
	coffee Coffee
}

func (d *MilkDecorator) GetDescription() string {
	return d.coffee.GetDescription() + ", Milk"
}
func (d *MilkDecorator) GetCost() float64 { return d.coffee.GetCost() + 3.0 }

type MochaDecorator struct {
	coffee Coffee
}

func (d *MochaDecorator) GetDescription() string {
	return d.coffee.GetDescription() + ", Mocha"
}
func (d *MochaDecorator) GetCost() float64 { return d.coffee.GetCost() + 4.0 }

// 使用
// var coffee Coffee = &Espresso{}
// coffee = &MilkDecorator{coffee: coffee}
// coffee = &MochaDecorator{coffee: coffee}
// fmt.Printf("%s = %.0f元\n", coffee.GetDescription(), coffee.GetCost())
```

## Flutter 中的真实应用

- **Container** 就是最常用的装饰器——在不改变 child 的前提下，包装 padding、decoration、margin、constraints 等行为
- **Padding、SizedBox、DecoratedBox** 都是装饰器——包装 child 并添加行为
- 整个 Widget 树就是层层装饰：`Scaffold > Container > Padding > Card > Text`

## 什么时候用

- 需要动态添加/组合功能
- 用继承会导致类爆炸
- 功能可以任意组合

## 什么时候不用

- 只有一种固定组合——直接用继承更简单
- 装饰层数太多影响性能

## 与其他模式的关系

- 装饰器和**组合**结构相似，但装饰器只包装一个对象（不是集合）
- 装饰器是**代理**的变体——都包装对象，但装饰器重在"增加行为"，代理重在"控制访问"
