# TermiSlide

**在幻灯片中嵌入实时交互终端** — 基于 [Slidev](https://sli.dev) 的 fork，集成持久化 PTY 终端，专为教学演示、系统课程和 Workshop 设计。

```
┌──────────────────────────────────────────────────────┐
│  ┌─────────────────────┬───────────────────────────┐  │
│  │                     │                           │  │
│  │   # Shell Basics    │  basics $ ls              │  │
│  │                     │  file.txt  dir/            │  │
│  │   ```bash           │  basics $ echo "hello"    │  │
│  │   echo $0           │  hello                    │  │
│  │   ```               │  basics $ _               │  │
│  │                     │                           │  │
│  │   Slide Content     │   Live Terminal (xterm.js) │  │
│  └─────────────────────┴───────────────────────────┘  │
│            Shift+←/→ 切换幻灯片                        │
└──────────────────────────────────────────────────────┘
```

## 核心特性

- **实时终端** — 幻灯片右侧嵌入真实的 `/bin/bash` 终端，学生可直接操作
- **PTY 常驻** — 切换页面或断开连接后终端进程不销毁，回来时自动恢复画面
- **环境隔离** — 每个 lab 环境独立的 bash 进程、工作目录、环境变量
- **多环境切换** — 不同幻灯片可绑定不同的终端环境，无缝切换
- **Shift+Arrow 换页** — 终端聚焦状态下也能通过 Shift+←/→ 切换幻灯片
- **自动聚焦** — 切换到终端页面时自动 focus，可直接输入

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

前端通过 WebSocket (JSON) 与后端 Python Daemon 通信。Daemon 基于 `asyncio` + `ptyprocess`，使用 `epoll` 异步读取 PTY 输出，通过 ~200KB 环形缓冲区实现断线重连时的画面恢复。

## 快速开始

### 环境要求

- **Node.js** ≥ 18 + **pnpm**
- **Python** ≥ 3.10
- Linux / macOS（需要 PTY 支持）

### 一键启动

```bash
# 克隆项目
git clone <repo-url> TermiSlide
cd TermiSlide

# 安装前端依赖
pnpm install

# 一键启动后端 + 前端
./start.sh
```

启动后访问 http://localhost:3030 即可看到带终端的幻灯片。

### 分别启动（推荐开发时使用）

```bash
# 终端 1：启动后端 daemon
./start.sh daemon

# 终端 2：启动前端
./start.sh frontend
```

### 自定义端口

```bash
TERMISLIDE_PORT=9000 ./start.sh
```

## 幻灯片中使用终端

在 Slidev markdown 中使用 `terminal-split` 布局，通过 `env` 指定终端环境：

```md
---
layout: terminal-split
env: shell-basics
---

# 幻灯片标题

左侧展示教学内容，右侧自动嵌入终端。

学生可以在右侧终端中练习命令：

\`\`\`bash
echo "hello world"
ls -la
\`\`\`
```

## 环境配置

终端环境在 `config.yaml` 中定义：

```yaml
environments:
  - name: "shell-basics"
    path: "../../labs/shell-basics"    # 相对于 config.yaml 所在目录

  - name: "shell-tools"
    path: "../../labs/shell-tools"
```

每个 lab 目录可以包含 `.lab.env` 初始化脚本，PTY 启动时自动 source：

```bash
# labs/shell-basics/.lab.env
export LAB_NAME="Shell Basics"
export PS1='\[\e[1;36m\]basics\[\e[0m\] \$ '
echo -e "\e[1;32m✔ Lab ready: $LAB_NAME\e[0m"
```

## 添加新环境

1. 创建 lab 目录和初始化脚本：
   ```bash
   mkdir labs/my-lab
   echo 'export PS1="\[\e[1;32m\]my-lab\[\e[0m\] \$ "' > labs/my-lab/.lab.env
   ```

2. 在 `config.yaml` 中注册：
   ```yaml
   - name: "my-lab"
     path: "../../labs/my-lab"
   ```

3. 在幻灯片中使用：
   ```md
   ---
   layout: terminal-split
   env: my-lab
   ---
   ```

## 项目结构

```
TermiSlide/
├── packages/
│   ├── daemon/                # 后端 PTY daemon
│   │   ├── daemon.py          # asyncio WebSocket + PTY 服务
│   │   ├── requirements.txt   # Python 依赖 (websockets, ptyprocess, PyYAML)
│   │   └── README.md          # 后端详细文档
│   └── client/                # Slidev 前端 (Vue 3)
│       ├── layouts/
│       │   └── terminal-split.vue   # 左右分栏布局 (42% 内容 / 58% 终端)
│       └── builtin/
│           └── WebTerminal.vue      # xterm.js 终端组件
├── labs/                      # 实验环境目录
│   ├── shell-basics/
│   ├── shell-tools/
│   └── shell-scripts/
├── demo/terminal/             # 示例幻灯片 (Shell Tutorial)
│   ├── slides.md
│   ├── config.yaml
│   └── assets/
├── start.sh                   # 一键启动脚本
└── SLIDEV_README.md           # 上游 Slidev 原始 README
```

## WebSocket 协议

| 方向 | type | 字段 | 说明 |
|------|------|------|------|
| C→S | `attach` | `env`, `cols`, `rows` | 绑定环境（首次时创建 PTY） |
| C→S | `input` | `data` | 转发键盘输入到 PTY |
| C→S | `resize` | `cols`, `rows` | 调整终端尺寸 |
| S→C | `output` | `data` | PTY 输出（含缓冲回放） |
| S→C | `attached` | `env` | 绑定确认 |
| S→C | `error` | `message` | 错误信息 |

## 关键机制

### 缓冲回放

每个 PTY 维护 ~200KB 环形输出缓冲区。客户端 attach 到已有 PTY 时，daemon 一次性回放全部缓冲内容，使终端画面无缝恢复。

### Resize 所有权

当多个客户端共享同一环境时，仅最近活跃的客户端（最后 attach 或发送过 input 的客户端）拥有 resize 控制权，防止多窗口 resize 冲突导致光标错位。

### 优雅关闭

`Ctrl+C` 或 `SIGTERM` 触发：取消所有 PTY 读取循环 → 终止 PTY 子进程 → 关闭 WebSocket 服务器。

## 基于 Slidev

TermiSlide 基于 [Slidev](https://sli.dev) 构建，保留了 Slidev 的所有功能（Markdown 幻灯片、主题、动画、导出等）。上游 Slidev 的完整文档参见 [SLIDEV_README.md](./SLIDEV_README.md) 和 [sli.dev](https://sli.dev)。

## License

[MIT](./LICENSE)
