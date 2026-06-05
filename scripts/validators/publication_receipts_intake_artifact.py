"""Publication receipt intake dry-review artifact shape and reference checks."""

from __future__ import annotations

from pathlib import Path

from validators import publication_receipts_intake_common as common
from validators.publication_receipts_common import ValidationIssue


RECEIPT_INTAKE_DRY_REVIEW_NAME = common.RECEIPT_INTAKE_DRY_REVIEW_NAME


def validate_receipt_intake_artifact_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    payload = common.load_dry_review_payload(repo_root, issues)
    if payload is None:
        return issues

    for field in common.PUBLISHABLE_RECEIPT_FIELDS:
        if field in payload:
            issues.append(
                ValidationIssue(
                    RECEIPT_INTAKE_DRY_REVIEW_NAME,
                    f"receipt intake dry review must not contain publishable receipt field {field!r}",
                )
            )

    for key, expected in common.EXPECTED_SOURCE_REFS.items():
        value = payload.get(key)
        if value != expected:
            issues.append(ValidationIssue(RECEIPT_INTAKE_DRY_REVIEW_NAME, f"{key} must be {expected!r}"))
            continue
        local_path = repo_root / expected.removeprefix("repo:aoa-evals/")
        if not local_path.exists():
            issues.append(ValidationIssue(RECEIPT_INTAKE_DRY_REVIEW_NAME, f"{key} target is missing: {expected}"))

    for key, expected in common.EXPECTED_TOP_LEVEL.items():
        if payload.get(key) != expected:
            issues.append(ValidationIssue(RECEIPT_INTAKE_DRY_REVIEW_NAME, f"{key} must be {expected!r}"))
    return issues
