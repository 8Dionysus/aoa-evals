#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _env() -> dict[str, str]:
    env = os.environ.copy()
    deps = {
        "AOA_TECHNIQUES_ROOT": "aoa-techniques",
        "AOA_SKILLS_ROOT": "aoa-skills",
        "AOA_AGENTS_ROOT": "aoa-agents",
        "AOA_PLAYBOOKS_ROOT": "aoa-playbooks",
        "AOA_MEMO_ROOT": "aoa-memo",
        "ABYSS_STACK_ROOT": "abyss-stack",
    }
    for env_var, repo_name in deps.items():
        candidates = [
            env.get(env_var),
            str((REPO_ROOT / ".deps" / repo_name).resolve()),
            str((REPO_ROOT.parent / repo_name).resolve()),
        ]
        for candidate in candidates:
            if candidate and Path(candidate).exists():
                env[env_var] = str(Path(candidate).resolve())
                break
    return env


COMMANDS = [
    ("check generated catalog", [sys.executable, "scripts/build_catalog.py", "--check"]),
    ("validate repo", [sys.executable, "scripts/validate_repo.py"]),
    ("run tests", [sys.executable, "-m", "pytest", "-q"]),
]


def run_step(label: str, command: list[str]) -> int:
    print(f"[run] {label}: {subprocess.list2cmdline(command)}", flush=True)
    completed = subprocess.run(command, cwd=REPO_ROOT, env=_env(), check=False)
    if completed.returncode != 0:
        print(f"[error] {label} failed with exit code {completed.returncode}", flush=True)
        return completed.returncode
    print(f"[ok] {label}", flush=True)
    return 0


def main() -> int:
    for label, command in COMMANDS:
        exit_code = run_step(label, command)
        if exit_code != 0:
            return exit_code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
