/*
 * lifecycle.c — GDB basic lifecycle demo
 *
 * Demonstrates: breakpoints, run, step, next, print, backtrace
 *
 * Compile: gcc -g lifecycle.c -o lifecycle
 * Usage:   gdb ./lifecycle
 */

#include <stdio.h>

int add(int a, int b) {
    int result = a + b;
    return result;
}

int multiply(int x, int y) {
    int product = 0;
    for (int i = 0; i < y; i++) {
        product = add(product, x);
    }
    return product;
}

int main(void) {
    int a = 3, b = 4;

    printf("add(%d, %d) = %d\n", a, b, add(a, b));

    int m = multiply(a, b);
    printf("multiply(%d, %d) = %d\n", a, b, m);

    return 0;
}
