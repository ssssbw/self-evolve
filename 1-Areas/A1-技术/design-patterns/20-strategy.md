# 策略模式（Strategy）

## 一句话

定义一系列算法，把它们封装成独立的策略对象，使算法可以在运行时切换。

## Dart 代码

```dart
abstract class SortStrategy {
  List<int> sort(List<int> data);
}

class BubbleSort implements SortStrategy {
  @override
  List<int> sort(List<int> data) {
    final arr = List<int>.from(data);
    for (int i = 0; i < arr.length - 1; i++) {
      for (int j = 0; j < arr.length - i - 1; j++) {
        if (arr[j] > arr[j + 1]) {
          final tmp = arr[j]; arr[j] = arr[j + 1]; arr[j + 1] = tmp;
        }
      }
    }
    return arr;
  }
}

class QuickSort implements SortStrategy {
  @override
  List<int> sort(List<int> data) {
    if (data.length <= 1) return data;
    final pivot = data[data.length ~/ 2];
    return [
      ...sort(data.where((e) => e < pivot).toList()),
      ...data.where((e) => e == pivot),
      ...sort(data.where((e) => e > pivot).toList()),
    ];
  }
}

class Sorter {
  SortStrategy strategy;
  Sorter(this.strategy);

  List<int> sort(List<int> data) => strategy.sort(data);
}

void main() {
  final data = [5, 3, 8, 1, 9, 2];
  final sorter = Sorter(BubbleSort());
  print(sorter.sort(data)); // [1, 2, 3, 5, 8, 9]

  sorter.strategy = QuickSort(); // 运行时切换策略
  print(sorter.sort(data));
}
```

## Go 代码

```go
package strategy

type SortStrategy interface {
	Sort(data []int) []int
}

type BubbleSort struct{}
func (s *BubbleSort) Sort(data []int) []int {
	arr := make([]int, len(data))
	copy(arr, data)
	for i := 0; i < len(arr)-1; i++ {
		for j := 0; j < len(arr)-i-1; j++ {
			if arr[j] > arr[j+1] {
				arr[j], arr[j+1] = arr[j+1], arr[j]
			}
		}
	}
	return arr
}

type Sorter struct{ Strategy SortStrategy }
func (s *Sorter) Sort(data []int) []int { return s.Strategy.Sort(data) }
```

## Flutter 中的真实应用

- **ThemeData**：切换主题就是切换渲染策略
- **TextStyle**：不同的文字样式就是不同的渲染策略
- **CrossAxisAlignment / MainAxisAlignment**：布局策略

## 什么时候用 / 不用

- 用：有多种算法变体，需要在运行时切换；避免大量条件判断
- 不用：只有一种算法，或算法极少变化

## 与其他模式的关系

- 策略和**状态**结构相同，但意图不同：策略选算法，状态管状态
- 策略和**模板方法**互补：策略用组合，模板方法用继承
