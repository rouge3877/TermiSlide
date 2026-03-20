import { defineAppSetup } from '@slidev/types'
import { initV86, preloadAssets, attachSerialBridge, getOrCreateTerminal } from './v86'

// Load all environment configs (must happen before VM boots)
import '../environments'

export default defineAppSetup(() => {
  // 1. Preload assets with high priority
  preloadAssets()

  // 2. Start booting the VM immediately — don't wait for a terminal slide
  //    This overlaps the ~5s boot time with the user reading the title slide.
  initV86().then((emulator) => {
    // Set up the serial bridge and xterm early
    getOrCreateTerminal()
    attachSerialBridge(emulator)
  })
})
