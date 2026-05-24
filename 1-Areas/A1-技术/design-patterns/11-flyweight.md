# 享元模式（Flyweight）

## 一句话

通过共享对象来最小化内存使用，适用于大量相似对象的场景。

## 问题场景

一个地图 App 需要在地图上显示 10000 个图标，每个图标有图标类型、颜色、大小（共享）和坐标（不共享）。如果每个图标都创建一个完整对象，内存会爆炸。

## Dart 代码

```dart
// 享元——共享部分
class IconStyle {
  final String icon;
  final String color;
  final int size;

  const IconStyle({required this.icon, required this.color, required this.size});

  @override
  String toString() => '$icon($color, ${size}px)';
}

// 享元工厂
class IconStyleFactory {
  static final Map<String, IconStyle> _cache = {};

  static IconStyle getStyle(String icon, String color, int size) {
    final key = '$icon-$color-$size';
    return _cache.putIfAbsent(key, () => IconStyle(icon: icon, color: color, size: size));
  }

  static int get cacheSize => _cache.length;
}

// 上下文——不共享部分
class MapMarker {
  final double x;
  final double y;
  final IconStyle style; // 共享的享元

  MapMarker({required this.x, required this.y, required this.style});

  @override
  String toString() => 'Marker($x, $y) $style';
}

// 使用
void main() {
  // 10000 个 marker，但只有 3 种样式
  final markers = <MapMarker>[];
  for (int i = 0; i < 10000; i++) {
    final style = IconStyleFactory.getStyle(
      ['restaurant', 'gas_station', 'hotel'][i % 3],
      ['red', 'blue', 'green'][i % 3],
      24,
    );
    markers.add(MapMarker(x: i * 0.001, y: i * 0.002, style: style));
  }

  print('标记数量: ${markers.length}');       // 10000
  print('样式对象数: ${IconStyleFactory.cacheSize}'); // 3（共享！）
}
```

## Go 代码

```go
package flyweight

import "fmt"

// 享元
type IconStyle struct {
	Icon  string
	Color string
	Size  int
}

// 享元工厂
type IconStyleFactory struct {
	cache map[string]*IconStyle
}

func NewIconStyleFactory() *IconStyleFactory {
	return &IconStyleFactory{cache: make(map[string]*IconStyle)}
}

func (f *IconStyleFactory) GetStyle(icon, color string, size int) *IconStyle {
	key := fmt.Sprintf("%s-%s-%d", icon, color, size)
	if style, ok := f.cache[key]; ok {
		return style
	}
	style := &IconStyle{Icon: icon, Color: color, Size: size}
	f.cache[key] = style
	return style
}

// 上下文
type MapMarker struct {
	X, Y  float64
	Style *IconStyle
}
```

## Flutter 中的真实应用

- **ImageCache**：Flutter 的图片缓存就是享元——同一张图片在多处使用只占一份内存
- **TextStyle**：相同的 TextStyle 可以在多个 Text Widget 间共享
- **Color**：Flutter 的 `Colors.blue` 等是 const 常量——全局共享

## 什么时候用

- 大量相似对象，只有少数字段不同
- 内存是瓶颈
- 可以将对象状态分为"共享"和"不共享"两部分

## 什么时候不用

- 对象数量不多
- 对象之间没有共享部分

## 与其他模式的关系

- 享元通常和**工厂**结合——工厂管理共享对象的缓存
- 享元的"共享/不共享"分离类似**桥接**的"抽象/实现"分离
