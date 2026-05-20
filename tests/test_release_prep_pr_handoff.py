from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HANDOFF_PATH = REPO_ROOT / "reports" / "release-prep-pr-handoff-v1.json"


def load_handoff() -> dict:
    return json.loads(HANDOFF_PATH.read_text(encoding="utf-8"))


def test_release_prep_pr_handoff_keeps_pre_pr_snapshot_bounded() -> None:
    handoff = load_handoff()
    github_status = handoff["pre_handoff_github_status"]

    assert handoff["handoff_verdict"] == "ready_for_owner_landing_route_with_open_pr"
    assert handoff["status_snapshot_kind"] == "pre_pr_handoff_snapshot"
    assert handoff["pre_landing_worktree_posture"] == "dirty_uncommitted_local_diff"
    assert github_status["branch_status"] == "not_created_by_this_handoff"
    assert github_status["commit_status"] == "not_created_by_this_handoff"
    assert github_status["push_status"] == "not_attempted"
    assert github_status["pr_status"] == "not_opened"
    assert github_status["repo_validation_status"] == "not_observed_for_this_uncommitted_diff"
    assert github_status["merge_status"] == "not_attempted"
    assert github_status["tag_status"] == "not_created"
    assert github_status["github_release_status"] == "not_published"

    assert "At the snapshot time" in handoff["claim_limit"]
    assert "did not create a branch" in handoff["claim_limit"]
    assert "did not open a PR" in handoff["claim_limit"]
    assert "did not observe GitHub Repo Validation" in handoff["claim_limit"]
    assert "did not mark the goal complete" in handoff["claim_limit"]
    assert "supersedes this snapshot" in handoff["claim_limit"]


def test_release_prep_pr_handoff_maps_changed_surface_groups() -> None:
    handoff = load_handoff()
    groups = {
        entry["group_id"]: entry for entry in handoff["changed_surface_groups"]
    }

    assert set(groups) == {
        "root_design_and_route",
        "decision_memory",
        "roadmap_changelog_quests",
        "proof_topology_legacy_mechanics",
        "active_proof_loop",
        "agent_lane_and_generated_readers",
        "validators_and_tests",
    }
    for entry in groups.values():
        assert entry["summary"]
        assert entry["evidence_refs"]

    assert "repo:aoa-evals/DESIGN.md" in groups["root_design_and_route"]["evidence_refs"]
    assert "repo:aoa-evals/reports/strategic-closeout-audit-v1.json" in groups["active_proof_loop"]["evidence_refs"]
    assert "repo:aoa-evals/tests/test_release_prep_pr_handoff.py" in groups["validators_and_tests"]["evidence_refs"]


def test_release_prep_pr_handoff_has_reviewable_pr_body() -> None:
    handoff = load_handoff()
    pr_body = "\n".join(handoff["draft_pr_body"])

    assert "## Summary" in pr_body
    assert "## Validation" in pr_body
    assert "## Boundaries" in pr_body
    assert "python scripts/validate_repo.py" in pr_body
    assert "python scripts/release_check.py" in pr_body
    assert "no tag or GitHub Release" in pr_body
    assert "no live eval-result receipt publication" in pr_body
    assert "no runtime evidence acceptance" in pr_body
    assert "no sibling repository mutation" in pr_body
    assert "goal completion remains open" in pr_body


def test_release_prep_pr_handoff_lists_landing_steps_and_gates() -> None:
    handoff = load_handoff()
    landing_steps = "\n".join(handoff["landing_steps"])
    commands = {entry["command"]: entry for entry in handoff["verification_snapshot"]}

    for token in (
        "create a branch",
        "commit the intended accumulated diff",
        "push the branch",
        "open a PR",
        "watch GitHub Repo Validation",
        "merge only after required checks are green",
        "worktree is clean",
        "final owner-visible completion audit",
    ):
        assert token in landing_steps

    for command in (
        "python -m pytest -q tests/test_release_prep_pr_handoff.py tests/test_validate_repo.py -k release_prep_pr_handoff",
        "python scripts/validate_repo.py",
        "python scripts/validate_semantic_agents.py",
        "python scripts/validate_nested_agents.py",
        "git diff --check",
        "python scripts/build_catalog.py --check",
        "python scripts/generate_eval_report_index.py --check",
        "python scripts/generate_runtime_candidate_template_index.py --check",
        "python scripts/generate_runtime_candidate_intake.py --check",
        "python scripts/generate_phase_alpha_eval_matrix.py --check",
        "python scripts/run_sibling_canary.py --repo-root . --format json",
        "python -m pytest -q tests",
        "python scripts/release_check.py",
    ):
        assert commands[command]["result"] == "passed"
