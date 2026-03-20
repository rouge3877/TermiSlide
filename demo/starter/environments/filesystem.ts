import type { LabEnvConfig } from '../setup/v86'

/**
 * Environment: filesystem
 *
 * An isolated environment for exploring the Linux filesystem.
 * User is chrooted — only sees files specific to this lab.
 */
const config: LabEnvConfig = {
  description: 'Filesystem exploration lab',
  hostname: 'fs-lab',
  init: [
    'echo "Welcome to the Filesystem Lab!" > README.md',
    'echo "This file was created by TermiSlide." >> README.md',
    'echo "#!/bin/sh" > hello.sh && echo "echo Hello from TermiSlide!" >> hello.sh && chmod +x hello.sh',
    'mkdir -p docs && echo "Sample document" > docs/example.txt',
  ],
}

export default config
