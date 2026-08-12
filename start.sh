#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
echo "=== MIKROBOT PRO X ULTIMATE ==="
pkill -f "uvicorn.*8765" 2>/dev/null || true
pkill -f "python.*8765" 2>/dev/null || true
python3 -m pip install -q -r requirements.txt
echo "Servidor: http://0.0.0.0:8765"
exec python3 main.py
