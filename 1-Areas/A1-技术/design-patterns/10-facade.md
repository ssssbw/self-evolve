# 外观模式（Facade）

## 一句话

为复杂子系统提供一个简化的统一接口。

## 问题场景

Flutter 的路由管理涉及 Route、Navigator、Overlay、Animation、Focus 等多个子系统。如果每次跳转都要手动操作这些，代码会极其复杂。

## Dart 代码

```dart
// 复杂子系统
class RouteManager {
  void createRoute() => print('创建路由');
  void disposeRoute() => print('销毁路由');
}

class AnimationController {
  void forward() => print('播放入场动画');
  void reverse() => print('播放退场动画');
}

class OverlayManager {
  void insert() => print('插入 Overlay 层');
  void remove() => print('移除 Overlay 层');
}

class FocusManager {
  void requestFocus() => print('请求焦点');
  void clearFocus() => print('清除焦点');
}

// 外观——简化接口
class NavigatorFacade {
  final RouteManager _route = RouteManager();
  final AnimationController _anim = AnimationController();
  final OverlayManager _overlay = OverlayManager();
  final FocusManager _focus = FocusManager();

  void push(String pageName) {
    _route.createRoute();
    _overlay.insert();
    _anim.forward();
    _focus.requestFocus();
    print('已跳转到: $pageName');
  }

  void pop() {
    _focus.clearFocus();
    _anim.reverse();
    _overlay.remove();
    _route.disposeRoute();
    print('已返回上一页');
  }
}

// 使用：简单！
void main() {
  final nav = NavigatorFacade();
  nav.push('详情页');
  nav.pop();
}
```

## Go 代码

```go
package facade

import "fmt"

// 子系统
type RouteManager struct{}
func (r *RouteManager) Create() { fmt.Println("创建路由") }
func (r *RouteManager) Dispose() { fmt.Println("销毁路由") }

type AnimationCtrl struct{}
func (a *AnimationCtrl) Forward() { fmt.Println("播放入场动画") }
func (a *AnimationCtrl) Reverse() { fmt.Println("播放退场动画") }

// 外观
type NavigatorFacade struct {
	route *RouteManager
	anim  *AnimationCtrl
}

func NewNavigatorFacade() *NavigatorFacade {
	return &NavigatorFacade{route: &RouteManager{}, anim: &AnimationCtrl{}}
}

func (n *NavigatorFacade) Push(page string) {
	n.route.Create()
	n.anim.Forward()
	fmt.Printf("已跳转到: %s\n", page)
}

func (n *NavigatorFacade) Pop() {
	n.anim.Reverse()
	n.route.Dispose()
	fmt.Println("已返回上一页")
}
```

## Flutter 中的真实应用

- **Navigator.of(context).push()** 就是外观——底层涉及 Route/Overlay/Animation/Focus，你只需要一行代码
- **Scaffold** 也是外观——把 AppBar/Body/FAB/Drawer/Snackbar 的复杂布局藏在一个 Widget 后面
- **MaterialApp** 是最大的外观——封装了 Theme、Router、Localization 等全部配置

## 什么时候用

- 子系统非常复杂，需要简化调用
- 需要为子系统定义分层入口
- 第三方库的 API 太复杂，想包装一层好用的

## 什么时候不用

- 子系统本身就简单
- 调用者需要直接操作子系统细节

## 与其他模式的关系

- 外观提供简化接口，**适配器**转换接口，**代理**控制访问
- 外观通常和**单例**结合（一个全局的外观对象）
- 外观不"隐藏"子系统，只是提供快捷方式——需要时仍可直接操作子系统
