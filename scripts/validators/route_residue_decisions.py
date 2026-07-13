"""Decision-record route-residue validation."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from validators.common import ValidationIssue, read_text_or_issue, relative_location
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
from validators.route_residue_root_authored import (
    ROOT_AUTHORED_ROUTE_RESIDUE_CONTEXT_TOKENS,
)


DECISION_ROUTE_RESIDUE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0078-decision-route-residue-guard.md"
)
DECISION_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k decision_route_residue"
)
DECISION_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS = (
    "Decision Route Residue Guard",
    "decision records",
    "historical context",
    "route-card-only root district",
    "`evals/<family>/<eval>/...`",
    "active `mechanics/...`",
)
DECISION_ROUTE_RESIDUE_CONTEXT_TOKENS = (
    *ROOT_AUTHORED_ROUTE_RESIDUE_CONTEXT_TOKENS,
    "legacy",
    "provenance",
    "old root",
    "previous root",
    "stale authored path example",
)


def iter_decision_route_residue_files(repo_root: Path) -> list[Path]:
    decisions_root = repo_root / "docs" / "decisions"
    if not decisions_root.is_dir():
        return []
    return sorted(
        (
            path
            for path in decisions_root.glob("*.md")
            if path.name not in {"AGENTS.md", "README.md", "TEMPLATE.md"}
        ),
        key=lambda path: path.relative_to(repo_root).as_posix(),
    )


def decision_route_context_allows(lines: Sequence[str], line_number: int) -> bool:
    start = max(0, line_number - 2)
    end = min(len(lines), line_number + 1)
    context = "\n".join(lines[start:end])
    return any(token in context for token in DECISION_ROUTE_RESIDUE_CONTEXT_TOKENS)


def decision_route_residue_message(
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
        "decision record must not present route-card-only root district payload "
        f"'{normalized}' as a current route; mark it as former root or "
        "historical context, route to `evals/<family>/<eval>/...` or active "
        f"`mechanics/...`, or cite the root route card '{district_name}/README.md' "
        f"or '{district_name}/AGENTS.md'"
    )


def validate_decision_route_residue(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path in iter_decision_route_residue_files(repo_root):
        file_location = relative_location(path, repo_root)
        text = read_text_or_issue(path, issues, root=repo_root)
        if not text:
            continue
        lines = text.splitlines()
        for line_number, line in enumerate(lines, start=1):
            if decision_route_context_allows(lines, line_number):
                continue
            line_location = f"{file_location}:{line_number}"
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE.finditer(line):
                message = decision_route_residue_message(
                    match.group("token"),
                    source_file=path,
                    repo_root=repo_root,
                )
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))

    return issues


def validate_decision_route_residue_surfaces(
    repo_root: Path,
    *,
    context: RouteResidueContext,
) -> list[ValidationIssue]:
    issues = validate_decision_route_residue(repo_root)
    for path_name, tokens in (
        (DECISION_ROUTE_RESIDUE_DECISION_NAME, DECISION_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS),
        (
            "docs/decisions/README.md",
            (DECISION_ROUTE_RESIDUE_DECISION_NAME, "Decision Route Residue Guard"),
        ),
        (PROOF_TOPOLOGY_NAME, ("Decision route residue", "historical context")),
        (LEGACY_NAMING_NAME, ("decision records", "former root")),
        (ROADMAP_NAME, ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS),
    ):
        context.require_tokens(repo_root, path_name, tokens, issues)
    return issues


__all__ = (
    "DECISION_ROUTE_RESIDUE_DECISION_NAME",
    "DECISION_ROUTE_RESIDUE_COMMAND",
    "DECISION_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS",
    "DECISION_ROUTE_RESIDUE_CONTEXT_TOKENS",
    "iter_decision_route_residue_files",
    "decision_route_context_allows",
    "decision_route_residue_message",
    "validate_decision_route_residue",
    "validate_decision_route_residue_surfaces",
)
