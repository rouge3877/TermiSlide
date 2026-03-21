<!--
  WebTerminal - Interactive terminal component powered by xterm.js

  Connects to a Python Terminal Daemon via WebSocket for live shell access.
  Each slide can specify its own terminal environment via the `envName` prop.

  Usage in Slidev markdown (with terminal-split layout):

  ```md
  ---
  layout: terminal-split
  env: python-dev
  ---

  # My Terminal Slide

  Instructions go here on the left side.
  ```
-->

<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { Terminal } from 'xterm'
import { FitAddon } from 'xterm-addon-fit'
import 'xterm/css/xterm.css'

const props = withDefaults(defineProps<{
  envName?: string
  wsUrl?: string
}>(), {
  envName: 'default',
  wsUrl: 'ws://localhost:8765',
})

const terminalRef = ref<HTMLDivElement>()

let term: Terminal | null = null
let fitAddon: FitAddon | null = null
let ws: WebSocket | null = null
let resizeObserver: ResizeObserver | null = null
let reconnectTimer: ReturnType<typeof setTimeout> | null = null
let disposed = false

const RECONNECT_DELAY = 3000

function sendJSON(data: Record<string, unknown>) {
  if (ws?.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify(data))
  }
}

function attachEnv(envName: string) {
  if (!term)
    return
  term.clear()
  sendJSON({
    type: 'attach',
    env: envName,
    cols: term.cols,
    rows: term.rows,
  })
}

function connectWebSocket() {
  if (disposed)
    return

  ws = new WebSocket(props.wsUrl)

  ws.onopen = () => {
    attachEnv(props.envName)
  }

  ws.onmessage = (event) => {
    try {
      const msg = JSON.parse(event.data)
      if (msg.type === 'output' && msg.data) {
        term?.write(msg.data)
      }
    }
    catch {
      // Non-JSON message, write raw
      term?.write(event.data)
    }
  }

  ws.onclose = () => {
    if (!disposed) {
      reconnectTimer = setTimeout(connectWebSocket, RECONNECT_DELAY)
    }
  }

  ws.onerror = () => {
    ws?.close()
  }
}

function performFit() {
  if (!fitAddon || !term)
    return
  try {
    fitAddon.fit()
    sendJSON({
      type: 'resize',
      cols: term.cols,
      rows: term.rows,
    })
  }
  catch {
    // Container may not be visible yet
  }
}

onMounted(() => {
  if (!terminalRef.value)
    return

  term = new Terminal({
    cursorBlink: true,
    fontSize: 14,
    fontFamily: '\'Cascadia Code\', \'Fira Code\', Menlo, Monaco, \'Courier New\', monospace',
    theme: {
      background: '#1e1e2e',
      foreground: '#cdd6f4',
      cursor: '#f5e0dc',
      selectionBackground: '#585b7066',
      black: '#45475a',
      red: '#f38ba8',
      green: '#a6e3a1',
      yellow: '#f9e2af',
      blue: '#89b4fa',
      magenta: '#f5c2e7',
      cyan: '#94e2d5',
      white: '#bac2de',
      brightBlack: '#585b70',
      brightRed: '#f38ba8',
      brightGreen: '#a6e3a1',
      brightYellow: '#f9e2af',
      brightBlue: '#89b4fa',
      brightMagenta: '#f5c2e7',
      brightCyan: '#94e2d5',
      brightWhite: '#a6adc8',
    },
  })

  fitAddon = new FitAddon()
  term.loadAddon(fitAddon)
  term.open(terminalRef.value)

  // Initial fit after DOM is ready
  requestAnimationFrame(() => performFit())

  // Forward user input to backend
  term.onData((data) => {
    sendJSON({ type: 'input', data })
  })

  // Observe container resize
  resizeObserver = new ResizeObserver(() => {
    requestAnimationFrame(() => performFit())
  })
  resizeObserver.observe(terminalRef.value)

  connectWebSocket()
})

// Re-attach when envName changes (slide navigation)
watch(() => props.envName, (newEnv) => {
  attachEnv(newEnv)
})

onUnmounted(() => {
  disposed = true

  if (reconnectTimer) {
    clearTimeout(reconnectTimer)
    reconnectTimer = null
  }

  resizeObserver?.disconnect()
  resizeObserver = null

  if (ws) {
    ws.onclose = null // Prevent reconnect on intentional close
    ws.close()
    ws = null
  }

  term?.dispose()
  term = null
  fitAddon = null
})
</script>

<template>
  <div ref="terminalRef" class="web-terminal" />
</template>

<style scoped>
.web-terminal {
  width: 100%;
  height: 100%;
  overflow: hidden;
  border-radius: 6px;
  background: #1e1e2e;
}

.web-terminal :deep(.xterm) {
  height: 100%;
  padding: 8px;
}

.web-terminal :deep(.xterm-viewport) {
  border-radius: 6px;
}
</style>
