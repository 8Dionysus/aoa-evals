from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[5]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validators import release_support as release_support_validator

REPO_REF_ROOTS = {
    "aoa-evals": REPO_ROOT,
    "aoa-techniques": REPO_ROOT.parent / "aoa-techniques",
    "aoa-skills": REPO_ROOT.parent / "aoa-skills",
    "aoa-agents": REPO_ROOT.parent / "aoa-agents",
    "aoa-playbooks": REPO_ROOT.parent / "aoa-playbooks",
    "aoa-memo": REPO_ROOT.parent / "aoa-memo",
    "aoa-routing": REPO_ROOT.parent / "aoa-routing",
    "aoa-kag": REPO_ROOT.parent / "aoa-kag",
    "aoa-sdk": REPO_ROOT.parent / "aoa-sdk",
    "aoa-stats": REPO_ROOT.parent / "aoa-stats",
    "abyss-stack": REPO_ROOT.parent / "abyss-stack",
}

HANDOFF_PATH = (
    REPO_ROOT
    / "mechanics"
    / "release-support"
    / "parts"
    / "pr-handoff"
    / "reports"
    / "release-prep-pr-handoff-v1.json"
)


def load_handoff() -> dict:
    return json.loads(HANDOFF_PATH.read_text(encoding="utf-8"))


def write_json_payload(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def copy_repo_text(repo_root: Path, relative_path: str) -> None:
    source = REPO_ROOT / relative_path
    if not source.exists():
        raise FileNotFoundError(source)
    destination = repo_root / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def make_release_prep_pr_handoff_surface(repo_root: Path) -> Path:
    copy_repo_text(repo_root, release_support_validator.RELEASE_PREP_PR_HANDOFF_NAME)
    return repo_root / release_support_validator.RELEASE_PREP_PR_HANDOFF_NAME


def validate_release_prep_pr_handoff_surface(repo_root: Path):
    return release_support_validator.validate_release_prep_pr_handoff_surface(
        repo_root,
        repo_ref_roots=REPO_REF_ROOTS,
        strict_sibling_compat=False,
    )


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
    assert "repo:aoa-evals/mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json" in groups["active_proof_loop"]["evidence_refs"]
    assert "repo:aoa-evals/mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py" in groups["validators_and_tests"]["evidence_refs"]


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
        "python -m pytest -q mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py",
        "python -m pytest -q tests/test_generated_route_residue.py",
        "python -m pytest -q tests/test_mechanic_part_contracts.py -k mechanic_part_readme_contract",
        "python -m pytest -q tests/test_mechanic_part_contracts.py -k mechanic_part_payload_inventory",
        "python -m pytest -q tests/test_mechanic_part_validation_commands.py -k mechanic_part_validation_command",
        "python -m pytest -q tests/test_mechanic_parts_index.py -k mechanic_parts_index_sync",
        "python -m pytest -q tests/test_mechanic_legacy_bridge.py -k mechanic_legacy_single_bridge",
        "python -m pytest -q tests/test_mechanic_legacy_bridge.py -k mechanic_provenance_bridge_posture",
        "python -m pytest -q tests/test_root_surface_roles.py -k legacy_naming_single_bridge_language",
        "python -m pytest -q tests/test_mechanic_legacy_archive_routes.py -k active_legacy_parent_wording",
        "python -m pytest -q tests/test_validate_repo.py -k mechanic_provenance_entry",
        "python -m pytest -q tests/test_mechanic_root_district_recon.py -k mechanic_root_district_recon",
        "python -m pytest -q tests/test_mechanics_topology.py",
        "python scripts/validate_repo.py",
        "python scripts/validate_semantic_agents.py",
        "python scripts/validate_nested_agents.py",
        "git diff --check",
        "python scripts/build_catalog.py --check",
        "python scripts/generate_eval_report_index.py --check",
        "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check",
        "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check",
        "python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check",
        "python mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py --repo-root . --format json",
        "python -m pytest -q",
        "python scripts/release_check.py",
    ):
        assert commands[command]["result"] == "passed"


def test_release_prep_pr_handoff_surface_validates_current_route() -> None:
    assert validate_release_prep_pr_handoff_surface(REPO_ROOT) == []


def test_release_prep_pr_handoff_rejects_open_pr_claim(
    tmp_path: Path,
) -> None:
    handoff_path = make_release_prep_pr_handoff_surface(tmp_path)
    payload = json.loads(handoff_path.read_text(encoding="utf-8"))
    payload["pre_handoff_github_status"]["pr_status"] = "opened"
    write_json_payload(handoff_path, payload)

    issues = validate_release_prep_pr_handoff_surface(tmp_path)

    assert any(
        issue.location == f"{release_support_validator.RELEASE_PREP_PR_HANDOFF_NAME}.pre_handoff_github_status"
        and "pre_handoff pr_status must be 'not_opened'" in issue.message
        for issue in issues
    )


def test_release_prep_pr_handoff_rejects_missing_surface_group(
    tmp_path: Path,
) -> None:
    handoff_path = make_release_prep_pr_handoff_surface(tmp_path)
    payload = json.loads(handoff_path.read_text(encoding="utf-8"))
    payload["changed_surface_groups"] = [
        entry
        for entry in payload["changed_surface_groups"]
        if entry["group_id"] != "active_proof_loop"
    ]
    write_json_payload(handoff_path, payload)

    issues = validate_release_prep_pr_handoff_surface(tmp_path)

    assert any(
        issue.location == f"{release_support_validator.RELEASE_PREP_PR_HANDOFF_NAME}.changed_surface_groups"
        and "active_proof_loop" in issue.message
        for issue in issues
    )


def test_release_prep_pr_handoff_rejects_missing_landing_step(
    tmp_path: Path,
) -> None:
    handoff_path = make_release_prep_pr_handoff_surface(tmp_path)
    payload = json.loads(handoff_path.read_text(encoding="utf-8"))
    payload["landing_steps"] = [
        item
        for item in payload["landing_steps"]
        if "watch GitHub Repo Validation" not in item
    ]
    write_json_payload(handoff_path, payload)

    issues = validate_release_prep_pr_handoff_surface(tmp_path)

    assert any(
        issue.location == f"{release_support_validator.RELEASE_PREP_PR_HANDOFF_NAME}.landing_steps"
        and "watch GitHub Repo Validation" in issue.message
        for issue in issues
    )


def test_release_prep_pr_handoff_rejects_missing_focused_gate(
    tmp_path: Path,
) -> None:
    handoff_path = make_release_prep_pr_handoff_surface(tmp_path)
    payload = json.loads(handoff_path.read_text(encoding="utf-8"))
    payload["verification_snapshot"] = [
        entry
        for entry in payload["verification_snapshot"]
        if entry["command"]
        != "python -m pytest -q mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py"
    ]
    write_json_payload(handoff_path, payload)

    issues = validate_release_prep_pr_handoff_surface(tmp_path)

    assert any(
        issue.location == f"{release_support_validator.RELEASE_PREP_PR_HANDOFF_NAME}.verification_snapshot"
        and "mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py"
        in issue.message
        for issue in issues
    )
