# 原型模式（Prototype）

## 一句话

通过克隆已有对象来创建新对象，而不是从头构建。适用于创建成本高的对象。

## 问题场景

你有一个配置复杂的对象（从网络加载、经过多次计算），需要创建几个"差不多但有一点不同"的副本。如果每次都重新创建和配置，太浪费。

## 解决方案

让对象支持克隆自己。新对象基于克隆副本修改，而不是从头创建。

## Dart 代码

```dart
// Dart 没有内置 Cloneable，需要自己实现
class UserConfig implements Cloneable {
  String theme;
  String language;
  List<String> permissions;
  Map<String, dynamic> preferences;

  UserConfig({
    required this.theme,
    required this.language,
    required this.permissions,
    required this.preferences,
  });

  // 深拷贝
  @override
  UserConfig clone() {
    return UserConfig(
      theme: theme,
      language: language,
      permissions: List.from(permissions),
      preferences: Map.from(preferences),
    );
  }

  @override
  String toString() => 'UserConfig(theme: $theme, lang: $language, perms: $permissions)';
}

mixin Cloneable {
  Cloneable clone();
}

// 使用
void main() {
  // 原型——创建成本"高"的对象
  final defaultConfig = UserConfig(
    theme: 'light',
    language: 'zh-CN',
    permissions: ['read', 'write'],
    preferences: {'fontSize': 14, 'darkMode': false},
  );

  // 克隆并修改——低成本
  final userA = defaultConfig.clone() as UserConfig;
  userA.theme = 'dark';

  final userB = defaultConfig.clone() as UserConfig;
  userB.language = 'en-US';
  userB.permissions.add('admin');

  // 原型不受影响
  print(defaultConfig); // light, zh-CN
  print(userA);          // dark, zh-CN
  print(userB);          // light, en-US, +admin
}
```

## Go 代码

```go
package prototype

import "encoding/json"

// 产品——需要支持克隆
type UserConfig struct {
	Theme       string
	Language    string
	Permissions []string
	Preferences map[string]interface{}
}

// Clone 使用 JSON 序列化/反序列化实现深拷贝
func (c *UserConfig) Clone() *UserConfig {
	data, _ := json.Marshal(c)
	clone := &UserConfig{}
	json.Unmarshal(data, clone)
	return clone
}

// 使用
// defaultConfig := &UserConfig{
//     Theme:       "light",
//     Language:    "zh-CN",
//     Permissions: []string{"read", "write"},
//     Preferences: map[string]interface{}{"fontSize": 14},
// }
//
// userA := defaultConfig.Clone()
// userA.Theme = "dark"           // 不影响 defaultConfig
//
// userB := defaultConfig.Clone()
// userB.Language = "en-US"
```

## Flutter 中的真实应用

- Flutter 的 Widget 是 immutable 的，每次 `setState` 本质上是"克隆一份状态 → 修改 → 生成新 Widget 树"
- Dart 的 `List.from()`、`Map.from()` 就是浅拷贝的原型模式

## 什么时候用

- 对象创建成本高（网络请求、复杂计算）
- 需要创建很多相似对象
- 对象结构复杂，构造参数多

## 什么时候不用

- 对象创建成本很低——直接 new 即可
- 对象之间没有相似性

## 与其他模式的关系

- 原型可以作为**抽象工厂**的替代——不是创建新对象，而是克隆原型
- **建造者**关注分步构建，原型关注克隆已有对象
- Go 中常用 JSON/Gob 序列化实现深拷贝，也可以手动实现
