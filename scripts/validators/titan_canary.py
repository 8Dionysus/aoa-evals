"""Titan seed canary shape validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from validators.common import ValidationIssue, relative_location
from validators.titan_route_paths import TITAN_SEED_BOUNDARY_SEEDS_DIR_NAME


def load_titan_canary_yaml(
    path: Path,
    issues: list[ValidationIssue],
    *,
    root: Path,
) -> Any | None:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
        return None
    except yaml.YAMLError as exc:
        issues.append(ValidationIssue(relative_location(path, root), f"invalid YAML: {exc}"))
        return None


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
        payload = load_titan_canary_yaml(canary_path, issues, root=repo_root)
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


__all__ = (
    "load_titan_canary_yaml",
    "validate_titan_canary_surfaces",
)
