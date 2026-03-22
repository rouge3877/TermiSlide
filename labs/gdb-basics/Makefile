CC = gcc
CFLAGS = -g -Wall -Wextra -std=c11

TARGETS = lifecycle segfault watchme conditional memory

all: $(TARGETS)

%: %.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -f $(TARGETS)

.PHONY: all clean
