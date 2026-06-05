"""Mechanic parent index and command-hygiene guards."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue, read_text_or_issue
from validators.mechanic_parent_common import markdown_python_commands, require_tokens


MECHANIC_LOWER_PARTS_INDEX_REQUIRED_TOKENS = (
    "## Operating Card",
    "| role |",
    "| input |",
    "| output |",
    "| owner |",
    "| next route |",
    "| tools |",
    "| validation |",
    "## Active Parts",
    "## Part Admission Route",
    "AGENTS.md#validation",
)


def validate_mechanic_index_command_ownership(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    index_paths = sorted((repo_root / "mechanics").glob("*/PARTS.md"))
    index_paths.extend(sorted((repo_root / "mechanics").glob("*/parts/README.md")))

    for path in index_paths:
        relative_name = path.relative_to(repo_root).as_posix()
        text = read_text_or_issue(path, issues, root=repo_root)
        if not text:
            continue
        if markdown_python_commands(text):
            issues.append(
                ValidationIssue(
                    relative_name,
                    "mechanic index surfaces must route executable validation commands to the nearest AGENTS.md instead of carrying python command blocks",
                )
            )

    return issues


def validate_mechanic_lower_parts_index_operating_cards(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    parts_dirs = sorted(
        path for path in (repo_root / "mechanics").glob("*/parts") if path.is_dir()
    )

    for parts_dir in parts_dirs:
        path = parts_dir / "README.md"
        relative_name = path.relative_to(repo_root).as_posix()
        if not path.exists():
            issues.append(
                ValidationIssue(
                    relative_name,
                    "lower parts index README is missing",
                )
            )
            continue
        require_tokens(
            repo_root=repo_root,
            path_name=relative_name,
            tokens=MECHANIC_LOWER_PARTS_INDEX_REQUIRED_TOKENS,
            issues=issues,
        )

    return issues


__all__ = (
    "MECHANIC_LOWER_PARTS_INDEX_REQUIRED_TOKENS",
    "validate_mechanic_index_command_ownership",
    "validate_mechanic_lower_parts_index_operating_cards",
)
