# Flutter SDK 中的设计模式真实案例分析

> 用你每天都在用的 Flutter SDK 来理解设计模式。每个模式都对应一个你见过的真实类或 API。

---

## 1. 观察者模式（Observer）

**SDK 中的体现：** `ChangeNotifier`、`ValueNotifier`、`Listenable`

这是 Flutter 响应式框架的根基。

```dart
// Flutter SDK 源码简化版
class ChangeNotifier extends Listenable {
  final List<VoidCallback> _listeners = [];

  @override
  void addListener(VoidCallback listener) {
    _listeners.add(listener);
  }

  @override
  void removeListener(VoidCallback listener) {
    _listeners.remove(listener);
  }

  void notifyListeners() {
    for (final listener in _listeners) {
      listener();
    }
  }
}
```

**为什么 Flutter 团队选这个模式：** UI 需要在数据变化时自动刷新。观察者模式让数据（Subject）不需要知道谁在看它，只管"喊一声"（notifyListeners），所有监听者（Observer）自行响应。

**你日常用的：** 每次调用 `notifyListeners()` 让 UI 刷新，就是在用观察者模式。

---

## 2. 组合模式（Composite）

**SDK 中的体现：** 整个 Widget 树

Widget 树是组合模式的教科书实现——单个叶子节点（Text、Icon）和容器节点（Column、Row、Container）实现同一个接口（Widget），容器可以包含任意数量的子节点。

```dart
// Flutter 的 Widget 树天然是组合模式
Widget build(BuildContext context) {
  return Column(                    // 容器（Composite）
    children: [
      Text('Hello'),                // 叶子（Leaf）
      Row(                          // 容器（Composite）
        children: [
          Icon(Icons.star),         // 叶子（Leaf）
          Text('World'),            // 叶子（Leaf）
        ],
      ),
    ],
  );
}
```

**为什么 Flutter 团队选这个模式：** 组合模式让 Flutter 可以用统一的方式处理"一个 Widget"和"一组 Widget"。build 方法不需要关心返回的是单个 Widget 还是一棵复杂的子树。

---

## 3. 建造者模式（Builder）

**SDK 中的体现：** `AlertDialog`、`ListView.builder`、`Builder` widget

```dart
// AlertDialog 用建造者模式逐步配置
final dialog = AlertDialog(
  title: Text('确认'),
  content: Text('确定要删除吗？'),
  actions: [
    TextButton(onPressed: () => Navigator.pop(context), child: Text('取消')),
    TextButton(onPressed: () => doDelete(), child: Text('删除')),
  ],
);
```

```dart
// ListView.builder 延迟构建（只构建可见项）
ListView.builder(
  itemCount: 1000,
  itemBuilder: (context, index) {
    return ListTile(title: Text('Item $index'));
  },
)
```

**为什么 Flutter 团队选这个模式：** AlertDialog 有很多可选参数，建造者模式（通过命名可选参数）让你只配置需要的部分。`ListView.builder` 则是一种特殊的建造者——按需构建，不一次性创建所有子项。

---

## 4. 单例模式（Singleton）

**SDK 中的体现：** `WidgetsBinding.instance`、`SchedulerBinding.instance`

```dart
// Flutter 中的 binding 都是单例
class WidgetsBinding extends BindingBase {
  static WidgetsBinding? _instance;
  static WidgetsBinding get instance => _instance!;

  // 工厂构造函数确保只创建一个实例
  static WidgetsBinding ensureInitialized() {
    if (_instance == null) {
      _instance = WidgetsBinding();
    }
    return _instance!;
  }
}
```

**为什么 Flutter 团队选这个模式：** Binding 是 App 与底层引擎的唯一桥梁，全局只需要一个。多个实例会导致状态混乱。

---

## 5. 策略模式（Strategy）

**SDK 中的体现：** `ThemeData`、`TextEditingController`、各种 `Formatter`

```dart
// ThemeData 就是策略模式的体现——切换整套渲染策略
MaterialApp(
  theme: ThemeData.light(),     // 策略 A
  darkTheme: ThemeData.dark(),  // 策略 B
  themeMode: ThemeMode.system,  // 策略选择器
);

// 使用时
final color = Theme.of(context).primaryColor;  // 当前策略的颜色
```

**为什么 Flutter 团队选这个模式：** 主题切换需要在运行时改变大量视觉行为。策略模式将"如何渲染"封装为可替换的对象，而不是写满 if-else。

---

## 6. 装饰器模式（Decorator）

