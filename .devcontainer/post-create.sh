#!/usr/bin/env bash
# Install the environments the gate needs, and only those: `experiment` carries QGIS and three gigabytes,
# so it is pulled on demand by the task that needs it rather than on every container.
set -euo pipefail

if [[ ! -f pixi.toml ]]; then
  echo "no pixi.toml yet: the environments arrive with the first code commit" >&2
  exit 0
fi

pixi install -e qa
pixi install -e test
