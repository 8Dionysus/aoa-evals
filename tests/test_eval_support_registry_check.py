from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_eval_readiness_dashboard as readiness
import check_eval_support_registry as support_check


def test_current_support_registry_has_semantic_review_coverage() -> None:
    support = readiness.build_support_registry(REPO_ROOT)
    payload = support_check.build_review_payload(support)
    summary = payload["summary"]

    assert payload["overall_severity"] == "ok"
    assert payload["issues"] == []
    assert summary["eval_lane_relevant"] > 0
    assert summary["reviewed_eval_relevant"] == summary["eval_lane_relevant"]
    assert summary["by_review_status"].get("manual_review_required", 0) == 0
    assert summary["unsafe_side_effect_scripts"] >= 1


def test_support_registry_review_rejects_unresolved_eval_relevant_surface() -> None:
    support = {
        "surfaces": [
            {
                "kind": "script",
                "path": "scripts/example.py",
                "semantic_class": "manual_review_needed",
                "review_status": "manual_review_required",
                "eval_lane_relevant": True,
                "classification_evidence": ["family: eval helper"],
                "recommended_route": "eval_lane_support_review",
                "safe_to_apply_directly": False,
                "forbidden_interpretations": ["automatic_eval_apply"],
                "owner_surface": "scripts/AGENTS.md",
                "side_effects": "stdout only",
            }
        ]
    }

    payload = support_check.build_review_payload(support)

    assert payload["overall_severity"] == "error"
    assert {
        item["id"] for item in payload["issues"]
    } >= {"support_registry_unresolved_eval_relevant_review"}


def test_support_registry_review_rejects_write_surface_as_direct_apply() -> None:
    support = {
        "surfaces": [
            {
                "kind": "script",
                "path": "scripts/build_state.py",
                "semantic_class": "deterministic_validator",
                "review_status": "rule_reviewed",
                "eval_lane_relevant": True,
                "classification_evidence": ["side_effects: writes tracked state"],
                "recommended_route": "apply_as_deterministic_eval_support",
                "safe_to_apply_directly": True,
                "forbidden_interpretations": ["central_proof_acceptance"],
                "owner_surface": "scripts/AGENTS.md",
                "side_effects": "writes tracked state",
            }
        ]
    }

    payload = support_check.build_review_payload(support)

    assert payload["overall_severity"] == "error"
    assert {
        item["id"] for item in payload["issues"]
    } >= {"support_registry_write_surface_marked_direct_apply"}


def test_support_registry_review_rejects_unsafe_writer_route_drift() -> None:
    support = {
        "surfaces": [
            {
                "kind": "script",
                "path": "scripts/mutate.py",
                "semantic_class": "unsafe_side_effect_script",
                "review_status": "reviewed_forbidden",
                "eval_lane_relevant": True,
                "classification_evidence": ["side_effects: mutates state"],
                "recommended_route": "apply_as_deterministic_eval_support",
                "safe_to_apply_directly": False,
                "forbidden_interpretations": ["central_proof_acceptance"],
                "owner_surface": "scripts/AGENTS.md",
                "side_effects": "mutates state",
            }
        ]
    }

    payload = support_check.build_review_payload(support)

    assert payload["overall_severity"] == "error"
    assert {
        item["id"] for item in payload["issues"]
    } >= {"support_registry_unsafe_writer_route_mismatch"}
