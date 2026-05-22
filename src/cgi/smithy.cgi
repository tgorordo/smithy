#!/usr/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

exec "$SCRIPT_DIR/../smithy/.venv/bin/python" "$SCRIPT_DIR/../smithy/src/cgi/cgi.py"
