# Dart 3 高级特性指南

> 你每天写 Dart，但可能没用过这些特性。掌握它们，你的代码质量会有质的飞跃。

---

## 1. Sealed Classes（密封类）

### 是什么
限制类的继承层次——所有子类必须在同一个文件中定义。编译器知道所有可能的子类，可以帮你做穷举检查。

### 为什么重要
替代了大量 if-else + 类型判断，编译器帮你保证不遗漏。

### 代码

```dart
// 定义密封类——所有子类型在这里穷举
sealed class Result<T> {
  const Result();
}

class Success<T> extends Result<T> {
  final T data;
  const Success(this.data);
}

class Failure<T> extends Result<T> {
  final String message;
  const Failure(this.message);
}

class Loading<T> extends Result<T> {
  const Loading();
}

// 使用——switch 必须穷举所有子类，否则编译报错
String describe(Result<int> result) => switch (result) {
  Success(:final data) => '成功: $data',
  Failure(:final message) => '失败: $message',
  Loading() => '加载中...',
};

// 实际应用：替代你的 API 请求状态管理
Widget build(BuildContext context) {
  return switch (apiState) {
    Loading() => CircularProgressIndicator(),
    Success(:final data) => ListView(children: data),
    Failure(:final message) => ErrorWidget(message),
  };
}
```

### Flutter 中的应用
- 网络请求状态（Loading/Success/Failure）
- 表单验证结果（Valid/Invalid/Empty）
- 支付状态（Pending/Completed/Failed/Refunded）

---

## 2. Pattern Matching（模式匹配）

### 是什么
Dart 3 引入了强大的模式匹配，可以解构对象、匹配类型、提取值。

### 代码

```dart
// 解构 Record
var (name, age) = ('Flutter', 5);
print('$name is $age years old');

// 解构 List
var [first, _, third] = [1, 2, 3];
// _ 表示忽略

// 解构 Map
var {'name': name, 'age': age} = {'name': 'Dart', 'age': 12};

// 解构对象
class User {
  final String name;
  final int age;
  const User(this.name, this.age);
}

var User(name: n, age: a) = User('Alice', 25);

// if-case 模式匹配
if (json case {'type': 'user', 'name': String name}) {
  print('User: $name');
}

// for-in 模式匹配
for (var User(:name, :age) in users) {
  print('$name, $age');
}
```

### Flutter 中的应用

```dart
// 代替 if-else 链
Widget buildItem(dynamic item) {
  return switch (item) {
    Product(:final name, :final price) => ProductCard(name, price),
    Category(:final title) => CategoryHeader(title),
    Ad(:final imageUrl) => AdBanner(imageUrl),
    _ => SizedBox(), // default
  };
}
```

---

## 3. Records（记录类型）

### 是什么
轻量级的匿名数据聚合。不需要写 class 就能组合多个值。

### 代码

```dart
// 基本用法
var user = ('Alice', 25);
print(user.$1); // Alice
print(user.$2); // 25

// 命名字段
var user2 = (name: 'Bob', age: 30);
print(user2.name); // Bob

// 作为函数返回值——不需要再定义 Tuple 或 DTO
(String, int) getUser() => ('Charlie', 28);

// 实际应用：API 响应
typedef ApiResponse<T> = ({T? data, String? error, int statusCode});

ApiResponse<List<User>> fetchUsers() {
  try {
    final users = [...];
    return (data: users, error: null, statusCode: 200);
  } catch (e) {
    return (data: null, error: e.toString(), statusCode: 500);
  }
}

// 解构
final (:data, :error, :statusCode) = fetchUsers();
```

### Flutter 中的应用

```dart
// 替代 Map<String, dynamic> 传递配置
typedef ButtonConfig = ({
  Color color,
  double radius,
  String text,
});

Widget buildButton(ButtonConfig config) {
  return ElevatedButton(
    style: ElevatedButton.styleFrom(
      backgroundColor: config.color,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(config.radius),
      ),
    ),
    onPressed: () {},
    child: Text(config.text),
  );
}
```

