---
theme: default
title: TermiSlide Demo
---

# TermiSlide

Interactive terminal slides for developers

Press **→** to begin

---
layout: terminal-split
env: python-dev
---

# Python 环境

在右侧终端中尝试以下命令：

```bash
python3 --version
python3 -c "print('Hello from TermiSlide!')"
```

<v-click>

### 练习

1. 创建一个变量 `x = 42`
2. 打印 `x * 2` 的结果

</v-click>

---
layout: terminal-split
env: node-dev
---

# Node.js 环境

右侧终端已切换到 Node.js 环境。

```bash
node --version
node -e "console.log(Array.from({length:5}, (_,i) => i*i))"
```

> 每张幻灯片可通过 `env` 字段指定不同的终端环境，  
> 后端会自动管理对应的 PTY 会话。

---
layout: terminal-split
---

# 默认环境

未指定 `env` 时，将使用 `"default"` 环境。

```yaml
# Frontmatter 配置
---
layout: terminal-split
env: my-custom-env    # 可选，默认 "default"
---
```

---

# 架构说明

```
┌─────────────┐  WebSocket   ┌──────────────────┐
│  Slidev     │◄────────────►│  Python Daemon    │
│  (xterm.js) │  JSON frames │  (Terminal Mgr)   │
└─────────────┘              └──────────────────┘
                                    │
                              ┌─────┴─────┐
                              │  PTY Pool  │
                              │ (per env)  │
                              └───────────┘
```

**控制帧协议**:
- `attach` — 绑定到指定环境的终端
- `input` — 发送用户键盘输入
- `resize` — 同步终端尺寸
- `output` — 接收终端输出（后端→前端）
