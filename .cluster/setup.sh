#!/usr/bin/env bash
# Provision the sweep host: the box that serves the model and runs the harness.
#
# Sent over ssh and run with `bash -s`, so it needs nothing on the host but bash, and the version
# that runs is always the one in the repository. Modes:
#
#   --probe   report what the host has and what would be chosen; change nothing
#   --plan    print the steps, resolved against the probe; change nothing
#   --check   is the host provisioned as `host.env` demands?
#   (default) provision
#
# Exit codes from --check: 0 ready · 10 nothing provisioned · 11 provisioned but drifted ·
# 12 a sweep is running (never reconfigure under one) · 13 the host lacks something this script
# will not install for it.
#
# Re-running provision is safe: every step is guarded, and the heavy ones (pixi, weights) are
# cached by the tools themselves.

set -euo pipefail

# ───────────────────────────────────────────────────────────── configuration ────
# What the host must look like, and nothing about the host itself. Every value is a *default*: the
# environment wins, so the workflow — or `environment="…"` in the host's authorized_keys, for values
# that must not live in git — overrides one without editing this file.
#
# It is inline rather than in a second file because the script travels over ssh as stdin (`bash -s`),
# where `${BASH_SOURCE[0]}` is unset and a sibling file cannot be found.

# Bumped whenever a field below changes meaning, so an old marker reads as drift and not as truth.
schema=${schema:-1}

# Where the project is checked out on the host, and where the host keeps its own state (the
# provision marker, the venv, the logs). Both under $HOME: the sweep runs as an unprivileged user.
HOST_DIR=${HOST_DIR:-$HOME/research}
SWEEP_HOME=${SWEEP_HOME:-$HOME/.config/qgis-agent-harness}

# Cloned once, fetched afterwards. Public read-only: the host never needs write access to the repo.
REPO_URL=${REPO_URL:-https://github.com/Archont561/qgis-agent-harness.git}

# The pixi the lock was solved with. `relock.yml` pins v0.81.0; another one on the host is drift.
PIXI_VERSION=${PIXI_VERSION:-0.81.0}
# The environment that carries QGIS and the harness wheel — `ci.yml`'s `test` env cannot run a sweep.
EXPERIMENT_ENV=${EXPERIMENT_ENV:-experiment}

# `auto` picks vLLM when the probe finds a CUDA GPU at or above MIN_VRAM_MIB, and Ollama otherwise.
# `thesis/design/harness.md` §8 wants vLLM for the series and keeps Ollama as the development mirror:
# it serialises per model and has no tensor parallelism, which is fine for a smoke test and painful
# for a thousand runs.
ENGINE=${ENGINE:-auto}
ENGINE_VERSION=${ENGINE_VERSION:-}
MIN_VRAM_MIB=${MIN_VRAM_MIB:-20000}

# Pinned, because `run_id` is derived from `model_digest` (runs.md): an unpinned model is a sweep
# whose rows cannot be compared. An empty MODEL_ID provisions the box but leaves it unfit to measure.
MODEL_ID=${MODEL_ID:-}
MODEL_REVISION=${MODEL_REVISION:-}
QUANTIZATION=${QUANTIZATION:-}

# Concurrent shard workers; 0 means let the probe decide from VRAM. The pilot (phase 2) replaces the
# guess with the measured tokens/turn and wall time.
WORKERS=${WORKERS:-0}

# Loopback only. A model server bound to 0.0.0.0 on a publicly reachable box is an open inference
# proxy; the workflow reaches this one through the ssh tunnel.
ENGINE_HOST=${ENGINE_HOST:-127.0.0.1}
ENGINE_PORT=${ENGINE_PORT:-8000}

# ──────────────────────────────────────────────────────────────────── runtime ────
MODE=provision
SHA=
ALLOW_CPU=0

MARKER=$SWEEP_HOME/provisioned.env
LOCK=$HOST_DIR/runs/.sweep

usage() {
	cat <<'USAGE'
usage: setup.sh [--probe|--plan|--check|provision] [--sha <commit>] [--allow-cpu]

  --probe          print host facts and the engine they imply, as key=value lines
  --plan           print the steps provision would take, resolved against the probe
  --check          compare the host against host.env; exit 0/10/11/12/13
  provision        the default: pixi, the checkout, the environment, the engine, the weights
  --sha <commit>   the commit the host must run; a sweep always runs a named commit, never a branch
  --allow-cpu      provision without a GPU, for plumbing only: no measurement may run there
USAGE
}

while [ $# -gt 0 ]; do
	case "$1" in
	--probe | --plan | --check | provision)
		MODE=${1#--}
		shift
		;;
	--sha)
		SHA=${2:?--sha needs a commit}
		shift 2
		;;
	--allow-cpu)
		ALLOW_CPU=1
		shift
		;;
	-h | --help)
		usage
		exit 0
		;;
	*)
		printf 'setup.sh: unknown argument: %s\n' "$1" >&2
		usage >&2
		exit 64
		;;
	esac
