"""Shared publication receipt intake dry-review constants and helpers."""

from __future__ import annotations

from pathlib import Path

from validators import publication_receipts_route_paths as route_paths
from validators.publication_receipts_common import (
    EVAL_REPORT_INDEX_NAME,
    EVAL_RESULT_RECEIPT_SCHEMA_PATH,
    LIVE_EVAL_RECEIPT_LOG_NAME,
    STATS_EVENT_ENVELOPE_SCHEMA_PATH,
    ValidationIssue,
    load_json_payload,
)


RECEIPT_INTAKE_DRY_REVIEW_NAME = route_paths.RECEIPT_INTAKE_DRY_REVIEW_NAME
RECEIPT_INTAKE_DRY_REVIEW_DECISION_NAME = route_paths.RECEIPT_INTAKE_DRY_REVIEW_DECISION_NAME
PROOF_LOOP_LOCAL_REPORT_NAME = route_paths.PROOF_LOOP_LOCAL_REPORT_NAME

PUBLISHABLE_RECEIPT_FIELDS = (
    "event_kind",
    "event_id",
    "observed_at",
    "run_ref",
    "session_ref",
    "actor_ref",
    "object_ref",
    "evidence_refs",
    "payload",
)
EXPECTED_TOP_LEVEL = {
    "artifact_kind": "receipt_intake_dry_review",
    "schema_version": 1,
    "review_id": "eval-result-receipt-intake-dry-review-v1",
    "reviewed_at": "2026-05-19",
}
EXPECTED_SOURCE_REFS = {
    "source_report_ref": f"repo:aoa-evals/{PROOF_LOOP_LOCAL_REPORT_NAME}",
    "source_bundle_ref": "repo:aoa-evals/evals/workflow/aoa-verification-honesty/EVAL.md",
    "source_manifest_ref": "repo:aoa-evals/evals/workflow/aoa-verification-honesty/eval.yaml",
    "report_index_ref": "repo:aoa-evals/generated/eval_report_index.min.json",
    "receipt_payload_schema_ref": f"repo:aoa-evals/{EVAL_RESULT_RECEIPT_SCHEMA_PATH}",
    "event_envelope_schema_ref": f"repo:aoa-evals/{STATS_EVENT_ENVELOPE_SCHEMA_PATH}",
    "publisher_ref": f"repo:aoa-evals/{route_paths.EVAL_RESULT_RECEIPT_PUBLISHER_NAME}",
    "owner_local_log_ref": f"repo:aoa-evals/{LIVE_EVAL_RECEIPT_LOG_NAME}",
}


def load_dry_review_payload(
    repo_root: Path,
    issues: list[ValidationIssue],
) -> dict | None:
    payload = load_json_payload(repo_root / RECEIPT_INTAKE_DRY_REVIEW_NAME, issues, root=repo_root)
    if not isinstance(payload, dict):
        if payload is not None:
            issues.append(
                ValidationIssue(
                    RECEIPT_INTAKE_DRY_REVIEW_NAME,
                    "receipt intake dry review must be a JSON object",
                )
            )
        return None
    return payload


def receipt_payload_schema_path(repo_root: Path, *, fallback_repo_root: Path) -> Path:
    payload_schema_path = repo_root / EVAL_RESULT_RECEIPT_SCHEMA_PATH
    if not payload_schema_path.exists() and repo_root != fallback_repo_root:
        return fallback_repo_root / EVAL_RESULT_RECEIPT_SCHEMA_PATH
    return payload_schema_path
