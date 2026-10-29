#!/usr/bin/env bash
# Verificación completa del proyecto AWEN (Linux / macOS / Git Bash)
# Uso: bash scripts/verify.sh

set -uo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
failed=0

step() {
    local name="$1"
    local dir="$2"
    shift 2

    echo
    echo "== $name =="
    ( cd "$dir" && "$@" )
    local code=$?
    if [ "$code" -ne 0 ]; then
        echo "FALLO: $name (exit $code)"
        failed=1
    fi
}

if ! command -v python >/dev/null 2>&1; then
    echo "ERROR: python no esta instalado o no esta en PATH."
    exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
    echo "ERROR: npm no esta instalado o no esta en PATH."
    exit 1
fi

export AWEN_SECRET_KEY=test

step "Backend: pytest" "$root/back-end" python -m pytest tests -q

if [ ! -d "$root/front-end/node_modules" ]; then
    step "Frontend: npm ci" "$root/front-end" npm ci
fi

step "Frontend: lint"  "$root/front-end" npm run lint
step "Frontend: tests" "$root/front-end" npm test
step "Frontend: build" "$root/front-end" npm run build

echo
if [ "$failed" -ne 0 ]; then
    echo "VERIFICACION FALLIDA"
    exit 1
fi

echo "VERIFICACION OK"
