/*
 * memory.c — Memory inspection demo (x command)
 *
 * Demonstrates: x/Nfw, examining arrays, strings, pointers
 *
 * Compile: gcc -g memory.c -o memory
 * Usage:   gdb ./memory → b main → r → x/4xw &nums → x/12cb msg
 */

#include <stdio.h>

int main(void) {
    int nums[] = {0xDEADBEEF, 0xCAFEBABE, 0x12345678, 0x0};
    char msg[] = "Hello, GDB!";
    int *ptr = &nums[2];

    printf("nums[0] = 0x%X\n", nums[0]);
    printf("msg = %s\n", msg);
    printf("*ptr = 0x%X\n", *ptr);

    return 0;
}
