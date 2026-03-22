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

**A brief tutorial for beginners**, so feel free to absent if you are familiar with Linux shell 🙉🙈

</div>

<!--
下午好，我是李雨轩。欢迎来到第二次ICS实验课。

本次tutorial由两部分构成，分别是Shell和GDB调试器。以及BombLab的实验指导。其中Shll由我

开始之前需要说明的一些事情是，无论是Shell还是GDB调试器，都是非常庞大的主题，所以在有限时间内我们无法做到一个step by step的讲解。因此本次tutorial的目的是让大家对Shell和GDB调试器有一个初步的认识，并且认识到它们的重要性。真正想要通过这两个工具提升效率还需要大家进一步学习，本次课程主要希望起到一个引导的作用。

-->

---

# Interactive with Computer System

As we all know, there are many ways to interact with a computer system: GUI, CLI, AR, VR, etc.

<div class="flex justify-center my-4">
  <img src="./assets/GUICLI.png" alt="GUI vs CLI" class="w-full max-w-xl" />
</div>

As a human being, we are more familiar with GUI, but CLI is also very powerful and efficient.

<!--

通俗来讲，shell是OS Kernel和人类之间的交互接口

如今计算机有着多种多样的交互接口让我们与之进行交互，有图形界面、命令行界面、语音输入甚至AR、VR等等。

对于大家少则几年多则十几年的计算机使用经验，图形界面应该是最为熟悉的。大家已经习惯了在vscode或者一些IDE中编写代码，然后通过鼠标点击按钮来进行编译、运行、调试等操作，也习惯了通过alt+tab来切换不同的窗口，通过鼠标和键盘来进行复制粘贴等操作。

不可否认的是，图形界面确实提供了一个很直观的交互界面，并且在90%的场景下都可以满足我们的需求。然而，它们也从根本上限制了你的操作方式——你不能点击一个不存在的按钮，也很难将两个应用程序连接在一起使用。所以为了充分利用计算机的能力，我们不得不回到与计算机交互的最基本的方式——命令行界面CLI。而Linux 系统的shell就是这样一个CLI界面，它是我们与操作系统内核进行交互的接口。
-->

---

# Why should I use Linux Shell?

1. **GUI is not available Sometimes** (e.g. server, embedded system). Many powerful tools are CLI only (e.g. `git`, `ssh`, `vim`)
2. CLI is more **efficient**, **flexible** and **programmable** (e.g. `>`, `|`, `&&`)
3. The So-Called "Unix Philosophy" [^xx]
4. <u>***ICS*** hopes you to use CLI 😂</u>

<div class="mt-8" />

### LLM's Perspective:

"**bash is all agent need**"

