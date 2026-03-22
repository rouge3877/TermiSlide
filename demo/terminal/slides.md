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

<!--
下午好，我是李雨轩。欢迎来到第二次ICS实验课。

本次tutorial由两部分构成，分别是Shell和GDB调试器。其中Shell的相关部分由我来讲解，GDB调试器的相关部分由唐堂助教来讲解。

开始之前需要说明的一些事情是，无论是Shell还是GDB调试器，都是非常庞大的主题，所以在有限时间内我们无法做到一个step by step的讲解。因此本次tutorial的目的是让大家对Shell和GDB调试器有一个初步的认识，并且认识到它们的重要性。真正想要通过这两个工具提升效率还需要大家进一步学习，本次课程主要希望起到一个引导的作用。

当然，如果你已经是一个Shell和GDB的熟练使用者，那么——feel free to absent.
-->

---

# Interactive with Computer System

As we all know, there are many ways to interact with a computer system: GUI, CLI, AR, VR, etc.

<div class="flex justify-center my-4">
  <img src="./assets/GUICLI.png" alt="GUI vs CLI" class="w-full max-w-xl" />
</div>

As a human being, we are more familiar with GUI, but CLI is also very powerful and efficient.

<!--
OK，我们进入主题。

如今计算机有着多种多样的交互接口让我们与之进行交互，有图形界面、命令行界面、语音输入甚至AR、VR等等。

对于大家少则几年多则十几年的计算机使用经验，图形界面应该是最为熟悉的。大家已经习惯了在vscode或者一些IDE中编写代码，然后通过鼠标点击按钮来进行编译、运行、调试等操作，也习惯了通过alt+tab来切换不同的窗口，通过鼠标和键盘来进行复制粘贴等操作。

不可否认的是，图形界面确实提供了一个很直观的交互界面，并且在90%的场景下都可以满足我们的需求。然而，它们也从根本上限制了你的操作方式——你不能点击一个不存在的按钮，也很难将两个应用程序连接在一起使用。所以为了充分利用计算机的能力，我们不得不回到与计算机交互的最基本的方式——命令行界面CLI。
-->

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

<!--
当然，课程的目的不是让大家放弃图形界面，而是让大家认识到命令行界面具有的优势——展示CLI在许多场景下的高效，以及灵活性和可组合使用的优势。以便在之后的某一天里，当你发现你要做的事情在图形界面下很难完成时，或者你所工作的环境压根不存在图形化界面时，大家能够有选择使用命令行界面来完成的能力。

本次tutorial主要从以下几个方面来讲解Shell：首先最基本的是认识shell，以及shell的基本操作；接下来会展示一些shell的实用或者fancy的工具；最后会进一步讨论如何使用shell script来提升工作效率，自动化地完成一些操作。在tutorial的进行中，我也会穿插互联网的一句黑话——RTFM，并简单地带领大家试着去阅读手册，这也是一个很重要的技能。
-->

---
layout: section
---

## 1. Basic Setup

<!--
那么说了这么多，首先是basic setup部分。
-->

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

<!--
想要使用CLI界面与计算机进行交互，首先需要一个terminal，确切来讲是terminal emulator。这个东西是一个运行在图形界面下的程序，它模拟了一个传统的终端。毕竟2025年了，大家应该很难有一个真正的终端了。在Linux下，大家可以使用gnome-terminal、konsole、xterm等等，Windows下也有Windows Terminal供大家使用。

或者大家也可以ssh到远程的Linux服务器上，关于ssh在第一次实验课上已经讲解过了，这里就不再赘述了。

当然，如果大家手上有运行某个Linux发行版的电脑，那么可以尝试按下Ctrl+Alt+F1~F6来进入一个virtual console。这个console是一个真正的终端，没有图形界面，只有一个光标在黑屏上闪烁，这个时候你就可以输入你的用户名和密码来登录系统了。

现在就会进入一个真正的CLI界面，你会发现有一个提示符跟着一个闪烁的光标，等待你的输入。
-->

---
layout: section
---

## 2. Shell: The "Shell" of the Kernel

<!--
这一切完成后，我们就可以开始使用shell了。Shell是一个运行在CLI环境下的程序，它是用户与操作系统内核之间的接口。用户通过shell来向操作系统内核发送命令，内核接收到命令后执行相应的操作并返回结果给用户。

