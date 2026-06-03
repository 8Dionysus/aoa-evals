#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from pathlib import Path

import validation_lanes

REPO_ROOT = Path(__file__).resolve().parents[1]
# Release lane still includes the generated report index check:
# `python scripts/generate_eval_report_index.py --check`.


def _command_label(command: tuple[str, ...]) -> str:
    if len(command) >= 2 and command[1].endswith(".py"):
        return Path(command[1]).stem.replace("_", " ")
    if "-m" in command and "pytest" in command:
        return "run tests"
    return " ".join(command)


def run_step(label: str, command: tuple[str, ...]) -> int:
    runtime_command = validation_lanes.command_for_runtime(command)
    print(f"[run] {label}: {subprocess.list2cmdline(runtime_command)}", flush=True)
    completed = subprocess.run(runtime_command, cwd=REPO_ROOT, env=None, check=False)
    if completed.returncode != 0:
        print(f"[error] {label} failed with exit code {completed.returncode}", flush=True)
        return completed.returncode
    print(f"[ok] {label}", flush=True)
    return 0


def main() -> int:
    for command in validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE:
        label = _command_label(command)
        exit_code = run_step(label, command)
        if exit_code != 0:
            return exit_code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
