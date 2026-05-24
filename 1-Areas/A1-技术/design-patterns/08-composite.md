# 组合模式（Composite）

## 一句话

将对象组合成树形结构来表示"部分-整体"层次，使客户端统一对待单个对象和组合对象。

## 问题场景

你需要实现一个文件系统：文件夹里可以有文件和子文件夹，子文件夹里又可以有文件和文件夹。你需要统一计算大小、统一显示结构——不想写 if (isFile) ... else if (isFolder) ...。

## Dart 代码

```dart
// 组件接口
abstract class FileComponent {
  String getName();
  int getSize();
  void display([int indent = 0]);
}

// 叶子——文件
class File extends FileComponent {
  final String name;
  final int size;

  File(this.name, this.size);

  @override
  String getName() => name;

  @override
  int getSize() => size;

  @override
  void display([int indent = 0]) {
    print('${'  ' * indent}- $name (${size}KB)');
  }
}

// 容器——文件夹
class Folder extends FileComponent {
  final String name;
  final List<FileComponent> _children = [];

  Folder(this.name);

  void add(FileComponent component) => _children.add(component);
  void remove(FileComponent component) => _children.remove(component);

  @override
  String getName() => name;

  @override
  int getSize() => _children.fold(0, (sum, c) => sum + c.getSize());

  @override
  void display([int indent = 0]) {
    print('${'  ' * indent}+ $name/ (${getSize()}KB)');
    for (final child in _children) {
      child.display(indent + 1);
    }
  }
}

// 使用
void main() {
  final root = Folder('self-evolve');
  root.add(File('README.md', 5));
  root.add(File('.gitignore', 1));

  final notes = Folder('notes');
  notes.add(File('ch01-计算机系统漫游.md', 8));
  notes.add(File('ch02-信息的表示和处理.md', 12));
  root.add(notes);

  final homework = Folder('homework');
  homework.add(File('001-你写的代码计算机在做什么.md', 3));
  root.add(homework);

  root.display();
  // + self-evolve/ (29KB)
  //   - README.md (5KB)
  //   - .gitignore (1KB)
  //   + notes/ (20KB)
  //     - ch01-计算机系统漫游.md (8KB)
  //     - ch02-信息的表示和处理.md (12KB)
  //   + homework/ (3KB)
  //     - 001-你写的代码计算机在做什么.md (3KB)
}
```

## Go 代码

```go
package composite

import "fmt"

// 组件接口
type FileComponent interface {
	GetName() string
	GetSize() int
	Display(indent int)
}

// 叶子
type File struct {
	Name string
	Size int
}

func (f *File) GetName() string  { return f.Name }
func (f *File) GetSize() int     { return f.Size }
func (f *File) Display(indent int) {
	fmt.Printf("%s- %s (%dKB)\n", spaces(indent), f.Name, f.Size)
}

// 容器
type Folder struct {
	Name     string
	Children []FileComponent
}

func (f *Folder) GetName() string { return f.Name }
func (f *Folder) GetSize() int {
	total := 0
	for _, c := range f.Children {
		total += c.GetSize()
	}
	return total
}
func (f *Folder) Display(indent int) {
	fmt.Printf("%s+ %s/ (%dKB)\n", spaces(indent), f.Name, f.GetSize())
	for _, c := range f.Children {
		c.Display(indent + 1)
	}
}

func spaces(n int) string {
	s := ""
	for i := 0; i < n; i++ {
		s += "  "
	}
	return s
}

// 使用
// root := &Folder{Name: "self-evolve"}
// root.Children = append(root.Children, &File{Name: "README.md", Size: 5})
// root.Display(0)
```

## Flutter 中的真实应用

- **Widget 树**是组合模式的经典实现。Widget（组件）是接口，Text/Icon（叶子）和 Column/Row/Container（容器）统一实现 Widget 接口
- `RenderObject` 树也是组合模式——`RenderBox` 可以包含子 `RenderBox`

## 什么时候用

- 需要表示"部分-整体"树形结构
- 希望统一处理单个对象和组合对象
- 文件系统、组织架构、UI 组件树、菜单系统

## 什么时候不用

- 结构不是树形的
- 单个对象和组合对象行为差异很大

## 与其他模式的关系

- 组合和**装饰器**结构相似，但目的不同：组合管理子节点集合，装饰器只包装一个对象
- 组合经常和**访问者**配合——遍历树形结构
- Flutter 的 Widget 树同时用了组合和装饰器
