"""Mechanic PROVENANCE active-to-archive bridge contracts."""

from __future__ import annotations

import re
from pathlib import Path

from validators import mechanics as mechanics_validator
from validators.common import ValidationIssue, read_text_or_issue
from validators.mechanic_legacy_common import (
    DECISION_RECORDS_README_NAME,
    DESIGN_NAME,
    LEGACY_NAMING_NAME,
    MECHANICS_README_NAME,
    MECHANIC_PROVENANCE_FILES,
    PROOF_TOPOLOGY_NAME,
    ROADMAP_LEGACY_BRIDGE_DIRECTION_TOKENS,
    ROADMAP_NAME,
    require_tokens,
)

MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0089-mechanic-legacy-single-bridge.md"
)
MECHANIC_LEGACY_SINGLE_BRIDGE_COMMAND = (
    "python -m pytest -q tests/test_mechanic_legacy_bridge.py -k mechanic_legacy_single_bridge"
)
MECHANIC_PROVENANCE_BRIDGE_POSTURE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0090-mechanic-provenance-bridge-posture.md"
)
MECHANIC_PROVENANCE_BRIDGE_POSTURE_COMMAND = (
    "python -m pytest -q tests/test_mechanic_legacy_bridge.py -k mechanic_provenance_bridge_posture"
)
MECHANIC_PROVENANCE_ENTRY_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0075-mechanic-provenance-entry-contract.md"
)

MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_REQUIRED_TOKENS = (
    "Mechanic Legacy Single Bridge",
    "`PROVENANCE.md`",
    "single controlled bridge",
    "active mechanic surfaces",
    "legacy archive",
    "active surface",
    "direct archive-internal references",
    "must not carry archive details",
    "JSON",
    "YAML",
    MECHANIC_LEGACY_SINGLE_BRIDGE_COMMAND,
)
MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS = (
    "`PROVENANCE.md` is the active-to-archive bridge for this mechanic.",
    "Use active surfaces first:",
    "DIRECTION.md",
    "PARTS.md",
    "parts/",
    "legacy archive",
    "legacy/README.md",
    "owns its own details",
    "archive details stay in the legacy archive",
)
MECHANIC_PROVENANCE_BRIDGE_POSTURE_DECISION_REQUIRED_TOKENS = (
    "Mechanic Provenance Bridge Posture",
    "Current Applicability",
    "active-to-archive bridge",
    "Review Log",
    "Use active surfaces first:",
    "`DIRECTION.md`",
    "legacy archive",
    "legacy/README.md",
    "owns its own details",
    MECHANIC_PROVENANCE_BRIDGE_POSTURE_COMMAND,
)
MECHANIC_PROVENANCE_ENTRY_REQUIRED_TOKENS = (
    "active",
    "legacy/README.md",
    "legacy archive owns",
    "archive details",
)
MECHANIC_PROVENANCE_ENTRY_DECISION_REQUIRED_TOKENS = (
    "Mechanic Provenance Entry Contract",
    "`PROVENANCE.md`",
    "`legacy/README.md`",
    "active route first",
    "not active topology",
    "archive details",
    "python -m pytest -q tests/test_validate_repo.py -k mechanic_provenance_entry",
)

MECHANIC_LEGACY_ACTIVE_DIRECT_REF_RE = re.compile(
    r"(?:mechanics/[a-z0-9-]+/)?legacy/(?:README\.md|INDEX\.md|DISTILLATION_LOG\.md|raw(?:/|`|\)|\]|\s|$))"
    r"|raw/README\.md"
)
MECHANIC_LEGACY_ACTIVE_SURFACE_SUFFIXES = (".md", ".json", ".yaml", ".yml", ".py")
MECHANIC_PROVENANCE_ARCHIVE_DETAIL_RE = re.compile(
    r"legacy/(?:INDEX\.md|DISTILLATION_LOG\.md|raw(?:/|`|\)|\]|\s|$))"
    r"|raw/README\.md"
)