几乎所有你能够接触到的平台都支持某种形式的shell，有些甚至还提供了多种shell供你选择。在Linux系统中，常见的shell有bash、zsh、sh等等，而在Windows系统中，常见的shell有cmd、powershell等等。作为计算机的学生，我们肯定是以Linux系统为主，并且本节课我们会以Bourne Again Shell（bash）为例来讲解。这是被最广泛使用的一种shell，它的语法和其他的shell都是类似的，它们中的很大一部分都是POSIX shell compatible的。
-->

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

<!--
当你打开终端时，你会看到一个提示符，这是shell最主要的文本接口，它告诉你shell正在等待你输入命令。命令最终会被shell解析。最简单的命令是执行一个程序，你可以选择指定路径，或者它会在PATH环境变量中查找。

Shell的命令格式通常是命令名+参数，参数之间用空格分隔。例如，ls -l /home/lyx，其中ls是命令名，-l和/home/lyx是参数。

我们可以发现，其实CLI界面的shell和图形界面的操作是一样的，我们都可以创建、管理文件、可以启动程序。在GUI下通过双击图标启动程序。相比于GUI，CLI还可以在程序进入死循环时通过Ctrl+C来终止程序，但是GUI下就不太好操作了，你或许需要打开任务管理器来终止程序。

在shell中同样有前后台的概念，我们可以通过&符号来让程序在后台运行，通过fg命令来将程序调回前台。jobs命令可以查看当前有哪些程序在后台运行，kill命令可以终止一个进程。此外，Ctrl+Z可以将一个程序挂起，bg命令可以将一个程序放到后台运行。
-->

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

<!--
在命令行环境下有着大量的命令，这些命令可以帮助我们完成各种各样的任务，例如查看文件内容，创建文件，删除文件，查看进程等等。

这里大家可以跟着右边的终端一起试一试。pwd查看当前目录，cd切换目录，mkdir创建目录。cat查看文件内容，cp复制文件，less分页查看文件——按q退出。

Shell还有许多其他功能，我们稍后解释。
-->

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

<!--
此外还有tar命令，可以用来打包文件。tar是tape archive的缩写，最早是用来将文件打包到磁带上的。现在我们用它来将多个文件或目录打包成一个文件。

注意-f选项一定要放在最后，因为它后面跟的是文件名。
-->

---

# `Tmux`

Usage Scenario: manage multiple terminal sessions

<div class="flex justify-center my-4">
  <img src="./assets/tmux.png" alt="tmux" class="w-1/2" />
</div>

- prefix key: <kbd>Ctrl + b</kbd>
- Client-Server model: `tmux` (server) + `tmux attach` (client)

<!--
tmux是一个终端复用器，它可以在一个终端窗口中创建多个会话、窗口和面板。它采用Client-Server模型，即使你断开SSH连接，tmux server中的会话仍然在运行，下次连接时可以通过tmux attach重新接入。

所有快捷键都需要先按prefix key（默认是Ctrl+b），然后再按对应的键。比如Ctrl+b再按%是垂直分屏，Ctrl+b再按"是水平分屏。
-->

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

<!--
还有grep命令，可以用来查找文件中的某些内容，它支持正则表达式。grep是Global Regular Expression Print的缩写。

-i可以忽略大小写，-r可以递归搜索整个目录，-n可以显示行号，-v可以反转匹配——也就是显示不包含匹配内容的行。
-->

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

<!--
因为课程实验所迫，你不得不使用Linux，不得不使用十分"落后"的命令行。你一边尝试新的命令，就这样探索着这个陌生的世界。有些时候你或许会遇到invalid command、invalid option、invalid argument等等错误。

然后你知道了，这个时候你需要RTFM——Read The Friendly Manual。你需要去阅读手册，去使用man这样一个命令来查看命令的手册。于是在命令行输入man然后敲了回车，只见屏幕上输出了一行信息：What manual page do you want? ……

man是系统自带的手册查看器，几乎所有命令都有对应的man page。如果觉得man page太长太复杂，可以试试tldr——它提供了更简洁的、以实际用例为主的帮助页面。

注意，有些命令比如cd是shell builtin，它没有独立的man page，需要用help cd来查看。
-->

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

<!--
还有find命令，可以用来查找文件，甚至可以用来对找到的文件执行一些操作。

