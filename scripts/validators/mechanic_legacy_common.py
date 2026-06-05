"""Shared mechanic legacy validator helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from validators import decision_index_paths
from validators import mechanics as mechanics_validator
from validators.common import ValidationIssue, read_text_or_issue

DECISION_RECORDS_README_NAME = "docs/decisions/README.md"
MECHANICS_README_NAME = "mechanics/README.md"
MECHANICS_EVIDENCE_CLUSTERS_NAME = "mechanics/EVIDENCE_CLUSTERS.md"
PROOF_TOPOLOGY_NAME = "docs/architecture/PROOF_TOPOLOGY.md"
ROUTE_RESIDUE_GUARDS_NAME = "docs/architecture/ROUTE_RESIDUE_GUARDS.md"
LEGACY_NAMING_NAME = "docs/architecture/LEGACY_NAMING.md"
ROADMAP_NAME = "ROADMAP.md"
DESIGN_NAME = "DESIGN.md"
CHANGELOG_NAME = "CHANGELOG.md"

MECHANIC_PROVENANCE_FILES = tuple(
    f"mechanics/{parent_name}/PROVENANCE.md"
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_LEGACY_README_FILES = tuple(
    f"mechanics/{parent_name}/legacy/README.md"
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_LEGACY_INDEX_FILES = tuple(
    f"mechanics/{parent_name}/legacy/INDEX.md"
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_LEGACY_DISTILLATION_LOG_FILES = tuple(
    f"mechanics/{parent_name}/legacy/DISTILLATION_LOG.md"
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_LEGACY_RAW_README_FILES = tuple(
    f"mechanics/{parent_name}/legacy/raw/README.md"
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
)
ROADMAP_LEGACY_BRIDGE_DIRECTION_TOKENS = (
    "Legacy bridge",
    "single controlled bridge posture",
    "active mechanic surfaces",
    "runtime evidence limits",
)


def require_tokens(
    *,
    repo_root: Path,
    path_name: str,
    tokens: Sequence[str],
    issues: list[ValidationIssue],
) -> str:
    text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
    if not text:
        return text

    companion_texts: list[str] = []
    if path_name == DECISION_RECORDS_README_NAME:
        for relative_path in decision_index_paths.GENERATED_INDEX_PATHS:
            index_path = repo_root / relative_path
            if index_path.is_file():
                companion_texts.append(index_path.read_text(encoding="utf-8"))
    if path_name == PROOF_TOPOLOGY_NAME:
        route_guard_path = repo_root / ROUTE_RESIDUE_GUARDS_NAME
        if route_guard_path.is_file():
            companion_texts.append(route_guard_path.read_text(encoding="utf-8"))

    search_text = "\n\n".join((text, *companion_texts)) if companion_texts else text
    for token in tokens:
        if token not in search_text:
            issues.append(ValidationIssue(path_name, f"missing required token: {token!r}"))
    return text


__all__ = (
    "CHANGELOG_NAME",
    "DECISION_RECORDS_README_NAME",
    "DESIGN_NAME",
    "LEGACY_NAMING_NAME",
    "MECHANICS_EVIDENCE_CLUSTERS_NAME",
    "MECHANICS_README_NAME",
    "MECHANIC_LEGACY_DISTILLATION_LOG_FILES",
    "MECHANIC_LEGACY_INDEX_FILES",
    "MECHANIC_LEGACY_RAW_README_FILES",
    "MECHANIC_LEGACY_README_FILES",
    "MECHANIC_PROVENANCE_FILES",
    "PROOF_TOPOLOGY_NAME",
    "ROADMAP_LEGACY_BRIDGE_DIRECTION_TOKENS",
    "ROADMAP_NAME",
    "ROUTE_RESIDUE_GUARDS_NAME",
    "require_tokens",
)
