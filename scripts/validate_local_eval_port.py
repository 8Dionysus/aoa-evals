#!/usr/bin/env python3
"""Validate sibling-repo local eval ports."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import yaml
from jsonschema import Draft202012Validator


CONTRACT_ROOT = Path(__file__).resolve().parents[1]
EVAL_NEED_SCHEMA = (
    CONTRACT_ROOT
    / "mechanics"
    / "proof-object"
    / "parts"
    / "eval-authoring"
    / "schemas"
    / "eval-need.schema.json"
)

REQUIRED_PORT_FILES = (
    "AGENTS.md",
    "README.md",
    "PORT.yaml",
    "intake/README.md",
    "suites/README.md",
    "reports/README.md",
)
REQUIRED_PORT_FIELDS = (
    "schema_version",
    "owner_repo",
    "status",
    "proof_owner_repo",
    "default_intake_schema",
    "local_role",
    "central_boundary",
)
VALID_STATUSES = {"skeleton", "active"}
AUTHORITY_BOUNDARY_TOKENS = ("verdict", "scoring", "regression", "proof doctrine")
CLAIM_FAMILIES = {
    "artifact",
    "boundary",
    "capability",
    "comparative",
    "longitudinal",
    "regression",
    "stress",
    "workflow",
}


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target-root",
        default=".",
        help="Repository root that should contain the local eval port.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit a JSON result instead of human-readable issues.",
    )
    return parser.parse_args(argv)


def relative_location(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def load_yaml_payload(path: Path, root: Path, issues: list[ValidationIssue]) -> Any | None:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
    except yaml.YAMLError as exc:
        issues.append(ValidationIssue(relative_location(path, root), f"invalid YAML: {exc}"))
    return None


def load_json_payload(path: Path, root: Path, issues: list[ValidationIssue]) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
    except json.JSONDecodeError as exc:
        issues.append(ValidationIssue(relative_location(path, root), f"invalid JSON: {exc}"))
    return None


def format_schema_path(path_parts: Sequence[Any]) -> str:
    parts: list[str] = []
    for part in path_parts:
        if isinstance(part, int):
            if parts:
                parts[-1] = f"{parts[-1]}[{part}]"
            else:
                parts.append(f"[{part}]")
        else:
            parts.append(str(part))
    return ".".join(parts)


def eval_need_validator() -> Draft202012Validator:
    schema = json.loads(EVAL_NEED_SCHEMA.read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def validate_port_file(
    repo_root: Path,
    evals_dir: Path,
    issues: list[ValidationIssue],
) -> dict[str, Any] | None:
    port_path = evals_dir / "PORT.yaml"
    payload = load_yaml_payload(port_path, repo_root, issues)
    if payload is None:
        return None
    location = relative_location(port_path, repo_root)
    if not isinstance(payload, dict):
        issues.append(ValidationIssue(location, "PORT.yaml must contain a mapping"))
        return None

    for field in REQUIRED_PORT_FIELDS:
        if field not in payload:
            issues.append(ValidationIssue(location, f"missing required field '{field}'"))

    if payload.get("schema_version") != "local_eval_port_v1":
        issues.append(
            ValidationIssue(location, "schema_version must be 'local_eval_port_v1'")
        )
    if payload.get("owner_repo") != repo_root.name:
        issues.append(
            ValidationIssue(location, f"owner_repo must match target root '{repo_root.name}'")
        )
    if payload.get("status") not in VALID_STATUSES:
        issues.append(ValidationIssue(location, "status must be 'skeleton' or 'active'"))
    if payload.get("proof_owner_repo") != "aoa-evals":
        issues.append(ValidationIssue(location, "proof_owner_repo must be 'aoa-evals'"))
    if payload.get("default_intake_schema") != "eval_need_v1":
        issues.append(ValidationIssue(location, "default_intake_schema must be 'eval_need_v1'"))

    central_boundary = payload.get("central_boundary")
    if not isinstance(central_boundary, str) or not central_boundary.strip():
        issues.append(ValidationIssue(location, "central_boundary must be a non-empty string"))
    else:
        lowered = central_boundary.lower()
        missing = [token for token in AUTHORITY_BOUNDARY_TOKENS if token not in lowered]
        if missing:
            issues.append(
                ValidationIssue(
                    location,
                    "central_boundary must name no verdict, scoring, regression, "
                    "or proof doctrine authority",
                )
            )

    local_role = payload.get("local_role")
    if not isinstance(local_role, str) or not local_role.strip():
        issues.append(ValidationIssue(location, "local_role must be a non-empty string"))

    return payload


def validate_required_shape(repo_root: Path, evals_dir: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if not evals_dir.is_dir():
        issues.append(ValidationIssue("evals", "local eval port directory is missing"))
        return issues
    for relative_path in REQUIRED_PORT_FILES:
        path = evals_dir / relative_path
        if not path.is_file():
            issues.append(ValidationIssue(relative_location(path, repo_root), "file is missing"))
    return issues


def validate_port_docs(repo_root: Path, evals_dir: Path, issues: list[ValidationIssue]) -> None:
    for relative_path in ("README.md", "AGENTS.md"):
        path = evals_dir / relative_path
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8").lower()
        missing = [
            token
            for token in ("aoa-evals", "verdict", "scoring", "regression", "proof doctrine")
            if token not in text
        ]
        if missing:
            issues.append(
                ValidationIssue(
                    relative_location(path, repo_root),
                    "local eval port docs must name aoa-evals and the central "
                    "verdict/scoring/regression/proof doctrine boundary",
                )
            )


def validate_intake_payloads(
    repo_root: Path,
    evals_dir: Path,
    issues: list[ValidationIssue],
) -> int:
    intake_dir = evals_dir / "intake"
    if not intake_dir.is_dir():
        return 0

    validator = eval_need_validator()
    intake_count = 0
    for path in sorted(intake_dir.glob("*.eval_need.json")):
        intake_count += 1
        payload = load_json_payload(path, repo_root, issues)
        if payload is None:
            continue
        errors = sorted(
            validator.iter_errors(payload),
            key=lambda error: (list(error.absolute_path), error.message),
        )
        for error in errors:
            error_path = format_schema_path(error.absolute_path)
            if error_path:
                message = f"schema violation at '{error_path}': {error.message}"
            else:
                message = f"schema violation: {error.message}"
            issues.append(ValidationIssue(relative_location(path, repo_root), message))
    return intake_count


def expected_family(manifest: dict[str, Any]) -> Path | None:
    baseline_mode = manifest.get("baseline_mode", "none")
    category = manifest.get("category")
    if baseline_mode != "none":
        if not isinstance(baseline_mode, str) or not baseline_mode:
            return None
        return Path("comparison") / baseline_mode
    if not isinstance(category, str) or category not in CLAIM_FAMILIES:
        return None
    return Path(category)


def validate_local_bundles(
    repo_root: Path,
    evals_dir: Path,
    issues: list[ValidationIssue],
) -> int:
    bundle_count = 0
    for manifest_path in sorted(evals_dir.glob("**/eval.yaml")):
        bundle_count += 1
        bundle_dir = manifest_path.parent
        eval_md_path = bundle_dir / "EVAL.md"
        if not eval_md_path.is_file():
            issues.append(ValidationIssue(relative_location(eval_md_path, repo_root), "file is missing"))

        manifest = load_yaml_payload(manifest_path, repo_root, issues)
        if not isinstance(manifest, dict):
            issues.append(
                ValidationIssue(
                    relative_location(manifest_path, repo_root),
                    "eval.yaml must contain a mapping",
                )
            )
            continue

        name = manifest.get("name")
        if not isinstance(name, str) or not name:
            issues.append(ValidationIssue(relative_location(manifest_path, repo_root), "missing string 'name'"))
        elif name != bundle_dir.name:
            issues.append(
                ValidationIssue(
                    relative_location(manifest_path, repo_root),
                    f"name '{name}' must match bundle directory '{bundle_dir.name}'",
                )
            )

        family = expected_family(manifest)
        if family is None:
            issues.append(
                ValidationIssue(
                    relative_location(manifest_path, repo_root),
                    "manifest must expose a valid category and baseline_mode",
                )
            )
            continue
        try:
            bundle_relative = bundle_dir.relative_to(evals_dir)
        except ValueError:
            continue
        family_relative = Path(*bundle_relative.parts[:-1])
        if family_relative != family:
            issues.append(
                ValidationIssue(
                    relative_location(manifest_path, repo_root),
                    f"bundle must live under evals/{family.as_posix()}/",
                )
            )
    return bundle_count


def validate_status(
    repo_root: Path,
    evals_dir: Path,
    port_payload: dict[str, Any] | None,
    *,
    intake_count: int,
    bundle_count: int,
    issues: list[ValidationIssue],
) -> None:
    if not port_payload:
        return
    location = relative_location(evals_dir / "PORT.yaml", repo_root)
    status = port_payload.get("status")
    if status == "active" and intake_count == 0 and bundle_count == 0:
        issues.append(
            ValidationIssue(
                location,
                "active local eval port must contain at least one intake packet or local bundle",
            )
        )
    if status == "skeleton" and (intake_count > 0 or bundle_count > 0):
        issues.append(
            ValidationIssue(
                location,
                "skeleton local eval port must not contain active intake packets or bundles",
            )
        )


def validate_local_eval_port(repo_root: Path) -> list[ValidationIssue]:
    repo_root = repo_root.resolve()
    evals_dir = repo_root / "evals"
    issues = validate_required_shape(repo_root, evals_dir)
    if not evals_dir.is_dir():
        return issues

    port_payload = validate_port_file(repo_root, evals_dir, issues)
    validate_port_docs(repo_root, evals_dir, issues)
    intake_count = validate_intake_payloads(repo_root, evals_dir, issues)
    bundle_count = validate_local_bundles(repo_root, evals_dir, issues)
    validate_status(
        repo_root,
        evals_dir,
        port_payload,
        intake_count=intake_count,
        bundle_count=bundle_count,
        issues=issues,
    )
    return issues


def format_issues(issues: Sequence[ValidationIssue]) -> str:
    return "\n".join(f"- {issue.location}: {issue.message}" for issue in issues)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    target_root = Path(args.target_root)
    issues = validate_local_eval_port(target_root)
    if args.json:
        print(
            json.dumps(
                {
                    "schema": "local_eval_port_validation_v1",
                    "target_root": str(target_root.resolve()),
                    "ok": not issues,
                    "issues": [
                        {"location": issue.location, "message": issue.message}
                        for issue in issues
                    ],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif issues:
        print("Local eval port validation failed:")
        print(format_issues(issues))
    else:
        print("Local eval port validation passed.")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
