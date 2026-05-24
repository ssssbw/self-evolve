# 迭代器模式（Iterator）

## 一句话

顺序访问集合中的元素，而不暴露集合的内部结构。

## Dart 代码

```dart
// Dart 已经内置了迭代器支持，这里展示原理
class NumberIterator implements Iterator<int> {
  final List<int> _items;
  int _index = -1;

  NumberIterator(this._items);

  @override
  int get current => _items[_index];

  @override
  bool moveNext() {
    _index++;
    return _index < _items.length;
  }
}

class NumberCollection implements Iterable<int> {
  final List<int> _items;
  NumberCollection(this._items);

  @override
  Iterator<int> get iterator => NumberIterator(_items);
}

void main() {
  final collection = NumberCollection([1, 2, 3, 4, 5]);
  for (final n in collection) {
    print(n); // 1 2 3 4 5
  }
  // Dart 的 for-in 就是迭代器模式的语法糖
}
```

## Go 代码

```go
package iterator

// Go 没有内置迭代器接口，通常用 channel 或闭包模拟
type IntIterator struct {
	items []int
	index int
}

func NewIntIterator(items []int) *IntIterator {
	return &IntIterator{items: items, index: -1}
}

func (it *IntIterator) Next() bool {
	it.index++
	return it.index < len(it.items)
}

func (it *IntIterator) Value() int {
	return it.items[it.index]
}

// 使用
// it := NewIntIterator([]int{1, 2, 3})
// for it.Next() { fmt.Println(it.Value()) }
```

## Flutter/Dart 中的真实应用

- **for-in 循环**：`for (final item in list)` 就是迭代器
- **map/where/expand**：返回 lazy Iterable，不立即计算
- **Stream**：异步版的迭代器——`await for (final event in stream)`

## 什么时候用 / 不用

- 用：需要遍历不同类型的集合（List、Set、Map、Tree）用统一方式
- 不用：只需要简单的 for 循环遍历 List
