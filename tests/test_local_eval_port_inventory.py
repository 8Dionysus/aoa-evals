from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_local_eval_port_inventory as inventory


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def make_repo(workspace: Path, relative_path: str) -> Path:
    repo_root = workspace / relative_path
    git_dir = repo_root / ".git"
    git_dir.mkdir(parents=True)
    write_text(git_dir / "HEAD", "ref: refs/heads/main\n")
    return repo_root


def make_port(repo_root: Path, *, status: str = "skeleton", include_local_role: bool = True) -> None:
    lines = [
        "schema_version: local_eval_port_v1",
        f"owner_repo: {repo_root.name}",
        f"status: {status}",
        "proof_owner_repo: aoa-evals",
        "default_intake_schema: eval_need_v1",
    ]
    if include_local_role:
        lines.append("local_role: repo-local eval pressure, fixtures, suites, and reports")
    lines.append("central_boundary: no verdict, scoring, regression, or proof doctrine authority")
    write_text(repo_root / "evals" / "PORT.yaml", "\n".join(lines) + "\n")
    write_text(
        repo_root / "evals" / "README.md",
        """
        # Local Eval Port

        `aoa-evals` owns central verdict, scoring, regression, and proof doctrine
        authority.
        """,
    )
    write_text(
        repo_root / "evals" / "AGENTS.md",
        """
        # AGENTS.md

        Route verdict, scoring, regression, and proof doctrine authority to `aoa-evals`.
        """,
    )
    write_text(repo_root / "evals" / "intake" / "README.md", "# Intake\n")
    write_text(repo_root / "evals" / "suites" / "README.md", "# Suites\n")
    write_text(repo_root / "evals" / "reports" / "README.md", "# Reports\n")


def write_valid_intake(repo_root: Path, *, name: str = "aoa-memory-guardrail-pressure") -> None:
    payload = {
        "schema_version": "eval_need_v1",
        "name": name,
        "proof_question": "Does local pressure route before central proof adoption?",
        "origin_need": "A local handoff needs a route before central proof adoption.",
        "summary": "Checks whether local pressure stays below proof authority.",
        "object_under_evaluation": "local guardrail handoff",
        "category": "boundary",
        "claim_type": "bounded",
        "baseline_mode": "none",
        "report_format": "summary-with-breakdown",
        "verdict_shape": "categorical",
        "authoring_route": "candidate_evidence_packet",
        "expected_use_when": ["local guardrail pressure appears"],
        "blind_spot_notes": ["does not accept a central proof verdict"],
        "candidate_evidence_refs": ["evals/README.md"],
        "source_refs": ["evals/README.md"],
    }
    write_text(
        repo_root / "evals" / "intake" / f"{name}.eval_need.json",
        json.dumps(payload, indent=2) + "\n",
    )


def write_valid_suite(repo_root: Path) -> None:
    write_text(
        repo_root / "evals" / "suites" / "guardrail.suite.md",
        f"""
        ---
        schema_version: local_eval_suite_note_v1
        owner_repo: {repo_root.name}
        status: draft
        authority_boundary: no verdict, scoring, regression, or proof doctrine authority
        ---

        # Guardrail Suite
        """,
    )


def write_valid_report(repo_root: Path) -> None:
    write_text(
        repo_root / "evals" / "reports" / "guardrail.report.md",
        f"""
        ---
        schema_version: local_eval_report_note_v1
        owner_repo: {repo_root.name}
        status: draft
        authority_boundary: no verdict, scoring, regression, or proof doctrine authority
        ---

        # Guardrail Report
        """,
    )


def test_inventory_contract_matches_builder_surface() -> None:
    contract = inventory.load_inventory_contract()
    route_keys = {
        route["route_key"]
        for route in contract["route_recommendations"]
        if isinstance(route, dict)
    }

    assert contract["schema_version"] == "aoa_local_eval_port_inventory_contract_v1"
    assert contract["inventory_schema_version"] == inventory.SCHEMA_VERSION
    assert contract["layer"] == "aoa-evals-local-port-inventory"
    assert contract["proof_owner_repo"] == inventory.PROOF_OWNER_REPO
    assert contract["authority_boundary"] == inventory.AUTHORITY_BOUNDARY
    assert contract["source_of_truth"] == inventory.SOURCE_OF_TRUTH
    assert contract["inventory_statuses"] == [
        "missing",
        "stale_candidate",
        "invalid",
        "skeleton",
        "active",
    ]
    assert contract["summary_keys"] == [
        "repos",
        "validator_ok",
        "validator_failed",
        "with_local_port",
        "with_detected_pressure",
        "excluded_repos",
        "missing",
        "stale_candidate",
        "invalid",
        "skeleton",
        "active",
    ]
    assert contract["pressure_count_keys"] == [
        "intake_packets",
        "suite_notes",
        "report_notes",
        "local_bundles",
        "active_total",
    ]
    assert contract["excluded_repo_reason"] == "central_proof_owner_not_repo_local_port"
    assert contract["discovery"]["default_max_depth"] == inventory.DEFAULT_MAX_DEPTH
    assert contract["discovery"]["valid_git_markers"] == [
        ".git directory with HEAD file",
        ".git file whose first line starts with gitdir:",
    ]
    assert set(contract["discovery"]["ignored_dir_names"]) == inventory.IGNORED_DIR_NAMES
    assert contract["discovery"]["ignored_relative_prefixes"] == list(
        inventory.IGNORED_RELATIVE_PREFIXES
    )
    assert route_keys == {
        "missing_no_pressure",
        "stale_local_eval_surface_review",
        "invalid_port_repair",
        "invalid_active_repair",
        "central_overlap_apply_existing_first",
        "valid_skeleton_keep_dormant",
        "local_bundle_central_review_candidate",
        "active_suite_apply_or_regression_check",
        "active_intake_select_then_apply_or_design",
        "active_reports_only_suite_extraction_or_review",
        "active_without_detected_pressure",
    }


