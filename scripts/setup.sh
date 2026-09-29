#!/usr/bin/env bash
# One-command environment setup for every teammate (Windows Git Bash, Linux, macOS).
# Usage: bash scripts/setup.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fail() {
    echo "ERROR: $*" >&2
    exit 1
}

# ---------------------------------------------------------------------------
# 1. Find a Python 3.11 interpreter
# ---------------------------------------------------------------------------
PY=""
for candidate in python3.11 python python3 "py -3.11"; do
    if "$candidate" -c 'import sys; sys.exit(0 if sys.version_info[:2] == (3, 11) else 1)' >/dev/null 2>&1; then
        PY="$candidate"
        break
    fi
done
[ -n "$PY" ] || fail "Python 3.11 is required but was not found. \
Install it from https://www.python.org/downloads/ (or pyenv) and re-run."

echo "==> Using interpreter: $PY ($("$PY" --version))"

# ---------------------------------------------------------------------------
# 2. Create the virtual environment (.venv)
# ---------------------------------------------------------------------------
if [ -f ".venv/Scripts/python.exe" ]; then
    VENV_PY=".venv/Scripts/python.exe"   # Windows (Git Bash)
elif [ -f ".venv/bin/python" ]; then
    VENV_PY=".venv/bin/python"           # Linux / macOS
else
    echo "==> Creating virtual environment in .venv/"
    "$PY" -m venv .venv
    if [ -f ".venv/Scripts/python.exe" ]; then
        VENV_PY=".venv/Scripts/python.exe"
    elif [ -f ".venv/bin/python" ]; then
        VENV_PY=".venv/bin/python"
    else
        fail "Could not locate the python executable inside .venv/"
    fi
fi

# ---------------------------------------------------------------------------
# 3. Install the pinned dependencies
# ---------------------------------------------------------------------------
echo "==> Installing requirements.txt (pinned versions)"
"$VENV_PY" -m pip install --quiet --upgrade pip
"$VENV_PY" -m pip install --quiet -r requirements.txt

# ---------------------------------------------------------------------------
# 4. Local configuration file (.env, never committed)
# ---------------------------------------------------------------------------
if [ ! -f ".env" ]; then
    echo "==> Creating .env from .env.example"
    cp .env.example .env
else
    echo "==> Keeping existing .env"
fi

# ---------------------------------------------------------------------------
# 5. Verify the environment
# ---------------------------------------------------------------------------
echo "==> Running scripts/check_env.py"
"$VENV_PY" scripts/check_env.py

echo ""
echo "Setup complete. Activate the venv with:"
echo "  Git Bash / Linux / macOS : source .venv/Scripts/activate | source .venv/bin/activate"
echo "Next commands: make check && make test && make lint"
