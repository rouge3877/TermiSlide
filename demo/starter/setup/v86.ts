import { shallowRef } from 'vue'
import { Terminal } from '@xterm/xterm'
import { FitAddon } from '@xterm/addon-fit'
import '@xterm/xterm/css/xterm.css'

declare global {
  interface Window {
    V86: any
  }
}

export interface V86Instance {
  serial0_send(data: string): void
  add_listener(event: string, callback: (...args: any[]) => void): void
  remove_listener(event: string, callback: (...args: any[]) => void): void
  destroy(): void
}

export interface LabEnvConfig {
  init?: string[]
  description?: string
  hostname?: string
}

// ─── Emulator singleton ──────────────────────────────────────────────────────
const v86Instance = shallowRef<V86Instance | null>(null)
const v86Booted = shallowRef(false)
let initPromise: Promise<V86Instance> | null = null
let bootPromise: Promise<void> | null = null
let bootResolve: (() => void) | null = null

// ─── Terminal singleton ──────────────────────────────────────────────────────
let globalTerm: Terminal | null = null
let globalFitAddon: FitAddon | null = null
let globalContainer: HTMLDivElement | null = null
let serialBridgeAttached = false
let writeBuf = ''
let writeTimer: ReturnType<typeof setTimeout> | null = null

// ─── Environment state ──────────────────────────────────────────────────────
let currentEnvName: string | null = null
const initializedEnvs = new Set<string>()
let serialMuted = false
const readyRef = shallowRef(false)
let setupPromise: Promise<void> | null = null
const switchingRef = shallowRef(false)

// Switch scheduling: only one doSwitch runs at a time.
let switchRunning = false
let nextEnvToSwitch: string | null = null
let switchResolvers: Array<() => void> = []

// Safety watchdog: if serialMuted is stuck for >3s, force-unmute
let muteWatchdog: ReturnType<typeof setTimeout> | null = null
function startMuteWatchdog() {
  clearMuteWatchdog()
  muteWatchdog = setTimeout(() => {
    if (serialMuted) {
      console.warn('[v86] Mute watchdog: force-unmuting serial output')
      serialMuted = false
    }
    muteWatchdog = null
  }, 3000)
}
function clearMuteWatchdog() {
  if (muteWatchdog) { clearTimeout(muteWatchdog); muteWatchdog = null }
}

// ─── Environment registry ────────────────────────────────────────────────────
const envRegistry = new Map<string, LabEnvConfig>()
export function registerEnv(name: string, config: LabEnvConfig) { envRegistry.set(name, config) }

// ─── Helpers ─────────────────────────────────────────────────────────────────

function delay(ms: number): Promise<void> {
  return new Promise(r => setTimeout(r, ms))
}

/** Send a command via serial and wait a fixed time for it to execute */
async function sendCmd(emulator: V86Instance, cmd: string, waitMs = 50) {
  emulator.serial0_send(`${cmd}\r`)
  if (waitMs > 0) await delay(waitMs)
}

/** Buffered serial→xterm write (batches with setTimeout, works even when tab hidden) */
function flushWriteBuffer() {
  if (globalTerm && writeBuf) {
    globalTerm.write(writeBuf)
    writeBuf = ''
  }
  writeTimer = null
}

function bufferedTermWrite(byte: number) {
  writeBuf += String.fromCharCode(byte)
  if (!writeTimer) writeTimer = setTimeout(flushWriteBuffer, 8)
}

/** Wait for a marker string to appear in serial output */
function waitForMarker(emulator: V86Instance, marker: string, timeoutMs = 5000): Promise<void> {
  return new Promise((resolve) => {
    let buf = ''
    const timer = setTimeout(() => {
      emulator.remove_listener('serial0-output-byte', listener)
      resolve() // always resolve — never block forever
    }, timeoutMs)
    const listener = (byte: number) => {
      buf += String.fromCharCode(byte)
      if (buf.length > 500) buf = buf.slice(-300)
      if (buf.includes(marker)) {
        clearTimeout(timer)
        emulator.remove_listener('serial0-output-byte', listener)
        resolve()
      }
    }
    emulator.add_listener('serial0-output-byte', listener)
  })
}

// ─── Asset preloading ────────────────────────────────────────────────────────

