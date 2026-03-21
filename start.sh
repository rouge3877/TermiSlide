#!/usr/bin/env bash
#
# TermiSlide — 统一启动脚本
#
# 用法:
#   ./start.sh                    启动后端 + 前端 (默认 demo/terminal)
#   ./start.sh <config> <slides>  指定 config.yaml 和 slides 目录
#   ./start.sh --daemon-only      仅启动后端
#   ./start.sh --help             帮助信息
#
# 停止: Ctrl+C (脚本会同时终止后端和前端)

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
DAEMON="$ROOT_DIR/packages/daemon/daemon.py"
VENV_DIR="$ROOT_DIR/packages/daemon/.venv"
DEFAULT_CONFIG="$ROOT_DIR/demo/terminal/config.yaml"
DEFAULT_SLIDES_DIR="$ROOT_DIR/demo/terminal"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

DAEMON_PID=""
FRONTEND_PID=""

usage() {
    echo -e "${BOLD}TermiSlide${NC} — 交互式终端教学平台"
    echo ""
    echo -e "用法: ${CYAN}./start.sh${NC} [选项] [config.yaml] [slides目录]"
    echo ""
    echo "选项:"
    echo "  --daemon-only    仅启动后端 daemon"
    echo "  --help, -h       显示帮助"
    echo ""
    echo "示例:"
    echo "  ./start.sh                                   # 默认: demo/terminal"
    echo "  ./start.sh demo/terminal/config.yaml demo/terminal"
    echo "  ./start.sh --daemon-only"
    echo ""
    echo "环境变量:"
    echo "  TERMISLIDE_HOST   后端监听地址 (默认 0.0.0.0)"
    echo "  TERMISLIDE_PORT   后端监听端口 (默认 8765)"
}

cleanup() {
    echo ""
    echo -e "${YELLOW}正在关闭...${NC}"
    # 移除 trap 避免重复触发
    trap - EXIT INT TERM
    if [ -n "$FRONTEND_PID" ] && kill -0 "$FRONTEND_PID" 2>/dev/null; then
        kill "$FRONTEND_PID" 2>/dev/null
        wait "$FRONTEND_PID" 2>/dev/null || true
        echo -e "  ${GREEN}✔${NC} 前端已停止"
    fi
    if [ -n "$DAEMON_PID" ] && kill -0 "$DAEMON_PID" 2>/dev/null; then
        kill "$DAEMON_PID" 2>/dev/null
        wait "$DAEMON_PID" 2>/dev/null || true
        echo -e "  ${GREEN}✔${NC} 后端已停止"
    fi
    echo -e "${GREEN}已退出${NC}"
    exit 0
}

trap cleanup INT TERM

# --------------------------------------------------------------------------
# 解析参数
# --------------------------------------------------------------------------
DAEMON_ONLY=false
CONFIG="$DEFAULT_CONFIG"
SLIDES_DIR="$DEFAULT_SLIDES_DIR"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --daemon-only)
            DAEMON_ONLY=true
            shift
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        *)
            if [ -z "${ARG1:-}" ]; then
                ARG1="$1"
            else
                ARG2="$1"
            fi
            shift
            ;;
    esac
done

if [ -n "${ARG1:-}" ]; then CONFIG="$ARG1"; fi
if [ -n "${ARG2:-}" ]; then SLIDES_DIR="$ARG2"; fi

# --------------------------------------------------------------------------
# 检查依赖
# --------------------------------------------------------------------------
echo -e "${BOLD}TermiSlide${NC}"
echo ""

# Python
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}✗ python3 未找到${NC}"
    exit 1
fi

# Python venv + 依赖
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${CYAN}→${NC} 创建 Python 虚拟环境..."
    python3 -m venv "$VENV_DIR"
fi

# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

if ! python3 -c "import websockets, ptyprocess, yaml" 2>/dev/null; then
    echo -e "${CYAN}→${NC} 安装 Python 依赖..."
    pip install -q -r "$ROOT_DIR/packages/daemon/requirements.txt"
fi

# 验证文件存在
if [ ! -f "$CONFIG" ]; then
    echo -e "${RED}✗ 配置文件不存在: $CONFIG${NC}"
    exit 1
fi

if [ ! -f "$DAEMON" ]; then
    echo -e "${RED}✗ daemon.py 不存在: $DAEMON${NC}"
    exit 1
fi

# --------------------------------------------------------------------------
# 启动后端
# --------------------------------------------------------------------------
PORT="${TERMISLIDE_PORT:-8765}"

echo -e "${CYAN}→${NC} 启动后端 daemon (port $PORT)..."
python3 "$DAEMON" "$CONFIG" &
DAEMON_PID=$!
sleep 2

if ! kill -0 "$DAEMON_PID" 2>/dev/null; then
    echo -e "${RED}✗ 后端启动失败${NC}"
    exit 1
fi
echo -e "  ${GREEN}✔${NC} 后端已启动 (PID $DAEMON_PID, ws://localhost:$PORT)"

# --------------------------------------------------------------------------
# 启动前端
# --------------------------------------------------------------------------
if [ "$DAEMON_ONLY" = true ]; then
    echo ""
    echo -e "${GREEN}后端运行中，按 Ctrl+C 停止${NC}"
    wait "$DAEMON_PID"
    exit 0
fi

if [ ! -f "$SLIDES_DIR/slides.md" ]; then
    echo -e "${RED}✗ slides.md 不存在: $SLIDES_DIR/slides.md${NC}"
    exit 1
fi

echo -e "${CYAN}→${NC} 启动前端 (slidev)..."
cd "$SLIDES_DIR"
npx slidev slides.md --open --log=info &
FRONTEND_PID=$!
cd "$ROOT_DIR"

sleep 3
if ! kill -0 "$FRONTEND_PID" 2>/dev/null; then
    echo -e "${RED}✗ 前端启动失败${NC}"
    exit 1
fi
echo -e "  ${GREEN}✔${NC} 前端已启动 (PID $FRONTEND_PID)"

echo ""
echo -e "${BOLD}${GREEN}TermiSlide 已就绪${NC}"
echo -e "  前端: ${CYAN}http://localhost:3030${NC}"
echo -e "  后端: ${CYAN}ws://localhost:$PORT${NC}"
echo -e "  按 ${YELLOW}Ctrl+C${NC} 停止"
echo ""

# 等待任一进程退出
wait -n "$DAEMON_PID" "$FRONTEND_PID" 2>/dev/null || true
