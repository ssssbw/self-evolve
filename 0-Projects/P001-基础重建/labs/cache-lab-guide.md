# CSAPP Cache Lab 攻略指南

> Cache Lab 要求你实现一个缓存模拟器（Part A）和优化矩阵转置的缓存命中率（Part B）。

## Lab 概述

- Part A：用 C 实现一个缓存模拟器，读取内存访问 trace，统计命中/缺失/驱逐次数
- Part B：优化矩阵转置函数，最小化缓存缺失次数
- 核心：深入理解第 6 章的缓存映射方式

## 环境准备

```bash
# 下载
wget http://csapp.cs.cmu.edu/3e/cachelab-handout.tar
tar -xvf cachelab-handout.tar
cd cachelab-handout

# 编译
make

# 测试 Part A
./csim -s 4 -E 1 -b 4 -t traces/yi.trace

# 测试 Part B
./test-trans -M 32 -N 32
```

## Part A — 缓存模拟器

### 目标
模拟一个 S 组、E 行/组、B 字节/行的缓存，统计：
- **hits**：缓存命中
- **misses**：缓存缺失
- **evictions**：驱逐（缓存满时替换）

### 核心数据结构

```c
// 用结构体表示一个缓存行
typedef struct {
    int valid;       // 有效位
    int tag;         // 标记位
    int lru_counter; // LRU 计数器（用于替换策略）
} cache_line;

// 缓存 = 多组 × 多行
cache_line **cache; // cache[set_index][line_index]
```

### 地址分解

```
地址（64位）被分解为：
+--------+-----------+--------+
|  tag   | set index | offset |
+--------+-----------+--------+
|  t 位   |   s 位     |  b 位   |
| 64-s-b |   s 位     |  b 位   |
```

```c
// 从地址提取各部分
int set_index = (address >> b) & ((1 << s) - 1);
int tag = address >> (s + b);
```

### 核心逻辑（伪代码）

```c
void access_cache(int set_index, int tag) {
    // 1. 在目标组中查找 tag
    for (int i = 0; i < E; i++) {
        if (cache[set_index][i].valid && cache[set_index][i].tag == tag) {
            // 命中！更新 LRU
            hits++;
            update_lru(set_index, i);
            return;
        }
    }
    
    // 2. 未命中
    misses++;
    
    // 3. 找一个空行或驱逐最久未用的行
    int victim = find_lru_line(set_index);
    if (cache[set_index][victim].valid) {
        evictions++; // 有有效行被替换
    }
    
    // 4. 加载新行
    cache[set_index][victim].valid = 1;
    cache[set_index][victim].tag = tag;
    update_lru(set_index, victim);
}
```

### LRU 实现

```c
// 简单方案：用一个全局计数器
int global_counter = 0;

void update_lru(int set, int line) {
    cache[set][line].lru_counter = ++global_counter;
}

int find_lru_line(int set) {
    int min_counter = cache[set][0].lru_counter;
    int min_index = 0;
    for (int i = 1; i < E; i++) {
        if (cache[set][i].lru_counter < min_counter) {
            min_counter = cache[set][i].lru_counter;
            min_index = i;
        }
    }
    return min_index;
}
```

### 解析命令行参数

```c
// 用 getopt 解析：-s 4 -E 1 -b 4 -t tracefile
int s, E, b;
char *tracefile;
// getopt 处理...
```

### 解析 trace 文件

```c
// trace 格式：[空格] 操作 地址,大小
// 操作：I（指令）、L（读）、S（写）、M（修改=读+写）
// I 忽略，L/S 算一次访问，M 算两次（先读后写）
```

## Part B — 矩阵转置优化

### 目标
在 32×32、64×64、61×67 三种矩阵上，最小化缓存缺失次数。

### 缓存参数（已知）
- s=5, E=1, b=5（直接映射缓存）
- 32 组，每行 32 字节 = 8 个 int
- 总容量 = 32 × 1 × 32 = 1024 字节

### 为什么矩阵转置会缓存缺失多？

```c
// naive 转置
void transpose(int M, int N, int A[N][M], int B[M][N]) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < M; j++) {
            B[j][i] = A[i][j]; // A 行优先读取，B 列优先写入
        }
    }
}
// B 的列优先写入导致冲突缺失（不同行映射到同一组）
```

### 优化 1：分块（Blocking）

**核心思想：** 把大矩阵分成小块，让小块适配缓存。

```c
// 32×32 矩阵，8×8 分块
void transpose_32x32(int A[32][32], int B[32][32]) {
    for (int ii = 0; ii < 32; ii += 8) {      // 块行
        for (int jj = 0; jj < 32; jj += 8) {  // 块列
            for (int i = ii; i < ii + 8; i++) {
                for (int j = jj; j < jj + 8; j++) {
                    B[j][i] = A[i][j];
                }
            }
        }
    }
}
```

**为什么 8×8？**
- 缓存行 = 32 字节 = 8 个 int
- 8×8 块 = 64 个 int = 256 字节
- 一块的 A 和 B 共 512 字节 < 1024 字节缓存容量
- 所以 8×8 块可以完全放入缓存！

### 优化 2：利用局部变量

```c
// 用局部变量暂存一行，减少对 B 的写入次数
void transpose_optimized(int A[32][32], int B[32][32]) {
    for (int ii = 0; ii < 32; ii += 8) {
        for (int jj = 0; jj < 32; jj += 8) {
            for (int i = ii; i < ii + 8; i++) {
                // 一次读 A 的一行，存到局部变量
                int a0 = A[i][jj];
                int a1 = A[i][jj+1];
                int a2 = A[i][jj+2];
                int a3 = A[i][jj+3];
                int a4 = A[i][jj+4];
                int a5 = A[i][jj+5];
                int a6 = A[i][jj+6];
                int a7 = A[i][jj+7];
                
                // 一次写 B 的一行
                B[jj][i]   = a0;
                B[jj+1][i] = a1;
                B[jj+2][i] = a2;
                B[jj+3][i] = a3;
                B[jj+4][i] = a4;
                B[jj+5][i] = a5;
                B[jj+6][i] = a6;
                B[jj+7][i] = a7;
            }
        }
    }
}
```

### 优化 3：64×64 需要 4×4 分块

64×64 矩阵比缓存大一倍，8×8 分块会冲突。需要更精细的策略：
- 先在 8×8 块内做 4×4 子块转置
- 利用局部变量暂存中间结果

### 调试技巧

```bash
# 查看你的函数的缓存统计
./csim -v -s 5 -E 1 -b 5 -t trace.txt

# 用 valgrind 检查内存错误
valgrind ./csim -s 4 -E 1 -b 4 -t traces/yi.trace
```

## 完成标准

- Part A：`./csim` 输出与参考实现一致
- Part B：32×32 miss < 300，64×64 miss < 1300，61×67 miss < 2000

## 你会学到什么

- 缓存的精确实现在长什么样
- 分块（Blocking/Tiling）是高性能计算最核心的优化手段
- 为什么 CSAPP 第 6 章说"缓存命中率决定性能"
