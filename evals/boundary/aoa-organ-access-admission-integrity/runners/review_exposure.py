#!/usr/bin/env python3
"""Review matched progressive-exposure fixtures without claiming economy effect."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from typing import Any

BUNDLE_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = BUNDLE_ROOT / "fixtures" / "exposure"
CLAIM_LIMIT = (
    "This source-contract review proves deterministic disclosure accounting and fail-closed authority boundaries only. It does not prove a live endpoint, activation, owner acceptance, central proof, utility, latency, or economy effect."
)
PLAN_CLAIM_LIMIT = (
    "This candidate records deterministic disclosure identity and visibility accounting only. It does not authorize activation, execute a tool, prove runtime reachability, establish owner acceptance, or issue central proof."
)
EXPECTED_EXPANSION_REASONS = (
    "baseline_gate_satisfied",
    "progressive_exposure_explicitly_enabled",
    "explicit_schema_reveal",
    "ordered_tool_selection",
    "visibility_budget_recorded",
)
EXPECTED_MODES = {
    "default_off",
    "explicit_candidate",
    "feature_disabled_baseline_ready",
    "feature_enabled_baseline_missing",
}
POLICY_RANK = {"read": 0, "candidate": 1}
OWNER_FIELDS = {
    "source_owner",
    "access_owner",
    "control_owner",
    "runtime_owner",
    "proof_owner",
    "acceptance_owner",
}


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
        raise TypeError(f"{path}: fixture must be an object")
    return value


def selection_identity(plan: Mapping[str, Any]) -> dict[str, Any] | None:
    capability = plan.get("capability")
    primitive_ids = plan.get("requested_primitive_ids")
    if not isinstance(capability, Mapping) or not isinstance(primitive_ids, list):
        return None
    if not all(isinstance(item, str) and item for item in primitive_ids):
        return None
    qualified = capability.get("qualified_capability_id")
    capability_digest = capability.get("capability_digest")
    schema_digest = capability.get("schema_digest")
    source_revision = capability.get("source_revision")
    owners = capability.get("owners")
    policy = plan.get("requested_policy_family")
    if (
        not isinstance(qualified, str)
        or not qualified
        or not isinstance(capability_digest, str)
        or not capability_digest
        or not isinstance(schema_digest, str)
        or not schema_digest
        or not isinstance(source_revision, Mapping)
        or not isinstance(source_revision.get("revision"), str)
        or not source_revision.get("revision")
        or not isinstance(source_revision.get("digest"), str)
        or not source_revision.get("digest")
        or not isinstance(owners, Mapping)
        or set(owners) != OWNER_FIELDS
        or not all(isinstance(value, str) and value for value in owners.values())
        or not isinstance(policy, str)
    ):
        return None
    return {
        "qualified_capability_id": qualified,
        "capability_digest": capability_digest,
        "schema_digest": schema_digest,
        "source_revision": dict(source_revision),
        "owners": dict(owners),
        "requested_policy_family": policy,
        "requested_primitive_ids": primitive_ids,
    }


def snapshot_metrics(fixture: Mapping[str, Any]) -> tuple[int, int | None]:
    plan = fixture.get("plan")
    snapshot = plan.get("rendered_snapshot") if isinstance(plan, Mapping) else None
    if not isinstance(snapshot, Mapping):
        return 0, None
    rendered_bytes = snapshot.get("rendered_bytes")
    rendered_tokens = snapshot.get("rendered_tokens")
    safe_bytes = (
        rendered_bytes
        if isinstance(rendered_bytes, int) and not isinstance(rendered_bytes, bool)
        and rendered_bytes >= 0
        else 0
    )
    safe_tokens = (
        rendered_tokens
        if isinstance(rendered_tokens, int)
        and not isinstance(rendered_tokens, bool)
        and rendered_tokens >= 0
        else None
    )
    return safe_bytes, safe_tokens


def parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def review_fixture(fixture: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    plan = fixture.get("plan")
    expected = fixture.get("expected")
    if fixture.get("schema_version") != "aoa_progressive_exposure_fixture_v1":
        issues.append("fixture_schema_version_invalid")
    if not isinstance(plan, dict) or not isinstance(expected, dict):
        return ["fixture_plan_or_expected_missing"]
    identity = selection_identity(plan)
    if identity is None:
        issues.append("selection_identity_missing")
    elif fixture.get("source_selection_digest") != digest(identity):
        issues.append("source_selection_digest_invalid")
    snapshot = plan.get("rendered_snapshot")
    capability = plan.get("capability")
    tools = plan.get("visible_tools")
    if not isinstance(snapshot, dict) or not isinstance(capability, dict):
        issues.append("plan_binding_missing")
        return issues
    if not isinstance(tools, list):
        issues.append("visible_tools_not_array")
        return issues
    if plan.get("schema_version") != "aoa_organ_exposure_plan_v1":
        issues.append("plan_schema_version_invalid")
    if snapshot.get("schema_version") != "aoa_organ_exposure_snapshot_v1":
        issues.append("snapshot_schema_version_invalid")
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
    plan_unsigned = {
        key: value
        for key, value in plan.items()
        if key not in {"plan_id", "claim_limit"}
    }
    if plan.get("plan_id") != digest(plan_unsigned):
        issues.append("plan_not_content_addressed")
    if plan.get("claim_limit") != PLAN_CLAIM_LIMIT:
        issues.append("plan_claim_limit_invalid")
    if plan.get("execution_authorized") is not False:
        issues.append("execution_authority_not_false")
    if plan.get("activation_authorized") is not False:
        issues.append("activation_authority_not_false")
    owners = capability.get("owners")
    if (
        not isinstance(owners, Mapping)
        or set(owners) != OWNER_FIELDS
        or not all(isinstance(value, str) and value for value in owners.values())
        or capability.get("qualified_capability_id")
        != (
        f"{owners.get('source_owner')}:{capability.get('organ_id')}:{capability.get('capability_id')}"
        )
    ):
        issues.append("capability_not_owner_qualified")
    if capability.get("effect_ceiling") != "read":
        issues.append("capability_effect_ceiling_widened")
    requested_policy_family = plan.get("requested_policy_family")
    capability_effect_ceiling = capability.get("effect_ceiling")
    if not (
        isinstance(requested_policy_family, str)
        and requested_policy_family in POLICY_RANK
        and isinstance(capability_effect_ceiling, str)
        and capability_effect_ceiling in POLICY_RANK
        and POLICY_RANK[requested_policy_family]
        <= POLICY_RANK[capability_effect_ceiling]
    ):
        issues.append("requested_policy_exceeds_capability")
    freshness = capability.get("freshness")
    source_revision = capability.get("source_revision")
    if (
        not isinstance(freshness, Mapping)
        or not isinstance(source_revision, Mapping)
        or snapshot.get("source_digest") != freshness.get("source_digest")
        or freshness.get("source_digest") != source_revision.get("digest")
    ):
        issues.append("snapshot_source_not_capability_bound")
    requested_at = parse_timestamp(plan.get("requested_at"))
    plan_expires_at = parse_timestamp(plan.get("expires_at"))
    snapshot_observed_at = parse_timestamp(snapshot.get("observed_at"))
    snapshot_expires_at = parse_timestamp(snapshot.get("expires_at"))
    freshness_observed_at = (
        parse_timestamp(freshness.get("observed_at"))
        if isinstance(freshness, Mapping)
        else None
    )
    freshness_expires_at = (
        parse_timestamp(freshness.get("expires_at"))
        if isinstance(freshness, Mapping)
        else None
    )
    windows = (
        requested_at,
        plan_expires_at,
        snapshot_observed_at,
        snapshot_expires_at,
        freshness_observed_at,
        freshness_expires_at,
    )
    if (
        any(value is None for value in windows)
        or requested_at != snapshot_observed_at
        or requested_at != freshness_observed_at
        or plan_expires_at != snapshot_expires_at
        or plan_expires_at != freshness_expires_at
        or requested_at >= plan_expires_at
        or not isinstance(freshness.get("ttl_seconds"), int)
        or isinstance(freshness.get("ttl_seconds"), bool)
        or freshness.get("ttl_seconds")
        != int((plan_expires_at - requested_at).total_seconds())
    ):
        issues.append("exposure_window_invalid")
    if plan.get("rollback_route") != capability.get("rollback_route"):
        issues.append("rollback_route_not_capability_bound")
    requested_primitive_ids = plan.get("requested_primitive_ids")
    requested_capability_id = capability.get("capability_id")
    if (
        not isinstance(requested_primitive_ids, list)
        or not all(isinstance(item, str) and item for item in requested_primitive_ids)
        or not isinstance(requested_capability_id, str)
    ):
        issues.append("requested_selection_missing")
        requested_tool_ids: list[str] = []
    else:
        if len(set(requested_primitive_ids)) != len(requested_primitive_ids):
            issues.append("requested_selection_not_unique")
        requested_tool_ids = [
            f"{requested_capability_id}.{primitive_id}"
            for primitive_id in requested_primitive_ids
        ]
    requested_ids_for_check = (
        requested_primitive_ids if isinstance(requested_primitive_ids, list) else []
    )
    actual_tool_ids = [
        tool.get("tool_id") for tool in tools if isinstance(tool, Mapping)
    ]
    if plan.get("plan_state") == "candidate":
        if actual_tool_ids != requested_tool_ids:
            issues.append("visible_tool_selection_mismatch")
    elif tools:
        issues.append("blocked_plan_revealed_tools")
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
        if tool.get("schema_digest") != capability.get("schema_digest"):
            issues.append("visible_tool_schema_not_capability_bound")
        for schema_field in ("input_schema_ref", "output_schema_ref"):
            if not isinstance(tool.get(schema_field), str) or not tool.get(schema_field):
                issues.append("visible_tool_schema_ref_missing")
        if tool.get("capability_id") != requested_capability_id:
            issues.append("visible_tool_capability_mismatch")
        if tool.get("primitive_id") not in requested_ids_for_check:
            issues.append("visible_tool_primitive_not_requested")
    rendered_bytes = snapshot.get("rendered_bytes")
    rendered_tokens = snapshot.get("rendered_tokens")
    if tools:
        if snapshot.get("token_count_posture") != "estimated":
            issues.append("candidate_token_posture_invalid")
        if snapshot.get("token_count_method") != "utf8_bytes_per_4_v1":
            issues.append("candidate_token_method_invalid")
        if (
            not isinstance(rendered_bytes, int)
            or isinstance(rendered_bytes, bool)
            or not isinstance(rendered_tokens, int)
            or isinstance(rendered_tokens, bool)
            or rendered_tokens != max(1, (rendered_bytes + 3) // 4)
        ):
            issues.append("candidate_token_estimate_invalid")
    elif rendered_tokens is not None:
        issues.append("blocked_plan_reported_tokens")
    mode = fixture.get("mode")
    if mode in {
        "default_off",
        "feature_disabled_baseline_ready",
        "feature_enabled_baseline_missing",
    }:
        if plan.get("plan_state") != "blocked":
            issues.append("default_off_plan_not_blocked")
        expected_feature, expected_baseline = {
            "default_off": (False, False),
            "feature_disabled_baseline_ready": (False, True),
            "feature_enabled_baseline_missing": (True, False),
        }[mode]
        if plan.get("feature_enabled") is not expected_feature:
            issues.append("feature_gate_state_mismatch")
        if plan.get("baseline_ready") is not expected_baseline:
            issues.append("baseline_gate_state_mismatch")
        if tools or snapshot.get("rendered_bytes") != 2:
            issues.append("default_off_revealed_schema")
        if snapshot.get("rendered_tokens") is not None:
            issues.append("default_off_reported_tokens")
        expected_refusals = []
        if not expected_feature:
            expected_refusals.append("progressive_exposure_disabled")
        if not expected_baseline:
            expected_refusals.append("baseline_not_ready")
        if plan.get("refusal_reasons") != expected_refusals:
            issues.append("blocked_plan_refusal_reasons_invalid")
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
        if tuple(plan.get("expansion_reasons", ())) != EXPECTED_EXPANSION_REASONS:
            issues.append("candidate_expansion_reasons_invalid")
        if plan.get("refusal_reasons") != []:
            issues.append("candidate_refusal_reasons_present")
    else:
        issues.append("fixture_mode_unknown")
    if plan.get("plan_state") != "candidate" and plan.get("expansion_reasons"):
        issues.append("blocked_plan_expansion_reasons_present")
    if snapshot.get("refusal_reasons") != []:
        issues.append("snapshot_refusal_reasons_present")
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
    if {item.get("mode") for item in fixtures} != EXPECTED_MODES:
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
    identities: list[dict[str, Any] | None] = [
        selection_identity(item.get("plan", {}))
        if isinstance(item.get("plan"), Mapping)
        else None
        for item in fixtures
    ]
    valid_selection = all(
        identity is not None
        and fixture.get("source_selection_digest") == digest(identity)
        for fixture, identity in zip(fixtures, identities)
    )
    comparable_identities = [identity for identity in identities if identity is not None]
    same_selection = valid_selection and len(
        {digest(identity) for identity in comparable_identities}
    ) == 1
    if not same_selection:
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
    default_bytes, default_tokens = snapshot_metrics(default)
    candidate_bytes, candidate_tokens = snapshot_metrics(candidate)
    report = {
        "schema_version": "aoa_progressive_exposure_eval_report_v1",
        "eval_id": "aoa-organ-access-admission-integrity",
        "track": "progressive-tool-exposure",
        "integrity_verdict": (
            "supports_bounded_claim" if not issues else "does_not_support_bounded_claim"
        ),
        "fixture_breakdown": breakdown,
        "matched_selection": {
            "source_selection_digest": (
                digest(comparable_identities[0]) if same_selection else None
            ),
            "same_selection": same_selection,
        },
        "visibility_comparison": {
            "default_off_bytes": default_bytes,
            "candidate_bytes": candidate_bytes,
            "candidate_minus_default_bytes": candidate_bytes - default_bytes,
            "default_off_tokens": default_tokens,
            "candidate_tokens": candidate_tokens,
            "candidate_minus_default_tokens": (
                candidate_tokens - default_tokens
                if candidate_tokens is not None and default_tokens is not None
                else None
            ),
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
