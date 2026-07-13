"""Root proof-topology and roadmap topology posture checks."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue, read_text_or_issue
from validators.root_design_common import (
    PROOF_TOPOLOGY_NAME,
    ROADMAP_NAME,
    require_tokens,
)


PROOF_TOPOLOGY_REQUIRED_TOKENS = (
    "Convex topology",
    "source proof objects",
    "derived readers",
    "candidate evidence",
    "Memory evidence context",
    "Owner-local statistics",
    "receipts",
    "quest obligations",
    "decisions",
    "legacy lineage",
    "mechanic operations",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "Root Technical Districts",
    "| `stats/` | owner-local statistics port",
    "after mechanics movement",
    "additional root path becomes",
    "part-owned tests live under `mechanics/<mechanic>/parts/<part>/tests/`",
    "generated surfaces are companions",
    "candidate packets enter bundle-local review before verdict meaning",
    "quest records carry obligation return routes",
    "source truth stays with the source surface; decisions preserve route rationale",
    "source proof surfaces keep verdict meaning; guidance owns edit route and validation",
    "proof canon stays with source proof objects",
    "verdict meaning stays with reviewed reports and source bundles",
    "at least one living non-mechanics evidence route in addition to validator and rationale refs",
    "active topology starts at the current owner route",
    "A new `mechanics/` parent",
    "No remaining named candidate family is promoted by symmetry",
)
PROOF_TOPOLOGY_FORBIDDEN_STALE_MECHANIC_WORDING = (
    "mechanic-ready operations",
    "while Phase 4 maps the topology",
    "before mechanics growth starts from a root path",
    "A future `mechanics/` package",
    "It is not the roadmap",
    "The goal is not a decorative tree",
)
PROOF_TOPOLOGY_FORBIDDEN_ROUTE_SCAFFOLD = (
    "quests are obligations, not eval bundles",
    "package movement is not planned",
    "no active root examples payload should live here",
    "no active root reports payload should live here",
    "no active root config payload",
    "not proof canon",
    "without owning proof meaning",
    "not a verdict source",
    "a generic root validator file and a rationale-only decision ref are not enough",
    "without stealing their authority",
    "do not move the file yet",
    "are not historical memory",
    "should\nnot point",
    "should not look like",
    "no sibling authority transfer",
    "no empty package taxonomy",
)
PROOF_TOPOLOGY_DECISION_FORBIDDEN_STALE_MECHANIC_WORDING = (
    "mechanic-ready operations",
    "Keep physical movement deferred",
    "This decision does not create `mechanics/`.",
)
ROADMAP_FORBIDDEN_STALE_TOPOLOGY_WORDING = (
    "mechanic-ready artifact classes",
    "mechanics and legacy topology decision before any package creation or move",
    "runtime-evidence intake decision",
    "future mechanic packages",
)
PROOF_TOPOLOGY_DECISION_REQUIRED_TOKENS = (
    "docs/architecture/PROOF_TOPOLOGY.md",
    "mechanics",
    "source proof objects",
    "candidate evidence",
    "legacy lineage",
    "mechanic operations",
    "active `mechanics/` atlas",
)


def _require_proof_topology_tokens(repo_root: Path, issues: list[ValidationIssue]) -> str:
    text = read_text_or_issue(repo_root / PROOF_TOPOLOGY_NAME, issues, root=repo_root)
    if not text:
        return text
    for token in PROOF_TOPOLOGY_REQUIRED_TOKENS:
        if token not in text:
            issues.append(ValidationIssue(PROOF_TOPOLOGY_NAME, f"file must mention '{token}'"))
    return text


def validate_proof_topology_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    topology_text = _require_proof_topology_tokens(repo_root, issues)
    decision_text = require_tokens(
        repo_root,
        "docs/decisions/AOA-EV-D-0005-proof-topology-map.md",
        PROOF_TOPOLOGY_DECISION_REQUIRED_TOKENS,
        issues,
    )
    roadmap_text = require_tokens(
        repo_root,
        ROADMAP_NAME,
        (PROOF_TOPOLOGY_NAME, "Proof Topology Map"),
        issues,
    )
    if topology_text:
        for stale_phrase in PROOF_TOPOLOGY_FORBIDDEN_STALE_MECHANIC_WORDING:
            if stale_phrase in topology_text:
                issues.append(
                    ValidationIssue(
                        PROOF_TOPOLOGY_NAME,
                        f"proof topology must describe active mechanics, not stale preparatory wording '{stale_phrase}'",
                    )
                )
        for stale_phrase in PROOF_TOPOLOGY_FORBIDDEN_ROUTE_SCAFFOLD:
            if stale_phrase in topology_text:
                issues.append(
                    ValidationIssue(
                        PROOF_TOPOLOGY_NAME,
                        "proof topology should name owner routes before old "
                        f"negative scaffold '{stale_phrase}'",
                    )
                )
    if decision_text:
        for stale_phrase in PROOF_TOPOLOGY_DECISION_FORBIDDEN_STALE_MECHANIC_WORDING:
            if stale_phrase in decision_text:
                issues.append(
                    ValidationIssue(
                        "docs/decisions/AOA-EV-D-0005-proof-topology-map.md",
                        f"proof topology decision must describe the active mechanics atlas, not stale preparatory wording '{stale_phrase}'",
                    )
                )
    if roadmap_text:
        for stale_phrase in ROADMAP_FORBIDDEN_STALE_TOPOLOGY_WORDING:
            if stale_phrase in roadmap_text:
                issues.append(
                    ValidationIssue(
                        ROADMAP_NAME,
                        f"roadmap must describe active mechanics direction, not stale preparatory wording '{stale_phrase}'",
                    )
                )
    return issues


__all__ = (
    "ROADMAP_NAME",
    "PROOF_TOPOLOGY_NAME",
    "PROOF_TOPOLOGY_REQUIRED_TOKENS",
    "PROOF_TOPOLOGY_FORBIDDEN_STALE_MECHANIC_WORDING",
    "PROOF_TOPOLOGY_FORBIDDEN_ROUTE_SCAFFOLD",
    "PROOF_TOPOLOGY_DECISION_FORBIDDEN_STALE_MECHANIC_WORDING",
    "ROADMAP_FORBIDDEN_STALE_TOPOLOGY_WORDING",
    "PROOF_TOPOLOGY_DECISION_REQUIRED_TOKENS",
    "validate_proof_topology_surfaces",
)
