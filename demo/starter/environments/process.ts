import type { LabEnvConfig } from '../setup/v86'

/**
 * Environment: process
 *
 * An isolated environment for learning about Linux processes.
 * User is chrooted — only sees files specific to this lab.
 */
const config: LabEnvConfig = {
  description: 'Process management lab',
  hostname: 'proc-lab',
  init: [
    'echo "Lab: Process Management" > README.md',
    'cat /proc/cpuinfo > cpuinfo.txt',
    'echo "#!/bin/sh" > busyloop.sh && echo "while true; do :; done" >> busyloop.sh && chmod +x busyloop.sh',
  ],
}

export default config
