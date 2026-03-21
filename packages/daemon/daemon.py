#!/usr/bin/env python3
"""
TermiSlide Terminal Daemon
==========================
基于 asyncio 的多路复用伪终端（PTY）WebSocket 服务。

架构概览
--------
                         ┌─────────────────────────────┐
                         │        config.yaml           │
                         │  (环境名 → 工作目录映射)       │
                         └──────────┬──────────────────┘
                                    │ 启动时解析
                         ┌──────────▼──────────────────┐
                         │     Terminal Daemon          │
                         │  (asyncio event loop)        │
                         │                              │
  WebSocket 客户端 ◄────►│  ws_handler() 路由分发        │
                         │    ├─ attach  → 绑定/创建 PTY │
                         │    ├─ input   → 写入 PTY      │
                         │    └─ resize  → 调整窗口       │
                         │                              │
                         │  _pty_read_loop() 异步读取    │
                         │    └─ fd readable → 广播输出   │
                         └──────────────────────────────┘

PTY 异步读取机制
----------------
ptyprocess 底层通过 os.openpty() 获得文件描述符(fd)。该 fd 是一个
标准的 UNIX 文件描述符，可以被 epoll/kqueue 监视。

本实现使用 asyncio 事件循环的 add_reader(fd, callback) 将 PTY 的
master fd 注册到 I/O 多路复用器。当子进程产生输出时，内核将该 fd
标记为可读，事件循环触发回调，回调内通过 os.read() 非阻塞地读取
数据，随后：
  1. 写入该 PTY 的环形缓冲区 (用于后续客户端 attach 时回放)
  2. 广播给所有已绑定该环境的 WebSocket 客户端

缓冲回放逻辑
--------------
每个 PTYSession 持有一个 collections.deque(maxlen=OUTPUT_BUFFER_SIZE)
作为字节级环形缓冲区。新客户端 attach 到已有 PTY 时，daemon 将缓冲
区中的全部内容拼接后一次性发送，使前端能立即恢复终端画面，避免黑屏。
"""

from __future__ import annotations

import asyncio
import collections
import json
import logging
import os
import signal
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import websockets
import yaml
from ptyprocess import PtyProcessUnicode

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

DEFAULT_CONFIG_PATH = "config.yaml"
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8765

# 环形输出缓冲区保留的最大字节数。
# 约 200 KB，足够缓存一个全屏终端(200×50)的几十屏滚动历史。
OUTPUT_BUFFER_MAX_BYTES = 200 * 1024

# PTY 单次 os.read() 的最大读取字节数
PTY_READ_CHUNK = 4096

# 默认终端尺寸
DEFAULT_COLS = 80
DEFAULT_ROWS = 24

# ---------------------------------------------------------------------------
# 日志
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("termislide")

# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------


@dataclass
class EnvConfig:
    """从 config.yaml 解析出的单个环境配置。"""
    name: str
    path: str


@dataclass
class PTYSession:
    """
    封装一个 PTY 进程及其关联状态。

    Attributes
    ----------
    env_name : str
        环境名称，与 config.yaml 中的 name 对应。
    process : PtyProcessUnicode
        底层 ptyprocess 实例。
    output_buffer : collections.deque
        环形输出缓冲区，存储 bytes 分片。通过 maxlen 限制总条目数，
        同时用 buffer_bytes 跟踪实际字节量以便在超限时主动裁剪。
    buffer_bytes : int
        缓冲区当前总字节数。
    clients : set
        当前绑定到此 PTY 的所有 WebSocket 连接。
    read_task : asyncio.Task | None
        异步读取循环的 Task 句柄。
    """
    env_name: str
    process: PtyProcessUnicode
    output_buffer: list = field(default_factory=list)
    buffer_bytes: int = 0
    clients: set = field(default_factory=set)
    read_task: asyncio.Task | None = None

    def append_output(self, data: str) -> None:
        """
        将一段输出追加到环形缓冲区。

        当累计字节数超过 OUTPUT_BUFFER_MAX_BYTES 时，从头部丢弃旧数据
        直到总量回到阈值以下。这保证了内存占用可控，同时尽可能多地保留
        最近的终端输出用于回放。
        """
        encoded = data.encode("utf-8", errors="replace")
        self.output_buffer.append(encoded)
        self.buffer_bytes += len(encoded)

        # 裁剪：从头部弹出旧数据直到低于上限
        while self.buffer_bytes > OUTPUT_BUFFER_MAX_BYTES and self.output_buffer:
            removed = self.output_buffer.pop(0)
            self.buffer_bytes -= len(removed)

    def get_buffered_output(self) -> str:
        """拼接缓冲区并返回完整的字符串，用于回放。"""
        return b"".join(self.output_buffer).decode("utf-8", errors="replace")


