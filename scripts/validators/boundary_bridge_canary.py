"""Boundary-bridge sibling canary matrix shape."""

from __future__ import annotations

import json
from pathlib import Path

from validators.boundary_bridge_common import (
    SIBLING_CANARY_EXPECTED_REPOS,
    SIBLING_CANARY_MATRIX_NAME,
    ValidationIssue,
)


def validate_sibling_canary_matrix_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    matrix_path = repo_root / SIBLING_CANARY_MATRIX_NAME
    try:
        matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(SIBLING_CANARY_MATRIX_NAME, "file is missing"))
        return issues
    except json.JSONDecodeError as exc:
        issues.append(
            ValidationIssue(
                SIBLING_CANARY_MATRIX_NAME,
                f"invalid JSON: {exc}",
            )
        )
        return issues

    entries = matrix.get("entries") if isinstance(matrix, dict) else None
    if not isinstance(entries, list):
        issues.append(
            ValidationIssue(
                SIBLING_CANARY_MATRIX_NAME,
                "entries must be a list",
            )
        )
        return issues

    repos = {
        entry.get("repo")
        for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("repo"), str)
    }
    for repo_name in SIBLING_CANARY_EXPECTED_REPOS:
        if repo_name not in repos:
            issues.append(
                ValidationIssue(
                    SIBLING_CANARY_MATRIX_NAME,
                    f"missing sibling canary entry for {repo_name}",
                )
            )

    for entry in entries:
        if (
            isinstance(entry, dict)
            and entry.get("repo") == "abyss-stack"
            and entry.get("resolver") != "abyss-stack-source"
        ):
            issues.append(
                ValidationIssue(
                    SIBLING_CANARY_MATRIX_NAME,
                    "abyss-stack sibling canary entry must use resolver 'abyss-stack-source'",
                )
            )

    return issues


__all__ = ("validate_sibling_canary_matrix_surface",)
