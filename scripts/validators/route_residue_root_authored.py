"""Root-authored route-residue validation."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from validators.common import ValidationIssue, read_text_or_issue, relative_location
from validators.root_route_cards import ROOT_ROUTE_CARD_ONLY_DISTRICTS
from validators.route_residue_common import (
    ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE,
    LEGACY_NAMING_NAME,
    PROOF_TOPOLOGY_NAME,
    ROADMAP_NAME,
    ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS,
    RouteResidueContext,
    normalize_active_mechanic_route_token,
    root_route_card_reference_is_allowed,
)


ROOT_AUTHORED_ROUTE_RESIDUE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0077-root-authored-route-residue-guard.md"
)
ROOT_AUTHORED_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k root_authored_route_residue"
)
ROOT_AUTHORED_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS = (
    "Root Authored Route Residue Guard",
    "root-facing authored surfaces",
    "route-card-only root district",
    "docs/decisions/",
    "historical context",
    "`evals/<family>/<eval>/...`",
)
ROOT_AUTHORED_ROUTE_RESIDUE_ROOT_FILES = (
    ".agents/spark/SWARM.md",
    "AGENTS.md",
    "AUDIT.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "DESIGN.AGENTS.md",
    "DESIGN.md",
    "EVAL_INDEX.md",
    "EVAL_SELECTION.md",
    "QUESTBOOK.md",
    "README.md",
    "ROADMAP.md",
    "evals/AGENTS.md",
)
ROOT_AUTHORED_ROUTE_RESIDUE_CONTEXT_TOKENS = (
    "Former root",
    "former root",
    "historical root",
    "Do not recreate",
    "compatibility route card",
    "mapped through",
    "route-card",
    "route card",
)


def iter_root_authored_route_residue_files(repo_root: Path) -> list[Path]:
    paths: set[Path] = set()

    for path_name in ROOT_AUTHORED_ROUTE_RESIDUE_ROOT_FILES:
        path = repo_root / path_name
        if path.is_file():
            paths.add(path)

    docs_root = repo_root / "docs"
    if docs_root.is_dir():
        paths.update(path for path in docs_root.glob("*.md") if path.is_file())

    for district_name, allowed_names in ROOT_ROUTE_CARD_ONLY_DISTRICTS.items():
        district = repo_root / district_name
        for allowed_name in allowed_names:
            path = district / allowed_name
            if path.is_file():
                paths.add(path)

    return sorted(paths, key=lambda path: path.relative_to(repo_root).as_posix())


def root_authored_route_context_allows(lines: Sequence[str], line_number: int) -> bool:
    start = max(0, line_number - 2)
    end = min(len(lines), line_number + 1)
    context = "\n".join(lines[start:end])
    return any(token in context for token in ROOT_AUTHORED_ROUTE_RESIDUE_CONTEXT_TOKENS)


def root_authored_route_residue_message(
    value: str,
    *,
    source_file: Path,
    repo_root: Path,
) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if not normalized or root_route_card_reference_is_allowed(normalized):
        return None
    if (repo_root / normalized).exists() or (source_file.parent / normalized).exists():
        return None

    district_name = normalized.split("/", 1)[0]
    return (
        "root-facing authored surface must not point at route-card-only root "
        f"district payload '{normalized}'; use `evals/<family>/<eval>/...`, an "
        "active `mechanics/...` route, or the root route card "
        f"'{district_name}/README.md' or '{district_name}/AGENTS.md'"
    )


def validate_root_authored_route_residue(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path in iter_root_authored_route_residue_files(repo_root):
        file_location = relative_location(path, repo_root)
        text = read_text_or_issue(path, issues, root=repo_root)
        if not text:
            continue
        lines = text.splitlines()
        for line_number, line in enumerate(lines, start=1):
            if root_authored_route_context_allows(lines, line_number):
                continue
            line_location = f"{file_location}:{line_number}"
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE.finditer(line):
                message = root_authored_route_residue_message(
                    match.group("token"),
                    source_file=path,
                    repo_root=repo_root,
                )
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))

    return issues


def validate_root_authored_route_residue_surfaces(
    repo_root: Path,
    *,
    context: RouteResidueContext,
) -> list[ValidationIssue]:
    issues = validate_root_authored_route_residue(repo_root)
    for path_name, tokens in (
        (
            ROOT_AUTHORED_ROUTE_RESIDUE_DECISION_NAME,
            ROOT_AUTHORED_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS,
        ),
        (
            "docs/decisions/README.md",
            (ROOT_AUTHORED_ROUTE_RESIDUE_DECISION_NAME, "Root Authored Route Residue Guard"),
        ),
        (PROOF_TOPOLOGY_NAME, ("Root authored route residue", "`evals/<family>/<eval>/...`")),
        (LEGACY_NAMING_NAME, ("root-facing authored surfaces", "historical context")),
        (ROADMAP_NAME, ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS),
    ):
        context.require_tokens(repo_root, path_name, tokens, issues)
    return issues


__all__ = (
    "ROOT_AUTHORED_ROUTE_RESIDUE_DECISION_NAME",
    "ROOT_AUTHORED_ROUTE_RESIDUE_COMMAND",
    "ROOT_AUTHORED_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS",
    "ROOT_AUTHORED_ROUTE_RESIDUE_ROOT_FILES",
    "ROOT_AUTHORED_ROUTE_RESIDUE_CONTEXT_TOKENS",
    "iter_root_authored_route_residue_files",
    "root_authored_route_context_allows",
    "root_authored_route_residue_message",
    "validate_root_authored_route_residue",
    "validate_root_authored_route_residue_surfaces",
)
