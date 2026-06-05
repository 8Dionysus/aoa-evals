"""Root legacy naming posture guide and decision checks."""

from __future__ import annotations

from pathlib import Path

from validators import root_legacy_common as common
from validators.common import ValidationIssue, read_text_or_issue


LEGACY_NAMING_NAME = common.LEGACY_NAMING_NAME
LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME = (
    common.LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME
)
LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_COMMAND = common.LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_COMMAND
LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME = common.LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME
LEGACY_NAMING_POSTURE_GUIDE_COMMAND = common.LEGACY_NAMING_POSTURE_GUIDE_COMMAND
LEGACY_NAMING_REQUIRED_TOKENS = common.LEGACY_NAMING_REQUIRED_TOKENS
LEGACY_NAMING_FORBIDDEN_DETAIL_TOKENS = common.LEGACY_NAMING_FORBIDDEN_DETAIL_TOKENS
LEGACY_NAMING_DECISION_REQUIRED_TOKENS = common.LEGACY_NAMING_DECISION_REQUIRED_TOKENS
LEGACY_NAMING_POSTURE_GUIDE_DECISION_REQUIRED_TOKENS = (
    common.LEGACY_NAMING_POSTURE_GUIDE_DECISION_REQUIRED_TOKENS
)
LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_REQUIRED_TOKENS = (
    common.LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_REQUIRED_TOKENS
)
ROADMAP_LEGACY_NAMING_DIRECTION_TOKENS = common.ROADMAP_LEGACY_NAMING_DIRECTION_TOKENS


def validate_legacy_naming_posture_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    common.require_tokens(repo_root, LEGACY_NAMING_NAME, LEGACY_NAMING_REQUIRED_TOKENS, issues)
    text = read_text_or_issue(repo_root / LEGACY_NAMING_NAME, issues, root=repo_root)
    if text:
        for forbidden_token in LEGACY_NAMING_FORBIDDEN_DETAIL_TOKENS:
            if forbidden_token in text:
                issues.append(
                    ValidationIssue(
                        LEGACY_NAMING_NAME,
                        "legacy naming posture guide must not carry concrete legacy-name inventories or wrong-parent maps; use active topology surfaces or owning legacy archives",
                    )
                )
    common.require_tokens(
        repo_root,
        "docs/decisions/AOA-EV-D-0009-legacy-naming-containment.md",
        LEGACY_NAMING_DECISION_REQUIRED_TOKENS,
        issues,
    )
    common.require_tokens(
        repo_root,
        LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME,
        LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_REQUIRED_TOKENS,
        issues,
    )
    common.require_tokens(
        repo_root,
        LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME,
        LEGACY_NAMING_POSTURE_GUIDE_DECISION_REQUIRED_TOKENS,
        issues,
    )
    common.require_tokens(
        repo_root,
        common.DECISION_RECORDS_README_NAME,
        (
            LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME,
            "Legacy Naming Single-Bridge Language",
            LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME,
            "Legacy Naming Posture Guide",
        ),
        issues,
    )
    common.require_tokens(repo_root, "README.md", (LEGACY_NAMING_NAME, "accepted-input"), issues)
    common.require_tokens(
        repo_root,
        common.PROOF_TOPOLOGY_NAME,
        (LEGACY_NAMING_NAME, "generated-projection", "provenance-bridge"),
        issues,
    )
    common.require_tokens(repo_root, common.ROADMAP_NAME, ROADMAP_LEGACY_NAMING_DIRECTION_TOKENS, issues)
    common.require_tokens(
        repo_root,
        "CHANGELOG.md",
        (
            "Legacy Naming Single-Bridge Language",
            "Legacy Naming Posture Guide",
            "single controlled bridge",
        ),
        issues,
    )
    return issues
