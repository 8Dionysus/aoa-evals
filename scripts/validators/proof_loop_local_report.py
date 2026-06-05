"""Proof-loop bundle-local report boundary checks."""

from __future__ import annotations

from pathlib import Path

from validators import proof_loop_common as common
from validators.common import ValidationIssue


DECISION_RECORDS_README_NAME = common.DECISION_RECORDS_README_NAME
PROOF_INFRA_MECHANIC_README_NAME = common.PROOF_INFRA_MECHANIC_README_NAME
PROOF_LOOP_MECHANIC_README_NAME = common.PROOF_LOOP_MECHANIC_README_NAME
PROOF_LOOP_LOCAL_REPORT_NAME = common.PROOF_LOOP_LOCAL_REPORT_NAME
PROOF_LOOP_LOCAL_REPORT_DECISION_NAME = common.PROOF_LOOP_LOCAL_REPORT_DECISION_NAME

PROOF_LOOP_LOCAL_REPORT_REQUIRED_TOKENS = (
    "aoa-verification-honesty",
    "aoa-evals slice 19 quest lifecycle contract",
    "No receipt publisher run was attempted",
    "No runtime mutation or machine maintenance check was attempted",
    "`python scripts/release_check.py`",
)
PROOF_LOOP_LOCAL_REPORT_DECISION_REQUIRED_TOKENS = (
    PROOF_LOOP_LOCAL_REPORT_NAME,
    "bundle-local report",
    "reports/summary.schema.json",
    "validate every bundle-local `*.report.json`",
    "no eval result receipt",
    "no bundle status is promoted",
)


def validate_proof_loop_local_report_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name, tokens in (
        (PROOF_LOOP_LOCAL_REPORT_NAME, PROOF_LOOP_LOCAL_REPORT_REQUIRED_TOKENS),
        (PROOF_LOOP_LOCAL_REPORT_DECISION_NAME, PROOF_LOOP_LOCAL_REPORT_DECISION_REQUIRED_TOKENS),
        (
            PROOF_LOOP_MECHANIC_README_NAME,
            (PROOF_LOOP_LOCAL_REPORT_NAME, "First Bundle-Local Report", "no eval result receipt"),
        ),
        (
            PROOF_INFRA_MECHANIC_README_NAME,
            ("`*.report.json`", "`evals/<family>/<eval>/reports/summary.schema.json`"),
        ),
        ("ROADMAP.md", ("Proof loop route", "mechanics/proof-loop/README.md")),
        ("CHANGELOG.md", (PROOF_LOOP_LOCAL_REPORT_NAME, "bundle-local report validation")),
        (DECISION_RECORDS_README_NAME, (PROOF_LOOP_LOCAL_REPORT_DECISION_NAME, "Further proof-loop examples")),
    ):
        common.require_tokens(repo_root=repo_root, path_name=path_name, tokens=tokens, issues=issues)
    return issues
