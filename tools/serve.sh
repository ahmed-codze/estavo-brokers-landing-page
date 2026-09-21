#!/bin/sh
# ============================================================
# Estavo v3 — local static server
#
# Pages reference assets root-relatively (/assets/...), which
# only resolves when the site is served from its root. Opening
# a subdirectory page as a file:// URL loads it unstyled.
#
# Usage:  sh tools/serve.sh [port]     (default 8731)
# ============================================================
set -e
cd "$(dirname "$0")/.."
PORT="${1:-8731}"
echo "serving $(pwd) at http://127.0.0.1:$PORT/"
exec python3 -m http.server "$PORT"
