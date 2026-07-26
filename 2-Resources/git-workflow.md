# Git 工作流指南 — self-evolve 项目专用

> 你在多台电脑上更新这个知识库，需要一套简单可靠的工作流。

---

## 日常操作

### 开始工作前（每次打开电脑）

Windows PowerShell（默认目录）：

```powershell
Set-Location 'D:\self-evolve'
git pull
```

macOS Terminal（默认目录）：

```bash
cd "$HOME/self-evolve"
git pull
```

如果仓库不在默认目录，进入实际克隆位置后执行相同的 Git 命令。

### 完成一天的学习后

```bash
# 查看改了什么
git status
git diff

# 添加所有改动
git add -A

# 提交（写清楚做了什么）
git commit -m "feat: 完成 CSAPP 第 2 章笔记"

# 推送到远程
git push
```

---

## 提交信息规范

| 前缀 | 用途 | 例子 |
|------|------|------|
| `feat:` | 新增内容 | `feat: 添加第 3 章学习笔记` |
| `update:` | 更新已有内容 | `update: 补充第 2 章浮点数部分` |
| `fix:` | 修正错误 | `fix: 修正补码公式错误` |
| `review:` | 复盘记录 | `review: 2026-W18 周复盘` |
| `homework:` | 作业 | `homework: 完成 #001 作业` |

---

## 多设备协作

### 场景：公司电脑写了笔记，回家继续

```
公司电脑：
  git add -A
  git commit -m "feat: CSAPP ch02 笔记"
  git push

家里电脑：
  git pull                    # 拉取公司电脑的提交
  （继续学习...）
  git add -A
  git commit -m "feat: 工厂模式练习"
  git push
```

### 冲突处理

如果两台电脑改了同一个文件：

```bash
git pull
# 如果有冲突，会提示哪些文件冲突了
# 打开冲突文件，手动选择保留哪个版本
# 然后提交
git add -A
git commit -m "fix: 解决合并冲突"
git push
```

**预防冲突的最好方法：** 每次结束工作都 `git push`，每次开始工作都 `git pull`。

---

## 和 AI 协作时

### AI 帮你改了文件后

```bash
git status      # 查看 AI 改了什么
git diff        # 看具体改动
git add -A
git commit -m "feat: AI 协助添加 xxx"
git push
```

### AI 的改动你不满意

```bash
# 撤销 AI 的改动，回到上一个提交
git checkout .
# 或者只撤销某个文件
git checkout -- path/to/file.md
```

---

## 常用命令速查

| 命令 | 用途 |
|------|------|
| `git status` | 查看当前状态 |
| `git diff` | 查看具体改动 |
| `git add -A` | 添加所有改动 |
| `git commit -m "msg"` | 提交 |
| `git push` | 推送到远程 |
| `git pull` | 拉取远程更新 |
| `git log --oneline -10` | 查看最近 10 条提交 |
| `git checkout .` | 撤销所有未提交的改动 |
| `git stash` | 暂存当前改动 |
| `git stash pop` | 恢复暂存的改动 |
