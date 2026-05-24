# 抽象工厂模式（Abstract Factory）

## 一句话

创建一组相关或相互依赖的对象，而不指定具体类。是工厂方法的升级版——一次创建一整套。

## 问题场景

你的 App 支持亮色和暗色主题。切换主题时，Button、Card、AppBar 的样式要同时变。如果每种控件单独创建，很容易漏掉某个或风格不统一。

## 解决方案

定义一个"主题工厂"接口，一次性提供该主题下的所有控件样式。切换主题只需切换工厂。

## Dart 代码

```dart
// 产品族接口
abstract class ButtonStyle {
  String get color;
  String get borderRadius;
}

abstract class CardStyle {
  String get backgroundColor;
  String get shadow;
}

// 抽象工厂
abstract class ThemeFactory {
  ButtonStyle createButton();
  CardStyle createCard();
  String get themeName;
}

// 亮色主题产品族
class LightButton implements ButtonStyle {
  @override
  String get color => '#2196F3';
  @override
  String get borderRadius => '8';
}

class LightCard implements CardStyle {
  @override
  String get backgroundColor => '#FFFFFF';
  @override
  String get shadow => 'elevation=2';
}

class LightThemeFactory implements ThemeFactory {
  @override
  ButtonStyle createButton() => LightButton();
  @override
  CardStyle createCard() => LightCard();
  @override
  String get themeName => 'Light';
}

// 暗色主题产品族
class DarkButton implements ButtonStyle {
  @override
  String get color => '#BB86FC';
  @override
  String get borderRadius => '12';
}

class DarkCard implements CardStyle {
  @override
  String get backgroundColor => '#1E1E1E';
  @override
  String get shadow => 'elevation=0';
}

class DarkThemeFactory implements ThemeFactory {
  @override
  ButtonStyle createButton() => DarkButton();
  @override
  CardStyle createCard() => DarkCard();
  @override
  String get themeName => 'Dark';
}

// 使用
void main() {
  ThemeFactory factory = LightThemeFactory();
  final button = factory.createButton();
  final card = factory.createCard();
  print('主题: ${factory.themeName}');
  print('按钮颜色: ${button.color}');
  print('卡片背景: ${card.backgroundColor}');

  // 切换主题只需换工厂
  factory = DarkThemeFactory();
  // 所有控件自动切换
}
```

## Go 代码

```go
package abstractfactory

import "fmt"

// 产品接口
type ButtonStyle interface {
	Color() string
	BorderRadius() string
}

type CardStyle interface {
	BackgroundColor() string
	Shadow() string
}

// 抽象工厂
type ThemeFactory interface {
	CreateButton() ButtonStyle
	CreateCard() CardStyle
	ThemeName() string
}

// 亮色主题
type LightButton struct{}

func (b *LightButton) Color() string        { return "#2196F3" }
func (b *LightButton) BorderRadius() string { return "8" }

type LightCard struct{}

func (c *LightCard) BackgroundColor() string { return "#FFFFFF" }
func (c *LightCard) Shadow() string          { return "elevation=2" }

type LightThemeFactory struct{}

func (f *LightThemeFactory) CreateButton() ButtonStyle { return &LightButton{} }
func (f *LightThemeFactory) CreateCard() CardStyle     { return &LightCard{} }
func (f *LightThemeFactory) ThemeName() string         { return "Light" }

// 暗色主题
type DarkButton struct{}

func (b *DarkButton) Color() string        { return "#BB86FC" }
func (b *DarkButton) BorderRadius() string { return "12" }

type DarkCard struct{}

func (c *DarkCard) BackgroundColor() string { return "#1E1E1E" }
func (c *DarkCard) Shadow() string          { return "elevation=0" }

type DarkThemeFactory struct{}

func (f *DarkThemeFactory) CreateButton() ButtonStyle { return &DarkButton{} }
func (f *DarkThemeFactory) CreateCard() CardStyle     { return &DarkCard{} }
func (f *DarkThemeFactory) ThemeName() string         { return "Dark" }

// 使用
// var factory ThemeFactory = &LightThemeFactory{}
// button := factory.CreateButton()
// fmt.Println(button.Color())
```

## Flutter 中的真实应用

- `ThemeData` 就是抽象工厂的实际体现——它一次提供整套视觉配置（颜色、字体、形状、间距）
- `MaterialApp(theme: ThemeData.light(), darkTheme: ThemeData.dark())` — 切换工厂切换整套主题

## 什么时候用

- 需要创建一组相关的对象（产品族）
- 系统需要独立于产品的创建、组合和表示
- 需要在运行时切换整套配置

## 什么时候不用

- 只有一种产品，不需要产品族
- 产品之间的关系不紧密

## 与其他模式的关系

- 抽象工厂通常用**工厂方法**实现（每个创建方法就是一个工厂方法）
- 也可以用**原型模式**实现（克隆预配置的对象）
- 和**建造者**的区别：抽象工厂关注"创建产品族"，建造者关注"分步构建复杂对象"
