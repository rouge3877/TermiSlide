# TermiSlide Demo — Shell Tutorial

本示例使用 TermiSlide 创建的 Shell 教学幻灯片。

## 快速开始

需要同时启动**后端**（Terminal Daemon）和**前端**（Slidev）。

### 1. 启动后端

```bash
cd packages/daemon

# 安装依赖（首次）
pip install -r requirements.txt

# 使用 demo 的 config 启动（从项目根目录运行）
cd ../../
python packages/daemon/daemon.py demo/terminal/config.yaml
```

后端将在 `ws://localhost:8765` 监听 WebSocket 连接。

### 2. 启动前端

```bash
# 启动 Slidev
cd demo/terminal
npx slidev slides.md --open
```

### 3. 使用

打开浏览器访问 `http://localhost:3030`，按 → 翻页。

> 详细的架构说明和开发文档见 [packages/daemon/README.md](../../packages/daemon/README.md)。
