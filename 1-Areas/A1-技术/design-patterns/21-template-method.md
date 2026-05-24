# 模板方法模式（Template Method）

## 一句话

在基类中定义算法骨架，将某些步骤延迟到子类实现。

## Dart 代码

```dart
abstract class DataParser {
  // 模板方法——定义算法骨架（final 防止子类覆盖）
  void parse(String source) {
    final raw = readData(source);
    final processed = processData(raw);
    final result = formatOutput(processed);
    print(result);
  }

  // 具体步骤由子类实现
  String readData(String source);
  String processData(String raw);
  String formatOutput(String processed);
}

class JsonParser extends DataParser {
  @override
  String readData(String source) => 'JSON原始数据: $source';
  @override
  String processData(String raw) => raw.toUpperCase();
  @override
  String formatOutput(String processed) => '解析结果: $processed';
}

class XmlParser extends DataParser {
  @override
  String readData(String source) => 'XML原始数据: $source';
  @override
  String processData(String raw) => raw.split('').reversed.join();
  @override
  String formatOutput(String processed) => '<result>$processed</result>';
}

void main() {
  JsonParser().parse('{"name":"hello"}');
  XmlParser().parse('<name>world</name>');
}
```

## Go 代码

```go
package template

import "fmt"

// Go 没有继承，用组合 + 接口模拟
type DataParser interface {
	ReadData(source string) string
	ProcessData(raw string) string
	FormatOutput(processed string) string
}

func Parse(p DataParser, source string) {
	raw := p.ReadData(source)
	processed := p.ProcessData(raw)
	result := p.FormatOutput(processed)
	fmt.Println(result)
}

type JsonParser struct{}
func (j *JsonParser) ReadData(source string) string { return "JSON: " + source }
func (j *JsonParser) ProcessData(raw string) string  { return raw }
func (j *JsonParser) FormatOutput(p string) string   { return "结果: " + p }
```

## Flutter 中的真实应用

- **StatefulWidget.createState()** — 框架定义了 Widget 的生命周期骨架（createElement → mount → build → update → unmount），具体每个阶段做什么由你的 State 子类决定
- **InheritedWidget.updateShouldNotify()** — 框架定义了何时重建子树，你定义判断条件

## 什么时候用 / 不用

- 用：算法骨架固定，但某些步骤需要定制；代码复用
- 不用：算法没有固定骨架，或每个步骤都不同

## 与其他模式的关系

- 模板方法用**继承**，**策略**用组合——策略更灵活
- 模板方法是**工厂方法**的超集（工厂方法是模板方法的一种）