**SDK 中的体现：** `Container`、`DecoratedBox`、`Wrap`

```dart
// Container 是最典型的装饰器——层层包装一个 child
Container(
  padding: EdgeInsets.all(16),        // 装饰：内边距
  decoration: BoxDecoration(          // 装饰：背景+圆角
    color: Colors.blue,
    borderRadius: BorderRadius.circular(8),
  ),
  child: Text('Hello'),               // 被装饰的核心
)
```

**为什么 Flutter 团队选这个模式：** Widget 树的本质就是层层装饰。你可以在任何 Widget 外面包一层 Container/Padding/SizedBox 来添加新行为，而不修改内部 Widget。

---

## 7. 外观模式（Facade）

**SDK 中的体现：** `Navigator`、`Scaffold`

```dart
// Navigator 隐藏了复杂的路由管理
Navigator.of(context).push(
  MaterialPageRoute(builder: (context) => SecondPage()),
);

// 实际上底层涉及：Route 管理、Animation、Overlay、Focus 等
// 但你只需要调用 push/pop
```

```dart
// Scaffold 隐藏了 AppBar/Body/FAB/BottomSheet/Drawer 的复杂布局
Scaffold(
  appBar: AppBar(title: Text('首页')),
  body: Center(child: Text('内容')),
  floatingActionButton: FloatingActionButton(onPressed: () {}),
);
```

**为什么 Flutter 团队选这个模式：** 路由和页面布局极其复杂（涉及动画、手势、焦点管理），但 99% 的开发者只需要 `push` 和 `pop`。外观模式把复杂性藏在简单接口后面。

---

## 8. 工厂方法模式（Factory Method）

**SDK 中的体现：** `StatefulWidget.createState()`、`InheritedWidget` 的 `updateShouldNotify`

```dart
// createState() 就是工厂方法——由框架调用，你只负责"生产"一个 State
class MyWidget extends StatefulWidget {
  @override
  State<MyWidget> createState() => _MyWidgetState();  // 工厂方法
}
```

```dart
// ThemeData 的工厂构造函数
ThemeData.light();  // 工厂方法——生产一个亮色主题
ThemeData.dark();   // 工厂方法——生产一个暗色主题
```

**为什么 Flutter 团队选这个模式：** 框架需要控制 State 的生命周期（何时创建、何时销毁），所以把创建逻辑委托给子类（你的 Widget），但调用时机由框架决定。

---

## 9. 模板方法模式（Template Method）

**SDK 中的体现：** `State` 的生命周期方法

```dart
// State 的生命周期就是模板方法——框架定义了调用顺序，你填充具体行为
class _MyState extends State<MyWidget> {
  @override
  void initState() { super.initState(); /* 初始化 */ }

  @override
  Widget build(BuildContext context) { /* 构建UI */ }

  @override
  void dispose() { super.dispose(); /* 清理 */ }
}
// 框架按固定顺序调用：initState → build → (didUpdateWidget) → dispose
```

**为什么 Flutter 团队选这个模式：** Widget 的生命周期是固定的（创建→构建→更新→销毁），但每个阶段做什么由开发者决定。模板方法定义了"骨架"，你填"血肉"。

---

## 10. 代理模式（Proxy）

**SDK 中的体现：** `Proxy` widget、`InheritedWidget`

```dart
// InheritedWidget 是数据代理——子树中的任何 Widget 都可以"代理访问"数据
class MyInheritedWidget extends InheritedWidget {
  final String data;
  MyInheritedWidget({required this.data, required Widget child}) : super(child: child);

  static MyInheritedWidget? of(BuildContext context) {
    return context.dependOnInheritedWidgetOfExactType<MyInheritedWidget>();
  }

  @override
  bool updateShouldNotify(MyInheritedWidget old) => data != old.data;
}
```

**为什么 Flutter 团队选这个模式：** Widget 树很深，逐层传递数据很痛苦。InheritedWidget 作为代理，让任何深度的子 Widget 都可以直接访问数据，不需要层层传参。

---

## 11. 适配器模式（Adapter）

**SDK 中的体现：** Platform Interface 模式（如 `url_launcher`、`shared_preferences`）

```dart
// url_launcher 的平台接口适配器
abstract class UrlLauncherPlatform {
  Future<bool> launch(String url);  // 统一接口
}

class UrlLauncherIOS extends UrlLauncherPlatform {
  @override
  Future<bool> launch(String url) {
    // 调用 iOS 原生 UIApplication.shared.openURL
  }
}

class UrlLauncherAndroid extends UrlLauncherPlatform {
  @override
  Future<bool> launch(String url) {
    // 调用 Android 原生 Intent.ACTION_VIEW
  }
}
```