# ---------------------------------------------------------------------------
# 全局状态
# ---------------------------------------------------------------------------

# 环境名 → PTYSession
pty_sessions: dict[str, PTYSession] = {}

# WebSocket → 当前绑定的环境名（每个 ws 同一时刻只绑定一个 PTY）
ws_env_map: dict[Any, str] = {}

# 环境名 → EnvConfig（启动时从 config.yaml 加载）
env_configs: dict[str, EnvConfig] = {}

# shutdown() 用于通知 main() 退出的 Future
_shutdown_event: asyncio.Future | None = None

# ---------------------------------------------------------------------------
# 配置加载
# ---------------------------------------------------------------------------


def load_config(path: str = DEFAULT_CONFIG_PATH) -> dict[str, EnvConfig]:
    """
    解析 config.yaml，返回 {env_name: EnvConfig} 字典。

    环境的 path 字段支持相对路径，解析时相对于配置文件所在目录。
    例如 config 在 demo/terminal/config.yaml，path 为 "labs/foo"，
    则实际路径为 demo/terminal/labs/foo。

    配置文件格式示例：
        environments:
          - name: "env_a"
            path: "/path/to/dir_a"
    """
    config_path = Path(path)
    if not config_path.exists():
        log.error("配置文件不存在: %s", config_path.resolve())
        sys.exit(1)

    config_dir = config_path.resolve().parent

    with open(config_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    if not raw or "environments" not in raw:
        log.error("配置文件格式错误: 缺少 'environments' 键")
        sys.exit(1)

    configs: dict[str, EnvConfig] = {}
    for entry in raw["environments"]:
        name = entry.get("name")
        env_path = entry.get("path")
        if not name or not env_path:
            log.warning("跳过无效环境配置: %s", entry)
            continue
        # 将相对路径解析为相对于配置文件所在目录的绝对路径
        resolved = str((config_dir / env_path).resolve())
        configs[name] = EnvConfig(name=name, path=resolved)
        log.info("已加载环境: %s → %s", name, resolved)

    if not configs:
        log.error("未找到任何有效的环境配置")
        sys.exit(1)

    return configs


# ---------------------------------------------------------------------------
# PTY 生命周期
# ---------------------------------------------------------------------------


async def spawn_pty(env: EnvConfig, cols: int = DEFAULT_COLS, rows: int = DEFAULT_ROWS) -> PTYSession:
    """
    为指定环境衍生一个新的 PTY 进程。

    流程：
    1. 使用 ptyprocess 启动 /bin/bash
    2. 设置初始终端尺寸
    3. 向 bash 写入初始化指令（cd + source .lab.env + clear）
    4. 启动异步读取循环任务
    5. 注册到全局 pty_sessions

    Parameters
    ----------
    env : EnvConfig
        目标环境配置。
    cols, rows : int
        初始终端尺寸。

    Returns
    -------
    PTYSession
        创建好的会话对象。
    """
    log.info("正在为环境 '%s' 衍生 PTY (cwd=%s, size=%dx%d)", env.name, env.path, cols, rows)

    # 衍生 bash 进程，dimensions=(rows, cols)
    process = PtyProcessUnicode.spawn(
        ["/bin/bash"],
        dimensions=(rows, cols),
    )

    session = PTYSession(env_name=env.name, process=process)
    pty_sessions[env.name] = session

    # 向 bash 发送初始化指令：
    #   - cd 到环境目录
    #   - source .lab.env（如果存在）加载环境变量
    #   - clear 清屏，给前端一个干净的起点
    init_cmd = f"cd {env.path} && [ -f .lab.env ] && source .lab.env; clear\n"
    process.write(init_cmd)

    # 启动异步读取循环
    session.read_task = asyncio.create_task(
        _pty_read_loop(session),
        name=f"pty-reader-{env.name}",
    )

    log.info("环境 '%s' PTY 已就绪 (PID=%d)", env.name, process.pid)
    return session


async def _pty_read_loop(session: PTYSession) -> None:
    """
    PTY 异步读取循环（核心 I/O 引擎）。

    设计说明
    --------
    ptyprocess 的 read() 方法是阻塞的，不能直接在 asyncio 协程中调用。
    本实现采用 loop.add_reader() 将 PTY 的 master 文件描述符注册到事件
    循环的 I/O 多路复用器（Linux 上为 epoll）。

    工作流：
    1. 获取 PTY 的 master fd
    2. 创建一个 asyncio.Event 作为"可读"信号
    3. 用 add_reader(fd, event.set) 注册回调
    4. 主循环中 await event.wait() —— 零 CPU 开销等待
    5. 事件触发时，用 os.read(fd, CHUNK) 非阻塞读取
    6. 将数据存入缓冲区 + 广播给所有客户端
    7. 重置 event，继续等待

    这种方式比 run_in_executor(blocking_read) 更高效，因为：
    - 无需线程池，减少上下文切换开销
    - 直接利用内核的 I/O 通知机制
    - 与 asyncio 事件循环完美集成
    """
    loop = asyncio.get_running_loop()
    fd = session.process.fd
    readable_event = asyncio.Event()

    def _on_readable():
        """当 PTY fd 可读时，由事件循环调用，设置 asyncio.Event 信号。"""
        readable_event.set()

    loop.add_reader(fd, _on_readable)

    try:
        while True:
            # 等待 PTY 产生输出（epoll 级别的等待，零 CPU）
            readable_event.clear()
            await readable_event.wait()

            try:
                # 非阻塞读取：此时 fd 已确认可读，os.read 不会阻塞
                raw = os.read(fd, PTY_READ_CHUNK)
            except OSError:
                # fd 关闭或进程退出
                log.info("环境 '%s' PTY 读取结束 (fd 关闭)", session.env_name)
                break

            if not raw:
                # EOF — 子进程已退出
                log.info("环境 '%s' PTY EOF", session.env_name)
                break

            data = raw.decode("utf-8", errors="replace")

            # 1) 存入环形缓冲区，供后续 attach 回放
            session.append_output(data)

            # 2) 构造输出帧并广播给所有已绑定的 WebSocket 客户端
            output_frame = json.dumps({"type": "output", "data": data})
            if session.clients:
                # 使用 asyncio.gather 并发发送，任一失败不影响其他客户端
                await asyncio.gather(
                    *(
                        _safe_send(ws, output_frame)
                        for ws in set(session.clients)  # 复制 set 防止迭代中修改
                    ),
                    return_exceptions=True,
                )
    except asyncio.CancelledError:
        log.info("环境 '%s' 读取循环被取消", session.env_name)
    finally:
        loop.remove_reader(fd)
        log.info("环境 '%s' 读取循环已退出", session.env_name)


async def _safe_send(ws: Any, data: str) -> None:
    """安全发送：捕获连接关闭异常，避免影响其他客户端的广播。"""
    try:
        await ws.send(data)
    except websockets.exceptions.ConnectionClosed:
        pass
    except Exception as e:
        log.warning("向客户端发送数据失败: %s", e)


# ---------------------------------------------------------------------------
# WebSocket 处理
# ---------------------------------------------------------------------------


async def ws_handler(websocket: Any) -> None:
    """
    WebSocket 连接主处理函数。

    每个 WebSocket 连接视为一个独立会话。通过 JSON 帧进行通信：

    客户端 → 服务端：
      {"type": "attach", "env": "<envName>", "cols": 80, "rows": 24}
      {"type": "input", "data": "<键盘输入>"}
      {"type": "resize", "cols": 120, "rows": 40}

    服务端 → 客户端：
      {"type": "output", "data": "<终端输出>"}
      {"type": "error", "message": "<错误信息>"}
      {"type": "attached", "env": "<envName>"}
    """
    remote = websocket.remote_address
    log.info("新 WebSocket 连接: %s", remote)

    try:
        async for raw_message in websocket:
            try:
                msg = json.loads(raw_message)
            except json.JSONDecodeError:
                await _send_error(websocket, "无效的 JSON 格式")
                continue

            msg_type = msg.get("type")

            if msg_type == "attach":
                await _handle_attach(websocket, msg)
            elif msg_type == "input":
                await _handle_input(websocket, msg)
            elif msg_type == "resize":
                await _handle_resize(websocket, msg)
            else:
                await _send_error(websocket, f"未知的消息类型: {msg_type}")

    except websockets.exceptions.ConnectionClosed:
        log.info("WebSocket 连接关闭: %s", remote)
    except Exception as e:
        log.exception("WebSocket 处理异常: %s", e)
    finally:
        # 清理：将此 ws 从所绑定的 PTY 客户端列表中移除
        _detach_ws(websocket)
        log.info("WebSocket 会话结束: %s", remote)


async def _handle_attach(ws: Any, msg: dict) -> None:
    """
    处理 attach 请求。

    逻辑流程：
    1. 验证环境名是否在配置中存在
    2. 如果客户端之前绑定了其他环境，先解绑
    3. 如果该环境尚无 PTY，创建一个
    4. 将客户端绑定到目标 PTY
    5. 如果 PTY 已有缓冲输出，回放给客户端（恢复画面）
    6. 如果请求中包含 cols/rows，调整 PTY 窗口大小
    """
    env_name = msg.get("env")
    if not env_name:
        await _send_error(ws, "attach 请求缺少 'env' 字段")
        return

    # 1) 检查环境是否存在
    if env_name not in env_configs:
        await _send_error(ws, f"未知的环境: '{env_name}'（不在 config.yaml 中）")
        return

    # 2) 如果此 ws 之前绑定了其他环境，先解绑
    _detach_ws(ws)

    # 3) 获取或创建 PTY 会话
    cols = msg.get("cols", DEFAULT_COLS)
    rows = msg.get("rows", DEFAULT_ROWS)

    session = pty_sessions.get(env_name)
    if session is None:
        # 首次 attach 该环境：衍生新 PTY
        env_cfg = env_configs[env_name]
        session = await spawn_pty(env_cfg, cols=cols, rows=rows)
    else:
        log.info("环境 '%s' PTY 已存在，复用", env_name)

    # 4) 绑定客户端到此 PTY
    session.clients.add(ws)
    ws_env_map[ws] = env_name

    # 5) 回放缓冲区输出（核心：防止前端黑屏）
    buffered = session.get_buffered_output()
    if buffered:
        replay_frame = json.dumps({"type": "output", "data": buffered})
        await _safe_send(ws, replay_frame)
        log.info(
            "已向客户端回放 %d 字节缓冲输出 (env=%s)",
            len(buffered.encode("utf-8", errors="replace")),
            env_name,
        )

    # 6) 调整终端尺寸（如果请求中提供了 cols/rows）
    if "cols" in msg and "rows" in msg:
        try:
            session.process.setwinsize(rows, cols)
        except Exception as e:
            log.warning("设置终端尺寸失败: %s", e)

    # 确认 attach 成功
    await _safe_send(ws, json.dumps({"type": "attached", "env": env_name}))
    log.info("客户端已 attach 到环境 '%s'", env_name)


async def _handle_input(ws: Any, msg: dict) -> None:
    """
    处理 input 请求：将用户键盘输入转发到绑定的 PTY stdin。
    """
    data = msg.get("data")
    if data is None:
        await _send_error(ws, "input 请求缺少 'data' 字段")
        return

    env_name = ws_env_map.get(ws)
    if not env_name:
        await _send_error(ws, "尚未 attach 到任何环境，请先发送 attach 请求")
        return

    session = pty_sessions.get(env_name)
    if not session:
        await _send_error(ws, f"环境 '{env_name}' 的 PTY 已不存在")
        return

    try:
        session.process.write(data)
    except Exception as e:
        log.error("写入 PTY 失败 (env=%s): %s", env_name, e)
        await _send_error(ws, f"写入 PTY 失败: {e}")


async def _handle_resize(ws: Any, msg: dict) -> None:
    """
    处理 resize 请求：调整绑定 PTY 的终端行列数。

    底层通过 ioctl(fd, TIOCSWINSZ, ...) 实现，ptyprocess 已封装为
    setwinsize(rows, cols) 方法。
    """
    cols = msg.get("cols")
    rows = msg.get("rows")
    if cols is None or rows is None:
        await _send_error(ws, "resize 请求缺少 'cols' 或 'rows' 字段")
        return

    env_name = ws_env_map.get(ws)
    if not env_name:
        await _send_error(ws, "尚未 attach 到任何环境")
        return

    session = pty_sessions.get(env_name)
    if not session:
        await _send_error(ws, f"环境 '{env_name}' 的 PTY 已不存在")
        return

    try:
        session.process.setwinsize(int(rows), int(cols))
        log.info("已调整终端尺寸: env=%s, %dx%d", env_name, cols, rows)
    except Exception as e:
        log.error("调整终端尺寸失败 (env=%s): %s", env_name, e)
        await _send_error(ws, f"调整终端尺寸失败: {e}")


def _detach_ws(ws: Any) -> None:
    """
    将 WebSocket 从其绑定的 PTY 会话中解绑。

    注意：PTY 进程本身不会因客户端断开而终止——这是"常驻"语义的核心。
    即使所有客户端都断开，PTY 仍然运行，缓冲区继续积累输出，下次
    attach 时可以回放。
    """
    env_name = ws_env_map.pop(ws, None)
    if env_name:
        session = pty_sessions.get(env_name)
        if session:
            session.clients.discard(ws)
            log.info(
                "客户端已从环境 '%s' 解绑 (剩余客户端: %d)",
                env_name,
                len(session.clients),
            )


async def _send_error(ws: Any, message: str) -> None:
    """发送错误帧给客户端。"""
    frame = json.dumps({"type": "error", "message": message})
    await _safe_send(ws, frame)


# ---------------------------------------------------------------------------
# 服务启动与优雅关闭
# ---------------------------------------------------------------------------


async def shutdown(sig: signal.Signals) -> None:
    """
    优雅关闭流程：
    1. 取消所有 PTY 读取循环任务
    2. 终止所有 PTY 子进程
    3. 取消 main() 中的等待 Future，使事件循环退出
    """
    log.info("收到信号 %s，正在关闭...", sig.name)

    for env_name, session in pty_sessions.items():
        # 取消读取循环
        if session.read_task and not session.read_task.done():
            session.read_task.cancel()

        # 终止 PTY 进程
        if session.process.isalive():
            log.info("终止 PTY: env=%s, PID=%d", env_name, session.process.pid)
            session.process.terminate(force=True)

    # 等待所有读取任务完成
    tasks = [s.read_task for s in pty_sessions.values() if s.read_task]
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)

    pty_sessions.clear()
    log.info("所有 PTY 已清理，daemon 退出")

    # 通知 main() 退出：取消 _shutdown_event Future
    if _shutdown_event and not _shutdown_event.done():
        _shutdown_event.set_result(True)


