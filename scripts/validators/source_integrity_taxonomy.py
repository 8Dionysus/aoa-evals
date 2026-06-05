"""Integrity taxonomy source-surface checks."""

from __future__ import annotations

from pathlib import Path

from validators.source_doctrine_common import (
    INTEGRITY_RISK_CLASSES,
    ValidationIssue,
    load_json_payload,
    read_text_or_issue,
    source_eval_dir,
)


def validate_integrity_taxonomy_surfaces(
    repo_root: Path,
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    relevant_names = {
        "aoa-eval-integrity-check",
        "aoa-regression-same-task",
        "aoa-output-vs-process-gap",
        "aoa-longitudinal-growth-snapshot",
        "aoa-artifact-review-rubric",
        "aoa-bounded-change-quality",
    }
    if selected_evals is not None and not relevant_names.intersection(selected_evals):
        return []

    issues: list[ValidationIssue] = []
    eval_dir = source_eval_dir(repo_root, "aoa-eval-integrity-check")
    eval_text = read_text_or_issue(
        eval_dir / "EVAL.md",
        issues,
        root=repo_root,
    )
    review_text = read_text_or_issue(
        eval_dir / "notes" / "review-contract.md",
        issues,
        root=repo_root,
    )
    example_report_location = "evals/capability/aoa-eval-integrity-check/examples/example-report.md"
    example_report_text = read_text_or_issue(
        eval_dir / "examples" / "example-report.md",
        issues,
        root=repo_root,
    )
    schema_location = "evals/capability/aoa-eval-integrity-check/reports/summary.schema.json"
    schema_payload = load_json_payload(
        eval_dir / "reports" / "summary.schema.json",
        issues,
        root=repo_root,
    )
    schema_enum: list[str] = []
    if isinstance(schema_payload, dict):
        properties = schema_payload.get("properties", {})
        if isinstance(properties, dict):
            per_target_breakdown = properties.get("per_target_breakdown", {})
            if isinstance(per_target_breakdown, dict):
                items = per_target_breakdown.get("items", {})
                if isinstance(items, dict):
                    item_properties = items.get("properties", {})
                    if isinstance(item_properties, dict):
                        risk_schema = item_properties.get("integrity_risk_class", {})
                        if isinstance(risk_schema, dict):
                            raw_enum = risk_schema.get("enum", [])
                            if isinstance(raw_enum, list):
                                schema_enum = [
                                    item
                                    for item in raw_enum
                                    if isinstance(item, str)
                                ]
    if tuple(schema_enum) != INTEGRITY_RISK_CLASSES:
        issues.append(
            ValidationIssue(
                schema_location,
                "integrity_risk_class enum must match the public integrity risk taxonomy",
            )
        )

    for phrase in INTEGRITY_RISK_CLASSES:
        if phrase not in review_text:
            issues.append(
                ValidationIssue(
                    "evals/capability/aoa-eval-integrity-check/notes/review-contract.md",
                    f"integrity review contract must mention '{phrase}'",
                )
            )
        if phrase not in eval_text and phrase not in review_text:
            issues.append(
                ValidationIssue(
                    "evals/capability/aoa-eval-integrity-check/EVAL.md",
                    f"integrity sidecar surfaces must mention '{phrase}' in EVAL.md or review-contract.md",
                )
            )
        if phrase not in example_report_text:
            issues.append(
                ValidationIssue(
                    example_report_location,
                    f"integrity example report must mention '{phrase}'",
                )
            )
    return issues


__all__ = ("validate_integrity_taxonomy_surfaces",)
