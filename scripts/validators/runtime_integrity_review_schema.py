"""Runtime integrity review schema closure checks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from jsonschema import Draft202012Validator

from validators import runtime_integrity_review_common as common
from validators.common import (
    ValidationIssue,
    load_json_payload,
    relative_location,
    validate_inline_schema,
)


RUNTIME_INTEGRITY_REVIEW_SCHEMA_NAME = common.RUNTIME_INTEGRITY_REVIEW_SCHEMA_NAME
RUNTIME_INTEGRITY_REVIEW_SCHEMA_PATH = common.RUNTIME_INTEGRITY_REVIEW_SCHEMA_PATH
RUNTIME_INTEGRITY_REVIEW_BUDGET_REF = common.RUNTIME_INTEGRITY_REVIEW_BUDGET_REF
RUNTIME_INTEGRITY_REVIEW_EVIDENCE_REFS = common.RUNTIME_INTEGRITY_REVIEW_EVIDENCE_REFS
RUNTIME_INTEGRITY_REVIEW_REPLAY_KEYS = common.RUNTIME_INTEGRITY_REVIEW_REPLAY_KEYS
RUNTIME_INTEGRITY_REVIEW_FORBIDDEN_CLAIMS = common.RUNTIME_INTEGRITY_REVIEW_FORBIDDEN_CLAIMS


@dataclass(frozen=True)
class RuntimeIntegrityReviewSchemaValidation:
    issues: list[ValidationIssue]
    validator: Draft202012Validator | None


def runtime_integrity_review_schema_validation(
    repo_root: Path,
) -> RuntimeIntegrityReviewSchemaValidation:
    issues: list[ValidationIssue] = []
    schema_path = repo_root / RUNTIME_INTEGRITY_REVIEW_SCHEMA_PATH
    schema = load_json_payload(schema_path, issues, root=repo_root)
    if schema is None:
        return RuntimeIntegrityReviewSchemaValidation(issues, None)
    schema_location = relative_location(schema_path, repo_root)
    if not validate_inline_schema(schema, location=schema_location, issues=issues):
        return RuntimeIntegrityReviewSchemaValidation(issues, None)
    if schema.get("title") != "aoa-evals runtime integrity review":
        issues.append(
            ValidationIssue(
                schema_location,
                "runtime integrity review schema title must be 'aoa-evals runtime integrity review'",
            )
        )
    if schema.get("additionalProperties") is not False:
        issues.append(
            ValidationIssue(
                schema_location,
                "runtime integrity review schema must keep top-level additionalProperties set to false",
            )
        )
    required_fields = schema.get("required")
    expected_required_fields = {
        "schema_version",
        "owner_repo",
        "surface_kind",
        "status",
        "budget_ref",
        "evidence_refs",
        "replay_requirements",
        "human_review_needed",
        "forbidden_claims",
        "notes",
    }
    if not isinstance(required_fields, list) or set(required_fields) != expected_required_fields:
        issues.append(
            ValidationIssue(
                schema_location,
                "runtime integrity review schema must require the full owner-local contract field set",
            )
        )
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        issues.append(
            ValidationIssue(
                schema_location,
                "runtime integrity review schema must define object properties",
            )
        )
    else:
        const_fields = {
            "schema_version": "runtime_integrity_review_v1",
            "owner_repo": "aoa-evals",
            "surface_kind": "runtime_integrity_review",
            "status": "candidate_only",
            "budget_ref": RUNTIME_INTEGRITY_REVIEW_BUDGET_REF,
            "human_review_needed": True,
        }
        for field_name, expected_value in const_fields.items():
            field_schema = properties.get(field_name)
            if not isinstance(field_schema, dict) or field_schema.get("const") != expected_value:
                issues.append(
                    ValidationIssue(
                        schema_location,
                        f"runtime integrity review schema must keep '{field_name}' bound to its owner-local constant",
                    )
                )

        evidence_schema = properties.get("evidence_refs")
        if (
            not isinstance(evidence_schema, dict)
            or evidence_schema.get("type") != "array"
            or evidence_schema.get("uniqueItems") is not True
            or evidence_schema.get("minItems") != len(RUNTIME_INTEGRITY_REVIEW_EVIDENCE_REFS)
            or evidence_schema.get("maxItems") != len(RUNTIME_INTEGRITY_REVIEW_EVIDENCE_REFS)
        ):
            issues.append(
                ValidationIssue(
                    schema_location,
                    "runtime integrity review schema must keep evidence_refs as an exact-count unique repo-ref array",
                )
            )
        else:
            evidence_items = evidence_schema.get("items")
            if (
                not isinstance(evidence_items, dict)
                or evidence_items.get("type") != "string"
                or evidence_items.get("pattern") != r"^repo:[^\s]+/.+$"
            ):
                issues.append(
                    ValidationIssue(
                        schema_location,
                        "runtime integrity review schema must keep evidence_refs items constrained to repo-qualified refs",
                    )
                )

        replay_schema = properties.get("replay_requirements")
        if (
            not isinstance(replay_schema, dict)
            or replay_schema.get("type") != "object"
            or replay_schema.get("additionalProperties") is not False
        ):
            issues.append(
                ValidationIssue(
                    schema_location,
                    "runtime integrity review schema must keep replay_requirements as a closed object",
                )
            )
        else:
            replay_required = replay_schema.get("required")
            if not isinstance(replay_required, list) or set(replay_required) != set(
                RUNTIME_INTEGRITY_REVIEW_REPLAY_KEYS
            ):
                issues.append(
                    ValidationIssue(
                        schema_location,
                        "runtime integrity review schema must require the full replay_requirements key set",
                    )
                )
            replay_properties = replay_schema.get("properties")
            if not isinstance(replay_properties, dict):
                issues.append(
                    ValidationIssue(
                        schema_location,
                        "runtime integrity review schema must define replay_requirements properties",
                    )
                )
            else:
                for field_name in RUNTIME_INTEGRITY_REVIEW_REPLAY_KEYS:
                    field_schema = replay_properties.get(field_name)
                    if not isinstance(field_schema, dict) or field_schema.get("const") is not True:
                        issues.append(
                            ValidationIssue(
                                schema_location,
                                f"runtime integrity review schema must keep replay_requirements.{field_name} bound to true",
                            )
                        )

        forbidden_schema = properties.get("forbidden_claims")
        if (
            not isinstance(forbidden_schema, dict)
            or forbidden_schema.get("type") != "array"
            or forbidden_schema.get("uniqueItems") is not True
            or forbidden_schema.get("minItems") != len(RUNTIME_INTEGRITY_REVIEW_FORBIDDEN_CLAIMS)
            or forbidden_schema.get("maxItems") != len(RUNTIME_INTEGRITY_REVIEW_FORBIDDEN_CLAIMS)
        ):
            issues.append(
                ValidationIssue(
                    schema_location,
                    "runtime integrity review schema must keep forbidden_claims as an exact-count unique array",
                )
            )
        else:
            forbidden_items = forbidden_schema.get("items")
            forbidden_enum = (
                forbidden_items.get("enum") if isinstance(forbidden_items, dict) else None
            )
            if not isinstance(forbidden_enum, list) or set(forbidden_enum) != set(
                RUNTIME_INTEGRITY_REVIEW_FORBIDDEN_CLAIMS
            ):
                issues.append(
                    ValidationIssue(
                        schema_location,
                        "runtime integrity review schema must keep forbidden_claims bound to the no-authority guard set",
                    )
                )

        notes_schema = properties.get("notes")
        if (
            not isinstance(notes_schema, dict)
            or notes_schema.get("type") != "string"
            or notes_schema.get("minLength") != 1
        ):
            issues.append(
                ValidationIssue(
                    schema_location,
                    "runtime integrity review schema must keep notes as a non-empty string",
                )
            )
    return RuntimeIntegrityReviewSchemaValidation(issues, Draft202012Validator(schema))


def validate_runtime_integrity_review_schema_surface(repo_root: Path) -> list[ValidationIssue]:
    return runtime_integrity_review_schema_validation(repo_root).issues
