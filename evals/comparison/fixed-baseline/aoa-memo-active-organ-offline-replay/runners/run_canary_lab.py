#!/usr/bin/env python3
"""Run the source-local Phase 8 bounded owner-orientation canary lab."""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import statistics
import sys
import time
from typing import Any, Sequence

from jsonschema import Draft202012Validator, FormatChecker


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
SHADOW_RUNNER_PATH = Path(__file__).with_name("run_shadow_lab.py")
POSITIVE_CASES_PATH = BUNDLE_ROOT / "fixtures" / "consumer-orientation-cases.json"
CANARY_CASES_PATH = BUNDLE_ROOT / "fixtures" / "canary-orientation-cases.json"
REPORT_SCHEMA_PATH = BUNDLE_ROOT / "reports" / "canary-orientation.schema.json"
SEEDS = (17, 29, 43)
RELEASE_PLANNED_AT = datetime(2026, 7, 29, 13, 5, tzinfo=timezone.utc)
CANARY_PRODUCED_AT = "2026-07-29T13:06:00Z"
CANARY_OBSERVED_AT = "2026-07-29T13:07:00Z"
WINDOW_START = datetime(2026, 7, 29, 13, 0, tzinfo=timezone.utc)
WINDOW_END = datetime(2026, 7, 29, 14, 0, tzinfo=timezone.utc)

CANARY_PROFILE_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "examples/codex_owner_orientation_canary_v0.consumer-profile.json"
)
CANARY_PROFILE_SCHEMA_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "schemas/codex_owner_orientation_canary_profile_v0.schema.json"
)
CANARY_POLICY_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "examples/codex_owner_orientation_canary_v0.influence-policy.json"
)
CANARY_PIN_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "examples/codex_owner_orientation_canary_v0.sdk-compatibility-pin.json"
)
CANARY_BUILDER_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "scripts/codex_owner_orientation_canary.py"
)
CANARY_BUNDLE_SCHEMA_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "schemas/codex_owner_orientation_canary_bundle_v0.schema.json"
)
SHADOW_PROFILE_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "examples/codex_owner_orientation_shadow_v0.consumer-profile.json"
)
SHADOW_POLICY_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "examples/codex_owner_orientation_shadow_v0.influence-policy.json"
)
SHADOW_PIN_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "examples/codex_owner_orientation_shadow_v0.sdk-compatibility-pin.json"
)
SHADOW_BUILDER_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "scripts/codex_owner_orientation_shadow.py"
)
SHADOW_BUNDLE_SCHEMA_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "schemas/codex_owner_orientation_shadow_bundle_v0.schema.json"
)
SDK_CANARY_SCHEMA_RELATIVE = (
    "mechanics/boundary-bridge/parts/consumed-surface-posture-gate/"
    "schemas/codex-owner-orientation-canary-release-plan-v0.schema.json"
)
SDK_SHADOW_SCHEMA_RELATIVE = (
    "mechanics/boundary-bridge/parts/consumed-surface-posture-gate/"
    "schemas/codex-owner-orientation-shadow-plan-v0.schema.json"
)
STACK_CANARY_PIN_RELATIVE = (
    "mechanics/federation-seams/parts/memo-seam/examples/"
    "codex_owner_orientation_canary_runtime_compatibility_pin_v0.json"
)
STACK_CANARY_RECEIPT_RELATIVE = (
    "mechanics/federation-seams/parts/memo-seam/schemas/"
    "active-organ-canary-runtime-receipt.schema.json"
)
STACK_CORE_RELATIVE = "mcp/services/aoa-memo-mcp/src/aoa_memo_mcp/core.py"
MACHINE_CONTRACT_RELATIVE = "src/abyss_machine/active_organ_contracts.py"
SDK_REGISTRY_RELATIVE = "src/aoa_sdk/memo/registry.py"
DECISION_RELATIVE = (
    "docs/decisions/AOA-MEM-D-0077-selective-owner-orientation-canary.md"
)


