#!/bin/bash
set -e
export PATH=$PATH:/usr/bin
export DISPLAY=:0
export XDG_RUNTIME_DIR=/run/user/$(id -u)

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
source "$SCRIPT_DIR/.venv/bin/activate"
python3 "$SCRIPT_DIR/src/main.py"
