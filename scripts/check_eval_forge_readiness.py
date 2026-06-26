#!/usr/bin/env python3
"""Check the OS Abyss Eval Forge readiness layer."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

import build_eval_readiness_dashboard as readiness
import check_eval_freshness_sentinel as freshness_sentinel
import check_eval_support_registry as support_registry_review


SCHEMA_VERSION = "os_abyss_eval_forge_readiness_check_v1"
STATUS_RANK = {"ok": 0, "warning": 1, "error": 2}
REQUIRED_SESSION_PACKET_IDS = {
    "packet:session:aoa-eval-criteria-before-mining",
    "packet:session:aoa-eval-goal-shrink-completion-overclaim",
    "packet:session:aoa-eval-keyword-mining-blindspot",
    "packet:session:aoa-eval-session-front-door-actionability-gap",
    "packet:session:aoa-eval-working-process-fossilized-as-doctrine",
}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", default=str(readiness.DEFAULT_WORKSPACE_ROOT))
    parser.add_argument("--evals-root", default=str(readiness.REPO_ROOT))
    parser.add_argument("--aoa-root", default=str(readiness.DEFAULT_AOA_ROOT))
    parser.add_argument("--skills-source-root", default=str(readiness.DEFAULT_SKILLS_SOURCE_ROOT))
    parser.add_argument("--installed-skills-root", default=str(readiness.DEFAULT_INSTALLED_SKILLS_ROOT))
    parser.add_argument("--stack-root", default="")
    parser.add_argument("--live-timeout", type=int, default=30)
    parser.add_argument("--max-generated-age-hours", type=float, default=24.0)
    parser.add_argument("--no-live-checks", action="store_true")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on warnings as well as errors.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    return parser.parse_args(argv)


def status_max(values: Sequence[str]) -> str:
    if not values:
        return "ok"
    return max(values, key=lambda value: STATUS_RANK.get(value, 99))


def gate(
    gate_id: str,
    *,
    status: str,
    reason: str,
    evidence: dict[str, Any] | None = None,
    next_command: str | None = None,
) -> dict[str, Any]:
    return {
        "id": gate_id,
        "status": status,
        "reason": reason,
        "evidence": evidence or {},
        "next_command": next_command,
    }


def file_contains(path: Path, needles: Sequence[str]) -> tuple[bool, list[str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return False, list(needles)
    missing = [needle for needle in needles if needle not in text]
    return not missing, missing


def selected_stack_root(value: str | None) -> Path | None:
    explicit = Path(value).resolve() if value else None
    return readiness.selected_stack_root(explicit)


def build_dirty_state_gate(dashboard: dict[str, Any]) -> dict[str, Any]:
    summary = dashboard.get("workspace_git_drift", {}).get("summary", {})
    dirty_count = int(summary.get("dirty_repos") or 0) if isinstance(summary, dict) else 0
    if dirty_count:
        return gate(
            "dirty_state_gate",
            status="warning",
            reason="workspace has dirty repositories; classify before editing and ignore unrelated changes",
            evidence={"dirty_repos": dirty_count, "summary": summary},
            next_command="git status --short --branch in affected repositories",
        )
    return gate(
        "dirty_state_gate",
        status="ok",
        reason="workspace git summary reports no dirty repositories",
        evidence={"summary": summary},
    )


def build_mcp_write_side_gate(stack_root: Path | None) -> dict[str, Any]:
    if stack_root is None:
        return gate(
            "mcp_write_side_gate",
            status="error",
            reason="abyss-stack root was not found, so aoa-evals-mcp write side cannot be checked",
        )
    core_path = stack_root / "mcp/services/aoa-evals-mcp/src/aoa_evals_mcp/core.py"
    tests_path = stack_root / "mcp/services/aoa-evals-mcp/tests/test_evals_mcp.py"
    core_ok, core_missing = file_contains(
        core_path,
        [
            "write_receipt",
            "aoa_evals_local_write_receipt_v1",
            "allowed_relative_globs",
            "proof_authority",
            "promotion_allowed",
        ],
    )
    tests_ok, tests_missing = file_contains(
        tests_path,
        [
            "write_receipt",
            "aoa_evals_local_write_receipt_v1",
        ],
    )
    missing = [f"core:{item}" for item in core_missing] + [f"tests:{item}" for item in tests_missing]
    return gate(
        "mcp_write_side_gate",
        status="ok" if core_ok and tests_ok else "error",
        reason=(
            "aoa-evals-mcp local write side exposes dry-run/path-bounded audit receipts"
            if core_ok and tests_ok
            else "aoa-evals-mcp local write side is missing audit receipt source or test coverage"
        ),
        evidence={
            "stack_root": stack_root.as_posix(),
            "core_path": core_path.as_posix(),
            "tests_path": tests_path.as_posix(),
            "missing_markers": missing,
        },
        next_command="python mcp/services/aoa-evals-mcp/scripts/validate_evals_mcp.py",
    )


def build_payload(
    *,
    evals_root: Path,
    workspace_root: Path,
    aoa_root: Path,
    skills_source_root: Path,
    installed_skills_root: Path,
    stack_root: Path | None,
    include_live_checks: bool,
    live_timeout: int,
    max_generated_age_hours: float,
) -> dict[str, Any]:
    dashboard, support_registry = readiness.build_dashboard(
        evals_root=evals_root,
        workspace_root=workspace_root,
        aoa_root=aoa_root,
        skills_source_root=skills_source_root,
        installed_skills_root=installed_skills_root,
        stack_root=stack_root,
        include_live_checks=include_live_checks,
        live_timeout=live_timeout,
    )
    sentinel = freshness_sentinel.build_sentinel_payload(
        dashboard=dashboard,
        support_registry=support_registry,
        evals_root=evals_root,
        max_generated_age_hours=max_generated_age_hours,
    )
    support_review = support_registry_review.build_review_payload(support_registry)
    dashboard_shape_issues = readiness.validate_dashboard_shape(dashboard, support_registry)

    local_summary = dashboard["local_eval_ports"]["summary"]
    candidate_queue = dashboard["candidate_queue"]
    candidate_ids = {str(item.get("candidate_id")) for item in candidate_queue.get("entries", []) if isinstance(item, dict)}
    missing_packets = sorted(REQUIRED_SESSION_PACKET_IDS.difference(candidate_ids))
    mining_status = dashboard["trigger_criteria"]["session_mining_status"]
    docs_guide = evals_root / "docs/guides/EVAL_FORGE_READINESS_LAYER.md"
    docs_map = evals_root / "docs/README.md"
    root_readme = evals_root / "README.md"

    docs_ok = all(path.is_file() for path in (docs_guide, docs_map, root_readme))
    docs_markers_ok, docs_missing = file_contains(
        docs_map,
        ["Eval Forge Readiness Layer", "check_eval_forge_readiness.py"],
    )
    root_markers_ok, root_missing = file_contains(root_readme, ["Eval Forge Readiness Layer"])

    gates = [
        gate(
            "freshness_gate",
            status="error" if sentinel["overall_severity"] == "error" else ("warning" if sentinel["overall_severity"] == "warning" else "ok"),
            reason="freshness sentinel has no errors" if sentinel["overall_severity"] != "error" else "freshness sentinel reports errors",
            evidence={
                "overall_severity": sentinel["overall_severity"],
                "signals": [
                    {"id": item["id"], "severity": item["severity"], "status": item["status"]}
                    for item in sentinel.get("signals", [])
                ],
            },
            next_command="python scripts/check_eval_freshness_sentinel.py --json",
        ),
        build_dirty_state_gate(dashboard),
        gate(
            "trigger_rubric_gate",
            status="ok" if len(dashboard["trigger_criteria"]["taxonomy"]) >= 8 else "error",
            reason="trigger taxonomy and admission packet schema are present",
            evidence={
                "trigger_class_count": len(dashboard["trigger_criteria"]["taxonomy"]),
                "sample_schema": dashboard["trigger_criteria"]["sample_packet_schema"]["schema_version"],
            },
            next_command="open docs/guides/AGENT_TRACE_EVAL_CANDIDATE_DISCOVERY.md",
        ),
        gate(
            "manual_session_mining_gate",
            status="ok" if not missing_packets and int(mining_status.get("reviewed_count") or 0) >= 20 else "error",
            reason="manual mining report reviewed real episodes and imported the five known candidate packets",
            evidence={
                "reviewed_count": mining_status.get("reviewed_count"),
                "packetized_count": mining_status.get("packetized_count"),
                "missing_required_packet_ids": missing_packets,
                "report_refs": mining_status.get("report_refs"),
            },
            next_command="python scripts/validate_eval_candidate_packets.py mechanics/audit/parts/candidate-readers/packets",
        ),
        gate(
            "repo_local_forge_flow_gate",
            status="ok"
            if int(local_summary.get("invalid") or 0) == 0
            and int(local_summary.get("validator_failed") or 0) == 0
            and int(local_summary.get("missing") or 0) == 0
            else "error",
            reason="all discovered repo-local eval ports validate and active/skeleton states are explicit",
            evidence={"local_eval_port_summary": local_summary},
            next_command="python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json",
        ),
        build_mcp_write_side_gate(stack_root),
        gate(
            "support_classification_gate",
            status="ok" if support_review["overall_severity"] == "ok" else "error",
            reason="support registry is classified for direct, candidate-only, component-only, and forbidden routes",
            evidence={
                "overall_severity": support_review["overall_severity"],
                "summary": support_review["summary"],
                "issue_count": len(support_review.get("issues", [])),
            },
            next_command="python scripts/check_eval_support_registry.py --json",
        ),
        gate(
            "freshness_drift_model_gate",
            status="ok" if dashboard["freshness_sentinel"].get("tracked_dimensions") else "error",
            reason="dashboard tracks generated age, MCP mirror, .aoa catchup, dirty repos, support registry, and local ports",
            evidence={"tracked_dimensions": dashboard["freshness_sentinel"].get("tracked_dimensions")},
            next_command="python scripts/check_eval_freshness_sentinel.py --json",
        ),
        gate(
            "agent_ux_entrypoint_gate",
            status="ok" if docs_ok and docs_markers_ok and root_markers_ok else "error",
            reason="landing guide and root docs expose one Eval Forge front door",
            evidence={
                "guide": docs_guide.as_posix(),
                "docs_map": docs_map.as_posix(),
                "root_readme": root_readme.as_posix(),
                "missing_markers": docs_missing + root_missing,
            },
            next_command="python scripts/check_eval_forge_readiness.py --json",
        ),
        gate(
            "verification_shape_gate",
            status="ok" if not dashboard_shape_issues else "error",
            reason="readiness dashboard/support registry shape validates",
            evidence={"dashboard_shape_issue_count": len(dashboard_shape_issues), "issues": dashboard_shape_issues},
            next_command="python scripts/build_eval_readiness_dashboard.py --check",
        ),
    ]
    overall = status_max([item["status"] for item in gates])
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "authority_boundary": (
            "This check proves routing readiness only. It does not accept proof, score evals, "
            "promote candidates, mutate sibling repos, or widen MCP write authority."
        ),
        "overall_status": overall,
        "gates": gates,
        "verification_commands": [
            "python scripts/aoa_eval_session_start.py --json",
            "python scripts/check_eval_forge_readiness.py --json",
            "python scripts/check_eval_freshness_sentinel.py --json",
            "python scripts/build_eval_readiness_dashboard.py --check",
            "python scripts/check_eval_support_registry.py --json",
            "python scripts/check_eval_candidate_queue_lifecycle.py --json",
            "python scripts/validate_eval_candidate_packets.py --schema-only",
            "python scripts/validate_eval_candidate_packets.py mechanics/audit/parts/candidate-readers/packets",
            "python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json",
            "python scripts/validate_repo.py",
            "python scripts/validate_semantic_agents.py",
            "python mcp/services/aoa-evals-mcp/scripts/validate_evals_mcp.py",
            "python -m pytest -q mcp/services/aoa-evals-mcp/tests",
        ],
        "warnings_are_intentional_when": [
            "freshness reports live-tail waiting for quiet window",
            "MCP federation mirror is stale but source checkout is selected",
            "dirty repositories are classified and unrelated paths are not edited",
            "unsafe side-effect scripts are present but forbidden as direct eval application",
        ],
        "dashboard_summary": {
            "generated_at_utc": dashboard.get("generated_at_utc"),
            "local_eval_ports": local_summary,
            "candidate_queue": candidate_queue.get("summary"),
            "support_registry": support_registry.get("summary"),
        },
    }


def render_text(payload: dict[str, Any]) -> str:
    lines = [
        "# OS Abyss Eval Forge Readiness Check",
        "",
        payload["authority_boundary"],
        "",
        f"overall: {payload['overall_status']}",
        "",
        "## Gates",
    ]
    for item in payload["gates"]:
        lines.append(f"- {item['status']} {item['id']}: {item['reason']}")
        if item.get("next_command"):
            lines.append(f"  next: `{item['next_command']}`")
    lines.extend(["", "## Verification Commands"])
    for command in payload["verification_commands"]:
        lines.append(f"- `{command}`")
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    stack_root = selected_stack_root(args.stack_root)
    payload = build_payload(
        evals_root=Path(args.evals_root).resolve(),
        workspace_root=Path(args.workspace_root).resolve(),
        aoa_root=Path(args.aoa_root).resolve(),
        skills_source_root=Path(args.skills_source_root).resolve(),
        installed_skills_root=Path(args.installed_skills_root).resolve(),
        stack_root=stack_root,
        include_live_checks=not args.no_live_checks,
        live_timeout=args.live_timeout,
        max_generated_age_hours=args.max_generated_age_hours,
    )
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(render_text(payload), end="")
    if payload["overall_status"] == "error":
        return 1
    if args.strict and payload["overall_status"] == "warning":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