def test_discovery_ignores_empty_git_marker_at_workspace_root(tmp_path: Path) -> None:
    workspace = tmp_path / "AbyssOS"
    (workspace / ".git").mkdir(parents=True)
    repo_root = make_repo(workspace, "aoa-routing")

    repo_roots = inventory.discover_repo_roots(workspace, max_depth=inventory.DEFAULT_MAX_DEPTH)

    assert repo_roots == [repo_root.resolve()]


def test_inventory_classifies_repo_port_states(tmp_path: Path) -> None:
    workspace = tmp_path / "AbyssOS"
    missing = make_repo(workspace, "missing-repo")

    skeleton = make_repo(workspace, "aoa-routing")
    make_port(skeleton)

    active_intake = make_repo(workspace, "aoa-memo")
    make_port(active_intake, status="active")
    write_valid_intake(active_intake)

    active_suite = make_repo(workspace, "aoa-skills")
    make_port(active_suite, status="active")
    write_valid_suite(active_suite)

    active_report = make_repo(workspace, "aoa-stats")
    make_port(active_report, status="active")
    write_valid_report(active_report)

    invalid_active = make_repo(workspace, "aoa-4pda-connector")
    make_port(invalid_active, status="active", include_local_role=False)

    stale_candidate = make_repo(workspace, "legacy-evals")
    write_text(stale_candidate / "evals" / "README.md", "# Old eval notes\n")

    central_proof_owner = make_repo(workspace, "aoa-evals")
    write_text(central_proof_owner / "evals" / "workflow" / "central-proof" / "eval.yaml", "name: central-proof\n")

    payload = inventory.build_inventory_payload(workspace)
    entries = {entry["repo_id"]: entry for entry in payload["repos"]}

    assert "aoa-evals" not in entries
    assert payload["contract_schema_version"] == "aoa_local_eval_port_inventory_contract_v1"
    assert payload["contract_ref"] == "docs/architecture/local_eval_port_inventory.contract.v1.json"
    assert sorted(payload["summary"]) == sorted(inventory.load_inventory_contract()["summary_keys"])
    assert payload["excluded_repos"] == [
        {
            "repo": "aoa-evals",
            "repo_path": "aoa-evals",
            "repo_id": "aoa-evals",
            "reason": "central_proof_owner_not_repo_local_port",
        }
    ]

    assert entries["missing-repo"]["inventory_status"] == "missing"
    assert entries["missing-repo"]["route_recommendation"]["route_key"] == "missing_no_pressure"

    assert entries["aoa-routing"]["inventory_status"] == "skeleton"
    assert entries["aoa-routing"]["validator_ok"] is True
    assert entries["aoa-routing"]["route_recommendation"]["route_key"] == "valid_skeleton_keep_dormant"

    assert entries["aoa-memo"]["inventory_status"] == "active"
    assert entries["aoa-memo"]["pressure_counts"]["intake_packets"] == 1
    assert entries["aoa-memo"]["route_recommendation"]["route_key"] == "active_intake_select_then_apply_or_design"

    assert entries["aoa-skills"]["route_recommendation"]["route_key"] == "active_suite_apply_or_regression_check"
    assert entries["aoa-stats"]["route_recommendation"]["route_key"] == "active_reports_only_suite_extraction_or_review"

    assert entries["aoa-4pda-connector"]["inventory_status"] == "invalid"
    assert entries["aoa-4pda-connector"]["route_recommendation"]["route_key"] == "invalid_active_repair"
    assert entries["aoa-4pda-connector"]["owner_boundary"]["central_proof_boundary_ok"] is True

    assert entries["legacy-evals"]["inventory_status"] == "stale_candidate"
    assert entries["legacy-evals"]["route_recommendation"]["route_key"] == "stale_local_eval_surface_review"

    assert payload["summary"]["repos"] == 7
    assert payload["summary"]["active"] == 3
    assert payload["summary"]["skeleton"] == 1
    assert payload["summary"]["missing"] == 1
    assert payload["summary"]["stale_candidate"] == 1
    assert payload["summary"]["invalid"] == 1
    assert payload["summary"]["excluded_repos"] == 1
    assert missing.name == "missing-repo"


def test_central_overlap_routes_existing_eval_first(tmp_path: Path) -> None:
    workspace = tmp_path / "AbyssOS"
    repo_root = make_repo(workspace, "aoa-memo")
    make_port(repo_root, status="active")
    write_valid_intake(repo_root, name="aoa-existing-central-eval")

    entry = inventory.build_repo_entry(
        repo_root,
        workspace,
        central_eval_names={"aoa-existing-central-eval"},
    )

    assert entry["validator_ok"] is True
    assert entry["central_eval_name_matches"] == ["aoa-existing-central-eval"]
    assert (
        entry["route_recommendation"]["route_key"]
        == "central_overlap_apply_existing_first"
    )


def test_markdown_report_names_boundary_and_routes(tmp_path: Path) -> None:
    workspace = tmp_path / "AbyssOS"
    repo_root = make_repo(workspace, "aoa-routing")
    make_port(repo_root, status="active")
    write_valid_intake(repo_root)

    payload = inventory.build_inventory_payload(workspace)
    report = inventory.build_markdown_report(payload)

    assert "routing evidence, not central" in report
    assert "Repo-local eval ports carry intake" in report
    assert "`aoa-routing`" in report
    assert "active_intake_select_then_apply_or_design" in report
