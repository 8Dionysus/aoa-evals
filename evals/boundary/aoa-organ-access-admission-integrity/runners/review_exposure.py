#!/usr/bin/env python3
"""Review matched progressive-exposure fixtures without claiming economy effect."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = BUNDLE_ROOT / "fixtures" / "exposure"
CLAIM_LIMIT = (
    "This source-contract review proves deterministic disclosure accounting and fail-closed authority boundaries only. It does not prove a live endpoint, activation, owner acceptance, central proof, utility, latency, or economy effect."
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


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: fixture must be an object")
    return value


def review_fixture(fixture: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    plan = fixture.get("plan")
    expected = fixture.get("expected")
    if fixture.get("schema_version") != "aoa_progressive_exposure_fixture_v1":
        issues.append("fixture_schema_version_invalid")
    if not isinstance(plan, dict) or not isinstance(expected, dict):
        return ["fixture_plan_or_expected_missing"]
    snapshot = plan.get("rendered_snapshot")
    capability = plan.get("capability")
    tools = plan.get("visible_tools")
    if not isinstance(snapshot, dict) or not isinstance(capability, dict):
        issues.append("plan_binding_missing")
        return issues
    if not isinstance(tools, list):
        issues.append("visible_tools_not_array")
        return issues
    snapshot_tools = snapshot.get("tools")
    if snapshot_tools != tools:
        issues.append("plan_snapshot_tool_set_mismatch")
    visible_ids = snapshot.get("visible_tool_ids")
    expected_ids = [tool.get("tool_id") for tool in tools if isinstance(tool, dict)]
    if visible_ids != expected_ids:
        issues.append("visible_tool_order_or_identity_mismatch")
    if snapshot.get("rendered_bytes") != len(canonical(tools)):
        issues.append("visible_byte_accounting_mismatch")
    if snapshot.get("rendered_schema_digest") != digest(tools):
        issues.append("visible_schema_digest_mismatch")
    snapshot_unsigned = {
        key: value for key, value in snapshot.items() if key != "snapshot_id"
    }
    if snapshot.get("snapshot_id") != digest(snapshot_unsigned):
        issues.append("snapshot_not_content_addressed")
    plan_unsigned = {key: value for key, value in plan.items() if key != "plan_id"}
    if plan.get("plan_id") != digest(plan_unsigned):
        issues.append("plan_not_content_addressed")
    if plan.get("execution_authorized") is not False:
        issues.append("execution_authority_not_false")
    if plan.get("activation_authorized") is not False:
        issues.append("activation_authority_not_false")
    if capability.get("qualified_capability_id") != (
        f"{capability.get('owners', {}).get('source_owner')}:{capability.get('organ_id')}:{capability.get('capability_id')}"
    ):
        issues.append("capability_not_owner_qualified")
    for tool in tools:
        if not isinstance(tool, dict):
            issues.append("visible_tool_not_object")
            continue
        if tool.get("tool_id") != f"{tool.get('capability_id')}.{tool.get('primitive_id')}":
            issues.append("tool_id_not_capability_qualified")
        expected_policy = {
            "observe": "read",
            "derive": "read",
            "validate": "read",
            "prepare_candidate": "candidate",
        }.get(tool.get("effect_class"))
        if expected_policy != tool.get("policy_family"):
            issues.append("tool_effect_policy_mismatch")
        if tool.get("effect_ceiling") != "read":
            issues.append("tool_effect_ceiling_widened")
    mode = fixture.get("mode")
    if mode == "default_off":
        if plan.get("plan_state") != "blocked":
            issues.append("default_off_plan_not_blocked")
        if plan.get("feature_enabled") is not False:
            issues.append("default_off_feature_flag_not_false")
        if plan.get("baseline_ready") is not False:
            issues.append("default_off_baseline_not_false")
        if tools or snapshot.get("rendered_bytes") != 2:
            issues.append("default_off_revealed_schema")
        if snapshot.get("rendered_tokens") is not None:
            issues.append("default_off_reported_tokens")
        if not plan.get("refusal_reasons"):
            issues.append("default_off_refusal_reasons_missing")
    elif mode == "explicit_candidate":
        if plan.get("plan_state") != "candidate":
            issues.append("candidate_plan_not_candidate")
        if plan.get("feature_enabled") is not True:
            issues.append("candidate_feature_flag_not_true")
        if plan.get("baseline_ready") is not True:
            issues.append("candidate_baseline_flag_not_true")
        if not tools or snapshot.get("rendered_tokens") is None:
            issues.append("candidate_visibility_accounting_missing")
        if not plan.get("expansion_reasons"):
            issues.append("candidate_expansion_reasons_missing")
    else:
        issues.append("fixture_mode_unknown")
    if expected.get("plan_state") != plan.get("plan_state"):
        issues.append("expected_plan_state_mismatch")
    if expected.get("visible_tool_count") != len(tools):
        issues.append("expected_tool_count_mismatch")
    if expected.get("rendered_bytes") != snapshot.get("rendered_bytes"):
        issues.append("expected_byte_count_mismatch")
    if expected.get("rendered_tokens") != snapshot.get("rendered_tokens"):
        issues.append("expected_token_count_mismatch")
    return sorted(set(issues))


def run_scenarios() -> tuple[dict[str, Any], bool]:
    fixtures = [load(path) for path in sorted(FIXTURE_ROOT.glob("*.json"))]
    if {item.get("mode") for item in fixtures} != {
        "default_off",
        "explicit_candidate",
    }:
        raise ValueError("matched exposure fixtures are incomplete")
    breakdown: list[dict[str, Any]] = []
    for fixture in fixtures:
        issues = review_fixture(fixture)
        breakdown.append(
            {
                "fixture_id": fixture.get("fixture_id"),
                "mode": fixture.get("mode"),
                "observed": "accept" if not issues else "reject",
                "issue_codes": issues,
                "source_selection_digest": fixture.get("source_selection_digest"),
            }
        )
    selection_digests = {
        item["source_selection_digest"] for item in breakdown
    }
    if len(selection_digests) != 1:
        breakdown.append(
            {
                "fixture_id": "matched-selection",
                "mode": "pair",
                "observed": "reject",
                "issue_codes": ["matched_selection_digest_drift"],
            }
        )
    issues = [
        issue
        for item in breakdown
        for issue in item.get("issue_codes", [])
    ]
    default = next(item for item in fixtures if item["mode"] == "default_off")
    candidate = next(
        item for item in fixtures if item["mode"] == "explicit_candidate"
    )
    default_snapshot = default["plan"]["rendered_snapshot"]
    candidate_snapshot = candidate["plan"]["rendered_snapshot"]
    report = {
        "schema_version": "aoa_progressive_exposure_eval_report_v1",
        "eval_id": "aoa-organ-access-admission-integrity",
        "track": "progressive-tool-exposure",
        "integrity_verdict": (
            "supports_bounded_claim" if not issues else "does_not_support_bounded_claim"
        ),
        "fixture_breakdown": breakdown,
        "matched_selection": {
            "source_selection_digest": next(iter(selection_digests), None),
            "same_selection": len(selection_digests) == 1,
        },
        "visibility_comparison": {
            "default_off_bytes": default_snapshot["rendered_bytes"],
            "candidate_bytes": candidate_snapshot["rendered_bytes"],
            "candidate_minus_default_bytes": (
                candidate_snapshot["rendered_bytes"]
                - default_snapshot["rendered_bytes"]
            ),
            "default_off_tokens": default_snapshot["rendered_tokens"],
            "candidate_tokens": candidate_snapshot["rendered_tokens"],
            "candidate_minus_default_tokens": candidate_snapshot["rendered_tokens"],
        },
        "economy": {
            "status": "not_run_baseline_admission_missing",
            "baseline_ready": False,
            "utility_observed": False,
            "latency_observed": False,
            "promotion_authorized": False,
            "claim_limit": CLAIM_LIMIT,
        },
        "activation_authorized": False,
        "execution_authorized": False,
        "owner_acceptance_inferred": False,
        "central_proof_asserted": False,
        "claim_limit": CLAIM_LIMIT,
    }
    return report, not issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("run-scenarios",))
    parser.parse_args()
    report, passed = run_scenarios()
    print(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
