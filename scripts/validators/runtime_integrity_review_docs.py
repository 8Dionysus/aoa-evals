"""Runtime integrity review guide and landing-note checks."""

from __future__ import annotations

from pathlib import Path

from validators import runtime_integrity_review_common as common
from validators.common import ValidationIssue, read_text_or_issue, relative_location


RUNTIME_INTEGRITY_REVIEW_DOC_NAME = common.RUNTIME_INTEGRITY_REVIEW_DOC_NAME
RUNTIME_INTEGRITY_REVIEW_REQUIRED_TOKENS = common.RUNTIME_INTEGRITY_REVIEW_REQUIRED_TOKENS
RUNTIME_INTEGRITY_REVIEW_LANDING_TOKENS = common.RUNTIME_INTEGRITY_REVIEW_LANDING_TOKENS


def validate_runtime_integrity_review_doc_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    doc_path = repo_root / RUNTIME_INTEGRITY_REVIEW_DOC_NAME
    docs_map_path = repo_root / "docs" / "README.md"
    landing_path = (
        repo_root
        / "mechanics"
        / "agon"
        / "legacy"
        / "raw"
        / "AGON_WAVE10_EVAL_LANDING.md"
    )

    doc_text = read_text_or_issue(doc_path, issues, root=repo_root)
    if doc_text:
        for token in RUNTIME_INTEGRITY_REVIEW_REQUIRED_TOKENS:
            if token not in doc_text:
                issues.append(
                    ValidationIssue(
                        relative_location(doc_path, repo_root),
                        f"runtime integrity review guide must mention '{token}'",
                    )
                )

    read_text_or_issue(docs_map_path, issues, root=repo_root)

    landing_text = read_text_or_issue(landing_path, issues, root=repo_root)
    if landing_text:
        for token in RUNTIME_INTEGRITY_REVIEW_LANDING_TOKENS:
            if token not in landing_text:
                issues.append(
                    ValidationIssue(
                        relative_location(landing_path, repo_root),
                        f"Agon Wave X landing note must mention '{token}'",
                    )
                )
    return issues
