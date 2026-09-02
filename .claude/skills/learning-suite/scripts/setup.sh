#!/usr/bin/env bash
# One-time setup: python venv holding websocket-client for the CDP driver.
set -e
VENV="${LS_VENV:-$HOME/.cache/learningsuite/venv}"
[ -d "$VENV" ] || python3 -m venv "$VENV"
"$VENV/bin/pip" -q install websocket-client pyyaml
echo "venv ready: $VENV"
