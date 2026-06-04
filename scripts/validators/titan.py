"""Titan mechanic route and seed-canary validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Sequence

import yaml

from validators.common import ValidationIssue, read_text_or_issue, relative_location


TITAN_MECHANIC_README_NAME = "mechanics/titan/README.md"
TITAN_MECHANIC_AGENTS_NAME = "mechanics/titan/AGENTS.md"
TITAN_MECHANIC_DIRECTION_NAME = "mechanics/titan/DIRECTION.md"
TITAN_PARTS_INDEX_README_NAME = "mechanics/titan/parts/README.md"
TITAN_SEED_BOUNDARY_PART_README_NAME = "mechanics/titan/parts/seed-boundary/README.md"
TITAN_SEED_BOUNDARY_SEEDS_DIR_NAME = "mechanics/titan/parts/seed-boundary/seeds"
TITAN_SEED_BOUNDARY_SEEDS_README_NAME = "mechanics/titan/parts/seed-boundary/seeds/README.md"
TITAN_SEED_BOUNDARY_SEEDS_AGENTS_NAME = "mechanics/titan/parts/seed-boundary/seeds/AGENTS.md"
TITAN_SEED_BOUNDARY_CONTRACT_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0055-titan-seed-boundary-contract.md"
)

TITAN_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "mechanics/titan/parts/seed-boundary/docs/TITAN_INCARNATION_CANARIES.md",
    "mechanics/titan/parts/seed-boundary/docs/TITAN_SUMMON_DISCIPLINE_CANARIES.md",
    "mechanics/titan/parts/seed-boundary/seeds/titan*.yaml",
    "mechanics/titan/parts/seed-boundary/seeds/AGENTS.md",
    "validate_titan_canary_surfaces",
    "seed canary",
    "aoa-agents",
    "future executable scorer",
    "full incarnation proof",
    "hidden arena",
    "mutation gate",
    "judgment gate",
    "python scripts/validate_repo.py",
)
TITAN_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "Titan seed canaries",
    "mechanics/titan/parts/seed-boundary/seeds/titan*.yaml",
    "seed-boundary evidence only",
    "mutation gate",
    "judgment gate",
    "validate_titan_canary_surfaces",
    "python scripts/validate_repo.py",
)
TITAN_MECHANIC_DIRECTION_REQUIRED_TOKENS = (
    "aoa-agents",
    "Titan role classes",
    "bearer identity",
    "summon boundary law",
    "incarnation posture",
    "seed-boundary",
    "seed-boundary evidence",
)
TITAN_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/titan/",
    "mechanics/titan/parts/seed-boundary/seeds/titan*.yaml",
    "validate_titan_canary_surfaces",
    "moves the seed YAML files",
    "full incarnation proof",
    "future executable scorer",
    "owner-named evals-native",
    "aoa-agents",
)
TITAN_INCARNATION_CANARIES_REQUIRED_TOKENS = (
    "mechanics/titan/README.md",
    "mechanics/titan/parts/seed-boundary/seeds/titan*.yaml",
    "seed canaries",
    "full incarnation proof",
    "runtime cohort",
    "summon authority",
    "memory sovereignty",
    "AGENTS.md#validation",
)
TITAN_SUMMON_DISCIPLINE_REQUIRED_TOKENS = (
    "mechanics/titan/README.md",
    "seed-defined",
    "named Titan targets",
    "generic role",
    "hidden background arena",
    "full incarnation",
)
TITAN_SEED_BOUNDARY_SEEDS_AGENTS_REQUIRED_TOKENS = (
    "## Operating Card",
    "Titan seed canaries",
    "mechanics/titan/parts/seed-boundary/seeds/titan*.yaml",
    "seed-local route card",
    "full incarnation proof",
    "runtime activation",
    "validate_titan_canary_surfaces",
    "Filename or identifier drift",
    "centralized-child-validation",
)
TITAN_SEED_BOUNDARY_SEEDS_README_REQUIRED_TOKENS = (
    "Titan Canary Seeds",
    "mechanics/titan/parts/seed-boundary/seeds/",
    "titan*.yaml",
    "seed-defined",
    "id` or `eval_id",
    "full incarnation proof",
    "Use [AGENTS.md](AGENTS.md#validation)",
    "parent `mechanics/titan/parts/AGENTS.md` lane",
)
TITAN_SEED_BOUNDARY_PART_README_REQUIRED_TOKENS = (
    "Seed Boundary Part",
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "validate_titan_canary_surfaces",
    "aoa-agents",
    "aoa-memo",
    "runtime activation",
    "summon authority",
    "memory sovereignty",
    "canary presence reads as proof",
    "python scripts/validate_repo.py",
)
TITAN_PARTS_INDEX_README_REQUIRED_TOKENS = (
    "# Titan / Parts Route",
    "## Operating Card",
    "| role | lower index for active Titan proof-seed parts |",
    "## Active Parts",
    "| `seed-boundary/` | seed-defined Titan boundary canary family and seed-local route law | `seed-boundary/README.md` |",
    "## Owner Pressure Routes",
    "| canary presence reads as incarnation, summon authority, or runtime cohort proof | keep the part seed-defined and route stronger claims to Titan/runtime owners |",
    "| canary presence reads as memory sovereignty | route to `aoa-memo` before proof adoption |",
    "| executable scorer-backed proof pressure appears | wait for scorer, fixture, report, and validator contracts |",
    "## Part Admission Route",
    "| seed-defined Titan canary YAML | current source shape and validator lane match the seed-boundary contract | `seed-boundary/README.md` |",
    "mechanics/titan/parts/AGENTS.md#validation",
)
TITAN_SEED_BOUNDARY_ROUTE_SURFACE_NAMES = (
    TITAN_MECHANIC_AGENTS_NAME,
    TITAN_MECHANIC_DIRECTION_NAME,
    "mechanics/titan/PARTS.md",
    TITAN_PARTS_INDEX_README_NAME,
    TITAN_SEED_BOUNDARY_PART_README_NAME,
    "mechanics/titan/parts/seed-boundary/docs/TITAN_INCARNATION_CANARIES.md",
    "mechanics/titan/parts/seed-boundary/docs/TITAN_SUMMON_DISCIPLINE_CANARIES.md",
    TITAN_SEED_BOUNDARY_SEEDS_AGENTS_NAME,
    TITAN_SEED_BOUNDARY_SEEDS_README_NAME,
)
TITAN_SEED_BOUNDARY_STALE_ROUTE_PHRASES = (
    "not full incarnation proof",
    "not incarnation proof",
    "not full proof by themselves",
    "not named after the canary artifact form",
    "Do not split named Titan",
    "This part is seed-defined only. It does not create",
    "Do not use canary presence as proof",
    "These files are boundary-check seeds, not full eval bundles",
    "These files are seed-defined boundary checks. They are not full eval bundles",
    "Seed canaries are not full incarnation proof",
    "Seed canaries do not activate",
    "Seed canaries do not grant",
    "Seed canaries do not create",
    "Seed canaries do not bypass",
    "They do not grant summon authority",
    "Do not claim full incarnation proof",
    "Do not bypass mutation gate",
    "Do not move canary files",
)
TITAN_SEED_BOUNDARY_CONTRACT_DECISION_REQUIRED_TOKENS = (
    "Titan Seed-boundary Contract",
    "mechanics/titan/parts/seed-boundary/README.md",
    "titan-canaries",
    "stronger owner split",
    "stop-lines",
    "aoa-agents",
    "aoa-memo",
    "runtime activation",
    "python scripts/validate_repo.py",
)


@dataclass(frozen=True)
class TitanRouteContext:
    require_tokens: Callable[..., str]


def _require(
    context: TitanRouteContext,
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


def load_yaml_file(path: Path, issues: list[ValidationIssue], *, root: Path) -> Any | None:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
        return None
    except yaml.YAMLError as exc:
        issues.append(ValidationIssue(relative_location(path, root), f"invalid YAML: {exc}"))
        return None


def validate_titan_route_surfaces(
    repo_root: Path,
    *,
    context: TitanRouteContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _require(context, repo_root, TITAN_MECHANIC_README_NAME, TITAN_MECHANIC_REQUIRED_TOKENS, issues)
    _require(context, repo_root, TITAN_MECHANIC_AGENTS_NAME, TITAN_MECHANIC_AGENTS_REQUIRED_TOKENS, issues)
    _require(context, repo_root, TITAN_MECHANIC_DIRECTION_NAME, TITAN_MECHANIC_DIRECTION_REQUIRED_TOKENS, issues)
    _require(
        context,
        repo_root,
        "docs/decisions/AOA-EV-D-0015-titan-mechanic-package.md",
        TITAN_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        "mechanics/titan/parts/seed-boundary/docs/TITAN_INCARNATION_CANARIES.md",
        TITAN_INCARNATION_CANARIES_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        "mechanics/titan/parts/seed-boundary/docs/TITAN_SUMMON_DISCIPLINE_CANARIES.md",
        TITAN_SUMMON_DISCIPLINE_REQUIRED_TOKENS,
        issues,
    )
    _require(context, repo_root, TITAN_SEED_BOUNDARY_SEEDS_AGENTS_NAME, TITAN_SEED_BOUNDARY_SEEDS_AGENTS_REQUIRED_TOKENS, issues)
    _require(context, repo_root, TITAN_SEED_BOUNDARY_SEEDS_README_NAME, TITAN_SEED_BOUNDARY_SEEDS_README_REQUIRED_TOKENS, issues)
    _require(context, repo_root, TITAN_PARTS_INDEX_README_NAME, TITAN_PARTS_INDEX_README_REQUIRED_TOKENS, issues)
    _require(context, repo_root, TITAN_SEED_BOUNDARY_PART_README_NAME, TITAN_SEED_BOUNDARY_PART_README_REQUIRED_TOKENS, issues)
    for path_name in TITAN_SEED_BOUNDARY_ROUTE_SURFACE_NAMES:
        route_text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
        for stale_phrase in TITAN_SEED_BOUNDARY_STALE_ROUTE_PHRASES:
            if route_text and stale_phrase in route_text:
                issues.append(
                    ValidationIssue(
                        path_name,
                        "Titan seed-boundary route surfaces must route pressure through owner maps instead of stale negative claim-limit phrasing",
                    )
                )
    _require(
        context,
        repo_root,
        TITAN_SEED_BOUNDARY_CONTRACT_DECISION_NAME,
        TITAN_SEED_BOUNDARY_CONTRACT_DECISION_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        "docs/decisions/README.md",
        (
            TITAN_SEED_BOUNDARY_CONTRACT_DECISION_NAME,
            "Titan Seed-boundary Contract",
        ),
        issues,
    )
    return issues


def validate_titan_canary_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    canary_dir = repo_root / TITAN_SEED_BOUNDARY_SEEDS_DIR_NAME
    canary_paths = sorted(canary_dir.glob("titan*.yaml"))
    if not canary_paths:
        issues.append(
            ValidationIssue(
                TITAN_SEED_BOUNDARY_SEEDS_DIR_NAME,
                "Titan seed YAML files must be present under mechanics/titan/parts/seed-boundary/seeds/titan*.yaml",
            )
        )
        return issues

    for canary_path in canary_paths:
        location = relative_location(canary_path, repo_root)
        payload = load_yaml_file(canary_path, issues, root=repo_root)
        if not isinstance(payload, dict):
            if payload is not None:
                issues.append(ValidationIssue(location, "Titan canary must be a YAML mapping"))
            continue
        canary_id = payload.get("id") or payload.get("eval_id")
        if canary_id != canary_path.stem:
            issues.append(ValidationIssue(location, "Titan canary id must match the filename stem"))
        if "version" in payload and not isinstance(payload.get("version"), int):
            issues.append(ValidationIssue(location, "Titan canary version must be an integer"))
        if not any(
            isinstance(payload.get(field), str) and payload[field].strip()
            for field in ("purpose", "claim", "kind", "description", "objective")
        ):
            issues.append(ValidationIssue(location, "Titan canary must expose purpose, claim, kind, description, or objective"))
        checks = payload.get("checks")
        if checks is not None:
            if not isinstance(checks, list) or not checks:
                issues.append(ValidationIssue(location, "Titan canary checks must be a non-empty list when present"))
                continue
            for index, check in enumerate(checks):
                check_location = f"{location}.checks[{index}]"
                if not isinstance(check, dict):
                    issues.append(ValidationIssue(check_location, "Titan canary check must be an object"))
                    continue
                if not isinstance(check.get("name"), str) or not check["name"].strip():
                    issues.append(
                        ValidationIssue(
                            check_location,
                            "Titan canary check name must be a non-empty string",
                        )
                    )
                if not any(
                    isinstance(check.get(field), str) and check[field].strip()
                    for field in ("assert", "command", "expect", "rule")
                ):
                    issues.append(
                        ValidationIssue(
                            check_location,
                            "Titan canary check must expose assert, command, expect, or rule",
                        )
                    )
        failure_examples = payload.get("failure_examples")
        if failure_examples is None:
            if not any(
                key in payload
                for key in (
                    "expected_failure",
                    "expected_result",
                    "expected",
                    "forbidden",
                    "description",
                    "checks",
                    "required_fields",
                )
            ):
                issues.append(
                    ValidationIssue(
                        location,
                        "Titan canary must expose failure_examples, expected_failure, expected_result, expected, forbidden, checks, or required_fields",
                    )
                )
        elif not isinstance(failure_examples, list) or not failure_examples:
            issues.append(
                ValidationIssue(
                    location,
                    "Titan canary failure_examples must be a non-empty list when present",
                )
            )
        elif not all(isinstance(item, str) and item.strip() for item in failure_examples):
            issues.append(
                ValidationIssue(
                    location,
                    "Titan canary failure_examples must be non-empty strings",
                )
            )

    return issues