---

## 4. Extension Methods（扩展方法）

### 是什么
给现有类添加新方法，不需要继承或修改原始类。

### 代码

```dart
// 给 String 添加验证方法
extension StringValidation on String {
  bool get isValidEmail => RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$').hasMatch(this);
  bool get isValidPhone => RegExp(r'^1[3-9]\d{9}$').hasMatch(this);
  bool get isNotBlank => trim().isNotEmpty;
}

// 使用
'email@example.com'.isValidEmail; // true
'13800138000'.isValidPhone;       // true

// 给 List 添加安全访问
extension ListSafety<T> on List<T> {
  T? get firstOrNull => isEmpty ? null : first;
  T? lastWhereOrNull(bool Function(T) test) {
    for (var i = length - 1; i >= 0; i--) {
      if (test(this[i])) return this[i];
    }
    return null;
  }
}

// 给 int 添加时间格式化
extension IntDuration on int {
  Duration get seconds => Duration(seconds: this);
  Duration get minutes => Duration(minutes: this);
  Duration get hours => Duration(hours: this);
}

// 使用
await Future.delayed(2.seconds);
```

### Flutter 中的应用

```dart
// 给 BuildContext 添加快捷方法
extension ContextExtensions on BuildContext {
  ThemeData get theme => Theme.of(this);
  MediaQueryData get mediaQuery => MediaQuery.of(this);
  double get screenWidth => mediaQuery.size.width;
  double get screenHeight => mediaQuery.size.height;
}

// 使用（简洁！）
Widget build(BuildContext context) {
  return Container(
    width: context.screenWidth * 0.8,
    color: context.theme.primaryColor,
  );
}
```

---

## 5. Isolate 深入理解

### 是什么
Dart 的并发模型——每个 Isolate 有独立的内存堆，通过消息传递通信。

### 代码

```dart
// 简单用法：compute 函数（Flutter 封装）
final result = await compute(heavyComputation, data);

int heavyComputation(int input) {
  // 在独立 Isolate 中执行，不阻塞 UI
  return input * input;
}

// 高级用法：双向通信的 Isolate
import 'dart:isolate';

void main() async {
  final receivePort = ReceivePort();
  
  await Isolate.spawn(dataProcessor, receivePort.sendPort);
  
  receivePort.listen((message) {
    print('收到: $message');
  });
}

void dataProcessor(SendPort sendPort) {
  sendPort.send('处理完成');
}

// 使用 Completer 等待 Isolate 结果
Future<List<int>> sortInIsolate(List<int> data) async {
  final completer = Completer<List<int>>();
  
  final receivePort = ReceivePort();
  await Isolate.spawn(
    (SendPort port) => Isolate.exit(port, _sort(data)),
    receivePort.sendPort,
  );
  
  receivePort.listen((sorted) {
    completer.complete(sorted);
    receivePort.close();
  });
  
  return completer.future;
}

List<int> _sort(List<int> data) => data..sort();
```

### 什么时候用 Isolate

| 场景 | 用 Isolate？ | 理由 |
|------|-------------|------|
| JSON 解析（<100KB） | 不用 | 足够快 |
| JSON 解析（>1MB） | 用 | 避免 UI 卡顿 |
| 图片处理 | 用 | CPU 密集 |
| 文件加密 | 用 | CPU 密集 |
| 网络请求 | 不用 | I/O 操作，async/await 就够了 |
| 复杂数学计算 | 用 | CPU 密集 |

---

## 学习检查清单

- [ ] 用 sealed class 重构一个 if-else 类型判断
- [ ] 用 pattern matching 替代一个 switch-case
- [ ] 用 Record 替代一个 Map<String, dynamic>
- [ ] 给 String/num/List 写一个实用的 extension
- [ ] 用 compute() 把一个 CPU 密集操作移到 Isolate
