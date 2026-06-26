#!/usr/bin/env python3
"""Check OS Abyss eval-control freshness and route drift."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

import build_eval_readiness_dashboard as readiness


SCHEMA_VERSION = "os_abyss_eval_freshness_sentinel_check_v1"
SEVERITY_RANK = {"ok": 0, "info": 1, "warning": 2, "error": 3}


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
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero on warnings as well as errors.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    return parser.parse_args(argv)


def severity_max(values: Sequence[str]) -> str:
    if not values:
        return "ok"
    return max(values, key=lambda item: SEVERITY_RANK.get(item, 99))


def signal(
    *,
    signal_id: str,
    severity: str,
    surface: str,
    status: str,
    reason: str,
    owner: str,
    next_command: str | None = None,
) -> dict[str, Any]:
    return {
        "id": signal_id,
        "severity": severity,
        "surface": surface,
        "status": status,
        "reason": reason,
        "owner": owner,
        "next_command": next_command,
    }


def generated_age_signal(evals_root: Path, *, max_age_hours: float, now: datetime) -> dict[str, Any]:
    path = evals_root / "generated" / "eval_readiness_dashboard.json"
    if not path.exists():
        return signal(
            signal_id="generated_dashboard_missing",
            severity="error",
            surface="generated/eval_readiness_dashboard.json",
            status="missing",
            reason="freshness sentinel needs the generated dashboard read-model to exist",
            owner="aoa-evals/generated",
            next_command="python scripts/build_eval_readiness_dashboard.py --write-generated",
        )
    mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    age_hours = max(0.0, (now - mtime).total_seconds() / 3600)
    severity = "warning" if age_hours > max_age_hours else "ok"
    return signal(
        signal_id="generated_dashboard_age",
        severity=severity,
        surface="generated/eval_readiness_dashboard.json",
        status=f"{age_hours:.2f}h",
        reason=(
            f"generated dashboard age is {age_hours:.2f}h; max configured age is "
            f"{max_age_hours:.2f}h"
        ),
        owner="aoa-evals/generated",
        next_command="python scripts/build_eval_readiness_dashboard.py --write-generated"
        if severity == "warning"
        else None,
    )


def mcp_signals(dashboard: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    mcp = dashboard.get("mcp_runtime_status")
    if not isinstance(mcp, dict):
        return [
            signal(
                signal_id="mcp_runtime_status_missing",
                severity="error",
                surface="aoa-evals-mcp",
                status="missing",
                reason="dashboard has no MCP runtime status object",
                owner="abyss-stack/aoa-evals-mcp",
            )
        ]
    status = str(mcp.get("status") or "unknown")
    if status not in {"ok", "skipped"}:
        result.append(
            signal(
                signal_id="mcp_runtime_status_unhealthy",
                severity="error",
                surface="aoa-evals-mcp",
                status=status,
                reason="MCP runtime-status command did not return a healthy JSON payload",
                owner="abyss-stack/aoa-evals-mcp",
                next_command=mcp.get("next_route"),
            )
        )
    payload = mcp.get("json") if isinstance(mcp.get("json"), dict) else {}
    freshness = payload.get("freshness") if isinstance(payload.get("freshness"), dict) else {}
    if freshness.get("mirror_is_stale") is True:
        result.append(
            signal(
                signal_id="mcp_federation_mirror_stale",
                severity="warning",
                surface="aoa-evals-mcp federation mirror",
                status=str(freshness.get("status") or "stale"),
                reason="MCP selected source is usable, but federation mirror is stale",
                owner="abyss-stack/aoa-evals-mcp",
                next_command=str(
                    freshness.get("refresh_command")
                    or "scripts/aoa-sync-federation-surfaces --layer aoa-evals"
                ),
            )
        )
    return result


def aoa_signals(dashboard: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    freshness = dashboard.get("aoa_session_memory_freshness")
    if not isinstance(freshness, dict):
        return [
            signal(
                signal_id="aoa_freshness_missing",
                severity="error",
                surface=".aoa",
                status="missing",
                reason="dashboard has no .aoa freshness object",
                owner=".aoa",
            )
        ]
    status = str(freshness.get("status") or "unknown")
    if status not in {"ok", "skipped"}:
        result.append(
            signal(
                signal_id="aoa_freshness_unhealthy",
                severity="error",
                surface=".aoa session memory",
                status=status,
                reason=".aoa maintenance-status did not return healthy freshness",
                owner=".aoa",
                next_command=freshness.get("next_route"),
            )
        )
    summary = freshness.get("json_summary") if isinstance(freshness.get("json_summary"), dict) else {}
    if summary.get("live_catchup_pending") is True or summary.get("recommendation") not in {
        None,
        "ok",
        "current",
    }:
        result.append(
            signal(
                signal_id="aoa_live_catchup_pending",
                severity="warning",
                surface=".aoa session memory",
                status=str(summary.get("recommendation") or "live_catchup_pending"),
                reason=".aoa is usable but has deferred live catchup or a freshness recommendation",
                owner=".aoa",
                next_command=str(summary.get("exact_next_command") or freshness.get("next_route") or ""),
            )
        )
    return result


def support_registry_signals(support_registry: dict[str, Any]) -> list[dict[str, Any]]:
    summary = support_registry.get("summary") if isinstance(support_registry, dict) else {}
    review_status = summary.get("by_review_status") if isinstance(summary, dict) else {}
    recommended = summary.get("by_recommended_route") if isinstance(summary, dict) else {}
    unsafe_count = int(summary.get("unsafe_side_effect_scripts") or 0) if isinstance(summary, dict) else 0
    unresolved = int(review_status.get("manual_review_required") or 0) if isinstance(review_status, dict) else 0
    result: list[dict[str, Any]] = []
    if unresolved:
        result.append(
            signal(
                signal_id="support_registry_unresolved_manual_review",
                severity="error",
                surface="generated/eval_support_registry.json",
                status=str(unresolved),
                reason="eval-relevant support surfaces still require unresolved manual review",
                owner="aoa-evals/scripts",
                next_command="python scripts/build_eval_readiness_dashboard.py --write-generated",
            )
        )
    if unsafe_count:
        result.append(
            signal(
                signal_id="support_registry_unsafe_writers",
                severity="warning",
                surface="generated/eval_support_registry.json",
                status=str(unsafe_count),
                reason="write-capable scripts are present and must not be direct eval-apply routes",
                owner="aoa-evals/scripts",
                next_command="inspect entries with recommended_route=forbidden_as_eval_apply_until_manual_owner_review",
            )
        )
    component_count = 0
    if isinstance(recommended, dict):
        component_count = int(recommended.get("component_only_use_owning_validator_or_lane_command") or 0)
    if component_count:
        result.append(
            signal(
                signal_id="support_registry_component_only_validators",
                severity="info",
                surface="generated/eval_support_registry.json",
                status=str(component_count),
                reason="validator helper components are reviewed but must be reached through owning validators or lane commands",
                owner="aoa-evals/scripts",
            )
        )
    return result


def local_port_signals(dashboard: dict[str, Any]) -> list[dict[str, Any]]:
    local_ports = dashboard.get("local_eval_ports")
    summary = local_ports.get("summary") if isinstance(local_ports, dict) else {}
    invalid = int(summary.get("invalid") or 0) if isinstance(summary, dict) else 0
    active = int(summary.get("active") or 0) if isinstance(summary, dict) else 0
    result: list[dict[str, Any]] = []
    if invalid:
        result.append(
            signal(
                signal_id="local_eval_port_invalid",
                severity="error",
                surface="repo-local evals/",
                status=str(invalid),
                reason="one or more local eval ports are invalid and block safe route selection",
                owner="repo-local evals/ + aoa-evals local-port contract",
                next_command="python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json",
            )
        )
    if active:
        result.append(
            signal(
                signal_id="local_eval_port_active_pressure",
                severity="info",
                surface="repo-local evals/",
                status=str(active),
                reason="active local eval pressure exists and should be routed before new central design",
                owner="repo-local evals/",
                next_command="python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json",
            )
        )
    return result


def git_drift_signals(dashboard: dict[str, Any]) -> list[dict[str, Any]]:
    git = dashboard.get("workspace_git_drift")
    summary = git.get("summary") if isinstance(git, dict) else {}
    dirty = int(summary.get("dirty_repos") or 0) if isinstance(summary, dict) else 0
    if not dirty:
        return []
    return [
        signal(
            signal_id="workspace_dirty_repos",
            severity="warning",
            surface="workspace git drift",
            status=str(dirty),
            reason="dirty repositories can change eval route interpretation; inspect before proof claims",
            owner="repo owners",
            next_command="git status --short in affected repositories",
        )
    ]


def build_sentinel_payload(
    *,
    dashboard: dict[str, Any],
    support_registry: dict[str, Any],
    evals_root: Path,
    max_generated_age_hours: float,
    now: datetime | None = None,
) -> dict[str, Any]:
    now = now or datetime.now(timezone.utc)
    signals = [
        generated_age_signal(evals_root, max_age_hours=max_generated_age_hours, now=now),
        *mcp_signals(dashboard),
        *aoa_signals(dashboard),
        *support_registry_signals(support_registry),
        *local_port_signals(dashboard),
        *git_drift_signals(dashboard),
    ]
    overall = severity_max([str(item["severity"]) for item in signals])
    actionable = [
        item
        for item in signals
        if item["severity"] in {"warning", "error"} and item.get("next_command")
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at_utc": now.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "authority_boundary": "Freshness sentinel reports drift and owner routes; it does not sync mirrors, mutate repos, score evals, or accept proof.",
        "overall_severity": overall,
        "exit_policy": {
            "default_nonzero_on": ["error"],
            "strict_nonzero_on": ["warning", "error"],
        },
        "signals": signals,
        "next_commands": actionable,
    }


def render_text(payload: dict[str, Any]) -> str:
    lines = [
        "# OS Abyss Eval Freshness Sentinel",
        "",
        f"Overall severity: `{payload['overall_severity']}`",
        "",
        payload["authority_boundary"],
        "",
        "## Signals",
    ]
    for item in payload["signals"]:
        lines.append(
            "- {severity} {surface}: {status} - {reason}".format(
                severity=item["severity"],
                surface=item["surface"],
                status=item["status"],
                reason=item["reason"],
            )
        )
        if item.get("next_command"):
            lines.append(f"  next: `{item['next_command']}`")
    return "\n".join(lines) + "\n"


def exit_code(payload: dict[str, Any], *, strict: bool) -> int:
    severity = str(payload.get("overall_severity") or "error")
    if severity == "error":
        return 2
    if strict and severity == "warning":
        return 2
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    evals_root = Path(args.evals_root).resolve()
    stack_root = readiness.selected_stack_root(Path(args.stack_root).resolve() if args.stack_root else None)
    dashboard, support_registry = readiness.build_dashboard(
        evals_root=evals_root,
        workspace_root=Path(args.workspace_root).resolve(),
        aoa_root=Path(args.aoa_root).resolve(),
        skills_source_root=Path(args.skills_source_root).resolve(),
        installed_skills_root=Path(args.installed_skills_root).resolve(),
        stack_root=stack_root,
        include_live_checks=not args.no_live_checks,
        live_timeout=args.live_timeout,
    )
    payload = build_sentinel_payload(
        dashboard=dashboard,
        support_registry=support_registry,
        evals_root=evals_root,
        max_generated_age_hours=args.max_generated_age_hours,
    )
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(render_text(payload), end="")
    return exit_code(payload, strict=args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
