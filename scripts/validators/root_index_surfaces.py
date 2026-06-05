"""Root index surface role contracts."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue
from validators.root_common import require_tokens


EVAL_INDEX_NAME = "EVAL_INDEX.md"
MECHANICS_README_NAME = "mechanics/README.md"
INDEX_SURFACE_ROLE_REQUIRED_TOKENS: dict[str, tuple[str, ...]] = {
    EVAL_INDEX_NAME: (
        "# Eval Bundle Index",
        "repository-wide agent-facing index of public eval bundles",
        "bundle-local",
    ),
    "docs/decisions/README.md": (
        "# Decision Records Index",
        "agent-facing index",
        "decision rationale",
        "docs/decisions/AGENTS.md#validation",
    ),
    MECHANICS_README_NAME: (
        "# Mechanics Operation Atlas",
        "operation atlas",
        "Top-down route",
    ),
}


def validate_index_surface_roles(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path_name, tokens in INDEX_SURFACE_ROLE_REQUIRED_TOKENS.items():
        require_tokens(repo_root, path_name, tokens, issues)

    return issues


__all__ = (
    "EVAL_INDEX_NAME",
    "INDEX_SURFACE_ROLE_REQUIRED_TOKENS",
    "MECHANICS_README_NAME",
    "validate_index_surface_roles",
)
