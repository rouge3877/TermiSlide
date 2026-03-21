#!/usr/bin/env bash
#
# TermiSlide 启动脚本
#
# 在两个终端中分别启动后端和前端：
#   终端1: ./start.sh daemon
#   终端2: ./start.sh frontend
#
# 或一键启动（后端在后台）：
#   ./start.sh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
DAEMON="$ROOT_DIR/packages/daemon/daemon.py"
VENV_DIR="$ROOT_DIR/packages/daemon/.venv"
CONFIG="${2:-$ROOT_DIR/demo/terminal/config.yaml}"
SLIDES_DIR="${3:-$ROOT_DIR/demo/terminal}"
PORT="${TERMISLIDE_PORT:-8765}"

# 确保 Python 虚拟环境和依赖就绪
setup_venv() {
    if [ ! -d "$VENV_DIR" ]; then
        echo "创建 Python 虚拟环境..."
        python3 -m venv "$VENV_DIR"
    fi
    # shellcheck source=/dev/null
    source "$VENV_DIR/bin/activate"
    if ! python3 -c "import websockets, ptyprocess, yaml" 2>/dev/null; then
        echo "安装 Python 依赖..."
        pip install -q -r "$ROOT_DIR/packages/daemon/requirements.txt"
    fi
}

start_daemon() {
    setup_venv
    echo "启动后端 daemon (ws://localhost:$PORT)..."
    python3 "$DAEMON" "$CONFIG"
}

start_frontend() {
    echo "启动前端 (http://localhost:3030)..."
    cd "$SLIDES_DIR"
    exec npx slidev slides.md --open
}

case "${1:-all}" in
    daemon|backend|d)
        start_daemon
        ;;
    frontend|front|f)
        start_frontend
        ;;
    all)
        setup_venv
        echo "启动后端 daemon (ws://localhost:$PORT)..."
        python3 "$DAEMON" "$CONFIG" &
        DAEMON_PID=$!
        trap 'kill $DAEMON_PID 2>/dev/null; wait $DAEMON_PID 2>/dev/null; echo "已退出"' INT TERM
        sleep 2

        if ! kill -0 "$DAEMON_PID" 2>/dev/null; then
            echo "后端启动失败，请检查端口 $PORT 是否被占用"
            exit 1
        fi

        echo "启动前端 (http://localhost:3030)..."
        cd "$SLIDES_DIR"
        npx slidev slides.md --open &

        echo ""
        echo "TermiSlide 已启动"
        echo "  前端: http://localhost:3030"
        echo "  后端: ws://localhost:$PORT"
        echo "  按 Ctrl+C 停止"
        echo ""
        wait "$DAEMON_PID" 2>/dev/null || true
        ;;
    -h|--help|help)
        echo "用法: ./start.sh [daemon|frontend|all]"
        echo ""
        echo "  daemon    仅启动后端 (前台运行，适合单独开一个终端)"
        echo "  frontend  仅启动前端 (前台运行，适合单独开一个终端)"
        echo "  all       一键启动后端+前端 (默认)"
        echo ""
        echo "推荐方式：开两个终端分别运行"
        echo "  终端1: ./start.sh daemon"
        echo "  终端2: ./start.sh frontend"
        echo ""
        echo "环境变量:"
        echo "  TERMISLIDE_PORT  后端端口 (默认 8765)"
        ;;
    *)
        echo "未知参数: $1"
        echo "用法: ./start.sh [daemon|frontend|all|--help]"
        exit 1
        ;;
esac
