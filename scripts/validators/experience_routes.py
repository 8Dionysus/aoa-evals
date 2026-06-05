"""Experience mechanic route and part-contract validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from validators import experience_route_paths as experience_paths
from validators import experience_route_tokens as experience_tokens
from validators.common import ValidationIssue


@dataclass(frozen=True)
class ExperienceRouteContext:
    require_tokens: Callable[..., str]
    provenance_tokens: Sequence[str]


def _require(
    context: ExperienceRouteContext,
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


def validate_experience_route_surfaces(
    repo_root: Path,
    *,
    context: ExperienceRouteContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name, tokens in (
        (
            experience_paths.EXPERIENCE_MECHANIC_README_NAME,
            experience_tokens.EXPERIENCE_MECHANIC_REQUIRED_TOKENS,
        ),
        (
            experience_paths.EXPERIENCE_MECHANIC_AGENTS_NAME,
            experience_tokens.EXPERIENCE_MECHANIC_AGENTS_REQUIRED_TOKENS,
        ),
        (
            experience_paths.EXPERIENCE_MECHANIC_PARTS_NAME,
            experience_tokens.EXPERIENCE_MECHANIC_PARTS_REQUIRED_TOKENS,
        ),
        (
            experience_paths.EXPERIENCE_PROTOCOL_PART_README_NAME,
            experience_tokens.EXPERIENCE_PROTOCOL_PART_REQUIRED_TOKENS,
        ),
        (
            experience_paths.EXPERIENCE_CERTIFICATION_PART_README_NAME,
            experience_tokens.EXPERIENCE_CERTIFICATION_PART_REQUIRED_TOKENS,
        ),
        (
            experience_paths.EXPERIENCE_ADOPTION_PART_README_NAME,
            experience_tokens.EXPERIENCE_ADOPTION_PART_REQUIRED_TOKENS,
        ),
        (
            experience_paths.EXPERIENCE_GOVERNANCE_PART_README_NAME,
            experience_tokens.EXPERIENCE_GOVERNANCE_PART_REQUIRED_TOKENS,
        ),
        (
            experience_paths.EXPERIENCE_OFFICE_PART_README_NAME,
            experience_tokens.EXPERIENCE_OFFICE_PART_REQUIRED_TOKENS,
        ),
        (
            experience_paths.EXPERIENCE_MECHANIC_DECISION_NAME,
            experience_tokens.EXPERIENCE_MECHANIC_DECISION_REQUIRED_TOKENS,
        ),
        (
            experience_paths.EXPERIENCE_VERDICT_RESIDUE_DECISION_NAME,
            experience_tokens.EXPERIENCE_VERDICT_RESIDUE_DECISION_REQUIRED_TOKENS,
        ),
        (
            experience_paths.EXPERIENCE_PART_CONTRACT_GUARD_DECISION_NAME,
            experience_tokens.EXPERIENCE_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS,
        ),
    ):
        _require(context, repo_root, path_name, tokens, issues)
    _require(
        context,
        repo_root,
        experience_paths.EXPERIENCE_MECHANIC_PROVENANCE_NAME,
        context.provenance_tokens,
        issues,
    )
    _require(
        context,
        repo_root,
        "docs/decisions/README.md",
        (
            experience_paths.EXPERIENCE_PART_CONTRACT_GUARD_DECISION_NAME,
            "Experience Part Contract Guard",
        ),
        issues,
    )
    return issues


__all__ = (
    "ExperienceRouteContext",
    "validate_experience_route_surfaces",
)
