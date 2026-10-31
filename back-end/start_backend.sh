#!/usr/bin/env bash
# start_backend.sh - Inicia el backend AWEN
# Uso: ./start_backend.sh

set -euo pipefail

cd "$(dirname "$0")"
exec python -m uvicorn app.main:app --port 8000