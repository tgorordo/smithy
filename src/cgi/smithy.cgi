#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [[ "$QUERY_STRING" == "source" ]]; then
  
    echo "Content-Type: text/plain"
    echo
    echo "<pre>"
    sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g' "$0"
    echo "</pre>"
    exit 0
fi

exec "$SCRIPT_DIR/../../.venv/bin/python" "$SCRIPT_DIR/script.py"
