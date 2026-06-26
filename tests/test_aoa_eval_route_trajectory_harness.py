from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import run_aoa_eval_route_trajectory_harness as harness


REQUIRED_REFS = [
    "evals/workflow/aoa-tool-trajectory-discipline/EVAL.md",
    "evals/workflow/aoa-trace-outcome-separation/EVAL.md",
    "evals/capability/aoa-eval-integrity-check/EVAL.md",
]


def passing_dashboard() -> dict:
    return {"trajectory_eval_slice": {"source_eval_refs": REQUIRED_REFS}}


def passing_session_payload() -> dict:
    return {
        "session_entry_commands": [
            {"command": "python scripts/check_eval_freshness_sentinel.py --json"},
            {"command": "python scripts/build_eval_readiness_dashboard.py --check"},
            {"command": "python scripts/check_eval_support_registry.py --json"},
            {"command": "python scripts/validate_eval_candidate_packets.py --schema-only"},
            {"command": "python scripts/check_eval_candidate_queue_lifecycle.py --json"},
            {"command": "python scripts/review_eval_promotion_path.py --json"},
            {
                "command": "python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json"
            },
        ],
        "active_repo_routes": [
            {
                "repo_id": "aoa-skills",
                "exact_next_command": "python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json",
            }
        ],
        "candidate_packet_contract": {"candidate_only": True, "proof_authority": False},
        "promotion_review_route": {
            "command": "python scripts/review_eval_promotion_path.py --json",
            "dry_run": True,
            "promotion_allowed": False,
            "mcp_promotion_allowed": False,
            "gates": ["local_owner_review", "central_overlap_check", "human_acceptance"],
        },
        "stop_lines": [
            "do not treat .aoa, MCP, dashboard, generated readers, or candidate packets as proof"
        ],
    }


def passing_support_registry() -> dict:
    return {
        "summary": {
            "by_recommended_route": {
                "forbidden_as_eval_apply_until_manual_owner_review": 2
            }
        }
    }


def passing_sentinel_payload() -> dict:
    return {
        "signals": [
            {
                "id": "mcp_federation_mirror_stale",
                "severity": "warning",
                "next_command": "scripts/aoa-sync-federation-surfaces --layer aoa-evals",
            }
        ]
    }


def test_route_trajectory_harness_passes_expected_route_sequence() -> None:
    payload = harness.evaluate_route_trajectory(
        dashboard=passing_dashboard(),
        support_registry=passing_support_registry(),
        session_payload=passing_session_payload(),
        sentinel_payload=passing_sentinel_payload(),
    )

    assert payload["schema_version"] == harness.SCHEMA_VERSION
    assert payload["summary"] == {"cases": 7, "passed": 7, "failed": 0}
    assert {
        "session_front_door_sequence",
        "existing_central_eval_refs_before_new_design",
        "local_pressure_inspects_local_port_first",
        "promotion_review_before_central_adoption",
        "freshness_sentinel_before_proof_claim",
        "session_evidence_candidate_only",
        "unsafe_scripts_require_owner_review",
    } == {case["case_id"] for case in payload["cases"]}


def test_route_trajectory_harness_names_missing_front_door_violation() -> None:
    session_payload = passing_session_payload()
    session_payload["session_entry_commands"] = [
        {"command": "python scripts/build_eval_readiness_dashboard.py --check"}
    ]

    payload = harness.evaluate_route_trajectory(
        dashboard=passing_dashboard(),
        support_registry=passing_support_registry(),
        session_payload=session_payload,
        sentinel_payload=passing_sentinel_payload(),
    )

    front_door = {
        case["case_id"]: case for case in payload["cases"]
    }["session_front_door_sequence"]
    assert front_door["passed"] is False
    assert front_door["violation"] == "session-start first commands are missing or out of order"
    assert payload["summary"]["failed"] >= 1
