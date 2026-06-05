"""Method-growth mechanic route and part-contract validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from validators import method_growth_route_paths as method_growth_paths
from validators import method_growth_route_tokens as method_growth_tokens
from validators.common import ValidationIssue


@dataclass(frozen=True)
class MethodGrowthRouteContext:
    require_tokens: Callable[..., str]
    provenance_tokens: Sequence[str]


def _require(
    context: MethodGrowthRouteContext,
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


def validate_method_growth_route_surfaces(
    repo_root: Path,
    *,
    context: MethodGrowthRouteContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name, tokens in (
        (
            method_growth_paths.METHOD_GROWTH_MECHANIC_README_NAME,
            method_growth_tokens.METHOD_GROWTH_MECHANIC_REQUIRED_TOKENS,
        ),
        (
            method_growth_paths.METHOD_GROWTH_MECHANIC_AGENTS_NAME,
            method_growth_tokens.METHOD_GROWTH_MECHANIC_AGENTS_REQUIRED_TOKENS,
        ),
        (
            method_growth_paths.METHOD_GROWTH_MECHANIC_PARTS_NAME,
            method_growth_tokens.METHOD_GROWTH_MECHANIC_PARTS_REQUIRED_TOKENS,
        ),
        (
            method_growth_paths.METHOD_GROWTH_CANDIDATE_LINEAGE_PART_README_NAME,
            method_growth_tokens.METHOD_GROWTH_CANDIDATE_LINEAGE_PART_REQUIRED_TOKENS,
        ),
        (
            method_growth_paths.METHOD_GROWTH_OWNER_LANDING_PART_README_NAME,
            method_growth_tokens.METHOD_GROWTH_OWNER_LANDING_PART_REQUIRED_TOKENS,
        ),
        (
            method_growth_paths.METHOD_GROWTH_MECHANIC_DECISION_NAME,
            method_growth_tokens.METHOD_GROWTH_MECHANIC_DECISION_REQUIRED_TOKENS,
        ),
        (
            method_growth_paths.METHOD_GROWTH_PART_OWNER_SPLIT_DECISION_NAME,
            method_growth_tokens.METHOD_GROWTH_PART_OWNER_SPLIT_DECISION_REQUIRED_TOKENS,
        ),
    ):
        _require(context, repo_root, path_name, tokens, issues)
    _require(
        context,
        repo_root,
        method_growth_paths.METHOD_GROWTH_MECHANIC_PROVENANCE_NAME,
        context.provenance_tokens,
        issues,
    )
    _require(
        context,
        repo_root,
        "docs/decisions/README.md",
        (
            method_growth_paths.METHOD_GROWTH_PART_OWNER_SPLIT_DECISION_NAME,
            "Method-growth Part Owner-split Contract",
        ),
        issues,
    )
    return issues


__all__ = (
    "MethodGrowthRouteContext",
    "validate_method_growth_route_surfaces",
)
