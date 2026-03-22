---
theme: default
title: Shell Tutorial
transition: slide-left
---

# `Shell` Tutorial

<div class="mt-4 text-lg text-gray-400">

- 2026-03-22
- [ICS@XJTU](https://xjtu-ics.github.io/)
- Tang Tang, Yuxuan Li

</div>

<div class="mt-8 text-sm text-gray-500 italic">

**A brief tutorial for beginners**, so feel free to absent if you are familiar with shell 🙉🙈

</div>

---

# Interactive with Computer System

As we all know, there are many ways to interact with a computer system: GUI, CLI, AR, VR, etc.

<div class="flex justify-center my-4">
  <img src="./assets/GUICLI.png" alt="GUI vs CLI" class="w-full max-w-xl" />
</div>

As a human being, we are more familiar with GUI, but CLI is also very powerful and efficient.

---

# Why should I use CLI?

1. Sometimes, **GUI is not available** (e.g. server, embedded system). And many powerful tools are CLI only (e.g. `git`, `ssh`, `vim`)
2. CLI is more **efficient** (e.g. `mv` v.s. drag and drop)
3. CLI is more **flexible** and **programmable** (e.g. `>`, `|`, `&&`)
4. <u>***ICS*** hopes you to use CLI 😂</u>

<div class="mt-8" />

### Overview

1. **Brief Intro**: all you need to know about starting using shell.
2. **Recommend**: basic but useful command line tools.
3. **Automation**: write a bash scripts.
4. **GDB**: debug like a pro.

> ***RTFM**: use `man` and `tldr`.*

---
layout: section
---

## 1. Basic Setup

---

# Basic Setup

1. Terminal (emulator): emulate a (text-based) terminal inside the GUI environment.
   - Linux: `kitty`, `gnome-terminal`, `konsole`, `xterm`, `terminator`, etc.
   - Windows: `Windows Terminal`
   - *Open `vscode` and <kbd>Ctrl + ~</kbd>*

<v-click>

2. `SSH` to server:

```bash
ssh <your stuid>-ics@igw.dfshan.net -p2291
```

</v-click>

<v-click>

3. ***Try the tty: <kbd>Ctrl + Alt + F1</kbd> (F1-F6, in some Linux distros)***

> **[The TTY demystified](https://www.linusakesson.net/programming/tty/)**

</v-click>

---
layout: section
---

## 2. Shell: The "Shell" of the Kernel

---
layout: terminal-split
env: shell-basics
---

# Shell Basics

We focus on [`bash shell`](https://www.gnu.org/software/bash/)

```bash
echo $0     # Check which shell you are using
```

```bash
command-name arg1 arg2 arg3 ...   # Basic format
```

<div class="text-sm mt-2">

| DO - | In GUI | In CLI |
|------|--------|--------|
| Create a file | Right click, New file | `touch filename` |
| Move a file | Drag and drop | `mv f1 f2` |
| Launch an app | Click icon | `./app` |
| Quit an app | Click close | <kbd>Ctrl+C</kbd> |
| Suspend an app | Minimize | <kbd>Ctrl+Z</kbd> |
| Background jobs | Task Manager | `jobs` |
| Foreground | Alt+Tab | `fg %n` |

</div>

---
layout: terminal-split
env: shell-basics
---

# Basic Tools (Commands)

Try them out in the terminal →

**Directories:** `pwd`, `cd`, `mkdir`

```bash
pwd
cd /tmp && pwd
cd - && pwd
mkdir -p test/sub
```

**Files:** `touch`, `cp`, `mv`, `rm`, `cat`, `less`

```bash
cat sample.txt
cp sample.txt copy.txt
less copy.txt        # press q to quit
```

**Others:** `sort`, `wc`, `echo`, `grep`, `chmod`

```bash
wc -l sample.txt
sort sample.txt
```

---
layout: terminal-split
env: shell-tools
---

# `Tar`

Usage Scenario: archive files in 1 bundle

- `-c`: create a tarball
- `-x`: open a tarball
- `-v`: verbose mode
- `-t`: list files in a tarball
- `-f`: specify file name — **always the last option**

```bash
tar -cf archive.tar project/
tar -tf archive.tar
tar -xf archive.tar -C /tmp/
ls /tmp/project/
```

```bash
# compress multiple items
tar -cvf bundle.tar fruits.txt project/
```

---

# `Tmux`

Usage Scenario: manage multiple terminal sessions

<div class="flex justify-center my-4">
  <img src="./assets/tmux.png" alt="tmux" class="w-1/2" />
</div>

- prefix key: <kbd>Ctrl + b</kbd>
- Client-Server model: `tmux` (server) + `tmux attach` (client)

---
layout: terminal-split
env: shell-tools
---

# `grep`

Usage Scenario: search for a specific string in a file

`grep` + regex

- `-i`: case insensitive
- `-r`: recursive search
- `-n`: show line number
- `-v`: invert match

```bash
grep "apple" fruits.txt
grep -n "an" fruits.txt
grep -i "HELLO" project/hello.txt
grep -r "hello" project/
grep -v "a" fruits.txt
```

---
layout: terminal-split
env: shell-tools
---

# Interlude: SO MANY COMMANDS 😭

How to learn them all?

- `-h`, `--help`
- **`man`**: the system's manual pager (<u>Ask the man XD</u>)

```bash
man ls
man -k ipc
man man
```

- **`tldr`**: https://github.com/tldr-pages/tldr
  - Simpler help pages focused on practical examples
  - `man tar` v.s. `tldr tar`

```bash
# Compare:
tar --help | head -20
```

> Some commands like `cd` are shell builtins — try `help cd`

---
layout: terminal-split
env: shell-tools
---

# `Find`

Usage Scenario: search files in a directory

- `-name`: search by name
- `-type`: search by type (`f` = file, `d` = dir)
- `-exec`: execute command on each file found

```bash
find . -type f -name "*.txt"
find . -type f -name "*.c"
find project/ -type d
```

<v-click>

```bash
# exec: cat all .txt files
find . -type f -name "*.txt" -exec cat {} \;
```

</v-click>

---

# More Tools

<div class="grid grid-cols-2 gap-4">
<div>

**Text Processing**
- `awk` — pattern scanning & processing
- `sed` — stream editor for filtering & transforming text

**Search**
- `ag` — code-searching tool (like `grep`)
- `tree` — list directories in tree format

</div>
<div>

**Monitoring**
- `htop` — interactive process viewer

**Network**
- `curl` — transfer data from/to server
- `ping`, `ssh`, `scp`

**Fun**
- `cmatrix` — Matrix rain effect
- `sl` — steam locomotive 🚂

</div>
</div>

---

# Install Software in CLI

**1. Package manager:** `apt` (Ubuntu/Debian), `brew` (macOS), `dnf` (Fedora), `pacman` (Arch)

```bash
apt search cmatrix
# https://command-not-found.com/
```

<v-click>

**2. [Build from source](https://github.com/abishekvashok/cmatrix)**

- Read README / INSTALL doc
- `configure` → `make` → `make install`

```bash
git clone https://github.com/abishekvashok/cmatrix.git
cd cmatrix
mkdir build && cd build
cmake ..
make
```

</v-click>

---

# Communication: Pipe

A lot of CLI tools — communication is required to do complex jobs.

**Pipe `|`** : use the `stdout` of previous command as the `stdin` of the next.

<div class="flex justify-center my-4">
  <img src="./assets/pipe.png" alt="pipe" class="w-2/3" />
</div>

---

# Communication: Redirect 1

**Redirect `>` & `<`** : `stdout` to file, or file to `stdin`.

<div class="flex justify-center my-4">
  <img src="./assets/redirect.png" alt="redirect" class="w-2/3" />
</div>

---

# Communication: Redirect 2

File descriptors:
- **0** — `stdin`, the standard input stream.
- **1** — `stdout`, the standard output stream.
- **2** — `stderr`, the standard error stream.

<div class="flex justify-center my-4">
  <img src="./assets/redirect-test.png" alt="redirect test" class="w-2/3" />
</div>

---
layout: terminal-split
env: shell-tools
---

# Combining Commands

Try these examples:

```bash
# 1. Count files in project/
find project/ -type f | wc -l

# 2. Fetch all #include lines
grep -r "#include" project/

# 3. Diff between two dirs
diff <(ls project/src) <(ls project/tests)
```

<v-click>

```bash
# 4. Disk usage in /usr/bin (top 5)
du -sh /usr/bin/* 2>/dev/null | sort -rh | head -5
```

</v-click>

<div class="mt-4 text-sm">

- `xargs` — build commands from stdin
- `<()` — process substitution (temp file)
- `$()` — command substitution

> Build temporary tool combinations — **a "natural programming language"**

</div>

---
layout: section
---

## 3. Shell Scripts

Shell is also a programming language, which allows you to combine a series of commands and execute.

---
layout: terminal-split
env: shell-scripts
---

# Variables

In `bash`, assign with `foo=bar`, access with `$foo`.

```bash
foo=bar
echo $foo
```

<v-click>

⚠️ **Notes:**

1. `foo = bar` (with spaces) will NOT work — bash interprets `foo` as a command with `=` and `bar` as arguments.
2. **In shell scripts, spaces separate arguments.**

```bash
foo = bar    # This is WRONG!
```

</v-click>

---
layout: terminal-split
env: shell-scripts
---

# Strings

Strings can be defined using `'` and `"`, but they have different meanings:

- **`'...'`** — literal strings, variables are **NOT** replaced.
- **`"..."`** — variables are replaced with their values.

```bash
foo=bar
echo "$foo"
echo '$foo'
```

<v-click>

Read more: [Bash Manual — Quoting](https://www.gnu.org/software/bash/manual/html_node/Quoting.html)

</v-click>

---
layout: terminal-split
env: shell-scripts
---

# Control Structures

```bash
# if-elif-else
if [ -f sample.txt ]; then
    echo "File exists"
else
    echo "Not found"
fi
```

```bash
# for loop
for i in 1 2 3 4 5; do
    echo "Number: $i"
done
```

```bash
# while loop
count=0
while [ $count -lt 3 ]; do
    echo "count=$count"
    count=$((count + 1))
done
```

---
layout: terminal-split
env: shell-scripts
---

# `test`

```bash
test expression
[ expression ]
[[ expression ]]
```

- `[ -e file ]` — if file exists, then true
- `[ string ]` — if string is not empty, then true
- `[ str1 != str2 ]` — if strings differ, then true
- `[ int1 -eq int2 ]` — if integers equal, then true

> ⚠️ **Do NOT confuse numeric and string comparison**

```bash
[ 1 -eq 1 ] && echo "equal"
[ "abc" != "def" ] && echo "different"
[ -e /etc/passwd ] && echo "exists"
```

---
layout: terminal-split
env: shell-scripts
---

# Functions

```bash
mcd () {
    mkdir -p "$1"
    cd "$1"
}
```

Try it:

```bash
source mcd.sh
mcd my_new_dir
pwd
```

<v-click>

> `$1` is the first argument passed to the function.

</v-click>

---
layout: terminal-split
env: shell-scripts
---

# Special Variables

`bash` uses many special variables:

<div class="text-sm">

| Variable | Meaning |
|----------|---------|
| `$0` | Script name |
| `$1`~`$9` | Script parameters |
| `$@` | All parameters |
| `$#` | Number of parameters |
| `$?` | Return value of previous command |
| `$$` | Process ID of current script |
| `!!` | Last command (try `sudo !!`) |
| `$_` | Last parameter of last command |

</div>

```bash
echo "Shell: $0, PID: $$"
ls /nonexistent 2>/dev/null; echo "Exit: $?"
```

---
layout: terminal-split
env: shell-scripts
---

# Shebang

`#!` tells the system which interpreter to use.

```bash
#!/bin/bash
echo "Hello, World!"
```

```bash
#!/usr/bin/env python3
# use env to find python3 in PATH
print("Hello, World!")
```

Try it:

```bash
echo '#!/bin/bash
echo "Hello from script!"
echo "PID: $$"' > hello.sh

chmod +x hello.sh
./hello.sh
```

---

# `builtin`

Shell builtins are commands built into the shell itself, not external programs.

- **`source`** (or **`.`**) — run commands in the **current** shell
- **`cd`** — change directory
- **`echo`**, **`export`**, **`alias`**, **`history`** ...

```bash
help cd
man bash-builtins
```

> Builtins have no separate man page — use `help <command>` or `man bash-builtins`.

---
layout: section
---

## 4. GDB: The Core Workflow

**GDB (GNU Debugger)** uses the `ptrace` system call to control process execution, allowing you to inspect memory, registers, and execution flow.

---
layout: terminal-split
env: gdb-basics
---

# Prerequisite: Debug Symbols

GDB operates on machine code. To map instructions back to source code, the compiler must embed **DWARF** metadata (variable names, types, line numbers).

**You must compile with `-g`:**

```bash
# Check the source
cat lifecycle.c
```

```bash
# Compile WITH debug symbols
gcc -g lifecycle.c -o lifecycle
```

<v-click>

```bash
# Without -g, GDB cannot show source
gcc lifecycle.c -o lifecycle_nodebug
gdb ./lifecycle_nodebug -batch -ex "b main" -ex "r" -ex "list"
```

</v-click>

---
layout: terminal-split
env: gdb-basics
---

# Start, Break, Run, Step

`gdb ./main` loads the executable — **it does not start the program yet**.

```bash
gdb ./lifecycle
```

Inside GDB, try this workflow:

```
(gdb) break main          # Set breakpoint
(gdb) run                 # Start execution
(gdb) next                # Step over (skip into functions)
(gdb) step                # Step into function call
(gdb) print a             # Inspect variable
(gdb) info locals         # All local variables
(gdb) continue            # Run until next breakpoint
(gdb) quit
```

<div class="text-sm mt-2">

- **Breakpoint**: GDB replaces the instruction at that address with a `trap` (`int 3` on x86). When the CPU hits it, control returns to GDB.
- **`step` vs `next`**: `step` enters function calls; `next` executes them as one unit.

</div>

---
layout: terminal-split
env: gdb-basics
---

# Backtrace: Understanding Crashes

When a program crashes (e.g., Segfault), `backtrace` shows the call chain that led to the crash.

```bash
gdb ./segfault
```

```
(gdb) run
# Program receives SIGSEGV...
(gdb) backtrace
(gdb) frame 1
(gdb) info locals
(gdb) print buffer
```

<v-click>

<div class="text-sm mt-2">

**Reading the backtrace:**

- `#0` — where the crash happened (`strcpy`)
- `#1` — who called it (`copy_data`)
- `#2` — who called *that* (`process` — `buffer` is `NULL` here!)
- `#3` — `main`

Use `frame N` to switch context and inspect local variables at each level.

</div>

</v-click>

---
layout: section
---

## 5. GDB: The "Fancy" Operations

Once you have the basics, GDB provides tools that `printf` debugging simply cannot match.

---
layout: terminal-split
env: gdb-basics
---

# TUI: Visual Debugging

GDB has a built-in terminal UI — no IDE needed.

```bash
gdb ./lifecycle
```

```
(gdb) break multiply
(gdb) run
(gdb) layout src
(gdb) next
(gdb) next
(gdb) step
```

<div class="text-sm mt-2">

| Command | Effect |
|---------|--------|
| `layout src` | Source code + current line |
| `layout asm` | Assembly view |
| `layout split` | Source + assembly |
| <kbd>Ctrl+X</kbd> <kbd>A</kbd> | Toggle TUI on/off |
| <kbd>Ctrl+L</kbd> | Redraw (if garbled) |

</div>

---
layout: terminal-split
env: gdb-basics
---

# Hardware Watchpoints

*"Something is modifying my variable, but I don't know where."*

A watchpoint uses the CPU's **hardware debug registers** to halt execution at the exact instruction that modifies a variable.

```bash
gdb ./watchme
```

```
(gdb) break main
(gdb) run
(gdb) watch counter
(gdb) continue
# GDB stops at each modification of counter.
# Keep pressing continue — notice when counter
# suddenly becomes -1. Check the backtrace!
(gdb) backtrace
```

<div class="text-sm mt-2">

- `watch var` — pause when `var` is **written**
- `rwatch var` — pause when `var` is **read**
- `awatch var` — pause on **any** access

</div>

---
layout: terminal-split
env: gdb-basics
---

# Conditional Breakpoints

*A loop runs 100 times. The bug is at iteration 42.*

Attach a condition to a breakpoint — GDB evaluates it on each hit, but only pauses when `true`.

```bash
gdb ./conditional
```

```
(gdb) break fill_array
(gdb) run
(gdb) break 19 if i == 42
(gdb) continue
(gdb) print i
(gdb) print arr[i]
```

<div class="text-sm mt-2">

**Syntax:** `break [location] if [condition]`

```
break utils.c:45 if i == 9999
break my_func if ptr == 0x0
```

</div>

---
layout: terminal-split
env: gdb-basics
---

# Reverse Debugging (Time Travel)

*Stepped over a function but the bug was inside it. No need to restart.*

GDB can record state changes and execute instructions **backwards**.

```bash
gdb ./watchme
```

```
(gdb) break main
(gdb) run
(gdb) target record-full
(gdb) continue
# Program finishes. counter is wrong.
(gdb) break corrupt
(gdb) reverse-continue
# GDB runs BACKWARDS to the last call to corrupt()!
(gdb) backtrace
(gdb) info locals
```

<div class="text-sm mt-2">

| Command | Effect |
|---------|--------|
| `target record-full` | Start recording |
| `reverse-step` (`rs`) | Step backward one line |
| `reverse-next` (`rn`) | Step back over a call |
| `reverse-continue` (`rc`) | Run back to prev breakpoint |

</div>

---
layout: terminal-split
env: gdb-basics
---

# Memory Inspection (`x` command)

In *ICS*, you deal with pointers and raw memory. The `x` command reads memory directly.

```bash
gdb ./memory
```

```
(gdb) break main
(gdb) run
(gdb) next 3
(gdb) x/4xw &nums
(gdb) x/12cb msg
(gdb) x/5i main
```

<div class="text-sm mt-2">

**Syntax:** `x/[Count][Format][Size] [Address]`

| Format | Meaning | Size | Meaning |
|--------|---------|------|---------|
| `x` | hex | `b` | byte (1) |
| `d` | decimal | `h` | halfword (2) |
| `c` | char | `w` | word (4) |
| `i` | instruction | `g` | giant (8) |

</div>

---
layout: end
---

## $. The Best Way to Learn it, is to Use it.

*"Unix is user-friendly; it's just choosy about who its friends are."*

<div class="mt-8 text-left text-sm">

- MIT — [The Missing Semester](https://missing-semester-cn.github.io/)
- USTC — [Linux101](https://101.ustclug.org/)
- [The Art of Command Line](https://github.com/jlevy/the-art-of-command-line)

</div>

