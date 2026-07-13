"""Repo-config route-residue validation."""

from __future__ import annotations

from pathlib import Path

from validators import mechanics as mechanics_validator
from validators.common import ValidationIssue, read_text_or_issue, relative_location
from validators.route_residue_common import (
    ACTIVE_MECHANIC_ROUTE_RESIDUE_MECHANIC_TOKEN_RE,
    ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE,
    LEGACY_NAMING_NAME,
    PROOF_TOPOLOGY_NAME,
    ROADMAP_NAME,
    ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS,
    RouteResidueContext,
    normalize_active_mechanic_route_token,
    root_route_card_reference_is_allowed,
)


REPO_CONFIG_ROUTE_RESIDUE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0079-repo-config-route-residue-guard.md"
)
REPO_CONFIG_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k repo_config_route_residue"
)
REPO_CONFIG_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS = (
    "Repo Config Route Residue Guard",
    ".gitignore",
    ".github/workflows/",
    "legacy mechanic parent",
    "route-card-only root district",
    "not historical memory",
)


def iter_repo_config_route_residue_files(repo_root: Path) -> list[Path]:
    paths: set[Path] = set()
    for path_name in (".gitignore", "pytest.ini"):
        path = repo_root / path_name
        if path.is_file():
            paths.add(path)

    workflows_root = repo_root / ".github" / "workflows"
    if workflows_root.is_dir():
        paths.update(path for path in workflows_root.glob("*.yml") if path.is_file())
        paths.update(path for path in workflows_root.glob("*.yaml") if path.is_file())

    return sorted(paths, key=lambda path: path.relative_to(repo_root).as_posix())


def repo_config_root_route_residue_message(
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
        "repo config surface must not point at route-card-only root district "
        f"payload '{normalized}'; use an active `mechanics/...` route, "
        f"`evals/<family>/<eval>/...`, or the root route card "
        f"'{district_name}/README.md' or '{district_name}/AGENTS.md'"
    )


def repo_config_legacy_parent_residue_message(value: str) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if not normalized:
        return None

    for wrong_parent, correct_route in mechanics_validator.FORMER_WRONG_MECHANIC_PARENT_ROUTES:
        wrong_route = f"mechanics/{wrong_parent}"
        if normalized == wrong_route or normalized.startswith(f"{wrong_route}/"):
            return (
                "repo config surface must not point at legacy mechanic parent "
                f"`{wrong_route}/`; use active `mechanics/{correct_route}/`"
            )
    return None


def validate_repo_config_route_residue(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path in iter_repo_config_route_residue_files(repo_root):
        file_location = relative_location(path, repo_root)
        text = read_text_or_issue(path, issues, root=repo_root)
        if not text:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            line_location = f"{file_location}:{line_number}"
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE.finditer(line):
                message = repo_config_root_route_residue_message(
                    match.group("token"),
                    source_file=path,
                    repo_root=repo_root,
                )
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_MECHANIC_TOKEN_RE.finditer(line):
                message = repo_config_legacy_parent_residue_message(match.group("token"))
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))

    return issues


def validate_repo_config_route_residue_surfaces(
    repo_root: Path,
    *,
    context: RouteResidueContext,
) -> list[ValidationIssue]:
    issues = validate_repo_config_route_residue(repo_root)
    for path_name, tokens in (
        (REPO_CONFIG_ROUTE_RESIDUE_DECISION_NAME, REPO_CONFIG_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS),
        (
            "docs/decisions/README.md",
            (REPO_CONFIG_ROUTE_RESIDUE_DECISION_NAME, "Repo Config Route Residue Guard"),
        ),
        (PROOF_TOPOLOGY_NAME, ("Repo config route residue", ".gitignore")),
        (LEGACY_NAMING_NAME, ("repo config surfaces", "legacy mechanic parent")),
        (ROADMAP_NAME, ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS),
    ):
        context.require_tokens(repo_root, path_name, tokens, issues)
    return issues


__all__ = (
    "REPO_CONFIG_ROUTE_RESIDUE_DECISION_NAME",
    "REPO_CONFIG_ROUTE_RESIDUE_COMMAND",
    "REPO_CONFIG_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS",
    "iter_repo_config_route_residue_files",
    "repo_config_root_route_residue_message",
    "repo_config_legacy_parent_residue_message",
    "validate_repo_config_route_residue",
    "validate_repo_config_route_residue_surfaces",
)