find的-exec选项非常强大，它可以对每一个找到的文件执行指定的命令。花括号{}会被替换为找到的文件名，反斜杠分号\;表示命令结束。
-->

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

<!--
除此之外还有许多实用的工具。awk可以用来处理文本文件，sed可以用来编辑文本文件，ag是一个类似grep但更快的代码搜索工具，tree可以以树状结构列出目录。

还有一些有趣的工具，比如cmatrix可以在终端里显示黑客帝国的数字雨效果，sl则是——当你不小心把ls打成sl时会出现一辆蒸汽火车。
-->

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

<!--
上面介绍的一些命令或者工具有时你会发现在你的系统上并没有安装，这是因为有些命令或者工具并不是所有的Linux发行版都默认安装的，或者还没有被管理员安装。这个时候你可以通过包管理器来安装这些工具。包管理器是一个用来安装、卸载、更新软件包的工具，在不同的Linux发行版上有不同的包管理器，比如apt、yum、pacman等等。

或者，你也可以通过源码安装。这个时候你需要下载源码，然后解压，然后进入解压后的目录，然后执行configure、make、make install来安装。

当然，你也可以通过docker来运行一个Linux容器，这个时候你就可以在容器中安装你需要的工具，而不会影响到你的主机系统。
-->

---

# Communication: Pipe

A lot of CLI tools — communication is required to do complex jobs.

**Pipe `|`** : use the `stdout` of previous command as the `stdin` of the next.

<div class="flex justify-center my-4">
  <img src="./assets/pipe.png" alt="pipe" class="w-2/3" />
</div>

<!--
回到正题，上面展示的都是shell可以帮助我们执行一些命令，但实际上shell还有一个很重要的功能，就是pipe和重定向。

Pipe实际上是操作系统中提到的一种IPC（Inter-Process Communication）方式，大家在操作系统课程中应该学过。通俗来说，它可以将一个程序的输出作为另一个程序的输入，这样就可以将多个程序连接在一起使用，实现更复杂的功能。图很好地展示了这一点。比如我们可以通过 ls | wc -l 来统计当前目录下有多少个文件。
-->

---

# Communication: Redirect 1

**Redirect `>` & `<`** : `stdout` to file, or file to `stdin`.

<div class="flex justify-center my-4">
  <img src="./assets/redirect.png" alt="redirect" class="w-2/3" />
</div>

<!--
重定向则是将一个程序的输出重定向到一个文件中，或者将一个文件的内容重定向到一个程序中。

比如我们可以通过 ls > file.txt 来将ls的输出重定向到file.txt中，通过 cat < file.txt 来将file.txt的内容输出到屏幕上。
-->

---

# Communication: Redirect 2

File descriptors:
- **0** — `stdin`, the standard input stream.
- **1** — `stdout`, the standard output stream.
- **2** — `stderr`, the standard error stream.

<div class="flex justify-center my-4">
  <img src="./assets/redirect-test.png" alt="redirect test" class="w-2/3" />
</div>

<!--
好，我们现在有一个文件同时产生stdout和stderr的输出。如果我们执行>，会发现stderr的内容并没有被重定向到文件中。

这里就涉及到一个概念：stdout和stderr。stdout是标准输出，stderr是标准错误输出。它们的区别在于stdout是用来输出正常的程序输出，而stderr是用来输出错误信息的。这样做的好处是可以将正常的输出和错误的输出分开。

如果我们希望将stderr的内容也重定向到文件中，我们可以通过 2>&1 来实现，这个命令的意思是将stderr重定向到stdout中。当然，我们也可以通过 &> 来将stdout和stderr都重定向到一个文件中。还有一个特殊的文件 /dev/null，写入它的内容会被丢弃，可以用来抑制不需要的输出。
-->

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

<!--
上面我们展示了一些shell的基本功能，单独来看每一个功能都是很简单的，但是当我们将它们组合在一起使用时，就可以实现很多复杂的功能。

Pipe和重定向就是起到这样一个连接作用。此外还有 $() 用来做命令替换——将命令的执行结果替换到当前位置；<() 是进程替换——将命令的执行结果当做一个临时文件来使用，比如diff命令需要两个文件做比较，我们可以用 <() 将两个ls命令的结果作为"文件"传给diff。

这就是shell的强大之处：每个命令都很简单，但组合起来就是一种"自然编程语言"。
-->

---
layout: section
---

## 3. Shell Scripts

