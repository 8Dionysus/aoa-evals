"""Growth-cycle mechanic route and diagnosis-gate validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from validators import growth_cycle_route_paths as growth_cycle_paths
from validators import growth_cycle_route_tokens as growth_cycle_tokens
from validators.common import ValidationIssue


@dataclass(frozen=True)
class GrowthCycleRouteContext:
    require_tokens: Callable[..., str]
    provenance_tokens: Sequence[str]


def _require(
    context: GrowthCycleRouteContext,
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


def validate_growth_cycle_route_surfaces(
    repo_root: Path,
    *,
    context: GrowthCycleRouteContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name, tokens in (
        (
            growth_cycle_paths.GROWTH_CYCLE_MECHANIC_README_NAME,
            growth_cycle_tokens.GROWTH_CYCLE_MECHANIC_REQUIRED_TOKENS,
        ),
        (
            growth_cycle_paths.GROWTH_CYCLE_MECHANIC_AGENTS_NAME,
            growth_cycle_tokens.GROWTH_CYCLE_MECHANIC_AGENTS_REQUIRED_TOKENS,
        ),
        (
            growth_cycle_paths.GROWTH_CYCLE_MECHANIC_PARTS_NAME,
            growth_cycle_tokens.GROWTH_CYCLE_MECHANIC_PARTS_REQUIRED_TOKENS,
        ),
        (
            growth_cycle_paths.GROWTH_CYCLE_PARTS_README_NAME,
            growth_cycle_tokens.GROWTH_CYCLE_PARTS_README_REQUIRED_TOKENS,
        ),
        (
            growth_cycle_paths.GROWTH_CYCLE_DIAGNOSIS_GATE_PART_README_NAME,
            growth_cycle_tokens.GROWTH_CYCLE_DIAGNOSIS_GATE_PART_REQUIRED_TOKENS,
        ),
        (
            growth_cycle_paths.GROWTH_CYCLE_MECHANIC_DECISION_NAME,
            growth_cycle_tokens.GROWTH_CYCLE_MECHANIC_DECISION_REQUIRED_TOKENS,
        ),
        (
            growth_cycle_paths.GROWTH_CYCLE_DIAGNOSIS_GATE_CONTRACT_DECISION_NAME,
            growth_cycle_tokens.GROWTH_CYCLE_DIAGNOSIS_GATE_CONTRACT_DECISION_REQUIRED_TOKENS,
        ),
        (
            growth_cycle_paths.REPAIR_DIAGNOSIS_ROUTE_BOUNDARY_DECISION_NAME,
            growth_cycle_tokens.REPAIR_DIAGNOSIS_ROUTE_BOUNDARY_DECISION_REQUIRED_TOKENS,
        ),
    ):
        _require(context, repo_root, path_name, tokens, issues)
    _require(
        context,
        repo_root,
        growth_cycle_paths.GROWTH_CYCLE_MECHANIC_PROVENANCE_NAME,
        context.provenance_tokens,
        issues,
    )
    for decision_name, decision_title in (
        (
            growth_cycle_paths.GROWTH_CYCLE_DIAGNOSIS_GATE_CONTRACT_DECISION_NAME,
            "Growth-cycle Diagnosis-gate Contract",
        ),
        (
            growth_cycle_paths.REPAIR_DIAGNOSIS_ROUTE_BOUNDARY_DECISION_NAME,
            "Repair Diagnosis Route Boundary",
        ),
    ):
        _require(
            context,
            repo_root,
            "docs/decisions/README.md",
            (decision_name, decision_title),
            issues,
        )
    return issues


__all__ = (
    "GrowthCycleRouteContext",
    "validate_growth_cycle_route_surfaces",
)