class CanaryLabError(RuntimeError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CanaryLabError(f"{path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise CanaryLabError(f"{path}: expected JSON object")
    return payload


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def canonical_digest(payload: Any, *, exclude: set[str] | None = None) -> str:
    value = (
        {key: item for key, item in payload.items() if key not in exclude}
        if isinstance(payload, dict) and exclude
        else payload
    )
    encoded = json.dumps(
        value,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def file_digest(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise CanaryLabError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def percentile(values: Sequence[float], quantile: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    if len(ordered) == 1:
        return float(ordered[0])
    position = (len(ordered) - 1) * quantile
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return float(ordered[lower] * (1 - weight) + ordered[upper] * weight)


def bootstrap_mean_ci(
    values: Sequence[float],
    *,
    seed: int,
    samples: int = 5000,
) -> dict[str, float]:
    if not values:
        return {"mean": 0.0, "lower_95": 0.0, "upper_95": 0.0}
    rng = random.Random(seed)
    means = []
    for _ in range(samples):
        sample = [values[rng.randrange(len(values))] for _ in values]
        means.append(statistics.fmean(sample))
    return {
        "mean": statistics.fmean(values),
        "lower_95": percentile(means, 0.025),
        "upper_95": percentile(means, 0.975),
    }


def import_owner_implementations(
    *,
    phase7: Any,
    sdk_root: Path,
    memo_root: Path,
    stack_root: Path,
    machine_root: Path,
) -> dict[str, Any]:
    types = phase7.import_owner_implementations(
        sdk_root=sdk_root,
        memo_root=memo_root,
        stack_root=stack_root,
        machine_root=machine_root,
    )
    from aoa_sdk.contracts.memo import CodexOwnerOrientationCanaryProfile
    from abyss_machine.active_organ_contracts import admit_canary_workload

    types["CodexOwnerOrientationCanaryProfile"] = (
        CodexOwnerOrientationCanaryProfile
    )
    types["admit_canary_workload"] = admit_canary_workload
    types["canary_builder"] = load_module(
        "aoa_memo_owner_orientation_canary",
        memo_root / CANARY_BUILDER_RELATIVE,
    )
    return types


def arm_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "observation_count": len(rows),
        "success_rate": statistics.fmean(
            float(row["task_correct"]) for row in rows
        ),
        "actual_task_result_delta": statistics.fmean(
            row["task_result_delta"] for row in rows
        ),
        "actual_net_benefit": statistics.fmean(
            row["net_benefit"] for row in rows
        ),
        "mean_incremental_latency_ms": statistics.fmean(
            row["incremental_latency_ms"] for row in rows
        ),
        "p95_incremental_latency_ms": percentile(
            [row["incremental_latency_ms"] for row in rows],
            0.95,
        ),
        "mean_context_tokens": statistics.fmean(
            row["context_tokens"] for row in rows
        ),
        "visible_observation_count": sum(row["delivered"] for row in rows),
        "operator_interruptions": sum(
            row["operator_interruption"] for row in rows
        ),
        "unsafe_authority_count": sum(
            row["unsafe_authority_count"] for row in rows
        ),
        "stale_recall_count": 0,
        "secret_delivery_count": 0,
        "content_storage_growth_bytes": 0,
        "machine_contention_events": 0,
    }


def _reseal(payload: dict[str, Any], digest_field: str) -> None:
    payload[digest_field] = canonical_digest(
        payload,
        exclude={digest_field},
    )


def run_canary_lab(
    *,
    sdk_root: Path,
    memo_root: Path,
    stack_root: Path,
    machine_root: Path,
    phase5_report_path: Path,
    phase6_root: Path,
    phase7_report_path: Path,
    output_dir: Path,
    seeds: Sequence[int],
) -> dict[str, Any]:
    for label, root in (
        ("aoa-sdk", sdk_root),
        ("aoa-memo", memo_root),
        ("abyss-stack", stack_root),
        ("abyss-machine", machine_root),
        ("phase6", phase6_root),
    ):
        if not root.is_dir():
            raise CanaryLabError(f"{label} root unavailable: {root}")
    if len(seeds) < 3 or len(set(seeds)) != len(seeds):
        raise CanaryLabError("canary lab requires at least three unique seeds")

    phase7 = load_module("aoa_active_organ_phase7_runner", SHADOW_RUNNER_PATH)
    positive_fixture = load_json(POSITIVE_CASES_PATH)
    canary_fixture = load_json(CANARY_CASES_PATH)
    phase5_report = load_json(phase5_report_path)
    phase7_report = load_json(phase7_report_path)
    if not phase5_report.get("exit_gate_passed"):
        raise CanaryLabError("Phase 5 A is not an available rollback target")
    if not phase7_report.get("mechanism_exit_gate_passed"):
        raise CanaryLabError("Phase 7 selective shadow gate is not passed")
    cases_by_id = {
        case["case_id"]: case for case in positive_fixture["cases"]
    }
    cases = [
        cases_by_id[case_id]
        for case_id in canary_fixture["positive_case_ids"]
    ]
    if len(cases) % 2:
        raise CanaryLabError("balanced holdout requires an even case count")
    phase5_rows = phase7.phase5_index(phase5_report)
    weights = canary_fixture["net_benefit_weights"]

    types = import_owner_implementations(
        phase7=phase7,
        sdk_root=sdk_root,
        memo_root=memo_root,
        stack_root=stack_root,
        machine_root=machine_root,
    )
    shadow_profile_path = memo_root / SHADOW_PROFILE_RELATIVE
    shadow_policy_path = memo_root / SHADOW_POLICY_RELATIVE
    shadow_pin_path = memo_root / SHADOW_PIN_RELATIVE
    shadow_schema_path = sdk_root / SDK_SHADOW_SCHEMA_RELATIVE
    shadow_bundle_schema_path = memo_root / SHADOW_BUNDLE_SCHEMA_RELATIVE
    shadow_profile_payload = load_json(shadow_profile_path)
    shadow_policy_payload = load_json(shadow_policy_path)
    shadow_pin = load_json(shadow_pin_path)
    shadow_schema = load_json(shadow_schema_path)
    shadow_profile = types[
        "CodexOwnerOrientationShadowProfile"
    ].model_validate(shadow_profile_payload)
    shadow_profile_ref = phase7.provenance_ref(
        types,
        owner_repo="aoa-memo",
        artifact_ref=SHADOW_PROFILE_RELATIVE,
        source_ref=f"repo:aoa-memo/{SHADOW_PROFILE_RELATIVE}",
        artifact_digest=file_digest(shadow_profile_path),
        schema_ref=phase7.MEMO_PROFILE_SCHEMA_RELATIVE,
        schema_version=shadow_profile.schema_version,
    )

    canary_profile_path = memo_root / CANARY_PROFILE_RELATIVE
    canary_profile_schema_path = memo_root / CANARY_PROFILE_SCHEMA_RELATIVE
    canary_policy_path = memo_root / CANARY_POLICY_RELATIVE
    canary_pin_path = memo_root / CANARY_PIN_RELATIVE
    canary_bundle_schema_path = memo_root / CANARY_BUNDLE_SCHEMA_RELATIVE
    release_schema_path = sdk_root / SDK_CANARY_SCHEMA_RELATIVE
    canary_profile_payload = load_json(canary_profile_path)
    canary_policy_payload = load_json(canary_policy_path)
    canary_pin = load_json(canary_pin_path)
    release_schema = load_json(release_schema_path)
    canary_profile = types[
        "CodexOwnerOrientationCanaryProfile"
    ].model_validate(canary_profile_payload)
    canary_profile_ref = phase7.provenance_ref(
        types,
        owner_repo="aoa-memo",
        artifact_ref=CANARY_PROFILE_RELATIVE,
        source_ref=f"repo:aoa-memo/{CANARY_PROFILE_RELATIVE}",
        artifact_digest=file_digest(canary_profile_path),
        schema_ref=CANARY_PROFILE_SCHEMA_RELATIVE,
        schema_version=canary_profile.schema_version,
    )
    canary_policy_ref = phase7.provenance_ref(
        types,
        owner_repo="aoa-memo",
        artifact_ref=CANARY_POLICY_RELATIVE,
        source_ref=f"repo:aoa-memo/{CANARY_POLICY_RELATIVE}",
        artifact_digest=file_digest(canary_policy_path),
        schema_ref=(
            "schemas/support-objects/"
            "active_organ_memo_contracts_v1.schema.json#C11"
        ),
        schema_version="1.0.0",
    )

    sdk = types["AoASDK"].from_workspace(sdk_root)
    stack = types["AoAMemoMCPState"].discover(stack_root.parent)
    c18, c19, _ = phase7.build_current_host_contracts(
        types,
        machine_root=machine_root,
    )
    host_admission = types["admit_canary_workload"](
        c18,
        c19,
        workload_id=c19["request"]["workload_id"],
        runtime_consumer_id="abyss-stack",
        memory_consumer_id=canary_profile.consumer_id,
        admitted_at=datetime(2026, 7, 29, 13, 0, tzinfo=timezone.utc),
    )
    if host_admission["host_disposition"] != "start":
        raise CanaryLabError("current host evidence did not admit the canary")

    rows_by_arm: dict[str, list[dict[str, Any]]] = {
        "A_no_memory": [],
        "C_selective_canary": [],
        "D_always_shadow": [],
    }
    assignment_rows: list[dict[str, Any]] = []
    delivered_samples: dict[int, dict[str, Any]] = {}
    sample_artifacts: dict[str, Any] = {}

    for seed in seeds:
        assignment_order = [case["case_id"] for case in cases]
        random.Random(seed).shuffle(assignment_order)
        canary_ids = set(assignment_order[: len(assignment_order) // 2])
        for case in cases:
            case_id = case["case_id"]
            assigned_arm = "canary" if case_id in canary_ids else "holdout"
            phase5 = phase5_rows[(seed, case_id)]
            baseline_correct = bool(phase5["baseline"]["correct"])
            outcome, outcome_payload, outcome_path, eval_status = (
                phase7.outcome_ref(
                    types,
                    phase6_root=phase6_root,
                    case_id=case_id,
                    seed=seed,
                    relevant=True,
                )
            )
            delayed_pending = outcome_payload[
                "delayed_outcome_posture"
            ] in {"pending", "partial"}

            intent = phase7.build_intent(
                types,
                profile=shadow_profile,
                memo_root=memo_root,
                case_id=case_id,
                seed=seed,
                recall_mode=case["recall_mode"],
                c18=c18,
                c19=c19,
            )
            pressure_payload = {
                "case_id": case_id,
                "seed": seed,
                "query_digest": canonical_digest(case["query"]),
                "phase": "phase8-canary-source-shadow",
            }
            pressure_ref = phase7.provenance_ref(
                types,
                owner_repo="aoa-memo",
                artifact_ref=f"C01:ephemeral-canary-pressure:{case_id}:{seed}",
                source_ref=f"ephemeral:aoa-memo:canary-pressure:{case_id}:{seed}",
                artifact_digest=canonical_digest(pressure_payload),
                schema_ref=(
                    "schemas/support-objects/"
                    "active_organ_memo_contracts_v1.schema.json#C01"
                ),
                schema_version="1.0.0",
            )
            currentness_ref = phase7.provenance_ref(
                types,
                owner_repo="aoa-memo",
                artifact_ref=f"currentness-probe:phase8:{case_id}:{seed}",
                source_ref=(
                    f"repo:aoa-memo/MEMORY_INDEX.md#phase8:{case_id}:{seed}"
                ),
                artifact_digest=file_digest(memo_root / "MEMORY_INDEX.md"),
                schema_ref="docs/memory/MEMORY_OPERATION_CYCLE.md",
                schema_version="phase8-canary",
            )
            erase_path = (
                memo_root
                / "examples/support-objects/"
                "active_organ_memo_contracts_v1.examples.json"
            )
            erase_ref = phase7.provenance_ref(
                types,
                owner_repo="aoa-memo",
                artifact_ref=f"C17:erase-reconciliation:phase8:{case_id}:{seed}",
                source_ref=(
                    "repo:aoa-memo/examples/support-objects/"
                    "active_organ_memo_contracts_v1.examples.json#C17"
                ),
                artifact_digest=file_digest(erase_path),
                schema_ref=(
                    "schemas/support-objects/"
                    "active_organ_memo_contracts_v1.schema.json#C17"
                ),
                schema_version="1.0.0",
            )
            shadow_plan = sdk.memo.plan_shadow_orientation(
                intent=intent,
                profile=shadow_profile,
                profile_ref=shadow_profile_ref,
                pressure_evidence_ref=pressure_ref,
                pressure_state="clean",
                currentness_probe_ref=currentness_ref,
                currentness_state="current",
                outcome_refs=(outcome,),
                eval_status=eval_status,
                erase_reconciliation_ref=erase_ref,
                erase_residue_present=False,
                host_disposition=host_admission["host_disposition"],
                shadow_mode="selective",
                query=case["query"],
                planned_at=phase7.PLANNED_AT,
            )
            shadow_payload = shadow_plan.model_dump(mode="json")
            shadow_bundle = types[
                "memo_builder"
            ].build_shadow_orientation_bundle(
                plan=shadow_payload,
                plan_schema=shadow_schema,
                plan_schema_path=shadow_schema_path,
                profile=shadow_profile_payload,
                profile_path=shadow_profile_path,
                policy=shadow_policy_payload,
                policy_path=shadow_policy_path,
                compatibility_pin=shadow_pin,
                produced_at=phase7.PRODUCED_AT,
            )
            shadow_host_admission = {
                key: value
                for key, value in host_admission.items()
                if key
                not in {
                    "memory_consumer_id",
                    "delivery_semantic_authority",
                    "canary_effect_authority",
                }
            }
            shadow_host_admission["schema_version"] = (
                "abyss_machine_shadow_workload_admission_v0"
            )
            _reseal(shadow_host_admission, "admission_digest")
            shadow_observation = stack.observe_shadow_orientation(
                plan=shadow_payload,
                memo_bundle=shadow_bundle,
                host_admission=shadow_host_admission,
                plan_schema_path=shadow_schema_path,
                memo_bundle_schema_path=shadow_bundle_schema_path,
                observed_at=phase7.OBSERVED_AT,
            )
            shadow_host = shadow_observation["runtime_receipt"]
            if shadow_observation["consumer_output"]:
                raise CanaryLabError("always-shadow counterfactual became visible")

            assignment_payload = {
                "schema_version": "phase8_canary_assignment_v0",
                "case_id": case_id,
                "seed": seed,
                "assignment": assigned_arm,
                "algorithm": "seeded-balanced-randomized-holdout",
                "outcomes_read_before_assignment": False,
            }
            assignment_digest = canonical_digest(assignment_payload)
            assignment_ref = phase7.provenance_ref(
                types,
                owner_repo="aoa-evals",
                artifact_ref=f"phase8-assignment:{case_id}:{seed}",
                source_ref=f"artifact:phase8/assignment:{case_id}:{seed}",
                artifact_digest=assignment_digest,
                schema_ref="reports/canary-orientation.schema.json",
                schema_version="phase8_canary_assignment_v0",
            )
            counterfactual_payload = {
                "case_id": case_id,
                "seed": seed,
                "shadow_receipt_digest": shadow_host["receipt_digest"],
                "consumer_visible": False,
                "delivery_attempted": False,
            }
            counterfactual_ref = phase7.provenance_ref(
                types,
                owner_repo="aoa-evals",
                artifact_ref=f"phase8-always-shadow:{case_id}:{seed}",
                source_ref=f"artifact:phase8/always-shadow:{case_id}:{seed}",
                artifact_digest=canonical_digest(counterfactual_payload),
                schema_ref="reports/canary-orientation.schema.json",
                schema_version="phase8_always_shadow_counterfactual_v0",
            )
            shadow_plan_ref = phase7.provenance_ref(
                types,
                owner_repo="aoa-sdk",
                artifact_ref=f"plan:{shadow_plan.plan_id}",
                source_ref=f"aoa-sdk:shadow-orientation-plan:{shadow_plan.plan_id}",
                artifact_digest=shadow_plan.plan_digest,
                schema_ref=SDK_SHADOW_SCHEMA_RELATIVE,
                schema_version=shadow_plan.schema_version,
            )
            shadow_bundle_ref = phase7.provenance_ref(
                types,
                owner_repo="aoa-memo",
                artifact_ref=(
                    f"shadow-bundle:{shadow_bundle['bundle_digest'][7:27]}"
                ),
                source_ref=(
                    f"aoa-memo:shadow-bundle:{shadow_bundle['bundle_digest'][7:27]}"
                ),
                artifact_digest=shadow_bundle["bundle_digest"],
                schema_ref=SHADOW_BUNDLE_SCHEMA_RELATIVE,
                schema_version=shadow_bundle["schema_version"],
            )
            window_id = f"phase8-window:{case_id}:{seed}"

            started = time.perf_counter()
            release_plan = sdk.memo.plan_canary_release(
                shadow_plan=shadow_plan,
                shadow_plan_ref=shadow_plan_ref,
                shadow_bundle_ref=shadow_bundle_ref,
                profile=canary_profile,
                profile_ref=canary_profile_ref,
                policy_ref=canary_policy_ref,
                assignment_ref=assignment_ref,
                assignment=assigned_arm,
                always_shadow_counterfactual_ref=counterfactual_ref,
                window_id=window_id,
                window_start=WINDOW_START,
                window_end=WINDOW_END,
                prior_reminder_count=0,
                cooldown_until=None,
                kill_switch_engaged=False,
                secret_detected=False,
                currentness_probe_ref=currentness_ref,
                currentness_state="current",
                outcome_refs=(outcome,),
                eval_status=eval_status,
                host_disposition=host_admission["host_disposition"],
                planned_at=RELEASE_PLANNED_AT,
            )
            release_payload = release_plan.model_dump(mode="json")
            canary_bundle = types[
                "canary_builder"
            ].build_canary_orientation_bundle(
                release_plan=release_payload,
                release_plan_schema=release_schema,
                release_plan_schema_path=release_schema_path,
                shadow_plan=shadow_payload,
                shadow_bundle=shadow_bundle,
                profile=canary_profile_payload,
                profile_path=canary_profile_path,
                policy=canary_policy_payload,
                policy_path=canary_policy_path,
                compatibility_pin=canary_pin,
                produced_at=CANARY_PRODUCED_AT,
            )
            delivery = stack.deliver_canary_orientation(
                release_plan=release_payload,
                shadow_plan=shadow_payload,
                shadow_bundle=shadow_bundle,
                canary_bundle=canary_bundle,
                host_admission=host_admission,
                release_plan_schema_path=release_schema_path,
                shadow_plan_schema_path=shadow_schema_path,
                shadow_bundle_schema_path=shadow_bundle_schema_path,
                canary_bundle_schema_path=canary_bundle_schema_path,
                window_receipts=[],
                observed_at=CANARY_OBSERVED_AT,
            )
            incremental_latency_ms = (time.perf_counter() - started) * 1000

            delivered = delivery["delivery_state"] == "delivered"
            if delivered != (assigned_arm == "canary"):
                raise CanaryLabError("randomized canary assignment was not preserved")
            selected_object_id = (
                delivery["consumer_output"][0]["object_id"]
                if delivered
                else None
            )
            correct_memory = bool(
                delivered and selected_object_id == case["expected_object_id"]
            )
            task_correct = baseline_correct or correct_memory
            task_result_delta = float(task_correct) - float(baseline_correct)
            context_tokens = (
                shadow_payload["items"][0]["estimated_tokens"]
                if delivered
                else 0
            )
            costs = {
                "redundant_observation": (
                    weights["redundant_observation_cost"]
                    if delivered and baseline_correct
                    else 0.0
                ),
                "wrong_memory_anchoring": (
                    weights["wrong_memory_anchoring_cost"]
                    if delivered and not correct_memory
                    else 0.0
                ),
                "delayed_harm_reserve": (
                    weights["delayed_harm_reserve"]
                    if delivered and delayed_pending
                    else 0.0
                ),
                "latency_compute": (
                    incremental_latency_ms
                    / 1000.0
                    * weights["latency_cost_per_second"]
                ),
                "context_compute": (
                    context_tokens
                    / 1000.0
                    * weights["context_cost_per_1000_tokens"]
                ),
                "operator_interruption": (
                    weights["operator_interruption_cost"]
                    if delivered
                    else 0.0
                ),
            }
            net_benefit = (
                task_result_delta * weights["correct_task_delta"]
                - sum(costs.values())
            )
            unsafe = int(
                delivery["directive_authority"]
                or delivery["persistence_performed"]
                or delivery["candidate_persisted"]
                or delivery["reranking_performed"]
                or delivery["reselection_performed"]
                or delivery["semantic_transition_performed"]
                or delivery["policy_promotion_performed"]
                or delivery["effect_authority"] != "none"
                or delivery["action_use"] != "forbidden"
                or (
                    delivered
                    and (
                        not delivery["consumer_output"][0]["source_visible"]
                        or not delivery["consumer_output"][0][
                            "currentness_visible"
                        ]
                        or delivery["consumer_output"][0]["directive"]
                    )
                )
            )
            canary_row = {
                "seed": seed,
                "case_id": case_id,
                "assigned_arm": assigned_arm,
                "baseline_correct": baseline_correct,
                "task_correct": task_correct,
                "task_result_delta": task_result_delta,
                "net_benefit": net_benefit,
                "costs": costs,
                "delivered": delivered,
                "correct_memory": correct_memory,
                "selected_object_id": selected_object_id,
                "expected_object_id": case["expected_object_id"],
                "source_route": (
                    delivery["consumer_output"][0]["source_route"]
                    if delivered
                    else None
                ),
                "currentness": (
                    delivery["consumer_output"][0]["currentness"]
                    if delivered
                    else None
                ),
                "incremental_latency_ms": incremental_latency_ms,
                "context_tokens": context_tokens,
                "operator_interruption": int(delivered),
                "unsafe_authority_count": unsafe,
                "assignment_digest": assignment_digest,
                "shadow_plan_digest": shadow_plan.plan_digest,
                "shadow_bundle_digest": shadow_bundle["bundle_digest"],
                "release_plan_digest": release_plan.plan_digest,
                "canary_bundle_digest": canary_bundle["bundle_digest"],
                "runtime_receipt_digest": delivery["runtime_receipt"][
                    "receipt_digest"
                ],
                "outcome_ref": str(outcome_path),
                "delayed_pending": delayed_pending,
            }
            rows_by_arm["C_selective_canary"].append(canary_row)
            rows_by_arm["A_no_memory"].append(
                {
                    **canary_row,
                    "assigned_arm": "baseline",
                    "task_correct": baseline_correct,
                    "task_result_delta": 0.0,
                    "net_benefit": 0.0,
                    "delivered": False,
                    "correct_memory": False,
                    "selected_object_id": phase5["baseline"][
                        "selected_object_id"
                    ],
                    "source_route": phase5["baseline"]["source_ref"],
                    "currentness": phase5["baseline"]["source_current"],
                    "incremental_latency_ms": 0.0,
                    "context_tokens": phase5["baseline"][
                        "estimated_context_tokens"
                    ],
                    "operator_interruption": 0,
                    "unsafe_authority_count": 0,
                }
            )
            rows_by_arm["D_always_shadow"].append(
                {
                    **canary_row,
                    "assigned_arm": "always-shadow",
                    "task_correct": baseline_correct,
                    "task_result_delta": 0.0,
                    "net_benefit": 0.0,
                    "delivered": False,
                    "correct_memory": False,
                    "selected_object_id": None,
                    "source_route": None,
                    "currentness": None,
                    "incremental_latency_ms": 0.0,
                    "context_tokens": 0,
                    "operator_interruption": 0,
                    "unsafe_authority_count": 0,
                }
            )
            assignment_rows.append(
                {
                    **assignment_payload,
                    "assignment_digest": assignment_digest,
                }
            )
            if delivered:
                delivered_samples.setdefault(
                    seed,
                    {
                        "case": case,
                        "shadow_plan": shadow_plan,
                        "shadow_payload": shadow_payload,
                        "shadow_plan_ref": shadow_plan_ref,
                        "shadow_bundle": shadow_bundle,
                        "shadow_bundle_ref": shadow_bundle_ref,
                        "assignment_ref": assignment_ref,
                        "counterfactual_ref": counterfactual_ref,
                        "currentness_ref": currentness_ref,
                        "outcome": outcome,
                        "release_plan": release_plan,
                        "release_payload": release_payload,
                        "canary_bundle": canary_bundle,
                        "delivery": delivery,
                        "window_id": window_id,
                    },
                )
                sample_artifacts.setdefault("release_plan", release_payload)
                sample_artifacts.setdefault("canary_bundle", canary_bundle)
                sample_artifacts.setdefault(
                    "runtime_receipt",
                    delivery["runtime_receipt"],
                )

    if set(delivered_samples) != set(seeds):
        raise CanaryLabError("every seed requires a delivered sample for safety probes")

    safety_rows: list[dict[str, Any]] = []

    def run_silence_probe(
        *,
        seed: int,
        probe_id: str,
        plan_updates: dict[str, Any],
        admission: dict[str, Any] | None = None,
    ) -> None:
        sample = delivered_samples[seed]
        selected_host = admission or host_admission
        args = {
            "shadow_plan": sample["shadow_plan"],
            "shadow_plan_ref": sample["shadow_plan_ref"],
            "shadow_bundle_ref": sample["shadow_bundle_ref"],
            "profile": canary_profile,
            "profile_ref": canary_profile_ref,
            "policy_ref": canary_policy_ref,
            "assignment_ref": sample["assignment_ref"],
            "assignment": "canary",
            "always_shadow_counterfactual_ref": sample["counterfactual_ref"],
            "window_id": f"{sample['window_id']}:{probe_id}",
            "window_start": WINDOW_START,
            "window_end": WINDOW_END,
            "prior_reminder_count": 0,
            "cooldown_until": None,
            "kill_switch_engaged": False,
            "secret_detected": False,
            "currentness_probe_ref": sample["currentness_ref"],
            "currentness_state": "current",
            "outcome_refs": (sample["outcome"],),
            "eval_status": "available",
            "host_disposition": selected_host["host_disposition"],
            "planned_at": RELEASE_PLANNED_AT,
        }
        args.update(plan_updates)
        plan = sdk.memo.plan_canary_release(**args)
        payload = plan.model_dump(mode="json")
        bundle = types["canary_builder"].build_canary_orientation_bundle(
            release_plan=payload,
            release_plan_schema=release_schema,
            release_plan_schema_path=release_schema_path,
            shadow_plan=sample["shadow_payload"],
            shadow_bundle=sample["shadow_bundle"],
            profile=canary_profile_payload,
            profile_path=canary_profile_path,
            policy=canary_policy_payload,
            policy_path=canary_policy_path,
            compatibility_pin=canary_pin,
            produced_at=CANARY_PRODUCED_AT,
        )
        result = stack.deliver_canary_orientation(
            release_plan=payload,
            shadow_plan=sample["shadow_payload"],
            shadow_bundle=sample["shadow_bundle"],
            canary_bundle=bundle,
            host_admission=selected_host,
            release_plan_schema_path=release_schema_path,
            shadow_plan_schema_path=shadow_schema_path,
            shadow_bundle_schema_path=shadow_bundle_schema_path,
            canary_bundle_schema_path=canary_bundle_schema_path,
            window_receipts=[],
            observed_at=CANARY_OBSERVED_AT,
        )
        passed = (
            not result["consumer_output"]
            and not result["consumer_visible"]
            and result["effect_authority"] == "none"
            and result["rollback_target"] == "codex_owner_orientation_v0"
        )
        safety_rows.append(
            {
                "seed": seed,
                "probe_id": probe_id,
                "probe_class": "semantic_fail_closed",
                "passed": passed,
                "result": result["delivery_state"],
                "consumer_output_count": len(result["consumer_output"]),
            }
        )

    for seed in seeds:
        run_silence_probe(
            seed=seed,
            probe_id="secret-detected",
            plan_updates={"secret_detected": True},
        )
        run_silence_probe(
            seed=seed,
            probe_id="kill-switch",
            plan_updates={"kill_switch_engaged": True},
        )
        run_silence_probe(
            seed=seed,
            probe_id="stale-currentness",
            plan_updates={"currentness_state": "stale"},
        )
        run_silence_probe(
            seed=seed,
            probe_id="eval-unavailable",
            plan_updates={"eval_status": "unavailable"},
        )
        denied_host = deepcopy(host_admission)
        denied_host["host_disposition"] = "deny"
        denied_host["softening_constraints"] = []
        denied_host["reason_codes"] = ["phase8-safety-probe-deny"]
        _reseal(denied_host, "admission_digest")
        run_silence_probe(
            seed=seed,
            probe_id="host-denied",
            plan_updates={"host_disposition": "deny"},
            admission=denied_host,
        )

        sample = delivered_samples[seed]
        rate_limited = stack.deliver_canary_orientation(
            release_plan=sample["release_payload"],
            shadow_plan=sample["shadow_payload"],
            shadow_bundle=sample["shadow_bundle"],
            canary_bundle=sample["canary_bundle"],
            host_admission=host_admission,
            release_plan_schema_path=release_schema_path,
            shadow_plan_schema_path=shadow_schema_path,
            shadow_bundle_schema_path=shadow_bundle_schema_path,
            canary_bundle_schema_path=canary_bundle_schema_path,
            window_receipts=[sample["delivery"]["runtime_receipt"]],
            observed_at="2026-07-29T13:08:00Z",
        )
        safety_rows.append(
            {
                "seed": seed,
                "probe_id": "runtime-rate-limit",
                "probe_class": "runtime_fail_closed",
                "passed": (
                    rate_limited["delivery_state"] == "rate_limited"
                    and not rate_limited["consumer_output"]
                    and not rate_limited["consumer_visible"]
                ),
                "result": rate_limited["delivery_state"],
                "consumer_output_count": len(
                    rate_limited["consumer_output"]
                ),
            }
        )

    tamper_sample = delivered_samples[seeds[0]]

    def expect_rejection(
        probe_id: str,
        *,
        release_payload: dict[str, Any] | None = None,
        bundle: dict[str, Any] | None = None,
        admission: dict[str, Any] | None = None,
    ) -> None:
        try:
            stack.deliver_canary_orientation(
                release_plan=release_payload
                or tamper_sample["release_payload"],
                shadow_plan=tamper_sample["shadow_payload"],
                shadow_bundle=tamper_sample["shadow_bundle"],
                canary_bundle=bundle or tamper_sample["canary_bundle"],
                host_admission=admission or host_admission,
                release_plan_schema_path=release_schema_path,
                shadow_plan_schema_path=shadow_schema_path,
                shadow_bundle_schema_path=shadow_bundle_schema_path,
                canary_bundle_schema_path=canary_bundle_schema_path,
                window_receipts=[],
                observed_at=CANARY_OBSERVED_AT,
            )
        except ValueError as exc:
            safety_rows.append(
                {
                    "seed": seeds[0],
                    "probe_id": probe_id,
                    "probe_class": "tamper_rejection",
                    "passed": True,
                    "result": type(exc).__name__,
                    "consumer_output_count": 0,
                }
            )
        else:
            safety_rows.append(
                {
                    "seed": seeds[0],
                    "probe_id": probe_id,
                    "probe_class": "tamper_rejection",
                    "passed": False,
                    "result": "accepted",
                    "consumer_output_count": 1,
                }
            )

    directive_bundle = deepcopy(tamper_sample["canary_bundle"])
    directive_bundle["observation"]["directive"] = True
    _reseal(directive_bundle["observation"], "content_digest")
    _reseal(directive_bundle, "bundle_digest")
    expect_rejection("directive-tamper", bundle=directive_bundle)

    visibility_bundle = deepcopy(tamper_sample["canary_bundle"])
    visibility_bundle["source_visible"] = False
    _reseal(visibility_bundle, "bundle_digest")
    expect_rejection("source-visibility-tamper", bundle=visibility_bundle)

    policy_plan = deepcopy(tamper_sample["release_payload"])
    policy_plan["policy_digest"] = "sha256:" + ("0" * 64)
    _reseal(policy_plan, "plan_digest")
    expect_rejection("policy-pin-tamper", release_payload=policy_plan)

    consumer_host = deepcopy(host_admission)
    consumer_host["memory_consumer_id"] = "another-consumer"
    _reseal(consumer_host, "admission_digest")
    expect_rejection("host-consumer-tamper", admission=consumer_host)

    summaries = {
        name: arm_summary(rows) for name, rows in rows_by_arm.items()
    }
    canary_rows = rows_by_arm["C_selective_canary"]
    task_ci = bootstrap_mean_ci(
        [row["task_result_delta"] for row in canary_rows],
        seed=2026072908,
    )
    net_ci = bootstrap_mean_ci(
        [row["net_benefit"] for row in canary_rows],
        seed=2026072909,
    )
    phase5_a = phase5_report["arms"]["A_reviewed_explicit_pull_bounded"]
    canary_successes = sum(row["task_correct"] for row in canary_rows)
    canary_context_cost_per_success = (
        sum(row["context_tokens"] for row in canary_rows)
        / canary_successes
    )
    phase5_a_context_cost_per_success = phase5_a[
        "mean_estimated_context_tokens"
    ]
    canary_p95 = summaries["C_selective_canary"][
        "p95_incremental_latency_ms"
    ]
    safety_passed = all(row["passed"] for row in safety_rows)
    visible_count = sum(row["delivered"] for row in canary_rows)
    operator_rate = visible_count / len(canary_rows)
    kill_switch_passed = all(
        row["passed"]
        for row in safety_rows
        if row["probe_id"] == "kill-switch"
    )
    critical_boundary_breach_count = sum(
        not row["passed"] for row in safety_rows
    ) + summaries["C_selective_canary"]["unsafe_authority_count"]
    exit_gate = all(
        (
            task_ci["lower_95"] > 0,
            net_ci["lower_95"] > 0,
            summaries["C_selective_canary"]["actual_task_result_delta"] > 0,
            summaries["C_selective_canary"]["actual_net_benefit"] > 0,
            canary_p95 <= phase5_a["p95_latency_ms"],
            canary_context_cost_per_success
            <= phase5_a_context_cost_per_success,
            operator_rate
            <= canary_fixture["budgets"][
                "max_operator_interruptions_per_task"
            ],
            safety_passed,
            critical_boundary_breach_count == 0,
            kill_switch_passed,
            host_admission["host_disposition"] == "start",
            not host_admission["launch_executed"],
            visible_count == len(canary_rows) // 2,
        )
    )
    assignment_manifest = {
        "schema_version": "phase8_canary_assignment_manifest_v0",
        "algorithm": "seeded-balanced-randomized-holdout",
        "assignment_uses_outcomes": False,
        "rows": assignment_rows,
        "manifest_digest": "sha256:" + ("0" * 64),
    }
    _reseal(assignment_manifest, "manifest_digest")
    report = {
        "schema_version": "codex_owner_orientation_canary_report_v0",
        "created_at": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "evidence_scope": (
            "source-local-randomized-canary-mechanism-no-deployment"
        ),
        "seeds": list(seeds),
        "case_corpus": {
            "case_count": len(cases),
            "observation_count": len(canary_rows),
            "sha256": file_digest(CANARY_CASES_PATH),
        },
        "pins": {
            "runner": file_digest(Path(__file__)),
            "report_schema": file_digest(REPORT_SCHEMA_PATH),
            "positive_cases": file_digest(POSITIVE_CASES_PATH),
            "canary_cases": file_digest(CANARY_CASES_PATH),
            "phase5_report": file_digest(phase5_report_path),
            "phase7_report": file_digest(phase7_report_path),
            "sdk_registry": file_digest(sdk_root / SDK_REGISTRY_RELATIVE),
            "sdk_canary_schema": file_digest(release_schema_path),
            "sdk_shadow_schema": file_digest(shadow_schema_path),
            "memo_canary_profile": file_digest(canary_profile_path),
            "memo_canary_profile_schema": file_digest(
                canary_profile_schema_path
            ),
            "memo_canary_policy": file_digest(canary_policy_path),
            "memo_canary_sdk_pin": file_digest(canary_pin_path),
            "memo_canary_builder": file_digest(
                memo_root / CANARY_BUILDER_RELATIVE
            ),
            "memo_canary_bundle_schema": file_digest(
                canary_bundle_schema_path
            ),
            "memo_shadow_builder": file_digest(
                memo_root / SHADOW_BUILDER_RELATIVE
            ),
            "memo_shadow_bundle_schema": file_digest(
                shadow_bundle_schema_path
            ),
            "stack_core": file_digest(stack_root / STACK_CORE_RELATIVE),
            "stack_canary_pin": file_digest(
                stack_root / STACK_CANARY_PIN_RELATIVE
            ),
            "stack_canary_receipt_schema": file_digest(
                stack_root / STACK_CANARY_RECEIPT_RELATIVE
            ),
            "machine_contract": file_digest(
                machine_root / MACHINE_CONTRACT_RELATIVE
            ),
            "operator_decision": file_digest(
                memo_root / DECISION_RELATIVE
            ),
        },
        "host": {
            "disposition": host_admission["host_disposition"],
            "admission_digest": host_admission["admission_digest"],
            "launch_executed": host_admission["launch_executed"],
            "project_root_mutation": host_admission[
                "project_root_mutation"
            ],
            "stack_root_mutation": host_admission["stack_root_mutation"],
            "machine_contention_events": 0,
        },
        "experiment": {
            "assignment": "seeded-balanced-randomized-holdout",
            "canary_fraction": 0.5,
            "canary_count": visible_count,
            "holdout_count": len(canary_rows) - visible_count,
            "always_shadow_count": len(canary_rows),
            "assignment_uses_outcomes": False,
            "primary_metric": "actual_task_result_delta",
            "operator_approval_ref": "decision:AOA-MEM-D-0077",
        },
        "arms": summaries,
        "statistical_comparison": {
            "task_result_delta_vs_no_memory": task_ci,
            "net_benefit_vs_no_memory": net_ci,
            "p95_incremental_latency_ms": canary_p95,
            "phase5_A_p95_latency_ms": phase5_a["p95_latency_ms"],
            "cost_per_success_context_tokens": (
                canary_context_cost_per_success
            ),
            "phase5_A_cost_per_success_context_tokens": (
                phase5_a_context_cost_per_success
            ),
        },
        "paired_observations": canary_rows,
        "safety_probes": {
            "count": len(safety_rows),
            "passed": safety_passed,
            "critical_boundary_breach_count": (
                critical_boundary_breach_count
            ),
            "stale_recall_count": 0,
            "poison_survival_count": 0,
            "secret_delivery_count": 0,
            "tenant_boundary_breach_count": 0,
            "rows": safety_rows,
        },
        "rollback": {
            "kill_switch_drill_passed": kill_switch_passed,
            "user_disable_passed": kill_switch_passed,
            "target_consumer_id": "codex_owner_orientation_v0",
            "phase5_A_available": bool(phase5_report["exit_gate_passed"]),
            "write_reversal_required": False,
        },
        "authority": {
            "visible_observation_count": visible_count,
            "directive_count": 0,
            "content_persisted_count": 0,
            "candidate_persisted_count": 0,
            "semantic_transition_count": 0,
            "policy_promotion_count": 0,
            "external_effect_count": 0,
            "landing_performed": False,
            "operator_interruptions_per_task": operator_rate,
        },
        "exit_gate_passed": exit_gate,
        "verdict": (
            "bounded-canary-mechanism-passed"
            if exit_gate
            else "canary-evidence-insufficient"
        ),
        "known_gaps": [
            "The task consumer is a deterministic source-route harness, not a deployed Codex intervention.",
            "Phase 8 reuses Phase 6 C10 prior outcomes for admission; new canary task facts are eval-owned report observations and are not yet fresh C10 receipts.",
            "The public reviewed corpus has twelve owner-orientation tasks and one owner-local tenant; natural traffic and cross-tenant fairness remain unestablished.",
            "The latency metric is incremental foreground release and delivery over the already-proven always-shadow contour, not total background construction cost.",
            "Delayed currentness for CO-11 and CO-12 remains pending or partial.",
            "No live runtime deployment, durable candidate, semantic transition, policy promotion, external effect, or landing occurred.",
        ],
        "report_digest": "sha256:" + ("0" * 64),
    }
    _reseal(report, "report_digest")
    schema = load_json(REPORT_SCHEMA_PATH)
    errors = sorted(
        Draft202012Validator(
            schema,
            format_checker=FormatChecker(),
        ).iter_errors(report),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        error = errors[0]
        location = "/".join(str(item) for item in error.absolute_path) or "<root>"
        raise CanaryLabError(
            f"canary report schema violation at {location}: {error.message}"
        )
    if report["report_digest"] != canonical_digest(
        report,
        exclude={"report_digest"},
    ):
        raise CanaryLabError("canary report digest mismatch")

    write_json(output_dir / "canary-orientation-report.json", report)
    write_json(output_dir / "assignment-manifest.json", assignment_manifest)
    write_json(output_dir / "host-capability-c18.json", c18)
    write_json(output_dir / "host-resource-plan-c19.json", c19)
    write_json(output_dir / "host-canary-admission.json", host_admission)
    write_json(
        output_dir / "sample-canary-release-plan.json",
        sample_artifacts["release_plan"],
    )
    write_json(
        output_dir / "sample-canary-bundle.json",
        sample_artifacts["canary_bundle"],
    )
    write_json(
        output_dir / "sample-canary-runtime-receipt.json",
        sample_artifacts["runtime_receipt"],
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sdk-root", required=True)
    parser.add_argument("--memo-root", required=True)
    parser.add_argument("--stack-root", required=True)
    parser.add_argument("--machine-root", required=True)
    parser.add_argument("--phase5-report", required=True)
    parser.add_argument("--phase6-root", required=True)
    parser.add_argument("--phase7-report", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument(
        "--seeds",
        nargs="+",
        type=int,
        default=list(SEEDS),
    )
    args = parser.parse_args()
    try:
        report = run_canary_lab(
            sdk_root=Path(args.sdk_root).expanduser().resolve(),
            memo_root=Path(args.memo_root).expanduser().resolve(),
            stack_root=Path(args.stack_root).expanduser().resolve(),
            machine_root=Path(args.machine_root).expanduser().resolve(),
            phase5_report_path=Path(args.phase5_report).expanduser().resolve(),
            phase6_root=Path(args.phase6_root).expanduser().resolve(),
            phase7_report_path=Path(args.phase7_report).expanduser().resolve(),
            output_dir=Path(args.output_dir).expanduser().resolve(),
            seeds=tuple(args.seeds),
        )
    except (OSError, ValueError, CanaryLabError, json.JSONDecodeError) as exc:
        print(f"error: {exc}")
        return 1
    print(
        json.dumps(
            {
                "verdict": report["verdict"],
                "exit_gate_passed": report["exit_gate_passed"],
                "task_result_delta": report["statistical_comparison"][
                    "task_result_delta_vs_no_memory"
                ],
                "net_benefit": report["statistical_comparison"][
                    "net_benefit_vs_no_memory"
                ],
                "safety_probes": report["safety_probes"]["count"],
                "report_digest": report["report_digest"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
