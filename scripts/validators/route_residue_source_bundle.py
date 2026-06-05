"""Source-bundle route-residue validation."""

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
    SOURCE_EVALS_DIR_NAME,
    RouteResidueContext,
    normalize_active_mechanic_route_token,
    root_route_card_reference_is_allowed,
)


SOURCE_BUNDLE_ROUTE_RESIDUE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0080-source-bundle-route-residue-guard.md"
)
SOURCE_BUNDLE_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k source_bundle_route_residue"
)
SOURCE_BUNDLE_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS = (
    "Source Bundle Route Residue Guard",
    "source proof objects",
    "bundle-local path",
    "repo-qualified sibling",
    "legacy mechanic parent",
    "route-card-only root district",
    SOURCE_BUNDLE_ROUTE_RESIDUE_COMMAND,
)
SOURCE_BUNDLE_ROUTE_RESIDUE_SUFFIXES = frozenset(
    {".json", ".md", ".txt", ".yaml", ".yml"}
)


def iter_source_bundle_route_residue_files(repo_root: Path) -> list[Path]:
    source_root = repo_root / SOURCE_EVALS_DIR_NAME
    if not source_root.is_dir():
        return []
    return sorted(
        (
            path
            for path in source_root.rglob("*")
            if path.is_file() and path.suffix in SOURCE_BUNDLE_ROUTE_RESIDUE_SUFFIXES
        ),
        key=lambda path: path.relative_to(repo_root).as_posix(),
    )


def bundle_root_for_source_file(path: Path, repo_root: Path) -> Path | None:
    try:
        path.relative_to(repo_root / SOURCE_EVALS_DIR_NAME)
    except ValueError:
        return None

    for parent in (path.parent, *path.parents):
        if parent == repo_root:
            break
        try:
            parent.relative_to(repo_root / SOURCE_EVALS_DIR_NAME)
        except ValueError:
            continue
        if (parent / "EVAL.md").is_file() and (parent / "eval.yaml").is_file():
            return parent
    return None


def source_bundle_root_route_residue_message(
    value: str,
    *,
    source_file: Path,
    repo_root: Path,
) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if (
        not normalized
        or normalized.startswith("repo:")
        or root_route_card_reference_is_allowed(normalized)
    ):
        return None

    bundle_root = bundle_root_for_source_file(source_file, repo_root)
    if bundle_root is not None and (bundle_root / normalized).exists():
        return None
    if (repo_root / normalized).exists() or (source_file.parent / normalized).exists():
        return None

    district_name = normalized.split("/", 1)[0]
    return (
        "source bundle must not carry ambiguous route-card-only root district "
        f"payload '{normalized}'; use a bundle-local path that exists under the "
        "owning eval package, `evals/<family>/<target>/...`, a repo-qualified sibling ref, "
        f"or the root route card '{district_name}/README.md' or "
        f"'{district_name}/AGENTS.md'"
    )


def source_bundle_legacy_parent_residue_message(value: str) -> str | None:
    normalized = normalize_active_mechanic_route_token(value)
    if not normalized:
        return None

    for wrong_parent, correct_route in mechanics_validator.FORMER_WRONG_MECHANIC_PARENT_ROUTES:
        wrong_route = f"mechanics/{wrong_parent}"
        if normalized == wrong_route or normalized.startswith(f"{wrong_route}/"):
            return (
                "source bundle must not point at legacy mechanic parent "
                f"`{wrong_route}/`; use active `mechanics/{correct_route}/` or "
                "a provenance/legacy route with explicit historical context"
            )
    return None


def validate_source_bundle_route_residue(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path in iter_source_bundle_route_residue_files(repo_root):
        file_location = relative_location(path, repo_root)
        text = read_text_or_issue(path, issues, root=repo_root)
        if not text:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            line_location = f"{file_location}:{line_number}"
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_ROOT_TOKEN_RE.finditer(line):
                message = source_bundle_root_route_residue_message(
                    match.group("token"),
                    source_file=path,
                    repo_root=repo_root,
                )
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))
            for match in ACTIVE_MECHANIC_ROUTE_RESIDUE_MECHANIC_TOKEN_RE.finditer(line):
                message = source_bundle_legacy_parent_residue_message(match.group("token"))
                if message is not None:
                    issues.append(ValidationIssue(line_location, message))

    return issues


def validate_source_bundle_route_residue_surfaces(
    repo_root: Path,
    *,
    context: RouteResidueContext,
) -> list[ValidationIssue]:
    issues = validate_source_bundle_route_residue(repo_root)
    for path_name, tokens in (
        (SOURCE_BUNDLE_ROUTE_RESIDUE_DECISION_NAME, SOURCE_BUNDLE_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS),
        (
            "docs/decisions/README.md",
            (SOURCE_BUNDLE_ROUTE_RESIDUE_DECISION_NAME, "Source Bundle Route Residue Guard"),
        ),
        (PROOF_TOPOLOGY_NAME, ("Source bundle route residue", "repo-qualified sibling")),
        (LEGACY_NAMING_NAME, ("source proof bundles", "repo-qualified sibling")),
        (ROADMAP_NAME, ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS),
    ):
        context.require_tokens(repo_root, path_name, tokens, issues)
    return issues


__all__ = (
    "SOURCE_BUNDLE_ROUTE_RESIDUE_DECISION_NAME",
    "SOURCE_BUNDLE_ROUTE_RESIDUE_COMMAND",
    "SOURCE_BUNDLE_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS",
    "SOURCE_BUNDLE_ROUTE_RESIDUE_SUFFIXES",
    "iter_source_bundle_route_residue_files",
    "bundle_root_for_source_file",
    "source_bundle_root_route_residue_message",
    "source_bundle_legacy_parent_residue_message",
    "validate_source_bundle_route_residue",
    "validate_source_bundle_route_residue_surfaces",
)
