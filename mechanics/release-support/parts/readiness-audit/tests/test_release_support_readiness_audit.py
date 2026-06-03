from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[5]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_repo

AUDIT_PATH = (
    REPO_ROOT
    / "mechanics"
    / "release-support"
    / "parts"
    / "readiness-audit"
    / "reports"
    / "release-support-readiness-audit-v1.json"
)


def load_audit() -> dict:
    return json.loads(AUDIT_PATH.read_text(encoding="utf-8"))


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


def make_release_support_readiness_audit_surface(repo_root: Path) -> Path:
    copy_repo_text(repo_root, validate_repo.RELEASE_SUPPORT_READINESS_AUDIT_NAME)
    return repo_root / validate_repo.RELEASE_SUPPORT_READINESS_AUDIT_NAME


def test_release_support_readiness_audit_keeps_publication_open() -> None:
    audit = load_audit()
    boundary = audit["publication_boundary"]

    assert audit["readiness_verdict"] == "local_release_prep_review_ready_with_open_landing"
    assert boundary["release_publication_status"] == "not_published"
    assert boundary["tag_status"] == "not_created"
    assert boundary["github_release_status"] == "not_published"
    assert boundary["github_pr_status"] == "not_opened"
    assert boundary["github_repo_validation_status"] == "not_observed_for_this_uncommitted_diff"
    assert boundary["goal_completion_status"] == "not_complete"
    assert boundary["live_receipt_publication_status"] == "not_attempted"
    assert "not a release" in boundary["boundary"]
    assert "not goal completion" in boundary["boundary"]


def test_release_support_readiness_audit_maps_required_strategic_surfaces() -> None:
    audit = load_audit()
    requirements = {
        entry["requirement_id"]: entry for entry in audit["requirements_review"]
    }

    assert set(requirements) == {
        "root_design_spine",
        "decision_memory",
        "roadmap_quest_and_lifecycle_route",
        "proof_topology_legacy_and_mechanics",
        "proof_loop_materialization",
        "generated_reader_freshness",
        "local_release_gate_coverage",
        "sibling_boundary_and_canary",
    }
    for entry in requirements.values():
        assert entry["status"] == "ready_for_release_prep_review"
        assert entry["evidence_refs"]
        assert "claim_limit" in entry

    proof_loop_refs = requirements["proof_loop_materialization"]["evidence_refs"]
    assert "repo:aoa-evals/mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json" in proof_loop_refs
    assert "repo:aoa-evals/generated/eval_report_index.min.json" in proof_loop_refs


def test_release_support_readiness_audit_lists_local_gates_and_limits() -> None:
    audit = load_audit()
    commands = {entry["command"]: entry for entry in audit["verification_snapshot"]}

    for command in (
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
        "python scripts/build_catalog.py --check",
        "python scripts/generate_eval_report_index.py --check",
        "python mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py --repo-root . --format json",
        "python -m pytest -q",
        "python scripts/release_check.py",
        "git diff --check",
    ):
        assert commands[command]["result"] == "passed"

    assert "does not publish a release" in audit["claim_limit"]
    assert "mark the aoa-evals strategic goal complete" in audit["claim_limit"]


def test_release_support_readiness_audit_surface_validates_current_route() -> None:
    assert validate_repo.validate_release_support_readiness_audit_surface(REPO_ROOT) == []


def test_release_support_readiness_audit_rejects_goal_completion_claim(
    tmp_path: Path,
) -> None:
    audit_path = make_release_support_readiness_audit_surface(tmp_path)
    payload = json.loads(audit_path.read_text(encoding="utf-8"))
    payload["publication_boundary"]["goal_completion_status"] = "complete"
    write_json_payload(audit_path, payload)

    issues = validate_repo.validate_release_support_readiness_audit_surface(tmp_path)

    assert any(
        issue.location == f"{validate_repo.RELEASE_SUPPORT_READINESS_AUDIT_NAME}.publication_boundary"
        and "goal_completion_status must be 'not_complete'" in issue.message
        for issue in issues
    )


def test_release_support_readiness_audit_rejects_missing_release_gate(
    tmp_path: Path,
) -> None:
    audit_path = make_release_support_readiness_audit_surface(tmp_path)
    payload = json.loads(audit_path.read_text(encoding="utf-8"))
    payload["verification_snapshot"] = [
        entry
        for entry in payload["verification_snapshot"]
        if entry["command"] != "python scripts/release_check.py"
    ]
    write_json_payload(audit_path, payload)

    issues = validate_repo.validate_release_support_readiness_audit_surface(tmp_path)

    assert any(
        issue.location == f"{validate_repo.RELEASE_SUPPORT_READINESS_AUDIT_NAME}.verification_snapshot"
        and "python scripts/release_check.py" in issue.message
        for issue in issues
    )