done

die() {
	code=$1
	shift
	printf 'setup.sh: %s\n' "$*" >&2
	exit "$code"
}

step() { printf '  %s\n' "$*"; }

run_step() {
	printf '\n== %s\n' "$1"
	shift
	"$@"
}

# ───────────────────────────────────────────────────────────── what the host has ────
probe() {
	CORES=$(nproc 2>/dev/null || echo 1)
	MEM_MIB=$(awk '/MemTotal/ {printf "%d", $2 / 1024}' /proc/meminfo)
	DISK_MIB=$(df -Pm "$HOME" 2>/dev/null | awk 'NR==2 {print $4}')
	GPU_NAME=none
	VRAM_MIB=0
	if command -v nvidia-smi >/dev/null 2>&1; then
		GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -1)
		VRAM_MIB=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1)
	fi
	# A stubbed or driverless nvidia-smi prints nothing useful; empty and non-numeric mean no GPU.
	case "${GPU_NAME:-}" in '') GPU_NAME=none ;; esac
	case "${VRAM_MIB:-}" in '' | *[!0-9]*) VRAM_MIB=0 ;; esac
	case "${DISK_MIB:-}" in '' | *[!0-9]*) DISK_MIB=0 ;; esac
	HOST_OS=$(uname -s)
	HOST_ARCH=$(uname -m)
}

# The one decision the design leaves to the machine: vLLM wants a real GPU, Ollama tolerates none.
choose() {
	if [ "$ENGINE" = auto ]; then
		if [ "$VRAM_MIB" -ge "$MIN_VRAM_MIB" ]; then
			ENGINE=vllm
		else
			ENGINE=ollama
		fi
	fi
	if [ "$VRAM_MIB" -eq 0 ]; then
		CPU_ONLY=1
	else
		CPU_ONLY=0
	fi
	if [ "$WORKERS" = 0 ]; then
		# One shard per 12 GB of VRAM, never more than four; the pilot measures the real ratio.
		WORKERS=$((VRAM_MIB / 12288))
		if [ "$WORKERS" -gt 4 ]; then WORKERS=4; fi
		if [ "$WORKERS" -lt 1 ]; then WORKERS=1; fi
	fi
}

emit_probe() {
	printf '%s\n' \
		"host_os=$HOST_OS" \
		"host_arch=$HOST_ARCH" \
		"cores=$CORES" \
		"memory_mib=$MEM_MIB" \
		"disk_free_mib=$DISK_MIB" \
		"gpu=$GPU_NAME" \
		"vram_mib=$VRAM_MIB" \
		"engine=$ENGINE" \
		"engine_version=${ENGINE_VERSION:-unpinned}" \
		"model=${MODEL_ID:-unset}" \
		"quantization=${QUANTIZATION:-default}" \
		"workers=$WORKERS" \
		"cpu_only=$CPU_ONLY"
}

# ──────────────────────────────────────────────────────── what host.env demands ────
wants() {
	printf '%s\n' \
		"schema=$schema" \
		"host_dir=$HOST_DIR" \
		"pixi_version=$PIXI_VERSION" \
		"experiment_env=$EXPERIMENT_ENV" \
		"engine=$ENGINE" \
		"engine_version=$ENGINE_VERSION" \
		"model=$MODEL_ID" \
		"model_revision=$MODEL_REVISION" \
		"quantization=$QUANTIZATION" \
		"engine_host=$ENGINE_HOST" \
		"engine_port=$ENGINE_PORT"
}

