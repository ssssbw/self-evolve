# 建造者模式（Builder）

## 一句话

分步构建复杂对象，将构造过程与表示分离。同样的构建过程可以创建不同的表示。

## 问题场景

一个对话框有很多可选参数（标题、内容、按钮、图标、动画、圆角...）。如果用构造函数传参，参数列表会非常长，而且大部分时候你只需要其中几个。

## 解决方案

用链式调用逐步设置参数，最后调用 `build()` 生成最终对象。

## Dart 代码

```dart
// 产品
class DialogConfig {
  final String? title;
  final String? content;
  final List<String> actions;
  final String? icon;
  final double? borderRadius;
  final bool dismissible;

  DialogConfig({
    this.title,
    this.content,
    this.actions = const [],
    this.icon,
    this.borderRadius,
    this.dismissible = true,
  });
}

// 建造者
class DialogBuilder {
  String? _title;
  String? _content;
  List<String> _actions = [];
  String? _icon;
  double? _borderRadius;
  bool _dismissible = true;

  DialogBuilder setTitle(String title) {
    _title = title;
    return this;
  }

  DialogBuilder setContent(String content) {
    _content = content;
    return this;
  }

  DialogBuilder addAction(String action) {
    _actions = [..._actions, action];
    return this;
  }

  DialogBuilder setIcon(String icon) {
    _icon = icon;
    return this;
  }

  DialogBuilder setBorderRadius(double radius) {
    _borderRadius = radius;
    return this;
  }

  DialogBuilder setDismissible(bool dismissible) {
    _dismissible = dismissible;
    return this;
  }

  DialogConfig build() {
    return DialogConfig(
      title: _title,
      content: _content,
      actions: _actions,
      icon: _icon,
      borderRadius: _borderRadius,
      dismissible: _dismissible,
    );
  }
}

// 使用
void main() {
  final dialog = DialogBuilder()
      .setTitle('确认删除')
      .setContent('此操作不可撤销')
      .addAction('取消')
      .addAction('删除')
      .setBorderRadius(12)
      .setDismissible(false)
      .build();

  print('标题: ${dialog.title}');
  print('按钮: ${dialog.actions}');
}
```

## Go 代码

```go
package builder

// 产品
type DialogConfig struct {
	Title         string
	Content       string
	Actions       []string
	Icon          string
	BorderRadius  float64
	Dismissible   bool
}

// 建造者
type DialogBuilder struct {
	config DialogConfig
}

func NewDialogBuilder() *DialogBuilder {
	return &DialogBuilder{
		config: DialogConfig{
			Dismissible: true,
		},
	}
}

func (b *DialogBuilder) SetTitle(title string) *DialogBuilder {
	b.config.Title = title
	return b
}

func (b *DialogBuilder) SetContent(content string) *DialogBuilder {
	b.config.Content = content
	return b
}

func (b *DialogBuilder) AddAction(action string) *DialogBuilder {
	b.config.Actions = append(b.config.Actions, action)
	return b
}

func (b *DialogBuilder) SetBorderRadius(radius float64) *DialogBuilder {
	b.config.BorderRadius = radius
	return b
}

func (b *DialogBuilder) SetDismissible(dismissible bool) *DialogBuilder {
	b.config.Dismissible = dismissible
	return b
}

func (b *DialogBuilder) Build() *DialogConfig {
	return &b.config
}

// 使用
// dialog := NewDialogBuilder().
//     SetTitle("确认删除").
//     SetContent("此操作不可撤销").
//     AddAction("取消").
//     AddAction("删除").
//     SetDismissible(false).
//     Build()
```

## Flutter 中的真实应用

- `AlertDialog` 的属性就是建造者模式的体现——你选择性设置 title、content、actions
- `ListView.builder` —— 按需构建列表项
- `Dio` 的 `Options` —— 链式设置请求头、超时、回调

## 什么时候用

- 对象有很多可选参数
- 需要分步构建复杂对象
- 想让构造过程可读性更好（链式调用）

## 什么时候不用

- 对象简单、参数少——直接用构造函数
- 参数都是必填的——用构造函数更明确

## 与其他模式的关系

- 建造者关注"分步构建"，**抽象工厂**关注"创建产品族"
- 建造者通常返回最终产品，中间状态对外不可见
- Go 中建造者用结构体+方法链实现，不需要接口（和 Java 不同）
