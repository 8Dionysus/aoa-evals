"""Release-support route-card, part-contract, provenance, and legacy checks."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue
from validators.release_support_route_tokens import (
    DECISION_RECORDS_README_NAME,
    require_route_tokens,
)

RELEASE_SUPPORT_MECHANIC_README_NAME = "mechanics/release-support/README.md"
RELEASE_SUPPORT_MECHANIC_AGENTS_NAME = "mechanics/release-support/AGENTS.md"
RELEASE_SUPPORT_MECHANIC_PARTS_NAME = "mechanics/release-support/PARTS.md"
RELEASE_SUPPORT_MECHANIC_PARTS_README_NAME = "mechanics/release-support/parts/README.md"
RELEASE_SUPPORT_MECHANIC_PROVENANCE_NAME = "mechanics/release-support/PROVENANCE.md"
RELEASE_SUPPORT_READINESS_AUDIT_PART_README_NAME = (
    "mechanics/release-support/parts/readiness-audit/README.md"
)
RELEASE_SUPPORT_STRATEGIC_CLOSEOUT_PART_README_NAME = (
    "mechanics/release-support/parts/strategic-closeout/README.md"
)
RELEASE_SUPPORT_PR_HANDOFF_PART_README_NAME = "mechanics/release-support/parts/pr-handoff/README.md"
RELEASE_SUPPORT_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0058-release-support-part-contract-guard.md"
)
RELEASE_SUPPORT_LEGACY_INDEX_NAME = "mechanics/release-support/legacy/INDEX.md"
RELEASE_SUPPORT_LEGACY_DISTILLATION_LOG_NAME = (
    "mechanics/release-support/legacy/DISTILLATION_LOG.md"
)
RELEASE_SUPPORT_LEGACY_RAW_README_NAME = "mechanics/release-support/legacy/raw/README.md"
RELEASE_SUPPORT_MECHANIC_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0014-release-support-mechanic-package.md"
)

MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS = (
    "`PROVENANCE.md` is the active-to-archive bridge for this mechanic.",
    "Use active surfaces first:",
    "DIRECTION.md",
    "PARTS.md",
    "parts/",
    "legacy archive",
    "legacy/README.md",
    "owns its own details",
    "archive details stay in the legacy archive",
)
RELEASE_SUPPORT_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "PARTS.md",
    "docs/operations/RELEASING.md",
    "CHANGELOG.md",
    "scripts/release_check.py",
    ".github/workflows/repo-validation.yml",
    "parts/readiness-audit",
    "parts/strategic-closeout",
    "parts/pr-handoff",
    "tests/test_release_support_readiness_audit.py",
    "tests/test_strategic_closeout_audit.py",
    "tests/test_release_prep_pr_handoff.py",
    "Repo Validation",
    "pre-PR owner landing handoff",
    "bounded release scope",
    "changelog narrative",
    "GitHub release notes",
    "eval claim strength stays with source proof surfaces",
    "AGENTS.md#validation",
    "owns command execution",
)
RELEASE_SUPPORT_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "bounded `aoa-evals` release",
    "mechanics/release-support/PARTS.md",
    "mechanics/release-support/parts/",
    "CHANGELOG.md",
    "scripts/release_check.py",
    "Repo Validation",
    "plain tag-shaped",
    "bundle-local review",
    "python scripts/release_check.py",
)
RELEASE_SUPPORT_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/release-support/",
    "mechanics/release-support/parts/",
    "bounded release scope",
    "changelog narrative",
    "release audit",
    "Repo Validation",
    "does not create a tag",
    "release notes",
    "bundle-local `EVAL.md`",
)
RELEASE_SUPPORT_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "Release Support / Part Index",
    "CHANGELOG.md",
    "docs/operations/RELEASING.md",
    "scripts/release_check.py",
    ".github/workflows/repo-validation.yml",
    "Readiness Audit",
    "Strategic Closeout",
    "PR Handoff",
    "Live publication state is",
)
RELEASE_SUPPORT_PARTS_README_REQUIRED_TOKENS = (
    "Release Support / Parts Route",
    "Readiness Audit",
    "Strategic Closeout",
    "PR Handoff",
    "current git and GitHub evidence own live branch",
)
RELEASE_SUPPORT_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
RELEASE_SUPPORT_PART_README_COMMON_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "VALIDATION.md",
    "parent `parts/AGENTS.md` lane",
)
RELEASE_SUPPORT_READINESS_AUDIT_PART_REQUIRED_TOKENS = (
    "Readiness Audit",
    "release_support_readiness_audit",
    "publication_boundary",
    "GitHub PR approval and Repo Validation",
    "current git branch/merge state",
    "current goal review",
    "not_complete",
    "readiness audit treated as tag",
) + RELEASE_SUPPORT_PART_README_COMMON_REQUIRED_TOKENS
RELEASE_SUPPORT_STRATEGIC_CLOSEOUT_PART_REQUIRED_TOKENS = (
    "Strategic Closeout",
    "strategic_closeout_audit",
    "goal_completion_status",
    "not_complete",
    "owner-visible final audit",
    "local handoff readiness as goal completion",
    "open landing requirements stay visible",
) + RELEASE_SUPPORT_PART_README_COMMON_REQUIRED_TOKENS
RELEASE_SUPPORT_PR_HANDOFF_PART_REQUIRED_TOKENS = (
    "PR Handoff",
    "release_prep_pr_handoff",
    "pre_handoff_github_status",
    "draft PR body",
    "Live GitHub state is owned by current local git",
    "snapshot treated as created branch",
    "current git and GitHub evidence replace this snapshot",
) + RELEASE_SUPPORT_PART_README_COMMON_REQUIRED_TOKENS
RELEASE_SUPPORT_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS = (
    "Release Support Part Contract Guard",
    "mechanics/release-support/parts/readiness-audit/README.md",
    "mechanics/release-support/parts/strategic-closeout/README.md",
    "mechanics/release-support/parts/pr-handoff/README.md",
    "part-level contracts",
    "readiness-audit",
    "strategic-closeout",
    "pr-handoff",
    "stronger owner split",
    "stop-lines",
    "not_complete",
)
RELEASE_SUPPORT_LEGACY_INDEX_REQUIRED_TOKENS = (
    "mechanics/proof-release/",
    "mechanics/release-support/",
    "reports/proof-release-readiness-audit-v1.json",
    "mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json",
    "tests/test_proof_release_readiness_audit.py",
    "mechanics/release-support/parts/readiness-audit/tests/test_release_support_readiness_audit.py",
    "docs/decisions/0014-proof-release-mechanic-package.md",
    "docs/decisions/AOA-EV-D-0014-release-support-mechanic-package.md",
)
RELEASE_SUPPORT_LEGACY_DISTILLATION_REQUIRED_TOKENS = (
    "proof-release",
    "release-support",
    "readiness-audit",
    "strategic-closeout",
    "pr-handoff",
    "Current route:",
    "new release-support work starts in the owning active part",
)
RELEASE_SUPPORT_LEGACY_RAW_README_REQUIRED_TOKENS = (
    "No raw payload copies",
    "git history",
    "active parts",
)


def validate_release_support_route_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    require_route_tokens(
        repo_root,
        issues,
        (
            (RELEASE_SUPPORT_MECHANIC_README_NAME, RELEASE_SUPPORT_MECHANIC_REQUIRED_TOKENS),
            (RELEASE_SUPPORT_MECHANIC_AGENTS_NAME, RELEASE_SUPPORT_MECHANIC_AGENTS_REQUIRED_TOKENS),
            (RELEASE_SUPPORT_MECHANIC_PARTS_NAME, RELEASE_SUPPORT_MECHANIC_PARTS_REQUIRED_TOKENS),
            (RELEASE_SUPPORT_MECHANIC_PARTS_README_NAME, RELEASE_SUPPORT_PARTS_README_REQUIRED_TOKENS),
            (
                RELEASE_SUPPORT_READINESS_AUDIT_PART_README_NAME,
                RELEASE_SUPPORT_READINESS_AUDIT_PART_REQUIRED_TOKENS,
            ),
            (
                RELEASE_SUPPORT_STRATEGIC_CLOSEOUT_PART_README_NAME,
                RELEASE_SUPPORT_STRATEGIC_CLOSEOUT_PART_REQUIRED_TOKENS,
            ),
            (RELEASE_SUPPORT_PR_HANDOFF_PART_README_NAME, RELEASE_SUPPORT_PR_HANDOFF_PART_REQUIRED_TOKENS),
            (
                RELEASE_SUPPORT_PART_CONTRACT_GUARD_DECISION_NAME,
                RELEASE_SUPPORT_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS,
            ),
            (
                DECISION_RECORDS_README_NAME,
                (RELEASE_SUPPORT_PART_CONTRACT_GUARD_DECISION_NAME, "Release Support Part Contract Guard"),
            ),
            (RELEASE_SUPPORT_MECHANIC_PROVENANCE_NAME, RELEASE_SUPPORT_MECHANIC_PROVENANCE_REQUIRED_TOKENS),
            (RELEASE_SUPPORT_LEGACY_INDEX_NAME, RELEASE_SUPPORT_LEGACY_INDEX_REQUIRED_TOKENS),
            (RELEASE_SUPPORT_LEGACY_DISTILLATION_LOG_NAME, RELEASE_SUPPORT_LEGACY_DISTILLATION_REQUIRED_TOKENS),
            (RELEASE_SUPPORT_LEGACY_RAW_README_NAME, RELEASE_SUPPORT_LEGACY_RAW_README_REQUIRED_TOKENS),
            (RELEASE_SUPPORT_MECHANIC_DECISION_NAME, RELEASE_SUPPORT_MECHANIC_DECISION_REQUIRED_TOKENS),
        ),
    )
    return issues
