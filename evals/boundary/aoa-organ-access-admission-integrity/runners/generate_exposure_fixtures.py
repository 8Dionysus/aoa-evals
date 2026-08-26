#!/usr/bin/env python3
"""Render public-safe matched progressive-exposure source fixtures."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = BUNDLE_ROOT / "fixtures" / "exposure"
OBSERVED_AT = "2026-08-26T05:00:00Z"
EXPIRES_AT = "2026-08-26T06:00:00Z"
CLAIM_LIMIT = (
    "This source fixture proves deterministic disclosure accounting only. It does not prove a live endpoint, activation, owner acceptance, central proof, utility, latency, or economy effect."
)
PLAN_CLAIM_LIMIT = (
    "This candidate records deterministic disclosure identity and visibility accounting only. It does not authorize activation, execute a tool, prove runtime reachability, establish owner acceptance, or issue central proof."
)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def capability() -> dict[str, Any]:
    return {
        "organ_id": "aoa-kag",
        "capability_id": "knowledge-inspect",
        "qualified_capability_id": "aoa-kag:aoa-kag:knowledge-inspect",
        "owners": {
            "source_owner": "aoa-kag",
            "access_owner": "aoa-kag",
            "control_owner": "aoa-sdk",
            "runtime_owner": "abyss-stack",
            "proof_owner": "aoa-evals",
            "acceptance_owner": "aoa-kag",
        },
        "capability_digest": digest({"capability": "knowledge-inspect-v1"}),
        "schema_digest": "sha256:" + "d" * 64,
        "source_revision": {
            "revision": "source-exposure-fixture-v1",
            "digest": "sha256:" + "a" * 64,
        },
        "freshness": {
            "state": "fresh",
            "source_ref": "owner://aoa-kag/exposure-source",
            "source_digest": "sha256:" + "a" * 64,
            "observed_at": OBSERVED_AT,
            "expires_at": EXPIRES_AT,
            "ttl_seconds": 3600,
            "provider_watermark": "aoa-kag-exposure-v1",
            "reason_codes": [],
        },
        "effect_ceiling": "read",
        "approval_ref": None,
        "rollback_route": "owner://aoa-kag/rollback/exposure",
    }


def visible_tool() -> dict[str, Any]:
    return {
        "tool_id": "knowledge-inspect.inspect-knowledge",
        "capability_id": "knowledge-inspect",
        "primitive_id": "inspect-knowledge",
        "mcp_name": "runtime-inspect",
        "effect_class": "observe",
        "policy_family": "read",
        "input_schema_ref": "owner://aoa-kag/schema/input",
        "output_schema_ref": "owner://aoa-kag/schema/output",
        "schema_digest": "sha256:" + "d" * 64,
        "effect_ceiling": "read",
    }


def snapshot(tools: list[dict[str, Any]]) -> dict[str, Any]:
    snapshot_body = {
        "schema_version": "aoa_organ_exposure_snapshot_v1",
        "source_digest": "sha256:" + "a" * 64,
        "tools": tools,
        "visible_tool_ids": [tool["tool_id"] for tool in tools],
        "rendered_schema_digest": digest(tools),
        "rendered_bytes": len(canonical(tools)),
        "rendered_tokens": max(1, (len(canonical(tools)) + 3) // 4)
        if tools
        else None,
        "token_count_posture": "estimated" if tools else "unknown",
        "token_count_method": "utf8_bytes_per_4_v1" if tools else None,
        "observed_at": OBSERVED_AT,
        "expires_at": EXPIRES_AT,
        "refusal_reasons": [],
    }
    return {"snapshot_id": digest(snapshot_body), **snapshot_body}


def plan(*, feature_enabled: bool, baseline_ready: bool) -> dict[str, Any]:
    candidate = feature_enabled and baseline_ready
    tools = [visible_tool()] if candidate else []
    refusal_reasons = []
    if not feature_enabled:
        refusal_reasons.append("progressive_exposure_disabled")
    if not baseline_ready:
        refusal_reasons.append("baseline_not_ready")
    body = {
        "schema_version": "aoa_organ_exposure_plan_v1",
        "plan_state": "candidate" if candidate else "blocked",
        "execution_authorized": False,
        "activation_authorized": False,
        "feature_enabled": feature_enabled,
        "baseline_ready": baseline_ready,
        "request_id": "exposure-matched-request-v1",
        "capability": capability(),
        "requested_policy_family": "read",
        "requested_primitive_ids": ["inspect-knowledge"],
        "visible_tools": tools,
        "rendered_snapshot": snapshot(tools),
        "approval_ref": None,
        "rollback_route": "owner://aoa-kag/rollback/exposure",
        "requested_at": OBSERVED_AT,
        "expires_at": EXPIRES_AT,
        "expansion_reasons": (
            [
                "baseline_gate_satisfied",
                "progressive_exposure_explicitly_enabled",
                "explicit_schema_reveal",
                "ordered_tool_selection",
                "visibility_budget_recorded",
            ]
            if candidate
            else []
        ),
        "refusal_reasons": refusal_reasons,
        "claim_limit": PLAN_CLAIM_LIMIT,
    }
    unsigned = {key: value for key, value in body.items() if key != "claim_limit"}
    return {"plan_id": digest(unsigned), **body}


def rendered() -> dict[Path, str]:
    selection_digest = digest(
        {
            "qualified_capability_id": capability()["qualified_capability_id"],
            "requested_policy_family": "read",
            "requested_primitive_ids": ["inspect-knowledge"],
        }
    )
    fixtures = {
        FIXTURE_ROOT / "01-default-off.json": {
            "schema_version": "aoa_progressive_exposure_fixture_v1",
            "fixture_id": "progressive-exposure-default-off-v1",
            "mode": "default_off",
            "source_selection_digest": selection_digest,
            "plan": plan(feature_enabled=False, baseline_ready=False),
            "expected": {
                "plan_state": "blocked",
                "visible_tool_count": 0,
                "rendered_bytes": 2,
                "rendered_tokens": None,
                "economy_status": "not_run_baseline_admission_missing",
            },
        },
        FIXTURE_ROOT / "02-explicit-candidate.json": {
            "schema_version": "aoa_progressive_exposure_fixture_v1",
            "fixture_id": "progressive-exposure-explicit-candidate-v1",
            "mode": "explicit_candidate",
            "source_selection_digest": selection_digest,
            "plan": plan(feature_enabled=True, baseline_ready=True),
            "expected": {
                "plan_state": "candidate",
                "visible_tool_count": 1,
                "rendered_bytes": len(canonical([visible_tool()])),
                "rendered_tokens": max(1, (len(canonical([visible_tool()])) + 3) // 4),
                "economy_status": "not_run_baseline_admission_missing",
            },
        },
        FIXTURE_ROOT / "03-feature-off-baseline-ready.json": {
            "schema_version": "aoa_progressive_exposure_fixture_v1",
            "fixture_id": "progressive-exposure-feature-off-baseline-ready-v1",
            "mode": "feature_disabled_baseline_ready",
            "source_selection_digest": selection_digest,
            "plan": plan(feature_enabled=False, baseline_ready=True),
            "expected": {
                "plan_state": "blocked",
                "visible_tool_count": 0,
                "rendered_bytes": 2,
                "rendered_tokens": None,
                "economy_status": "not_run_baseline_admission_missing",
            },
        },
        FIXTURE_ROOT / "04-feature-enabled-baseline-missing.json": {
            "schema_version": "aoa_progressive_exposure_fixture_v1",
            "fixture_id": "progressive-exposure-feature-enabled-baseline-missing-v1",
            "mode": "feature_enabled_baseline_missing",
            "source_selection_digest": selection_digest,
            "plan": plan(feature_enabled=True, baseline_ready=False),
            "expected": {
                "plan_state": "blocked",
                "visible_tool_count": 0,
                "rendered_bytes": 2,
                "rendered_tokens": None,
                "economy_status": "not_run_baseline_admission_missing",
            },
        },
    }
    return {
        path: json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
        for path, value in fixtures.items()
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale: list[str] = []
    for path, expected in rendered().items():
        current = path.read_text(encoding="utf-8") if path.is_file() else None
        if current == expected:
            continue
        stale.append(str(path.relative_to(BUNDLE_ROOT)))
        if not args.check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8")
    if stale and args.check:
        print("stale progressive exposure fixtures:")
        for path in stale:
            print(f"  - {path}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
