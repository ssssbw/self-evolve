# CSAPP Data Lab 攻略指南

> Data Lab 是 CSAPP 的第一个 Lab，要求你只使用位运算来实现各种功能。不能使用算术运算符、条件语句、循环和函数调用。

## Lab 概述

- 目标：在严格限制下实现 15 个位运算谜题
- 限制：只能用 `! ~ & ^ | + << >>`，不能用 `if/for/while/&&/||`
- 意义：逼迫你真正理解位运算和补码

## 环境准备

```bash
# 下载 Lab
wget http://csapp.cs.cmu.edu/3e/datalab-handout.tar
tar -xvf datalab-handout.tar
cd datalab-handout

# 编译测试
make
./btest    # 测试你的解答
./dlc bits.c  # 检查是否违反操作符限制
```

## 核心技巧

### 技巧 1：用异或判断相等
```c
// 判断 x == y
// 如果 x == y，则 x ^ y == 0
int isEqual(int x, int y) {
    return !(x ^ y);
}
```

### 技巧 2：用掩码提取特定位
```c
// 提取最低字节
int getLSB(int x) {
    return x & 0xFF;
}
```

### 技巧 3：符号扩展
```c
// 如果 x 的最高位是 1，返回全 1；否则返回全 0
// 右移算术：>> 在有符号数上是算术右移（补符号位）
int signBit = x >> 31; // 0x00000000 或 0xFFFFFFFF
```

### 技巧 4：取反加一 = 求负数
```c
// -x = ~x + 1（补码的定义）
int negate(int x) {
    return ~x + 1;
}
```

### 技巧 5：判断是否为 0
```c
// x == 0 返回 1，否则返回 0
// !0 == 1, !nonzero == 0
int isZero(int x) {
    return !x;
}
```

### 技巧 6：获取最小负数 TMin
```c
// TMin = 1 << 31 = 0x80000000 = -2147483648
int tmin(void) {
    return 1 << 31;
}
```

### 技巧 7：获取全 1 掩码
```c
// ~0 = 0xFFFFFFFF = -1
int allOnes = ~0;
```

## 经典题目解析

### 题目 1：bitXor — 只用 & 和 ~ 实现 ^
```c
/*
 * bitXor - x^y using only ~ and &
 *   Example: bitXor(4, 5) = 1
 *   Legal ops: ~ &
 *   Max ops: 14
 */
int bitXor(int x, int y) {
    // 异或 = "不同为1"
    // ~(x & y) = 不是"都是1"的位
    // ~(~x & ~y) = 不是"都是0"的位
    // 两个条件的 AND = 异或
    return ~(x & y) & ~(~x & ~y);
}
```

**推导过程：**
- `x ^ y` 的真值表：00→0, 01→1, 10→1, 11→0
- 本质是"不是同时为0，也不是同时为1"
- `~(~x & ~y)` = 不是同时为0 → 结果为 0x1, 1x, x0, 11
- `~(x & y)` = 不是同时为1 → 结果为 00, 01, 10, x0
- 两者 AND → 01, 10 → 正好是异或

### 题目 2：tmax — 返回最大正整数
```c
/*
 * tmax - return maximum two's complement integer
 *   Legal ops: ! ~ & ^ | +
 *   Max ops: 4
 */
int tmax(void) {
    // TMax = 0x7FFFFFFF = ~(1 << 31)
    return ~(1 << 31);
}
```

### 题目 3：isNegative — 判断是否为负数
```c
/*
 * isNegative - return 1 if x < 0, return 0 otherwise
 *   Example: isNegative(-1) = 1
 *   Legal ops: ! ~ & ^ | +
 *   Max ops: 6
 */
int isNegative(int x) {
    // 右移31位得到符号位：负数返回1，正数返回0
    return (x >> 31) & 1;
}
```

### 题目 4：addOK — 判断加法是否溢出
```c
/*
 * addOK - Determine if can compute x+y without overflow
 *   Example: addOK(0x80000000,0x80000000) = 0
 *   Legal ops: ! ~ & ^ | +
 *   Max ops: 20
 */
int addOK(int x, int y) {
    int sum = x + y;
    int x_sign = (x >> 31) & 1;
    int y_sign = (y >> 31) & 1;
    int s_sign = (sum >> 31) & 1;

    // 溢出条件：两个正数相加变负，或两个负数相加变正
    // 即 x 和 y 同号，但 sum 和它们不同号
    // 用异或判断不同：x_sign ^ y_sign == 0 表示同号
    int same_sign = !(x_sign ^ y_sign);  // x 和 y 同号
    int diff_sign = x_sign ^ s_sign;      // x 和 sum 不同号
    return !(same_sign & diff_sign);      // 同号且结果不同号 = 溢出
}
```

### 题目 5：logicalShift — 用算术右移实现逻辑右移
```c
/*
 * logicalShift - shift x to the right by n, using a logical shift
 *   Can assume that 0 <= n <= 31
 *   Examples: logicalShift(0x87654321,4) = 0x08765432
 *   Legal ops: ! ~ & ^ | +
 *   Max ops: 20
 */
int logicalShift(int x, int n) {
    // 算术右移会在高位补符号位
    // 需要用掩码把高位清零
    // 掩码：低位 n 个 1，高位全 0
    // mask = ~(((1 << 31) >> n) << 1) 但这太复杂

    // 更好的方法：
    // mask = ~(~0 << (32 + ~n + 1))... 也不对

    // 简洁方案：
    int mask = ~(((1 << 31) >> n) << 1);
    return (x >> n) & mask;
}
```

## 调试技巧

1. **用 printf 打印中间值的十六进制**：`printf("x = %x\n", x);`
2. **从简单的开始**：先做 bitXor、tmax、isNegative 这类 2-4 行的题
3. **在纸上画真值表**：位运算用真值表推导最清晰
4. **善用 Python 验证**：在 Python 中快速测试位运算结果
5. **操作符计数**：`./dlc -e bits.c` 显示每题用了几个操作符

## 常见错误

- 忘记右移有算术/逻辑之分（C 中有符号数右移是算术右移）
- 掩码构造错误（左移32位是未定义行为）
- 用了不允许的操作符（仔细看每题的 Legal ops）

## 完成标准

- `./btest` 全部通过
- `./dlc bits.c` 无违规
- 操作符数量在限制内
- 能解释每一行代码为什么这样写

## 下一步

完成 Data Lab 后，你对位运算的理解会有质的飞跃。这会直接帮助你在第 2 章的学习中事半功倍。完成后更新 `plan.md` 中 Data Lab 的状态为 ✅。