export function preloadAssets() {
  for (const url of ['/v86.wasm', '/buildroot-bzimage68.bin', '/seabios.bin', '/vgabios.bin', '/libv86.js']) {
    const link = document.createElement('link')
    link.rel = 'preload'
    link.href = url
    link.as = url.endsWith('.js') ? 'script' : 'fetch'
    if (!url.endsWith('.js')) link.crossOrigin = 'anonymous'
    document.head.appendChild(link)
  }
}

// ─── VM init ─────────────────────────────────────────────────────────────────

export function initV86(): Promise<V86Instance> {
  if (initPromise) return initPromise
  bootPromise = new Promise<void>(r => { bootResolve = r })

  initPromise = (async () => {
    // Load script
    await new Promise<void>((resolve, reject) => {
      if (window.V86) { resolve(); return }
      const s = document.createElement('script')
      s.src = '/libv86.js'
      s.onload = () => resolve()
      s.onerror = () => reject(new Error('Failed to load libv86.js'))
      document.head.appendChild(s)
    })

    const sc = document.createElement('div')
    sc.style.display = 'none'
    sc.appendChild(document.createElement('div'))
    sc.appendChild(document.createElement('canvas'))
    document.body.appendChild(sc)

    const emulator: V86Instance = new window.V86({
      wasm_path: '/v86.wasm',
      memory_size: 128 * 1024 * 1024,
      vga_memory_size: 2 * 1024 * 1024,
      screen_container: sc,
      bios: { url: '/seabios.bin' },
      vga_bios: { url: '/vgabios.bin' },
      bzimage: { url: '/buildroot-bzimage68.bin' },
      autostart: true,
      disable_keyboard: true,
      disable_mouse: true,
      disable_speaker: true,
    })
    v86Instance.value = emulator

    // Boot detection
    let buf = ''
    const onBoot = () => {
      if (v86Booted.value) return
      v86Booted.value = true
      if (bootResolve) { bootResolve(); bootResolve = null }
      emulator.remove_listener('serial0-output-byte', bl)
      postBootSetup(emulator)
    }
    const bl = (byte: number) => {
      buf += String.fromCharCode(byte)
      if (buf.length > 200) buf = buf.slice(-100)
      if (buf.match(/[#$]\s$/) || buf.includes('login:')) onBoot()
    }
    emulator.add_listener('serial0-output-byte', bl)
    setTimeout(() => { if (!v86Booted.value) onBoot() }, 15000)

    return emulator
  })()
  return initPromise
}

export function waitForBoot(): Promise<void> {
  if (v86Booted.value) return Promise.resolve()
  if (bootPromise) return bootPromise
  return Promise.resolve()
}

// ─── Post-boot setup (runs once, as root) ────────────────────────────────────

function postBootSetup(emulator: V86Instance): Promise<void> {
  if (setupPromise) return setupPromise
  setupPromise = (async () => {
    // Create isolated directories for each environment under /env/
    await sendCmd(emulator, 'mkdir -p /env', 50)

    for (const [name, config] of envRegistry.entries()) {
      const dir = `/env/${name}`
      await sendCmd(emulator, `mkdir -p ${dir}`, 50)

      if (config.init && config.init.length > 0) {
        await sendCmd(emulator, `cd ${dir}`, 30)
        for (const cmd of config.init) {
          if (cmd.trim()) await sendCmd(emulator, cmd, 80)
        }
      }
      initializedEnvs.add(name)
    }

    await sendCmd(emulator, 'cd /', 30)
    const marker = `__ready_${Date.now()}__`
    await sendCmd(emulator, `echo ${marker}`, 0)
    await waitForMarker(emulator, marker, 8000)

    readyRef.value = true
  })()
  return setupPromise
}

function waitForReady(): Promise<void> {
  if (readyRef.value) return Promise.resolve()
  if (setupPromise) return setupPromise
  return Promise.resolve()
}

// ─── Terminal ────────────────────────────────────────────────────────────────

export function getOrCreateTerminal() {
  if (!globalTerm) {
    globalContainer = document.createElement('div')
    globalContainer.style.width = '100%'
    globalContainer.style.height = '100%'

    globalTerm = new Terminal({
      cursorBlink: true,
      fontSize: 14,
      fontFamily: 'Menlo, Monaco, Consolas, "Liberation Mono", monospace',
      theme: { background: '#1e1e2e', foreground: '#cdd6f4', cursor: '#f5e0dc' },
    })
    globalFitAddon = new FitAddon()
    globalTerm.loadAddon(globalFitAddon)
    globalTerm.open(globalContainer)
  }
  return { term: globalTerm, container: globalContainer!, fitAddon: globalFitAddon! }
}

export function attachSerialBridge(emulator: V86Instance) {
  if (serialBridgeAttached) return
  serialBridgeAttached = true
  const { term } = getOrCreateTerminal()

  emulator.add_listener('serial0-output-byte', (byte: number) => {
    if (v86Booted.value && readyRef.value && !serialMuted) {
      bufferedTermWrite(byte)
    }
  })

  term.onData((data: string) => {
    emulator.serial0_send(data)
  })
}

export function mountTerminalTo(parent: HTMLElement) {
  const { container, fitAddon } = getOrCreateTerminal()
  parent.appendChild(container)
  requestAnimationFrame(() => fitAddon.fit())
}

// ─── Environment switching (serialized, never concurrent) ────────────────────

/**
 * Request a switch to a named environment.
 * - If a switch is already running, this queues the request (only keeps the latest).
 * - If multiple calls happen while a switch runs, only the last-requested env executes.
 * - Returns a promise that resolves when this env is active (or superseded).
 */
export function switchEnv(envName: string): Promise<void> {
  if (currentEnvName === envName && !switchRunning) return Promise.resolve()

  return new Promise<void>((resolve) => {
    switchResolvers.push(resolve)
    nextEnvToSwitch = envName
    switchingRef.value = true
    scheduleSwitchLoop()
  })
}

let switchLoopScheduled = false
function scheduleSwitchLoop() {
  if (switchLoopScheduled) return
  switchLoopScheduled = true
  // Small delay to coalesce rapid-fire calls
  setTimeout(runSwitchLoop, 100)
}

async function runSwitchLoop() {
  switchLoopScheduled = false
  if (switchRunning) return

  while (nextEnvToSwitch !== null) {
    const env = nextEnvToSwitch
    nextEnvToSwitch = null
    const resolvers = switchResolvers
    switchResolvers = []

    switchRunning = true
    switchingRef.value = true
    try {
      await doSwitch(env)
    } catch (e) {
      console.error('[v86] doSwitch error:', e)
    } finally {
      // ALWAYS reset — even if doSwitch threw
      switchRunning = false
      serialMuted = false
      clearMuteWatchdog()
    }

    resolvers.forEach(r => r())
  }

  switchingRef.value = false
}

/**
 * The actual environment switch. Ultra-minimal:
 *   1. Ctrl+C to kill foreground
 *   2. cd /env/<name>  (no quotes, no special chars)
 *   3. clear           (no quotes, no special chars)
 *
 * NO export, NO PS1 changes, NO term.reset(), NO quoting of ANY kind.
 * BusyBox ash default PS1 shows CWD automatically.
 * This can NEVER leave the shell in a stuck state.
 */
async function doSwitch(envName: string) {
  await waitForBoot()
  await waitForReady()

  const emulator = v86Instance.value
  if (!emulator) return

  const envDir = `/env/${envName}`

  // Mute serial output to hide the cd command, with watchdog safety net
  serialMuted = true
  startMuteWatchdog()

  // Kill foreground process
  emulator.serial0_send('\x03')
  await delay(50)

  // cd to env directory — simple command, no quotes, no special chars
  await sendCmd(emulator, `cd ${envDir}`, 60)

  // Discard any buffered output from the muted period
  if (writeTimer) { clearTimeout(writeTimer); writeBuf = ''; writeTimer = null }

  // Unmute BEFORE sending clear, so the clear output + prompt are visible
  serialMuted = false
  clearMuteWatchdog()

  // Clear screen — user sees a clean prompt in the env directory
  await sendCmd(emulator, 'clear', 30)

  currentEnvName = envName
}

// ─── Public API ──────────────────────────────────────────────────────────────

export function useV86() {
  return {
    instance: v86Instance,
    booted: v86Booted,
    ready: readyRef,
    switching: switchingRef,
    initV86,
    waitForBoot,
  }
}
