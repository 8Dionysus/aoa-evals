"""Bundle-local source eval report artifact validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from validators import source_eval_report_longitudinal as report_longitudinal
from validators import source_eval_report_modes as report_modes
from validators.common import ValidationIssue
from validators.source_eval_artifact_common import requires_materialized_comparison_artifacts
from validators.source_eval_common import (
    load_json_payload,
    relative_location,
    validate_inline_schema,
    validate_json_against_inline_schema,
)


def validate_bundle_report_artifacts(
    repo_root: Path,
    bundle_dir: Path,
    manifest: dict[str, Any] | None,
    issues: list[ValidationIssue],
) -> None:
    schema_path = bundle_dir / "reports" / "summary.schema.json"
    example_path = bundle_dir / "reports" / "example-report.json"
    has_schema = schema_path.is_file()
    has_example = example_path.is_file()
    required_mode = manifest.get("baseline_mode") if isinstance(manifest, dict) else None
    requires_materialized = requires_materialized_comparison_artifacts(manifest)

    if has_schema and not has_example:
        issues.append(
            ValidationIssue(
                relative_location(bundle_dir, repo_root),
                "bundle-local report schema exists but reports/example-report.json is missing",
            )
        )
    elif requires_materialized and not has_example:
        issues.append(
            ValidationIssue(
                relative_location(bundle_dir, repo_root),
                f"comparative-summary bundle with baseline_mode '{required_mode}' must ship reports/example-report.json",
            )
        )

    if has_example and not has_schema:
        issues.append(
            ValidationIssue(
                relative_location(bundle_dir, repo_root),
                "bundle-local report example exists but reports/summary.schema.json is missing",
            )
        )
    elif requires_materialized and not has_schema:
        issues.append(
            ValidationIssue(
                relative_location(bundle_dir, repo_root),
                f"comparative-summary bundle with baseline_mode '{required_mode}' must ship reports/summary.schema.json",
            )
        )

    if not has_schema or not has_example:
        return

    schema_location = relative_location(schema_path, repo_root)
    example_location = relative_location(example_path, repo_root)
    schema_issues: list[ValidationIssue] = []
    schema = load_json_payload(schema_path, schema_issues)
    issues.extend(schema_issues)
    if schema is None or not validate_inline_schema(
        schema,
        location=schema_location,
        issues=issues,
    ):
        return

    example_payload = load_json_payload(example_path, issues)
    if example_payload is None:
        return
    example_valid = validate_json_against_inline_schema(
        example_payload,
        schema,
        location=example_location,
        issues=issues,
    )
    if manifest is not None and manifest.get("report_format") == "comparative-summary":
        report_modes.validate_comparative_report_mode_contract(
            schema,
            example_payload,
            required_mode=required_mode,
            schema_location=schema_location,
            example_location=example_location,
            issues=issues,
        )
    if example_valid and required_mode == "longitudinal-window":
        report_longitudinal.validate_longitudinal_report_example(
            example_payload,
            location=example_location,
            issues=issues,
        )

    for report_path in sorted(schema_path.parent.glob("*.report.json")):
        validate_actual_bundle_report_artifact(
            report_path,
            schema,
            repo_root=repo_root,
            manifest=manifest,
            issues=issues,
        )


def validate_actual_bundle_report_artifact(
    report_path: Path,
    schema: dict[str, Any],
    *,
    repo_root: Path,
    manifest: dict[str, Any] | None,
    issues: list[ValidationIssue],
) -> None:
    report_location = relative_location(report_path, repo_root)
    report_payload = load_json_payload(report_path, issues)
    if report_payload is None:
        return

    validate_json_against_inline_schema(
        report_payload,
        schema,
        location=report_location,
        issues=issues,
    )

    if not isinstance(report_payload, dict) or not isinstance(manifest, dict):
        return

    expected_name = manifest.get("name")
    if isinstance(expected_name, str) and report_payload.get("eval_name") != expected_name:
        issues.append(
            ValidationIssue(
                report_location,
                f"actual bundle report eval_name must match manifest name '{expected_name}'",
            )
        )

    expected_status = manifest.get("status")
    if isinstance(expected_status, str) and report_payload.get("bundle_status") != expected_status:
        issues.append(
            ValidationIssue(
                report_location,
                f"actual bundle report bundle_status must match manifest status '{expected_status}'",
            )
        )

__all__ = (
    "validate_actual_bundle_report_artifact",
    "validate_bundle_report_artifacts",
)
