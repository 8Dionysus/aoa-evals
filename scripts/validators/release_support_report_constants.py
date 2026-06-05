"""Release-support report artifact constants."""

from __future__ import annotations

RELEASE_SUPPORT_READINESS_AUDIT_NAME = (
    "mechanics/release-support/parts/readiness-audit/reports/"
    "release-support-readiness-audit-v1.json"
)
RELEASE_SUPPORT_READINESS_AUDIT_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0025-release-support-readiness-audit.md"
)
STRATEGIC_CLOSEOUT_AUDIT_NAME = (
    "mechanics/release-support/parts/strategic-closeout/reports/"
    "strategic-closeout-audit-v1.json"
)
STRATEGIC_CLOSEOUT_AUDIT_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0026-strategic-closeout-audit.md"
)
RELEASE_PREP_PR_HANDOFF_NAME = (
    "mechanics/release-support/parts/pr-handoff/reports/"
    "release-prep-pr-handoff-v1.json"
)
RELEASE_PREP_PR_HANDOFF_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0027-release-prep-pr-handoff.md"
)

RELEASE_SUPPORT_READINESS_AUDIT_REQUIRED_TOKENS = (
    "release_support_readiness_audit",
    "local_release_prep_review_ready_with_open_landing",
    "accumulated_strategic_refactor_diff",
    "ready_for_release_prep_review",
    "not_published",
    "not_created",
    "not_opened",
    "not_observed_for_this_uncommitted_diff",
    "not_complete",
    "not_attempted",
    "not a release",
    "not a tag",
    "not GitHub Repo Validation",
    "not goal completion",
)
RELEASE_SUPPORT_READINESS_AUDIT_DECISION_REQUIRED_TOKENS = (
    RELEASE_SUPPORT_READINESS_AUDIT_NAME,
    "scripts/release_check.py",
    "GitHub `Repo Validation`",
    "not the same as a bounded release-prep review",
    "no tag",
    "no GitHub Release",
    "no PR approval",
    "no goal completion",
)
STRATEGIC_CLOSEOUT_AUDIT_REQUIRED_TOKENS = (
    "strategic_closeout_audit",
    "current_objective_audit_and_landing_route_in_progress_after_mechanics_validation_hardening",
    "not_complete_pending_requirement_audit_and_landing_route",
    "satisfied_for_local_refactor",
    "meta_truth_and_positive_boundary",
    "codex_maxxing_durable_loop",
    "phase_8_active_proof_loop",
    "trap_audit_and_completion_boundary",
    "does not mark the goal complete",
    "does not treat PR or GitHub landing alone as objective completion",
    "requirement-by-requirement mechanics objective audit",
    "does not publish an eval result receipt",
    "does not mutate sibling repos",
)
STRATEGIC_CLOSEOUT_AUDIT_DECISION_REQUIRED_TOKENS = (
    STRATEGIC_CLOSEOUT_AUDIT_NAME,
    "requirement-by-requirement",
    "current objective audit",
    "not a PR ritual",
    "GitHub `Repo Validation`",
    "live eval-result receipt",
    "mutate sibling repos",
)
RELEASE_PREP_PR_HANDOFF_REQUIRED_TOKENS = (
    "release_prep_pr_handoff",
    "ready_for_owner_landing_route_with_open_pr",
    "pre_pr_handoff_snapshot",
    "pre_landing_worktree_posture",
    "dirty_uncommitted_local_diff",
    "pre_handoff_github_status",
    "not_created_by_this_handoff",
    "not_opened",
    "not_observed_for_this_uncommitted_diff",
    "candidate_branch_name",
    "candidate_pr_title",
    "draft_pr_body",
    "At the snapshot time",
    "did not create a branch",
    "did not create a commit",
    "did not push",
    "did not open a PR",
    "did not observe GitHub Repo Validation",
    "did not mark the goal complete",
    "supersedes this snapshot",
)
RELEASE_PREP_PR_HANDOFF_DECISION_REQUIRED_TOKENS = (
    RELEASE_PREP_PR_HANDOFF_NAME,
    "PR shape prepared",
    "this artifact alone is not PR evidence",
    "GitHub `Repo Validation`",
    "not an explicit commit/push/merge instruction",
    "Do not infer from this artifact alone that a branch was created",
    "After a branch or PR exists",
    "mutate sibling repos",
    "mark the goal complete",
)


__all__ = (
    "RELEASE_PREP_PR_HANDOFF_DECISION_NAME",
    "RELEASE_PREP_PR_HANDOFF_DECISION_REQUIRED_TOKENS",
    "RELEASE_PREP_PR_HANDOFF_NAME",
    "RELEASE_PREP_PR_HANDOFF_REQUIRED_TOKENS",
    "RELEASE_SUPPORT_READINESS_AUDIT_DECISION_NAME",
    "RELEASE_SUPPORT_READINESS_AUDIT_DECISION_REQUIRED_TOKENS",
    "RELEASE_SUPPORT_READINESS_AUDIT_NAME",
    "RELEASE_SUPPORT_READINESS_AUDIT_REQUIRED_TOKENS",
    "STRATEGIC_CLOSEOUT_AUDIT_DECISION_NAME",
    "STRATEGIC_CLOSEOUT_AUDIT_DECISION_REQUIRED_TOKENS",
    "STRATEGIC_CLOSEOUT_AUDIT_NAME",
    "STRATEGIC_CLOSEOUT_AUDIT_REQUIRED_TOKENS",
)
