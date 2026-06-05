"""Mechanic legacy archive skeleton, route-language, and raw accounting contracts."""

from __future__ import annotations

import re
from pathlib import Path

from validators import mechanics as mechanics_validator
from validators.common import ValidationIssue, read_text_or_issue
from validators.mechanic_legacy_common import (
    DECISION_RECORDS_README_NAME,
    MECHANIC_LEGACY_DISTILLATION_LOG_FILES,
    MECHANIC_LEGACY_INDEX_FILES,
    MECHANIC_LEGACY_RAW_README_FILES,
    MECHANIC_LEGACY_README_FILES,
    MECHANIC_PROVENANCE_FILES,
    require_tokens,
)
from validators.mechanic_provenance_bridge import validate_mechanic_legacy_bridge_surfaces

MECHANIC_LEGACY_SKELETON_FILES = (
    MECHANIC_PROVENANCE_FILES
    + MECHANIC_LEGACY_README_FILES
    + MECHANIC_LEGACY_INDEX_FILES
    + MECHANIC_LEGACY_DISTILLATION_LOG_FILES
    + MECHANIC_LEGACY_RAW_README_FILES
)
MECHANIC_LEGACY_ARCHIVE_ROUTE_FILES = (
    MECHANIC_LEGACY_README_FILES
    + MECHANIC_LEGACY_INDEX_FILES
    + MECHANIC_LEGACY_DISTILLATION_LOG_FILES
    + MECHANIC_LEGACY_RAW_README_FILES
)

MECHANIC_LEGACY_SKELETON_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0071-mechanic-legacy-skeleton-contract.md"
)
MECHANIC_LEGACY_RAW_README_REQUIRED_TOKENS = (
    "git history",
    "INDEX.md",
)
MECHANIC_LEGACY_README_REQUIRED_TOKENS = (
    "../PROVENANCE.md",
    "INDEX.md",
    "DISTILLATION_LOG.md",
    "raw/README.md",
    "archive-local route",
    "current active route",
)
MECHANIC_LEGACY_RAW_PAYLOAD_DECISION_REQUIRED_TOKENS = (
    "raw payload",
    "archive-local index or accounting log",
    "forgotten residue",
    "current active route",
    "active part route",
    "raw-only archive route",
)
MECHANIC_LEGACY_SKELETON_DECISION_REQUIRED_TOKENS = (
    "Mechanic Legacy Archive Boundary",
    "`PROVENANCE.md`",
    "`legacy/README.md`",
    "archive-local route",
    "archive-local index",
    "accounting log",
    "`../PROVENANCE.md`",
    "Current Applicability",
    "Review Log",
    "current active route",
    "unindexed raw payloads",
    "current-route expectations",
    "validation through the nearest legacy `AGENTS.md`",
    "python -m pytest -q tests/test_mechanic_parent_topology.py -k mechanic_legacy_skeleton",
    "python -m pytest -q tests/test_mechanic_legacy_archive_routes.py -k mechanic_legacy_raw_payload",
)

MECHANIC_LEGACY_ARCHIVE_COMMAND_RE = re.compile(
    r"```(?:bash|sh)\b|`python (?:scripts/|-m pytest)|^python (?:scripts/|-m pytest)",
    re.MULTILINE,
)
MECHANIC_LEGACY_ARCHIVE_STALE_ROUTE_PHRASES = (
    "Do not create new",
    "Do not begin new",
    "Do not recreate",
    "Do not treat",
    "Do not use",
    "It is not",
    "does not own",
    "Legacy only explains",
    "legacy only explains",
    "not the active",
    "not an active",
    "not active",
    "not a changelog",
    " not ",
)


