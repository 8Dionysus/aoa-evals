"""Validation topology documentation contract checks."""

from __future__ import annotations

from pathlib import Path

from validators.validation_topology_common import (
    COMMAND_AUTHORITY_PATH,
    VALIDATOR_TOPOLOGY_PATH,
    _require_tokens,
)


def validate_validation_topology_docs(repo_root: Path) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []
    issues.extend(
        _require_tokens(
            repo_root,
            VALIDATOR_TOPOLOGY_PATH,
            (
                "source-fast",
                "generated",
                "trace/eval",
                "Memory/context validators",
                "Security/adversarial validators",
            ),
        )
    )
    issues.extend(
        _require_tokens(
            repo_root,
            COMMAND_AUTHORITY_PATH,
            (
                "docs/validation/validation_lanes.json",
                "`config/` is currently a route-card-only",
                "Promotion Rule",
            ),
        )
    )
    return issues


__all__ = ("validate_validation_topology_docs",)
