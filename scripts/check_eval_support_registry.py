#!/usr/bin/env python3
"""Audit the eval support registry as an actionable routing surface."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Sequence

import build_eval_readiness_dashboard as readiness


SCHEMA_VERSION = "os_abyss_eval_support_registry_review_v1"
SEVERITY_RANK = {"ok": 0, "warning": 1, "error": 2}
DIRECT_APPLY_CLASSES = {
    "deterministic_validator",
    "generated_parity_check",
    "unit_contract_property_test",
    "trace_trajectory_eval_support",
}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evals-root", default=str(readiness.REPO_ROOT))
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    return parser.parse_args(argv)


def issue(
    *,
    issue_id: str,
    severity: str,
    path: str,
    reason: str,
    owner_surface: str | None = None,
    next_route: str | None = None,
) -> dict[str, Any]:
    return {
        "id": issue_id,
        "severity": severity,
        "path": path,
        "reason": reason,
        "owner_surface": owner_surface,
        "next_route": next_route,
    }


def severity_max(values: Sequence[str]) -> str:
    if not values:
        return "ok"
    return max(values, key=lambda value: SEVERITY_RANK.get(value, 99))


def side_effects_mentions_write(entry: dict[str, Any]) -> bool:
    side_effects = str(entry.get("side_effects") or "").lower()
    return any(
        token in side_effects
        for token in (
            "writes ",
            "writes tracked",
            "scaffolds ",
            "creates ",
            "mutates",
            "deletes ",
            "rewrites ",
            "overwrites ",
        )
    )


def audit_surface(entry: dict[str, Any]) -> list[dict[str, Any]]:
    path = str(entry.get("path") or "<unknown>")
    owner_surface = entry.get("owner_surface") if isinstance(entry.get("owner_surface"), str) else None
    semantic_class = str(entry.get("semantic_class") or "")
    review_status = str(entry.get("review_status") or "")
    recommended_route = str(entry.get("recommended_route") or "")
    forbidden = entry.get("forbidden_interpretations")
    evidence = entry.get("classification_evidence")
    eval_relevant = entry.get("eval_lane_relevant") is True
    safe_direct = entry.get("safe_to_apply_directly") is True
    problems: list[dict[str, Any]] = []

    if not review_status:
        problems.append(
            issue(
                issue_id="support_registry_missing_review_status",
                severity="error",
                path=path,
                reason="support entry has no review_status",
                owner_surface=owner_surface,
            )
        )
    if not semantic_class:
        problems.append(
            issue(
                issue_id="support_registry_missing_semantic_class",
                severity="error",
                path=path,
                reason="support entry has no semantic_class",
                owner_surface=owner_surface,
            )
        )
    if not owner_surface:
        problems.append(
            issue(
                issue_id="support_registry_missing_owner_surface",
                severity="error",
                path=path,
                reason="support entry has no owner surface, so an agent cannot route failures safely",
            )
        )
    if not isinstance(forbidden, list) or not forbidden:
        problems.append(
            issue(
                issue_id="support_registry_missing_forbidden_interpretations",
                severity="error",
                path=path,
                reason="support entry does not name forbidden interpretations",
                owner_surface=owner_surface,
            )
        )

    if eval_relevant:
        if review_status == "manual_review_required":
            problems.append(
                issue(
                    issue_id="support_registry_unresolved_eval_relevant_review",
                    severity="error",
                    path=path,
                    reason="eval-relevant surface still needs manual semantic review before routing",
                    owner_surface=owner_surface,
                    next_route="classify this surface or downgrade it with an explicit reason",
                )
            )
        if not isinstance(evidence, list) or not evidence:
            problems.append(
                issue(
                    issue_id="support_registry_missing_classification_evidence",
                    severity="error",
                    path=path,
                    reason="eval-relevant surface has no evidence explaining its semantic class",
                    owner_surface=owner_surface,
                )
            )
        if semantic_class == "ordinary_support":
            problems.append(
                issue(
                    issue_id="support_registry_relevant_but_ordinary",
                    severity="error",
                    path=path,
                    reason="eval-relevant surface was classified as ordinary support",
                    owner_surface=owner_surface,
                )
            )

    if safe_direct:
        if semantic_class not in DIRECT_APPLY_CLASSES:
            problems.append(
                issue(
                    issue_id="support_registry_unsafe_direct_apply_class",
                    severity="error",
                    path=path,
                    reason=(
                        "safe_to_apply_directly is only allowed for deterministic validators, "
                        "generated parity checks, and unit/contract/property or trace trajectory tests"
                    ),
                    owner_surface=owner_surface,
                )
            )
        if recommended_route != "apply_as_deterministic_eval_support":
            problems.append(
                issue(
                    issue_id="support_registry_direct_apply_route_mismatch",
                    severity="error",
                    path=path,
                    reason="safe direct support must use apply_as_deterministic_eval_support",
                    owner_surface=owner_surface,
                )
            )
        if side_effects_mentions_write(entry):
            problems.append(
                issue(
                    issue_id="support_registry_write_surface_marked_direct_apply",
                    severity="error",
                    path=path,
                    reason="write-capable support surface cannot be a direct eval-apply route",
                    owner_surface=owner_surface,
                )
            )

    if semantic_class == "unsafe_side_effect_script":
        if safe_direct:
            problems.append(
                issue(
                    issue_id="support_registry_unsafe_writer_marked_safe",
                    severity="error",
                    path=path,
                    reason="unsafe side-effect script is marked safe_to_apply_directly",
                    owner_surface=owner_surface,
                )
            )
        if recommended_route != "forbidden_as_eval_apply_until_manual_owner_review":
            problems.append(
                issue(
                    issue_id="support_registry_unsafe_writer_route_mismatch",
                    severity="error",
                    path=path,
                    reason="unsafe side-effect script must route through manual owner review",
                    owner_surface=owner_surface,
                )
            )

    return problems


def build_review_payload(support_registry: dict[str, Any]) -> dict[str, Any]:
    surfaces = support_registry.get("surfaces") if isinstance(support_registry, dict) else []
    if not isinstance(surfaces, list):
        surfaces = []
    issues: list[dict[str, Any]] = []
    by_semantic_class: Counter[str] = Counter()
    by_review_status: Counter[str] = Counter()
    by_recommended_route: Counter[str] = Counter()
    relevant_count = 0
    reviewed_relevant_count = 0
    downgraded_count = 0
    safe_direct_count = 0
    unsafe_writer_count = 0

    for entry in surfaces:
        if not isinstance(entry, dict):
            continue
        semantic_class = str(entry.get("semantic_class") or "unknown")
        review_status = str(entry.get("review_status") or "unknown")
        route = str(entry.get("recommended_route") or "unknown")
        by_semantic_class[semantic_class] += 1
        by_review_status[review_status] += 1
        by_recommended_route[route] += 1
        if entry.get("eval_lane_relevant") is True:
            relevant_count += 1
            if review_status != "manual_review_required":
                reviewed_relevant_count += 1
        elif review_status == "not_eval_relevant":
            downgraded_count += 1
        if entry.get("safe_to_apply_directly") is True:
            safe_direct_count += 1
        if semantic_class == "unsafe_side_effect_script":
            unsafe_writer_count += 1
        issues.extend(audit_surface(entry))

    overall = severity_max([str(item["severity"]) for item in issues])
    return {
        "schema_version": SCHEMA_VERSION,
        "authority_boundary": (
            "This review audits eval-support routing metadata. It does not run support "
            "commands, accept proof, promote candidates, or mutate repository state."
        ),
        "overall_severity": overall,
        "summary": {
            "total_surfaces": len(surfaces),
            "eval_lane_relevant": relevant_count,
            "reviewed_eval_relevant": reviewed_relevant_count,
            "explicitly_downgraded": downgraded_count,
            "safe_to_apply_directly": safe_direct_count,
            "unsafe_side_effect_scripts": unsafe_writer_count,
            "by_semantic_class": dict(sorted(by_semantic_class.items())),
            "by_review_status": dict(sorted(by_review_status.items())),
            "by_recommended_route": dict(sorted(by_recommended_route.items())),
        },
        "invariants": [
            "eval-relevant support surfaces must not remain manual_review_required",
            "eval-relevant support surfaces must carry classification evidence",
            "safe direct apply is restricted to deterministic validators, generated parity checks, and tests",
            "write-capable scripts cannot be direct eval-apply routes",
            "unsafe side-effect scripts route to manual owner review only",
        ],
        "issues": issues,
    }


def render_text(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# Eval Support Registry Review",
        "",
        payload["authority_boundary"],
        "",
        f"overall: {payload['overall_severity']}",
        f"surfaces: {summary['total_surfaces']}",
        f"eval-lane relevant reviewed: {summary['reviewed_eval_relevant']}/{summary['eval_lane_relevant']}",
        f"explicitly downgraded: {summary['explicitly_downgraded']}",
        f"safe direct routes: {summary['safe_to_apply_directly']}",
        f"unsafe side-effect scripts: {summary['unsafe_side_effect_scripts']}",
        "",
        "## Issues",
    ]
    issues = payload.get("issues") or []
    if not issues:
        lines.append("- none")
    for item in issues:
        lines.append(
            "- {severity} {id} {path}: {reason}".format(
                severity=item.get("severity"),
                id=item.get("id"),
                path=item.get("path"),
                reason=item.get("reason"),
            )
        )
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    support_registry = readiness.build_support_registry(Path(args.evals_root))
    payload = build_review_payload(support_registry)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(render_text(payload), end="")
    return 0 if payload["overall_severity"] != "error" else 2


if __name__ == "__main__":
    raise SystemExit(main())
