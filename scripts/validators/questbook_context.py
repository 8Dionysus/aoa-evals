"""Questbook repo-root and sibling compatibility context."""

from __future__ import annotations

import os
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
STRICT_SIBLING_COMPAT_ENV = "AOA_EVALS_STRICT_SIBLING_COMPAT"


def repo_root_from_env(env_name: str, default: Path) -> Path:
    override = os.environ.get(env_name)
    if not override:
        return default
    return Path(override).expanduser().resolve()


AOA_AGENTS_ROOT = repo_root_from_env("AOA_AGENTS_ROOT", REPO_ROOT.parent / "aoa-agents")


__all__ = (
    "AOA_AGENTS_ROOT",
    "REPO_ROOT",
    "STRICT_SIBLING_COMPAT_ENV",
    "repo_root_from_env",
)
