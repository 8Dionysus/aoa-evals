"""Closeout ingress and contribution route validation."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue
from validators.root_guidance_common import reject_tokens, require_tokens

CLOSEOUT_WRITEBACK_INGRESS_NAME = "docs/operations/REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md"
CLOSEOUT_WRITEBACK_INGRESS_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0045-closeout-writeback-ingress-boundary.md"
)
CLOSEOUT_WRITEBACK_INGRESS_REQUIRED_TOKENS = (
    "traceable proof ingress",
    "owner-local re-read anchor",
    "bundle remains the source surface",
    "workflow meaning routes to `aoa-skills`",
    "neighboring proof context",
    "bundle truth stays",
    "new-bundle authority deferred",
)
CLOSEOUT_WRITEBACK_INGRESS_FORBIDDEN_ROUTE_SCAFFOLD = (
    "instead of leaving it as closeout residue or chat memory",
    "rather than as a second source of truth",
    "should not absorb this proof lane",
    "not a rewording of the already-landed recall",
    "not a shadow copy",
    "still does not name a new bundle",
)
CLOSEOUT_WRITEBACK_INGRESS_DECISION_REQUIRED_TOKENS = (
    "Closeout Writeback Ingress Boundary",
    "owner-local ingress anchor",
    "root ingress",
    "reviewed-candidate adoption",
    "Current Applicability",
    "Review Log",
    "owner-local re-read anchor",
    "traceable proof ingress",
)

CONTRIBUTING_ROUTE_REQUIRED_TOKENS = (
    "Operating Card",
    "public contribution route",
    "AGENTS.md` owns agent workflow",
    "validation evidence",
    "security handoff",
    "outputs that preserve claim limits",
    "fixtures and scoring expose public setup",
    "Canonical promotion needs evidence",
    "Hidden intuition routes to a written judgment rule",
    "A good eval bundle proves one bounded thing honestly",
)
CONTRIBUTING_FORBIDDEN_ROUTE_SCAFFOLD = (
    "outputs that do not overstate what was learned",
    "fixtures and scoring do not depend on hidden local assumptions",
    "Do not mark an eval `canonical`",
    "what does the eval still fail to prove?",
    "If the answer depends on hidden intuition, the bundle is not ready.",
    "do not open a public issue or PR",
    "A good eval bundle does not try to prove everything.",
)


def validate_closeout_writeback_ingress_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    ingress_text = require_tokens(
        repo_root,
        CLOSEOUT_WRITEBACK_INGRESS_NAME,
        CLOSEOUT_WRITEBACK_INGRESS_REQUIRED_TOKENS,
        issues,
    )
    if ingress_text:
        reject_tokens(
            text=ingress_text,
            path_name=CLOSEOUT_WRITEBACK_INGRESS_NAME,
            tokens=CLOSEOUT_WRITEBACK_INGRESS_FORBIDDEN_ROUTE_SCAFFOLD,
            message_template="closeout writeback ingress should name the active re-read route instead of stale scaffold '{token}'",
            issues=issues,
        )
    require_tokens(
        repo_root,
        CLOSEOUT_WRITEBACK_INGRESS_DECISION_NAME,
        CLOSEOUT_WRITEBACK_INGRESS_DECISION_REQUIRED_TOKENS,
        issues,
    )
    return issues


def validate_contributing_route_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    contributing_text = require_tokens(
        repo_root,
        "CONTRIBUTING.md",
        CONTRIBUTING_ROUTE_REQUIRED_TOKENS,
        issues,
    )
    if contributing_text:
        reject_tokens(
            text=contributing_text,
            path_name="CONTRIBUTING.md",
            tokens=CONTRIBUTING_FORBIDDEN_ROUTE_SCAFFOLD,
            message_template="contributing guide should name owner routes and proof criteria instead of stale scaffold '{token}'",
            issues=issues,
        )
    return issues
