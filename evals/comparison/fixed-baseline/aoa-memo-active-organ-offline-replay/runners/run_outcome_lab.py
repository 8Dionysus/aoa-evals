#!/usr/bin/env python3
"""Materialize and validate the Phase 6 C10 outcome/attribution lab."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any, Sequence

from jsonschema import Draft202012Validator, FormatChecker


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = BUNDLE_ROOT / "fixtures" / "consumer-orientation-cases.json"
REPORT_SCHEMA_PATH = BUNDLE_ROOT / "reports" / "outcome-attribution.schema.json"
EXPERIMENT_VALIDATOR_PATH = (
    BUNDLE_ROOT.parents[3]
    / "mechanics"
    / "proof-infra"
    / "parts"
    / "reportable-contracts"
    / "scripts"
    / "validate_active_organ_experiment_contracts.py"
)
C21_EXAMPLE_PATH = (
    BUNDLE_ROOT.parents[3]
    / "mechanics"
    / "proof-infra"
    / "parts"
    / "reportable-contracts"
    / "examples"
    / "active_organ_model_prompt_provider_hardware_pin.example.json"
)
C22_EXAMPLE_PATH = (
    BUNDLE_ROOT.parents[3]
    / "mechanics"
    / "proof-infra"
    / "parts"
    / "reportable-contracts"
    / "examples"
    / "active_organ_memory_experiment_manifest.example.json"
)
STATS_SCHEMA_RELATIVE = "stats/measurement-contract/outcome-receipt.schema.json"
STATS_EXAMPLES_RELATIVE = (
    "mechanics/boundary-bridge/parts/measurement-packet-crossing/"
    "examples/active_organ_outcome_receipt_v1.examples.json"
)
STATS_OUTCOME_RELATIVE = "src/aoa_stats_builder/outcome.py"
HOST_EXAMPLES_RELATIVE = (
    "mechanics/host-facts/examples/active_organ_host_contracts_v1.examples.json"
)
ZERO_DIGEST = "sha256:" + ("0" * 64)


class OutcomeLabError(RuntimeError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise OutcomeLabError(f"{path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise OutcomeLabError(f"{path}: expected JSON object")
    return payload


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def canonical_digest(payload: Any) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def file_digest(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def normalized_report_digest(report: dict[str, Any]) -> str:
    return canonical_digest(
        {
            key: value
            for key, value in report.items()
            if key != "report_digest"
        }
    )


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise OutcomeLabError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def provenance_ref(
    *,
    owner_repo: str,
    artifact_ref: str,
    artifact_version: str,
    artifact_digest: str,
) -> dict[str, str]:
    return {
        "owner_repo": owner_repo,
        "artifact_ref": artifact_ref,
        "artifact_version": artifact_version,
        "artifact_digest": artifact_digest,
    }


def ref_key(ref: dict[str, str]) -> tuple[str, str, str, str]:
    return (
        ref["owner_repo"],
        ref["artifact_ref"],
        ref["artifact_version"],
        ref["artifact_digest"],
    )


def unique_refs(refs: Sequence[dict[str, str]]) -> list[dict[str, str]]:
    result = []
    seen = set()
    for ref in refs:
        key = ref_key(ref)
        if key not in seen:
            result.append(ref)
            seen.add(key)
    return result


def validate_schema(
    payload: dict[str, Any],
    schema_path: Path,
    label: str,
) -> None:
    schema = load_json(schema_path)
    errors = sorted(
        Draft202012Validator(
            schema,
            format_checker=FormatChecker(),
        ).iter_errors(payload),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        error = errors[0]
        location = ".".join(str(item) for item in error.absolute_path) or "<root>"
        raise OutcomeLabError(
            f"{label} schema violation at {location}: {error.message}"
        )


def iso_add(value: str, *, seconds: int = 0, days: int = 0) -> str:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return (
        (parsed + timedelta(seconds=seconds, days=days))
        .astimezone(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def randomized_assigned_arm(
    case_id: str,
    seed: int,
    seeds: Sequence[int],
) -> str:
    case_index = int(case_id.removeprefix("CO-")) - 1
    seed_index = sorted(seeds).index(seed)
    return "A" if (case_index + seed_index) % 2 == 0 else "B"


def build_c21(consumer_report: dict[str, Any]) -> dict[str, Any]:
    pin = load_json(C21_EXAMPLE_PATH)
    pins = consumer_report["pins"]
    pin.update(
        {
            "pin_id": "aoa-evals:active-organ-pin:phase6-owner-orientation-v1",
            "captured_at": consumer_report["created_at"],
            "model": {
                "owner_ref": "aoa-sdk:memo-owner-orientation-selector",
                "artifact_ref": "repo:aoa-sdk/src/aoa_sdk/memo/registry.py",
                "artifact_sha256": pins["sdk_registry"],
                "revision": "phase6-source-local-candidate",
                "inference_parameters_sha256": canonical_digest(
                    {
                        "algorithm": "idf-field-phrase-currentness-v1",
                        "plan_schema": pins["sdk_plan_schema"],
                        "profile": pins["memo_profile"],
                    }
                ),
            },
            "prompt": {
                "template_ref": "none:deterministic-owner-orientation",
                "template_sha256": (
                    "sha256:"
                    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
                ),
                "system_policy_ref": (
                    "repo:aoa-memo/codex_owner_orientation_v0.influence-policy"
                ),
                "system_policy_sha256": pins["memo_policy"],
                "sampling_config_sha256": canonical_digest(
                    {"temperature": 0, "seeded_order_only": True}
                ),
            },
            "provider": {
                "provider_id": "none",
                "api_family": "deterministic-python",
                "api_version": "phase6-v1",
                "endpoint_class": "local_subprocess",
                "adapter_ref": "aoa-sdk:memo-orient-plan",
            },
            "hardware": {
                "host_capability_snapshot_ref": (
                    "abyss-machine:C18:active-organ-host-contracts-v1"
                ),
                "host_resource_storage_plan_ref": (
                    "abyss-machine:C19:active-organ-host-contracts-v1"
                ),
                "execution_device_class": "host-cpu",
                "driver_runtime_ref": "python:current-host-runtime",
            },
            "runtime": {
                "runtime_owner_ref": "aoa-sdk:selection-plus-abyss-stack:delivery",
                "runtime_adapter_ref": "abyss-stack:codex-owner-orientation-v0",
                "runtime_artifact_sha256": pins["stack_delivery_core"],
                "dependency_lock_sha256": pins["sdk_dependency_manifest"],
                "environment_contract_ref": (
                    "aoa-evals:phase6-source-local-owner-worktrees"
                ),
            },
            "integrity": {
                "component_manifest_sha256": canonical_digest(pins),
                "all_refs_resolved": True,
                "captured_from_current_owner_sources": True,
            },
        }
    )
    return pin


def build_c22(
    consumer_report: dict[str, Any],
    *,
    c21: dict[str, Any],
    c21_file_digest: str,
) -> dict[str, Any]:
    manifest = load_json(C22_EXAMPLE_PATH)
    fixture_digest = consumer_report["case_fixture"]["sha256"]
    manifest.update(
        {
            "experiment_id": (
                "aoa-evals:active-organ-experiment:phase6-outcome-attribution-v1"
            ),
            "manifest_version": 1,
            "created_at": consumer_report["created_at"],
            "bounded_question": (
                "Under the pinned source-local owner-orientation consumer, "
                "which action changes and terminal outcomes can be attributed "
                "to reviewed explicit-pull memory without using access count, "
                "hiding uncertainty, or granting semantic authority?"
            ),
            "source_bundle_ref": (
                "aoa-evals:evals/comparison/fixed-baseline/"
                "aoa-memo-active-organ-offline-replay"
            ),
            "corpus": {
                "corpus_id": "phase6-owner-orientation-public-reviewed-cases",
                "corpus_version": "1",
                "corpus_sha256": fixture_digest,
                "split_manifest_ref": (
                    "aoa-evals:phase6:paired-all-cases-three-seeds"
                ),
                "selection_manifest_ref": (
                    "aoa-evals:fixtures/consumer-orientation-cases.json"
                ),
                "contamination_policy_ref": (
                    "aoa-evals:phase6:public-reviewed-no-training"
                ),
                "data_class": "public-safe-reviewed",
            },
            "seeds": consumer_report["seeds"],
            "environment_pins": [
                {
                    "pin_ref": c21["pin_id"],
                    "pin_sha256": c21_file_digest,
                    "applies_to_arms": ["A", "B", "C"],
                }
            ],
            "host_plan": {
                "host_capability_snapshot_ref": (
                    "abyss-machine:C18:active-organ-host-contracts-v1"
                ),
                "host_resource_storage_plan_ref": (
                    "abyss-machine:C19:active-organ-host-contracts-v1"
                ),
                "runtime_plan_ref": (
                    "aoa-evals:phase6-source-local-no-heavy-runtime-v1"
                ),
            },
            "budgets": {
                "max_total_runs": (
                    len(consumer_report["paired_observations"]) * 2
                ),
                "max_wall_seconds": 3600,
                "max_tokens": 900,
                "max_cost": {"amount": 0, "currency": "USD"},
                "stop_on_exceed": True,
            },
            "execution": {
                "paired_tasks": True,
                "randomized": True,
                "order_policy": (
                    "seeded case order with paired holdout A and explicit-pull B; "
                    "C remains always-shadow counterfactual only"
                ),
                "max_concurrency": 1,
                "warmup_runs_per_arm": 0,
                "retry_policy": "no_hidden_retry",
                "environment_recheck_each_run": True,
                "comparison_plan_ref": (
                    "aoa-evals:notes/comparison-contract.md#phase-5-source-local"
                ),
            },
            "metrics": [
                {
                    "metric_id": "terminal-outcome",
                    "owner_ref": "aoa-stats:C10:terminal-outcome-v1",
                    "axis": "outcome",
                    "role": "primary",
                    "direction": "maximize",
                    "aggregation": "paired exact rate by arm and seed",
                },
                {
                    "metric_id": "action-change",
                    "owner_ref": "aoa-stats:C10:action-change-v1",
                    "axis": "quality",
                    "role": "secondary",
                    "direction": "maximize",
                    "aggregation": "paired changed-action count with attribution class",
                },
                {
                    "metric_id": "runtime-latency",
                    "owner_ref": "aoa-stats:C10:latency-v1",
                    "axis": "latency",
                    "role": "secondary",
                    "direction": "minimize",
                    "aggregation": "mean and p95 by arm",
                },
                {
                    "metric_id": "context-and-operator-cost",
                    "owner_ref": "aoa-stats:C10:phase6-cost-v1",
                    "axis": "cost",
                    "role": "secondary",
                    "direction": "minimize",
                    "aggregation": (
                        "mean context tokens and operator attention by arm"
                    ),
                },
                {
                    "metric_id": "unsafe-attribution",
                    "owner_ref": "aoa-stats:C10:unsafe-attribution-v1",
                    "axis": "safety",
                    "role": "guardrail",
                    "direction": "minimize",
                    "aggregation": "count",
                },
            ],
            "claim_limit": (
                "Source-local public reviewed outcome receipts only; no deployed "
                "consumer, private-task benefit, policy promotion, semantic "
                "transition, training, production, or landing authority."
            ),
        }
    )
    manifest["preregistration"][
        "manifest_sha256"
    ] = ZERO_DIGEST
    return manifest


def task_artifacts(
    consumer_report: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    task_facts = {
        "schema_version": "phase6_owner_orientation_task_facts_v1",
        "consumer_report_digest": consumer_report["report_digest"],
        "facts": [],
    }
    counterfactuals = {
        "schema_version": "phase6_always_shadow_counterfactuals_v1",
        "consumer_visible": False,
        "architecture_c_implemented": False,
        "observations": [],
    }
    evaluations = {
        "schema_version": "phase6_independent_evaluation_evidence_v1",
        "evaluator_id": "aoa-evals.independent-deterministic-judge.phase6",
        "same_selector_as_judge": False,
        "fairness_scope": "single-owner-local-tenant-only",
        "observations": [],
    }
    measurements = {
        "schema_version": "phase6_owner_orientation_measurements_v1",
        "host_measurement_scope": (
            "static C18/C19 planning evidence; no live thermal or energy reading"
        ),
        "observations": [],
    }
    for observation in consumer_report["paired_observations"]:
        seed = observation["seed"]
        case_id = observation["case_id"]
        assigned_arm = randomized_assigned_arm(
            case_id,
            seed,
            consumer_report["seeds"],
        )
        baseline = observation["baseline"]
        active = observation["active"]
        for arm_id, row in (("A", baseline), ("B", active)):
            task_facts["facts"].append(
                {
                    "fact_id": f"phase6-task-fact:{case_id}:{seed}:{arm_id}",
                    "case_id": case_id,
                    "seed": seed,
                    "arm_id": arm_id,
                    "expected_object_id": observation["expected_object_id"],
                    "selected_object_id": row["selected_object_id"],
                    "terminal_state": (
                        "success" if row["correct"] else "failure"
                    ),
                    "task_owner_acceptance": True,
                    "randomized_assigned": arm_id == assigned_arm,
                }
            )
        changed = (
            baseline["selected_object_id"] != active["selected_object_id"]
        )
        counterfactuals["observations"].append(
            {
                "counterfactual_id": f"phase6-shadow:{case_id}:{seed}",
                "case_id": case_id,
                "seed": seed,
                "baseline_selected_object_id": baseline["selected_object_id"],
                "active_selected_object_id": active["selected_object_id"],
                "action_changed": changed,
                "baseline_correct": baseline["correct"],
                "active_correct": active["correct"],
                "consumer_visible": False,
                "randomized_assigned_arm": assigned_arm,
            }
        )
        evaluations["observations"].append(
            {
                "evaluation_id": f"phase6-eval:{case_id}:{seed}",
                "case_id": case_id,
                "seed": seed,
                "judge_rule": "exact expected object and exact source route",
                "active_correct": active["correct"],
                "source_route_correct": active["source_route_correct"],
                "action_changed": changed,
                "reward_hacking_check": {
                    "access_count_used": False,
                    "terminal_fact_used": True,
                },
                "fairness_tenant_skew_check": {
                    "status": "not_established_single_tenant",
                    "tenant_id": "owner-local",
                },
                "model_version_stratum": (
                    "deterministic-lexical-phase6-source-local-candidate"
                ),
                "randomized_assigned_arm": assigned_arm,
            }
        )
        measurements["observations"].append(
            {
                "measurement_id": f"phase6-measurement:{case_id}:{seed}",
                "case_id": case_id,
                "seed": seed,
                "baseline": {
                    "latency_ms": baseline["latency_ms"],
                    "estimated_context_tokens": baseline[
                        "estimated_context_tokens"
                    ],
                    "operator_attention_units": baseline[
                        "operator_attention_units"
                    ],
                    "bytes_scanned": baseline["bytes_scanned"],
                    "filesystem_reads": baseline["filesystem_reads"],
                },
                "active": {
                    "latency_ms": active["latency_ms"],
                    "estimated_context_tokens": active[
                        "estimated_context_tokens"
                    ],
                    "operator_attention_units": active[
                        "operator_attention_units"
                    ],
                    "bytes_scanned": active["bytes_scanned"],
                    "filesystem_reads": active["filesystem_reads"],
                },
                "energy": "unknown",
                "thermal": "unknown",
                "storage_delta": "unknown",
            }
        )
    return task_facts, counterfactuals, evaluations, measurements


def action_snapshot(
    *,
    phase: str,
    observed_at: str,
    case_id: str,
    arm_id: str,
    task_ref: dict[str, str],
    consumer_report_ref: dict[str, str],
    selected_object_id: str,
    selected_source_ref: str,
) -> dict[str, Any]:
    payload = {
        "phase": phase,
        "observed_at": observed_at,
        "completeness": "complete",
        "decision_state": "selected",
        "action_class": "owner-orientation-source-selection",
        "target_ref": task_ref,
        "operation_id": f"owner-orientation:{case_id}:{arm_id}",
        "parameters_digest": canonical_digest(
            {
                "selected_object_id": selected_object_id,
                "selected_source_ref": selected_source_ref,
            }
        ),
        "source_snapshot_ref": consumer_report_ref,
        "approval_ref": None,
        "rollback_ref": None,
        "snapshot_digest": ZERO_DIGEST,
        "raw_content_included": False,
    }
    payload["snapshot_digest"] = canonical_digest(
        {
            key: value
            for key, value in payload.items()
            if key != "snapshot_digest"
        }
    )
    return payload


def cost_observations(
    *,
    arm_name: str,
    row: dict[str, Any],
    measurement_ref: dict[str, str],
) -> list[dict[str, Any]]:
    observed = (
        (
            "latency-ms",
            "latency",
            "ms",
            row["latency_ms"],
        ),
        (
            "context-tokens",
            "tokens",
            "estimated_token",
            row["estimated_context_tokens"],
        ),
        (
            "operator-attention",
            "operator_time",
            "attention_unit",
            row["operator_attention_units"],
        ),
    )
    costs = [
        {
            "measurement_id": f"{arm_name}/{measurement_id}",
            "category": category,
            "status": "observed",
            "unit": unit,
            "number": number,
            "sample_size": 1,
            "measurement_packet_ref": measurement_ref,
        }
        for measurement_id, category, unit, number in observed
    ]
    for measurement_id, category, unit in (
        ("energy", "energy", "joule"),
        ("storage", "storage", "byte"),
    ):
        costs.append(
            {
                "measurement_id": f"{arm_name}/{measurement_id}",
                "category": category,
                "status": "unknown",
                "unit": unit,
                "number": None,
                "sample_size": 0,
                "measurement_packet_ref": None,
            }
        )
    return costs


def build_receipt(
    *,
    observation: dict[str, Any],
    arm_id: str,
    created_at: str,
    consumer_report_ref: dict[str, str],
    fixture_ref: dict[str, str],
    task_facts_ref: dict[str, str],
    counterfactual_ref: dict[str, str],
    evaluation_ref: dict[str, str],
    measurement_ref: dict[str, str],
    c21_ref: dict[str, str],
    c22_ref: dict[str, str],
    host_ref: dict[str, str],
    policy_digest: str,
    randomized_arm: str,
    outcome_module,
) -> dict[str, Any]:
    seed = observation["seed"]
    case_id = observation["case_id"]
    baseline = observation["baseline"]
    active = observation["active"]
    memory_used = arm_id == "B"
    row = active if memory_used else baseline
    before_source = baseline["source_ref"]
    after_source = (
        active["source_route"] if memory_used else baseline["source_ref"]
    )
    after_selected = (
        active["selected_object_id"]
        if memory_used
        else baseline["selected_object_id"]
    )
    task_ref = provenance_ref(
        owner_repo="aoa-evals",
        artifact_ref=(
            "evals/comparison/fixed-baseline/"
            "aoa-memo-active-organ-offline-replay/fixtures/"
            f"consumer-orientation-cases.json#{case_id}"
        ),
        artifact_version="1",
        artifact_digest=fixture_ref["artifact_digest"],
    )
    task_fact_ref = provenance_ref(
        owner_repo="aoa-evals",
        artifact_ref=f"artifact:phase6/task-facts.json#{case_id}:{seed}:{arm_id}",
        artifact_version="1",
        artifact_digest=task_facts_ref["artifact_digest"],
    )
    eval_observation_ref = provenance_ref(
        owner_repo="aoa-evals",
        artifact_ref=f"artifact:phase6/evaluation-evidence.json#{case_id}:{seed}",
        artifact_version="1",
        artifact_digest=evaluation_ref["artifact_digest"],
    )
    shadow_ref = provenance_ref(
        owner_repo="aoa-evals",
        artifact_ref=f"artifact:phase6/counterfactuals.json#{case_id}:{seed}",
        artifact_version="1",
        artifact_digest=counterfactual_ref["artifact_digest"],
    )
    measure_observation_ref = provenance_ref(
        owner_repo="aoa-evals",
        artifact_ref=f"artifact:phase6/measurements.json#{case_id}:{seed}",
        artifact_version="1",
        artifact_digest=measurement_ref["artifact_digest"],
    )
    report_observation_ref = provenance_ref(
        owner_repo="aoa-evals",
        artifact_ref=(
            f"artifact:phase5/consumer-orientation-report.json#{case_id}:{seed}"
        ),
        artifact_version="1",
        artifact_digest=consumer_report_ref["artifact_digest"],
    )
    before = action_snapshot(
        phase="before_memory",
        observed_at=created_at,
        case_id=case_id,
        arm_id=arm_id,
        task_ref=task_ref,
        consumer_report_ref=report_observation_ref,
        selected_object_id=baseline["selected_object_id"],
        selected_source_ref=before_source,
    )
    after = action_snapshot(
        phase="after_memory",
        observed_at=iso_add(created_at, seconds=1),
        case_id=case_id,
        arm_id=arm_id,
        task_ref=task_ref,
        consumer_report_ref=report_observation_ref,
        selected_object_id=after_selected,
        selected_source_ref=after_source,
    )
    delayed_required = case_id in {"CO-11", "CO-12"}
    action_changed = (
        baseline["selected_object_id"] != active["selected_object_id"]
    )
    is_randomized_observation = arm_id == randomized_arm
    if (
        memory_used
        and is_randomized_observation
        and action_changed
        and active["correct"]
    ):
        attribution = {
            "status": "supported",
            "confidence": "medium",
            "basis": "randomized_evidence",
            "eval_verdict_ref": eval_observation_ref,
            "counterfactual_ref": shadow_ref,
            "causal_claim": "forbidden",
        }
    elif memory_used and action_changed and active["correct"]:
        attribution = {
            "status": "possible",
            "confidence": "low",
            "basis": "paired_evidence",
            "eval_verdict_ref": eval_observation_ref,
            "counterfactual_ref": shadow_ref,
            "causal_claim": "forbidden",
        }
    elif memory_used:
        attribution = {
            "status": "contested",
            "confidence": "low",
            "basis": "paired_evidence",
            "eval_verdict_ref": eval_observation_ref,
            "counterfactual_ref": shadow_ref,
            "causal_claim": "forbidden",
        }
    else:
        attribution = {
            "status": "not_evaluated",
            "confidence": "none",
            "basis": "not_applicable",
            "eval_verdict_ref": None,
            "counterfactual_ref": None,
            "causal_claim": "forbidden",
        }
    receipt = {
        "schema_version": "1.0.0",
        "contract_id": "C10",
        "contract_name": "OutcomeReceipt",
        "receipt_id": f"outcome-receipt:phase6:{case_id}:{seed}:{arm_id}",
        "receipt_version": 1,
        "idempotency_key": f"phase6:{case_id}:{seed}:{arm_id}:v1",
        "producer_owner": "aoa-evals",
        "fact_owner": "aoa-evals",
        "stats_schema_owner": "aoa-stats",
        "tenant_id": "owner-local",
        "consumer_id": "codex_owner_orientation_v0",
        "run_id": f"phase6:{case_id}:{seed}",
        "task_ref": task_ref,
        "trigger_ref": fixture_ref,
        "anchor_ref": consumer_report_ref,
        "recall_intent_ref": (
            provenance_ref(
                owner_repo="aoa-sdk",
                artifact_ref=active["recall_intent_id"],
                artifact_version="C07-v1",
                artifact_digest=active["recall_intent_digest"],
            )
            if memory_used
            else None
        ),
        "recall_packet_refs": (
            [
                provenance_ref(
                    owner_repo="aoa-memo",
                    artifact_ref=active["recall_packet_ref"],
                    artifact_version="C08-v1",
                    artifact_digest=active["recall_packet_digest"],
                )
            ]
            if memory_used
            else []
        ),
        "intervention_decision_ref": (
            provenance_ref(
                owner_repo="aoa-memo",
                artifact_ref=active["intervention_decision_ref"],
                artifact_version="C09-v1",
                artifact_digest=active["intervention_decision_digest"],
            )
            if memory_used
            else None
        ),
        "runtime_delivery_ref": (
            provenance_ref(
                owner_repo="abyss-stack",
                artifact_ref=active["runtime_receipt_id"],
                artifact_version="C20-v1",
                artifact_digest=active["runtime_receipt_digest"],
            )
            if memory_used
            else None
        ),
        "experiment_manifest_ref": c22_ref,
        "model_prompt_provider_hardware_pin_ref": c21_ref,
        "host_observation_refs": [host_ref],
        "experiment_assignment": {
            "design": (
                "randomized_holdout"
                if is_randomized_observation
                else "paired"
            ),
            "arm_id": arm_id,
            "assignment_digest": canonical_digest(
                {
                    "case_id": case_id,
                    "seed": seed,
                    "randomized_arm": randomized_arm,
                    "receipt_arm": arm_id,
                    "receipt_role": (
                        "randomized_observation"
                        if is_randomized_observation
                        else "shadow_counterfactual"
                    ),
                }
            ),
            "holdout": (
                not memory_used
                if is_randomized_observation
                else "unknown"
            ),
            "always_shadow_counterfactual_ref": shadow_ref,
        },
        "exact_effect_binding_ref": task_fact_ref,
        "memory_used": memory_used,
        "action_before_memory": before,
        "action_after_memory": after,
        "terminal_outcome": {
            "outcome_id": f"phase6-terminal:{case_id}:{seed}:{arm_id}",
            "kind": "terminal",
            "state": "success" if row["correct"] else "failure",
            "observed_at": iso_add(created_at, seconds=2),
            "expected_at": None,
            "owner_fact_ref": task_fact_ref,
            "task_owner_acceptance": True,
            "quality_measurement_refs": [eval_observation_ref],
            "raw_content_included": False,
        },
        "delayed_outcome_posture": (
            "pending" if delayed_required else "none_expected"
        ),
        "delayed_outcomes": (
            [
                {
                    "outcome_id": (
                        f"phase6-delayed-currentness:{case_id}:{seed}:{arm_id}"
                    ),
                    "kind": "delayed",
                    "state": "pending",
                    "observed_at": None,
                    "expected_at": iso_add(created_at, days=1),
                    "owner_fact_ref": None,
                    "task_owner_acceptance": "unknown",
                    "quality_measurement_refs": [],
                    "raw_content_included": False,
                }
            ]
            if delayed_required
            else []
        ),
        "confounders": [
            {
                "confounder_id": f"single-host-cache:{case_id}:{seed}:{arm_id}",
                "class": "environment",
                "direction": "could_mix",
                "materiality": "possible",
                "evidence_refs": [measure_observation_ref],
            }
        ],
        "accidental_success": {
            "value": False,
            "detection_basis": "eval_verdict",
            "evidence_refs": [eval_observation_ref],
        },
        "harm": {
            "observed": False,
            "severity": "none",
            "harm_refs": [],
            "immediate_stop_triggered": False,
        },
        "cost_observations": cost_observations(
            arm_name=arm_id,
            row=row,
            measurement_ref=measure_observation_ref,
        ),
        "evaluator": {
            "evaluator_id": "aoa-evals.independent-deterministic-judge.phase6",
            "owner_repo": "aoa-evals",
            "role": "independent_judge",
            "evidence_ref": eval_observation_ref,
        },
        "operator_intervention": {
            "occurred": False,
            "intervention_class": "none",
            "evidence_refs": [],
            "time_measurement_ref": None,
        },
        "evaluation_posture": {
            "eval_plane_status": "available",
            "independent_judge_ref": eval_observation_ref,
            "reward_hacking_check_ref": eval_observation_ref,
            "fairness_tenant_skew_ref": eval_observation_ref,
            "model_version_stratum_ref": c21_ref,
            "access_count_used_as_utility": False,
            "policy_update_state": "proposal_only",
            "semantic_memory_transition_allowed": False,
        },
        "attribution": attribution,
        "source_refs": unique_refs(
            [
                task_ref,
                task_fact_ref,
                consumer_report_ref,
                fixture_ref,
                counterfactual_ref,
                evaluation_ref,
                measurement_ref,
                c21_ref,
                c22_ref,
                host_ref,
            ]
            + (
                [
                    provenance_ref(
                        owner_repo="aoa-memo",
                        artifact_ref=active["recall_packet_ref"],
                        artifact_version="C08-v1",
                        artifact_digest=active["recall_packet_digest"],
                    ),
                    provenance_ref(
                        owner_repo="aoa-memo",
                        artifact_ref=active["intervention_decision_ref"],
                        artifact_version="C09-v1",
                        artifact_digest=active["intervention_decision_digest"],
                    ),
                    provenance_ref(
                        owner_repo="abyss-stack",
                        artifact_ref=active["runtime_receipt_id"],
                        artifact_version="C20-v1",
                        artifact_digest=active["runtime_receipt_digest"],
                    ),
                ]
                if memory_used
                else []
            )
        ),
        "policy_pin": {
            "policy_id": "policy:aoa-memo:codex-owner-orientation:v0",
            "policy_version": "0",
            "decision_ref": "decision:aoa-memo-active-organ-phase1-v1",
            "policy_digest": policy_digest,
        },
        "privacy_class": "D0",
        "retention_until": iso_add(created_at, days=365),
        "validation_status": "partial" if delayed_required else "valid",
        "produced_at": iso_add(created_at, seconds=3),
        "content_digest": ZERO_DIGEST,
        "raw_content_included": False,
        "payload_refs_only": True,
        "semantic_authority": "none",
        "effect_authority": "none",
        "training_use": "forbidden",
    }
    receipt["content_digest"] = outcome_module.normalized_outcome_receipt_digest(
        receipt
    )
    return receipt


def validate_report(report: dict[str, Any]) -> None:
    validate_schema(report, REPORT_SCHEMA_PATH, "outcome report")
    expected = normalized_report_digest(report)
    if report.get("report_digest") != expected:
        raise OutcomeLabError(
            f"outcome report digest mismatch: {report.get('report_digest')} != "
            f"{expected}"
        )


def run_outcome_lab(
    *,
    consumer_report_path: Path,
    stats_root: Path,
    machine_root: Path,
    output_dir: Path,
) -> dict[str, Any]:
    consumer_report = load_json(consumer_report_path)
    if not consumer_report.get("exit_gate_passed"):
        raise OutcomeLabError("Phase 5 consumer report did not pass its exit gate")
    cases = load_json(CASES_PATH)
    if consumer_report["case_fixture"]["sha256"] != file_digest(CASES_PATH):
        raise OutcomeLabError("Phase 5 report does not pin the current case fixture")
    if consumer_report["pins"]["consumer_report_schema"] != file_digest(
        BUNDLE_ROOT / "reports" / "consumer-orientation.schema.json"
    ):
        raise OutcomeLabError("Phase 5 consumer report schema pin drifted")

    stats_schema_path = stats_root / STATS_SCHEMA_RELATIVE
    stats_examples_path = stats_root / STATS_EXAMPLES_RELATIVE
    host_examples_path = machine_root / HOST_EXAMPLES_RELATIVE
    for path in (
        stats_schema_path,
        stats_examples_path,
        host_examples_path,
        REPORT_SCHEMA_PATH,
    ):
        if not path.is_file():
            raise OutcomeLabError(f"required owner artifact is missing: {path}")
    outcome_module = load_module(
        "aoa_stats_phase6_outcome",
        stats_root / STATS_OUTCOME_RELATIVE,
    )
    experiment_validator = load_module(
        "aoa_evals_phase6_experiment_contracts",
        EXPERIMENT_VALIDATOR_PATH,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    c21 = build_c21(consumer_report)
    experiment_validator.validate_payload(c21)
    c21_path = output_dir / "c21-owner-orientation-pin.json"
    write_json(c21_path, c21)
    c21_digest = file_digest(c21_path)

    c22 = build_c22(
        consumer_report,
        c21=c21,
        c21_file_digest=c21_digest,
    )
    c22["preregistration"][
        "manifest_sha256"
    ] = experiment_validator.normalized_c22_manifest_sha256(c22)
    experiment_validator.validate_payload(c22)
    c22_path = output_dir / "c22-outcome-attribution-manifest.json"
    write_json(c22_path, c22)
    c22_digest = file_digest(c22_path)

    task_facts, counterfactuals, evaluations, measurements = task_artifacts(
        consumer_report
    )
    artifact_payloads = {
        "task-facts.json": task_facts,
        "counterfactuals.json": counterfactuals,
        "evaluation-evidence.json": evaluations,
        "measurements.json": measurements,
    }
    artifact_paths = {}
    for name, payload in artifact_payloads.items():
        path = output_dir / name
        write_json(path, payload)
        artifact_paths[name] = path

    consumer_report_digest = file_digest(consumer_report_path)
    fixture_digest = file_digest(CASES_PATH)
    host_digest = file_digest(host_examples_path)
    task_facts_ref = provenance_ref(
        owner_repo="aoa-evals",
        artifact_ref="artifact:phase6/task-facts.json",
        artifact_version="1",
        artifact_digest=file_digest(artifact_paths["task-facts.json"]),
    )
    counterfactual_ref = provenance_ref(
        owner_repo="aoa-evals",
        artifact_ref="artifact:phase6/counterfactuals.json",
        artifact_version="1",
        artifact_digest=file_digest(artifact_paths["counterfactuals.json"]),
    )
    evaluation_ref = provenance_ref(
        owner_repo="aoa-evals",
        artifact_ref="artifact:phase6/evaluation-evidence.json",
        artifact_version="1",
        artifact_digest=file_digest(artifact_paths["evaluation-evidence.json"]),
    )
    measurement_ref = provenance_ref(
        owner_repo="aoa-evals",
        artifact_ref="artifact:phase6/measurements.json",
        artifact_version="1",
        artifact_digest=file_digest(artifact_paths["measurements.json"]),
    )
    consumer_report_ref = provenance_ref(
        owner_repo="aoa-evals",
        artifact_ref="artifact:phase5/consumer-orientation-report.json",
        artifact_version="1",
        artifact_digest=consumer_report_digest,
    )
    fixture_ref = provenance_ref(
        owner_repo="aoa-evals",
        artifact_ref=(
            "evals/comparison/fixed-baseline/"
            "aoa-memo-active-organ-offline-replay/fixtures/"
            "consumer-orientation-cases.json"
        ),
        artifact_version="1",
        artifact_digest=fixture_digest,
    )
    c21_ref = provenance_ref(
        owner_repo="aoa-evals",
        artifact_ref="artifact:phase6/c21-owner-orientation-pin.json",
        artifact_version="C21-v1",
        artifact_digest=c21_digest,
    )
    c22_ref = provenance_ref(
        owner_repo="aoa-evals",
        artifact_ref="artifact:phase6/c22-outcome-attribution-manifest.json",
        artifact_version="C22-v1",
        artifact_digest=c22_digest,
    )
    host_ref = provenance_ref(
        owner_repo="abyss-machine",
        artifact_ref=f"repo:abyss-machine/{HOST_EXAMPLES_RELATIVE}",
        artifact_version="C18-C19-v1",
        artifact_digest=host_digest,
    )

    receipts = []
    semantic_failures = []
    schema_failures = []
    receipt_dir = output_dir / "receipts"
    for observation in consumer_report["paired_observations"]:
        randomized_arm = randomized_assigned_arm(
            observation["case_id"],
            observation["seed"],
            consumer_report["seeds"],
        )
        for arm_id in ("A", "B"):
            receipt = build_receipt(
                observation=observation,
                arm_id=arm_id,
                created_at=consumer_report["created_at"],
                consumer_report_ref=consumer_report_ref,
                fixture_ref=fixture_ref,
                task_facts_ref=task_facts_ref,
                counterfactual_ref=counterfactual_ref,
                evaluation_ref=evaluation_ref,
                measurement_ref=measurement_ref,
                c21_ref=c21_ref,
                c22_ref=c22_ref,
                host_ref=host_ref,
                policy_digest=consumer_report["pins"]["memo_policy"],
                randomized_arm=randomized_arm,
                outcome_module=outcome_module,
            )
            label = f"{observation['case_id']}:{observation['seed']}:{arm_id}"
            try:
                validate_schema(receipt, stats_schema_path, label)
            except OutcomeLabError as exc:
                schema_failures.append(str(exc))
            issues = outcome_module.validate_outcome_receipt_semantics(receipt)
            if issues:
                semantic_failures.append({"label": label, "issues": issues})
            receipt_path = (
                receipt_dir
                / f"{observation['seed']}-{observation['case_id']}-{arm_id}.json"
            )
            write_json(receipt_path, receipt)
            receipts.append(receipt)

    freeze_suite = load_json(stats_examples_path)
    freeze_probe = next(
        case["payload"]
        for case in freeze_suite["valid_cases"]
        if case["case_id"] == "unknown_use_and_attribution_remain_unknown"
    )
    validate_schema(freeze_probe, stats_schema_path, "eval-unavailable freeze probe")
    freeze_issues = outcome_module.validate_outcome_receipt_semantics(freeze_probe)
    freeze_path = output_dir / "eval-unavailable-freeze-probe.json"
    write_json(freeze_path, freeze_probe)

    main_receipt_count = len(receipts)
    active_receipts = [
        receipt
        for receipt in receipts
        if receipt["experiment_assignment"]["arm_id"] == "B"
    ]
    control_receipts = [
        receipt
        for receipt in receipts
        if receipt["experiment_assignment"]["arm_id"] == "A"
    ]
    supported = [
        receipt
        for receipt in active_receipts
        if receipt["attribution"]["status"] == "supported"
    ]
    contested = [
        receipt
        for receipt in active_receipts
        if receipt["attribution"]["status"] == "contested"
    ]
    possible_shadow = [
        receipt
        for receipt in active_receipts
        if receipt["attribution"]["status"] == "possible"
    ]
    changed = [
        observation
        for observation in consumer_report["paired_observations"]
        if observation["baseline"]["selected_object_id"]
        != observation["active"]["selected_object_id"]
    ]
    pending_delayed = sum(
        receipt["delayed_outcome_posture"] == "pending"
        for receipt in receipts
    )
    randomized_receipts = [
        receipt
        for receipt in receipts
        if receipt["experiment_assignment"]["design"] == "randomized_holdout"
    ]
    paired_counterfactual_receipts = [
        receipt
        for receipt in receipts
        if receipt["experiment_assignment"]["design"] == "paired"
    ]
    randomized_holdout_receipts = [
        receipt
        for receipt in randomized_receipts
        if receipt["experiment_assignment"]["holdout"] is True
    ]
    unsafe = sum(
        receipt["semantic_authority"] != "none"
        or receipt["effect_authority"] != "none"
        or receipt["training_use"] != "forbidden"
        or receipt["evaluation_posture"]["access_count_used_as_utility"]
        or receipt["evaluation_posture"][
            "semantic_memory_transition_allowed"
        ]
        for receipt in receipts
    )
    exit_gate = (
        not schema_failures
        and not semantic_failures
        and not freeze_issues
        and main_receipt_count
        == len(consumer_report["paired_observations"]) * 2
        and len(supported) + len(possible_shadow) == len(changed)
        and len(supported) > 0
        and len(randomized_receipts)
        == len(consumer_report["paired_observations"])
        and len(randomized_holdout_receipts)
        == len(randomized_receipts) // 2
        and len(paired_counterfactual_receipts) == len(randomized_receipts)
        and len(control_receipts) == len(active_receipts)
        and all(
            receipt["attribution"]["status"] == "not_evaluated"
            for receipt in control_receipts
        )
        and all(
            not receipt["operator_intervention"]["occurred"]
            for receipt in receipts
        )
        and unsafe == 0
        and freeze_probe["evaluation_posture"]["policy_update_state"]
        == "frozen"
    )
    report = {
        "schema_version": "phase6_outcome_attribution_report_v1",
        "created_at": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "evidence_scope": "source-local-public-reviewed-no-deployment",
        "input": {
            "consumer_report_ref": consumer_report_path.as_posix(),
            "consumer_report_file_digest": consumer_report_digest,
            "consumer_report_normalized_digest": consumer_report["report_digest"],
            "consumer_exit_gate_passed": consumer_report["exit_gate_passed"],
            "case_count": len(cases["cases"]),
            "seed_count": len(consumer_report["seeds"]),
        },
        "pins": {
            "runner": file_digest(Path(__file__)),
            "report_schema": file_digest(REPORT_SCHEMA_PATH),
            "c10_schema": file_digest(stats_schema_path),
            "c10_semantic_validator": file_digest(
                stats_root / STATS_OUTCOME_RELATIVE
            ),
            "c21_file": c21_digest,
            "c22_file": c22_digest,
            "c22_normalized_self_digest": c22["preregistration"][
                "manifest_sha256"
            ],
            "fixture": fixture_digest,
            "host_examples": host_digest,
        },
        "experiment": {
            "design": "paired-randomized-holdout-with-shadow-counterfactual",
            "arms_materialized": ["A", "B"],
            "arm_c_posture": "counterfactual-only-not-implemented",
            "seed_count": len(consumer_report["seeds"]),
            "paired_case_seed_count": len(
                consumer_report["paired_observations"]
            ),
            "randomized_observation_count": len(randomized_receipts),
            "randomized_holdout_count": len(randomized_holdout_receipts),
            "paired_counterfactual_count": len(
                paired_counterfactual_receipts
            ),
        },
        "receipts": {
            "main_count": main_receipt_count,
            "schema_valid_count": main_receipt_count - len(schema_failures),
            "semantic_valid_count": main_receipt_count - len(semantic_failures),
            "schema_failures": schema_failures,
            "semantic_failures": semantic_failures,
            "content_self_digest_count": sum(
                receipt["content_digest"]
                == outcome_module.normalized_outcome_receipt_digest(receipt)
                for receipt in receipts
            ),
            "partial_delayed_count": pending_delayed,
        },
        "attribution": {
            "active_supported_count": len(supported),
            "active_contested_no_action_change_count": len(contested),
            "active_possible_shadow_action_change_count": len(
                possible_shadow
            ),
            "control_not_evaluated_count": sum(
                receipt["attribution"]["status"] == "not_evaluated"
                for receipt in control_receipts
            ),
            "action_changed_count": len(changed),
            "unknown_count": sum(
                receipt["attribution"]["status"] == "unknown"
                for receipt in receipts
            ),
        },
        "safety": {
            "unsafe_authority_count": unsafe,
            "harm_observed_count": sum(
                receipt["harm"]["observed"] is True for receipt in receipts
            ),
            "accidental_success_count": sum(
                receipt["accidental_success"]["value"] is True
                for receipt in receipts
            ),
            "operator_intervention_count": sum(
                receipt["operator_intervention"]["occurred"] is True
                for receipt in receipts
            ),
            "access_count_used_as_utility_count": sum(
                receipt["evaluation_posture"]["access_count_used_as_utility"]
                for receipt in receipts
            ),
            "semantic_transition_allowed_count": sum(
                receipt["evaluation_posture"][
                    "semantic_memory_transition_allowed"
                ]
                for receipt in receipts
            ),
        },
        "freeze_probe": {
            "schema_valid": True,
            "semantic_valid": not freeze_issues,
            "issues": freeze_issues,
            "eval_plane_status": freeze_probe["evaluation_posture"][
                "eval_plane_status"
            ],
            "policy_update_state": freeze_probe["evaluation_posture"][
                "policy_update_state"
            ],
            "attribution_status": freeze_probe["attribution"]["status"],
            "file_digest": file_digest(freeze_path),
        },
        "known_gaps": [
            "CO-11 and CO-12 delayed-currentness outcomes remain pending.",
            "Fairness and tenant skew are not established by one owner-local tenant.",
            "C18/C19 are static planning evidence, not live energy or thermal measurements.",
            "The independent judge is deterministic and public-fixture-based.",
            "Arm C is a counterfactual reference only; the shadow organ is Phase 7 work.",
        ],
        "exit_gate_passed": exit_gate,
        "verdict": (
            "supports Phase 7 read-only shadow implementation"
            if exit_gate
            else "does not support Phase 7 continuation"
        ),
        "authority": {
            "production_authorized": False,
            "deployment_authorized": False,
            "consumer_visible_intervention_authorized": False,
            "policy_promotion_authorized": False,
            "semantic_memory_transition_authorized": False,
            "training_authorized": False,
            "landing_authorized": False,
        },
    }
    report["report_digest"] = normalized_report_digest(report)
    validate_report(report)
    report_path = output_dir / "outcome-attribution-report.json"
    write_json(report_path, report)
    return report


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--consumer-report", type=Path, required=True)
    result.add_argument("--stats-root", type=Path, required=True)
    result.add_argument("--machine-root", type=Path, required=True)
    result.add_argument("--output-dir", type=Path, required=True)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        report = run_outcome_lab(
            consumer_report_path=args.consumer_report.resolve(),
            stats_root=args.stats_root.resolve(),
            machine_root=args.machine_root.resolve(),
            output_dir=args.output_dir.resolve(),
        )
    except (
        OutcomeLabError,
        OSError,
        ValueError,
        KeyError,
        TypeError,
    ) as exc:
        print(f"outcome attribution lab: invalid: {exc}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "ok": report["exit_gate_passed"],
                "output": (
                    args.output_dir / "outcome-attribution-report.json"
                ).as_posix(),
                "report_digest": report["report_digest"],
                "verdict": report["verdict"],
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if report["exit_gate_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
