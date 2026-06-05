"""Mechanic parent registry and class-map contracts."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue, read_text_or_issue
from validators.mechanics_common import (
    MECHANICS_EVIDENCE_CLUSTERS_NAME,
    MECHANICS_README_NAME,
    PROOF_TOPOLOGY_NAME,
    ROADMAP_MECHANICS_EVIDENCE_DIRECTION_TOKENS,
    ROADMAP_NAME,
    _markdown_heading_section,
    _require_tokens,
)


ACTIVE_MECHANIC_PARENT_NAMES = (
    "agon",
    "antifragility",
    "audit",
    "boundary-bridge",
    "checkpoint",
    "comparison-spine",
    "distillation",
    "experience",
    "growth-cycle",
    "method-growth",
    "proof-infra",
    "proof-loop",
    "proof-object",
    "publication-receipts",
    "questbook",
    "recurrence",
    "release-support",
    "rpg",
    "titan",
)
AOA_ALIGNED_MECHANIC_PARENT_NAMES = (
    "agon",
    "antifragility",
    "audit",
    "boundary-bridge",
    "checkpoint",
    "distillation",
    "experience",
    "growth-cycle",
    "method-growth",
    "questbook",
    "recurrence",
    "release-support",
    "rpg",
)
EVALS_NATIVE_MECHANIC_PARENT_NAMES = (
    "comparison-spine",
    "proof-infra",
    "proof-loop",
    "proof-object",
    "publication-receipts",
    "titan",
)
FORMER_WRONG_MECHANIC_PARENT_ROUTES = (
    ("agon-proof", "agon"),
    ("titan-canaries", "titan"),
    ("proof-release", "release-support"),
    ("runtime-evidence", "audit"),
    ("sibling-proof-refs", "boundary-bridge"),
    ("repair", "antifragility/repair-proof"),
)

MECHANIC_PARENT_CLASS_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0072-mechanic-parent-class-contract.md"
)
MECHANIC_PARENT_CLASS_DECISION_REQUIRED_TOKENS = (
    "Mechanic Parent Class Contract",
    "AoA-aligned mechanics",
    "evals-native mechanics",
    "owner-named evals-native",
    "aoa-agents` keeps Titan role, bearer, summon, and incarnation law",
    "every AoA-aligned parent appears in the AoA-aligned table",
    "owner-named evals-native parents state the stronger owner split",
    "the two class sets are disjoint",
    "former wrong parent forms",
    "`agon-proof`",
    "`titan-canaries`",
    "`proof-release`",
    "`runtime-evidence`",
    "`sibling-proof-refs`",
    "`repair`",
    "python -m pytest -q tests/test_mechanic_evidence_ledger.py -k mechanic_parent_class",
)


def validate_mechanic_parent_class_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    active_parents = set(ACTIVE_MECHANIC_PARENT_NAMES)
    aoa_parents = set(AOA_ALIGNED_MECHANIC_PARENT_NAMES)
    evals_native_parents = set(EVALS_NATIVE_MECHANIC_PARENT_NAMES)

    overlap = sorted(aoa_parents & evals_native_parents)
    if overlap:
        issues.append(
            ValidationIssue(
                "scripts/validators/mechanic_parent_registry.py",
                "mechanic parent class sets must be disjoint: " + ", ".join(overlap),
            )
        )

    missing = sorted(active_parents - (aoa_parents | evals_native_parents))
    extra = sorted((aoa_parents | evals_native_parents) - active_parents)
    if missing:
        issues.append(
            ValidationIssue(
                "scripts/validators/mechanic_parent_registry.py",
                "active mechanic parents missing from class sets: " + ", ".join(missing),
            )
        )
    if extra:
        issues.append(
            ValidationIssue(
                "scripts/validators/mechanic_parent_registry.py",
                "mechanic class sets contain non-active parents: " + ", ".join(extra),
            )
        )

    text = read_text_or_issue(repo_root / MECHANICS_EVIDENCE_CLUSTERS_NAME, issues, root=repo_root)
    if not text:
        return issues
    if "currently plausible" in text:
        issues.append(
            ValidationIssue(
                MECHANICS_EVIDENCE_CLUSTERS_NAME,
                "active mechanic parents must be described as active allowlisted parents, not merely plausible candidates",
            )
        )
    for token in ("owner-named evals-native", "`aoa-agents` keeps stronger Titan law"):
        if token not in text:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"mechanics evidence cluster map must mention {token!r}",
                )
            )

    aoa_section = _markdown_heading_section(text, "AoA-aligned parents")
    evals_native_section = _markdown_heading_section(text, "Evals-native parents")
    wrong_parent_section = _markdown_heading_section(text, "Former Wrong Parent Forms")
    for section_name, section_text in (
        ("AoA-aligned parents", aoa_section),
        ("Evals-native parents", evals_native_section),
        ("Former Wrong Parent Forms", wrong_parent_section),
    ):
        if not section_text:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"mechanics evidence cluster map must contain section {section_name!r}",
                )
            )

    for parent_name in AOA_ALIGNED_MECHANIC_PARENT_NAMES:
        row_token = f"| `{parent_name}` |"
        if row_token not in aoa_section:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"AoA-aligned parent `{parent_name}` must appear in the AoA-aligned table",
                )
            )
        if row_token in evals_native_section:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"AoA-aligned parent `{parent_name}` must not appear in the evals-native table",
                )
            )

    for parent_name in EVALS_NATIVE_MECHANIC_PARENT_NAMES:
        row_token = f"| `{parent_name}` |"
        if row_token not in evals_native_section:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"evals-native parent `{parent_name}` must appear in the evals-native table",
                )
            )
        if row_token in aoa_section:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"evals-native parent `{parent_name}` must not appear in the AoA-aligned table",
                )
            )

    for wrong_parent, correct_route in FORMER_WRONG_MECHANIC_PARENT_ROUTES:
        row_token = f"| `{wrong_parent}` | `{correct_route}` |"
        if row_token not in wrong_parent_section:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"former wrong parent `{wrong_parent}` must map to `{correct_route}`",
                )
            )

    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PARENT_CLASS_DECISION_NAME,
        tokens=MECHANIC_PARENT_CLASS_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=(
            "owner-named evals-native",
            "Concrete wrong-parent mappings live in",
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=(
            "owner-named evals-native",
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANICS_EVIDENCE_DIRECTION_TOKENS,
        issues=issues,
    )
    return issues


__all__ = (
    "ACTIVE_MECHANIC_PARENT_NAMES",
    "AOA_ALIGNED_MECHANIC_PARENT_NAMES",
    "EVALS_NATIVE_MECHANIC_PARENT_NAMES",
    "FORMER_WRONG_MECHANIC_PARENT_ROUTES",
    "MECHANIC_PARENT_CLASS_DECISION_NAME",
    "MECHANIC_PARENT_CLASS_DECISION_REQUIRED_TOKENS",
    "validate_mechanic_parent_class_surfaces",
)
