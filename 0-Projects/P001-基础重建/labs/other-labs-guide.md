# CSAPP Shell Lab / Malloc Lab / Proxy Lab 攻略指南

> 剩余三个 Lab 的思路指导。完成顺序：Shell Lab → Malloc Lab → Proxy Lab

---

## Shell Lab — 实现一个简易 Shell

### 目标
实现 `tsh.c`（tiny shell），支持：作业控制、前台/后台执行、信号处理

### 核心知识点（对应第 8 章）
- fork/exec/waitpid 进程管理
- SIGCHLD/SIGINT/SIGTSTP 信号处理
- 作业管理（前台/后台/停止）
- 竞态条件处理

### 实现框架

```c
void eval(char *cmdline) {
    // 1. 解析命令行
    int bg = parseline(cmdline, argv);
    
    // 2. 忽略空行和内置命令
    if (argv[0] == NULL) return;
    if (builtin_command(argv)) return; // quit, jobs, bg, fg
    
    // 3. 阻塞 SIGCHLD（防止 fork 后、addjob 前子进程结束）
    sigset_t mask;
    sigaddset(&mask, SIGCHLD);
    sigprocmask(SIG_BLOCK, &mask, NULL);
    
    // 4. fork 子进程
    if (fork() == 0) {
        // 子进程：解除阻塞，设置进程组，执行命令
        sigprocmask(SIG_UNBLOCK, &mask, NULL);
        setpgid(0, 0); // 新进程组
        execve(argv[0], argv, environ);
        exit(1); // execve 失败
    }
    
    // 5. 父进程：添加作业，解除阻塞
    addjob(...);
    sigprocmask(SIG_UNBLOCK, &mask, NULL);
    
    // 6. 前台作业等待完成
    if (!bg) waitfg(pid);
}
```

### 信号处理函数

```c
void sigchld_handler(int sig) {
    int status;
    pid_t pid;
    // WNOHANG: 非阻塞，WUNTRACED: 检测停止的子进程
    while ((pid = waitpid(-1, &status, WNOHANG | WUNTRACED)) > 0) {
        if (WIFEXITED(status) || WIFSIGNALED(status)) {
            deletejob(pid); // 子进程结束或被杀死
        } else if (WIFSTOPPED(status)) {
            // 子进程被停止（Ctrl+Z）
            // 修改作业状态为 stopped
        }
    }
}
```

### 关键陷阱
- **竞态条件**：fork 后必须先阻塞 SIGCHLD，否则 addjob 前子进程可能已结束
- **waitpid 循环**：用 while 而不是 if，因为可能多个子进程同时结束
- **进程组**：子进程必须 `setpgid(0, 0)` 否则信号会发给整个 shell

---

## Malloc Lab — 实现一个内存分配器

### 目标
实现 `malloc/free/realloc`，管理一个隐式/显式空闲链表

### 核心知识点（对应第 9 章）
- 虚拟内存的按需分配
- 空闲链表管理
- 首次适配/最佳适配/下次适配
- 合并（coalescing）和分割（splitting）

### 实现方案选择

| 方案 | 难度 | 性能 | 推荐顺序 |
|------|------|------|----------|
| 隐式空闲链表 | 简单 | 慢 | 第一个实现 |
| 显式空闲链表 | 中等 | 较快 | 第二个实现 |
| 分离空闲链表 | 较难 | 快 | 追求高分 |

### 隐式空闲链表（入门方案）

```c
// 每个块的结构：
// [header: size|alloc] [payload...] [footer: size|alloc]（可选）
// header 中最低位表示是否已分配

#define GET(p) (*(unsigned int *)(p))
#define PUT(p, val) (*(unsigned int *)(p) = (val))
#define GET_SIZE(p) (GET(p) & ~0x7) // 低 3 位是标志
#define GET_ALLOC(p) (GET(p) & 0x1)
#define PACK(size, alloc) ((size) | (alloc))

// 找到下一个块
#define NEXT_BLKP(bp) ((char *)(bp) + GET_SIZE((char *)(bp) - WSIZE))

void *malloc(size_t size) {
    // 1. 对齐 size（8 字节对齐）
    size = ALIGN(size);
    
    // 2. 遍历空闲链表，找第一个够大的块（首次适配）
    void *bp = find_fit(size);
    
    // 3. 找到了 → 分割并放置
    if (bp) {
        place(bp, size);
        return bp;
    }
    
    // 4. 没找到 → 扩展堆
    size_t extendsize = MAX(size, CHUNKSIZE);
    bp = extend_heap(extendsize);
    place(bp, size);
    return bp;
}

void free(void *bp) {
    // 1. 标记为未分配
    size_t size = GET_SIZE(HDRP(bp));
    PUT(HDRP(bp), PACK(size, 0));
    PUT(FTRP(bp), PACK(size, 0));
    
    // 2. 合并相邻空闲块
    coalesce(bp);
}
```

