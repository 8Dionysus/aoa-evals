"""Distillation mechanic route and part-contract validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from validators import distillation_route_paths as distillation_paths
from validators import distillation_route_tokens as distillation_tokens
from validators.common import ValidationIssue


@dataclass(frozen=True)
class DistillationRouteContext:
    require_tokens: Callable[..., str]
    provenance_tokens: Sequence[str]


def _require(
    context: DistillationRouteContext,
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


def validate_distillation_route_surfaces(
    repo_root: Path,
    *,
    context: DistillationRouteContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name, tokens in (
        (
            distillation_paths.DISTILLATION_MECHANIC_README_NAME,
            distillation_tokens.DISTILLATION_MECHANIC_REQUIRED_TOKENS,
        ),
        (
            distillation_paths.DISTILLATION_MECHANIC_DIRECTION_NAME,
            distillation_tokens.DISTILLATION_MECHANIC_DIRECTION_REQUIRED_TOKENS,
        ),
        (
            distillation_paths.DISTILLATION_MECHANIC_AGENTS_NAME,
            distillation_tokens.DISTILLATION_MECHANIC_AGENTS_REQUIRED_TOKENS,
        ),
        (
            distillation_paths.DISTILLATION_MECHANIC_PARTS_NAME,
            distillation_tokens.DISTILLATION_MECHANIC_PARTS_REQUIRED_TOKENS,
        ),
        (
            distillation_paths.DISTILLATION_COMPOST_PROVENANCE_PART_README_NAME,
            distillation_tokens.DISTILLATION_COMPOST_PROVENANCE_PART_REQUIRED_TOKENS,
        ),
        (
            distillation_paths.DISTILLATION_RUNTIME_CANDIDATE_ADOPTION_PART_README_NAME,
            distillation_tokens.DISTILLATION_RUNTIME_CANDIDATE_ADOPTION_PART_REQUIRED_TOKENS,
        ),
        (
            distillation_paths.DISTILLATION_MECHANIC_DECISION_NAME,
            distillation_tokens.DISTILLATION_MECHANIC_DECISION_REQUIRED_TOKENS,
        ),
        (
            distillation_paths.DISTILLATION_PART_CONTRACT_GUARD_DECISION_NAME,
            distillation_tokens.DISTILLATION_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS,
        ),
    ):
        _require(context, repo_root, path_name, tokens, issues)
    _require(
        context,
        repo_root,
        distillation_paths.DISTILLATION_MECHANIC_PROVENANCE_NAME,
        context.provenance_tokens,
        issues,
    )
    _require(
        context,
        repo_root,
        "docs/decisions/README.md",
        (
            distillation_paths.DISTILLATION_PART_CONTRACT_GUARD_DECISION_NAME,
            "Distillation Part Contract Guard",
        ),
        issues,
    )
    return issues


__all__ = (
    "DistillationRouteContext",
    "validate_distillation_route_surfaces",
)