# ────────────────────────────────────────────────────────── is it provisioned ────
check() {
	# A live sweep owns the box: pulling weights or restarting the server under it loses runs.
	if [ -e "$LOCK" ]; then die 12 "a sweep is running ($LOCK exists); reconfigure when it is done"; fi
	if [ ! -f "$MARKER" ]; then die 10 "nothing provisioned at $MARKER"; fi

	# Compared before the marker is sourced, or `wants` would report what the host already has.
	desired=$(wants)
	got=$(
		# shellcheck disable=SC1090
		. "$MARKER"
		while IFS= read -r line; do
			key=${line%%=*}
			printf '%s=%s\n' "$key" "${!key-}"
		done <<<"$desired"
	)
	if [ "$got" != "$desired" ]; then
		diff <(printf '%s\n' "$got") <(printf '%s\n' "$desired") >&2 || true
		die 11 "the host drifted from host.env"
	fi
	if [ -n "$SHA" ]; then
		head_sha=$(git -C "$HOST_DIR" rev-parse HEAD 2>/dev/null || echo unknown)
		if [ "$head_sha" != "$SHA" ]; then die 11 "the checkout is at $head_sha, not $SHA"; fi
	fi
	printf 'ready: %s at %s, %s (%s)\n' \
		"$ENGINE" "$ENGINE_HOST:$ENGINE_PORT" "${MODEL_ID:-no model pinned}" "$MARKER"
}

# ─────────────────────────────────────────────────────────────────── the plan ────
plan() {
	printf 'provision %s/%s as %s\n' "$HOST_OS" "$HOST_ARCH" "$ENGINE"
	step "install pixi $PIXI_VERSION"
	step "check out $REPO_URL at ${SHA:-the default branch} in $HOST_DIR"
	step "pixi install --frozen -e $EXPERIMENT_ENV"
	step "pixi run -e $EXPERIMENT_ENV sync   # rebuild the harness wheel from experiment/src"
	step "assert headless QGIS imports (QT_QPA_PLATFORM=offscreen)"
	case "$ENGINE" in
	vllm)
		step "python -m venv $SWEEP_HOME/venv && pip install vllm${ENGINE_VERSION:+==$ENGINE_VERSION}"
		step "vllm serve ${MODEL_ID:-<MODEL_ID>} on $ENGINE_HOST:$ENGINE_PORT"
		;;
	ollama)
		step "install ollama${ENGINE_VERSION:+ $ENGINE_VERSION}"
		step "ollama serve on $ENGINE_HOST:$ENGINE_PORT"
		;;
	esac
	if [ -n "$MODEL_ID" ]; then
		step "pull $MODEL_ID${MODEL_REVISION:+ at $MODEL_REVISION}"
	else
		step "no MODEL_ID pinned: the box provisions but cannot measure"
	fi
	step "wait for $ENGINE_HOST:$ENGINE_PORT/v1/models"
	step "write $MARKER with $WORKERS worker(s)"
}

# ──────────────────────────────────────────────────────────────────── do it ─────
need() {
	if ! command -v "$1" >/dev/null 2>&1; then
		die 13 "$1 is missing; install it on the host (sudo apt-get install -y $1)"
	fi
}

wait_for_engine() {
	for _ in $(seq 1 60); do
		listing=$(curl -fsS "http://$ENGINE_HOST:$ENGINE_PORT/v1/models" 2>/dev/null || true)
		if [ -n "$listing" ] && { [ -z "$MODEL_ID" ] || printf '%s' "$listing" | grep -q "$MODEL_ID"; }; then
			return 0
		fi
		sleep 5
	done
	die 13 "no engine answered on $ENGINE_HOST:$ENGINE_PORT"
}

provision() {
	need git
	need curl
	if [ -e "$LOCK" ]; then die 12 "a sweep is running ($LOCK exists); reconfigure when it is done"; fi
	if [ "$CPU_ONLY" = 1 ] && [ "$ALLOW_CPU" = 0 ]; then
		die 13 "no GPU found; pass --allow-cpu to provision for plumbing only, never to measure"
	fi
	mkdir -p "$SWEEP_HOME/logs"
	export PATH="$HOME/.pixi/bin:$PATH"

	run_step "pixi $PIXI_VERSION" install_pixi
	run_step "checkout" checkout
	run_step "environment" environment
	run_step "headless QGIS" headless_gis
	run_step "engine" install_engine
	run_step "weights" pull_weights
	run_step "health" wait_for_engine
	write_marker
	printf '\nprovisioned: %s\n' "$MARKER"
}

