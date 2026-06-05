"""Publication receipt intake source-alignment and non-publication boundary checks."""

from __future__ import annotations

from pathlib import Path

from validators import publication_receipts_intake_common as common
from validators.publication_receipts_common import ValidationIssue


RECEIPT_INTAKE_DRY_REVIEW_NAME = common.RECEIPT_INTAKE_DRY_REVIEW_NAME


def validate_receipt_intake_boundary_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    payload = common.load_dry_review_payload(repo_root, issues)
    if payload is None:
        return issues

    source_alignment = payload.get("source_alignment")
    if isinstance(source_alignment, dict):
        for key in (
            "eval_name_matches_report",
            "bundle_status_matches_manifest",
            "report_format_matches_manifest",
            "verdict_matches_report",
        ):
            if source_alignment.get(key) is not True:
                issues.append(ValidationIssue(f"{RECEIPT_INTAKE_DRY_REVIEW_NAME}.source_alignment", f"{key} must be true"))
        if source_alignment.get("case_count_source") != "per_case_breakdown length":
            issues.append(
                ValidationIssue(
                    f"{RECEIPT_INTAKE_DRY_REVIEW_NAME}.source_alignment",
                    "case_count_source must stay 'per_case_breakdown length'",
                )
            )
    else:
        issues.append(ValidationIssue(RECEIPT_INTAKE_DRY_REVIEW_NAME, "source_alignment must be a JSON object"))

    checks = payload.get("intake_checks")
    if isinstance(checks, list):
        by_id = {entry.get("check_id"): entry for entry in checks if isinstance(entry, dict)}
        expected_check_results = {
            "source_report_exists": "pass",
            "source_report_is_indexed": "pass",
            "candidate_payload_preview_validates_against_payload_schema": "pass",
            "stats_event_envelope_created": "not_attempted",
            "receipt_publisher_run": "not_attempted",
            "owner_local_live_log_append": "not_attempted",
        }
        for check_id, expected_result in expected_check_results.items():
            entry = by_id.get(check_id)
            if not isinstance(entry, dict):
                issues.append(ValidationIssue(f"{RECEIPT_INTAKE_DRY_REVIEW_NAME}.intake_checks", f"missing check_id {check_id!r}"))
                continue
            if entry.get("result") != expected_result:
                issues.append(
                    ValidationIssue(
                        f"{RECEIPT_INTAKE_DRY_REVIEW_NAME}.intake_checks.{check_id}",
                        f"result must be {expected_result!r}",
                    )
                )
            evidence_ref = entry.get("evidence_ref")
            if not isinstance(evidence_ref, str) or not evidence_ref.startswith("repo:aoa-evals/"):
                issues.append(
                    ValidationIssue(
                        f"{RECEIPT_INTAKE_DRY_REVIEW_NAME}.intake_checks.{check_id}",
                        "evidence_ref must point at a repo:aoa-evals/ surface",
                    )
                )
    else:
        issues.append(ValidationIssue(RECEIPT_INTAKE_DRY_REVIEW_NAME, "intake_checks must be a list"))

    publication_boundary = payload.get("publication_boundary")
    if isinstance(publication_boundary, dict):
        expected_boundary_values = {
            "publication_status": "dry_review_only",
            "receipt_status": "not_published",
            "event_envelope_status": "not_created",
            "live_log_append_status": "not_attempted",
            "publisher_execution_status": "not_attempted",
        }
        for key, expected in expected_boundary_values.items():
            if publication_boundary.get(key) != expected:
                issues.append(
                    ValidationIssue(
                        f"{RECEIPT_INTAKE_DRY_REVIEW_NAME}.publication_boundary",
                        f"{key} must be {expected!r}",
                    )
                )
        boundary = publication_boundary.get("boundary")
        if not isinstance(boundary, str):
            issues.append(
                ValidationIssue(
                    f"{RECEIPT_INTAKE_DRY_REVIEW_NAME}.publication_boundary",
                    "boundary must be a string",
                )
            )
        else:
            for token in (
                "receipt envelope pressure",
                "stats sidecar pressure",
                "live log pressure",
                "proof or bundle promotion pressure",
                "runtime acceptance pressure",
            ):
                if token not in boundary:
                    issues.append(
                        ValidationIssue(
                            f"{RECEIPT_INTAKE_DRY_REVIEW_NAME}.publication_boundary.boundary",
                            f"boundary must mention '{token}'",
                        )
                    )
    else:
        issues.append(ValidationIssue(RECEIPT_INTAKE_DRY_REVIEW_NAME, "publication_boundary must be a JSON object"))

    claim_limit = payload.get("claim_limit")
    if not isinstance(claim_limit, str):
        issues.append(ValidationIssue(RECEIPT_INTAKE_DRY_REVIEW_NAME, "claim_limit must be a string"))
    else:
        for token in (
            "Publication pressure routes",
            "live receipt memory append routes",
            "runtime evidence acceptance routes",
            "bundle promotion routes",
            "strategic closeout stays with the goal owner",
        ):
            if token not in claim_limit:
                issues.append(ValidationIssue(RECEIPT_INTAKE_DRY_REVIEW_NAME, f"claim_limit must mention '{token}'"))
    return issues