async def main() -> None:
    """
    Daemon 入口点。

    1. 加载配置
    2. 注册信号处理器
    3. 启动 WebSocket 服务器
    4. 永久运行直到收到终止信号
    """
    global env_configs

    # 支持通过命令行参数指定配置文件路径
    config_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CONFIG_PATH
    env_configs = load_config(config_path)

    log.info(
        "已加载 %d 个环境配置: %s",
        len(env_configs),
        ", ".join(env_configs.keys()),
    )

    # 用于 shutdown() 通知 main() 退出的 Future
    global _shutdown_event
    _shutdown_event = asyncio.get_running_loop().create_future()

    # 注册优雅关闭信号
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(
            sig,
            lambda s=sig: asyncio.create_task(shutdown(s)),
        )

    # 启动 WebSocket 服务器
    host = os.environ.get("TERMISLIDE_HOST", DEFAULT_HOST)
    port = int(os.environ.get("TERMISLIDE_PORT", str(DEFAULT_PORT)))

    async with websockets.serve(ws_handler, host, port):
        log.info("TermiSlide Daemon 已启动: ws://%s:%d", host, port)
        log.info("等待 WebSocket 客户端连接...")

        # 等待关闭信号
        await _shutdown_event


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Daemon 被 Ctrl+C 中断")