def validate_mechanic_legacy_archive_route_language(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path_name in MECHANIC_LEGACY_ARCHIVE_ROUTE_FILES:
        text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
        if text is None:
            continue
        command_match = MECHANIC_LEGACY_ARCHIVE_COMMAND_RE.search(text)
        if command_match is not None:
            issues.append(
                ValidationIssue(
                    path_name,
                    "legacy archive route files must point validation to AGENTS.md instead of carrying executable command blocks",
                )
            )
        for phrase in MECHANIC_LEGACY_ARCHIVE_STALE_ROUTE_PHRASES:
            if phrase in text:
                issues.append(
                    ValidationIssue(
                        path_name,
                        f"legacy archive route files must name current active route expectations instead of stale negative scaffold `{phrase}`",
                    )
                )

    return issues


def validate_mechanic_legacy_raw_payload_accounting(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES:
        legacy_root = repo_root / "mechanics" / parent_name / "legacy"
        raw_root = legacy_root / "raw"
        if not raw_root.is_dir():
            continue

        index_path = legacy_root / "INDEX.md"
        log_path = legacy_root / "DISTILLATION_LOG.md"
        if not index_path.is_file() or not log_path.is_file():
            continue

        accounting_text = (
            index_path.read_text(encoding="utf-8")
            + "\n"
            + log_path.read_text(encoding="utf-8")
        )
        index_text = index_path.read_text(encoding="utf-8")

        for path in sorted(raw_root.rglob("*")):
            if not path.is_file() or path.name == "README.md":
                continue
            legacy_relative = path.relative_to(legacy_root).as_posix()
            if legacy_relative not in accounting_text and path.name not in accounting_text:
                issues.append(
                    ValidationIssue(
                        path.relative_to(repo_root).as_posix(),
                        "legacy raw payload must be referenced by the archive-local index or accounting log",
                    )
                )
                continue

            raw_index_lines = [
                line
                for line in index_text.splitlines()
                if legacy_relative in line or path.name in line
            ]
            if not raw_index_lines:
                issues.append(
                    ValidationIssue(
                        path.relative_to(repo_root).as_posix(),
                        "legacy raw payload must have an archive-local INDEX.md row that maps it to a current active route",
                    )
                )
                continue

            active_part_route = f"mechanics/{parent_name}/parts/"
            package_wide_route = (
                f"mechanics/{parent_name}/DIRECTION.md",
                f"mechanics/{parent_name}/PARTS.md",
            )
            has_active_route = any(
                "/legacy/" not in line
                and (
                    active_part_route in line
                    or all(route in line for route in package_wide_route)
                )
                for line in raw_index_lines
            )
            if not has_active_route:
                issues.append(
                    ValidationIssue(
                        path.relative_to(repo_root).as_posix(),
                        "legacy raw payload INDEX.md row must map to a current active part route or package-wide DIRECTION/PARTS route, not only a raw-only archive route",
                    )
                )

    return issues


def validate_mechanic_legacy_skeleton_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path_name in MECHANIC_LEGACY_SKELETON_FILES:
        if not (repo_root / path_name).is_file():
            issues.append(
                ValidationIssue(
                    path_name,
                    "active mechanic parent must expose PROVENANCE.md and archive-local legacy entry/accounting surfaces",
                )
            )
    for path_name in MECHANIC_LEGACY_README_FILES:
        require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=MECHANIC_LEGACY_README_REQUIRED_TOKENS,
            issues=issues,
        )
    for path_name in MECHANIC_LEGACY_RAW_README_FILES:
        require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=MECHANIC_LEGACY_RAW_README_REQUIRED_TOKENS,
            issues=issues,
        )
    issues.extend(validate_mechanic_legacy_archive_route_language(repo_root))
    issues.extend(validate_mechanic_legacy_raw_payload_accounting(repo_root))
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_LEGACY_SKELETON_DECISION_NAME,
        tokens=MECHANIC_LEGACY_SKELETON_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_LEGACY_SKELETON_DECISION_NAME,
        tokens=MECHANIC_LEGACY_RAW_PAYLOAD_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(
            MECHANIC_LEGACY_SKELETON_DECISION_NAME,
            "Mechanic Legacy Archive Boundary",
        ),
        issues=issues,
    )

    return issues


def validate_mechanic_legacy_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(validate_mechanic_legacy_skeleton_surfaces(repo_root))
    issues.extend(validate_mechanic_legacy_bridge_surfaces(repo_root))
    return issues


__all__ = (
    "MECHANIC_LEGACY_ARCHIVE_ROUTE_FILES",
    "MECHANIC_LEGACY_DISTILLATION_LOG_FILES",
    "MECHANIC_LEGACY_INDEX_FILES",
    "MECHANIC_LEGACY_RAW_PAYLOAD_DECISION_REQUIRED_TOKENS",
    "MECHANIC_LEGACY_RAW_README_FILES",
    "MECHANIC_LEGACY_RAW_README_REQUIRED_TOKENS",
    "MECHANIC_LEGACY_README_FILES",
    "MECHANIC_LEGACY_README_REQUIRED_TOKENS",
    "MECHANIC_LEGACY_SKELETON_DECISION_NAME",
    "MECHANIC_LEGACY_SKELETON_DECISION_REQUIRED_TOKENS",
    "MECHANIC_LEGACY_SKELETON_FILES",
    "validate_mechanic_legacy_archive_route_language",
    "validate_mechanic_legacy_raw_payload_accounting",
    "validate_mechanic_legacy_skeleton_surfaces",
    "validate_mechanic_legacy_surfaces",
)
