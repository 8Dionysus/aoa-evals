#!/usr/bin/env python3
"""Validate AoA eval candidate packets without accepting proof."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from jsonschema import Draft202012Validator, FormatChecker

import build_eval_readiness_dashboard as readiness


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKET_SCHEMA_PATH = (
    REPO_ROOT
    / "mechanics"
    / "audit"
    / "parts"
    / "candidate-readers"
    / "schemas"
    / "aoa-eval-candidate-packet.schema.json"
)
DEFAULT_PACKET_ROOT = (
    REPO_ROOT / "mechanics" / "audit" / "parts" / "candidate-readers" / "packets"
)
EXAMPLE_PACKET = (
    REPO_ROOT
    / "mechanics"
    / "audit"
    / "parts"
    / "candidate-readers"
    / "examples"
    / "aoa_eval_candidate_packet.example.json"
)
BASE_FORBIDDEN_EFFECTS = {
    "central_proof_promotion",
    "verdict_acceptance",
    "score_or_baseline_creation",
    "repo_mutation",
    "mcp_created_bundle",
}
FORBIDDEN_PROOF_FIELDS = {
    "verdict",
    "score",
    "scoring",
    "baseline",
    "baseline_mode",
    "proof_status",
    "central_status",
    "bundle_status",
    "maturity_score",
    "report_format",
    "claim_type",
    "accepted_proof",
    "proof_verdict",
    "regression_baseline",
}


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "targets",
        nargs="*",
        help=(
            "Candidate packet files or directories. Directories are searched for "
            "'*.eval_candidate.json'. Defaults to the candidate-reader packets directory."
        ),
    )
    parser.add_argument(
        "--schema-only",
        action="store_true",
        help="Validate the schema and bundled example without requiring packet files.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON result.")
    return parser.parse_args(argv)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_validator() -> Draft202012Validator:
    schema = load_json(PACKET_SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


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
    return ".".join(parts) or "$"


def packet_paths(targets: Sequence[str]) -> list[Path]:
    if not targets:
        targets = (str(DEFAULT_PACKET_ROOT),)
    paths: list[Path] = []
    for target in targets:
        path = Path(target)
        if not path.is_absolute():
            path = REPO_ROOT / path
        if path.is_dir():
            paths.extend(sorted(path.rglob("*.eval_candidate.json")))
        elif path.exists():
            paths.append(path)
        else:
            paths.append(path)
    return paths


def relative(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def validate_payload(
    payload: Any,
    *,
    location: str,
    validator: Draft202012Validator,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    schema_errors = sorted(
        validator.iter_errors(payload),
        key=lambda error: [str(part) for part in error.path],
    )
    for error in schema_errors:
        issues.append(
            ValidationIssue(
                location,
                f"schema error at {format_schema_path(error.path)}: {error.message}",
            )
        )
    if not isinstance(payload, dict):
        return issues

    forbidden_present = sorted(FORBIDDEN_PROOF_FIELDS & set(payload))
    if forbidden_present:
        issues.append(
            ValidationIssue(
                location,
                "candidate packet must not carry proof-promotion fields: "
                + ", ".join(forbidden_present),
            )
        )

    trigger_ids = {item["id"] for item in readiness.TRIGGER_CLASSES}
    trigger_class_id = payload.get("trigger_class_id")
    if isinstance(trigger_class_id, str) and trigger_class_id not in trigger_ids:
        issues.append(
            ValidationIssue(
                location,
                f"trigger_class_id {trigger_class_id!r} is not in readiness trigger taxonomy",
            )
        )

    forbidden_effects = payload.get("forbidden_effects")
    if isinstance(forbidden_effects, list):
        missing = sorted(BASE_FORBIDDEN_EFFECTS - {str(item) for item in forbidden_effects})
        if missing:
            issues.append(
                ValidationIssue(
                    location,
                    "candidate packet forbidden_effects must include "
                    + ", ".join(missing),
                )
            )

    if payload.get("candidate_only") is not True:
        issues.append(ValidationIssue(location, "candidate_only must be true"))
    if payload.get("proof_authority") is not False:
        issues.append(ValidationIssue(location, "proof_authority must be false"))
    if payload.get("promotion_allowed") is not False:
        issues.append(ValidationIssue(location, "promotion_allowed must be false"))

    candidate_state = payload.get("candidate_state")
    if isinstance(candidate_state, str) and candidate_state not in readiness.CANDIDATE_QUEUE_STATES:
        issues.append(
            ValidationIssue(
                location,
                f"candidate_state {candidate_state!r} is not in queue lifecycle states",
            )
        )

    if candidate_state == "accepted":
        gates = payload.get("promotion_forbidden_until")
        gate_text = " ".join(str(item) for item in gates) if isinstance(gates, list) else ""
        if "human" not in gate_text.lower() or "owner" not in gate_text.lower():
            issues.append(
                ValidationIssue(
                    location,
                    "accepted candidate state still requires explicit human owner acceptance gate",
                )
            )

    return issues


def validate_files(paths: Sequence[Path]) -> list[ValidationIssue]:
    validator = schema_validator()
    issues: list[ValidationIssue] = []
    for path in paths:
        location = relative(path)
        if not path.exists():
            issues.append(ValidationIssue(location, "candidate packet path is missing"))
            continue
        try:
            payload = load_json(path)
        except json.JSONDecodeError as exc:
            issues.append(ValidationIssue(location, f"invalid JSON: {exc}"))
            continue
        issues.extend(validate_payload(payload, location=location, validator=validator))
    return issues


def result_payload(paths: Sequence[Path], issues: Sequence[ValidationIssue]) -> dict[str, Any]:
    return {
        "schema_version": "aoa_eval_candidate_packet_validation_v1",
        "authority_boundary": "Candidate packet validation checks candidate-only evidence; it does not accept proof, verdicts, scores, baselines, or central promotion.",
        "schema_ref": relative(PACKET_SCHEMA_PATH),
        "packet_count": len(paths),
        "valid": not issues,
        "issues": [
            {"location": issue.location, "message": issue.message}
            for issue in issues
        ],
    }


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    paths = [EXAMPLE_PACKET] if args.schema_only else packet_paths(args.targets)
    issues = validate_files(paths)
    payload = result_payload(paths, issues)

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif issues:
        print("Eval candidate packet validation failed.")
        for issue in issues:
            print(f"- {issue.location}: {issue.message}")
    else:
        print(f"Eval candidate packet validation passed for {len(paths)} packet(s).")

    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
