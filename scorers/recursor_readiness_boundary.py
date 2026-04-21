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
REQUIRED_ROLE_IDS = {"recursor.witness", "recursor.executor"}
PROJECTION_REQUIRED_FORBIDDEN = {
    "global": {
        "agent_spawn",
        "arena_session",
        "verdict",
        "scar_write",
        "rank_mutation",
        "hidden_scheduler",
    },
    "recursor.witness": {
        "workspace_write",
    },
    "recursor.executor": {
        "execute_without_plan",
        "self_verify_as_final",
    },
}
PROJECTION_REQUIRED_ACTIVATION = {"explicit_main_codex_call", "no_agonic_runtime_claim"}


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
    projection_agents = [agent for agent in projection.get("candidate_agents", []) if isinstance(agent, dict)]
    projection_ids = {agent.get("recursor_id") for agent in projection_agents}
    axis_results["candidate_only_projection"] = (
        projection.get("projection_status") == "candidate_only"
        and projection.get("install_by_default") is False
        and projection.get("requires_owner_review") is True
        and projection_ids == REQUIRED_ROLE_IDS
        and len(projection_agents) == len(REQUIRED_ROLE_IDS)
        and all(agent.get("activation_status") == "candidate_only" for agent in projection_agents)
        and all(
            PROJECTION_REQUIRED_ACTIVATION.issubset(set(agent.get("activation_requires", [])))
            for agent in projection_agents
        )
    )
    if not axis_results["candidate_only_projection"]:
        notes.append({"axis": "candidate_only_projection", "message": "Projection must remain candidate_only, disabled by default, two-role, and guarded against Agon runtime claims."})

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
    for agent in projection_agents:
        rid = agent.get("recursor_id")
        required_projection_forbidden = set(PROJECTION_REQUIRED_FORBIDDEN["global"])
        required_projection_forbidden |= PROJECTION_REQUIRED_FORBIDDEN.get(rid, set())
        if not required_projection_forbidden.issubset(set(agent.get("forbidden", []))):
            axis_results["no_spawn"] = False
            notes.append({"axis": "no_spawn", "recursor_id": rid, "message": "Projection candidate lacks required forbidden tokens."})

    # Axis: no scar/verdict/rank.
    axis_results["no_scar_verdict_rank"] = True
    for role in roles:
        forbidden = set(role.get("forbidden_actions", []))
        if {"issue_verdict", "write_scar", "mutate_rank"} - forbidden:
            axis_results["no_scar_verdict_rank"] = False
            notes.append({"axis": "no_scar_verdict_rank", "recursor_id": role.get("recursor_id"), "message": "Role lacks verdict/scar/rank stop actions."})

    # Axis: pair separation.
    required_separation = set(pair.get("required_separation", []))
    pair_roles = pair.get("roles", {})
    pair_binds_required_roles = (
        pair_roles.get("witness") == "recursor.witness"
        and pair_roles.get("executor") == "recursor.executor"
        and REQUIRED_ROLE_IDS.issubset(set(by_id))
    )
    axis_results["pair_separation"] = pair.get("activation_status") == "readiness_only" and pair_binds_required_roles and {
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
    expected_failed_axes = sorted(expected.get("expected_failed_axes", []))
    for axis in expected_failed_axes:
        if axis not in result.get("failed_axes", []):
            errors.append(f"Expected axis to fail: {axis}.")
    if expected_failed_axes:
        failed_axes = sorted(result.get("failed_axes", []))
        if failed_axes != expected_failed_axes:
            errors.append(f"Expected failed axes exactly {expected_failed_axes}, got {failed_axes}.")
    return not errors, errors
