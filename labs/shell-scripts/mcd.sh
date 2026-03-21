#!/bin/bash
# example: mcd function
mcd () {
    mkdir -p "$1"
    cd "$1"
}
echo "Usage: mcd <dirname>"
