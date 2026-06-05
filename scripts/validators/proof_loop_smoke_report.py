"""Proof-loop route-smoke report boundary checks."""

from __future__ import annotations

from pathlib import Path

from validators import proof_loop_common as common
from validators.common import ValidationIssue


DECISION_RECORDS_README_NAME = common.DECISION_RECORDS_README_NAME
PROOF_LOOP_MECHANIC_README_NAME = common.PROOF_LOOP_MECHANIC_README_NAME
PROOF_LOOP_SMOKE_REPORT_NAME = common.PROOF_LOOP_SMOKE_REPORT_NAME
PROOF_LOOP_SMOKE_DECISION_NAME = common.PROOF_LOOP_SMOKE_DECISION_NAME

PROOF_LOOP_SMOKE_REPORT_REQUIRED_TOKENS = (
    "bounded route-smoke",
    "proof question -> selection route -> source proof object",
    "candidate evidence packet",
    "bundle-local review",
    "aoa-verification-honesty",
    "no eval result receipt",
    "no bundle promotion",
    "defer/handoff",
    "No runtime candidate packet is accepted by this smoke",
    "No sibling proof ref is required by this smoke",
    "parts/AGENTS.md#validation",
)
PROOF_LOOP_SMOKE_DECISION_REQUIRED_TOKENS = (
    PROOF_LOOP_SMOKE_REPORT_NAME,
    "aoa-verification-honesty",
    "bounded route-smoke",
    "no eval result receipt",
    "no bundle promotion",
    "no runtime dispatch",
    "no sibling-owner approval",
)


def validate_proof_loop_smoke_report_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    report_text = common.require_tokens(
        repo_root=repo_root,
        path_name=PROOF_LOOP_SMOKE_REPORT_NAME,
        tokens=PROOF_LOOP_SMOKE_REPORT_REQUIRED_TOKENS,
        issues=issues,
    )
    if report_text and common.markdown_python_commands(report_text):
        issues.append(
            ValidationIssue(
                PROOF_LOOP_SMOKE_REPORT_NAME,
                "bounded route-smoke report must route executable validation commands to mechanics/proof-loop/parts/AGENTS.md",
            )
        )
    for path_name, tokens in (
        (PROOF_LOOP_SMOKE_DECISION_NAME, PROOF_LOOP_SMOKE_DECISION_REQUIRED_TOKENS),
        (
            PROOF_LOOP_MECHANIC_README_NAME,
            (PROOF_LOOP_SMOKE_REPORT_NAME, "bounded route-smoke", "no eval result receipt"),
        ),
        ("reports/README.md", (PROOF_LOOP_SMOKE_REPORT_NAME, "route-smoke report")),
        (
            DECISION_RECORDS_README_NAME,
            (PROOF_LOOP_SMOKE_DECISION_NAME, "Further proof-loop examples"),
        ),
    ):
        common.require_tokens(repo_root=repo_root, path_name=path_name, tokens=tokens, issues=issues)
    return issues
