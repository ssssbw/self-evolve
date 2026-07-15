# CSAPP Bomb Lab 攻略指南

> Bomb Lab 是 CSAPP 最经典的实验——你需要拆解一个"炸弹"二进制程序，逆向分析 6 个阶段的正确输入。这是理解汇编和 GDB 的最佳实战。

## Lab 概述

- 目标：分析 bomb 二进制程序的 6 个阶段，找到每个阶段的正确输入
- 工具：GDB（GNU Debugger）、objdump
- 意义：学会读懂真实的 x86-64 汇编代码

## 环境准备

```bash
# 下载 Lab
wget http://csapp.cs.cmu.edu/3e/bomblab.tar
tar -xvf bomblab.tar
cd bomblab

# 查看 bomb 的汇编代码
objdump -d bomb > bomb.asm
# 这个文件是你主要的分析对象！

# 用 GDB 运行（不要直接运行，会引爆！）
gdb bomb
```

## GDB 必备命令

```
# 基础
break main          # 在 main 设断点
break phase_1       # 在 phase_1 设断点
run                 # 运行程序
continue (c)        # 继续运行
step (s)            # 单步执行（进入函数）
next (n)            # 单步执行（不进入函数）
quit                # 退出

# 查看
disas phase_1       # 反汇编 phase_1 函数
print /x $rax       # 以十六进制打印寄存器值
print /s (char*)$rdi # 打印字符串
x/s 0x地址          # 查看内存中的字符串
x/10d 0x地址        # 查看内存中 10 个整数
info registers      # 查看所有寄存器

# 断点管理
info breakpoints    # 查看所有断点
delete 1            # 删除断点 1
```

## 安全策略

**永远不要直接运行 bomb！** 炸弹会扣分。

```bash
# 错误做法
./bomb              # 会引爆！

# 正确做法：先创建答案文件
echo "答案1" > answer.txt
gdb bomb
(gdb) break phase_1
(gdb) run answer.txt
# 在断点处分析，找到答案后写到 answer.txt
```

## 6 个阶段攻略思路

### Phase 1 — 字符串比较

**目标：** 找到程序期望的字符串

**分析方法：**
```bash
# 在 GDB 中
(gdb) break phase_1
(gdb) run
# 输入任意字符串（比如 "test"）

# 反汇编 phase_1
(gdb) disas phase_1
# 你会看到：
#   0x0000 callq <strings_not_equal>
#   0x0000 test %eax,%eax
#   0x0000 je ... (如果相等则跳转，否则爆炸)

# 关键：strings_not_equal 的第一个参数在 %rdi（你的输入）
# 第二个参数在 %rsi（正确答案）
# 在调用 strings_not_equal 之前，查看 %rsi 指向的字符串
(gdb) x/s $rsi
# 打印出来的就是答案！
```

**通用模式：** Phase 1 通常就是找出一个硬编码的字符串。

### Phase 2 — 读取 6 个数字

**目标：** 找到 6 个满足特定条件的数字

**分析方法：**
```bash
(gdb) break phase_2
(gdb) break read_six_numbers
(gdb) continue

# read_six_numbers 会调用 sscanf
# 查看 sscanf 的格式字符串
(gdb) x/s 0x地址
# 通常是 "%d %d %d %d %d %d"

# 然后看 phase_2 的逻辑
(gdb) disas phase_2
# 常见模式：
#   - 检查第一个数是否等于某个值
#   - 循环检查后一个数和前一个数的关系（等差、等比、斐波那契等）
#   - 看 cmp 指令后面跟的立即数
```

### Phase 3 — switch-case 跳转表

**目标：** 根据输入的某个值，匹配到一个分支

**分析方法：**
```bash
(gdb) disas phase_3
# 你会看到：
#   callq sscanf
#   cmp $0x7,某个值     # 检查值是否 <= 7
#   ja 爆炸             # 如果大于7就爆炸
#   jmp *0x地址(,%rax,8) # 跳转表！

# 查看跳转表
(gdb) x/8xg 0x地址    # 查看8个跳转地址
# 每个地址对应一个 case

# 选一个 case，看它期望什么值
# 注意：有些 case 会检查第二个参数
```

### Phase 4 — 递归函数

**目标：** 理解一个递归函数的逻辑

**分析方法：**
```bash
(gdb) disas phase_4
# 通常调用 func4(x)
# 你需要理解 func4 做了什么

# 手动跟踪 func4：
# 看 func4 的汇编，画调用树
# 常见的递归模式：二分查找、阶乘、斐波那契

# 找到 func4 期望的返回值
# 然后"反向求解"输入
```

### Phase 5 — 字符串变换

**目标：** 输入一个字符串，经过某种变换后匹配目标

**分析方法：**
```bash
(gdb) disas phase_5
# 常见模式：
#   取输入字符串每个字符的低 4 位作为索引
#   从一个固定数组中取对应的字符
#   拼接后和目标字符串比较

# 查看固定数组
(gdb) x/16bx 0x地址   # 查看16个字节

# 查看目标字符串
(gdb) x/s 0x地址

# 反向推导：从目标字符串的每个字符，在数组中找到索引
# 这些索引就是输入字符的低4位
```

### Phase 6 — 链表排序

**目标：** 对一个链表进行特定排序

**分析方法：**
```bash
(gdb) disas phase_6
# 这是最复杂的阶段
# 通常涉及：
#   1. 读取6个数字（1-6的排列）
#   2. 根据排列重排链表节点
#   3. 检查链表是否按某个字段排序（升序或降序）

# 查看链表结构
(gdb) x/24xw 0x地址    # 查看链表节点的数据
# 每个节点通常是 {value, next指针}

# 找到每个节点的 value
# 按要求排序（比如降序）
# 输出排序后的节点编号
```

## 通用解题流程

```
1. objdump -d bomb > bomb.asm     # 获取完整汇编
2. gdb bomb                        # 启动调试
3. break phase_X                   # 在目标阶段设断点
4. run answer.txt                  # 运行
5. disas phase_X                   # 反汇编
6. 分析指令逻辑                     # 重点看 cmp, test, jmp
7. 查看内存/寄存器                  # x/s, print
8. 推导答案                         # 写到 answer.txt
9. 重新运行验证                     # 如果爆炸就再来
```

## 心态建议

- **Phase 1-3** 比较简单，1-2 小时能搞定
- **Phase 4-5** 需要耐心跟踪，每题可能 1-3 小时
- **Phase 6** 最难，可能需要 3-5 小时
- **不要跳过**——每解出一个阶段，你的汇编能力就上一个台阶
- **画图**——在纸上画出函数调用流程、链表结构，比盯着屏幕看更有效

## 完成后

- 更新 `plan.md` 中 Bomb Lab 的状态为 ✅
- 记录你的解题过程和心得到 `notes/` 中
- 你现在可以读懂大部分 x86-64 汇编了——这是一个重要的里程碑
