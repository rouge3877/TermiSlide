# TermiSlide — Design Document

**An interactive, browser-based Linux terminal embedded in Slidev presentations.**

TermiSlide runs a real Linux kernel (via [v86](https://github.com/copy/v86) WebAssembly emulator) inside the browser. Each slide can reference a named "environment" that provides an isolated working directory with pre-configured files. There is no server — everything runs locally in WebAssembly.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│  Slidev Presentation                                    │
│                                                         │
│  ┌──────────────┐  ┌─────────────────────────────────┐  │
│  │  Slide        │  │  V86Terminal.vue                 │  │
│  │  Content      │  │  ┌───────────────────────────┐  │  │
│  │  (Markdown)   │  │  │  xterm.js                 │  │  │
│  │              │  │  │  (Terminal UI)             │  │  │
│  │              │  │  └──────────┬────────────────┘  │  │
│  └──────────────┘  │            │ serial bridge      │  │
│                    │  ┌──────────▼────────────────┐  │  │
│                    │  │  v86 Emulator (WASM)       │  │  │
│                    │  │  Linux Kernel + BusyBox    │  │  │
│                    │  │  /env/filesystem/           │  │  │
│                    │  │  /env/process/              │  │  │
│                    │  └───────────────────────────┘  │  │
│                    └─────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Changes from Upstream Slidev

All changes are confined to `demo/starter/`. No Slidev core packages were modified.

### New Files

| File | Purpose |
|------|---------|
| `setup/v86.ts` | Core VM lifecycle: boot, serial bridge, terminal singleton, environment switching |
| `setup/main.ts` | Slidev app setup — preloads assets and eagerly boots VM |
| `components/V86Terminal.vue` | Vue component: loading overlay + xterm container, manages slide activation |
| `layouts/terminal-split.vue` | Layout: left=markdown content, right=terminal |
| `environments/index.ts` | Auto-loader: scans `environments/*.ts` and registers them |
| `environments/filesystem.ts` | Example env: filesystem exploration lab |
| `environments/process.ts` | Example env: process management lab |
| `scripts/fetch-v86-assets.sh` | Downloads v86 engine + Linux kernel binaries to `public/` |
| `slides-terminal.md` | Demo slide deck using the terminal feature |
| `public/*.bin, *.js, *.wasm` | v86 engine + Linux kernel binaries (not committed, downloaded by script) |
| `DESIGN.md` | This file |

### Modified Files

| File | Change |
|------|--------|
| `package.json` | Added `@xterm/xterm` and `@xterm/addon-fit` dependencies |

### Dependencies Added

- **`@xterm/xterm`** — Terminal emulator UI (renders the terminal in the browser)
- **`@xterm/addon-fit`** — Auto-fits the terminal to its container

### VM Binaries (in `public/`, downloaded by script, NOT committed)

| File | Size | Source |
|------|------|--------|
| `buildroot-bzimage68.bin` | ~10 MB | Buildroot Linux kernel + initramfs |
| `v86.wasm` | ~2 MB | v86 emulator WebAssembly core |
| `libv86.js` | ~330 KB | v86 emulator JavaScript glue |
| `seabios.bin` | ~128 KB | SeaBIOS ROM |
| `vgabios.bin` | ~36 KB | VGA BIOS ROM |

---

## Key Design Decisions

### 1. Single VM, Muted Switching

One v86 emulator instance runs for the entire presentation. When switching between environment slides, the system sends `cd /env/<name>` and `clear` commands over the serial port. Output is temporarily muted during the switch so the user only sees a clean prompt.

### 2. No Quoting in Switch Commands

After extensive debugging, all shell commands sent during environment switching are quote-free (`cd /env/name`, `clear`). BusyBox ash's serial console can enter an unrecoverable state if a quoted command (`export PS1="..."`) is interrupted by Ctrl+C mid-parse. The minimal command set makes the switch immune to this class of bugs.

### 3. Serialized, Never-Concurrent Switching

A mutex-based loop (`switchRunning` flag) ensures only one `doSwitch()` executes at a time. Rapid slide navigation queues the latest-requested environment; earlier pending requests are dropped. A 100ms coalescing delay absorbs rapid-fire calls. `try/finally` guarantees the mutex and mute flags are always released.

### 4. Safety Watchdog

A 3-second watchdog timer auto-unmutes serial output if `serialMuted` gets stuck. This is a last-resort safety net that prevents permanent terminal freeze.

### 5. Eager Boot with Asset Preloading

The VM starts booting immediately when the Slidev app loads (`setup/main.ts`), not when the user navigates to a terminal slide. Assets are preloaded with `<link rel="preload">` tags. This overlaps the ~5s boot time with the user reading the title slide.

### 6. Environment Isolation via Directories

Each environment gets its own directory (`/env/<name>/`) created at boot time. Init commands (defined in `environments/*.ts`) populate these directories with lab-specific files. Switching environments is a simple `cd` — no chroot, no user switching, no nested shells.

---

## How to Add a New Environment

1. Create a file in `environments/`, e.g. `environments/networking.ts`:

```typescript
import type { LabEnvConfig } from '../setup/v86'

const config: LabEnvConfig = {
  description: 'Networking lab',
  hostname: 'net-lab',       // shown in prompt (optional)
  init: [
    'echo "Networking Lab" > README.md',
    'ip addr > interfaces.txt',
  ],
}

export default config
```

2. Reference it in a slide:

```markdown
---
layout: terminal-split
env: networking
---

# Networking Lab

Try `cat README.md` in the terminal.
```

That's it. The auto-loader in `environments/index.ts` picks up the new file automatically.

---

## How to Run

### Prerequisites

- Node.js 18+
- pnpm

### Setup

```bash
# 1. Clone and install dependencies
git clone <repo-url>
cd TermiSlide
pnpm install

# 2. Download v86 VM binaries (one-time, ~12 MB)
cd demo/starter
bash scripts/fetch-v86-assets.sh

# 3. Start the terminal slide deck
pnpm slidev slides-terminal.md
```

Open the URL shown in the terminal (usually `http://localhost:3030`).

### Usage

- **Slide 1**: Title slide. The VM boots in the background.
- **Slide 2**: Filesystem lab — terminal is at `/env/filesystem/` with sample files.
- **Slide 3**: Process lab — terminal switches to `/env/process/` with process-related files.
- **Slide 4**: Summary.

Navigate with arrow keys or spacebar. The terminal is fully interactive — you can type commands, run scripts, etc.

---

## File Structure

```
demo/starter/
├── components/
│   └── V86Terminal.vue          # Terminal component with loading overlay
├── environments/
│   ├── index.ts                 # Auto-loader (import.meta.glob)
│   ├── filesystem.ts            # Lab 1 config
│   └── process.ts               # Lab 2 config
├── layouts/
│   └── terminal-split.vue       # 50/50 split layout
├── public/                      # VM binaries (not committed)
│   ├── buildroot-bzimage68.bin
│   ├── libv86.js
│   ├── seabios.bin
│   ├── v86.wasm
│   └── vgabios.bin
├── scripts/
│   └── fetch-v86-assets.sh      # Downloads VM binaries
├── setup/
│   ├── main.ts                  # App setup: preload + eager boot
│   └── v86.ts                   # Core VM + terminal + env switching
├── slides-terminal.md           # Demo slide deck
├── package.json                 # Added xterm dependencies
├── DESIGN.md                    # This file
└── ...                          # Standard Slidev starter files
```