Shell is also a programming language, which allows you to combine a series of commands and execute.

<!--
好的，接下来进入第三部分：Shell Scripts。

Shell不仅仅是一个命令行解释器，它本身也是一门编程语言。我们可以把一系列命令写到一个文件里，然后一次性执行，这就是shell脚本。通过shell脚本可以自动化地完成很多重复性的操作，大大提升工作效率。
-->

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

<!--
在bash中，变量赋值使用等号，注意等号两边不能有空格！这是新手最容易犯的错误。

如果你写了 foo = bar，bash会把foo当成命令名，然后把=和bar当成它的两个参数，最终报错command not found。记住在shell scripts中空格是用来分隔参数的。
-->

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

<!--
字符串可以用单引号和双引号来定义，但它们的含义是不同的。单引号中的内容是原样输出，变量不会被替换。双引号中的变量会被替换为它们的值。

大家可以在右边的终端试一下，echo "$foo"会输出bar，而echo '$foo'会原样输出$foo这个字符串。
-->

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

<!--
Shell脚本也支持控制结构，包括if-else条件判断、for循环和while循环。语法和C语言不太一样，注意if后面需要then，结束需要fi，for和while结束需要done。

方括号[]实际上是test命令的简写形式，-f用来判断文件是否存在，-lt是less than的意思。大家注意方括号和表达式之间要有空格。
-->

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

<!--
test命令有三种写法，它们基本等价。注意数值比较使用-eq、-ne、-lt、-gt这些操作符，而字符串比较使用==和!=。千万不要搞混，否则结果可能不是你预期的。

双方括号[[]]是bash特有的增强版本，支持更多的特性比如正则匹配，但不是所有shell都支持。
-->

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

<!--
Shell脚本也可以定义函数。这里定义了一个mcd函数，它会先创建目录然后cd进去，非常实用。$1表示传给函数的第一个参数。

注意这里用source来加载脚本文件，因为source是在当前shell进程中执行脚本，而./mcd.sh会启动一个子进程，子进程中cd的效果不会影响到当前shell。
-->

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

<!--
Bash中有很多特殊变量。$0是脚本名，$1到$9是脚本的参数，$@是所有参数，$#是参数个数，$?是上一个命令的返回值——0表示成功，非0表示失败，$$是当前进程的PID。

还有一个非常实用的：双感叹号!!会被替换为上一条命令，所以当你执行了一个命令发现需要sudo权限时，可以直接输入sudo !!。
-->

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

<!--
Shebang——也就是脚本第一行的#!——告诉系统使用哪个解释器来执行这个脚本。#!/bin/bash表示使用bash来执行，#!/usr/bin/env python3表示使用python3来执行。

使用env的好处是它会在PATH中查找python3，这样脚本在不同系统上都能正确找到解释器，而不是硬编码路径。

注意写完脚本后需要chmod +x给它加上执行权限，然后才能用./来执行。
-->

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

<!--
最后提一下shell builtin。Shell builtins是内建在shell本身中的命令，而不是外部程序。比如cd、source、echo、export、alias等等。

它们和外部命令的区别在于，它们没有独立的man page，需要用help命令来查看帮助。还有一个重要区别是，像cd这样的命令必须是builtin——因为它需要改变当前shell进程的工作目录，如果是外部程序的话，它只会改变子进程的目录，对当前shell没有影响。

好的，Shell部分就到这里了，下面交给唐堂助教来讲解GDB部分。
-->

---
layout: section
---

## 4. GDB: The Core Workflow

**GDB (GNU Debugger)** uses the `ptrace` system call to control process execution, allowing you to inspect memory, registers, and execution flow.

<!--
好的，现在进入GDB部分。

GDB——GNU Debugger，是GNU项目中的调试器。它通过ptrace系统调用来控制另一个进程的执行，允许你检查内存、寄存器和执行流程。在ICS课程中，GDB是你排查程序bug的核心工具。
-->

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

<!--
在使用GDB之前，有一个很重要的前提条件：你必须在编译时加上-g选项。这会让编译器在可执行文件中嵌入DWARF格式的调试信息，包括变量名、类型、行号等元数据。

没有这些信息，GDB只能看到机器码和内存地址，无法将它们映射回你的C/C++源代码。大家可以在右边的终端试一下，对比加-g和不加-g的区别。
-->

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

