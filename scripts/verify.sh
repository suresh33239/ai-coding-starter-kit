#!/usr/bin/env sh
# POSIX wrapper for the one Python verifier.
set -eu
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if command -v python3 >/dev/null 2>&1; then
  exec python3 "$script_dir/verify.py" "$@"
fi

if command -v python >/dev/null 2>&1; then
  exec python "$script_dir/verify.py" "$@"
fi

printf '%s\n' 'Python 3.11+ not found. Verification did not run.' >&2
exit 127
