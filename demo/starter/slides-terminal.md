---
theme: seriph
title: TermiSlide - Interactive Terminal Slides
transition: slide-left
---

# TermiSlide

Interactive Linux terminal in your slides

Press **Space** to begin the first lab.

---
layout: terminal-split
env: filesystem
---

# Lab 1: Exploring the Filesystem

Welcome to your first lab! On the right you have a live Linux terminal.

Try running these commands:

```bash
ls -la
cat README.md
./hello.sh
```

### Objectives

- Navigate the filesystem using `cd` and `ls`
- View file contents with `cat`
- Run a shell script

---
layout: terminal-split
env: process
---

# Lab 2: Process Management

The terminal has switched to a new environment.

Try running these commands:

```bash
ls
cat README.md
ps aux
top -b -n 1 | head -20
```

### Objectives

- List running processes with `ps`
- Use `top` to monitor system resources
- Kill a process with `kill`

---

# Summary

You completed two interactive labs using a real Linux kernel running in your browser!

- **Lab 1:** Filesystem exploration
- **Lab 2:** Process management

The entire environment ran locally via WebAssembly — no server needed.
