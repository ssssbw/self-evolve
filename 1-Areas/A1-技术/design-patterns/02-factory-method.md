# 工厂方法模式（Factory Method）

## 一句话

定义一个创建对象的接口，让子类决定实例化哪个类。将"创建"和"使用"解耦。

## 问题场景

你的 App 需要支持 iOS 和 Material 两种风格的对话框。如果直接在代码里 `if (platform == iOS) ... else ...`，每新增一个平台就要改所有相关代码。

## 解决方案

定义一个创建者接口，让不同平台各自实现创建方法。调用者只关心接口，不关心具体类型。

## Dart 代码

```dart
// 产品接口
abstract class Dialog {
  void show();
  String getTitle();
}

// 具体产品 A
class IOSDialog implements Dialog {
  @override
  void show() => print('显示 iOS 风格对话框: ${getTitle()}');

  @override
  String getTitle() => 'iOS Alert';
}

// 具体产品 B
class MaterialDialog implements Dialog {
  @override
  void show() => print('显示 Material 风格对话框: ${getTitle()}');

  @override
  String getTitle() => 'Material Dialog';
}

// 创建者
abstract class DialogCreator {
  // 工厂方法——子类实现
  Dialog createDialog();

  // 业务逻辑可以复用
  void showDialog() {
    final dialog = createDialog();
    dialog.show();
  }
}

// 具体创建者
class IOSDialogCreator extends DialogCreator {
  @override
  Dialog createDialog() => IOSDialog();
}

class MaterialDialogCreator extends DialogCreator {
  @override
  Dialog createDialog() => MaterialDialog();
}

// 使用
void main() {
  DialogCreator creator = IOSDialogCreator();
  creator.showDialog(); // 显示 iOS 风格对话框

  creator = MaterialDialogCreator();
  creator.showDialog(); // 显示 Material 风格对话框
}
```

## Go 代码

```go
package factory

import "fmt"

// 产品接口
type Dialog interface {
	Show()
	GetTitle() string
}

// 具体产品 A
type IOSDialog struct{}

func (d *IOSDialog) Show() {
	fmt.Printf("显示 iOS 风格对话框: %s\n", d.GetTitle())
}
func (d *IOSDialog) GetTitle() string { return "iOS Alert" }

// 具体产品 B
type MaterialDialog struct{}

func (d *MaterialDialog) Show() {
	fmt.Printf("显示 Material 风格对话框: %s\n", d.GetTitle())
}
func (d *MaterialDialog) GetTitle() string { return "Material Dialog" }

// 创建者接口
type DialogCreator interface {
	CreateDialog() Dialog
}

// 具体创建者
type IOSDialogCreator struct{}

func (c *IOSDialogCreator) CreateDialog() Dialog { return &IOSDialog{} }

type MaterialDialogCreator struct{}

func (c *MaterialDialogCreator) CreateDialog() Dialog { return &MaterialDialog{} }

// 使用
// var creator DialogCreator = &IOSDialogCreator{}
// dialog := creator.CreateDialog()
// dialog.Show()
```

## Flutter 中的真实应用

- `StatefulWidget.createState()` — 框架调用此方法创建 State，具体创建什么由你的 Widget 决定
- `ThemeData.light()` / `ThemeData.dark()` — 工厂构造函数，根据需要创建不同主题
- `MaterialPageRoute` — 创建 Material 风格的路由页面

## 什么时候用

- 不预先知道需要创建哪种具体对象
- 想让框架/库的用户扩展创建逻辑
- 需要复用创建对象的逻辑

## 什么时候不用

- 只有一种产品类型时，直接构造即可
- 产品创建逻辑非常简单时，不需要额外抽象

## 与其他模式的关系

- 工厂方法是**抽象工厂**的简化版（只创建一种产品）
- 常和**模板方法**结合：创建者在工厂方法外定义业务骨架
- Go 中常用函数类型替代创建者接口（`type DialogFactory func() Dialog`）
