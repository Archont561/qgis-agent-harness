#!/usr/bin/env bash
# Render README.md from .readme/README.md.ejs — the README is generated, not edited by hand.
#
#   bash scripts/readme.sh           # write README.md from the template
#   bash scripts/readme.sh --check   # exit 1 when the committed README.md is not that render
#
# readme-md-generator asks before overwriting an existing README.md: `-y` answers its questions but
# not that prompt. So the file is moved aside rather than answered, and put back when the render
# fails, when it comes back empty, or when this is a check.
set -euo pipefail

cd "$(dirname "$0")/.."

template=.readme/README.md.ejs
generator=readme-md-generator@1.0.0
check=0
if [ "${1:-}" = "--check" ]; then
  check=1
fi

if [ ! -f "$template" ]; then
  echo "readme: $template is missing" >&2
  exit 1
fi

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
if [ -f README.md ]; then
  mv README.md "$tmp/previous.md"
fi

if ! bun x --bun "$generator" -p "$template" -y; then
  if [ -f "$tmp/previous.md" ]; then
    mv "$tmp/previous.md" README.md
  fi
  echo "readme: the render failed; README.md is unchanged" >&2
  exit 1
fi

if [ ! -s README.md ]; then
  if [ -f "$tmp/previous.md" ]; then
    mv "$tmp/previous.md" README.md
  fi
  echo "readme: the render came back empty; README.md is unchanged" >&2
  exit 1
fi

if [ "$check" = 0 ]; then
  exit 0
fi

if [ -f "$tmp/previous.md" ] && diff -q "$tmp/previous.md" README.md >/dev/null; then
  mv README.md "$tmp/rendered.md"
  mv "$tmp/previous.md" README.md
  echo "readme: README.md is the render of $template"
  exit 0
fi

if [ -f "$tmp/previous.md" ]; then
  diff -u "$tmp/previous.md" README.md || true
fi
mv README.md "$tmp/rendered.md"
if [ -f "$tmp/previous.md" ]; then
  mv "$tmp/previous.md" README.md
fi
echo "readme: README.md is not the render of $template — run pixi run readme" >&2
exit 1
