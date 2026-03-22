/*
 * watchme.c — Watchpoint demo
 *
 * Bug: counter is unexpectedly modified by corrupt().
 * Use `watch counter` to find exactly where it changes.
 *
 * Compile: gcc -g watchme.c -o watchme
 * Usage:   gdb ./watchme → b main → r → watch counter → c
 */

#include <stdio.h>

int counter = 0;

void increment(void) {
    counter++;
}

void corrupt(void) {
    /* Bug: accidentally resets counter */
    counter = -1;
}

void do_work(void) {
    for (int i = 0; i < 5; i++) {
        increment();
        if (i == 3) {
            corrupt();  /* The culprit */
        }
    }
}

int main(void) {
    printf("Initial counter: %d\n", counter);
    do_work();
    printf("Final counter: %d\n", counter);

    if (counter != 5) {
        printf("ERROR: expected 5, got %d\n", counter);
        return 1;
    }
    return 0;
}
