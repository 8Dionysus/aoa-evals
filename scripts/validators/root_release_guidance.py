"""Release guide route contract validation."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue
from validators.root_guidance_common import reject_tokens, require_tokens

RELEASING_GUIDE_NAME = "docs/operations/RELEASING.md"
RELEASING_ROUTE_MAP_REQUIRED_TOKENS = (
    "## Operating Card",
    "root release process guide",
    "bounded release scope",
    "readiness/live-status route",
    "release-support validation lane",
    "root validation lane",
    "local release-prep reviewability evidence",
    "current git, GitHub, tag, release, PR, and objective evidence",
    "requirement-by-requirement handoff evidence",
    "current objective audit and landing evidence",
    "pre-PR snapshot",
    "current git and GitHub evidence for live branch, commit, push, PR",
)
RELEASING_FORBIDDEN_STATUS_LEDGER_TOKENS = (
    "not a tag",
    "not a branch",
    "not goal completion",
    "goal-completion proof",
)


def validate_releasing_route_map_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    text = require_tokens(
        repo_root,
        RELEASING_GUIDE_NAME,
        RELEASING_ROUTE_MAP_REQUIRED_TOKENS,
        issues,
    )
    if text:
        reject_tokens(
            text=text,
            path_name=RELEASING_GUIDE_NAME,
            tokens=RELEASING_FORBIDDEN_STATUS_LEDGER_TOKENS,
            message_template=(
                "release guide must route readiness artifacts to live-status owners instead of stale "
                "status-ledger negative wording '{token}'"
            ),
            issues=issues,
        )

    return issues
