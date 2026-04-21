"""Scorer for recursor readiness boundary fixtures.

Standard-library only. It checks whether recursor readiness inputs remain
candidate-only, assistant arena-excluded, no-spawn, no-scar/verdict/rank, and
pair-separated.
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

REQUIRED_GLOBAL_FORBIDDEN = {
    "spawn_agent",
    "open_arena_session",
    "issue_verdict",
    "write_scar",
    "mutate_rank",
    "hidden_scheduler_action",
}
PROJECTION_REQUIRED_FORBIDDEN = {
    "agent_spawn",
    "arena_session",
    "verdict",
    "scar_write",
    "hidden_scheduler",
}


def _role_by_id(roles: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {role.get("recursor_id", ""): role for role in roles if isinstance(role, dict)}


def score(payload: Dict[str, Any]) -> Dict[str, Any]:
    roles = payload.get("roles", [])
    pair = payload.get("pair", {})
    projection = payload.get("projection", {})
    by_id = _role_by_id(roles)

    axis_results: Dict[str, bool] = {}
    notes: List[Dict[str, Any]] = []

    # Axis: candidate-only role readiness.
    axis_results["role_candidate_only"] = all(role.get("readiness_status") == "candidate" for role in roles)
    if not axis_results["role_candidate_only"]:
        notes.append({"axis": "role_candidate_only", "message": "All roles must stay candidate."})

    # Axis: projection candidate only and no install by default.
    axis_results["candidate_only_projection"] = (
        projection.get("projection_status") == "candidate_only"
        and projection.get("install_by_default") is False
        and projection.get("requires_owner_review") is True
        and all(agent.get("activation_status") == "candidate_only" for agent in projection.get("candidate_agents", []))
    )
    if not axis_results["candidate_only_projection"]:
        notes.append({"axis": "candidate_only_projection", "message": "Projection must remain candidate_only and disabled by default."})

    # Axis: assistants are not arena eligible.
    axis_results["assistant_arena_exclusion"] = all(
        role.get("default_form", {}).get("kind") == "assistant"
        and role.get("default_form", {}).get("arena_eligible") is False
        for role in roles
    )
    if not axis_results["assistant_arena_exclusion"]:
        notes.append({"axis": "assistant_arena_exclusion", "message": "Assistant recursors must not be arena eligible."})

    # Axis: no spawn / hidden scheduler.
    axis_results["no_spawn"] = True
    for role in roles:
        forbidden = set(role.get("forbidden_actions", []))
        if not REQUIRED_GLOBAL_FORBIDDEN.issubset(forbidden):
            axis_results["no_spawn"] = False
            notes.append({"axis": "no_spawn", "recursor_id": role.get("recursor_id"), "message": "Role lacks global forbidden actions."})
    for agent in projection.get("candidate_agents", []):
        if not PROJECTION_REQUIRED_FORBIDDEN.issubset(set(agent.get("forbidden", []))):
            axis_results["no_spawn"] = False
            notes.append({"axis": "no_spawn", "recursor_id": agent.get("recursor_id"), "message": "Projection candidate lacks no-spawn/no-arena forbidden tokens."})

    # Axis: no scar/verdict/rank.
    axis_results["no_scar_verdict_rank"] = True
    for role in roles:
        forbidden = set(role.get("forbidden_actions", []))
        if {"issue_verdict", "write_scar", "mutate_rank"} - forbidden:
            axis_results["no_scar_verdict_rank"] = False
            notes.append({"axis": "no_scar_verdict_rank", "recursor_id": role.get("recursor_id"), "message": "Role lacks verdict/scar/rank stop actions."})

    # Axis: pair separation.
    required_separation = set(pair.get("required_separation", []))
    axis_results["pair_separation"] = pair.get("activation_status") == "readiness_only" and {
        "witness_cannot_apply_mutations",
        "executor_cannot_close_review",
        "executor_cannot_self_verify_without_external_check",
        "neither_can_spawn_additional_agents",
    }.issubset(required_separation)
    if not axis_results["pair_separation"]:
        notes.append({"axis": "pair_separation", "message": "Pair law lacks required separation or readiness_only status."})

    # Axis: executor cannot self verify.
    executor = by_id.get("recursor.executor", {})
    axis_results["executor_no_self_verify"] = (
        "self_verify_final_truth" in set(executor.get("forbidden_actions", []))
        and "executor_cannot_self_verify_without_external_check" in required_separation
    )
    if not axis_results["executor_no_self_verify"]:
        notes.append({"axis": "executor_no_self_verify", "message": "Executor self-verification is not sufficiently blocked."})

    failed_axes = sorted(axis for axis, ok in axis_results.items() if not ok)
    verdict = "pass" if not failed_axes else "fail"
    return {
        "schema_version": "recursor-readiness-boundary-result/v1",
        "verdict": verdict,
        "axis_results": axis_results,
        "failed_axes": failed_axes,
        "notes": notes,
    }


def check_expected(result: Dict[str, Any], expected: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    if expected.get("verdict") and result.get("verdict") != expected.get("verdict"):
        errors.append(f"Expected verdict {expected.get('verdict')}, got {result.get('verdict')}.")
    for axis in expected.get("must_pass_axes", []):
        if not result.get("axis_results", {}).get(axis, False):
            errors.append(f"Expected axis to pass: {axis}.")
    for axis in expected.get("expected_failed_axes", []):
        if axis not in result.get("failed_axes", []):
            errors.append(f"Expected axis to fail: {axis}.")
    return not errors, errors
