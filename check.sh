#!/bin/sh
# Local equivalent of the CI.
# Usage: ./check.sh [style | hello_friends | timer | war]
set -e
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
    python3 -m venv .venv
    .venv/bin/pip install -q -r requirements.txt
fi
PATH="$PWD/.venv/bin:$PATH"

if [ -n "$1" ]; then
    pytest "tests/$1" -v
else
    pytest
fi
