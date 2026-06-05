"""Titan seed-boundary route validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from validators import titan_route_paths as titan_paths
from validators import titan_route_tokens as titan_tokens
from validators.common import ValidationIssue, read_text_or_issue


@dataclass(frozen=True)
class TitanRouteContext:
    require_tokens: Callable[..., str]


def _require(
    context: TitanRouteContext,
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


def validate_titan_route_surfaces(
    repo_root: Path,
    *,
    context: TitanRouteContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _require(
        context,
        repo_root,
        titan_paths.TITAN_MECHANIC_README_NAME,
        titan_tokens.TITAN_MECHANIC_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        titan_paths.TITAN_MECHANIC_AGENTS_NAME,
        titan_tokens.TITAN_MECHANIC_AGENTS_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        titan_paths.TITAN_MECHANIC_DIRECTION_NAME,
        titan_tokens.TITAN_MECHANIC_DIRECTION_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        "docs/decisions/AOA-EV-D-0015-titan-mechanic-package.md",
        titan_tokens.TITAN_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        titan_paths.TITAN_INCARNATION_CANARIES_NAME,
        titan_tokens.TITAN_INCARNATION_CANARIES_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        titan_paths.TITAN_SUMMON_DISCIPLINE_CANARIES_NAME,
        titan_tokens.TITAN_SUMMON_DISCIPLINE_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        titan_paths.TITAN_SEED_BOUNDARY_SEEDS_AGENTS_NAME,
        titan_tokens.TITAN_SEED_BOUNDARY_SEEDS_AGENTS_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        titan_paths.TITAN_SEED_BOUNDARY_SEEDS_README_NAME,
        titan_tokens.TITAN_SEED_BOUNDARY_SEEDS_README_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        titan_paths.TITAN_PARTS_INDEX_README_NAME,
        titan_tokens.TITAN_PARTS_INDEX_README_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        titan_paths.TITAN_SEED_BOUNDARY_PART_README_NAME,
        titan_tokens.TITAN_SEED_BOUNDARY_PART_README_REQUIRED_TOKENS,
        issues,
    )
    for path_name in titan_paths.TITAN_SEED_BOUNDARY_ROUTE_SURFACE_NAMES:
        route_text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
        for stale_phrase in titan_tokens.TITAN_SEED_BOUNDARY_STALE_ROUTE_PHRASES:
            if route_text and stale_phrase in route_text:
                issues.append(
                    ValidationIssue(
                        path_name,
                        "Titan seed-boundary route surfaces must route pressure through owner maps instead of stale negative claim-limit phrasing",
                    )
                )
    _require(
        context,
        repo_root,
        titan_paths.TITAN_SEED_BOUNDARY_CONTRACT_DECISION_NAME,
        titan_tokens.TITAN_SEED_BOUNDARY_CONTRACT_DECISION_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        "docs/decisions/README.md",
        (
            titan_paths.TITAN_SEED_BOUNDARY_CONTRACT_DECISION_NAME,
            "Titan Seed-boundary Contract",
        ),
        issues,
    )
    return issues


__all__ = (
    "TitanRouteContext",
    "validate_titan_route_surfaces",
)
