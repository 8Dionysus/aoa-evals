#!/usr/bin/env python3
"""Run a named aoa-evals validation lane."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

import validation_lanes

REPO_ROOT = Path(__file__).resolve().parents[1]

MODE_TO_LANE = {
    "source-fast": "source_fast",
    "generated": "generated",
    "mechanics-part-local": "mechanics_part_local",
    "pinned-sibling": "pinned_sibling",
    "latest-sibling": "latest_sibling",
    "release": "release",
    "nightly": "nightly",
    "advisory": "advisory",
}


def expand_command_globs(command: tuple[str, ...]) -> tuple[str, ...]:
    expanded: list[str] = []
    for part in command:
        if not any(marker in part for marker in ("*", "?", "[")):
            expanded.append(part)
            continue
        path = Path(part)
        if path.is_absolute():
            matches = sorted(
                Path(match).as_posix() for match in path.parent.glob(path.name)
            )
        else:
            matches = sorted(
                match.relative_to(REPO_ROOT).as_posix() for match in REPO_ROOT.glob(part)
            )
        expanded.extend(matches or [part])
    return tuple(expanded)


def run_command(label: str, command: tuple[str, ...]) -> int:
    runtime_command = validation_lanes.command_for_runtime(command)
    expanded_command = expand_command_globs(runtime_command)
    print(f"[run] {label}: {subprocess.list2cmdline(expanded_command)}", flush=True)
    env = os.environ.copy()
    if label == "pinned-sibling":
        env["AOA_EVALS_STRICT_SIBLING_COMPAT"] = "1"
    completed = subprocess.run(expanded_command, cwd=REPO_ROOT, env=env, check=False)
    if completed.returncode != 0:
        print(f"[error] {label} failed with exit code {completed.returncode}", flush=True)
        return completed.returncode
    print(f"[ok] {label}", flush=True)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        required=True,
        choices=sorted(MODE_TO_LANE),
        help="validation lane to execute",
    )
    args = parser.parse_args(argv)

    lane_id = MODE_TO_LANE[args.mode]
    if lane_id == "advisory":
        print("[info] advisory boundaries:")
        for boundary in validation_lanes.ADVISORY_BOUNDARIES:
            print(f"- {boundary}")
        return 0

    for command in validation_lanes.command_sequence_for_lane(lane_id):
        exit_code = run_command(args.mode, command)
        if exit_code != 0:
            return exit_code
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
