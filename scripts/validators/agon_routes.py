"""Agon mechanic route and part-contract validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from validators import agon_route_paths as agon_paths
from validators import agon_route_tokens as agon_tokens
from validators.common import ValidationIssue, read_text_or_issue


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
    _require(
        context,
        repo_root,
        agon_paths.AGON_MECHANIC_README_NAME,
        agon_tokens.AGON_MECHANIC_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        agon_paths.AGON_MECHANIC_AGENTS_NAME,
        agon_tokens.AGON_MECHANIC_AGENTS_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        agon_paths.AGON_MECHANIC_DECISION_NAME,
        agon_tokens.AGON_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues,
    )
    for path_name, tokens in agon_tokens.AGON_PART_README_CONTRACTS:
        _require(context, repo_root, path_name, tokens, issues)
        readme_text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
        for stale_phrase in agon_tokens.AGON_PART_README_STALE_STOP_LINE_PHRASES:
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
        agon_paths.AGON_PART_CONTRACT_GUARD_DECISION_NAME,
        agon_tokens.AGON_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        "docs/decisions/README.md",
        (agon_paths.AGON_PART_CONTRACT_GUARD_DECISION_NAME, "Agon Part Contract Guard"),
        issues,
    )
    return issues


__all__ = (
    "AgonRouteContext",
    "validate_agon_route_surfaces",
)
