from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import review_eval_promotion_path as review


def repo_entry(
    repo_id: str,
    *,
    active_total: int = 1,
    route_key: str = "active_intake_select_then_apply_or_design",
    central_matches: list[str] | None = None,
) -> dict:
    suite_state = "ready" if route_key == "active_suite_apply_or_regression_check" else "absent"
    return {
        "repo": repo_id,
        "repo_id": repo_id,
        "repo_path": repo_id,
        "port_path": "evals/PORT.yaml",
        "inventory_status": "active",
        "validator_ok": True,
        "pressure_counts": {
            "intake_packets": 1 if route_key.startswith("active_intake") else 0,
            "suite_notes": 1 if "suite" in route_key else 0,
            "report_notes": max(active_total - 1, 0),
            "local_bundles": 0,
            "active_total": active_total,
        },
        "owner_boundary": {
            "owner_repo": repo_id,
            "proof_owner_repo": "aoa-evals",
            "central_proof_boundary_ok": True,
        },
        "central_eval_name_matches": central_matches or [],
        "route_recommendation": {
            "route_key": route_key,
            "action": "Use the local surface without central proof acceptance.",
        },
        "suite_execution": {
            "state": suite_state,
            "suite_count": 1 if suite_state == "ready" else 0,
            "ready_count": 1 if suite_state == "ready" else 0,
            "suites": [],
            "auto_run_allowed": False,
            "inventory_executed_runner": False,
            "proof_authority": False,
            "promotion_allowed": False,
        },
    }


def inventory_payload(
    *repos: dict,
    schema_version: str = "os_abyss_local_eval_port_inventory_v2",
) -> dict:
    return {"schema_version": schema_version, "repos": list(repos)}


def catalog_payload() -> dict:
    return {
        "evals": [
            {
                "name": "aoa-existing-central-eval",
                "category": "workflow",
                "status": "bounded",
                "eval_path": "evals/workflow/aoa-existing-central-eval/EVAL.md",
                "summary": "Existing central route.",
                "skill_refs": [],
            },
            {
                "name": "aoa-tool-trajectory-discipline",
                "category": "workflow",
                "status": "bounded",
                "eval_path": "evals/workflow/aoa-tool-trajectory-discipline/EVAL.md",
                "summary": "Tool trajectory route discipline for aoa skills.",
                "skill_refs": [{"repo": "aoa-skills", "name": "aoa-change-protocol"}],
            },
        ]
    }


def test_promotion_review_auto_selects_active_pressure_and_stays_dry_run() -> None:
    payload = review.build_promotion_review_payload(
        inventory_payload(
            repo_entry("aoa-memo", active_total=2),
            repo_entry(
                "aoa-skills",
                active_total=6,
                route_key="active_suite_apply_or_regression_check",
            ),
        ),
        catalog_payload(),
    )

    assert payload["valid"] is True
    assert payload["selected_repo"]["repo_id"] == "aoa-skills"
    assert payload["selected_repo"]["pressure_severity"] == "high"
    assert payload["promotion_allowed"] is False
    assert payload["mcp_promotion_allowed"] is False
    assert payload["selected_repo"]["suite_execution"]["state"] == "ready"
    assert payload["selected_repo"]["suite_execution"]["execution_allowed"] is False
    assert payload["selected_repo"]["suite_execution"]["promotion_review_executed_runner"] is False
    assert payload["central_overlap"]["summary"]["adjacent_count"] == 1
    assert payload["recommended_next_route"] == "inspect_adjacent_central_evals_then_local_owner_review"
    assert [gate["gate"] for gate in payload["promotion_gates"]] == review.PROMOTION_GATES
    assert payload["promotion_gates"][0]["status"] == "needs_owner_review"
    assert any(stage["stage"] == "central_draft" for stage in payload["stage_boundaries"])


def test_promotion_review_downgrades_injected_v1_ready_suite_to_absent() -> None:
    injected = repo_entry(
        "aoa-skills",
        active_total=6,
        route_key="active_suite_apply_or_regression_check",
    )
    payload = review.build_promotion_review_payload(
        inventory_payload(
            injected,
            schema_version="os_abyss_local_eval_port_inventory_v1",
        ),
        {"evals": []},
        repo_id="aoa-skills",
    )

    assert payload["valid"] is True
    assert payload["selected_repo"]["suite_execution"]["state"] == "absent"
    assert payload["selected_repo"]["suite_execution"]["ready_count"] == 0
    assert payload["selected_repo"]["suite_execution"]["owner_apply_required"] is False
    assert payload["recommended_next_route"] != (
        "apply_local_suite_as_candidate_regression_check_before_central_draft"
    )


def test_promotion_review_routes_exact_duplicate_before_new_central_draft() -> None:
    payload = review.build_promotion_review_payload(
        inventory_payload(
            repo_entry(
                "aoa-memo",
                active_total=1,
                central_matches=["aoa-existing-central-eval"],
            )
        ),
        catalog_payload(),
        repo_id="aoa-memo",
    )

    assert payload["valid"] is True
    assert payload["central_overlap"]["summary"]["exact_count"] == 1
    assert payload["central_overlap"]["exact_name_matches"][0]["name"] == "aoa-existing-central-eval"
    assert payload["recommended_next_route"] == "select_or_apply_existing_central_eval_before_new_central_draft"
    source_gate = {
        gate["gate"]: gate for gate in payload["promotion_gates"]
    }["source_bundle_draft"]
    assert source_gate["status"] == "blocked"


def test_promotion_review_validator_rejects_proof_promotion_fields() -> None:
    payload = review.build_promotion_review_payload(
        inventory_payload(repo_entry("aoa-routing")),
        catalog_payload(),
        repo_id="aoa-routing",
    )
    payload["promotion_allowed"] = True
    payload["central_bundle_created"] = True
    payload["verdict"] = "accepted"

    issues = review.validate_promotion_review_payload(payload)

    assert {issue["code"] for issue in issues} >= {
        "promotion_allowed",
        "forbidden_truthy_field",
        "forbidden_proof_field",
    }


def test_promotion_review_payload_cli_fails_on_forbidden_promotion(tmp_path: Path) -> None:
    payload = review.build_promotion_review_payload(
        inventory_payload(repo_entry("aoa-routing")),
        catalog_payload(),
        repo_id="aoa-routing",
    )
    payload["mcp_promotion_allowed"] = True
    path = tmp_path / "bad-review.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/review_eval_promotion_path.py",
            "--review-payload",
            str(path),
            "--json",
        ],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    output = json.loads(completed.stdout)

    assert completed.returncode == 1
    assert output["valid"] is False
    assert any(issue["code"] == "mcp_promotion_allowed" for issue in output["issues"])
