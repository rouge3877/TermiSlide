# TermiSlide Terminal Daemon

基于 Python `asyncio` 的多路复用伪终端（PTY）WebSocket 后端服务。为 TermiSlide 前端提供持久化的交互式终端能力。

## 快速开始

```bash
# 安装依赖
cd packages/daemon
pip install -r requirements.txt

# 从项目根目录启动（config 中的路径相对于 cwd 解析）
cd ../../
python packages/daemon/daemon.py demo/terminal/config.yaml
```

默认监听 `ws://0.0.0.0:8765`，可通过环境变量覆盖：

```bash
TERMISLIDE_HOST=127.0.0.1 TERMISLIDE_PORT=9000 python packages/daemon/daemon.py config.yaml
```

## 架构

```
┌──────────────────────────┐         ┌──────────────────────────┐
│  Slidev Frontend         │  JSON   │  Terminal Daemon          │
│                          │  over   │  (Python asyncio)         │
│  ┌────────┬────────────┐ │  WS     │                          │
│  │ Slide  │ WebTerminal│◄├────────►│  ┌─ PTY: shell-basics    │
│  │  .md   │  (xterm.js)│ │         │  │  └─ /bin/bash          │
│  └────────┴────────────┘ │         │  │     output buffer 📋   │
│                          │         │  ├─ PTY: shell-tools      │
│  terminal-split layout   │         │  │  └─ /bin/bash          │
│    env → attach message  │         │  └─ ...                   │
└──────────────────────────┘         └──────────────────────────┘
```

### 核心流程

1. Daemon 启动时解析 `config.yaml`，获取环境名 → 工作目录映射
2. 前端发送 `attach` 时，daemon 为该环境按需衍生 `/bin/bash` PTY
3. PTY 初始化执行 `cd <path> && source .lab.env && clear`
4. 异步读取循环（`loop.add_reader` + epoll）持续读取 PTY 输出
5. 输出存入环形缓冲区（~200KB）并广播给所有绑定的客户端
6. 客户端断开后 PTY **保持运行**，重新 attach 时回放缓冲区恢复画面

## WebSocket 协议

### 客户端 → 服务端

| type | 字段 | 说明 |
|------|------|------|
| `attach` | `env`, `cols`, `rows` | 绑定到指定环境（首次时创建 PTY） |
| `input` | `data` | 转发键盘输入到 PTY stdin |
| `resize` | `cols`, `rows` | 调整 PTY 终端尺寸（ioctl TIOCSWINSZ） |

### 服务端 → 客户端

| type | 字段 | 说明 |
|------|------|------|
| `output` | `data` | PTY 输出（含 attach 时的缓冲回放） |
| `attached` | `env` | 环境绑定确认 |
| `error` | `message` | 错误信息 |

## 配置文件

`config.yaml` 路径相对于 daemon 启动时的工作目录解析：

```yaml
environments:
  - name: "shell-basics"        # 环境名（slides frontmatter 中引用）
    path: "labs/shell-basics"   # 工作目录（相对于 cwd）
```

## Lab 环境

每个 lab 目录可包含：

| 文件 | 作用 |
|------|------|
| `.lab.env` | PTY 初始化时 `source` 的脚本，用于设置 PS1、环境变量等 |
| 其他文件 | 练习素材（供学生在终端中操作） |

`.lab.env` 示例：

```bash
#!/bin/bash
export LAB_NAME="Shell Basics"
export PS1='\[\e[1;36m\]basics\[\e[0m\] \$ '
echo -e "\e[1;32m✔ Lab ready: $LAB_NAME\e[0m"
```

## 前端集成

### Slide 中使用终端

在 Slidev markdown 中使用 `terminal-split` 布局：

```md
---
layout: terminal-split
env: shell-basics
---

# 幻灯片标题

左侧内容，右侧自动显示终端。
```

### 关键前端组件

| 文件 | 说明 |
|------|------|
| `packages/client/layouts/terminal-split.vue` | 左右分栏布局（42% 内容 / 58% 终端） |
| `packages/client/builtin/WebTerminal.vue` | xterm.js 终端组件，WebSocket 通信 |

### 交互细节

- **自动聚焦**：切换到终端页面时自动 focus 终端，可直接输入
- **Shift + ←/→**：即使终端聚焦也能切换幻灯片（通过 `attachCustomKeyEventHandler` 拦截并调用 Slidev `nextSlide()`/`prevSlide()`）
- **缓冲回放**：切回之前的环境时，后端自动回放输出缓冲区，终端画面无缝恢复
- **多客户端**：多个浏览器窗口可同时 attach 到同一 PTY，输出实时广播
- **隐藏滚动条**：终端和左侧内容面板的滚动条均已隐藏
- **代码块自动换行**：左侧面板中的代码块 `pre-wrap`，不产生横向滚动条

## 项目结构

```
TermiSlide/
├── packages/daemon/           # 后端 daemon
│   ├── daemon.py              # Python asyncio WebSocket + PTY 服务
│   ├── requirements.txt       # Python 依赖
│   └── README.md              # 本文件
├── labs/                      # 实验环境（所有 demo 共享）
│   ├── shell-basics/
│   │   ├── .lab.env
│   │   └── sample.txt
│   ├── shell-tools/
│   │   ├── .lab.env
│   │   ├── fruits.txt
│   │   └── project/
│   └── shell-scripts/
│       ├── .lab.env
│       └── mcd.sh
├── demo/terminal/             # Shell Tutorial 幻灯片
│   ├── slides.md
│   ├── config.yaml            # 引用 ../../labs/* 的环境配置
│   └── assets/
└── packages/client/           # Slidev 前端
    ├── layouts/terminal-split.vue
    └── builtin/WebTerminal.vue
```

## 添加新的实验环境

1. 在 `labs/` 下创建目录：
   ```bash
   mkdir labs/my-new-lab
   ```

2. （可选）创建 `.lab.env`：
   ```bash
   echo 'export PS1="\[\e[1;32m\]my-lab\[\e[0m\] \$ "' > labs/my-new-lab/.lab.env
   ```

3. 放入练习文件

4. 在 `config.yaml` 中注册：
   ```yaml
   - name: "my-new-lab"
     path: "labs/my-new-lab"
   ```

5. 在 `slides.md` 中使用：
   ```md
   ---
   layout: terminal-split
   env: my-new-lab
   ---
   ```

## 优雅关闭

单次 `Ctrl+C` 或 `SIGTERM` 即可干净退出：

1. 取消所有 PTY 读取循环
2. 终止所有 PTY 子进程
3. 关闭 WebSocket 服务器
4. 进程退出
