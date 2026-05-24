# 代理模式（Proxy）

## 一句话

为另一个对象提供替身或占位符，以控制对这个对象的访问。

## 问题场景

你有一个从网络加载的大图片。如果直接加载，用户要等很久。你需要一个"替身"——先显示占位图，后台加载，加载完后替换。

## Dart 代码

```dart
// 接口
abstract class Image {
  void display();
}

// 真实对象——加载成本高
class RealImage implements Image {
  final String filename;

  RealImage(this.filename) {
    _loadFromDisk();
  }

  void _loadFromDisk() {
    print('从磁盘加载: $filename ...（耗时操作）');
  }

  @override
  void display() => print('显示图片: $filename');
}

// 代理——控制访问
class ImageProxy implements Image {
  final String filename;
  RealImage? _realImage;

  ImageProxy(this.filename);

  @override
  void display() {
    // 延迟加载——只有真正需要时才创建真实对象
    _realImage ??= RealImage(filename);
    _realImage!.display();
  }
}

// 使用
void main() {
  print('创建代理（不加载图片）...');
  final image = ImageProxy('photo.jpg');

  print('第一次 display（才真正加载）:');
  image.display();

  print('第二次 display（不再加载）:');
  image.display();
}
```

## Go 代码

```go
package proxy

import "fmt"

// 接口
type Image interface {
	Display()
}

// 真实对象
type RealImage struct {
	filename string
}

func NewRealImage(filename string) *RealImage {
	img := &RealImage{filename: filename}
	img.loadFromDisk()
	return img
}

func (r *RealImage) loadFromDisk() {
	fmt.Printf("从磁盘加载: %s ...\n", r.filename)
}
func (r *RealImage) Display() {
	fmt.Printf("显示图片: %s\n", r.filename)
}

// 代理
type ImageProxy struct {
	filename  string
	realImage *RealImage
}

func NewImageProxy(filename string) *ImageProxy {
	return &ImageProxy{filename: filename}
}

func (p *ImageProxy) Display() {
	if p.realImage == nil {
		p.realImage = NewRealImage(p.filename)
	}
	p.realImage.Display()
}
```

## Flutter 中的真实应用

- **Proxy** Widget — 名字就是 Proxy，在 Widget 树中代理数据给子树
- **InheritedWidget** — 代理数据的访问，子树不需要直接引用数据源
- **Image.network** 的缓存机制 — 代理图片加载过程，缓存已加载的图片

## 什么时候用

- 延迟初始化（虚拟代理）
- 访问控制（保护代理）
- 远程访问（远程代理，如 RPC）
- 缓存（缓存代理）
- 日志记录（智能代理）

## 什么时候不用

- 直接访问没有额外成本
- 不需要任何控制逻辑

## 与其他模式的关系

- 代理和**装饰器**结构相同，但目的不同：代理控制访问，装饰器增加行为
- 代理和**适配器**的区别：代理实现相同接口，适配器转换接口
- **Flutter 的 Proxy Widget** 名字直白——它就是代理模式
