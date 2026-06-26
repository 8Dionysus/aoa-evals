#!/usr/bin/env python3
"""Run a deterministic aoa-eval route-selection trajectory harness."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

import aoa_eval_session_start
import build_eval_readiness_dashboard as readiness
import check_eval_freshness_sentinel as sentinel


SCHEMA_VERSION = "aoa_eval_route_trajectory_harness_v1"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", default=str(readiness.DEFAULT_WORKSPACE_ROOT))
    parser.add_argument("--evals-root", default=str(readiness.REPO_ROOT))
    parser.add_argument("--aoa-root", default=str(readiness.DEFAULT_AOA_ROOT))
    parser.add_argument("--skills-source-root", default=str(readiness.DEFAULT_SKILLS_SOURCE_ROOT))
    parser.add_argument("--installed-skills-root", default=str(readiness.DEFAULT_INSTALLED_SKILLS_ROOT))
    parser.add_argument("--stack-root", default="")
    parser.add_argument("--live-timeout", type=int, default=30)
    parser.add_argument("--no-live-checks", action="store_true")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    return parser.parse_args(argv)


def case_result(
    *,
    case_id: str,
    claim: str,
    expected_trajectory: Sequence[str],
    observed_trajectory: Sequence[str],
    passed: bool,
    violation: str | None = None,
) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "claim": claim,
        "expected_trajectory": list(expected_trajectory),
        "observed_trajectory": list(observed_trajectory),
        "passed": passed,
        "violation": violation,
    }


def session_command_names(session_payload: dict[str, Any]) -> list[str]:
    commands = session_payload.get("session_entry_commands")
    if not isinstance(commands, list):
        return []
    return [str(item.get("command") or "") for item in commands if isinstance(item, dict)]


def appears_in_order(commands: Sequence[str], needles: Sequence[str]) -> bool:
    position = 0
    for command in commands:
        if position < len(needles) and needles[position] in command:
            position += 1
    return position == len(needles)


def evaluate_route_trajectory(
    *,
    dashboard: dict[str, Any],
    support_registry: dict[str, Any],
    session_payload: dict[str, Any],
    sentinel_payload: dict[str, Any],
) -> dict[str, Any]:
    cases: list[dict[str, Any]] = []
    commands = session_command_names(session_payload)
    front_door_needles = [
        "check_eval_freshness_sentinel.py",
        "build_eval_readiness_dashboard.py --check",
        "check_eval_support_registry.py",
        "validate_eval_candidate_packets.py --schema-only",
        "check_eval_candidate_queue_lifecycle.py",
        "review_eval_promotion_path.py",
        "build_local_eval_port_inventory.py",
    ]
    cases.append(
        case_result(
            case_id="session_front_door_sequence",
            claim="aoa-eval work starts by checking freshness, readiness, support routes, candidate packet contract, candidate lifecycle, promotion dry-run, and local ports in that order",
            expected_trajectory=front_door_needles,
            observed_trajectory=commands,
            passed=appears_in_order(commands, front_door_needles),
            violation=None
            if appears_in_order(commands, front_door_needles)
            else "session-start first commands are missing or out of order",
        )
    )

    trajectory = dashboard.get("trajectory_eval_slice")
    source_refs = trajectory.get("source_eval_refs") if isinstance(trajectory, dict) else []
    required_refs = {
        "evals/workflow/aoa-tool-trajectory-discipline/EVAL.md",
        "evals/workflow/aoa-trace-outcome-separation/EVAL.md",
        "evals/capability/aoa-eval-integrity-check/EVAL.md",
    }
    refs = set(source_refs if isinstance(source_refs, list) else [])
    cases.append(
        case_result(
            case_id="existing_central_eval_refs_before_new_design",
            claim="route behavior reuses existing central trajectory/integrity eval surfaces before new design",
            expected_trajectory=sorted(required_refs),
            observed_trajectory=sorted(refs),
            passed=required_refs.issubset(refs),
            violation=None
            if required_refs.issubset(refs)
            else "trajectory slice does not point to the existing central eval refs first",
        )
    )

    active_routes = session_payload.get("active_repo_routes")
    active_route_items = active_routes if isinstance(active_routes, list) else []
    active_route_commands = [
        str(item.get("exact_next_command") or "")
        for item in active_route_items
        if isinstance(item, dict)
    ]
    has_local_port_first = bool(active_route_commands) and all(
        "build_local_eval_port_inventory.py" in command for command in active_route_commands
    )
    cases.append(
        case_result(
            case_id="local_pressure_inspects_local_port_first",
            claim="repo-local pressure routes through local port inventory before central proof design",
            expected_trajectory=["build_local_eval_port_inventory.py for each active repo route"],
            observed_trajectory=active_route_commands,
            passed=has_local_port_first,
            violation=None
            if has_local_port_first
            else "active repo route does not point back to local eval-port inspection",
        )
    )

    promotion_route = session_payload.get("promotion_review_route")
    promotion_ok = (
        isinstance(promotion_route, dict)
        and promotion_route.get("dry_run") is True
        and promotion_route.get("promotion_allowed") is False
        and promotion_route.get("mcp_promotion_allowed") is False
        and "human_acceptance" in (promotion_route.get("gates") or [])
        and any("review_eval_promotion_path.py" in command for command in commands)
    )
    cases.append(
        case_result(
            case_id="promotion_review_before_central_adoption",
            claim="local pressure must pass dry-run promotion review and human acceptance before central adoption",
            expected_trajectory=[
                "review_eval_promotion_path.py",
                "dry_run=true",
                "promotion_allowed=false",
                "mcp_promotion_allowed=false",
                "human_acceptance gate",
            ],
            observed_trajectory=[
                *(commands if commands else []),
                f"dry_run={promotion_route.get('dry_run') if isinstance(promotion_route, dict) else None}",
                f"promotion_allowed={promotion_route.get('promotion_allowed') if isinstance(promotion_route, dict) else None}",
                f"mcp_promotion_allowed={promotion_route.get('mcp_promotion_allowed') if isinstance(promotion_route, dict) else None}",
            ],
            passed=promotion_ok,
            violation=None
            if promotion_ok
            else "promotion dry-run route, no-promotion flags, or human acceptance gate is missing",
        )
    )

    sentinel_signals = sentinel_payload.get("signals") if isinstance(sentinel_payload, dict) else []
    freshness_observed = [
        str(item.get("id"))
        for item in sentinel_signals
        if isinstance(item, dict)
        and str(item.get("id")) in {"mcp_federation_mirror_stale", "aoa_live_catchup_pending", "generated_dashboard_age"}
    ]
    sentinel_command_visible = any("check_eval_freshness_sentinel.py" in command for command in commands)
    cases.append(
        case_result(
            case_id="freshness_sentinel_before_proof_claim",
            claim="freshness and mirror drift route through sentinel before any proof claim",
            expected_trajectory=["check_eval_freshness_sentinel.py", "freshness signal or ok generated age"],
            observed_trajectory=["check_eval_freshness_sentinel.py", *freshness_observed],
            passed=sentinel_command_visible and bool(freshness_observed),
            violation=None
            if sentinel_command_visible and bool(freshness_observed)
            else "freshness sentinel is not visible in the trajectory or produced no freshness signal",
        )
    )

    candidate_contract = session_payload.get("candidate_packet_contract")
    stop_lines = session_payload.get("stop_lines") if isinstance(session_payload.get("stop_lines"), list) else []
    candidate_boundary_ok = (
        isinstance(candidate_contract, dict)
        and candidate_contract.get("candidate_only") is True
        and candidate_contract.get("proof_authority") is False
        and any(".aoa" in str(line) and "proof" in str(line) for line in stop_lines)
    )
    cases.append(
        case_result(
            case_id="session_evidence_candidate_only",
            claim=".aoa/session evidence is routed as candidate-only and never proof",
            expected_trajectory=["candidate_only=true", "proof_authority=false", ".aoa stop-line"],
            observed_trajectory=[
                f"candidate_only={candidate_contract.get('candidate_only') if isinstance(candidate_contract, dict) else None}",
                f"proof_authority={candidate_contract.get('proof_authority') if isinstance(candidate_contract, dict) else None}",
                *[str(line) for line in stop_lines],
            ],
            passed=candidate_boundary_ok,
            violation=None
            if candidate_boundary_ok
            else "candidate packet contract or .aoa proof stop-line is missing",
        )
    )

    support_summary = support_registry.get("summary") if isinstance(support_registry, dict) else {}
    routes = support_summary.get("by_recommended_route") if isinstance(support_summary, dict) else {}
    unsafe_route_count = int(routes.get("forbidden_as_eval_apply_until_manual_owner_review") or 0) if isinstance(routes, dict) else 0
    cases.append(
        case_result(
            case_id="unsafe_scripts_require_owner_review",
            claim="write-capable scripts are forbidden as direct eval-apply routes",
            expected_trajectory=["forbidden_as_eval_apply_until_manual_owner_review > 0"],
            observed_trajectory=[f"forbidden_as_eval_apply_until_manual_owner_review={unsafe_route_count}"],
            passed=unsafe_route_count > 0,
            violation=None
            if unsafe_route_count > 0
            else "support registry does not expose forbidden route for write-capable scripts",
        )
    )

    passed = sum(1 for item in cases if item["passed"])
    return {
        "schema_version": SCHEMA_VERSION,
        "authority_boundary": "Deterministic route trajectory harness; it checks route sequence and stop-lines, not central proof acceptance.",
        "source_eval_refs": sorted(required_refs),
        "summary": {
            "cases": len(cases),
            "passed": passed,
            "failed": len(cases) - passed,
        },
        "cases": cases,
    }


def render_text(payload: dict[str, Any]) -> str:
    lines = [
        "# aoa-eval Route Trajectory Harness",
        "",
        payload["authority_boundary"],
        "",
        f"Passed {payload['summary']['passed']} / {payload['summary']['cases']} cases.",
        "",
    ]
    for case in payload["cases"]:
        mark = "PASS" if case["passed"] else "FAIL"
        lines.append(f"- {mark} `{case['case_id']}`: {case['claim']}")
        if case.get("violation"):
            lines.append(f"  violation: {case['violation']}")
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    evals_root = Path(args.evals_root).resolve()
    dashboard, support_registry = readiness.build_dashboard(
        evals_root=evals_root,
        workspace_root=Path(args.workspace_root).resolve(),
        aoa_root=Path(args.aoa_root).resolve(),
        skills_source_root=Path(args.skills_source_root).resolve(),
        installed_skills_root=Path(args.installed_skills_root).resolve(),
        stack_root=readiness.selected_stack_root(Path(args.stack_root).resolve() if args.stack_root else None),
        include_live_checks=not args.no_live_checks,
        live_timeout=args.live_timeout,
    )
    session_payload = aoa_eval_session_start.build_session_start_payload(dashboard, support_registry)
    sentinel_payload = sentinel.build_sentinel_payload(
        dashboard=dashboard,
        support_registry=support_registry,
        evals_root=evals_root,
        max_generated_age_hours=24,
    )
    payload = evaluate_route_trajectory(
        dashboard=dashboard,
        support_registry=support_registry,
        session_payload=session_payload,
        sentinel_payload=sentinel_payload,
    )
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(render_text(payload), end="")
    return 0 if payload["summary"]["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
