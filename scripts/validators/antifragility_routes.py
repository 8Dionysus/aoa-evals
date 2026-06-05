"""Antifragility mechanic route and part-contract validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from validators import antifragility_route_paths as antifragility_paths
from validators import antifragility_route_tokens as antifragility_tokens
from validators.common import ValidationIssue, read_text_or_issue


@dataclass(frozen=True)
class AntifragilityRouteContext:
    require_tokens: Callable[..., str]
    provenance_tokens: Sequence[str]


def _require(
    context: AntifragilityRouteContext,
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


def validate_antifragility_route_surfaces(
    repo_root: Path,
    *,
    context: AntifragilityRouteContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name, tokens in (
        (
            antifragility_paths.ANTIFRAGILITY_MECHANIC_README_NAME,
            antifragility_tokens.ANTIFRAGILITY_MECHANIC_REQUIRED_TOKENS,
        ),
        (
            antifragility_paths.ANTIFRAGILITY_MECHANIC_AGENTS_NAME,
            antifragility_tokens.ANTIFRAGILITY_MECHANIC_AGENTS_REQUIRED_TOKENS,
        ),
        (
            antifragility_paths.ANTIFRAGILITY_MECHANIC_PARTS_NAME,
            antifragility_tokens.ANTIFRAGILITY_MECHANIC_PARTS_REQUIRED_TOKENS,
        ),
        (
            antifragility_paths.ANTIFRAGILITY_PARTS_README_NAME,
            antifragility_tokens.ANTIFRAGILITY_PARTS_README_REQUIRED_TOKENS,
        ),
    ):
        _require(context, repo_root, path_name, tokens, issues)

    parts_text = read_text_or_issue(
        repo_root / antifragility_paths.ANTIFRAGILITY_PARTS_README_NAME,
        issues,
        root=repo_root,
    )
    for forbidden_token in antifragility_tokens.ANTIFRAGILITY_PARTS_README_FORBIDDEN_TOKENS:
        if parts_text and forbidden_token in parts_text:
            issues.append(
                ValidationIssue(
                    antifragility_paths.ANTIFRAGILITY_PARTS_README_NAME,
                    "Antifragility parts lower index should use an operating card and owner pressure routes instead of stale negative boundary scaffold "
                    f"'{forbidden_token}'",
                )
            )

    for path_name, tokens in (
        (
            antifragility_paths.ANTIFRAGILITY_POSTURE_PART_README_NAME,
            antifragility_tokens.ANTIFRAGILITY_POSTURE_PART_REQUIRED_TOKENS,
        ),
        (
            antifragility_paths.ANTIFRAGILITY_STRESS_WINDOW_PART_README_NAME,
            antifragility_tokens.ANTIFRAGILITY_STRESS_WINDOW_PART_REQUIRED_TOKENS,
        ),
        (
            antifragility_paths.ANTIFRAGILITY_STRESS_WINDOW_DOC_NAME,
            antifragility_tokens.ANTIFRAGILITY_STRESS_WINDOW_DOC_REQUIRED_TOKENS,
        ),
        (
            antifragility_paths.ANTIFRAGILITY_REPAIR_PROOF_PART_README_NAME,
            antifragility_tokens.ANTIFRAGILITY_REPAIR_PROOF_PART_REQUIRED_TOKENS,
        ),
        (
            antifragility_paths.ANTIFRAGILITY_MECHANIC_DECISION_NAME,
            antifragility_tokens.ANTIFRAGILITY_MECHANIC_DECISION_REQUIRED_TOKENS,
        ),
        (
            antifragility_paths.ANTIFRAGILITY_PART_CONTRACT_GUARD_DECISION_NAME,
            antifragility_tokens.ANTIFRAGILITY_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS,
        ),
    ):
        _require(context, repo_root, path_name, tokens, issues)
    _require(
        context,
        repo_root,
        antifragility_paths.ANTIFRAGILITY_MECHANIC_PROVENANCE_NAME,
        context.provenance_tokens,
        issues,
    )
    _require(
        context,
        repo_root,
        "docs/decisions/README.md",
        (
            antifragility_paths.ANTIFRAGILITY_PART_CONTRACT_GUARD_DECISION_NAME,
            "Antifragility Part Contract Guard",
        ),
        issues,
    )
    return issues


__all__ = (
    "AntifragilityRouteContext",
    "validate_antifragility_route_surfaces",
)
