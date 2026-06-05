"""Root audit and GitHub route-card contracts."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue
from validators.root_common import require_tokens


GITHUB_AGENTS_NAME = ".github/AGENTS.md"
GITHUB_AGENTS_REQUIRED_TOKENS = (
    "## Operating Card",
    "GitHub platform route",
    "root `AGENTS.md` owns branch/PR/CI/merge",
    "Repo Validation",
    "## Boundary Routes",
    "CI-green pressure",
    "public-safe and deterministic",
)
GITHUB_AGENTS_STALE_ROUTE_PHRASES = (
    "Do not encode sibling-repo doctrine",
    "Do not add secrets",
    "Do not make CI green",
)
AUDIT_SURFACE_ROLE_REQUIRED_TOKENS = (
    "Audit Surface Map",
    "AGENTS.md#audit-and-review-route",
    "owns route law",
    "AGENTS.md#verify",
    "Route cards own the commands",
    "Route outward for:",
    "reusable technique truth: `aoa-techniques`",
    "execution workflow meaning: `aoa-skills`",
    "artifact-contract meaning",
    "sanitized evidence route",
)
AGENTS_AUDIT_ROUTE_REQUIRED_TOKENS = (
    "## Audit and review route",
    "`AUDIT.md` is the audit surface map",
    "approval gates",
    "Claim pressure routes",
    "generated reader, chooser doc, or index outranking source proof",
    "private dataset, secret-bearing fixture, hidden telemetry, or skipped validation",
    "Review severity",
    "P0",
    "P1",
    "report shape",
)
ROOT_AGENTS_STALE_NEGATIVE_ROUTE_PHRASES = (
    "Hard boundaries:",
    "bounded evals must not become total intelligence scores",
    "generated readers, chooser docs, and indexes must not outrank",
    "validation\n  that was not run must not be presented as public proof",
    "Do not use decisions as release notes",
)


def validate_audit_surface_role(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    require_tokens(repo_root, "AUDIT.md", AUDIT_SURFACE_ROLE_REQUIRED_TOKENS, issues)
    agents_text = require_tokens(repo_root, "AGENTS.md", AGENTS_AUDIT_ROUTE_REQUIRED_TOKENS, issues)
    if agents_text:
        for stale_phrase in ROOT_AGENTS_STALE_NEGATIVE_ROUTE_PHRASES:
            if stale_phrase in agents_text:
                issues.append(
                    ValidationIssue(
                        "AGENTS.md",
                        "root audit route should expose claim pressure routes "
                        "instead of stale negative boundary scaffold "
                        f"'{stale_phrase}'",
                    )
                )

    return issues


def validate_github_agent_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    text = require_tokens(repo_root, GITHUB_AGENTS_NAME, GITHUB_AGENTS_REQUIRED_TOKENS, issues)
    if text:
        for stale_phrase in GITHUB_AGENTS_STALE_ROUTE_PHRASES:
            if stale_phrase in text:
                issues.append(
                    ValidationIssue(
                        GITHUB_AGENTS_NAME,
                        ".github route card should use an operating card and boundary route table "
                        "instead of stale negative platform scaffold "
                        f"'{stale_phrase}'",
                    )
                )

    return issues


__all__ = (
    "AGENTS_AUDIT_ROUTE_REQUIRED_TOKENS",
    "AUDIT_SURFACE_ROLE_REQUIRED_TOKENS",
    "GITHUB_AGENTS_NAME",
    "GITHUB_AGENTS_REQUIRED_TOKENS",
    "GITHUB_AGENTS_STALE_ROUTE_PHRASES",
    "ROOT_AGENTS_STALE_NEGATIVE_ROUTE_PHRASES",
    "validate_audit_surface_role",
    "validate_github_agent_surface",
)
