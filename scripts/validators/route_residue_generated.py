"""Generated/readout route-residue validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

import eval_catalog_contract

from validators import mechanics as mechanics_validator
from validators.common import ValidationIssue, relative_location
from validators.root_route_cards import ROOT_ROUTE_CARD_ONLY_DISTRICTS
from validators.route_residue_common import (
    LEGACY_NAMING_NAME,
    PROOF_TOPOLOGY_NAME,
    ROADMAP_NAME,
    ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS,
    RouteResidueContext,
)


GENERATED_ROUTE_RESIDUE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0073-generated-route-residue-guard.md"
)
GENERATED_READER_INDEX_REQUIRED_TOKENS = (
    "# Generated Reader Index",
    "repo-wide derived reader surfaces",
    "authored source ownership",
    "generated/quest_catalog.min.json",
    "generated/quest_dispatch.min.example.json",
    "source owner surface",
    'Source surfaces answer\n"what is true?"',
)
GENERATED_AGENTS_REQUIRED_TOKENS = (
    "repo-wide derived reader surfaces only",
    "Authored source surfaces keep doctrine",
    "generated/quest_catalog.min.json",
    "generated/quest_dispatch.min.json",
    "generated/quest_catalog.min.example.json",
    "generated/quest_dispatch.min.example.json",
)
GENERATED_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS = (
    "Generated Route Residue Guard",
    "structured references",
    "route-card-only root district",
    "part-local generated readers",
    "content_markdown",
    "python -m pytest -q tests/test_generated_route_residue.py",
)
GENERATED_ROUTE_RESIDUE_MECHANIC_PREFIXES = tuple(
    f"mechanics/{wrong_parent}/"
    for wrong_parent, _correct_route in mechanics_validator.FORMER_WRONG_MECHANIC_PARENT_ROUTES
)
GENERATED_ROUTE_RESIDUE_MECHANIC_EXACT_ROUTES = tuple(
    f"mechanics/{wrong_parent}"
    for wrong_parent, _correct_route in mechanics_validator.FORMER_WRONG_MECHANIC_PARENT_ROUTES
)
GENERATED_ROUTE_RESIDUE_ROOT_PREFIXES = tuple(
    f"{district_name}/" for district_name in ROOT_ROUTE_CARD_ONLY_DISTRICTS
)
GENERATED_ROUTE_RESIDUE_ROOT_EXACT_ROUTES = tuple(ROOT_ROUTE_CARD_ONLY_DISTRICTS)
GENERATED_ROUTE_RESIDUE_SKIP_KEYS = frozenset({"content_markdown"})


def iter_generated_route_residue_files(repo_root: Path) -> list[Path]:
    paths: set[Path] = set()
    generated_root = repo_root / "generated"
    if generated_root.is_dir():
        paths.update(path for path in generated_root.glob("*.json") if path.is_file())
    mechanics_root = repo_root / "mechanics"
    if mechanics_root.is_dir():
        paths.update(
            path
            for path in mechanics_root.rglob("generated/*.json")
            if path.is_file()
        )
    return sorted(paths, key=lambda path: path.relative_to(repo_root).as_posix())


def format_generated_json_location(file_location: str, json_path: Sequence[str | int]) -> str:
    suffix = ""
    for part in json_path:
        if isinstance(part, int):
            suffix += f"[{part}]"
        else:
            suffix += f".{part}"
    return f"{file_location}{suffix}"


def mechanic_part_root_for_generated_json(path: Path, repo_root: Path) -> Path | None:
    try:
        parts = path.relative_to(repo_root).parts
    except ValueError:
        return None
    if len(parts) < 6:
        return None
    if parts[0] != "mechanics" or parts[2] != "parts" or parts[4] != "generated":
        return None
    return repo_root.joinpath(*parts[:4])


def generated_route_residue_message(
    value: str,
    *,
    source_file: Path,
    repo_root: Path,
) -> str | None:
    normalized = value.strip().replace("\\", "/")
    if not normalized or normalized.startswith("repo:"):
        return None

    for exact_route in GENERATED_ROUTE_RESIDUE_MECHANIC_EXACT_ROUTES:
        if normalized == exact_route:
            return (
                "generated/readout route must use the active mechanic parent, "
                f"not legacy parent route '{exact_route}'"
            )
    for prefix in GENERATED_ROUTE_RESIDUE_MECHANIC_PREFIXES:
        if normalized.startswith(prefix):
            return (
                "generated/readout route must use the active mechanic parent, "
                f"not legacy parent route '{prefix}'"
            )

    part_root = mechanic_part_root_for_generated_json(source_file, repo_root)
    if part_root is not None and (part_root / normalized).exists():
        return None

    for exact_route in GENERATED_ROUTE_RESIDUE_ROOT_EXACT_ROUTES:
        if normalized == exact_route:
            return (
                "generated/readout route must not point at route-card-only "
                f"root district '{exact_route}/'"
            )
    for prefix in GENERATED_ROUTE_RESIDUE_ROOT_PREFIXES:
        if normalized.startswith(prefix):
            return (
                "generated/readout route must not point at route-card-only "
                f"root district '{prefix}'"
            )

    return None


def validate_generated_route_residue(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    def walk_json(
        value: Any,
        *,
        source_file: Path,
        file_location: str,
        json_path: list[str | int],
    ) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key in GENERATED_ROUTE_RESIDUE_SKIP_KEYS:
                    continue
                walk_json(
                    child,
                    source_file=source_file,
                    file_location=file_location,
                    json_path=[*json_path, key],
                )
            return
        if isinstance(value, list):
            for index, child in enumerate(value):
                walk_json(
                    child,
                    source_file=source_file,
                    file_location=file_location,
                    json_path=[*json_path, index],
                )
            return
        if not isinstance(value, str):
            return

        message = generated_route_residue_message(
            value,
            source_file=source_file,
            repo_root=repo_root,
        )
        if message is not None:
            issues.append(
                ValidationIssue(
                    format_generated_json_location(file_location, json_path),
                    message,
                )
            )

    for path in iter_generated_route_residue_files(repo_root):
        file_location = relative_location(path, repo_root)
        payload, contract_issues = eval_catalog_contract.read_json_file(path, repo_root)
        issues.extend(
            ValidationIssue(issue.location, issue.message)
            for issue in contract_issues
        )
        if payload is None:
            continue
        walk_json(payload, source_file=path, file_location=file_location, json_path=[])

    return issues


def validate_generated_route_residue_surfaces(
    repo_root: Path,
    *,
    context: RouteResidueContext,
) -> list[ValidationIssue]:
    issues = validate_generated_route_residue(repo_root)
    for path_name, tokens in (
        ("generated/README.md", GENERATED_READER_INDEX_REQUIRED_TOKENS),
        ("generated/AGENTS.md", GENERATED_AGENTS_REQUIRED_TOKENS),
        (GENERATED_ROUTE_RESIDUE_DECISION_NAME, GENERATED_ROUTE_RESIDUE_DECISION_REQUIRED_TOKENS),
        (
            "docs/decisions/README.md",
            (GENERATED_ROUTE_RESIDUE_DECISION_NAME, "Generated Route Residue Guard"),
        ),
        (PROOF_TOPOLOGY_NAME, ("Generated route residue", "same part root")),
        (LEGACY_NAMING_NAME, ("generated/readout JSON", "same part")),
        (ROADMAP_NAME, ROADMAP_ROUTE_RESIDUE_GUARD_FAMILY_TOKENS),
    ):
        context.require_tokens(repo_root, path_name, tokens, issues)
    return issues
