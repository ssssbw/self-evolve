# Self-Evolve

> 终身成长知识库 — 技术深度 × 财富体系 × 认知升级

## 这是什么

这是一个伴随终身迭代的个人成长项目，记录学习轨迹、目标拆解、思考沉淀与行动落地。

## 三大成长维度

| 维度 | 目标 | 当前阶段 |
|------|------|----------|
| 技术 | 顶尖全栈工程师，深刻理解计算机底层 | Flutter 开发者，CS 基础待重建 |
| 理财 | 构建个人资产体系，获得人生选择权 | 入门阶段，已读《富爸爸穷爸爸》 |
| 认知 | 独立思辨，理解人与社会的运行逻辑 | 初学阶段，逻辑学/心理学/博弈论 |

## 目录结构

```
self-evolve/
├── 0-Projects/       # 进行中的学习项目（有明确目标+截止日期）
├── 1-Areas/          # 三大终身维度（技术/理财/认知）
├── 2-Resources/      # 参考资料索引（书单、课程、工具）
├── 3-Archive/        # 已完成的项目归档
├── 4-Journal/        # 周复盘 / 月复盘 / 年度回顾
├── 5-Playground/     # 课后作业 & 思辨讨论
└── .ai/              # AI 上下文（接手指南 + 会话日志）
```

## 快速开始

- **了解全貌**：阅读 `.ai/CONTEXT.md`
- **当前进展**：查看 `0-Projects/_index.md`
- **最近动态**：查看 `4-Journal/` 下最新的复盘文件
- **接续工作**：阅读 `.ai/SESSION-LOG.md`

## Trilium 同步

本仓库通过根目录脚本把 Markdown 单向同步到 Trilium：

```bash
./sync
```

Windows 使用：

```bat
sync.cmd
```

首次使用前，把 `.env.example` 复制为 `.env`，并填写 Trilium 地址、根笔记 ID 和 ETAPI token。`.env` 是本地密钥文件，不提交到 Git。

常用操作：

```bash
./sync --dry-run
```

只预览，不修改 Trilium。

```bash
./sync
```

执行真实同步，更新 Trilium 中对应笔记。

如果本地删除了 Markdown 文件，dry-run 或真实同步可能提示 orphan：

```text
Orphaned Trilium notes were left untouched:
- 2-Resources/example.md
```

这表示 Trilium 中还有旧笔记，但本地源文件已经不存在。确认这些文件确实是自己删除后，可以先预览清理：

```bash
./sync --prune-orphans --dry-run
```

确认列表无误后执行真实清理：

```bash
./sync --prune-orphans
```

清理会删除 Trilium 中对应 orphan 笔记，并从 `.trilium-sync-map.json` 移除映射。默认不带 `--prune-orphans` 时永远不会自动删除 Trilium 笔记。

## 基于 PARA 方法

本项目采用 [PARA](https://fortelabs.com/blog/para/) 方法组织知识：

- **P**rojects — 有截止日期的活跃项目
- **A**reas — 长期维护的领域
- **R**esources — 参考资料
- **A**rchive — 归档内容

## 许可

个人知识库，仅供本人使用。
