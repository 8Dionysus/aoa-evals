"""Active mechanic route-card residue validation."""

from __future__ import annotations

from pathlib import Path

from validators import mechanics as mechanics_validator
from validators.common import ValidationIssue, read_text_or_issue, relative_location
from validators.route_residue_common import (
    ACTIVE_MECHANIC_ROUTE_RESIDUE_MECHANIC_TOKEN_RE,
    ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE,
    LEGACY_NAMING_NAME,
    MECHANICS_README_NAME,
    PROOF_TOPOLOGY_NAME,
    ROADMAP_NAME,
    ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS,
    RouteResidueContext,
    normalize_active_mechanic_route_token,
    root_route_card_reference_is_allowed,
)


ACTIVE_MECHANIC_ROUTE_RESIDUE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0076-active-mechanic-route-residue-guard.md"
)
ACTIVE_MECHANIC_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k active_mechanic_route_residue"
)
ACTIVE_MECHANIC_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS = (
    "Active Mechanic Route Residue Guard",
    "authored mechanics route cards",
    "route-card-only root district",
    "same part root",
    "`evals/<family>/<eval>/...`",
    "legacy parent route",
)


def iter_active_mechanic_route_residue_files(repo_root: Path) -> list[Path]:
    paths: set[Path] = set()
    mechanics_readme = repo_root / MECHANICS_README_NAME
    if mechanics_readme.is_file():
        paths.add(mechanics_readme)

    mechanics_root = repo_root / "mechanics"
    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES:
        parent_root = mechanics_root / parent_name
        for route_card_name in ("AGENTS.md", "README.md", "PARTS.md"):
            route_card = parent_root / route_card_name
            if route_card.is_file():
                paths.add(route_card)

        parts_root = parent_root / "parts"
        parts_readme = parts_root / "README.md"
        if parts_readme.is_file():
            paths.add(parts_readme)
        if not parts_root.is_dir():
            continue
        for part_root in sorted(parts_root.iterdir(), key=lambda item: item.name):
            part_readme = part_root / "README.md"
            if part_readme.is_file():
                paths.add(part_readme)

    return sorted(paths, key=lambda path: path.relative_to(repo_root).as_posix())


def mechanic_owner_root_for_route_card(path: Path, repo_root: Path) -> Path:
    try:
        parts = path.relative_to(repo_root).parts
    except ValueError:
        return repo_root / "mechanics"

    if len(parts) >= 5 and parts[0] == "mechanics" and parts[2] == "parts":
        return repo_root.joinpath(*parts[:4])
    if len(parts) >= 2 and parts[0] == "mechanics":
        return repo_root.joinpath(*parts[:2])
    return repo_root / "mechanics"


def active_mechanic_root_route_residue_message(
    value: str,
    *,
    source_file: Path,
    repo_root: Path,
) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if not normalized or root_route_card_reference_is_allowed(normalized):
        return None

    owner_root = mechanic_owner_root_for_route_card(source_file, repo_root)
    if (owner_root / normalized).exists() or (source_file.parent / normalized).exists():
        return None

    district_name = normalized.split("/", 1)[0]
    return (
        "active mechanic route card must not point at route-card-only root "
        f"district payload '{normalized}'; use a part-local path under the "
        f"same part root, a bundle-local `evals/<family>/<eval>/...` path, or the "
        f"root route card '{district_name}/README.md' or '{district_name}/AGENTS.md'"
    )


def active_mechanic_legacy_parent_residue_message(value: str) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if not normalized:
        return None

    for wrong_parent, correct_route in mechanics_validator.FORMER_WRONG_MECHANIC_PARENT_ROUTES:
        wrong_route = f"mechanics/{wrong_parent}"
        if normalized == wrong_route or normalized.startswith(f"{wrong_route}/"):
            return (
                "active mechanic route card must use the active mechanic parent "
                f"`mechanics/{correct_route}/`, not legacy parent route "
                f"`{wrong_route}/`"
            )
    return None


def validate_active_mechanic_route_residue(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path in iter_active_mechanic_route_residue_files(repo_root):
        file_location = relative_location(path, repo_root)
        text = read_text_or_issue(path, issues, root=repo_root)
        if not text:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            line_location = f"{file_location}:{line_number}"
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE.finditer(line):
                message = active_mechanic_root_route_residue_message(
                    match.group("token"),
                    source_file=path,
                    repo_root=repo_root,
                )
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_MECHANIC_TOKEN_RE.finditer(line):
                message = active_mechanic_legacy_parent_residue_message(match.group("token"))
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))

    return issues


def validate_active_mechanic_route_residue_surfaces(
    repo_root: Path,
    *,
    context: RouteResidueContext,
) -> list[ValidationIssue]:
    issues = validate_active_mechanic_route_residue(repo_root)
    for path_name, tokens in (
        (
            ACTIVE_MECHANIC_ROUTE_RESIDUE_DECISION_NAME,
            ACTIVE_MECHANIC_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS,
        ),
        (
            "docs/decisions/README.md",
            (ACTIVE_MECHANIC_ROUTE_RESIDUE_DECISION_NAME, "Active Mechanic Route Residue Guard"),
        ),
        (PROOF_TOPOLOGY_NAME, ("Active mechanic route residue", "same part root")),
        (LEGACY_NAMING_NAME, ("authored mechanics route cards", "legacy parent route")),
        (ROADMAP_NAME, ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS),
    ):
        context.require_tokens(repo_root, path_name, tokens, issues)
    return issues


__all__ = (
    "ACTIVE_MECHANIC_ROUTE_RESIDUE_DECISION_NAME",
    "ACTIVE_MECHANIC_ROUTE_RESIDUE_COMMAND",
    "ACTIVE_MECHANIC_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS",
    "iter_active_mechanic_route_residue_files",
    "mechanic_owner_root_for_route_card",
    "active_mechanic_root_route_residue_message",
    "active_mechanic_legacy_parent_residue_message",
    "validate_active_mechanic_route_residue",
    "validate_active_mechanic_route_residue_surfaces",
)
