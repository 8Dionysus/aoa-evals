"""Phase Alpha matrix local generated projection contracts."""

from __future__ import annotations

from pathlib import Path

from jsonschema import Draft202012Validator

from validators.phase_alpha_matrix_common import (
    EXPECTED_RUNTIME_LANES,
    PHASE_ALPHA_EVAL_MATRIX_NAME,
    PHASE_ALPHA_EVAL_MATRIX_SCHEMA_NAME,
    ValidationIssue,
    load_json_payload,
    relative_location,
    validate_against_schema,
    validate_inline_schema,
)


def validate_phase_alpha_matrix_projection(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    generated_path = repo_root / PHASE_ALPHA_EVAL_MATRIX_NAME
    generated_location = relative_location(generated_path, repo_root)
    schema_path = repo_root / PHASE_ALPHA_EVAL_MATRIX_SCHEMA_NAME
    schema_location = relative_location(schema_path, repo_root)

    schema = load_json_payload(schema_path, issues, root=repo_root)
    if schema is None:
        return issues
    if not validate_inline_schema(schema, location=schema_location, issues=issues):
        return issues
    schema_validator = Draft202012Validator(schema)

    payload = load_json_payload(generated_path, issues, root=repo_root)
    if payload is None:
        return issues
    if not isinstance(payload, dict):
        issues.append(ValidationIssue(generated_location, "generated phase alpha eval matrix must be an object"))
        return issues

    validate_against_schema(
        payload,
        generated_location,
        issues,
        validator=schema_validator,
    )

    if payload.get("runtime_lanes") != EXPECTED_RUNTIME_LANES:
        issues.append(
            ValidationIssue(
                generated_location,
                "runtime_lanes must stay {'primary': 'llama.cpp', 'control': 'llama.cpp-second-pass'}",
            )
        )

    return issues


__all__ = ("validate_phase_alpha_matrix_projection",)
