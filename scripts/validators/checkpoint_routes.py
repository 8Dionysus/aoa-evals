"""Checkpoint mechanic route and part-contract validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from validators import checkpoint_route_paths as checkpoint_paths
from validators import checkpoint_route_tokens as checkpoint_tokens
from validators.common import ValidationIssue


@dataclass(frozen=True)
class CheckpointRouteContext:
    require_tokens: Callable[..., str]
    provenance_tokens: Sequence[str]


def _require(
    context: CheckpointRouteContext,
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


def validate_checkpoint_route_surfaces(
    repo_root: Path,
    *,
    context: CheckpointRouteContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _require(
        context,
        repo_root,
        checkpoint_paths.CHECKPOINT_MECHANIC_README_NAME,
        checkpoint_tokens.CHECKPOINT_MECHANIC_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        checkpoint_paths.CHECKPOINT_MECHANIC_AGENTS_NAME,
        checkpoint_tokens.CHECKPOINT_MECHANIC_AGENTS_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        checkpoint_paths.CHECKPOINT_MECHANIC_PARTS_NAME,
        checkpoint_tokens.CHECKPOINT_MECHANIC_PARTS_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        checkpoint_paths.CHECKPOINT_A2A_PART_README_NAME,
        checkpoint_tokens.CHECKPOINT_A2A_PART_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        checkpoint_paths.CHECKPOINT_RESTARTABLE_INQUIRY_PART_README_NAME,
        checkpoint_tokens.CHECKPOINT_RESTARTABLE_INQUIRY_PART_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        checkpoint_paths.CHECKPOINT_SELF_AGENT_PART_README_NAME,
        checkpoint_tokens.CHECKPOINT_SELF_AGENT_PART_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        checkpoint_paths.CHECKPOINT_SELF_AGENT_POSTURE_DOC_NAME,
        checkpoint_tokens.CHECKPOINT_SELF_AGENT_POSTURE_DOC_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        checkpoint_paths.CHECKPOINT_MECHANIC_PROVENANCE_NAME,
        context.provenance_tokens,
        issues,
    )
    _require(
        context,
        repo_root,
        checkpoint_paths.CHECKPOINT_MECHANIC_DECISION_NAME,
        checkpoint_tokens.CHECKPOINT_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        checkpoint_paths.CHECKPOINT_PART_CONTRACT_GUARD_DECISION_NAME,
        checkpoint_tokens.CHECKPOINT_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        "docs/decisions/README.md",
        (
            checkpoint_paths.CHECKPOINT_PART_CONTRACT_GUARD_DECISION_NAME,
            "Checkpoint Part Contract Guard",
        ),
        issues,
    )
    return issues


__all__ = (
    "CheckpointRouteContext",
    "validate_checkpoint_route_surfaces",
)
