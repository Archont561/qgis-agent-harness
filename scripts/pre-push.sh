#!/bin/sh
# Pre-push gate: the suite CI applies, so a push is never greener than the pull request.
# Prefers the pinned pixi environment; runs pytest on the ambient interpreter when pixi is
# absent; refuses the push with the remedy when neither is available.
set -eu

root=$(git rev-parse --show-toplevel)
cd "$root"

if command -v pixi >/dev/null 2>&1; then
  exec pixi run test
fi

if python3 -c 'import pytest, typer, yaml' >/dev/null 2>&1; then
  echo "pre-push: no pixi here, running the suite on the ambient interpreter" >&2
  python3 -m pytest scripts/tests || exit 1
  exec python3 -m pytest experiment
fi

echo "pre-push: neither pixi nor an interpreter carrying pytest was found" >&2
echo "pre-push: restore the environments (bash scripts/restore.sh) and push again" >&2
exit 1