**为什么 Flutter 团队选这个模式：** Flutter 要跑在 iOS、Android、Web、桌面等多个平台，每个平台的 API 完全不同。适配器模式让上层代码用统一接口调用，底层自动适配到各平台。

---

## 12. 状态模式（State）

**SDK 中的体现：** `StatefulWidget` + `State`

```dart
// State 对象持有状态，setState 改变状态后重新构建
class _CounterState extends State<Counter> {
  int _count = 0;  // 状态

  void _increment() {
    setState(() { _count++; });  // 状态变化 → 触发重建
  }

  @override
  Widget build(BuildContext context) {
    return Text('$_count');  // 根据当前状态渲染
  }
}
```

**为什么 Flutter 团队选这个模式：** UI 的核心问题就是"状态管理"。State 模式将状态和行为封装在一起，状态变化自动触发 UI 更新。

---

## 13. 命令模式（Command）

**SDK 中的体现：** `Actions` / `Intents` 系统

```dart
// Flutter 的 Action/Intent 系统
class CopyAction extends Action<CopyIntent> {
  @override
  void invoke(CopyIntent intent) {
    // 执行复制操作
    Clipboard.setData(ClipboardData(text: intent.text));
  }
}

// 使用
Actions(
  actions: {CopyIntent: CopyAction()},
  child: IntentSender(),
)
```

**为什么 Flutter 团队选这个模式：** 将"做什么"（Action）和"什么时候做"（Intent 触发）解耦。同一个复制操作可以由快捷键、菜单、右键等多种方式触发。

---

## 14. 中介者模式（Mediator）

**SDK 中的体现：** `InheritedWidget`（同时充当代理和中介者）

InheritedWidget 不仅代理数据，还充当中介者——协调祖先 Widget 和后代 Widget 之间的通信，避免它们直接引用彼此。

---

## 15. 迭代器模式（Iterator）

**SDK 中的体现：** Dart 的 `Iterable`、`List.map()`、`List.where()`

```dart
// Dart 的 Iterable 就是迭代器模式
final items = [1, 2, 3, 4, 5];
final doubled = items.map((e) => e * 2);  // 返回 Iterable（惰性迭代）
final evens = items.where((e) => e.isEven);
```

**为什么 Dart 团队选这个模式：** 集合的内部结构各不相同（List、Set、Map、Queue），但遍历方式统一。迭代器模式让你不需要关心集合内部怎么存储。

---

## 16. 责任链模式（Chain of Responsibility）

**SDK 中的体现：** Flutter 的手势识别系统（Hit Test）

```dart
// Flutter 事件分发是一个责任链
// 从最外层向最内层传递 hit test
// 每一层决定是否处理这个手势
// 如果处理就消费掉，不处理就继续传递
GestureDetector(          // 第 1 层：能否处理？
  child: InkWell(         // 第 2 层：能否处理？
    child: TextField(     // 第 3 层：能否处理？
    ),
  ),
)
```

**为什么 Flutter 团队选这个模式：** 手势事件需要从外到内逐层判断"谁该响应"。责任链让每个 Widget 独立决定是否消费事件，而不需要知道整棵树的结构。

---

## 总结：Flutter 开发者最该掌握的模式

按在日常开发中出现的频率排序：

| 排名 | 模式 | 出现频率 | 必须掌握 |
|------|------|----------|----------|
| 1 | 观察者 | 每天 | 是 |
| 2 | 组合 | 每天 | 是 |
| 3 | 模板方法 | 每天 | 是 |
| 4 | 状态 | 每天 | 是 |
| 5 | 装饰器 | 每天 | 是 |
| 6 | 外观 | 每天 | 是 |
| 7 | 工厂方法 | 经常 | 是 |
| 8 | 代理 | 经常 | 是 |
| 9 | 建造者 | 经常 | 是 |
| 10 | 策略 | 偶尔 | 建议掌握 |
| 11 | 单例 | 偶尔 | 了解 |
| 12 | 适配器 | 偶尔 | 了解 |
| 13 | 迭代器 | 偶尔 | 了解 |
| 14 | 责任链 | 少见 | 了解 |
| 15 | 命令 | 少见 | 了解 |
| 16 | 中介者 | 少见 | 了解 |
