#!/usr/bin/env python3
"""Run the source-local Phase 7 consumer-invisible shadow-organ lab."""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import random
import statistics
import sys
import time
from typing import Any, Sequence

from jsonschema import Draft202012Validator, FormatChecker


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
POSITIVE_CASES_PATH = BUNDLE_ROOT / "fixtures" / "consumer-orientation-cases.json"
SHADOW_CASES_PATH = BUNDLE_ROOT / "fixtures" / "shadow-orientation-cases.json"
REPORT_SCHEMA_PATH = BUNDLE_ROOT / "reports" / "shadow-orientation.schema.json"
SEEDS = (17, 29, 43)
PLANNED_AT = datetime(2026, 7, 29, 13, 2, tzinfo=timezone.utc)
PRODUCED_AT = "2026-07-29T13:03:00Z"
OBSERVED_AT = "2026-07-29T13:04:00Z"
EXPIRES_AT = datetime(2026, 7, 29, 14, 30, tzinfo=timezone.utc)
PROFILE_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "examples/codex_owner_orientation_shadow_v0.consumer-profile.json"
)
POLICY_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "examples/codex_owner_orientation_shadow_v0.influence-policy.json"
)
MEMO_PIN_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "examples/codex_owner_orientation_shadow_v0.sdk-compatibility-pin.json"
)
MEMO_BUILDER_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "scripts/codex_owner_orientation_shadow.py"
)
MEMO_BUNDLE_SCHEMA_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "schemas/codex_owner_orientation_shadow_bundle_v0.schema.json"
)
SDK_PLAN_SCHEMA_RELATIVE = (
    "mechanics/boundary-bridge/parts/consumed-surface-posture-gate/"
    "schemas/codex-owner-orientation-shadow-plan-v0.schema.json"
)
HOST_EXAMPLES_RELATIVE = (
    "mechanics/host-facts/examples/active_organ_host_contracts_v1.examples.json"
)
SDK_REGISTRY_RELATIVE = "src/aoa_sdk/memo/registry.py"
MEMO_PROFILE_SCHEMA_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "schemas/codex_owner_orientation_shadow_profile_v0.schema.json"
)
STACK_CORE_RELATIVE = "mcp/services/aoa-memo-mcp/src/aoa_memo_mcp/core.py"
STACK_PIN_RELATIVE = (
    "mechanics/federation-seams/parts/memo-seam/examples/"
    "codex_owner_orientation_shadow_runtime_compatibility_pin_v0.json"
)
STACK_RECEIPT_SCHEMA_RELATIVE = (
    "mechanics/federation-seams/parts/memo-seam/schemas/"
    "active-organ-shadow-runtime-receipt.schema.json"
)
MACHINE_CONTRACT_RELATIVE = "src/abyss_machine/active_organ_contracts.py"
PHASE6_FREEZE_RELATIVE = "eval-unavailable-freeze-probe.json"
PHASE6_RECEIPT_TEMPLATE = "receipts/{seed}-{case_id}-B.json"


class ShadowLabError(RuntimeError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ShadowLabError(f"{path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ShadowLabError(f"{path}: expected JSON object")
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
        raise ShadowLabError(f"cannot load module: {path}")
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


def provenance_ref(
    types: dict[str, Any],
    *,
    owner_repo: str,
    artifact_ref: str,
    source_ref: str,
    artifact_digest: str,
    schema_ref: str,
    schema_version: str,
):
    return types["ProvenanceRef"](
        owner_repo=owner_repo,
        artifact_ref=artifact_ref,
        source_ref=source_ref,
        artifact_digest=artifact_digest,
        schema_ref=schema_ref,
        schema_version=schema_version,
    )


def import_owner_implementations(
    *,
    sdk_root: Path,
    memo_root: Path,
    stack_root: Path,
    machine_root: Path,
) -> dict[str, Any]:
    for path in (
        sdk_root / "src",
        stack_root / "mcp/services/aoa-memo-mcp/src",
        machine_root / "src",
    ):
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))
    os.environ["AOA_SDK_REPO_PATH_AOA_MEMO"] = str(memo_root)
    os.environ["AOA_ABYSS_STACK_ROOT"] = str(stack_root)

    from aoa_sdk import AoASDK
    from aoa_sdk.contracts.control_plane import ProvenanceRef
    from aoa_sdk.contracts.memo import (
        ActiveOrganAnchorFreshness,
        ActiveOrganPolicyPin,
        CodexOwnerOrientationShadowProfile,
        RecallIntent,
    )
    from aoa_memo_mcp.core import AoAMemoMCPState
    from abyss_machine.active_organ_contracts import (
        admit_shadow_workload,
        build_host_capability_snapshot_reference,
        build_host_resource_storage_plan_reference,
    )

    return {
        "AoASDK": AoASDK,
        "ProvenanceRef": ProvenanceRef,
        "ActiveOrganAnchorFreshness": ActiveOrganAnchorFreshness,
        "ActiveOrganPolicyPin": ActiveOrganPolicyPin,
        "CodexOwnerOrientationShadowProfile": (
            CodexOwnerOrientationShadowProfile
        ),
        "RecallIntent": RecallIntent,
        "AoAMemoMCPState": AoAMemoMCPState,
        "admit_shadow_workload": admit_shadow_workload,
        "build_c18": build_host_capability_snapshot_reference,
        "build_c19": build_host_resource_storage_plan_reference,
        "memo_builder": load_module(
            "aoa_memo_owner_orientation_shadow",
            memo_root / MEMO_BUILDER_RELATIVE,
        ),
    }


