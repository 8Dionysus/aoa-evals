"""Agon mechanic route and part-contract validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from validators.common import ValidationIssue, read_text_or_issue


AGON_MECHANIC_README_NAME = "mechanics/agon/README.md"
AGON_MECHANIC_AGENTS_NAME = "mechanics/agon/AGENTS.md"
AGON_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0054-agon-part-contract-guard.md"
)

AGON_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "PARTS.md",
    "court-prebinding",
    "sophian-threshold-alignment",
    "part-local seed/config/docs",
    "observe-only recurrence hooks",
    "no_live_verdict",
    "bundle-local review",
    "python mechanics/agon/parts/court-prebinding/scripts/build_agon_eval_prebinding_registry.py --check",
    "python mechanics/agon/parts/court-prebinding/scripts/validate_agon_eval_prebindings.py",
    "python -m pytest -q mechanics/agon/parts/*/tests/test_agon*.py",
    "live verdict",
)
AGON_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "Agon proof-alignment loop",
    "part-local source config",
    "generated registry",
    "observe-only recurrence",
    "no_live_verdict",
    "bundle-local review",
)
AGON_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/agon/",
    "mechanics/agon/parts/",
    "seed prebindings",
    "part-local",
    "PARTS.md",
    "live verdict",
    "Tree of Sophia promotion",
)
AGON_PART_README_COMMON_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "generated",
    "validator",
)
AGON_PART_README_CONTRACTS = (
    (
        "mechanics/agon/parts/court-prebinding/README.md",
        AGON_PART_README_COMMON_REQUIRED_TOKENS
        + (
            "agon_eval_prebinding_registry.min.json",
            "no_live_verdict",
            "no_closure_grant",
        ),
    ),
    (
        "mechanics/agon/parts/ccs-alignment/README.md",
        AGON_PART_README_COMMON_REQUIRED_TOKENS
        + (
            "agon_ccs_eval_alignment_registry.min.json",
            "CCS law",
            "center law",
        ),
    ),
    (
        "mechanics/agon/parts/vds-alignment/README.md",
        AGON_PART_README_COMMON_REQUIRED_TOKENS
        + (
            "agon_vds_eval_alignment_registry.min.json",
            "no-live-verdict",
            "live verdict emission or acceptance pressure",
        ),
    ),
    (
        "mechanics/agon/parts/mechanical-trial-suites/README.md",
        AGON_PART_README_COMMON_REQUIRED_TOKENS
        + (
            "agon_mechanical_trial_eval_suite_registry.min.json",
            "candidate-only eval-suite",
            "arena run, live protocol, or trial execution pressure",
        ),
    ),
    (
        "mechanics/agon/parts/retention-rank-alignment/README.md",
        AGON_PART_README_COMMON_REQUIRED_TOKENS
        + (
            "agon_retention_rank_eval_alignment_registry.min.json",
            "retention execution",
            "no-mutation alignment evidence",
        ),
    ),
    (
        "mechanics/agon/parts/epistemic-alignment/README.md",
        AGON_PART_README_COMMON_REQUIRED_TOKENS
        + (
            "agon_epistemic_eval_alignment_registry.min.json",
            "doctrine rewrite",
            "owner-truth takeover",
        ),
    ),
    (
        "mechanics/agon/parts/slc-alignment/README.md",
        AGON_PART_README_COMMON_REQUIRED_TOKENS
        + (
            "agon_slc_eval_alignment_registry.min.json",
            "schools, lineages, and campaigns",
            "non-canon alignment",
        ),
    ),
    (
        "mechanics/agon/parts/kag-alignment/README.md",
        AGON_PART_README_COMMON_REQUIRED_TOKENS
        + (
            "agon_kag_eval_alignment_registry.min.json",
            "KAG canon",
            "KAG candidate promotion",
        ),
    ),
    (
        "mechanics/agon/parts/sophian-threshold-alignment/README.md",
        AGON_PART_README_COMMON_REQUIRED_TOKENS
        + (
            "agon_sophian_eval_alignment_registry.min.json",
            "Tree of Sophia canon",
            "Tree of Sophia canon write",
        ),
    ),
)
AGON_PART_README_STALE_STOP_LINE_PHRASES = (
    "Do not grant live verdict",
    "Do not weaken `no_live_verdict`",
    "Do not treat generated prebindings as court law",
    "Do not rewrite center law",
    "Do not issue live verdicts",
    "Do not let local registry output outrank",
    "Do not emit or accept a live verdict",
    "Do not turn verdict draft status",
    "Do not let generated draft-status records outrank",
    "Do not run an arena",
    "Do not issue verdicts",
    "Do not use candidate eval-suite output as proof",
    "Do not mutate rank",
    "Do not treat eval alignment as promotion",
    "Do not let generated rank-pressure records outrank",
    "Do not rewrite doctrine",
    "Do not issue live verdict",
    "Do not let generated epistemic records outrank",
    "Do not canonize",
    "Do not treat SLC alignment as owner acceptance",
    "Do not promote a KAG candidate",
    "Do not use generated KAG alignment records as proof",
    "Do not write Tree of Sophia canon",
    "Do not transfer canon authority",
)
AGON_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS = (
    "Agon Part Contract Guard",
    "mechanics/agon/parts/court-prebinding/README.md",
    "mechanics/agon/parts/sophian-threshold-alignment/README.md",
    "part-level contracts",
    "no new Agon parent",
    "stronger owner split",
    "stop-lines",
    "python scripts/validate_repo.py",
)


@dataclass(frozen=True)
class AgonRouteContext:
    require_tokens: Callable[..., str]


def _require(
    context: AgonRouteContext,
    repo_root: Path,
    path_name: str,
    tokens: Sequence[str],
    issues: list[ValidationIssue],
) -> str:
    return context.require_tokens(
        repo_root=repo_root,
        path_name=path_name,
        tokens=tokens,
        issues=issues,
    )


def validate_agon_route_surfaces(
    repo_root: Path,
    *,
    context: AgonRouteContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _require(context, repo_root, AGON_MECHANIC_README_NAME, AGON_MECHANIC_REQUIRED_TOKENS, issues)
    _require(context, repo_root, AGON_MECHANIC_AGENTS_NAME, AGON_MECHANIC_AGENTS_REQUIRED_TOKENS, issues)
    _require(
        context,
        repo_root,
        "docs/decisions/AOA-EV-D-0016-agon-mechanic-package.md",
        AGON_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues,
    )
    for path_name, tokens in AGON_PART_README_CONTRACTS:
        _require(context, repo_root, path_name, tokens, issues)
        readme_text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
        for stale_phrase in AGON_PART_README_STALE_STOP_LINE_PHRASES:
            if readme_text and stale_phrase in readme_text:
                issues.append(
                    ValidationIssue(
                        path_name,
                        "Agon part README Stop-Lines must route pressure through owner tables instead of stale imperative stop-line phrasing",
                    )
                )
    _require(
        context,
        repo_root,
        AGON_PART_CONTRACT_GUARD_DECISION_NAME,
        AGON_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        "docs/decisions/README.md",
        (AGON_PART_CONTRACT_GUARD_DECISION_NAME, "Agon Part Contract Guard"),
        issues,
    )
    return issues