<!--
GDB的基本工作流程是：启动、设断点、运行、单步执行。

需要注意的是gdb ./main只是加载了可执行文件和符号表，程序在这个阶段并没有开始执行。新手常犯的错误是输入gdb后立刻输入next，然后报错。必须通过run命令才能真正启动程序。

断点的底层机制是：GDB在目标地址替换了一条trap指令，当CPU执行到这条指令时，控制权会交还给GDB。step和next的区别在于，step会进入函数调用内部，而next会把整个函数调用当作一条语句执行完。
-->

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

<!--
当程序崩溃的时候，比如出现Segmentation Fault，最重要的事情就是知道它是怎么崩溃的——调用链是什么样的。

backtrace命令（简写bt）会打印出整个调用栈。它从当前的指令指针一直回溯到main函数，展示了完整的函数调用序列。你可以用frame N命令切换到任意一层栈帧，然后用info locals或print来检查那一层的局部变量。

在这个例子中，我们可以看到segfault.c中忘记了malloc，buffer是NULL，然后传给strcpy导致了崩溃。
-->

---
layout: section
---

## 5. GDB: The "Fancy" Operations

Once you have the basics, GDB provides tools that `printf` debugging simply cannot match.

<!--
掌握了基础操作之后，GDB还提供了一些非常强大的工具，这些是printf调试法无论如何都做不到的。
-->

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

<!--
你不需要IDE也可以进行可视化调试。GDB内置了一个TUI（Text User Interface）模式，输入layout src之后，屏幕会分成两部分，上面显示源代码并高亮当前执行的行，下面是GDB命令行。

每次你按next或step的时候，可以看到高亮的行在移动，这比盲目地输入命令要直观得多。如果程序的输出把TUI界面搞乱了，按Ctrl+L可以重新绘制。
-->

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

<!--
Watchpoint解决的问题是："我的变量被莫名其妙地修改了，但我不知道是哪段代码干的。"

Watchpoint利用了CPU的硬件调试寄存器，它会在指定的内存地址被写入时精确地暂停执行。与断点不同的是，你不需要知道bug在哪一行，只需要告诉GDB你想监视哪个变量。

在这个例子中，watchme.c里有一个隐藏的corrupt函数会把counter重置为-1。设置watch counter后，持续按continue，GDB会在每次counter被修改时停下来，你就能精确地找到是corrupt函数干的。
-->

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

<!--
条件断点解决的问题是：一个循环跑了100次甚至10000次，bug只在某一次迭代时出现。你总不能一直按continue按几千次吧？

条件断点允许你给断点附加一个布尔表达式。GDB每次命中断点时都会评估这个条件，但只有条件为真时才会暂停执行并把控制权交给你。

在这个例子中，conditional.c在第42次迭代时注入了一个错误值，我们用 break 19 if i == 42 直接跳到第42次迭代。
-->

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

<!--
这是真正称得上"Fancy"的操作——时间回溯调试。

传统调试中，一旦你step over了一个函数然后发现bug在那个函数里面，就只能重启程序重跑。但GDB的record-full模式可以记录程序执行过程中的所有状态变化（寄存器和内存修改），然后允许你反向执行。

reverse-continue会让GDB反向运行，直到碰到上一个断点。reverse-step和reverse-next则是逐行反向执行。这个功能可以有效打破大家"GDB难用且落后"的刻板印象——哪个IDE能让你倒着运行程序？
-->

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

<!--
在ICS课程中，你会大量接触指针和原始内存。x命令（examine）可以直接读取内存地址的内容。

x/4xw &nums 的意思是：从nums的地址开始，以十六进制(x)格式，每个word(w)大小（4字节），显示4个单元。你会看到0xDEADBEEF、0xCAFEBABE这些我们在memory.c中设置的魔数。

x/12cb msg 则是以字符(c)格式，每个byte(b)大小，显示12个单元，你会看到"Hello, GDB!"的每个字符。

x/5i main 则是以指令(i)格式显示main函数开头的5条机器指令。
-->

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

<!--
最后，学习Shell和GDB最好的方式就是去用它。这里列了一些推荐的学习资源：MIT的The Missing Semester、USTC的Linux101，以及The Art of Command Line。

希望今天的tutorial能够让大家对Shell和GDB有一个初步的认识，更重要的是在之后的实验和学习中，能够想起来去使用它们。感谢大家！
-->

