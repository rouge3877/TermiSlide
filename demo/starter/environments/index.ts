/**
 * Environment loader — auto-imports all environment configs from this folder.
 *
 * To add a new environment:
 *   1. Create a new .ts file in this folder (e.g. networking.ts)
 *   2. Export a default LabEnvConfig object
 *   3. The file name (without .ts) becomes the environment name
 *
 * Each environment gets:
 *   - Its own directory: /home/student/<envName>/
 *   - Isolated env vars (HOME, PS1, etc.) on each visit
 *   - Init commands run once (on first visit) to set up files
 *
 * Then reference it in a slide:
 *   ---
 *   layout: terminal-split
 *   env: networking
 *   ---
 */
import { registerEnv } from '../setup/v86'

// Vite's import.meta.glob eagerly imports all .ts files in this directory
const envModules = import.meta.glob<{ default: import('../setup/v86').LabEnvConfig }>(
  './*.ts',
  { eager: true },
)

for (const [path, mod] of Object.entries(envModules)) {
  // Skip this loader file itself
  if (path === './index.ts') continue
  // Extract env name from filename: "./filesystem.ts" → "filesystem"
  const name = path.replace('./', '').replace('.ts', '')
  registerEnv(name, mod.default)
}
