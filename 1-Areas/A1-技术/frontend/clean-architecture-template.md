# Clean Architecture Flutter 项目模板

> 学完设计模式和架构后，用 Clean Architecture 构建一个可维护的 Flutter 项目。

---

## Clean Architecture 核心原则

```
┌─────────────────────────────────┐
│           UI Layer               │  ← Widgets, Pages
│  ┌───────────────────────────┐   │
│  │      Presentation Layer    │   │  ← BLoC/Cubit/Provider
│  │  ┌───────────────────┐    │   │
│  │  │    Domain Layer    │    │   │  ← Entities, Use Cases
│  │  │  ┌───────────┐    │    │   │
│  │  │  │   Data     │    │    │   │  ← Repositories Impl, Data Sources
│  │  │  │  Layer     │    │    │   │
│  │  │  └───────────┘    │    │   │
│  │  └───────────────────┘    │   │
│  └───────────────────────────┘   │
└─────────────────────────────────┘

依赖规则：外层可以依赖内层，内层不能依赖外层
```

---

## 推荐目录结构

```
lib/
├── main.dart                    # 入口 + DI 配置
├── app.dart                     # MaterialApp 配置
│
├── core/                        # 跨功能基础设施
│   ├── constants/               # 常量
│   ├── errors/                  # 统一错误定义
│   │   ├── failures.dart
│   │   └── exceptions.dart
│   ├── network/                 # 网络层
│   │   ├── api_client.dart
│   │   └── network_info.dart
│   ├── theme/                   # 主题
│   └── utils/                   # 工具函数
│
├── features/                    # 按功能模块划分（最重要的约定）
│   ├── todo/                    # TODO 功能模块
│   │   ├── data/                # 数据层
│   │   │   ├── datasources/     # 数据源
│   │   │   │   ├── todo_local_ds.dart   # 本地（SQLite/Hive）
│   │   │   │   └── todo_remote_ds.dart  # 远程（API）
│   │   │   ├── models/          # DTO（数据传输对象）
│   │   │   │   └── todo_model.dart
│   │   │   └── repositories/    # Repository 实现
│   │   │       └── todo_repo_impl.dart
│   │   │
│   │   ├── domain/              # 领域层（纯 Dart，不依赖 Flutter）
│   │   │   ├── entities/        # 领域实体
│   │   │   │   └── todo.dart
│   │   │   ├── repositories/    # Repository 接口
│   │   │   │   └── todo_repo.dart
│   │   │   └── usecases/        # 用例（每个用例一个类）
│   │   │       ├── get_todos.dart
│   │   │       ├── add_todo.dart
│   │   │       └── delete_todo.dart
│   │   │
│   │   └── presentation/        # 表现层
│   │       ├── bloc/            # 状态管理
│   │       │   ├── todo_bloc.dart
│   │       │   ├── todo_event.dart
│   │       │   └── todo_state.dart
│   │       ├── pages/           # 页面
│   │       │   └── todo_page.dart
│   │       └── widgets/         # 页面内组件
│   │           └── todo_item.dart
│   │
│   └── auth/                    # 另一个功能模块
│       ├── data/
│       ├── domain/
│       └── presentation/
```

---

## 各层代码示例

### Domain Layer — 领域层（纯 Dart，最核心）

```dart
// entities/todo.dart — 领域实体，不依赖任何框架
class Todo {
  final int id;
  final String title;
  final bool isDone;
  final DateTime createdAt;

  Todo({
    required this.id,
    required this.title,
    this.isDone = false,
    required this.createdAt,
  });

  Todo copyWith({String? title, bool? isDone}) => Todo(
        id: id,
        title: title ?? this.title,
        isDone: isDone ?? this.isDone,
        createdAt: createdAt,
      );
}

// repositories/todo_repo.dart — Repository 接口（抽象）
abstract class TodoRepository {
  Future<List<Todo>> getTodos();
  Future<Todo> addTodo(String title);
  Future<void> deleteTodo(int id);
  Future<Todo> toggleTodo(int id);
}

// usecases/get_todos.dart — 用例（单一职责）
class GetTodos {
  final TodoRepository repository;
  GetTodos(this.repository);

  Future<List<Todo>> call() => repository.getTodos();
}
```

### Data Layer — 数据层

```dart
// models/todo_model.dart — DTO，负责 JSON 序列化
class TodoModel extends Todo {
  TodoModel({
    required super.id,
    required super.title,
    required super.isDone,
    required super.createdAt,
  });

  factory TodoModel.fromJson(Map<String, dynamic> json) => TodoModel(
        id: json['id'],
        title: json['title'],
        isDone: json['is_done'],
        createdAt: DateTime.parse(json['created_at']),
      );

  Map<String, dynamic> toJson() => {
        'id': id,
        'title': title,
        'is_done': isDone,
        'created_at': createdAt.toIso8601String(),
      };
}

// repositories/todo_repo_impl.dart — Repository 实现
class TodoRepositoryImpl implements TodoRepository {
  final TodoRemoteDataSource remoteDs;
  final TodoLocalDataSource localDs;
  final NetworkInfo networkInfo;

  TodoRepositoryImpl({
    required this.remoteDs,
    required this.localDs,
    required this.networkInfo,
  });

  @override
  Future<List<Todo>> getTodos() async {
    if (await networkInfo.isConnected) {
      final models = await remoteDs.getTodos();
      await localDs.cacheTodos(models);
      return models;
    } else {
      return localDs.getCachedTodos();
    }
  }
}
```

### Presentation Layer — 表现层

```dart
// bloc/todo_bloc.dart
class TodoBloc extends Bloc<TodoEvent, TodoState> {
  final GetTodos getTodos;
  final AddTodo addTodo;

  TodoBloc({required this.getTodos, required this.addTodo})
      : super(TodoInitial()) {
    on<LoadTodos>(_onLoadTodos);
    on<AddTodoEvent>(_onAddTodo);
  }

  Future<void> _onLoadTodos(LoadTodos event, Emitter<TodoState> emit) async {
    emit(TodoLoading());
    final result = await getTodos();
    emit(TodoLoaded(todos: result));
  }

  Future<void> _onAddTodo(AddTodoEvent event, Emitter<TodoState> emit) async {
    await addTodo(event.title);
    add(LoadTodos()); // 重新加载
  }
}
```

---

## 设计模式在 Clean Architecture 中的体现

| 设计模式 | 在哪里体现 |
|---------|-----------|
| **策略** | Use Case 封装不同的业务策略 |
| **工厂方法** | Repository 由 DI 容器创建 |
| **代理** | Repository 接口代理了实际数据源 |
| **观察者** | BLoC/Provider 的状态通知 |
| **依赖注入** | Domain 层通过构造函数接收 Repository |
| **单一职责** | 每个 Use Case 只做一件事 |

---

## 什么时候用 / 不用

- **用：** 中大型项目（10+ 页面）；多人协作；长期维护
- **不用：** 小型项目（2-3 页面）；个人 Demo；POC 验证

## 和其他架构的对比

| 架构 | 特点 | 适合 |
|------|------|------|
| MVC | 简单 | 小项目 |
| MVVM | ViewModel 绑定 View | 中等项目 |
| Clean Architecture | 依赖规则 + 分层 | 大型长期项目 |
| BLoC | 状态管理 + 事件驱动 | 需要清晰状态管理的项目 |

**推荐：** Flutter 项目从 MVVM 起步，项目变大后迁移到 Clean Architecture。