[https://www.youtube.com/watch?v=TqC1qOfiVcQ&t=2520s](https://www.youtube.com/watch?v=TqC1qOfiVcQ&t=2520s)

[^xx]: Generally, CLI is a broader concept that encompasses any text-based interface for interacting with a computer system, while Shell is a specific type of CLI that provides a command-line interface for users to interact with the operating system. But here we use them interchangeably for simplicity.


<!--
当然，课程的目的不是让大家放弃图形界面，而是让大家认识到命令行界面具有的优势——展示CLI在许多场景下的高效，以及灵活性和可组合使用的优势。

无论如何，学习使用CLI界面下的shell工具 在**不远的曾经**有很多理由：
- 服务器通常没有图形界面，许多强大的工具只有CLI版本
- 你能通过简单的组合命令来达到原本不存在的功能
- 你能通过编写shell脚本更快捷的实现一些自动化
- 你不得不用Linux，而Shell以及一些CLI工具是你仅有的工具


如果这还不能说服你，那么随着LLM以及各式Agent的告诉迭代，我们或许能在LLM时代找到一个更能够说服你的理由：

Anthropic 的工程师 在一场关于 Claude Agent SDK 的分享中，提出了一个观点。他认为，最强大的 Agent 工具，不是无数个定制的 API，而是开发者最熟悉的两样东西：Bash 和文件系统。

他表示这套基于 Unix 哲学的 Agent 构建思路，展现出远超传统 API 工具模式的灵活性和潜力。它预示着，AI Agent 不必是一个 API 调用大师，而是一个在虚拟环境中自主工作的工程师。Bash 和它背后的庞大命令行工具生态，是几十年来软件工程的最佳实践沉淀。

所以即使是在有这个LLM时代，Shell依然是一个非常重要的工具，如果对于shell不了解，那么或许未来一个你正在vibecoding的下午，一个LLM出现幻觉的下午，夹在一条Shell命令中的一个小小错误被不怎么看得懂Shell的你通过，于是整个生产环境开始崩塌，你所在的企业瞬间崩盘，那时你可能会想，如果我大学时期好好学一下Shell就好了……

-->


---


# Overview

1. **Brief Intro**: all you need to know about starting using shell.
2. **Recommend**: basic but useful command line tools.
3. **Automation**: write a bash scripts.

<div class="mt-8" />

4. **GDB**: debug like a pro.


<!-- 
本次tutorial主要从以下几个方面来讲解Shell：首先最基本的是认识shell，以及shell的基本操作；接下来会展示一些shell的实用或者fancy的工具；最后会进一步讨论如何使用shell script来提升工作效率，自动化地完成一些操作。

此外，本次Tutorial的第二部分会介绍GDB调试器以及如何调试。
GDB非常重要的一个工具，也是是ICS课程实验中非常重要的一环，它可以帮助你排查程序中的bug，理解程序的执行流程，以及分析程序的性能瓶颈。通过学习GDB，你可以更深入地理解计算机系统的工作原理，以及如何编写高效、可靠的代码。
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

We focus on [`bash shell`](https://www.gnu.org/software/bash/)


<!--
这一切完成后，我们就可以开始使用shell了。Shell是一个运行在CLI环境下的程序，它是用户与操作系统内核之间的接口。用户通过shell来向操作系统内核发送命令，内核接收到命令后执行相应的操作并返回结果给用户。

几乎所有你能够接触到的平台都支持某种形式的shell，有些甚至还提供了多种shell供你选择。在Linux系统中，常见的shell有bash、zsh、sh等等，而在Windows系统中，常见的shell有cmd、powershell等等。作为计算机的学生，我们肯定是以Linux系统为主，并且本节课我们会以Bourne Again Shell（bash）为例来讲解。这是被最广泛使用的一种shell，它的语法和其他的shell都是类似的，它们中的很大一部分都是POSIX shell compatible的。
-->

---
layout: terminal-split
env: shell-basics
---

# Shell Basics

```bash
# Basic format
command-name arg1 arg2 arg3 ...
```

<div class="text-sm mt-2">

| DO - | In GUI | In CLI |
|------|--------|--------|
| Launch an app | Click icon | `./<app name>` |
| Quit an app | Click close | <kbd>Ctrl+C</kbd> |
| Suspend an app | Minimize | <kbd>Ctrl+Z</kbd> |
| Background jobs | Task Manager | `jobs` |
| Foreground | Alt+Tab | `fg %n` |

</div>

<!--
当你打开终端时，你会看到一个提示符，这是shell最主要的文本接口，它告诉你shell正在等待你输入命令。命令最终会被shell解析。

正如我们刚刚所说，存在许多不同的shell，但它们的基本操作都是类似的。你可以通过执行:
```bash
echo $0
```
来查看你当前使用的shell是什么。

Shell的命令格式通常是命令名+参数，参数之间用空格分隔。


最简单的命令是执行一个程序，你可以选择指定路径，或者它会在PATH环境变量中查找。
PATH 是一个环境变量，可以理解为一个目录列表，当你输入一个命令时，shell会在这些目录中查找对应的可执行文件。你可以通过 

```bash
echo $PATH
```

来查看当前的PATH环境变量。


好，比如我们现在有一个叫welcome的程序，我们可以通过./welcome来执行它，前面的./表示当前目录。或者如果welcome在PATH中的某个目录下，我们也可以直接输入welcome来执行它。比如程序 yes 就在/usr/bin目录下，我们可以直接输入yes来执行它。

[;;;;;;;;;;;;;]

我们可以发现，其实CLI界面的shell和图形界面的操作是一样的，我们都可以创建、管理文件、可以启动程序。在GUI下通过双击图标启动程序。相比于GUI，CLI还可以在程序进入死循环时通过Ctrl+C来终止程序，但是GUI下就不太好操作了，你或许需要打开任务管理器来终止程序。

在shell中同样有前后台的概念，我们可以通过&符号来让程序在后台运行，通过fg命令来将程序调回前台。jobs命令可以查看当前有哪些程序在后台运行，kill命令可以终止一个进程。此外，Ctrl+Z可以将一个程序挂起


-->

---
layout: terminal-split
env: shell-basics
---

# Basic Commands

Try them out in the terminal →

**Directories:** `pwd`, `cd`, `mkdir`



**Files:** `touch`, `cp`, `mv`, `rm`, `cat`, `less`


**Others:** `sort`, `wc`, `echo`, `grep`, `chmod`



<!--
在命令行环境下有着大量的命令，这些命令可以帮助我们完成各种各样的任务，例如查看文件内容，创建文件，删除文件，查看进程等等。

这里大家可以跟着右边的终端一起试一试。pwd查看当前目录，cd切换目录，mkdir创建目录。cat查看文件内容，cp复制文件，less分页查看文件——按q退出。

```bash
pwd
cd /tmp && pwd
cd - && pwd
mkdir -p test/sub
```


```bash
cat sample.txt
cp sample.txt copy.txt
less copy.txt        # press q to quit
```

```bash
wc -l sample.txt
sort sample.txt
```
其中sort是字典序，如果想让其按照line后面的数字排序，

```
sort -k 2,2n sample.txt
sort -V sample.txt
```

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




<!--
此外还有tar命令，可以用来打包文件。tar是tape archive的缩写，最早是用来将文件打包到磁带上的。现在我们用它来将多个文件或目录打包成一个文件。

举个例子，现在目录下有一个project目录，我现在想要把她打包成一个archive.tar的文件，我就可以使用tar -cvf archive.tar project/这个命令来实现。-c表示create，-v表示verbose，会显示打包的过程，-f表示指定文件名，archive.tar就是我们要创建的tarball的名字。

然后我们可以通过tar -tf archive.tar来查看这个tarball里面有什么文件。以及通过tar -xf archive.tar -C /tmp/来将这个tarball解压到/tmp/目录下。解压完成后我们可以通过ls /tmp/project/来查看解压后的文件。

```bash
tar -cvf archive.tar project/
tar -tf archive.tar
tar -xf archive.tar -C /tmp/
ls /tmp/project/
```

注意-f选项一定要放在最后，因为它后面跟的是文件名。

此外，tar还支持gzip和bzip2等压缩算法，我们可以通过下面的命令把fruits.txt和project目录一起打包成一个压缩包

```bash
tar -cvf bundle.tar fruits.txt project/
```


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


<!--
还有grep命令，可以用来查找文件中的某些内容，它支持正则表达式。grep是Global Regular Expression Print的缩写。

-i可以忽略大小写，-r可以递归搜索整个目录，-n可以显示行号，-v可以反转匹配——也就是显示不包含匹配内容的行。



1. 我们现在要在fruits.txt这个文件中查找包含apple这个字符串的行，直接使用grep "apple" fruits.txt就可以了。
2. 如果我们想要知道这个字符串在文件中的哪一行，我们可以加上-n选项，这样就会在输出的每一行前面显示行号。
3. 如果我们想要忽略大小写来搜索，我们可以加上-i选项，这样就会同时匹配hello、Hello、HELLO等等。
4. 如我们想要在一个目录下递归搜索，我们可以加上-r选项，这样就会在project目录下的所有文件中搜索包含hello这个字符串的行。
5. 如果我们想要显示不包含a这个字符串的行，我们可以加上-v选项，这样就会反转匹配，显示所有不包含a的行。

```bash
grep "apple" fruits.txt 
grep -n "an" fruits.txt 
grep -i "HELLO" project/hello.txt 
grep -r "hello" project/ 
grep -v "a" fruits.txt 
```

当然，还支持正则表达式，比如我们想要匹配以ne结尾的字符串，我们可以使用

```bash
grep -P "ne$" fruits.txt
```

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

<!--
还有find命令，可以用来查找文件，甚至可以用来对找到的文件执行一些操作。

举个例子:

1. 你可以通过通配符，以及 -type选项来查找当前目录下所有的.txt文件，或者所有的.c文件
2. 或者你可以通过-type d来查找当前目录下的所有目录。

```bash
find . -type f -name "*.txt"
find . -type f -name "*.c"
find project/ -type d
```


find的-exec选项非常强大，它可以对每一个找到的文件执行指定的命令。花括号{}会被替换为找到的文件名，反斜杠分号\;表示命令结束。


```bash
find . -type f -name "*.c" -exec cat {} \;

# 进一步
find . -type f -name "*.c" -exec echo ---{}--- \; -exec cat {} \;
```

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
layout: terminal-split
env: shell-tools
---

###  SO MANY COMMANDS 😭

How to learn them all?

<v-click>

**RTFM——Read The Friendly Manual!**

- `-h`, `--help`
- **`man`**: the system's manual pager (<u>Ask the man XD</u>)
  - `man <command>` — read manual for a command
  - `man -k <keyword>` — search manuals by keyword
  - `man man` — read manual for man itself!

<div class="mt-8" />


> Some commands like `cd` are shell builtins — try `help cd`/ find builtin in `man bash` to learn more.

</v-click>

<!--
因为课程实验所迫，你不得不使用Linux，不得不使用十分"落后"的命令行。你一边尝试新的命令，就这样探索着这个陌生的世界。有些时候你或许会遇到invalid command、invalid option、invalid argument等等错误。

然后你知道了，这个时候你需要RTFM——Read The Friendly Manual。你需要去阅读手册，去使用man这样一个命令来查看命令的手册。于是在命令行输入man然后敲了回车，只见屏幕上输出了一行信息：What manual page do you want? ……

man是系统自带的手册查看器，几乎所有命令都有对应的man page。

```bash
man ls
man -k ipc
man man
```


注意，有些命令比如cd是shell builtin，它没有独立的man page，需要用help cd来查看。
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
Shell builtin。Shell builtins是内建在shell本身中的命令，而不是外部程序。比如cd、source、echo、export、alias等等。

它们和外部命令的区别在于，它们没有独立的man page，需要用help命令来查看帮助。还有一个重要区别是，像cd这样的命令必须是builtin——因为它需要改变当前shell进程的工作目录，如果是外部程序的话，它只会改变子进程的目录，对当前shell没有影响。

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

当然，绝大部分情况下系统自带的包管理工具安装需要管理员权限，如果你没有管理员权限，那么你就需要通过源码来安装了。

这个时候你需要下载源码，然后解压，然后进入解压后的目录，

比如一个常见的按照流程如下：
然后执行configure、make、make install来安装。


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

还有一个CLI下比较好用的工具是Tmux

tmux是一个终端复用器，它可以在一个终端窗口中创建多个会话、窗口和面板。它采用Client-Server模型，即使你断开SSH连接，tmux server中的会话仍然在运行，下次连接时可以通过tmux attach重新接入。

所有快捷键都需要先按prefix key（默认是Ctrl+b），然后再按对应的键。比如Ctrl+b再按%是垂直分屏，Ctrl+b再按"是水平分屏。
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


- `xargs` — build commands from stdin
- `<()` — process substitution (temp file)
- `$()` — command substitution

<div class="mt-8" />


> Build temporary tool combinations — **a "natural programming language"**


<!--
上面我们展示了一些shell的基本功能，单独来看每一个功能都是很简单的，但是当我们将它们组合在一起使用时，就可以实现很多复杂的功能。

Pipe和重定向就是起到这样一个连接作用。此外还有 $() 用来做命令替换——将命令的执行结果替换到当前位置；<() 是进程替换——将命令的执行结果当做一个临时文件来使用，比如diff命令需要两个文件做比较，我们可以用 <() 将两个ls命令的结果作为"文件"传给diff。

这就是shell的强大之处：每个命令都很简单，但组合起来就是一种"自然编程语言"。


这里体哦那个几个例子：

1. 统计当前目录下有多少个文件，ls -l会列出当前目录下的所有文件和目录，每行一个，然后通过wc -l来统计行数，也就是文件的数量。
2. 找到当前项目中所有的include的行，grep -r会递归搜索当前目录下的所有文件，找到包含#include的行并输出。


```bash
find project/ -type f | wc -l

grep -ro "#include <[^>]*>" project/ | sort | uniq -c | sort -rn

其中<[^>]*>是一个正则表达式，表示匹配以<开头，以>结尾的字符串，中间可以有任意字符但不能有>。


diff <(ls project/src) <(ls project/tests)
```

还有，你可以查看/usr/bin目录下每个文件的大小，并且按照大小排序，显示前5个最大的文件：

```bash
du -sh /usr/bin/* 2>/dev/null | sort -rh | head -5
```
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



⚠️ **Notes:**

1. `foo = bar` (with spaces) will NOT work — bash interprets `foo` as a command with `=` and `bar` as arguments.
2. **In shell scripts, spaces separate arguments.**

```bash
# This is WRONG!
foo = bar
```


<!--

进入shell脚本的第一个话题：变量。变量是用来存储数据的，我们可以通过变量来传递数据，或者在脚本中使用一些动态的值。

```bash
foo=bar
echo $foo
```


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



Read more: [Bash Manual — Quoting](https://www.gnu.org/software/bash/manual/html_node/Quoting.html)


<!--
字符串可以用单引号和双引号来定义，但它们的含义是不同的。单引号中的内容是原样输出，变量不会被替换。双引号中的变量会被替换为它们的值。


在右边的终端试一下，echo "$foo"会输出bar，而echo '$foo'会原样输出$foo这个字符串。

```bash
foo=bar
echo "$foo"
echo '$foo'
```

-->

---
layout: terminal-split
env: shell-scripts
---

# Control Structures

```bash
# if elif else format
if [ condition ]; then
    # code if condition is true
elif [ condition2 ]; then
    # code if condition2 is true
else
    # code if all conditions are false
fi
```

```bash
# For loop format
for var in list; do
    # code to execute for each item in list
done
```

```bash
# While loop format
while [ condition ]; do
    # code to execute while condition is true
done
```

<!--
Shell脚本也支持控制结构，包括if-else条件判断、for循环和while循环。语法和C语言不太一样，注意if后面需要then，结束需要fi，for和while结束需要done。


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
- `[ s1 != s2 ]` — if strings differ, then true
- `-lt`, `-gt`, `-le`, `-ge` for numeric comparison

<div class="mt-8" />

### `&&` and `||`
- `cmd1 && cmd2` — execute `cmd2` if `cmd1` succeeds (exit code 0)
- `cmd1 || cmd2` — execute `cmd2` if `cmd1` fails (non-zero exit code)



<!--
test命令有三种写法，它们基本等价。注意数值比较使用-eq、-ne、-lt、-gt这些操作符，而字符串比较使用==和!=。千万不要搞混，否则结果可能不是你预期的。

双方括号[[]]是bash特有的增强版本，支持更多的特性比如正则匹配，但不是所有shell都支持。

此外，shell脚本中的命令执行结果是通过exit code来表示的，0表示成功，非0表示失败。我们可以通过&&和||来根据命令的执行结果来决定是否执行下一个命令。

1. 比如第一个命令，如果条件成立，那么test命令会返回0，&&后面的echo命令就会被执行，输出"equal"。
2. 第二个命令，如果条件成立，那么test命令会返回0，&&后面的echo命令就会被执行，输出"different"。
3. 第三个命令，如果/etc/passwd这个文件存在，那么test命令会返回0，&&后面的echo命令就会被执行，输出"exists"。




```bash
[ 1 -eq 1 ] && echo "equal"
[ "abc" != "def" ] && echo "different"
[ -e /etc/passwd ] && echo "exists"
```

此外我们还可以通过 `echo $?` 来查看上一个命令的exit code。

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
| `$_` | Last parameter of last command |

</div>


<!--
Bash中有很多特殊变量。$0是脚本名，$1到$9是脚本的参数，$@是所有参数，$#是参数个数，$?是上一个命令的返回值——0表示成功，非0表示失败，$$是当前进程的PID。

特别的，如果直接echo $0, 正如果你是在bash中输入的，那么它会输出bash；如果你是在一个脚本中输入的，那么它会输出脚本的名字。


```bash
echo "Shell: $0, PID: $$"
ls /nonexistent 2>/dev/null; echo "Exit: $?"
```

$_也很实用，它会保存上一个命令的最后一个参数。比如你cat ./mcd.sh, 发现要改动这个脚本，那么你可以直接输入vim $_来打开这个文件。

```bash
cat ./mcd.sh
vim $_
```


!! 也很实用，比如你输入了一个需要管理员权限的命令，结果提示权限不足，这时候你可以输入sudo !!来重新执行上一个命令，这样就不需要重新输入命令了。

```
apt install gcc
sudo !!
```

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



<!--

现在我们已经基本掌握了shell脚本的语法和功能了，最好我们来看看shell脚本的第一行通常会有一个特殊的标记：Shebang。
or HashBang

Shebang——也就是脚本第一行的#!——告诉系统使用哪个解释器来执行这个脚本。#!/bin/bash表示使用bash来执行，#!/usr/bin/env python3表示使用python3来执行。

尽管我们可以直接使用 bash script.sh来执行一个shell脚本，但如果我们在脚本的第一行加上了shebang，并且给这个脚本加上了执行权限，那么我们就可以直接通过./script.sh来执行它了。


注意写完脚本后需要chmod +x给它加上执行权限，然后才能用./来执行。

Try it:

```bash

chmod +x hello.sh
./hello.sh
```


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

**You must compile with `-g`**

<!--
在使用GDB之前，有一个很重要的前提条件：你必须在编译时加上-g选项。这会让编译器在可执行文件中嵌入DWARF格式的调试信息，包括变量名、类型、行号等元数据。

没有这些信息，GDB只能看到机器码和内存地址，无法将它们映射回你的C/C++源代码。大家可以在右边的终端试一下，对比加-g和不加-g的区别。

```bash
# Check the source
cat lifecycle.c
```

```bash
# Compile WITH debug symbols
gcc -g lifecycle.c -o lifecycle
```

这里的-batch选项让GDB在执行完命令后自动退出，-ex选项用来指定要执行的命令。
我们在这里设置了一个断点，运行程序，然后列出当前执行的源代码行。后面会解释这些命令的含义。
这里的重点是，如果你不加-g，那么GDB就无法显示源代码了，因为它没有调试信息来告诉它每个机器指令对应的源代码行是什么。

```bash
# Without -g, GDB cannot show source
gcc lifecycle.c -o lifecycle_nodebug
gdb ./lifecycle_nodebug -batch -ex "b main" -ex "r" -ex "list"
```

-->

---
layout: terminal-split
env: gdb-basics
---

# Start, Break, Run, Step

`gdb ./main` loads the executable — **it does not start the program yet**.

```bash
# Try Gdb
gdb ./lifecycle
```

Inside GDB, try this workflow:

<div class="text-sm mt-2">

- **Breakpoint**: GDB replaces the instruction at that address with a `trap` (`int 3` on x86). When the CPU hits it, control returns to GDB.
- **`step` vs `next`**: `step` enters function calls; `next` executes them as one unit.

</div>

<!--
GDB的基本工作流程是：启动、设断点、运行、单步执行。




需要注意的是gdb ./main只是加载了可执行文件和符号表，程序在这个阶段并没有开始执行。新手常犯的错误是输入gdb后立刻输入next，然后报错。必须通过run命令才能真正启动程序。

简单来说，断点的底层机制是：GDB在目标地址替换了一条trap指令，当CPU执行到这条指令时，控制权会交还给GDB。step和next的区别在于，step会进入函数调用内部，而next会把整个函数调用当作一条语句执行完。

1. break: 在main函数的第一行设置断点。
2. run: 启动程序，程序会在main函数的第一行停下来。
3. next: 执行下一行代码，如果这一行有函数调用，整个函数会被当作一条语句执行完。
4. step: 执行下一行代码，如果这一行有函数调用，会进入函数内部。
5. print a: 打印变量
6. info locals: 显示当前函数的所有局部变量。
7. continue: 继续执行程序，直到下一个断点或者程序结束。
8. quit: 退出GDB。


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

-->

---
layout: terminal-split
env: gdb-basics
---

# Backtrace: Understanding Crashes

When a program crashes (e.g., Segfault), `backtrace` shows the call chain that led to the crash.

```bash
# Example: Segmentation Fault
gdb ./segfault
```

<div class="text-sm mt-2">

**Reading the backtrace:**

- `#0` — where the crash happened (`strcpy`)
- `#1` — who called it (`copy_data`)
- `#2` — who called *that* (`process` — `buffer` is `NULL` here!)
- `#3` — The `main`

Use `frame N` to switch context and inspect local variables at each level.

</div>

<!--
当程序崩溃的时候，比如出现Segmentation Fault，最重要的事情就是知道它是怎么崩溃的——调用链是什么样的。

backtrace命令（简写bt）会打印出整个调用栈。它从当前的指令指针一直回溯到main函数，展示了完整的函数调用序列。你可以用frame N命令切换到任意一层栈帧，然后用info locals或print来检查那一层的局部变量。


```bash
(gdb) run
# Program receives SIGSEGV...
(gdb) backtrace
(gdb) frame 2
(gdb) info locals /  print buffer
```

在这个例子中，我们可以看到segfault.c中忘记了malloc，buffer是NULL，然后传给strcpy导致了崩溃


-->

---
layout: section
---

## 5. GDB: The "Fancy" Operations

Once you have the basics, GDB provides tools that `printf` debugging simply cannot match.

<!--
掌握了基础操作之后，你或许会说这些操作使用起来很麻烦，为什么不直接在代码里加几个printf就好了？其实

GDB其实远比这要强大，其中的一些非常强大的工具，是printf调试法无论如何都做不到的。
-->

---
layout: terminal-split
env: gdb-basics
---

# TUI: Visual Debugging

GDB has a built-in terminal UI — no IDE needed.

```bash
# Try TUI
gdb ./lifecycle
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

当然在这之前，我们刚刚的调试或许显得过于"原始"了，记不住代码行号以及执行到那里了

不过。GDB虽然是一个命令行工具，但，GDB内置了一个TUI（Text User Interface）模式，输入layout src之后，屏幕会分成两部分，上面显示源代码并高亮当前执行的行，下面是GDB命令行。

每次你按next或step的时候，可以看到高亮的行在移动，这比盲目地输入命令要直观得多。如果程序的输出把TUI界面搞乱了，按Ctrl+L可以重新绘制。


```
(gdb) break multiply
(gdb) run
(gdb) layout src
(gdb) next
(gdb) next
(gdb) step
```

-->

---
layout: terminal-split
env: gdb-basics
---

# Hardware Watchpoints

*"Something is modifying my variable, but I don't know where."*

A watchpoint uses the CPU's **hardware debug registers** to halt execution at the exact instruction that modifies a variable.

```bash
# Try Watchpoint
gdb ./watchme
```


<div class="text-sm mt-2">

- `watch var` — pause when `var` is **written**
- `rwatch var` — pause when `var` is **read**
- `awatch var` — pause on **any** access

</div>

<!--
Watchpoint解决的问题是："我的变量被莫名其妙地修改了，但我不知道是哪段代码干的。"

Watchpoint利用了CPU的硬件调试寄存器，它会在指定的内存地址被写入时精确地暂停执行。与断点不同的是，你不需要知道bug在哪一行，只需要告诉GDB你想监视哪个变量。

比如对于程序watchme.c，你发现counter这个变量被修改成了一个错误的值，但你不知道是哪里修改的。你可以在GDB里设置watch counter，这样每次counter被修改时程序都会暂停，然后你就可以检查当前的调用栈，看看是谁修改了counter。


1. 首先在main函数设置断点，
2. 运行程序。
3. 然后设置watch counter，这样每次counter被修改时程序都会暂停
4. 持续按continue，直到counter突然变成-1，
5. 这时候检查backtrace，你就会发现是corrupt函数修改了counter。


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
# Try Conditional Breakpoint
gdb ./conditional
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


比如对于程序 `conditional.c`，我们知道fill_array函数的第42次迭代时发生了错误，我们可以直接在第19行设置一个条件断点，条件是i==42，这样GDB就会在第42次迭代时停下来，让我们检查i和arr[i]的值，看看发生了什么。


1. 首先在fill_array函数的第一行设置断点，
2. 运行程序。
3. 然后在第17行设置条件断点，条件是i==42
4. 继续运行程序，GDB会在第42次迭代时停下来。
5. 这时候你可以检查i和arr[i]的值，看看发生了什么。

```
(gdb) break fill_array
(gdb) run
(gdb) break 17 if i == 42
(gdb) continue
(gdb) print i
(gdb) print arr[i]
```


在这个例子中，conditional.c在第42次迭代时注入了一个错误值，我们用 break 17 if i == 42 直接跳到第42次迭代。


-->

---
layout: terminal-split
env: gdb-basics
---

# Reverse Debugging

*Stepped over a function but the bug was inside it. No need to restart.*

```bash
# Try Reverse Debugging
gdb ./watchme
```

<div class="text-sm mt-2">

| Command | Effect |
|---------|--------|
| `target record-full` | Start recording |
| `reverse-step` | Step backward one line |
| `reverse-next`| Step back over a call |
| `reverse-continue` | Run back to prev breakpoint |

</div>

<!--
一个特别有趣且强大的操作——时间回溯调试。

传统调试中，一旦你step over了一个函数然后发现bug在那个函数里面，就只能重启程序重跑。但GDB的record-full模式可以记录程序执行过程中的所有状态变化（寄存器和内存修改），然后允许你反向执行。


对于watchme.c这个程序，我们在之前的例子中发现counter被corrupt函数修改了，但我们是通过watchpoint来监视counter的修改的。现在我们可以用reverse-continue来直接反向运行程序，直到碰到上一个断点，这样就能直接跳回到corrupt函数被调用的地方，查看当时的调用栈和变量状态，而不需要重启程序。

1. 首先在main函数设置断点，
2. 运行程序。
3. 跳过printf
4. 然后启动record-full来记录程序的执行过程。
5. 继续运行程序，直到counter被修改。
6. 这时候设置一个断点在corrupt函数，然后用reverse-continue来反向运行程序，直到碰到corrupt函数的断点
7. 这时候你就可以检查当时的调用栈和变量状态了。


```
(gdb) break main
(gdb) run
(gdb) next
(gdb) target record-full
(gdb) next
(gdb) break corrupt
(gdb) reverse-continue
(gdb) backtrace
(gdb) p counters
```

reverse-continue会让GDB反向运行，直到碰到上一个断点。reverse-step和reverse-next则是逐行反向执行。这个功能可以有效打破大家"GDB难用且落后"的刻板印象——哪个IDE能让你倒着运行程序？
-->

---
layout: terminal-split
env: gdb-basics
---

# Memory Inspection

In *ICS*, you deal with pointers and raw memory. The `x` command reads memory directly.

```bash
gdb ./memory
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



1. x/4xw &nums 的意思是：从nums的地址开始，以十六进制(x)格式，每个word(w)大小（4字节），显示4个单元。你会看到0xDEADBEEF、0xCAFEBABE这些我们在memory.c中设置的magic number。
2. x/12cb msg 则是以字符(c)格式，每个byte(b)大小，显示12个单元，你会看到"Hello, GDB!"的每个字符。
3. x/5i main 则是以指令(i)格式显示main函数开头的5条机器指令。

```
(gdb) break main
(gdb) run
(gdb) next 3
(gdb) x/4xw &nums
(gdb) x/12cb msg
(gdb) x/5i main
```

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