install_pixi() {
	if command -v pixi >/dev/null 2>&1 && [ "$(pixi --version | awk '{print $2}')" = "$PIXI_VERSION" ]; then
		printf '  already %s\n' "$PIXI_VERSION"
		return
	fi
	curl -fsSL https://pixi.sh/install.sh | PIXI_VERSION="$PIXI_VERSION" bash
}

checkout() {
	if [ -d "$HOST_DIR/.git" ]; then
		git -C "$HOST_DIR" fetch --quiet origin
	else
		git clone --quiet "$REPO_URL" "$HOST_DIR"
	fi
	if [ -n "$SHA" ]; then
		git -C "$HOST_DIR" checkout --quiet "$SHA"
	else
		git -C "$HOST_DIR" checkout --quiet
	fi
	git -C "$HOST_DIR" rev-parse HEAD
}

environment() {
	# --frozen: a host that silently re-solved the lock is a host whose runs are not comparable.
	pixi install --frozen -e "$EXPERIMENT_ENV" --manifest-path "$HOST_DIR/pixi.toml"
	# The harness is a path dependency installed as a wheel; source edits stay invisible until rebuilt.
	pixi run -e "$EXPERIMENT_ENV" --manifest-path "$HOST_DIR/pixi.toml" sync
}

headless_gis() {
	QT_QPA_PLATFORM=offscreen pixi run -e "$EXPERIMENT_ENV" --manifest-path "$HOST_DIR/pixi.toml" \
		python -c "import qgis.core; print('qgis', qgis.core.Qgis.QGIS_VERSION)"
}

install_engine() {
	case "$ENGINE" in
	vllm)
		python3 -m venv "$SWEEP_HOME/venv"
		"$SWEEP_HOME/venv/bin/pip" install --quiet --upgrade pip
		if [ -n "$ENGINE_VERSION" ]; then
			"$SWEEP_HOME/venv/bin/pip" install --quiet "vllm==$ENGINE_VERSION"
		else
			"$SWEEP_HOME/venv/bin/pip" install --quiet vllm
		fi
		serve=(serve "$MODEL_ID" --host "$ENGINE_HOST" --port "$ENGINE_PORT")
		if [ -n "$MODEL_REVISION" ]; then serve+=(--revision "$MODEL_REVISION"); fi
		if [ -n "$QUANTIZATION" ]; then serve+=(--quantization "$QUANTIZATION"); fi
		nohup "$SWEEP_HOME/venv/bin/vllm" "${serve[@]}" >>"$SWEEP_HOME/logs/engine.log" 2>&1 &
		;;
	ollama)
		if ! command -v ollama >/dev/null 2>&1; then
			curl -fsSL https://ollama.com/install.sh | sh
		fi
		OLLAMA_HOST="$ENGINE_HOST:$ENGINE_PORT" nohup ollama serve \
			>>"$SWEEP_HOME/logs/engine.log" 2>&1 &
		;;
	*)
		die 13 "unknown ENGINE=$ENGINE"
		;;
	esac
}

pull_weights() {
	if [ -z "$MODEL_ID" ]; then
		printf '  skipped: no MODEL_ID configured, so the box cannot measure yet\n'
		return
	fi
	case "$ENGINE" in
	vllm) printf '  vLLM fetches %s on serve; --revision pins it\n' "$MODEL_ID" ;;
	ollama) ollama pull "$MODEL_ID" ;;
	esac
}

write_marker() {
	mkdir -p "$SWEEP_HOME"
	{
		printf '# Written by scripts/cluster/setup.sh and compared by --check. Do not edit on the host.\n'
		printf 'provisioned_at=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
		printf 'sha=%s\n' "$(git -C "$HOST_DIR" rev-parse HEAD 2>/dev/null || echo unknown)"
		printf 'workers=%s\n' "$WORKERS"
		printf 'cpu_only=%s\n' "$CPU_ONLY"
		wants
	} >"$MARKER"
	cat "$MARKER"
}

probe
choose

case "$MODE" in
probe) emit_probe ;;
plan) plan ;;
check) check ;;
provision) provision ;;
esac
