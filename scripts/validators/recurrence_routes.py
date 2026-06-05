"""Recurrence mechanic route validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from validators import recurrence_route_paths as recurrence_paths
from validators import recurrence_route_tokens as recurrence_tokens
from validators.common import ValidationIssue


@dataclass(frozen=True)
class RecurrenceRouteContext:
    require_tokens: Callable[..., str]
    provenance_tokens: Sequence[str]


def _require(
    context: RecurrenceRouteContext,
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


def validate_recurrence_route_surfaces(
    repo_root: Path,
    *,
    context: RecurrenceRouteContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _require(context, repo_root, recurrence_paths.RECURRENCE_MECHANIC_README_NAME, recurrence_tokens.RECURRENCE_MECHANIC_REQUIRED_TOKENS, issues)
    _require(context, repo_root, recurrence_paths.RECURRENCE_MECHANIC_AGENTS_NAME, recurrence_tokens.RECURRENCE_MECHANIC_AGENTS_REQUIRED_TOKENS, issues)
    _require(context, repo_root, recurrence_paths.RECURRENCE_MECHANIC_PARTS_NAME, recurrence_tokens.RECURRENCE_MECHANIC_PARTS_REQUIRED_TOKENS, issues)
    _require(context, repo_root, recurrence_paths.RECURRENCE_CONTROL_PLANE_PART_README_NAME, recurrence_tokens.RECURRENCE_CONTROL_PLANE_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, recurrence_paths.RECURRENCE_ANCHOR_RETURN_PART_README_NAME, recurrence_tokens.RECURRENCE_ANCHOR_RETURN_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, recurrence_paths.RECURRENCE_MEMORY_RECALL_PART_README_NAME, recurrence_tokens.RECURRENCE_MEMORY_RECALL_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, recurrence_paths.RECURRENCE_RECURSOR_BOUNDARY_PART_README_NAME, recurrence_tokens.RECURRENCE_RECURSOR_BOUNDARY_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, recurrence_paths.RECURRENCE_STATS_REGROUNDING_PART_README_NAME, recurrence_tokens.RECURRENCE_STATS_REGROUNDING_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, recurrence_paths.RECURRENCE_PORTABLE_PROOF_BEACONS_PART_README_NAME, recurrence_tokens.RECURRENCE_PORTABLE_PROOF_BEACONS_PART_REQUIRED_TOKENS, issues)
    portable_proof_beacons_agents_text = _require(
        context,
        repo_root,
        recurrence_paths.RECURRENCE_PORTABLE_PROOF_BEACONS_PART_AGENTS_NAME,
        recurrence_tokens.RECURRENCE_PORTABLE_PROOF_BEACONS_PART_AGENTS_REQUIRED_TOKENS,
        issues,
    )
    if portable_proof_beacons_agents_text:
        for stale_phrase in recurrence_tokens.RECURRENCE_PORTABLE_PROOF_BEACONS_PART_AGENTS_STALE_ROUTE_PHRASES:
            if stale_phrase in portable_proof_beacons_agents_text:
                issues.append(
                    ValidationIssue(
                        recurrence_paths.RECURRENCE_PORTABLE_PROOF_BEACONS_PART_AGENTS_NAME,
                        "recurrence portable-proof-beacons AGENTS card should use an operating card and owner route table instead of stale negative scaffold "
                        f"'{stale_phrase}'",
                    )
                )
    _require(context, repo_root, recurrence_paths.RECURRENCE_MECHANIC_PROVENANCE_NAME, context.provenance_tokens, issues)
    _require(context, repo_root, recurrence_paths.RECURRENCE_MECHANIC_DECISION_NAME, recurrence_tokens.RECURRENCE_MECHANIC_DECISION_REQUIRED_TOKENS, issues)
    _require(context, repo_root, recurrence_paths.RECURRENCE_SUPPORT_PARTS_DECISION_NAME, recurrence_tokens.RECURRENCE_SUPPORT_PARTS_DECISION_REQUIRED_TOKENS, issues)
    _require(context, repo_root, recurrence_paths.RECURRENCE_PORTABLE_PROOF_BEACONS_DECISION_NAME, recurrence_tokens.RECURRENCE_PORTABLE_PROOF_BEACONS_DECISION_REQUIRED_TOKENS, issues)
    _require(context, repo_root, recurrence_paths.RECURRENCE_CONTROL_PLANE_CONTRACT_DECISION_NAME, recurrence_tokens.RECURRENCE_CONTROL_PLANE_CONTRACT_DECISION_REQUIRED_TOKENS, issues)
    _require(
        context,
        repo_root,
        "docs/decisions/README.md",
        (
            recurrence_paths.RECURRENCE_CONTROL_PLANE_CONTRACT_DECISION_NAME,
            "Recurrence Control-plane Contract",
        ),
        issues,
    )
    return issues


__all__ = (
    "RecurrenceRouteContext",
    "validate_recurrence_route_surfaces",
)
