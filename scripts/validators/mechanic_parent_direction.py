"""Mechanic parent current-direction route contracts."""

from __future__ import annotations

from pathlib import Path

from validators import mechanics as mechanics_validator
from validators.common import ValidationIssue, read_text_or_issue
from validators.mechanic_parent_common import (
    DECISION_RECORDS_README_NAME,
    LEGACY_NAMING_NAME,
    MECHANICS_AGENTS_NAME,
    MECHANICS_README_NAME,
    PROOF_TOPOLOGY_NAME,
    ROADMAP_NAME,
    require_tokens,
)


MECHANIC_PARENT_DIRECTION_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0082-mechanic-parent-direction-contract.md"
)
MECHANIC_PARENT_DIRECTION_COMMAND = (
    "python -m pytest -q tests/test_mechanic_parent_direction.py -k mechanic_parent_direction"
)
MECHANIC_PARENT_README_FILES = tuple(
    f"mechanics/{parent_name}/README.md"
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_PARENT_AGENTS_FILES = tuple(
    f"mechanics/{parent_name}/AGENTS.md"
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_DIRECTION_FILES = tuple(
    f"mechanics/{parent_name}/DIRECTION.md"
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES
)
MECHANIC_DIRECTION_REQUIRED_TOKENS = (
    "current operating direction",
    "## Source-of-truth split",
    "`README.md`",
    "`DIRECTION.md`",
    "`PARTS.md`",
    "`PROVENANCE.md`",
    "`legacy/`",
    "archive-local route",
    "## Current contour",
    "## Growth rule",
    "## Stop-lines",
    "## Validation",
)
MECHANIC_PARENT_README_DIRECTION_ROUTE_REQUIRED_TOKENS = (
    "## Entry Route",
    "## Role",
    "## Owned Operation",
    "[DIRECTION.md](DIRECTION.md)",
    "current operating direction",
    "[PARTS.md](PARTS.md)",
    "[PROVENANCE.md](PROVENANCE.md)",
    "active-to-archive bridge",
    "## Validation",
    "AGENTS.md#validation",
    "## Next Route",
)
MECHANIC_PARENT_README_STALE_STOP_LINE_LEAD_IN = "Do not use this package to claim:"
MECHANIC_PARENT_README_STALE_PROVENANCE_ROUTE = (
    "[PROVENANCE.md](PROVENANCE.md) only"
)
ACTIVE_MECHANIC_ROUTE_STALE_ROLE_PHRASES: dict[str, tuple[str, ...]] = {
    "mechanics/boundary-bridge/README.md": (
        "refs that should not feed proof",
    ),
    "mechanics/agon/PARTS.md": (
        "Do not split one future-growing operation",
    ),
    "mechanics/agon/README.md": (
        "They do not define the active package name",
        "not the route for new Agon work",
    ),
    "mechanics/distillation/README.md": (
        "It is not an active Distillation source surface",
        "not a replacement for the source bundles",
    ),
    "mechanics/proof-loop/README.md": (
        "Do not use it as a generic eval-result example",
    ),
}
MECHANIC_PARENT_AGENTS_DIRECTION_ROUTE_REQUIRED_TOKENS = (
    "## Entry Route",
    "current operating direction",
    "active-to-archive bridge",
)
MECHANIC_PARENT_AGENTS_STALE_PROVENANCE_ROUTE_TEMPLATE = (
    "`mechanics/{parent_name}/PROVENANCE.md` only"
)
MECHANIC_PARENT_DIRECTION_DECISION_REQUIRED_TOKENS = (
    "Mechanic Parent Direction Contract",
    "`DIRECTION.md`",
    "current operating direction",
    "`## Role`",
    "`## Next Route`",
    "`README.md`",
    "`PARTS.md`",
    "`PROVENANCE.md`",
    "active-to-archive bridge",
    "not provenance",
    "not a part map",
    MECHANIC_PARENT_DIRECTION_COMMAND,
)
ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS = (
    "Mechanic lower index",
    "DIRECTION.md",
    "part/payload source surfaces",
    "parts index synchronization",
    "payload coverage",
)


def validate_mechanic_parent_direction_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path_name in MECHANIC_DIRECTION_FILES:
        require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=MECHANIC_DIRECTION_REQUIRED_TOKENS,
            issues=issues,
        )

    for path_name in MECHANIC_PARENT_README_FILES:
        require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=MECHANIC_PARENT_README_DIRECTION_ROUTE_REQUIRED_TOKENS,
            issues=issues,
        )
        text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
        if text is None:
            continue
        if MECHANIC_PARENT_README_STALE_PROVENANCE_ROUTE in text:
            issues.append(
                ValidationIssue(
                    path_name,
                    "mechanic parent README must route PROVENANCE.md as the active-to-archive bridge; stale only-when legacy side-path wording is retired",
                )
            )
        if MECHANIC_PARENT_README_STALE_STOP_LINE_LEAD_IN in text:
            issues.append(
                ValidationIssue(
                    path_name,
                    "mechanic parent README must introduce Stop-Lines as a bounded eval-side proof boundary, not the old package-claim scaffold",
                )
            )

    for path_name, stale_phrases in ACTIVE_MECHANIC_ROUTE_STALE_ROLE_PHRASES.items():
        text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
        if text is None:
            continue
        for stale_phrase in stale_phrases:
            if stale_phrase in text:
                issues.append(
                    ValidationIssue(
                        path_name,
                        "active mechanic route surface must use positive owner-route language instead of stale negative role scaffold "
                        f"{stale_phrase!r}",
                    )
                )

    for parent_name, path_name in zip(
        mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES,
        MECHANIC_PARENT_AGENTS_FILES,
        strict=True,
    ):
        require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=(
                *MECHANIC_PARENT_AGENTS_DIRECTION_ROUTE_REQUIRED_TOKENS,
                f"`mechanics/{parent_name}/DIRECTION.md`",
                f"`mechanics/{parent_name}/PARTS.md`",
                f"`mechanics/{parent_name}/PROVENANCE.md`",
            ),
            issues=issues,
        )
        text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
        if text is None:
            continue
        stale_route = MECHANIC_PARENT_AGENTS_STALE_PROVENANCE_ROUTE_TEMPLATE.format(
            parent_name=parent_name
        )
        if stale_route in text:
            issues.append(
                ValidationIssue(
                    path_name,
                    "mechanic parent AGENTS card must route PROVENANCE.md as the active-to-archive bridge; stale only-when legacy side-path wording is retired",
                )
            )

    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PARENT_DIRECTION_DECISION_NAME,
        tokens=MECHANIC_PARENT_DIRECTION_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(
            MECHANIC_PARENT_DIRECTION_DECISION_NAME,
            "Mechanic Parent Direction Contract",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("Mechanic parent direction", "`DIRECTION.md`"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=LEGACY_NAMING_NAME,
        tokens=("DIRECTION.md", "current operating direction"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("DIRECTION.md", "current operating direction", "Entry Route"),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_AGENTS_NAME,
        tokens=("target package `DIRECTION.md`", "current operating direction"),
        issues=issues,
    )
    return issues


__all__ = (
    "MECHANIC_PARENT_DIRECTION_DECISION_NAME",
    "MECHANIC_PARENT_DIRECTION_COMMAND",
    "MECHANIC_PARENT_README_FILES",
    "MECHANIC_PARENT_AGENTS_FILES",
    "MECHANIC_DIRECTION_FILES",
    "MECHANIC_DIRECTION_REQUIRED_TOKENS",
    "MECHANIC_PARENT_README_DIRECTION_ROUTE_REQUIRED_TOKENS",
    "MECHANIC_PARENT_README_STALE_STOP_LINE_LEAD_IN",
    "MECHANIC_PARENT_README_STALE_PROVENANCE_ROUTE",
    "ACTIVE_MECHANIC_ROUTE_STALE_ROLE_PHRASES",
    "MECHANIC_PARENT_AGENTS_DIRECTION_ROUTE_REQUIRED_TOKENS",
    "MECHANIC_PARENT_AGENTS_STALE_PROVENANCE_ROUTE_TEMPLATE",
    "MECHANIC_PARENT_DIRECTION_DECISION_REQUIRED_TOKENS",
    "ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS",
    "validate_mechanic_parent_direction_surfaces",
)