def validate_mechanic_legacy_single_bridge_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES:
        parent_root = repo_root / "mechanics" / parent_name
        if not parent_root.is_dir():
            continue

        for path in sorted(parent_root.rglob("*")):
            if not path.is_file() or path.suffix not in MECHANIC_LEGACY_ACTIVE_SURFACE_SUFFIXES:
                continue
            relative_parts = path.relative_to(parent_root).parts
            if "legacy" in relative_parts:
                continue
            text = read_text_or_issue(path, issues, root=repo_root)
            if text is None:
                continue
            if path.name == "PROVENANCE.md":
                for match in MECHANIC_PROVENANCE_ARCHIVE_DETAIL_RE.finditer(text):
                    issues.append(
                        ValidationIssue(
                            path.relative_to(repo_root).as_posix(),
                            f"PROVENANCE.md must bridge to legacy/README.md without carrying archive detail `{match.group(0)}`",
                        )
                    )
                continue
            for match in MECHANIC_LEGACY_ACTIVE_DIRECT_REF_RE.finditer(text):
                issues.append(
                    ValidationIssue(
                        path.relative_to(repo_root).as_posix(),
                        f"active mechanic surface must route legacy archive details through PROVENANCE.md, not direct `{match.group(0)}`",
                    )
                )

    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_NAME,
        tokens=MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(
            MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_NAME,
            "Mechanic Legacy Single Bridge",
        ),
        issues=issues,
    )
    for path_name in (MECHANICS_README_NAME, PROOF_TOPOLOGY_NAME, LEGACY_NAMING_NAME):
        require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=("single controlled bridge", "active mechanic surfaces", "legacy archive"),
            issues=issues,
        )
    require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_LEGACY_BRIDGE_DIRECTION_TOKENS,
        issues=issues,
    )

    return issues


def validate_mechanic_provenance_entry_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path_name in MECHANIC_PROVENANCE_FILES:
        require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=MECHANIC_PROVENANCE_ENTRY_REQUIRED_TOKENS,
            issues=issues,
        )
        text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
        if text:
            for match in MECHANIC_PROVENANCE_ARCHIVE_DETAIL_RE.finditer(text):
                issues.append(
                    ValidationIssue(
                        path_name,
                        f"PROVENANCE.md must bridge to legacy/README.md without carrying archive detail `{match.group(0)}`",
                    )
                )

    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PROVENANCE_ENTRY_DECISION_NAME,
        tokens=MECHANIC_PROVENANCE_ENTRY_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(
            MECHANIC_PROVENANCE_ENTRY_DECISION_NAME,
            "Mechanic Provenance Entry Contract",
        ),
        issues=issues,
    )

    return issues


def validate_mechanic_provenance_bridge_posture_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path_name in MECHANIC_PROVENANCE_FILES:
        require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS,
            issues=issues,
        )

    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PROVENANCE_BRIDGE_POSTURE_DECISION_NAME,
        tokens=MECHANIC_PROVENANCE_BRIDGE_POSTURE_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(
            MECHANIC_PROVENANCE_BRIDGE_POSTURE_DECISION_NAME,
            "Mechanic Provenance Bridge Posture",
        ),
        issues=issues,
    )
    for path_name in (MECHANICS_README_NAME, PROOF_TOPOLOGY_NAME, LEGACY_NAMING_NAME):
        require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=(
                "`PROVENANCE.md` is the active-to-archive bridge",
                "Use active surfaces first:",
                "legacy archive",
            ),
            issues=issues,
        )
    require_tokens(
        repo_root=repo_root,
        path_name=DESIGN_NAME,
        tokens=(
            "single controlled bridge",
            "active-to-archive bridge",
            "legacy archive",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_LEGACY_BRIDGE_DIRECTION_TOKENS,
        issues=issues,
    )

    return issues


def validate_mechanic_legacy_bridge_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(validate_mechanic_legacy_single_bridge_surfaces(repo_root))
    issues.extend(validate_mechanic_provenance_entry_surfaces(repo_root))
    issues.extend(validate_mechanic_provenance_bridge_posture_surfaces(repo_root))
    return issues


__all__ = (
    "MECHANIC_LEGACY_SINGLE_BRIDGE_COMMAND",
    "MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_NAME",
    "MECHANIC_LEGACY_SINGLE_BRIDGE_DECISION_REQUIRED_TOKENS",
    "MECHANIC_PROVENANCE_BRIDGE_POSTURE_COMMAND",
    "MECHANIC_PROVENANCE_BRIDGE_POSTURE_DECISION_NAME",
    "MECHANIC_PROVENANCE_BRIDGE_POSTURE_DECISION_REQUIRED_TOKENS",
    "MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS",
    "MECHANIC_PROVENANCE_ENTRY_DECISION_NAME",
    "MECHANIC_PROVENANCE_ENTRY_DECISION_REQUIRED_TOKENS",
    "MECHANIC_PROVENANCE_ENTRY_REQUIRED_TOKENS",
    "MECHANIC_PROVENANCE_FILES",
    "validate_mechanic_legacy_bridge_surfaces",
    "validate_mechanic_legacy_single_bridge_surfaces",
    "validate_mechanic_provenance_bridge_posture_surfaces",
    "validate_mechanic_provenance_entry_surfaces",
)
