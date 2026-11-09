"""The promises of `.cluster/setup.sh` as scenarios, which is how this repository states behaviour.

Each step runs the script the way the workflow does — `bash <script> <mode>`, in a throwaway home
whose `nvidia-smi` is a stub — so a scenario describes the host rather than the script's internals.
The stubs are the point: a test that needed a real GPU would never run in CI, and the decisions
under test are the ones made *from* the probe, not the installs that follow it.
"""

from __future__ import annotations

import os
import pathlib
import subprocess

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

REPO = pathlib.Path(__file__).resolve().parents[2]
SETUP = REPO / ".cluster" / "setup.sh"


class Result:
    """What one run left behind: its exit status and both of its streams."""

    def __init__(self, completed: subprocess.CompletedProcess[str]) -> None:
        self.code = completed.returncode
        self.out = completed.stdout
        self.err = completed.stderr

    def fact(self, key: str) -> str:
        for line in self.out.splitlines():
            if line.startswith(f"{key}="):
                return line.split("=", 1)[1]
        raise AssertionError(f"{key} missing in:\n{self.out}")


class Host:
    """A stand-in for the sweep host: a home directory, a PATH of stubs, and a GPU if given one.

    The `given` steps configure one instance rather than returning new ones, because a step's return
    value becomes a fixture named after the step function — not the `host` the later steps ask for.
    """

    def __init__(self, root: pathlib.Path) -> None:
        self.root = root
        self.home = root / "home"
        self.home.mkdir(parents=True, exist_ok=True)
        self.bin = root / "bin"
        self.bin.mkdir(parents=True, exist_ok=True)
        for name in ("git", "curl"):
            stub = self.bin / name
            stub.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            stub.chmod(0o755)
        self.env = {
            "PATH": f"{self.bin}:{os.environ['PATH']}",
            "HOME": str(self.home),
            "HOST_DIR": str(self.home / "research"),
            "SWEEP_HOME": str(self.home / "state"),
        }
        self.result: Result | None = None

    def add_gpu(self, vram_mib: int) -> None:
        # `--query-gpu=name` prints a label; `--query-gpu=memory.total` prints the bare number.
        gpu = self.bin / "nvidia-smi"
        gpu.write_text(
            f'#!/bin/sh\ncase "$*" in\n*name*) echo "Stub GPU {vram_mib}MiB" ;;\n'
            f"*) echo {vram_mib} ;;\nesac\n",
            encoding="utf-8",
        )
        gpu.chmod(0o755)

    def marker(self, pixi_version: str = "0.81.0") -> None:
        """Leave the marker provision would have left, as an already-provisioned host has it."""
        path = pathlib.Path(self.env["SWEEP_HOME"]) / "provisioned.env"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "\n".join(
                [
                    "schema=1",
                    f"host_dir={self.env['HOST_DIR']}",
                    f"pixi_version={pixi_version}",
                    "experiment_env=experiment",
                    "engine=ollama",  # no GPU on this host, so this is what provision chose
                    "engine_version=",
                    "model=",
                    "model_revision=",
                    "quantization=",
                    "engine_host=127.0.0.1",
                    "engine_port=8000",
                ]
            ),
            encoding="utf-8",
        )

    def start_sweep(self) -> None:
        lock = pathlib.Path(self.env["HOST_DIR"]) / "runs" / ".sweep"
        lock.mkdir(parents=True, exist_ok=True)
        (lock / "sweep-id").write_text("20260101T0000Z-abc1234\n", encoding="utf-8")

    def run(self, *args: str) -> Result:
        self.result = Result(
            subprocess.run(
                ["bash", str(SETUP), *args],
                env=self.env,
                capture_output=True,
                text=True,
                check=False,
            )
        )
        return self.result


@pytest.fixture(name="host")
def host_fixture(tmp_path: pathlib.Path) -> Host:
    return Host(tmp_path)


@given("a host with no NVIDIA driver")
def _host_without_a_gpu(host: Host) -> None:
    # The default: a host whose PATH has no nvidia-smi at all.
    assert host.result is None


@given(parsers.parse("a host with {vram:d} MiB of VRAM"))
def _host_with_vram(host: Host, vram: int) -> None:
    host.add_gpu(vram)


@given("a host that has never been provisioned")
def _host_never_provisioned(host: Host) -> None:
    assert not pathlib.Path(host.env["SWEEP_HOME"], "provisioned.env").exists()


@given(parsers.parse("a host provisioned with pixi {version}"))
def _host_provisioned_with(host: Host, version: str) -> None:
    host.marker(pixi_version=version)


@given("a host provisioned for the current configuration")
def _host_provisioned(host: Host) -> None:
    host.marker()


@given("a sweep is in progress on it")
def _sweep_in_progress(host: Host) -> None:
    host.start_sweep()


@when("the provisioner probes it")
def _probe(host: Host) -> None:
    host.run("--probe")


@when("the provisioner checks it")
def _check(host: Host) -> None:
    host.run("--check")


@when("the provisioner is asked to provision it")
def _provision(host: Host) -> None:
    host.run("provision")


@when("the provisioner plans for it")
def _plan(host: Host) -> None:
    host.run("--plan")


@then(parsers.parse("it reports {fact}"))
def _reports_fact(host: Host, fact: str) -> None:
    key, _, value = fact.partition("=")
    assert host.result is not None
    assert host.result.fact(key) == value


@then(parsers.parse("it offers the {engine} engine"))
def _offers_engine(host: Host, engine: str) -> None:
    assert host.result is not None
    assert host.result.fact("engine") == engine


@then(parsers.parse("it offers {workers:d} workers"))
def _offers_workers(host: Host, workers: int) -> None:
    assert host.result is not None
    assert host.result.fact("workers") == str(workers)


@then(parsers.parse("it exits with {code:d}"))
def _exits_with(host: Host, code: int) -> None:
    assert host.result is not None
    assert host.result.code == code


@then(parsers.parse("it says {message}"))
def _says(host: Host, message: str) -> None:
    assert host.result is not None
    assert message in host.result.err


@then("it names --allow-cpu as the way past it")
def _names_allow_cpu(host: Host) -> None:
    assert host.result is not None
    assert "--allow-cpu" in host.result.err


@then(parsers.parse('the plan includes "{text}"'))
def _plan_includes(host: Host, text: str) -> None:
    assert host.result is not None
    assert text in host.result.out


# Bound here, at the bottom: `scenarios()` looks up the steps that exist when it is called, so a
# call above the step definitions would bind nothing.
scenarios("../features/cluster-setup.feature")
