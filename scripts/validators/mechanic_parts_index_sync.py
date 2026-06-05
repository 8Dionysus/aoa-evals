"""Mechanic parent PARTS.md local part route synchronization."""

from __future__ import annotations

import re
from pathlib import Path

from validators import mechanics as mechanics_validator
from validators.common import ValidationIssue, read_text_or_issue
from validators.mechanic_part_contract_common import (
    MECHANICS_README_NAME,
    PROOF_TOPOLOGY_NAME,
    ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS,
    ROADMAP_NAME,
    _require_tokens,
)


MECHANIC_PARTS_INDEX_SYNC_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0088-mechanic-parts-index-synchronization.md"
)
MECHANIC_PARTS_INDEX_SYNC_COMMAND = (
    "python -m pytest -q tests/test_mechanic_parts_index.py -k mechanic_parts_index_sync"
)
MECHANIC_PARTS_INDEX_SYNC_DECISION_REQUIRED_TOKENS = (
    "Mechanic PARTS Index Synchronization",
    "`mechanics/<parent>/PARTS.md`",
    "actual part directory",
    "declared part route",
    "stale local part route",
    "cross-parent reference",
    MECHANIC_PARTS_INDEX_SYNC_COMMAND,
)
MECHANIC_PART_SLUG_PATTERN = r"[a-z0-9][a-z0-9_.-]+"


def mechanic_parts_index_declared_slugs(
    parts_index_text: str,
    parent_name: str,
) -> set[str]:
    declared: set[str] = set()

    full_path_pattern = re.compile(
        rf"mechanics/{re.escape(parent_name)}/parts/({MECHANIC_PART_SLUG_PATTERN})(?:/README\.md|/)"
    )
    declared.update(full_path_pattern.findall(parts_index_text))

    relative_path_pattern = re.compile(
        rf"(?:^|[^A-Za-z0-9_./-])parts/({MECHANIC_PART_SLUG_PATTERN})(?:/README\.md|/)",
        re.MULTILINE,
    )
    declared.update(relative_path_pattern.findall(parts_index_text))

    heading_pattern = re.compile(
        rf"^###\s+`?({MECHANIC_PART_SLUG_PATTERN})`?\s*$",
        re.MULTILINE,
    )
    declared.update(heading_pattern.findall(parts_index_text))

    lines = parts_index_text.splitlines()
    index = 0
    while index < len(lines) - 1:
        line = lines[index].strip()
        next_line = lines[index + 1].strip()
        if line.startswith("|") and next_line.startswith("|"):
            header_cells = [cell.strip().lower() for cell in line.strip("|").split("|")]
            separator_cells = [
                cell.strip().replace(" ", "")
                for cell in next_line.strip("|").split("|")
            ]
            is_separator = bool(separator_cells) and all(
                set(cell) <= {"-", ":"} and "-" in cell for cell in separator_cells
            )
            if header_cells and "part" in header_cells[0] and is_separator:
                row_index = index + 2
                while row_index < len(lines) and lines[row_index].strip().startswith("|"):
                    first_cell = lines[row_index].strip().strip("|").split("|")[0]
                    declared.update(
                        re.findall(rf"`({MECHANIC_PART_SLUG_PATTERN})`", first_cell)
                    )
                    row_index += 1
                index = row_index
                continue
        index += 1

    return declared


def validate_mechanic_parts_index_sync_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES:
        parent_root = repo_root / "mechanics" / parent_name
        parts_root = parent_root / "parts"
        parts_index_name = f"mechanics/{parent_name}/PARTS.md"
        if not parts_root.is_dir():
            continue

        actual_parts = {
            path.name
            for path in parts_root.iterdir()
            if path.is_dir()
        }
        parts_index_text = read_text_or_issue(
            repo_root / parts_index_name,
            issues,
            root=repo_root,
        )
        if not parts_index_text:
            continue

        declared_parts = mechanic_parts_index_declared_slugs(
            parts_index_text,
            parent_name,
        )
        for part_name in sorted(actual_parts - declared_parts):
            issues.append(
                ValidationIssue(
                    parts_index_name,
                    f"parent PARTS.md must declare actual part directory `{part_name}` as a local part route",
                )
            )
        for part_name in sorted(declared_parts - actual_parts):
            issues.append(
                ValidationIssue(
                    parts_index_name,
                    f"parent PARTS.md declares stale local part route `{part_name}` with no matching actual part directory",
                )
            )

    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PARTS_INDEX_SYNC_DECISION_NAME,
        tokens=MECHANIC_PARTS_INDEX_SYNC_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            MECHANIC_PARTS_INDEX_SYNC_DECISION_NAME,
            "Mechanic PARTS Index Synchronization",
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("declared part route", "stale local part route"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("actual part directory", "cross-parent reference"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS,
        issues=issues,
    )

    return issues


__all__ = (
    "MECHANIC_PARTS_INDEX_SYNC_COMMAND",
    "MECHANIC_PARTS_INDEX_SYNC_DECISION_NAME",
    "MECHANIC_PARTS_INDEX_SYNC_DECISION_REQUIRED_TOKENS",
    "MECHANIC_PART_SLUG_PATTERN",
    "mechanic_parts_index_declared_slugs",
    "validate_mechanic_parts_index_sync_surfaces",
)
