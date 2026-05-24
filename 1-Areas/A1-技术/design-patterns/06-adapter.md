# 适配器模式（Adapter）

## 一句话

将一个类的接口转换成客户端期望的另一个接口，让原本不兼容的类可以协同工作。

## 问题场景

你的 App 需要同时支持 iOS 和 Android 的分享功能。iOS 用 `UIActivityViewController`，Android 用 `Intent.ACTION_SEND`。接口完全不同，但你的业务代码不想关心平台差异。

## Dart 代码

```dart
// 目标接口——你的业务代码只关心这个
abstract class Sharer {
  void share(String text);
}

// 被适配者 A（iOS 风格）
class IOSShareService {
  void presentActivitySheet(String content) {
    print('iOS: 展示 Activity Sheet -> $content');
  }
}

// 被适配者 B（Android 风格）
class AndroidShareService {
  void sendIntent(String data) {
    print('Android: 发送 Intent -> $data');
  }
}

// 适配器 A
class IOSSharerAdapter implements Sharer {
  final IOSShareService _service = IOSShareService();

  @override
  void share(String text) => _service.presentActivitySheet(text);
}

// 适配器 B
class AndroidSharerAdapter implements Sharer {
  final AndroidShareService _service = AndroidShareService();

  @override
  void share(String text) => _service.sendIntent(text);
}

// 使用
void main() {
  final Sharer sharer = IOSSharerAdapter(); // 或 AndroidSharerAdapter()
  sharer.share('学完适配器模式了！');
}
```

## Go 代码

```go
package adapter

import "fmt"

// 目标接口
type Sharer interface {
	Share(text string)
}

// 被适配者 A
type IOSShareService struct{}

func (s *IOSShareService) PresentActivitySheet(content string) {
	fmt.Printf("iOS: Activity Sheet -> %s\n", content)
}

// 被适配者 B
type AndroidShareService struct{}

func (s *AndroidShareService) SendIntent(data string) {
	fmt.Printf("Android: Intent -> %s\n", data)
}

// 适配器
type IOSSharerAdapter struct {
	service *IOSShareService
}

func NewIOSSharerAdapter() *IOSSharerAdapter {
	return &IOSSharerAdapter{service: &IOSShareService{}}
}

func (a *IOSSharerAdapter) Share(text string) {
	a.service.PresentActivitySheet(text)
}

type AndroidSharerAdapter struct {
	service *AndroidShareService
}

func NewAndroidSharerAdapter() *AndroidSharerAdapter {
	return &AndroidSharerAdapter{service: &AndroidShareService{}}
}

func (a *AndroidSharerAdapter) Share(text string) {
	a.service.SendIntent(text)
}
```

## Flutter 中的真实应用

- Flutter 的 Platform Interface 机制（如 `url_launcher`、`shared_preferences`）——每个平台一个适配器
- `Platform.isIOS` / `Platform.isAndroid` + 不同实现就是手动适配

## 什么时候用

- 需要复用已有类，但接口不匹配
- 需要统一多个不同接口
- 跨平台场景

## 什么时候不用

- 接口已经统一——不需要适配
- 可以直接修改被适配者的代码——改代码比包一层更简单

## 与其他模式的关系

- 适配器重在"接口转换"，**装饰器**重在"增加行为"
- **外观**简化接口，适配器转换接口
