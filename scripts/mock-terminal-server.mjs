/**
 * Mock WebSocket server for testing WebTerminal component.
 * Simulates the Python Terminal Daemon protocol.
 *
 * Protocol:
 *   Client → Server:
 *     { type: "attach", env: string, cols: number, rows: number }
 *     { type: "input", data: string }
 *     { type: "resize", cols: number, rows: number }
 *   Server → Client:
 *     { type: "output", data: string }
 */

import { WebSocketServer } from 'ws'

const PORT = 8765
const wss = new WebSocketServer({ port: PORT })

console.log(`[MockTerminalServer] Listening on ws://localhost:${PORT}`)

/** Simple line-buffer per client to echo input */
const sessions = new WeakMap()

wss.on('connection', (ws) => {
  console.log('[MockTerminalServer] Client connected')
  sessions.set(ws, { env: null, lineBuffer: '' })

  ws.on('message', (raw) => {
    let msg
    try {
      msg = JSON.parse(raw.toString())
    }
    catch {
      console.log('[MockTerminalServer] Non-JSON message:', raw.toString())
      return
    }

    const session = sessions.get(ws)
    console.log('[MockTerminalServer] ←', JSON.stringify(msg))

    switch (msg.type) {
      case 'attach': {
        session.env = msg.env
        const welcome = [
          `\r\n\x1B[1;32m╔══════════════════════════════════════╗\x1B[0m`,
          `\x1B[1;32m║\x1B[0m  \x1B[1;36mTermiSlide Mock Terminal\x1B[0m           \x1B[1;32m║\x1B[0m`,
          `\x1B[1;32m║\x1B[0m  Environment: \x1B[1;33m${msg.env.padEnd(20)}\x1B[0m  \x1B[1;32m║\x1B[0m`,
          `\x1B[1;32m║\x1B[0m  Size: ${String(msg.cols).padEnd(3)}x${String(msg.rows).padEnd(15)}\x1B[0m  \x1B[1;32m║\x1B[0m`,
          `\x1B[1;32m╚══════════════════════════════════════╝\x1B[0m`,
          ``,
          `\x1B[90mType anything and press Enter to echo.\x1B[0m`,
          `\x1B[90mType "exit" to see disconnect message.\x1B[0m`,
          ``,
          `\x1B[1;32m${msg.env}\x1B[0m\x1B[1m $ \x1B[0m`,
        ].join('\r\n')
        ws.send(JSON.stringify({ type: 'output', data: welcome }))
        break
      }

      case 'input': {
        const data = msg.data
        for (const ch of data) {
          if (ch === '\r' || ch === '\n') {
            // Enter pressed - process line
            const line = session.lineBuffer.trim()
            session.lineBuffer = ''

            let response = '\r\n'
            if (line === 'exit') {
              response += '\x1B[1;31mGoodbye!\x1B[0m\r\n'
              ws.send(JSON.stringify({ type: 'output', data: response }))
              ws.close()
              return
            }
            else if (line === 'help') {
              response += [
                '\x1B[1;36mAvailable commands:\x1B[0m',
                '  \x1B[33mhelp\x1B[0m    - Show this message',
                '  \x1B[33mexit\x1B[0m    - Close connection',
                '  \x1B[33menv\x1B[0m     - Show current environment',
                '  \x1B[33mdate\x1B[0m    - Show current date/time',
                '  \x1B[33mcolors\x1B[0m  - Show color test',
                '  \x1B[90m(anything else is echoed back)\x1B[0m',
              ].join('\r\n')
            }
            else if (line === 'env') {
              response += `Environment: \x1B[1;33m${session.env}\x1B[0m`
            }
            else if (line === 'date') {
              response += `\x1B[1;34m${new Date().toISOString()}\x1B[0m`
            }
            else if (line === 'colors') {
              response += [
                '\x1B[31mRed\x1B[0m \x1B[32mGreen\x1B[0m \x1B[33mYellow\x1B[0m \x1B[34mBlue\x1B[0m \x1B[35mMagenta\x1B[0m \x1B[36mCyan\x1B[0m',
                '\x1B[1;31mBright Red\x1B[0m \x1B[1;32mBright Green\x1B[0m \x1B[1;33mBright Yellow\x1B[0m',
              ].join('\r\n')
            }
            else if (line.length > 0) {
              response += `echo: ${line}`
            }
            response += `\r\n\x1B[1;32m${session.env}\x1B[0m\x1B[1m $ \x1B[0m`
            ws.send(JSON.stringify({ type: 'output', data: response }))
          }
          else if (ch === '\x7F' || ch === '\b') {
            // Backspace
            if (session.lineBuffer.length > 0) {
              session.lineBuffer = session.lineBuffer.slice(0, -1)
              ws.send(JSON.stringify({ type: 'output', data: '\b \b' }))
            }
          }
          else if (ch >= ' ') {
            // Printable character - echo and buffer
            session.lineBuffer += ch
            ws.send(JSON.stringify({ type: 'output', data: ch }))
          }
          else if (ch === '\x03') {
            // Ctrl+C
            session.lineBuffer = ''
            ws.send(JSON.stringify({ type: 'output', data: '^C\r\n' + `\x1B[1;32m${session.env}\x1B[0m\x1B[1m $ \x1B[0m` }))
          }
        }
        break
      }

      case 'resize': {
        console.log(`[MockTerminalServer] Terminal resized to ${msg.cols}x${msg.rows}`)
        break
      }

      default:
        console.log('[MockTerminalServer] Unknown message type:', msg.type)
    }
  })

  ws.on('close', () => {
    console.log('[MockTerminalServer] Client disconnected')
    sessions.delete(ws)
  })
})
