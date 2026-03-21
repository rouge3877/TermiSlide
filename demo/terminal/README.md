# TermiSlide Demo — 交互式终端教学

本示例演示如何使用 TermiSlide 创建带有实时终端的交互式教学幻灯片。

## 快速开始

需要同时启动**后端**（Terminal Daemon）和**前端**（Slidev）。

### 1. 启动后端

```bash
cd /path/to/TermiSlide-Backend

# 安装依赖（首次）
pip install -r requirements.txt

# 使用 demo 的 config 启动
python daemon.py /path/to/TermiSlide/demo/terminal/config.yaml
```

后端将在 `ws://localhost:8765` 监听 WebSocket 连接。

### 2. 启动前端

```bash
cd /path/to/TermiSlide

# 安装依赖（首次）
pnpm install

# 构建 CLI
pnpm run --filter @slidev/parser build
pnpm run --filter @slidev/types build
pnpm run --filter @slidev/cli build

# 启动 Slidev
cd demo/terminal
npx slidev slides.md --open
```

### 3. 使用

打开浏览器访问 `http://localhost:3030`，按 → 翻页：

| 幻灯片 | 环境 | 内容 |
|--------|------|------|
| 1 | — | 标题页 |
| 2 | `linux-basics` | 文件查看、grep、管道 |
| 3 | `linux-basics` | 文件操作（状态保持） |
| 4 | `git-practice` | Git 初始化与提交 |
| 5 | `linux-basics` | 回到 Lab 1（缓冲回放） |
| 6 | — | 架构总览 |

## 项目结构

```
demo/terminal/
├── slides.md          # Slidev 幻灯片 Markdown
├── config.yaml        # 后端环境配置
├── package.json       # 前端依赖
├── README.md          # 本文件
└── labs/
    ├── linux-basics/  # Lab 1 工作目录
    │   ├── .lab.env   # 环境初始化脚本
    │   └── sample.txt # 练习用文件
    └── git-practice/  # Lab 2 工作目录
        └── .lab.env   # 环境初始化脚本
```

## 自定义

### 添加新环境

1. 在 `labs/` 下创建目录，放入练习文件
2. （可选）添加 `.lab.env` 脚本，设置环境变量和提示符
3. 在 `config.yaml` 中注册：
   ```yaml
   environments:
     - name: "my-new-lab"
       path: "./labs/my-new-lab"
   ```
4. 在 `slides.md` 中使用：
   ```md
   ---
   layout: terminal-split
   env: my-new-lab
   ---
   ```

### 自定义 WebSocket 地址

如果后端不在默认端口，可在 frontmatter 中指定：

```md
---
layout: terminal-split
env: my-env
wsUrl: ws://192.168.1.100:9000
---
```
