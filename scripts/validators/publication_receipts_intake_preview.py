"""Publication receipt intake candidate payload preview checks."""

from __future__ import annotations

from pathlib import Path

from jsonschema import Draft202012Validator, SchemaError

from validators import publication_receipts_intake_common as common
from validators.publication_receipts_common import (
    EVAL_REPORT_INDEX_NAME,
    EVAL_RESULT_RECEIPT_SCHEMA_NAME,
    EVAL_RESULT_RECEIPT_SCHEMA_PATH,
    ValidationIssue,
    get_schema_validator_with_format,
    load_json_payload,
    load_yaml_file,
    source_eval_dir,
    validate_against_schema,
)


RECEIPT_INTAKE_DRY_REVIEW_NAME = common.RECEIPT_INTAKE_DRY_REVIEW_NAME


def _payload_schema_validator(
    repo_root: Path,
    *,
    fallback_repo_root: Path,
    issues: list[ValidationIssue],
) -> Draft202012Validator | None:
    payload_schema_path = common.receipt_payload_schema_path(
        repo_root,
        fallback_repo_root=fallback_repo_root,
    )
    payload_schema = load_json_payload(
        payload_schema_path,
        issues,
        root=payload_schema_path.parents[5],
    )
    if not isinstance(payload_schema, dict):
        return None
    try:
        Draft202012Validator.check_schema(payload_schema)
    except SchemaError as exc:
        issues.append(
            ValidationIssue(
                EVAL_RESULT_RECEIPT_SCHEMA_PATH,
                f"invalid JSON schema: {exc.message}",
            )
        )
        return None
    return get_schema_validator_with_format(payload_schema)


def validate_receipt_intake_candidate_preview_surface(
    repo_root: Path,
    *,
    fallback_repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    payload = common.load_dry_review_payload(repo_root, issues)
    if payload is None:
        return issues

    source_report_path = repo_root / common.PROOF_LOOP_LOCAL_REPORT_NAME
    source_report = load_json_payload(source_report_path, issues, root=repo_root)
    manifest = load_yaml_file(
        source_eval_dir(repo_root, "aoa-verification-honesty") / "eval.yaml",
        issues,
        root=repo_root,
    )
    report_index = load_json_payload(repo_root / EVAL_REPORT_INDEX_NAME, issues, root=repo_root)
    preview = payload.get("candidate_payload_preview")
    payload_validator = _payload_schema_validator(
        repo_root,
        fallback_repo_root=fallback_repo_root,
        issues=issues,
    )

    if isinstance(preview, dict):
        if payload_validator is not None:
            validate_against_schema(
                preview,
                EVAL_RESULT_RECEIPT_SCHEMA_NAME,
                f"{RECEIPT_INTAKE_DRY_REVIEW_NAME}.candidate_payload_preview",
                issues,
                validator=payload_validator,
                fallback_repo_root=fallback_repo_root,
            )

        if isinstance(source_report, dict):
            expected_report_values = {
                "eval_name": source_report.get("eval_name"),
                "bundle_status": source_report.get("bundle_status"),
                "verdict": source_report.get("verdict"),
            }
            for key, expected in expected_report_values.items():
                if preview.get(key) != expected:
                    issues.append(
                        ValidationIssue(
                            f"{RECEIPT_INTAKE_DRY_REVIEW_NAME}.candidate_payload_preview",
                            f"{key} must match source report value {expected!r}",
                        )
                    )
            case_count = len(source_report.get("per_case_breakdown", []))
            if preview.get("case_count") != case_count:
                issues.append(
                    ValidationIssue(
                        f"{RECEIPT_INTAKE_DRY_REVIEW_NAME}.candidate_payload_preview",
                        "case_count must match source report per_case_breakdown length",
                    )
                )

        if isinstance(manifest, dict):
            if preview.get("report_format") != manifest.get("report_format"):
                issues.append(
                    ValidationIssue(
                        f"{RECEIPT_INTAKE_DRY_REVIEW_NAME}.candidate_payload_preview",
                        "report_format must match source manifest report_format",
                    )
                )
            if preview.get("bundle_status") != manifest.get("status"):
                issues.append(
                    ValidationIssue(
                        f"{RECEIPT_INTAKE_DRY_REVIEW_NAME}.candidate_payload_preview",
                        "bundle_status must match source manifest status",
                    )
                )
            if manifest.get("baseline_mode") == "none" and preview.get("comparison_mode") != "none":
                issues.append(
                    ValidationIssue(
                        f"{RECEIPT_INTAKE_DRY_REVIEW_NAME}.candidate_payload_preview",
                        "comparison_mode must stay 'none' when the source manifest baseline_mode is 'none'",
                    )
                )

        if preview.get("claim_scope") != "bundle_scoped":
            issues.append(
                ValidationIssue(
                    f"{RECEIPT_INTAKE_DRY_REVIEW_NAME}.candidate_payload_preview",
                    "claim_scope must stay 'bundle_scoped' for this dry review",
                )
            )
        if preview.get("bundle_ref") != common.EXPECTED_SOURCE_REFS["source_bundle_ref"]:
            issues.append(
                ValidationIssue(
                    f"{RECEIPT_INTAKE_DRY_REVIEW_NAME}.candidate_payload_preview",
                    "bundle_ref must match the dry review source_bundle_ref",
                )
            )
        if preview.get("report_ref") != common.EXPECTED_SOURCE_REFS["source_report_ref"]:
            issues.append(
                ValidationIssue(
                    f"{RECEIPT_INTAKE_DRY_REVIEW_NAME}.candidate_payload_preview",
                    "report_ref must match the dry review source_report_ref",
                )
            )
        interpretation_bound = preview.get("interpretation_bound")
        if not isinstance(interpretation_bound, str):
            issues.append(
                ValidationIssue(
                    f"{RECEIPT_INTAKE_DRY_REVIEW_NAME}.candidate_payload_preview",
                    "interpretation_bound must be a string",
                )
            )
        else:
            for token in (
                "Dry review only.",
                "publication pressure routes to a receipt envelope",
                ".aoa/live_receipts/",
                "verdict meaning stays with bundle-local review",
            ):
                if token not in interpretation_bound:
                    issues.append(
                        ValidationIssue(
                            f"{RECEIPT_INTAKE_DRY_REVIEW_NAME}.candidate_payload_preview.interpretation_bound",
                            f"interpretation_bound must mention '{token}'",
                        )
                    )
    else:
        issues.append(ValidationIssue(RECEIPT_INTAKE_DRY_REVIEW_NAME, "candidate_payload_preview must be a JSON object"))

    if isinstance(report_index, dict):
        reports = report_index.get("reports")
        indexed_paths = {
            entry.get("source_report_path")
            for entry in reports
            if isinstance(entry, dict)
        } if isinstance(reports, list) else set()
        if common.PROOF_LOOP_LOCAL_REPORT_NAME not in indexed_paths:
            issues.append(
                ValidationIssue(
                    RECEIPT_INTAKE_DRY_REVIEW_NAME,
                    f"report_index_ref must index {common.PROOF_LOOP_LOCAL_REPORT_NAME}",
                )
            )
    return issues
