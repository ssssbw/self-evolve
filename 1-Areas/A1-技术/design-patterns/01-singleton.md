# 单例模式（Singleton）

## 一句话

保证一个类只有一个实例，并提供全局访问点。

## 问题场景

你的 App 需要一个全局配置对象。如果多处创建配置实例，可能导致配置不一致。你需要确保无论谁访问，拿到的都是同一个对象。

## 解决方案

让类自己管理唯一的实例，通过类方法提供访问，禁止外部创建新实例。

## Dart 代码

```dart
// 方式一：工厂构造函数（Dart 惯用写法）
class AppConfig {
  static final AppConfig _instance = AppConfig._internal();

  final String appName;
  final String version;

  // 私有命名构造函数
  AppConfig._internal()
      : appName = 'SelfEvolve',
        version = '1.0.0';

  // 工厂构造函数，始终返回同一个实例
  factory AppConfig() => _instance;

  static AppConfig get instance => _instance;
}

// 使用
void main() {
  final config1 = AppConfig();
  final config2 = AppConfig();
  print(identical(config1, config2)); // true
}
```

## Go 代码

```go
package singleton

import (
	"sync"
)

// Config 是单例结构体
type Config struct {
	AppName string
	Version string
}

var (
	instance *Config
	once     sync.Once
)

// GetInstance 返回唯一的 Config 实例
// sync.Once 保证即使并发调用也只初始化一次
func GetInstance() *Config {
	once.Do(func() {
		instance = &Config{
			AppName: "SelfEvolve",
			Version: "1.0.0",
		}
	})
	return instance
}

// 使用
// c1 := GetInstance()
// c2 := GetInstance()
// fmt.Println(c1 == c2) // true
```

## Flutter 中的真实应用

- `WidgetsBinding.instance` — 全局唯一的 binding 实例
- `SharedPreferences` — 通常包装为单例，避免多次初始化
- `FirebaseFirestore.instance` — Firebase 的单例入口

## 什么时候用

- 全局配置对象
- 日志管理器
- 数据库连接池
- 缓存管理器

## 什么时候不用

- 需要多个不同实例的场景
- 测试时需要 mock 不同的行为（单例让测试变难）
- 依赖注入框架（如 get_it）通常能更好地解决全局访问问题

## 与其他模式的关系

- 单例常和**工厂方法**结合（instance 属性就是一个工厂）
- 单例可以是**外观模式**的提供者（一个全局入口点）
- 过度使用单例会导致全局状态难以管理，考虑用**依赖注入**替代