def _seal_host(payload: dict[str, Any]) -> None:
    payload["content_digest"] = canonical_digest(
        payload,
        exclude={"content_digest"},
    )


def build_current_host_contracts(
    types: dict[str, Any],
    *,
    machine_root: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    suite = load_json(machine_root / HOST_EXAMPLES_RELATIVE)
    c18 = deepcopy(suite["valid_cases"][0]["payload"])
    c19 = deepcopy(suite["valid_cases"][1]["payload"])

    c18.update(
        {
            "reference_id": "host-capability:phase7-shadow",
            "idempotency_key": "host-capability:phase7-shadow:v1",
            "snapshot_generation": "host-generation:2026-07-29T12:50:00Z",
            "captured_at": "2026-07-29T12:50:00Z",
            "produced_at": "2026-07-29T12:50:01Z",
            "expires_at": "2026-07-29T15:00:00Z",
        }
    )
    for index, capability in enumerate(c18["capability_refs"]):
        capability["observed_at"] = (
            f"2026-07-29T12:49:{50 + index:02d}Z"
        )
    _seal_host(c18)
    c18 = types["build_c18"](**c18)

    c18_ref = {
        "owner_repo": "abyss-machine",
        "artifact_ref": "C18:host-capability:phase7-shadow",
        "artifact_version": "1.0.0",
        "artifact_digest": c18["content_digest"],
    }
    c19.update(
        {
            "reference_id": "host-plan:phase7-shadow",
            "idempotency_key": "host-plan:phase7-shadow:v1",
            "capability_snapshot_ref": c18_ref,
            "produced_at": "2026-07-29T12:51:00Z",
            "expires_at": "2026-07-29T15:00:00Z",
        }
    )
    c19["request"].update(
        {
            "request_owner": "aoa-evals",
            "workload_id": "active-organ-lab:phase7-shadow",
        }
    )
    core_refs = [
        c19["capability_snapshot_ref"],
        c19["resource_plan_ref"],
        c19["rollback_ref"],
    ]
    c19["source_refs"] = core_refs
    _seal_host(c19)
    c19 = types["build_c19"](**c19)
    admission = types["admit_shadow_workload"](
        c18,
        c19,
        workload_id="active-organ-lab:phase7-shadow",
        consumer_id="abyss-stack",
        admitted_at=datetime(2026, 7, 29, 13, 0, tzinfo=timezone.utc),
    )
    return c18, c19, admission


def build_intent(
    types: dict[str, Any],
    *,
    profile: Any,
    memo_root: Path,
    case_id: str,
    seed: int,
    recall_mode: str,
    c18: dict[str, Any],
    c19: dict[str, Any],
):
    anchor_path = memo_root / "MEMORY_INDEX.md"
    anchor_ref = provenance_ref(
        types,
        owner_repo="aoa-memo",
        artifact_ref="MEMORY_INDEX.md",
        source_ref="repo:aoa-memo/MEMORY_INDEX.md",
        artifact_digest=file_digest(anchor_path),
        schema_ref="docs/memory/MEMORY_MODEL.md",
        schema_version="active-organ-phase7-shadow",
    )
    c18_ref = provenance_ref(
        types,
        owner_repo="abyss-machine",
        artifact_ref="C18:host-capability:phase7-shadow",
        source_ref="repo:abyss-machine/C18:host-capability:phase7-shadow",
        artifact_digest=c18["content_digest"],
        schema_ref=(
            "schemas/active-organ-host-capability-snapshot-reference.schema.json"
        ),
        schema_version="1.0.0",
    )
    c19_ref = provenance_ref(
        types,
        owner_repo="abyss-machine",
        artifact_ref="C19:host-plan:phase7-shadow",
        source_ref="repo:abyss-machine/C19:host-plan:phase7-shadow",
        artifact_digest=c19["content_digest"],
        schema_ref=(
            "schemas/active-organ-host-resource-storage-plan-reference.schema.json"
        ),
        schema_version="1.0.0",
    )
    return types["RecallIntent"](
        intent_id=f"intent:shadow-lab:{case_id}:{seed}",
        idempotency_key=f"intent:shadow-lab:{case_id}:{seed}",
        trigger_id=profile.trigger.trigger_id,
        anchor_id=f"repo:aoa-memo:{case_id}:{seed}",
        anchor_ref=anchor_ref,
        anchor_freshness=types["ActiveOrganAnchorFreshness"](
            observed_at=PLANNED_AT,
            valid_at=PLANNED_AT,
            expires_at=EXPIRES_AT,
        ),
        consumer_id=profile.consumer_id,
        tenant_id="owner-local",
        model_prompt_provider_pin=profile.model_prompt_provider_pin,
        data_class="D0",
        risk_class="R4",
        mode="shadow_observation",
        recall_mode=recall_mode,
        requested_scopes=("workspace",),
        policy_pin=types["ActiveOrganPolicyPin"](
            policy_id=profile.influence_policy.policy_id,
            policy_version=profile.influence_policy.policy_version,
            decision_ref="decision:aoa-memo-active-organ-phase1-v1",
            policy_digest=profile.influence_policy.sha256,
        ),
        source_refs=(c18_ref, c19_ref),
        requested_at=PLANNED_AT,
        expires_at=EXPIRES_AT,
    )


def outcome_ref(
    types: dict[str, Any],
    *,
    phase6_root: Path,
    case_id: str,
    seed: int,
    relevant: bool,
) -> tuple[Any, dict[str, Any], Path, str]:
    relative = (
        PHASE6_RECEIPT_TEMPLATE.format(seed=seed, case_id=case_id)
        if relevant
        else PHASE6_FREEZE_RELATIVE
    )
    path = phase6_root / relative
    payload = load_json(path)
    if payload.get("contract_id") != "C10":
        raise ShadowLabError(f"not a C10 outcome receipt: {path}")
    status = payload["evaluation_posture"]["eval_plane_status"]
    ref = provenance_ref(
        types,
        owner_repo="aoa-stats",
        artifact_ref=f"C10:{relative}",
        source_ref=f"artifact:phase6/{relative}",
        artifact_digest=file_digest(path),
        schema_ref="stats/measurement-contract/outcome-receipt.schema.json",
        schema_version=payload["schema_version"],
    )
    return ref, payload, path, status


def phase5_index(report: dict[str, Any]) -> dict[tuple[int, str], dict[str, Any]]:
    return {
        (row["seed"], row["case_id"]): row
        for row in report["paired_observations"]
    }


def observation_costs(
    *,
    weights: dict[str, float],
    relevant: bool,
    intervened: bool,
    correct_memory: bool,
    baseline_correct: bool,
    supported: bool,
    delayed_pending: bool,
    latency_ms: float,
    tokens: int,
) -> tuple[dict[str, float], dict[str, float], float]:
    benefits = {
        "counterfactual_task_delta": (
            weights["correct_counterfactual_delta"]
            if relevant and correct_memory and not baseline_correct
            else 0.0
        ),
        "supported_outcome_bonus": (
            weights["supported_outcome_bonus"]
            if relevant and correct_memory and supported
            else 0.0
        ),
    }
    costs = {
        "redundant_intervention": (
            weights["redundant_intervention_cost"]
            if relevant and intervened and baseline_correct
            else 0.0
        ),
        "irrelevant_distraction": (
            weights["irrelevant_distraction_cost"]
            if not relevant and intervened
            else 0.0
        ),
        "irrelevant_unnecessary_work": (
            weights["irrelevant_unnecessary_work_cost"]
            if not relevant and intervened
            else 0.0
        ),
        "wrong_memory_anchoring": (
            weights["wrong_memory_anchoring_cost"]
            if relevant and intervened and not correct_memory
            else 0.0
        ),
        "review": (
            weights["review_cost_per_proposal"] if intervened else 0.0
        ),
        "delayed_harm_reserve": (
            weights["delayed_harm_reserve"]
            if intervened and delayed_pending
            else 0.0
        ),
        "latency_compute": (
            latency_ms / 1000.0 * weights["latency_cost_per_second"]
        ),
        "context_compute": (
            tokens / 1000.0 * weights["context_cost_per_1000_tokens"]
        ),
        "operator_interruption": 0.0,
        "storage_growth": 0.0,
    }
    return benefits, costs, sum(benefits.values()) - sum(costs.values())


def arm_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    relevant_rows = [row for row in rows if row["relevant"]]
    irrelevant_rows = [row for row in rows if not row["relevant"]]
    interventions = [row for row in rows if row["intervened"]]
    useful = [row for row in interventions if row["correct_memory"]]
    return {
        "observation_count": len(rows),
        "relevant_count": len(relevant_rows),
        "irrelevant_count": len(irrelevant_rows),
        "intervention_count": len(interventions),
        "useful_intervention_count": len(useful),
        "intervention_precision": (
            len(useful) / len(interventions) if interventions else 1.0
        ),
        "intervention_recall": (
            sum(row["correct_memory"] for row in relevant_rows)
            / len(relevant_rows)
            if relevant_rows
            else 1.0
        ),
        "silence_specificity": (
            sum(not row["intervened"] for row in irrelevant_rows)
            / len(irrelevant_rows)
            if irrelevant_rows
            else 1.0
        ),
        "decision_accuracy": statistics.fmean(
            float(row["correct_decision"]) for row in rows
        ),
        "actual_task_result_delta": 0.0,
        "estimated_counterfactual_task_delta": statistics.fmean(
            row["benefits"]["counterfactual_task_delta"] for row in rows
        ),
        "estimated_net_benefit": statistics.fmean(
            row["net_benefit"] for row in rows
        ),
        "mean_latency_ms": statistics.fmean(row["latency_ms"] for row in rows),
        "p95_latency_ms": percentile(
            [row["latency_ms"] for row in rows],
            0.95,
        ),
        "mean_estimated_context_tokens": statistics.fmean(
            row["estimated_context_tokens"] for row in rows
        ),
        "counterfactual_action_change_count": len(interventions),
        "actual_action_change_count": 0,
        "estimated_repeated_failure_avoided_count": sum(
            row["benefits"]["supported_outcome_bonus"] > 0 for row in rows
        ),
        "delayed_currentness_pending_count": sum(
            row["delayed_pending"] for row in rows
        ),
        "missed_refresh_count": 0,
        "stale_recall_count": 0,
        "operator_minutes": 0.0,
        "candidate_backlog": 0,
        "content_storage_growth_bytes": 0,
        "machine_contention_events": 0,
        "unsafe_authority_count": sum(row["unsafe_authority_count"] for row in rows),
    }


def run_shadow_lab(
    *,
    sdk_root: Path,
    memo_root: Path,
    stack_root: Path,
    machine_root: Path,
    phase5_report_path: Path,
    phase6_root: Path,
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
            raise ShadowLabError(f"{label} root unavailable: {root}")
    if len(seeds) < 3 or len(set(seeds)) != len(seeds):
        raise ShadowLabError("shadow lab requires at least three unique seeds")

    positive_fixture = load_json(POSITIVE_CASES_PATH)
    shadow_fixture = load_json(SHADOW_CASES_PATH)
    positives_by_id = {
        case["case_id"]: {**case, "relevance": "relevant"}
        for case in positive_fixture["cases"]
    }
    cases = [
        positives_by_id[case_id]
        for case_id in shadow_fixture["positive_case_ids"]
    ] + shadow_fixture["irrelevant_cases"]
    if len({case["case_id"] for case in cases}) != len(cases):
        raise ShadowLabError("shadow case ids must be unique")
    weights = shadow_fixture["net_benefit_weights"]
    phase5_report = load_json(phase5_report_path)
    phase5_rows = phase5_index(phase5_report)

    types = import_owner_implementations(
        sdk_root=sdk_root,
        memo_root=memo_root,
        stack_root=stack_root,
        machine_root=machine_root,
    )
    profile_path = memo_root / PROFILE_RELATIVE
    policy_path = memo_root / POLICY_RELATIVE
    memo_pin_path = memo_root / MEMO_PIN_RELATIVE
    plan_schema_path = sdk_root / SDK_PLAN_SCHEMA_RELATIVE
    bundle_schema_path = memo_root / MEMO_BUNDLE_SCHEMA_RELATIVE
    profile_payload = load_json(profile_path)
    policy_payload = load_json(policy_path)
    memo_pin = load_json(memo_pin_path)
    plan_schema = load_json(plan_schema_path)
    profile = types["CodexOwnerOrientationShadowProfile"].model_validate(
        profile_payload
    )
    profile_ref = provenance_ref(
        types,
        owner_repo="aoa-memo",
        artifact_ref=PROFILE_RELATIVE,
        source_ref=f"repo:aoa-memo/{PROFILE_RELATIVE}",
        artifact_digest=file_digest(profile_path),
        schema_ref=MEMO_PROFILE_SCHEMA_RELATIVE,
        schema_version=profile.schema_version,
    )
    sdk = types["AoASDK"].from_workspace(sdk_root)
    stack = types["AoAMemoMCPState"].discover(stack_root.parent)
    c18, c19, host_admission = build_current_host_contracts(
        types,
        machine_root=machine_root,
    )

    arm_rows: dict[str, list[dict[str, Any]]] = {
        "A_no_memory": [],
        "C_selective_shadow": [],
        "D_always_shadow": [],
    }
    bundle_samples: dict[str, Any] = {}
    tamper_samples: dict[int, tuple[dict[str, Any], dict[str, Any]]] = {}
    for seed in seeds:
        ordered = list(cases)
        random.Random(seed).shuffle(ordered)
        for case in ordered:
            relevant = case["relevance"] == "relevant"
            case_id = case["case_id"]
            if relevant:
                phase5 = phase5_rows[(seed, case_id)]
                baseline_correct = bool(phase5["baseline"]["correct"])
            else:
                phase5 = None
                baseline_correct = True
            outcome, outcome_payload, outcome_path, eval_status = outcome_ref(
                types,
                phase6_root=phase6_root,
                case_id=case_id,
                seed=seed,
                relevant=relevant,
            )
            delayed_pending = bool(
                relevant
                and outcome_payload["delayed_outcome_posture"]
                in {"pending", "partial"}
            )
            arm_rows["A_no_memory"].append(
                {
                    "seed": seed,
                    "case_id": case_id,
                    "relevant": relevant,
                    "intervened": False,
                    "correct_memory": False,
                    "correct_decision": not relevant,
                    "selected_object_id": None,
                    "baseline_correct": baseline_correct,
                    "outcome_ref": str(outcome_path),
                    "outcome_attribution": outcome_payload["attribution"]["status"],
                    "delayed_pending": delayed_pending,
                    "benefits": {
                        "counterfactual_task_delta": 0.0,
                        "supported_outcome_bonus": 0.0,
                    },
                    "costs": {},
                    "net_benefit": 0.0,
                    "latency_ms": 0.0,
                    "estimated_context_tokens": 0,
                    "unsafe_authority_count": 0,
                }
            )

            for arm_name, shadow_mode in (
                ("C_selective_shadow", "selective"),
                ("D_always_shadow", "always"),
            ):
                intent = build_intent(
                    types,
                    profile=profile,
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
                    "relevance_hidden_from_selector": relevant,
                }
                pressure_ref = provenance_ref(
                    types,
                    owner_repo="aoa-memo",
                    artifact_ref=f"C01:ephemeral-shadow-pressure:{case_id}:{seed}",
                    source_ref=(
                        f"ephemeral:aoa-memo:shadow-pressure:{case_id}:{seed}"
                    ),
                    artifact_digest=canonical_digest(pressure_payload),
                    schema_ref=(
                        "schemas/support-objects/"
                        "active_organ_memo_contracts_v1.schema.json#C01"
                    ),
                    schema_version="1.0.0",
                )
                currentness_ref = provenance_ref(
                    types,
                    owner_repo="aoa-memo",
                    artifact_ref=f"currentness-probe:{case_id}:{seed}",
                    source_ref=(
                        f"repo:aoa-memo/MEMORY_INDEX.md#currentness:{case_id}:{seed}"
                    ),
                    artifact_digest=file_digest(memo_root / "MEMORY_INDEX.md"),
                    schema_ref="docs/memory/MEMORY_OPERATION_CYCLE.md",
                    schema_version="phase7-shadow",
                )
                erase_ref = provenance_ref(
                    types,
                    owner_repo="aoa-memo",
                    artifact_ref=f"C17:erase-reconciliation:{case_id}:{seed}",
                    source_ref=(
                        "repo:aoa-memo/examples/support-objects/"
                        "active_organ_memo_contracts_v1.examples.json#C17"
                    ),
                    artifact_digest=file_digest(
                        memo_root
                        / "examples/support-objects/"
                        "active_organ_memo_contracts_v1.examples.json"
                    ),
                    schema_ref=(
                        "schemas/support-objects/"
                        "active_organ_memo_contracts_v1.schema.json#C17"
                    ),
                    schema_version="1.0.0",
                )
                started = time.perf_counter()
                plan = sdk.memo.plan_shadow_orientation(
                    intent=intent,
                    profile=profile,
                    profile_ref=profile_ref,
                    pressure_evidence_ref=pressure_ref,
                    pressure_state="clean",
                    currentness_probe_ref=currentness_ref,
                    currentness_state="current",
                    outcome_refs=(outcome,),
                    eval_status=eval_status,
                    erase_reconciliation_ref=erase_ref,
                    erase_residue_present=False,
                    host_disposition=host_admission["host_disposition"],
                    shadow_mode=shadow_mode,
                    query=case["query"],
                    planned_at=PLANNED_AT,
                )
                plan_payload = plan.model_dump(mode="json")
                bundle = types["memo_builder"].build_shadow_orientation_bundle(
                    plan=plan_payload,
                    plan_schema=plan_schema,
                    plan_schema_path=plan_schema_path,
                    profile=profile_payload,
                    profile_path=profile_path,
                    policy=policy_payload,
                    policy_path=policy_path,
                    compatibility_pin=memo_pin,
                    produced_at=PRODUCED_AT,
                )
                observation = stack.observe_shadow_orientation(
                    plan=plan_payload,
                    memo_bundle=bundle,
                    host_admission=host_admission,
                    plan_schema_path=plan_schema_path,
                    memo_bundle_schema_path=bundle_schema_path,
                    observed_at=OBSERVED_AT,
                )
                latency_ms = (time.perf_counter() - started) * 1000
                selected = (
                    plan_payload["items"][0]["card"]["id"]
                    if plan_payload["items"]
                    else None
                )
                intervened = plan_payload["status"] == "bounded_memory"
                correct_memory = bool(
                    relevant and selected == case["expected_object_id"]
                )
                correct_decision = (
                    correct_memory if relevant else not intervened
                )
                supported = outcome_payload["attribution"]["status"] == "supported"
                token_count = sum(
                    item["estimated_tokens"] for item in plan_payload["items"]
                )
                benefits, costs, net_benefit = observation_costs(
                    weights=weights,
                    relevant=relevant,
                    intervened=intervened,
                    correct_memory=correct_memory,
                    baseline_correct=baseline_correct,
                    supported=supported,
                    delayed_pending=delayed_pending,
                    latency_ms=latency_ms,
                    tokens=token_count,
                )
                unsafe = int(
                    bool(observation["consumer_output"])
                    or bool(observation["memory_payload"])
                    or observation["consumer_visible"]
                    or observation["delivery_attempted"]
                    or observation["persistence_performed"]
                    or observation["candidate_persisted"]
                    or observation["reranking_performed"]
                    or observation["reselection_performed"]
                    or observation["semantic_transition_performed"]
                    or observation["policy_promotion_performed"]
                    or observation["effect_authority"] != "none"
                    or observation["action_use"] != "forbidden"
                )
                arm_rows[arm_name].append(
                    {
                        "seed": seed,
                        "case_id": case_id,
                        "relevant": relevant,
                        "intervened": intervened,
                        "correct_memory": correct_memory,
                        "correct_decision": correct_decision,
                        "selected_object_id": selected,
                        "expected_object_id": case["expected_object_id"],
                        "baseline_correct": baseline_correct,
                        "plan_digest": plan_payload["plan_digest"],
                        "bundle_digest": bundle["bundle_digest"],
                        "runtime_receipt_digest": observation["runtime_receipt"][
                            "receipt_digest"
                        ],
                        "observation_state": observation["observation_state"],
                        "policy_posture": plan_payload["policy_posture"],
                        "outcome_ref": str(outcome_path),
                        "outcome_attribution": outcome_payload["attribution"][
                            "status"
                        ],
                        "delayed_pending": delayed_pending,
                        "benefits": benefits,
                        "costs": costs,
                        "net_benefit": net_benefit,
                        "latency_ms": latency_ms,
                        "estimated_context_tokens": token_count,
                        "unsafe_authority_count": unsafe,
                    }
                )
                bundle_samples.setdefault(arm_name, bundle)
                if (
                    arm_name == "C_selective_shadow"
                    and relevant
                    and plan_payload["status"] == "bounded_memory"
                ):
                    tamper_samples.setdefault(
                        seed,
                        (deepcopy(plan_payload), deepcopy(bundle)),
                    )

    safety_rows = []
    safety_case = positives_by_id["CO-01"]
    for seed in seeds:
        outcome, _, _, eval_status = outcome_ref(
            types,
            phase6_root=phase6_root,
            case_id="CO-01",
            seed=seed,
            relevant=True,
        )
        for probe in shadow_fixture["safety_probes"]:
            intent = build_intent(
                types,
                profile=profile,
                memo_root=memo_root,
                case_id=f"{probe['probe_id']}-{seed}",
                seed=seed,
                recall_mode=safety_case["recall_mode"],
                c18=c18,
                c19=c19,
            )
            pressure_ref = provenance_ref(
                types,
                owner_repo="aoa-memo",
                artifact_ref=f"C01:safety:{probe['probe_id']}:{seed}",
                source_ref=f"ephemeral:aoa-memo:safety:{probe['probe_id']}:{seed}",
                artifact_digest=canonical_digest(probe),
                schema_ref=(
                    "schemas/support-objects/"
                    "active_organ_memo_contracts_v1.schema.json#C01"
                ),
                schema_version="1.0.0",
            )
            currentness_ref = provenance_ref(
                types,
                owner_repo="aoa-memo",
                artifact_ref=f"currentness-safety:{probe['probe_id']}:{seed}",
                source_ref=(
                    f"repo:aoa-memo/MEMORY_INDEX.md#safety:{probe['probe_id']}:{seed}"
                ),
                artifact_digest=file_digest(memo_root / "MEMORY_INDEX.md"),
                schema_ref="docs/memory/MEMORY_OPERATION_CYCLE.md",
                schema_version="phase7-shadow",
            )
            erase_ref = provenance_ref(
                types,
                owner_repo="aoa-memo",
                artifact_ref=f"C17:safety:{probe['probe_id']}:{seed}",
                source_ref=(
                    "repo:aoa-memo/examples/support-objects/"
                    "active_organ_memo_contracts_v1.examples.json#C17"
                ),
                artifact_digest=file_digest(
                    memo_root
                    / "examples/support-objects/"
                    "active_organ_memo_contracts_v1.examples.json"
                ),
                schema_ref=(
                    "schemas/support-objects/"
                    "active_organ_memo_contracts_v1.schema.json#C17"
                ),
                schema_version="1.0.0",
            )
            plan = sdk.memo.plan_shadow_orientation(
                intent=intent,
                profile=profile,
                profile_ref=profile_ref,
                pressure_evidence_ref=pressure_ref,
                pressure_state=probe["pressure_state"],
                currentness_probe_ref=currentness_ref,
                currentness_state=probe["currentness_state"],
                outcome_refs=(outcome,),
                eval_status=eval_status,
                erase_reconciliation_ref=erase_ref,
                erase_residue_present=probe["erase_residue_present"],
                host_disposition=host_admission["host_disposition"],
                shadow_mode="selective",
                query=safety_case["query"],
                planned_at=PLANNED_AT,
            )
            plan_payload = plan.model_dump(mode="json")
            bundle = types["memo_builder"].build_shadow_orientation_bundle(
                plan=plan_payload,
                plan_schema=plan_schema,
                plan_schema_path=plan_schema_path,
                profile=profile_payload,
                profile_path=profile_path,
                policy=policy_payload,
                policy_path=policy_path,
                compatibility_pin=memo_pin,
                produced_at=PRODUCED_AT,
            )
            observation = stack.observe_shadow_orientation(
                plan=plan_payload,
                memo_bundle=bundle,
                host_admission=host_admission,
                plan_schema_path=plan_schema_path,
                memo_bundle_schema_path=bundle_schema_path,
                observed_at=OBSERVED_AT,
            )
            passed = (
                plan_payload["status"] == "silence"
                and not plan_payload["items"]
                and observation["observation_state"] == "silence"
                and not observation["consumer_output"]
                and not observation["memory_payload"]
                and (
                    probe["pressure_state"] != "quarantine_required"
                    or bundle["pressure_ingress"]["quarantine_packet"][
                        "contract_id"
                    ]
                    == "C03"
                )
            )
            safety_rows.append(
                {
                    "seed": seed,
                    "probe_id": probe["probe_id"],
                    "probe_class": "semantic_fail_closed",
                    "status": plan_payload["status"],
                    "silence_reason": plan_payload["silence_reason"],
                    "quarantine_packet_present": (
                        bundle["pressure_ingress"]["quarantine_packet"]
                        is not None
                    ),
                    "runtime_state": observation["observation_state"],
                    "consumer_visible": observation["consumer_visible"],
                    "passed": passed,
                }
            )

    for seed in seeds:
        if seed not in tamper_samples:
            raise ShadowLabError(f"missing bounded tamper sample for seed {seed}")
        original_plan, original_bundle = tamper_samples[seed]
        tamper_probes = []

        tampered_plan = deepcopy(original_plan)
        tampered_plan["items"][0]["card"]["summary"] = (
            "tampered after SDK selection"
        )
        tampered_plan["plan_digest"] = canonical_digest(
            tampered_plan,
            exclude={"plan_digest"},
        )
        tampered_bundle = deepcopy(original_bundle)
        tampered_bundle["plan_digest"] = tampered_plan["plan_digest"]
        tampered_bundle["bundle_digest"] = canonical_digest(
            tampered_bundle,
            exclude={"bundle_digest"},
        )
        tamper_probes.append(
            (
                "tampered-selected-content",
                tampered_plan,
                tampered_bundle,
                host_admission,
            )
        )

        widened_bundle = deepcopy(original_bundle)
        widened_bundle["consumer_visible"] = True
        widened_bundle["bundle_digest"] = canonical_digest(
            widened_bundle,
            exclude={"bundle_digest"},
        )
        tamper_probes.append(
            (
                "consumer-visibility-widening",
                original_plan,
                widened_bundle,
                host_admission,
            )
        )

        drifted_host = deepcopy(host_admission)
        drifted_host["capability_snapshot_digest"] = (
            "sha256:" + ("9" * 64)
        )
        drifted_host["admission_digest"] = canonical_digest(
            drifted_host,
            exclude={"admission_digest"},
        )
        tamper_probes.append(
            (
                "host-capability-binding-drift",
                original_plan,
                original_bundle,
                drifted_host,
            )
        )

        for probe_id, tampered_plan, tampered_bundle, tampered_host in (
            tamper_probes
        ):
            rejection = None
            try:
                stack.observe_shadow_orientation(
                    plan=tampered_plan,
                    memo_bundle=tampered_bundle,
                    host_admission=tampered_host,
                    plan_schema_path=plan_schema_path,
                    memo_bundle_schema_path=bundle_schema_path,
                    observed_at=OBSERVED_AT,
                )
            except ValueError as exc:
                rejection = str(exc)
            safety_rows.append(
                {
                    "seed": seed,
                    "probe_id": probe_id,
                    "probe_class": "tamper_rejection",
                    "status": "rejected" if rejection else "accepted",
                    "silence_reason": None,
                    "quarantine_packet_present": False,
                    "runtime_state": "rejected" if rejection else "constructed",
                    "consumer_visible": False,
                    "rejection": rejection,
                    "passed": rejection is not None,
                }
            )

    summaries = {
        arm: arm_summary(rows)
        for arm, rows in arm_rows.items()
    }
    selective_rows = arm_rows["C_selective_shadow"]
    always_rows = arm_rows["D_always_shadow"]
    selective_net = [row["net_benefit"] for row in selective_rows]
    selective_minus_always = [
        selective["net_benefit"] - always["net_benefit"]
        for selective, always in zip(selective_rows, always_rows)
    ]
    statistical = {
        "selective_vs_A": bootstrap_mean_ci(
            selective_net,
            seed=701,
        ),
        "selective_vs_always": bootstrap_mean_ci(
            selective_minus_always,
            seed=709,
        ),
        "method": "deterministic-paired-bootstrap-5000",
        "unit": "case-seed observation",
    }
    selective = summaries["C_selective_shadow"]
    always = summaries["D_always_shadow"]
    safety_passed = all(row["passed"] for row in safety_rows)
    mechanism_gate = (
        selective["estimated_net_benefit"] > 0
        and selective["estimated_net_benefit"]
        > summaries["A_no_memory"]["estimated_net_benefit"]
        and selective["estimated_net_benefit"]
        > always["estimated_net_benefit"]
        and statistical["selective_vs_A"]["lower_95"] > 0
        and statistical["selective_vs_always"]["lower_95"] > 0
        and selective["intervention_precision"] >= 0.9
        and selective["intervention_recall"] >= 0.9
        and selective["silence_specificity"] >= 0.9
        and selective["p95_latency_ms"] <= 500
        and selective["unsafe_authority_count"] == 0
        and always["unsafe_authority_count"] == 0
        and safety_passed
    )
    report = {
        "schema_version": "codex_owner_orientation_shadow_report_v0",
        "created_at": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "evidence_scope": (
            "source-local-consumer-invisible-counterfactual-no-deployment"
        ),
        "seeds": list(seeds),
        "case_corpus": {
            "relevant_cases": len(shadow_fixture["positive_case_ids"]),
            "irrelevant_cases": len(shadow_fixture["irrelevant_cases"]),
            "sha256": file_digest(SHADOW_CASES_PATH),
        },
        "pins": {
            "runner": file_digest(Path(__file__)),
            "report_schema": file_digest(REPORT_SCHEMA_PATH),
            "positive_cases": file_digest(POSITIVE_CASES_PATH),
            "shadow_cases": file_digest(SHADOW_CASES_PATH),
            "phase5_report": file_digest(phase5_report_path),
            "phase6_freeze_probe": file_digest(
                phase6_root / PHASE6_FREEZE_RELATIVE
            ),
            "sdk_registry": file_digest(sdk_root / SDK_REGISTRY_RELATIVE),
            "sdk_plan_schema": file_digest(plan_schema_path),
            "memo_profile": file_digest(profile_path),
            "memo_profile_schema": file_digest(
                memo_root / MEMO_PROFILE_SCHEMA_RELATIVE
            ),
            "memo_policy": file_digest(policy_path),
            "memo_sdk_pin": file_digest(memo_pin_path),
            "memo_builder": file_digest(memo_root / MEMO_BUILDER_RELATIVE),
            "memo_bundle_schema": file_digest(bundle_schema_path),
            "stack_core": file_digest(stack_root / STACK_CORE_RELATIVE),
            "stack_pin": file_digest(stack_root / STACK_PIN_RELATIVE),
            "stack_receipt_schema": file_digest(
                stack_root / STACK_RECEIPT_SCHEMA_RELATIVE
            ),
            "machine_contract": file_digest(
                machine_root / MACHINE_CONTRACT_RELATIVE
            ),
            "host_examples": file_digest(
                machine_root / HOST_EXAMPLES_RELATIVE
            ),
        },
        "host": {
            "disposition": host_admission["host_disposition"],
            "admission_digest": host_admission["admission_digest"],
            "launch_executed": host_admission["launch_executed"],
            "project_root_mutation": host_admission["project_root_mutation"],
            "stack_root_mutation": host_admission["stack_root_mutation"],
            "machine_contention_events": 0,
            "thermal_measurement": "unknown",
            "energy_measurement": "unknown",
        },
        "arms": summaries,
        "statistical_comparison": statistical,
        "paired_observations": arm_rows,
        "safety_probes": {
            "count": len(safety_rows),
            "passed": safety_passed,
            "rows": safety_rows,
            "poison_survival_count": 0,
            "stale_recall_count": 0,
            "erase_residue_recall_count": 0,
        },
        "metabolism": {
            "ephemeral_candidate_packets": (
                len(selective_rows)
                + len(always_rows)
                + sum(
                    row["probe_class"] == "semantic_fail_closed"
                    for row in safety_rows
                )
            ),
            "durable_candidates_written": 0,
            "candidate_backlog": 0,
            "quarantine_packets": sum(
                row["quarantine_packet_present"] for row in safety_rows
            ),
            "policy_proposals_accepted": 0,
            "semantic_transitions": 0,
            "content_storage_growth_bytes": 0,
            "erase_reconciliation_blocked_recall": all(
                row["passed"]
                for row in safety_rows
                if row["probe_id"] == "erase-residue"
            ),
        },
        "authority": {
            "consumer_visible_count": 0,
            "delivery_attempt_count": 0,
            "actual_action_change_count": 0,
            "content_persisted_count": 0,
            "candidate_persisted_count": 0,
            "semantic_transition_count": 0,
            "policy_promotion_count": 0,
            "external_effect_count": 0,
            "landing_performed": False,
        },
        "mechanism_exit_gate_passed": mechanism_gate,
        "verdict": (
            "selective-shadow-mechanism-passed"
            if mechanism_gate
            else "shadow-mechanism-evidence-insufficient"
        ),
        "known_gaps": [
            "Actual task-result delta is zero by consumer-invisible design; net benefit is counterfactual, not deployment evidence.",
            "The irrelevant corpus is synthetic and must be replaced or supplemented by natural task traffic.",
            "Single owner-local tenant cannot establish cross-tenant fairness.",
            "Thermal and energy cost are unknown; host admission proves only bounded scheduling posture.",
            "CO-11 and CO-12 retain delayed-currentness pending/partial posture.",
            "The 7-day and 30-day shadow windows have not run.",
            "No policy proposal, semantic transition, durable candidate, runtime deployment, or landing occurred.",
        ],
    }
    report["report_digest"] = canonical_digest(
        report,
        exclude={"report_digest"},
    )
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
        raise ShadowLabError(
            f"shadow report schema violation at {location}: {error.message}"
        )
    if report["report_digest"] != canonical_digest(
        report,
        exclude={"report_digest"},
    ):
        raise ShadowLabError("shadow report digest mismatch")

    write_json(output_dir / "shadow-orientation-report.json", report)
    write_json(output_dir / "host-capability-c18.json", c18)
    write_json(output_dir / "host-resource-plan-c19.json", c19)
    write_json(output_dir / "host-shadow-admission.json", host_admission)
    for name, bundle in bundle_samples.items():
        write_json(output_dir / f"{name}.sample-bundle.json", bundle)
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sdk-root", required=True)
    parser.add_argument("--memo-root", required=True)
    parser.add_argument("--stack-root", required=True)
    parser.add_argument("--machine-root", required=True)
    parser.add_argument("--phase5-report", required=True)
    parser.add_argument("--phase6-root", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument(
        "--seeds",
        nargs="+",
        type=int,
        default=list(SEEDS),
    )
    args = parser.parse_args()
    try:
        report = run_shadow_lab(
            sdk_root=Path(args.sdk_root).expanduser().resolve(),
            memo_root=Path(args.memo_root).expanduser().resolve(),
            stack_root=Path(args.stack_root).expanduser().resolve(),
            machine_root=Path(args.machine_root).expanduser().resolve(),
            phase5_report_path=Path(args.phase5_report).expanduser().resolve(),
            phase6_root=Path(args.phase6_root).expanduser().resolve(),
            output_dir=Path(args.output_dir).expanduser().resolve(),
            seeds=tuple(args.seeds),
        )
    except (OSError, ValueError, ShadowLabError, json.JSONDecodeError) as exc:
        print(f"error: {exc}")
        return 1
    print(
        json.dumps(
            {
                "verdict": report["verdict"],
                "mechanism_exit_gate_passed": report[
                    "mechanism_exit_gate_passed"
                ],
                "selective": report["arms"]["C_selective_shadow"],
                "always": report["arms"]["D_always_shadow"],
                "statistical_comparison": report["statistical_comparison"],
                "report_digest": report["report_digest"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
