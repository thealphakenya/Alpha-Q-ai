#!/usr/bin/env bash
set -Eeuo pipefail

cache_dir="${PIP_CACHE_DIR:-${HOME}/.cache/pip}"
mkdir -p -- "$cache_dir"

if ! command -v python3 >/dev/null 2>&1; then
  printf '%s\n' "Python 3 is required by the configured devcontainer image." >&2
  exit 1
fi

printf 'Low-bandwidth setup prepared; Python: '
python3 --version
printf 'Pip cache directory: %s\n' "$cache_dir"
printf '%s\n' "No dependencies, extensions, Android SDK, Ollama runtime, or models were installed."
