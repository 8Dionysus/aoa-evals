"""RPG mechanic route and progression-unlock validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from validators import rpg_route_paths as rpg_paths
from validators import rpg_route_tokens as rpg_tokens
from validators.common import ValidationIssue


@dataclass(frozen=True)
class RpgRouteContext:
    require_tokens: Callable[..., str]
    provenance_tokens: Sequence[str]


def _require(
    context: RpgRouteContext,
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


def validate_rpg_route_surfaces(
    repo_root: Path,
    *,
    context: RpgRouteContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name, tokens in (
        (
            rpg_paths.RPG_MECHANIC_README_NAME,
            rpg_tokens.RPG_MECHANIC_REQUIRED_TOKENS,
        ),
        (
            rpg_paths.RPG_MECHANIC_AGENTS_NAME,
            rpg_tokens.RPG_MECHANIC_AGENTS_REQUIRED_TOKENS,
        ),
        (
            rpg_paths.RPG_MECHANIC_PARTS_NAME,
            rpg_tokens.RPG_MECHANIC_PARTS_REQUIRED_TOKENS,
        ),
        (
            rpg_paths.RPG_PROGRESS_UNLOCKS_PART_README_NAME,
            rpg_tokens.RPG_PROGRESS_UNLOCKS_PART_REQUIRED_TOKENS,
        ),
        (
            rpg_paths.RPG_MECHANIC_DECISION_NAME,
            rpg_tokens.RPG_MECHANIC_DECISION_REQUIRED_TOKENS,
        ),
        (
            rpg_paths.RPG_PROGRESS_UNLOCKS_CONTRACT_DECISION_NAME,
            rpg_tokens.RPG_PROGRESS_UNLOCKS_CONTRACT_DECISION_REQUIRED_TOKENS,
        ),
    ):
        _require(context, repo_root, path_name, tokens, issues)
    _require(
        context,
        repo_root,
        rpg_paths.RPG_MECHANIC_PROVENANCE_NAME,
        context.provenance_tokens,
        issues,
    )
    _require(
        context,
        repo_root,
        "docs/decisions/README.md",
        (
            rpg_paths.RPG_PROGRESS_UNLOCKS_CONTRACT_DECISION_NAME,
            "RPG Progression-unlocks Contract",
        ),
        issues,
    )
    return issues


__all__ = (
    "RpgRouteContext",
    "validate_rpg_route_surfaces",
)
