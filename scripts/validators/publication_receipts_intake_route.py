"""Publication receipt intake dry-review route-token checks."""

from __future__ import annotations

from pathlib import Path

from validators import publication_receipts_intake_common as common
from validators import publication_receipts_route_helpers as route_helpers
from validators import publication_receipts_route_paths as route_paths
from validators import publication_receipts_route_tokens as route_tokens
from validators.publication_receipts_common import ValidationIssue


RECEIPT_INTAKE_DRY_REVIEW_NAME = common.RECEIPT_INTAKE_DRY_REVIEW_NAME
RECEIPT_INTAKE_DRY_REVIEW_DECISION_NAME = common.RECEIPT_INTAKE_DRY_REVIEW_DECISION_NAME


def validate_receipt_intake_route_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    route_helpers.require_tokens(
        repo_root=repo_root,
        path_name=RECEIPT_INTAKE_DRY_REVIEW_NAME,
        tokens=route_tokens.RECEIPT_INTAKE_DRY_REVIEW_REQUIRED_TOKENS,
        issues=issues,
    )
    route_helpers.require_tokens(
        repo_root=repo_root,
        path_name=RECEIPT_INTAKE_DRY_REVIEW_DECISION_NAME,
        tokens=route_tokens.RECEIPT_INTAKE_DRY_REVIEW_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    for path_name, tokens in (
        (
            route_paths.PROOF_LOOP_MECHANIC_README_NAME,
            (
                RECEIPT_INTAKE_DRY_REVIEW_NAME,
                "Receipt Intake Dry Review",
                "`receipt_status` stays `not_published`",
            ),
        ),
        (
            route_paths.PUBLICATION_RECEIPTS_MECHANIC_README_NAME,
            (
                RECEIPT_INTAKE_DRY_REVIEW_NAME,
                "dry review",
                "`receipt_status` as `not_published`",
            ),
        ),
        ("reports/README.md", (RECEIPT_INTAKE_DRY_REVIEW_NAME, "receipt-intake", "`not_published`")),
        ("ROADMAP.md", ("Publication receipt posture", "mechanics/publication-receipts/README.md")),
        ("CHANGELOG.md", (RECEIPT_INTAKE_DRY_REVIEW_NAME, "validator coverage")),
        (
            "docs/decisions/README.md",
            (
                RECEIPT_INTAKE_DRY_REVIEW_DECISION_NAME,
                "real eval-result receipt publication",
            ),
        ),
    ):
        route_helpers.require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=tokens,
            issues=issues,
        )
    return issues
