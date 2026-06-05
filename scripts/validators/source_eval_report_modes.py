"""Comparative source eval report mode validation."""

from __future__ import annotations

from typing import Any

from validators.common import ValidationIssue


def validate_comparative_report_mode_contract(
    schema: dict[str, Any],
    example_payload: Any,
    *,
    required_mode: str | None,
    schema_location: str,
    example_location: str,
    issues: list[ValidationIssue],
) -> None:
    if required_mode is None:
        return

    required_fields = schema.get("required", [])
    if "comparison_mode" not in required_fields:
        issues.append(
            ValidationIssue(
                schema_location,
                "comparative-summary report schema must require 'comparison_mode'",
            )
        )
    properties = schema.get("properties", {})
    comparison_mode_schema = properties.get("comparison_mode")
    if not isinstance(comparison_mode_schema, dict) or comparison_mode_schema.get("const") != required_mode:
        issues.append(
            ValidationIssue(
                schema_location,
                f"comparative-summary report schema must pin comparison_mode to '{required_mode}'",
            )
        )

    if not isinstance(example_payload, dict):
        return
    if example_payload.get("comparison_mode") != required_mode:
        issues.append(
            ValidationIssue(
                example_location,
                f"comparative-summary report example must set comparison_mode to '{required_mode}'",
            )
        )


__all__ = ("validate_comparative_report_mode_contract",)
