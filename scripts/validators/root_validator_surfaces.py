"""Validator AGENTS surface role contracts."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue
from validators.root_common import require_tokens


VALIDATOR_SURFACE_ROLE_REQUIRED_TOKENS = (
    "## Applies to",
    "## Role",
    "root contract mesh",
    "authority class",
    "Part-local validators",
    "bounded proof posture",
    "precise failures",
    "tests/test_validate_repo.py",
)
VALIDATOR_TEST_SURFACE_ROLE_REQUIRED_TOKENS = (
    "## Applies to",
    "## Role",
    "root validator regression mesh",
    "scripts/validate_repo.py",
    "repository-wide invariant",
    "mechanic-owned tests",
    "incidental prose",
    "Expected-output pressure",
    "public-safe",
)
VALIDATOR_AGENT_SURFACE_STALE_ROUTE_PHRASES = (
    "## Guidance for `scripts/`",
    "## Guidance for `tests/`",
    "Validator changes must not weaken bounded proof posture",
    "Do not move a part-local test back",
    "Do not update expected outputs",
)


def validate_validator_surface_role(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    scripts_text = require_tokens(repo_root, "scripts/AGENTS.md", VALIDATOR_SURFACE_ROLE_REQUIRED_TOKENS, issues)
    tests_text = require_tokens(repo_root, "tests/AGENTS.md", VALIDATOR_TEST_SURFACE_ROLE_REQUIRED_TOKENS, issues)
    for path_name, text in (
        ("scripts/AGENTS.md", scripts_text),
        ("tests/AGENTS.md", tests_text),
    ):
        if not text:
            continue
        for stale_phrase in VALIDATOR_AGENT_SURFACE_STALE_ROUTE_PHRASES:
            if stale_phrase in text:
                issues.append(
                    ValidationIssue(
                        path_name,
                        "validator AGENTS cards should route pressure through owner maps "
                        "instead of stale negative scaffold "
                        f"'{stale_phrase}'",
                    )
                )

    return issues


__all__ = (
    "VALIDATOR_AGENT_SURFACE_STALE_ROUTE_PHRASES",
    "VALIDATOR_SURFACE_ROLE_REQUIRED_TOKENS",
    "VALIDATOR_TEST_SURFACE_ROLE_REQUIRED_TOKENS",
    "validate_validator_surface_role",
)
