// 循环输出 Welcome to ICS Tutorial!，并且每次输出后等待0.5秒钟。
// 接受参数: name, 例如：./welcome Alice → 输出 Welcome to ICS Tutorial, Alice!

#include <stdio.h>
#include <unistd.h>
#include <stdint.h>

int main(int argc, char *argv[]) {
    uint32_t i = 1;

    if (argc > 1) {
        while (1) {
            printf("[%u] ", i++);
            printf("Welcome to ICS Tutorial, %s!\n", argv[1]);
            usleep(500000);  // Sleep for 0.5 seconds (500,000 microseconds)
        }
    } else {
        printf("Welcome to ICS Tutorial!\n");
    }

    return 0;
}