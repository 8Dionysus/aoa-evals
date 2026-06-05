"""Questbook-linked RPG progression and unlock proof bridge contracts."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator, SchemaError

from validators.common import ValidationIssue


REPO_ROOT = Path(__file__).resolve().parents[2]

PROGRESSION_EVIDENCE_MODEL_NAME = (
    "mechanics/rpg/parts/progression-unlocks/docs/PROGRESSION_EVIDENCE_MODEL.md"
)
PROGRESSION_EVIDENCE_SCHEMA_NAME = (
    "mechanics/rpg/parts/progression-unlocks/schemas/progression_evidence.schema.json"
)
PROGRESSION_EVIDENCE_EXAMPLE_NAME = (
    "mechanics/rpg/parts/progression-unlocks/examples/progression_evidence.example.json"
)
UNLOCK_PROOF_BRIDGE_NAME = (
    "mechanics/rpg/parts/progression-unlocks/docs/UNLOCK_PROOF_BRIDGE.md"
)
UNLOCK_PROOF_SCHEMA_NAME = (
    "mechanics/rpg/parts/progression-unlocks/schemas/unlock_proof_catalog.schema.json"
)
UNLOCK_PROOF_EXAMPLE_NAME = (
    "mechanics/rpg/parts/progression-unlocks/generated/unlock_proof_cards.min.example.json"
)
PROGRESSION_EVIDENCE_REQUIRED_TOKENS = (
    "## Core route",
    "Progression evidence is quest-scoped or route-scoped proof.",
    "| one universal score or broad capability growth | keep multi-axis deltas here; route broad comparison through comparison/growth owner review |",
    "| quest acceptance or state-transition pressure | quest owner route plus cited evidence |",
    "cautions are first-class proof",
)
UNLOCK_PROOF_REQUIRED_TOKENS = (
    "## Core route",
    "`gated_grant`",
    "It interprets reviewed evidence",
    "| runtime equip or activation pressure | `abyss-stack` runtime route plus owner gates |",
    "| one proof object as a universal agent ranking | multi-axis progression evidence plus owner review |",
)


@lru_cache(maxsize=None)
def load_schema(schema_name: str) -> dict[str, Any]:
    schema_path = REPO_ROOT / schema_name
    with schema_path.open(encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=None)
def get_schema_validator(schema_name: str) -> Draft202012Validator:
    return Draft202012Validator(load_schema(schema_name))


def format_schema_path(path_parts: Iterable[Any]) -> str:
    parts: list[str] = []
    for part in path_parts:
        if isinstance(part, int):
            parts.append(f"[{part}]")
        else:
            if parts:
                parts.append(f".{part}")
            else:
                parts.append(str(part))
    return "".join(parts)


def relative_location(path: Path, root: Path | None = None) -> str:
    target_root = root or REPO_ROOT
    try:
        return path.relative_to(target_root).as_posix()
    except ValueError:
        return path.as_posix()


def read_text_or_issue(path: Path, issues: list[ValidationIssue], *, root: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
        return ""


def load_json_payload(path: Path, issues: list[ValidationIssue]) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path), "file is missing"))
        return None
    except json.JSONDecodeError as exc:
        issues.append(ValidationIssue(relative_location(path), f"invalid JSON: {exc}"))
        return None


def validate_against_schema(
    data: Any,
    schema_name: str,
    location: str,
    issues: list[ValidationIssue],
    *,
    validator: Draft202012Validator | None = None,
) -> bool:
    active_validator = validator or get_schema_validator(schema_name)
    schema_errors = sorted(
        active_validator.iter_errors(data),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    for error in schema_errors:
        error_path = format_schema_path(error.absolute_path)
        if error_path:
            message = f"schema violation at '{error_path}': {error.message}"
        else:
            message = f"schema violation: {error.message}"
        issues.append(ValidationIssue(location, message))
    return not schema_errors


def validate_unlock_proof_bridge_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    progression_doc_path = repo_root / PROGRESSION_EVIDENCE_MODEL_NAME
    progression_schema_path = repo_root / PROGRESSION_EVIDENCE_SCHEMA_NAME
    progression_example_path = repo_root / PROGRESSION_EVIDENCE_EXAMPLE_NAME
    doc_path = repo_root / UNLOCK_PROOF_BRIDGE_NAME
    schema_path = repo_root / UNLOCK_PROOF_SCHEMA_NAME
    example_path = repo_root / UNLOCK_PROOF_EXAMPLE_NAME

    progression_doc_text = read_text_or_issue(
        progression_doc_path,
        issues,
        root=repo_root,
    )
    if progression_doc_text:
        for token in PROGRESSION_EVIDENCE_REQUIRED_TOKENS:
            if token not in progression_doc_text:
                issues.append(
                    ValidationIssue(
                        relative_location(progression_doc_path, repo_root),
                        f"progression evidence note must mention '{token}'",
                    )
                )

    progression_schema_payload = load_json_payload(progression_schema_path, issues)
    if isinstance(progression_schema_payload, dict):
        if progression_schema_payload.get("title") != "progression_evidence_v1":
            issues.append(
                ValidationIssue(
                    relative_location(progression_schema_path, repo_root),
                    "progression evidence schema title must be 'progression_evidence_v1'",
                )
            )
        try:
            Draft202012Validator.check_schema(progression_schema_payload)
        except SchemaError as exc:
            issues.append(
                ValidationIssue(
                    relative_location(progression_schema_path, repo_root),
                    f"invalid JSON schema: {exc.message}",
                )
            )
    elif progression_schema_payload is not None:
        issues.append(
            ValidationIssue(
                relative_location(progression_schema_path, repo_root),
                "progression evidence schema must be a JSON object",
            )
        )

    progression_example_payload = load_json_payload(progression_example_path, issues)
    if isinstance(progression_example_payload, dict):
        validate_against_schema(
            progression_example_payload,
            PROGRESSION_EVIDENCE_SCHEMA_NAME,
            relative_location(progression_example_path, repo_root),
            issues,
        )
        if progression_example_payload.get("schema_version") != "progression_evidence_v1":
            issues.append(
                ValidationIssue(
                    relative_location(progression_example_path, repo_root),
                    "progression evidence example schema_version must be 'progression_evidence_v1'",
                )
            )
        if progression_example_payload.get("public_safe") is not True:
            issues.append(
                ValidationIssue(
                    relative_location(progression_example_path, repo_root),
                    "progression evidence example must keep public_safe true",
                )
            )
        if not progression_example_payload.get("cautions"):
            issues.append(
                ValidationIssue(
                    relative_location(progression_example_path, repo_root),
                    "progression evidence example must keep cautions explicit",
                )
            )
    elif progression_example_payload is not None:
        issues.append(
            ValidationIssue(
                relative_location(progression_example_path, repo_root),
                "progression evidence example must be a JSON object",
            )
        )

    doc_text = read_text_or_issue(doc_path, issues, root=repo_root)
    if doc_text:
        for token in UNLOCK_PROOF_REQUIRED_TOKENS:
            if token not in doc_text:
                issues.append(
                    ValidationIssue(
                        relative_location(doc_path, repo_root),
                        f"unlock proof bridge note must mention '{token}'",
                    )
                )

    schema_payload = load_json_payload(schema_path, issues)
    if isinstance(schema_payload, dict):
        if schema_payload.get("title") != "unlock_proof_catalog_v1":
            issues.append(
                ValidationIssue(
                    relative_location(schema_path, repo_root),
                    "unlock proof schema title must be 'unlock_proof_catalog_v1'",
                )
            )
        try:
            Draft202012Validator.check_schema(schema_payload)
        except SchemaError as exc:
            issues.append(
                ValidationIssue(
                    relative_location(schema_path, repo_root),
                    f"invalid JSON schema: {exc.message}",
                )
            )
    elif schema_payload is not None:
        issues.append(
            ValidationIssue(
                relative_location(schema_path, repo_root),
                "unlock proof schema must be a JSON object",
            )
        )

    example_text = read_text_or_issue(example_path, issues, root=repo_root)
    example_payload = load_json_payload(example_path, issues)
    if isinstance(example_payload, dict):
        validate_against_schema(
            example_payload,
            UNLOCK_PROOF_SCHEMA_NAME,
            relative_location(example_path, repo_root),
            issues,
        )
        if example_payload.get("schema_version") != "unlock_proof_catalog_v1":
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "unlock proof example schema_version must be 'unlock_proof_catalog_v1'",
                )
            )
        proofs = example_payload.get("proofs")
        if not isinstance(proofs, list) or not proofs:
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "unlock proof example must expose a non-empty proofs list",
                )
            )
        else:
            for index, proof in enumerate(proofs):
                if not isinstance(proof, dict):
                    continue
                if proof.get("public_safe") is not True:
                    issues.append(
                        ValidationIssue(
                            f"{relative_location(example_path, repo_root)}.proofs[{index}]",
                            "unlock proof example entries must keep public_safe true",
                        )
                    )
        if example_payload.get("notes") and "Example only." not in str(example_payload.get("notes")):
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "unlock proof example notes must keep example-only posture explicit",
                )
            )
    elif example_payload is not None:
        issues.append(
            ValidationIssue(
                relative_location(example_path, repo_root),
                "unlock proof example must be a JSON object",
            )
        )

    if example_text:
        if "AOA-PB-Q-0004" in example_text:
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "unlock proof example must not keep legacy playbook quest id 'AOA-PB-Q-0004'",
                )
            )
        if "AOA-EV-PROG-0002" in example_text:
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "unlock proof example must not reference missing progression evidence id 'AOA-EV-PROG-0002'",
                )
            )

    return issues
