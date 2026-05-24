# Flutter 状态管理深度对比

> Provider vs Riverpod vs Bloc vs GetX — 从设计模式角度分析，帮你选型。

---

## 总览

| 维度 | Provider | Riverpod | Bloc | GetX |
|------|----------|----------|------|------|
| 设计模式 | 观察者 + 代理 | 观察者 + 依赖注入 | 观察者 + 命令 | 依赖注入 + 响应式 |
| 学习曲线 | 低 | 中 | 中高 | 低 |
| 类型安全 | 弱（runtime） | 强（compile-time） | 强 | 弱 |
| 可测试性 | 中 | 高 | 高 | 低 |
| 社区推荐度 | 官方推荐 | 官方推荐 | 广泛使用 | 有争议 |
| 适合项目 | 中小型 | 中大型 | 大型 | 快速原型 |

---

## Provider — 官方推荐入门

### 设计模式分析

Provider 本质是 **InheritedWidget + 观察者模式** 的封装：

```
ChangeNotifier（Subject）
    ↓ notifyListeners()
Consumer/Selector（Observer）
    ↓ rebuild
Widget
```

### 代码示例

```dart
// Model
class Counter extends ChangeNotifier {
  int _count = 0;
  int get count => _count;
  
  void increment() {
    _count++;
    notifyListeners(); // 通知观察者
  }
}

// 在 Widget 树中提供
void main() {
  runApp(
    ChangeNotifierProvider(
      create: (_) => Counter(),
      child: MyApp(),
    ),
  );
}

// 消费
class CounterWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Consumer<Counter>( // 观察者
      builder: (context, counter, child) {
        return Text('${counter.count}');
      },
    );
  }
}
```

### 优缺点

**优点：** 简单、官方维护、文档多
**缺点：** 运行时依赖（忘记写 Provider 会 crash）、context 依赖导致测试困难

---

## Riverpod — Provider 的进化版

### 设计模式分析

Riverpod 在 Provider 基础上加入了 **依赖注入**，去掉了对 BuildContext 的依赖：

```
Provider（声明依赖关系）
    ↓ ref.watch / ref.read
ConsumerWidget（自动重建）
```

### 代码示例

```dart
// 声明 Provider（编译时检查）
final counterProvider = StateNotifierProvider<CounterNotifier, int>(
  (ref) => CounterNotifier(),
);

class CounterNotifier extends StateNotifier<int> {
  CounterNotifier() : super(0);
  void increment() => state++;
}

// 消费（无需 context！）
class CounterWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider); // 声明式依赖
    return Text('$count');
  }
}

// 在事件中修改
ref.read(counterProvider.notifier).increment();
```

### 关键优势：Provider 组合

```dart
// 一个 Provider 可以依赖另一个 Provider
final userRepositoryProvider = Provider((ref) => UserRepository());

final userServiceProvider = Provider((ref) {
  final repo = ref.watch(userRepositoryProvider); // 自动注入
  return UserService(repo);
});

final userListProvider = FutureProvider((ref) {
  final service = ref.watch(userServiceProvider);
  return service.getUsers();
});
```

### 优缺点

**优点：** 编译时安全、无需 context、可组合、可测试
**缺点：** 学习曲线比 Provider 陡、概念多

---

## Bloc — 事件驱动架构

### 设计模式分析

Bloc 基于 **观察者 + 命令模式**：

```
Event（命令）→ Bloc（处理器）→ State（状态）
     ↓              ↓                ↓
  用户操作     业务逻辑处理      UI 重建
```

### 代码示例

```dart
// Event
abstract class CounterEvent {}
class Increment extends CounterEvent {}
class Decrement extends CounterEvent {}

// State
class CounterState {
  final int count;
  CounterState(this.count);
}

// Bloc（处理器）
class CounterBloc extends Bloc<CounterEvent, CounterState> {
  CounterBloc() : super(CounterState(0)) {
    on<Increment>((event, emit) => emit(CounterState(state.count + 1)));
    on<Decrement>((event, emit) => emit(CounterState(state.count - 1)));
  }
}

// UI
class CounterWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocBuilder<CounterBloc, CounterState>(
      builder: (context, state) {
        return Column(
          children: [
            Text('${state.count}'),
            ElevatedButton(
              onPressed: () => context.read<CounterBloc>().add(Increment()),
              child: Text('+'),
            ),
          ],
        );
      },
    );
  }
}
```

### 关键优势：事件流可追踪

```dart
// Bloc 支持 transition 日志（状态变化记录）
// 方便调试：哪个 Event 导致了哪个 State 变化
class SimpleBlocObserver extends BlocObserver {
  @override
  void onTransition(Bloc bloc, Transition transition) {
    print('${bloc.runtimeType}: ${transition.event} → ${transition.nextState}');
  }
}
```

### 优缺点

**优点：** 状态变化可追踪、强类型、适合大团队
**缺点：** 样板代码多（Event/State/Bloc 三个类）、简单功能也要写很多代码

---

## GetX — 快速但争议

### 设计模式分析

GetX 是 **依赖注入 + 响应式编程** 的混合体：

```
Get.put<Controller>()    // 依赖注入
Obx(() => Widget)        // 响应式 UI
```

### 代码示例

```dart
class CounterController extends GetxController {
  var count = 0.obs; // 响应式变量
  void increment() => count++;
}

// UI
class CounterWidget extends GetView<CounterController> {
  @override
  Widget build(BuildContext context) {
    return Obx(() => Text('${controller.count}')); // 自动重建
  }
}
```

### 为什么有争议

- 全局状态无编译时检查
- 底层用了很多全局单例
- 违反 Flutter 的树形依赖传递理念
- 代码看似简洁，但隐藏了复杂度

**结论：** 原型阶段可以快速验证，正式项目不推荐。

---

## 选型建议

```
你的情况：
├── 个人项目 / 快速验证 → Provider（简单够用）
├── 正式项目（推荐）   → Riverpod（最佳平衡）
├── 大型团队项目       → Bloc（可追踪、可测试）
└── 想快速出活         → GetX（但要了解风险）
```

**我的建议：** 先用 Provider 上手，理解状态管理本质后迁移到 Riverpod。你学过的设计模式知识会帮助你理解每个框架的设计取舍。

---

## 设计模式映射

| 设计模式 | Provider | Riverpod | Bloc | GetX |
|---------|----------|----------|------|------|
| 观察者 | ChangeNotifier | StateNotifier | BlocBuilder | Obx |
| 代理 | InheritedWidget | ProviderScope | BlocProvider | Get.put |
| 命令 | — | — | Event | — |
| 依赖注入 | 手动 | 自动 | 手动 | 自动 |
| 单例 | Provider 单例 | Provider 单例 | BlocProvider | Get.put |
| 策略 | — | Provider 组合 | — | — |
