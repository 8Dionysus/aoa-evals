"""Active surface wording guard for former legacy parent names."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue, read_text_or_issue
from validators.mechanic_legacy_common import (
    CHANGELOG_NAME,
    DECISION_RECORDS_README_NAME,
    ROADMAP_LEGACY_BRIDGE_DIRECTION_TOKENS,
    ROADMAP_NAME,
    require_tokens,
)

ACTIVE_LEGACY_PARENT_WORDING_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0092-active-legacy-parent-wording-boundary.md"
)
ACTIVE_LEGACY_PARENT_WORDING_COMMAND = (
    "python -m pytest -q tests/test_mechanic_legacy_archive_routes.py -k active_legacy_parent_wording"
)
ACTIVE_LEGACY_PARENT_WORDING_DECISION_REQUIRED_TOKENS = (
    "Active Legacy Parent Wording Boundary",
    "legacy parent form",
    "active route wording",
    "`runtime-evidence`",
    "evidence class",
    "not the parent mechanic",
    "schema filename",
)
ACTIVE_LEGACY_PARENT_WORDING_FORBIDDEN: dict[str, tuple[str, ...]] = {
    "docs/operations/RELEASING.md": (
        "runtime-evidence example refs",
    ),
    "docs/architecture/PROOF_TOPOLOGY.md": (
        "audit runtime-evidence packets",
    ),
    "mechanics/boundary-bridge/README.md": (
        "runtime-evidence schema refs",
    ),
    "mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md": (
        "runtime-evidence schema",
    ),
    "mechanics/boundary-bridge/parts/latest-sibling-canary/config/sibling_canary_matrix.json": (
        "runtime-evidence schema refs",
    ),
    "mechanics/recurrence/parts/portable-proof-beacons/manifests/recurrence/hooks/component.evals.portable-proof-beacons.hooks.json": (
        "runtime-evidence bridge",
    ),
    "mechanics/audit/parts/README.md": (
        "# Runtime Evidence Parts",
        "`runtime-evidence` mechanic",
    ),
    "mechanics/titan/README.md": (
        "This package routes Titan canary work",
    ),
    "mechanics/titan/parts/README.md": (
        "# Titan Canaries Parts",
        "Titan-canary-owned",
    ),
    "reports/README.md": (
        "Proof-release reports",
    ),
}


def validate_active_legacy_parent_wording(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name, forbidden_tokens in ACTIVE_LEGACY_PARENT_WORDING_FORBIDDEN.items():
        text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
        if not text:
            continue
        for token in forbidden_tokens:
            if token in text:
                issues.append(
                    ValidationIssue(
                        path_name,
                        f"active route wording must not use legacy parent form {token!r}",
                    )
                )
    require_tokens(
        repo_root=repo_root,
        path_name=ACTIVE_LEGACY_PARENT_WORDING_DECISION_NAME,
        tokens=ACTIVE_LEGACY_PARENT_WORDING_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(
            ACTIVE_LEGACY_PARENT_WORDING_DECISION_NAME,
            "Active Legacy Parent Wording Boundary",
        ),
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_LEGACY_BRIDGE_DIRECTION_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=CHANGELOG_NAME,
        tokens=("Active Legacy Parent Wording Boundary", "runtime evidence"),
        issues=issues,
    )
    return issues


__all__ = (
    "ACTIVE_LEGACY_PARENT_WORDING_COMMAND",
    "ACTIVE_LEGACY_PARENT_WORDING_DECISION_NAME",
    "ACTIVE_LEGACY_PARENT_WORDING_DECISION_REQUIRED_TOKENS",
    "ACTIVE_LEGACY_PARENT_WORDING_FORBIDDEN",
    "validate_active_legacy_parent_wording",
)
