/*
 * segfault.c — Segmentation fault demo for backtrace
 *
 * Demonstrates: bt (backtrace), frame, inspecting crash context
 *
 * Compile: gcc -g segfault.c -o segfault
 * Usage:   gdb ./segfault → run → bt
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void copy_data(char *dst, const char *src) {
    /* Bug: dst is NULL, this will crash */
    strcpy(dst, src);
}

void process(const char *input) {
    char *buffer = NULL;  /* forgot to malloc! */
    copy_data(buffer, input);
    printf("Processed: %s\n", buffer);
}

int main(void) {
    printf("Starting...\n");
    process("hello world");
    printf("Done.\n");
    return 0;
}