### 合并策略

```c
void *coalesce(void *bp) {
    // 检查前后块的分配状态（4 种情况）
    int prev_alloc = GET_ALLOC(FTRP(PREV_BLKP(bp)));
    int next_alloc = GET_ALLOC(HDRP(NEXT_BLKP(bp)));
    size_t size = GET_SIZE(HDRP(bp));
    
    if (prev_alloc && next_alloc) {
        // 前后都分配了 → 不合并
    } else if (prev_alloc && !next_alloc) {
        // 后面空闲 → 和后面合并
        size += GET_SIZE(HDRP(NEXT_BLKP(bp)));
        PUT(HDRP(bp), PACK(size, 0));
        PUT(FTRP(bp), PACK(size, 0));
    } else if (!prev_alloc && next_alloc) {
        // 前面空闲 → 和前面合并
        // ...
    } else {
        // 前后都空闲 → 三块合一
        // ...
    }
    return bp;
}
```

### 关键陷阱
- **对齐**：所有块大小必须是 8/16 字节对齐
- **最小块大小**：header + footer + 最小 payload = 至少 16 字节
- **边界条件**：堆起始和结束的特殊处理
- **realloc 优化**：如果下一个块是空闲的，可以扩展而不是重新分配

---

## Proxy Lab — 实现一个 HTTP 代理服务器

### 目标
实现一个支持并发、缓存的小型 HTTP 代理

### 核心知识点（对应第 11-12 章）
- Socket 编程（connect/accept/read/write）
- HTTP 协议解析
- 并发：线程（推荐）或 I/O 多路复用
- 缓存：LRU 缓存 web 对象

### 实现框架

```c
int main(int argc, char **argv) {
    int listenfd = Open_listenfd(argv[1]); // 监听端口
    
    while (1) {
        struct sockaddr_in clientaddr;
        int clientlen = sizeof(clientaddr);
        int *connfd = Malloc(sizeof(int));
        *connfd = Accept(listenfd, (SA *)&clientaddr, &clientlen);
        
        // 并发：为每个连接创建线程
        pthread_t tid;
        Pthread_create(&tid, NULL, thread, connfd);
    }
}

void *thread(void *vargp) {
    int fd = *((int *)vargp);
    Pthread_detach(pthread_self()); // 分离线程，自动回收
    Free(vargp);
    
    // 1. 读取客户端 HTTP 请求
    // 2. 解析请求行（GET http://xxx HTTP/1.1）
    // 3. 检查缓存 → 命中则直接返回
    // 4. 未命中 → 连接目标服务器，转发请求
    // 5. 读取响应，缓存，转发给客户端
    // 6. 关闭连接
    Close(fd);
    return NULL;
}
```

### 请求解析

```c
// 客户端请求格式：
// GET http://www.example.com/index.html HTTP/1.1
// Host: www.example.com
// ...（其他 header）

// 需要解析出：method, host, port, path
void parse_uri(char *uri, char *host, char *port, char *path) {
    // 跳过 http://
    char *hoststart = strstr(uri, "://") + 3;
    
    // 提取 host:port
    char *pathstart = strchr(hoststart, '/');
    *pathstart = '\0';
    strcpy(host, hoststart);
    *pathstart = '/';
    strcpy(path, pathstart);
    
    // 检查是否有端口
    char *portstart = strchr(host, ':');
    if (portstart) {
        *portstart = '\0';
        strcpy(port, portstart + 1);
    } else {
        strcpy(port, "80");
    }
}
```

### 缓存实现

```c
// 简单 LRU 缓存
typedef struct cache_node {
    char *url;              // 缓存键
    char *data;             // 缓存数据
    size_t size;            // 数据大小
    struct cache_node *prev, *next; // 双向链表
    int readers;            // 读者计数（读写锁）
} cache_node;

// 缓存操作（线程安全）
cache_node *cache_find(char *url);       // 查找
void cache_add(char *url, char *data, size_t size); // 添加
void cache_evict(size_t needed);         // 驱逐
```

### 关键陷阱
- **线程安全**：缓存操作必须加锁（读写锁更高效）
- **HTTP 解析**：注意 header 的换行是 `\r\n`，不是 `\n`
- **连接管理**：记得关闭所有 socket
- **短读取**：read 可能返回不完整数据，需要循环读取
- **Rio 包**：使用 CSAPP 提供的 Robust I/O 函数处理短读取

---

## Lab 完成顺序建议

```
Data Lab (第 2 周)
    ↓
Bomb Lab (第 3 周)
    ↓
Cache Lab (第 4 周)
    ↓
Shell Lab (第 8 章学完后)
    ↓
Malloc Lab (第 9 章学完后)
    ↓
Proxy Lab (第 11-12 章学完后)
```

前三个 Lab 和首月学习日历同步，后三个 Lab 在学完对应章节后启动。
