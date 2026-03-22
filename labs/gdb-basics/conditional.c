/*
 * conditional.c — Conditional breakpoint demo
 *
 * Bug: array corruption occurs only at iteration i == 42.
 * Use `break 24 if i == 42` to catch it without stepping 42 times.
 *
 * Compile: gcc -g conditional.c -o conditional
 * Usage:   gdb ./conditional → break 24 if i == 42 → r
 */

#include <stdio.h>

#define SIZE 100

void fill_array(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        if (i == 42) {
            arr[i] = -999;  /* Bug: wrong value injected */
        } else {
            arr[i] = i * 2;
        }
    }
}

int sum_array(const int arr[], int n) {
    int total = 0;
    for (int i = 0; i < n; i++) {
        total += arr[i];
    }
    return total;
}

int main(void) {
    int data[SIZE];
    fill_array(data, SIZE);

    int total = sum_array(data, SIZE);
    int expected = SIZE * (SIZE - 1);  /* sum of 0,2,4,...,198 */

    printf("Sum = %d (expected %d)\n", total, expected);
    if (total != expected) {
        printf("ERROR: mismatch! Something corrupted the array.\n");
        return 1;
    }
    return 0;
}
