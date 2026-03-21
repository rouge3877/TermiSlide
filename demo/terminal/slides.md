---
theme: default
title: TermiSlide 交互式终端教学演示
---

# TermiSlide

用 Slidev 幻灯片驱动的交互式终端教学平台

<div class="mt-8 text-gray-400">

- 📝 左侧 Markdown 讲义，右侧实时终端
- 🔄 每张幻灯片可绑定独立的终端环境
- 💾 切换幻灯片后终端状态自动保留

</div>

<div class="abs-br m-8 text-sm text-gray-500">
  按 → 开始
</div>

---
layout: terminal-split
env: linux-basics
---

# Lab 1: Linux 基础

右侧是一个真实的 Bash 终端，试试这些命令：

```bash
ls -la
cat sample.txt
wc -l sample.txt
```

<v-click>

### 文本搜索

使用 `grep` 查找内容：

```bash
grep "lucky" sample.txt
grep -n "Line" sample.txt
```

</v-click>

<v-click>

### 管道操作

```bash
cat sample.txt | head -5
cat sample.txt | tail -3
```

</v-click>

---
layout: terminal-split
env: linux-basics
---

# Lab 1 续: 文件操作

还是同一个 **linux-basics** 环境 ——
你之前的命令历史和文件修改都还在！

试试创建和操作文件：

```bash
echo "Hello TermiSlide" > myfile.txt
cat myfile.txt
cp myfile.txt myfile_backup.txt
ls -la *.txt
```

<v-click>

### 进程查看

```bash
ps aux | head -10
whoami
pwd
```

</v-click>

---
layout: terminal-split
env: git-practice
---

# Lab 2: Git 练习

终端已自动切换到 **git-practice** 环境。

初始化一个 Git 仓库：

```bash
git init my-project
cd my-project
```

<v-click>

### 创建第一个提交

```bash
echo "# My Project" > README.md
git add README.md
git commit -m "Initial commit"
git log --oneline
```

</v-click>

---
layout: terminal-split
env: linux-basics
---

# 回到 Lab 1

切回 **linux-basics** 环境 — 注意终端自动恢复了之前的状态！

之前创建的文件应该还在：

```bash
ls *.txt
cat myfile.txt
```

<div class="mt-8 p-4 bg-blue-500/10 rounded">

💡 **核心特性**: 后端为每个环境维护独立的 PTY 进程和输出缓冲区。
切换环境时，终端画面通过缓冲回放自动恢复，实现无缝的上下文切换。

</div>

---

# 架构总览

```
┌─────────────────────┐           ┌──────────────────────────┐
│  Slidev Frontend    │ WebSocket │  TermiSlide Backend      │
│                     │◄─────────►│  (Python asyncio daemon) │
│  ┌───────┬────────┐ │   JSON    │                          │
│  │ Slide │ xterm  │ │  frames   │  ┌─ PTY: linux-basics    │
│  │ .md   │ .js    │ │           │  │  └─ /bin/bash (PID x) │
│  └───────┴────────┘ │           │  │     output buffer 📋  │
│                     │           │  │                        │
│  env: linux-basics ─┼─ attach ─►│  ├─ PTY: git-practice    │
│  键盘输入 ──────────┼─ input ──►│  │  └─ /bin/bash (PID y) │
│  窗口变化 ──────────┼─ resize ─►│  │     output buffer 📋  │
│  终端输出 ◄─────────┼─ output ──│  │                        │
│  错误提示 ◄─────────┼─ error ───│  └─ ...                  │
└─────────────────────┘           └──────────────────────────┘
```

**协议帧**:
| 方向 | type | 用途 |
|------|------|------|
| → | `attach` | 绑定/切换到指定环境 |
| → | `input` | 转发键盘输入到 PTY |
| → | `resize` | 同步终端尺寸 |
| ← | `output` | PTY 输出（含缓冲回放）|
| ← | `attached` | 环境绑定确认 |
| ← | `error` | 错误信息 |

