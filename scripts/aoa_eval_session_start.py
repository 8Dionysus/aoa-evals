#!/usr/bin/env python3
"""Print a session-start route packet for OS Abyss eval work."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

import build_eval_readiness_dashboard as readiness


SCHEMA_VERSION = "os_abyss_eval_session_start_v1"


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


def resolve_stack_root(value: str) -> Path | None:
    if value:
        return Path(value).resolve()
    return readiness.selected_stack_root(None)


def severity_rank(value: str) -> int:
    return {
        "blocked": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
        "none": 4,
        "unknown": 5,
    }.get(value, 6)


def active_repo_routes(dashboard: dict[str, Any], limit: int = 8) -> list[dict[str, Any]]:
    repos = dashboard.get("repo_readiness", {}).get("repos", [])
    if not isinstance(repos, list):
        return []
    active = [
        {
            "repo_id": item.get("repo_id"),
            "route_state": item.get("route_state"),
            "pressure_severity": item.get("pressure_severity"),
            "route_confidence": item.get("route_confidence"),
            "exact_next_command": item.get("exact_next_command"),
            "freshness_warnings": item.get("freshness_warnings", []),
            "suite_execution": item.get(
                "suite_execution",
                {
                    "state": "absent",
                    "execution_allowed": False,
                    "owner_apply_required": False,
                    "proof_authority": False,
                    "promotion_allowed": False,
                },
            ),
        }
        for item in repos
        if isinstance(item, dict)
        and item.get("route_state") not in {None, "no_active_eval_pressure"}
        and not str(item.get("route_state") or "").startswith("dormant")
    ]
    return sorted(
        active,
        key=lambda item: (
            severity_rank(str(item.get("pressure_severity") or "unknown")),
            str(item.get("repo_id") or ""),
        ),
    )[:limit]


def candidate_state_rank(value: str) -> int:
    return {
        "needs_owner_review": 0,
        "central_draft": 1,
        "observed": 2,
        "local_only": 3,
        "duplicate_existing_eval": 4,
        "deferred": 5,
        "accepted": 6,
        "rejected": 7,
    }.get(value, 8)


def candidate_source_rank(value: str) -> int:
    return {
        "session_episode": 0,
        "runtime_candidate_export": 1,
        "local_eval_port": 2,
    }.get(value, 3)


def candidate_queue_routes(dashboard: dict[str, Any], limit: int = 12) -> list[dict[str, Any]]:
    queue = dashboard.get("candidate_queue", {})
    entries = queue.get("entries", []) if isinstance(queue, dict) else []
    if not isinstance(entries, list):
        return []
    actionable: list[dict[str, Any]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        actionable.append(
            {
                "candidate_id": entry.get("candidate_id"),
                "state": entry.get("state"),
                "source_kind": entry.get("source_kind"),
                "owner_repo": entry.get("owner_repo"),
                "packet_ref": entry.get("packet_ref"),
                "trigger_class_id": entry.get("trigger_class_id"),
                "expected_aoa_eval_route": entry.get("expected_aoa_eval_route"),
                "review_gate": entry.get("review_gate"),
                "evidence_count": entry.get("evidence_count"),
                "next_route": entry.get("next_route"),
                "authority_boundary": entry.get("authority_boundary"),
                "proof_authority": entry.get("proof_authority", False),
                "promotion_allowed": entry.get("promotion_allowed", False),
            }
        )
    return sorted(
        actionable,
        key=lambda item: (
            candidate_state_rank(str(item.get("state") or "")),
            candidate_source_rank(str(item.get("source_kind") or "")),
            str(item.get("candidate_id") or ""),
        ),
    )[:limit]


def freshness_blockers(dashboard: dict[str, Any]) -> list[dict[str, Any]]:
    blockers: list[dict[str, Any]] = []
    mcp_status = dashboard.get("mcp_runtime_status", {})
    if isinstance(mcp_status, dict) and mcp_status.get("status") not in {"ok", "skipped"}:
        blockers.append(
            {
                "surface": "aoa-evals-mcp",
                "status": mcp_status.get("status"),
                "next_route": mcp_status.get("next_route"),
            }
        )
    aoa_status = dashboard.get("aoa_session_memory_freshness", {})
    if isinstance(aoa_status, dict) and aoa_status.get("status") not in {"ok", "skipped"}:
        blockers.append(
            {
                "surface": ".aoa",
                "status": aoa_status.get("status"),
                "next_route": aoa_status.get("next_route"),
            }
        )
    elif isinstance(aoa_status, dict):
        summary = aoa_status.get("json_summary")
        if isinstance(summary, dict):
            recommendation = summary.get("recommendation")
            next_action_id = summary.get("next_action_id")
            live_catchup_pending = summary.get("live_catchup_pending")
            maintenance_required = summary.get("maintenance_required")
            if (
                live_catchup_pending
                or maintenance_required
                or recommendation in {"run_live_catchup", "wait_live_catchup"}
            ):
                blockers.append(
                    {
                        "surface": ".aoa",
                        "status": next_action_id or recommendation or "freshness_recommendation",
                        "next_route": aoa_status.get("next_route")
                        or summary.get("exact_next_command"),
                        "warnings": [
                            f"recommendation={recommendation}",
                            f"live_tail_status={summary.get('live_tail_status')}",
                            f"next_ready_at={summary.get('live_tail_next_ready_at')}",
                        ],
                    }
                )
    for repo in active_repo_routes(dashboard, limit=20):
        warnings = repo.get("freshness_warnings")
        if warnings:
            blockers.append(
                {
                    "surface": f"repo:{repo.get('repo_id')}",
                    "status": "freshness_warning",
                    "next_route": repo.get("exact_next_command"),
                    "warnings": warnings,
                }
            )
    return blockers


def build_session_start_payload(
    dashboard: dict[str, Any],
    support_registry: dict[str, Any],
) -> dict[str, Any]:
    active_routes = active_repo_routes(dashboard)
    candidate_queue = dashboard.get("candidate_queue", {})
    queue_summary = candidate_queue.get("summary", {}) if isinstance(candidate_queue, dict) else {}
    candidate_routes = candidate_queue_routes(dashboard)
    forge = dashboard.get("eval_forge_readiness", {})
    forge_hints = forge.get("candidate_archetype_hints", []) if isinstance(forge, dict) else []
    if not isinstance(forge_hints, list):
        forge_hints = []
    forge_router_command = (
        forge.get("router_command")
        if isinstance(forge, dict)
        else "python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py --candidate-packet <path> --json"
    )
    forge_front_door = {
        "surface_refs": forge.get("front_door_refs", {}) if isinstance(forge, dict) else {},
        "exact_commands": forge.get("front_door_commands", []) if isinstance(forge, dict) else [],
        "surface_status": forge.get("front_door_surface_status", {}) if isinstance(forge, dict) else {},
        "proof_authority": False,
        "promotion_allowed": False,
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "authority_boundary": "Session-start output routes eval work; it cannot score, accept proof, promote candidates, mutate sibling repos, or execute local suite runner argv.",
        "read_model_posture": dashboard.get("read_model_posture", {}),
        "session_entry_commands": [
            {
                "purpose": "raise this per-session Eval Forge front door",
                "command": "python scripts/aoa_eval_session_start.py --json",
            },
            {
                "purpose": "check the session-ready Eval Forge gate across freshness, ports, support classes, packets, MCP write receipts, and docs",
                "command": "python scripts/check_eval_forge_readiness.py --json",
            },
            {
                "purpose": "check OS Abyss eval freshness, mirror drift, and route blockers",
                "command": "python scripts/check_eval_freshness_sentinel.py --json",
            },
            {
                "purpose": "refresh or check eval-control read-model",
                "command": "python scripts/build_eval_readiness_dashboard.py --check",
            },
            {
                "purpose": "audit validator/test/script support routes before applying them as eval support",
                "command": "python scripts/check_eval_support_registry.py --json",
            },
            {
                "purpose": "validate candidate packet contract before importing mined evidence",
                "command": "python scripts/validate_eval_candidate_packets.py --schema-only",
            },
            {
                "purpose": "validate real candidate packets currently imported into the queue",
                "command": "python scripts/validate_eval_candidate_packets.py mechanics/audit/parts/candidate-readers/packets",
            },
            {
                "purpose": "check candidate queue lifecycle routes without proof promotion",
                "command": "python scripts/check_eval_candidate_queue_lifecycle.py --json",
            },
            {
                "purpose": "dry-run local-to-central eval promotion review without creating proof",
                "command": "python scripts/review_eval_promotion_path.py --json",
            },
            {
                "purpose": "inspect workspace local eval ports",
                "command": (
                    "python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS "
                    "--json-output /tmp/aoa_local_eval_ports.current.json --json"
                ),
            },
            {
                "purpose": "route one concrete eval candidate through Eval Forge before authoring",
                "command": str(forge_router_command),
            },
        ],
        "eval_forge_front_door": forge_front_door,
        "local_suite_execution_boundary": {
            "state_vocabulary": ["absent", "invalid", "stale", "ready"],
            "aggregate_priority": ["invalid", "stale", "ready", "absent"],
            "readiness_scope": "source-contract-ready",
            "runtime_reproducibility_proven": False,
            "jit_revalidation_required": True,
            "execution_receipt_required": True,
            "environment_capture_required": True,
            "execution_allowed": False,
            "owner_apply_required_for_ready": True,
            "proof_authority": False,
            "promotion_allowed": False,
        },
        "active_repo_routes": active_routes,
        "candidate_queue_summary": queue_summary,
        "candidate_queue_routes": candidate_routes,
        "promotion_review_route": {
            "command": "python scripts/review_eval_promotion_path.py --json",
            "dry_run": True,
            "promotion_allowed": False,
            "mcp_promotion_allowed": False,
            "gates": [
                "local_owner_review",
                "central_overlap_check",
                "source_bundle_draft",
                "fixture_runner_report_contract_review",
                "human_acceptance",
                "catalog_report_regeneration",
                "release_advisory_validation",
            ],
            "purpose": "walk one active local pressure item through owner and overlap gates before any central draft",
        },
        "freshness_blockers": freshness_blockers(dashboard),
        "support_registry_summary": support_registry.get("summary", {}),
        "candidate_packet_contract": {
            "schema_ref": "mechanics/audit/parts/candidate-readers/schemas/aoa-eval-candidate-packet.schema.json",
            "validator_command": "python scripts/validate_eval_candidate_packets.py",
            "candidate_only": True,
            "proof_authority": False,
        },
        "eval_forge_readiness": {
            "schema_version": "os_abyss_eval_session_forge_readiness_v1",
            "registry_ref": forge.get("registry_ref") if isinstance(forge, dict) else None,
            "worksheet_schema_ref": forge.get("worksheet_schema_ref") if isinstance(forge, dict) else None,
            "registry_valid": (forge.get("registry_validation") or {}).get("valid") if isinstance(forge, dict) else False,
            "archetype_count": forge.get("archetype_count") if isinstance(forge, dict) else None,
            "router_command": forge_router_command,
            "local_port_pressure_hint_command": (
                forge.get("local_port_pressure_hint_command") if isinstance(forge, dict) else None
            ),
            "worksheet_write_command": (
                forge.get("worksheet_write_command") if isinstance(forge, dict) else None
            ),
            "front_door_refs": forge_front_door["surface_refs"],
            "front_door_commands": forge_front_door["exact_commands"],
            "top_candidate_hints": forge_hints[:5],
            "proof_authority": False,
            "promotion_allowed": False,
            "stop_lines": forge.get("stop_lines", []) if isinstance(forge, dict) else [],
        },
        "skill_route": {
            "source_owner": "aoa-skills",
            "runtime_adoption": dashboard.get("aoa_eval_runtime_adoption", {}),
            "use_when": [
                "eval pressure appears",
                "existing eval may apply",
                "local eval port pressure appears",
                "session/runtime evidence suggests candidate-only mining",
                "freshness may block proof claims",
            ],
        },
        "stop_lines": [
            "do not design a new eval before checking existing central/local surfaces",
            "do not treat .aoa, MCP, dashboard, generated readers, or candidate packets as proof",
            "do not apply write-capable scripts as evals without check or dry-run route",
            "do not import session evidence without candidate packet validation",
            "do not skip Eval Forge admission gates when designing a new eval from candidate pressure",
            "do not promote local eval pressure before promotion dry-run review and human owner acceptance",
            "do not treat .suite.md as runnable; only a source-contract-ready sidecar may route to owner/apply",
            "do not treat ready as pinned runtime reproducibility; owner/apply must JIT-revalidate and capture environment plus receipt",
            "session-start, readiness, dashboard, Eval Forge, inventory, promotion review, and MCP never execute runner.argv",
        ],
    }


def render_text(payload: dict[str, Any]) -> str:
    lines = [
        "# OS Abyss Eval Session Start",
        "",
        payload["authority_boundary"],
        "",
        "## First Commands",
    ]
    for item in payload["session_entry_commands"]:
        lines.append(f"- {item['purpose']}: `{item['command']}`")
    front_door = payload.get("eval_forge_front_door") or {}
    lines.extend(["", "## Forge Front Door"])
    refs = front_door.get("surface_refs") if isinstance(front_door, dict) else {}
    if isinstance(refs, dict) and refs:
        for label, ref in refs.items():
            lines.append(f"- {label}: `{ref}`")
    else:
        lines.append("- no Forge front-door refs available")
    commands = front_door.get("exact_commands") if isinstance(front_door, dict) else []
    if isinstance(commands, list) and commands:
        lines.append("- exact commands:")
        for item in commands:
            if isinstance(item, dict):
                lines.append(f"  - {item.get('purpose')}: `{item.get('command')}`")
    lines.append(
        "- proof authority: {proof}; promotion allowed: {promotion}".format(
            proof=front_door.get("proof_authority") if isinstance(front_door, dict) else None,
            promotion=front_door.get("promotion_allowed") if isinstance(front_door, dict) else None,
        )
    )
    lines.extend(["", "## Active Repo Routes"])
    routes = payload.get("active_repo_routes") or []
    if not routes:
        lines.append("- none currently actionable")
    for route in routes:
        lines.append(
            "- {repo}: {state} / {severity} / {confidence}; next `{command}`".format(
                repo=route.get("repo_id"),
                state=route.get("route_state"),
                severity=route.get("pressure_severity"),
                confidence=route.get("route_confidence"),
                command=route.get("exact_next_command"),
            )
        )
    lines.extend(["", "## Candidate Queue Routes"])
    candidates = payload.get("candidate_queue_routes") or []
    if not candidates:
        lines.append("- none currently actionable")
    for candidate in candidates:
        packet = candidate.get("packet_ref")
        packet_suffix = f"; packet `{packet}`" if packet else ""
        lines.append(
            "- {candidate}: {state} / {source} / {owner}; next {route}{packet}".format(
                candidate=candidate.get("candidate_id"),
                state=candidate.get("state"),
                source=candidate.get("source_kind"),
                owner=candidate.get("owner_repo"),
                route=candidate.get("next_route"),
                packet=packet_suffix,
            )
        )
    forge = payload.get("eval_forge_readiness") or {}
    lines.extend(["", "## Eval Forge"])
    if forge:
        lines.append(
            "- registry valid: {valid}; archetypes: {count}; router `{command}`".format(
                valid=forge.get("registry_valid"),
                count=forge.get("archetype_count"),
                command=forge.get("router_command"),
            )
        )
        local_command = forge.get("local_port_pressure_hint_command")
        if local_command:
            lines.append(f"- local-port route: `{local_command}`")
        worksheet_command = forge.get("worksheet_write_command")
        if worksheet_command:
            lines.append(f"- worksheet route: `{worksheet_command}`")
        hints = forge.get("top_candidate_hints") or []
        if hints:
            for hint in hints:
                lines.append(
                    "- {candidate}: {decision} -> `{archetype}` via `{route}`; promotion allowed: {allowed}".format(
                        candidate=hint.get("candidate_id"),
                        decision=hint.get("decision"),
                        archetype=hint.get("selected_archetype_id"),
                        route=hint.get("route_key"),
                        allowed=hint.get("promotion_allowed"),
                    )
                )
        else:
            lines.append("- no candidate archetype hints available")
    else:
        lines.append("- no Eval Forge readiness packet available")
    promotion = payload.get("promotion_review_route") or {}
    lines.extend(["", "## Promotion Review"])
    if promotion:
        gates = " -> ".join(str(gate) for gate in promotion.get("gates", []))
        lines.append(
            "- dry-run `{command}`; promotion allowed: {allowed}; MCP promotion allowed: {mcp_allowed}".format(
                command=promotion.get("command"),
                allowed=promotion.get("promotion_allowed"),
                mcp_allowed=promotion.get("mcp_promotion_allowed"),
            )
        )
        lines.append(f"- gates: {gates}")
    else:
        lines.append("- no promotion review route available")
    adoption = (payload.get("skill_route") or {}).get("runtime_adoption") or {}
    lines.extend(["", "## Skill Runtime"])
    if adoption:
        lines.append(
            "- aoa-eval posture `{posture}`; normal profile `{profile}` verified: {verified}; "
            "profile contains aoa-eval: {included}; live install exists: {live}; front door: {front_door}".format(
                posture=adoption.get("posture"),
                profile=adoption.get("normal_user_profile"),
                verified=adoption.get("normal_user_profile_verified"),
                included=adoption.get("normal_user_profile_contains_aoa_eval"),
                live=adoption.get("live_skill_exists"),
                front_door=adoption.get("front_door_invoke_capable"),
            )
        )
    else:
        lines.append("- no runtime adoption data available")
    lines.extend(["", "## Freshness Blockers"])
    blockers = payload.get("freshness_blockers") or []
    if not blockers:
        lines.append("- none reported by session-start packet")
    for blocker in blockers:
        lines.append(
            f"- {blocker.get('surface')}: {blocker.get('status')}; next {blocker.get('next_route')}"
        )
    lines.extend(["", "## Stop Lines"])
    for line in payload["stop_lines"]:
        lines.append(f"- {line}")
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    stack_root = resolve_stack_root(args.stack_root)
    dashboard, support = readiness.build_dashboard(
        evals_root=Path(args.evals_root),
        workspace_root=Path(args.workspace_root),
        aoa_root=Path(args.aoa_root),
        skills_source_root=Path(args.skills_source_root),
        installed_skills_root=Path(args.installed_skills_root),
        stack_root=stack_root,
        include_live_checks=not args.no_live_checks,
        live_timeout=args.live_timeout,
    )
    payload = build_session_start_payload(dashboard, support)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(render_text(payload), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
