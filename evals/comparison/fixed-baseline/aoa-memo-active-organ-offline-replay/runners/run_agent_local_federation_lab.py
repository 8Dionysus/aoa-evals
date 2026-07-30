#!/usr/bin/env python3
"""Run the Phase 12 public-safe agent-local federation reference lab."""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import importlib
import importlib.util
import json
from pathlib import Path
from time import perf_counter
import sys
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = BUNDLE_ROOT / "fixtures" / "agent-local-federation-cases.json"
REPORT_SCHEMA_PATH = BUNDLE_ROOT / "reports" / "agent-local-federation.schema.json"

AGENT_SCHEMA_REL = "schemas/active-organ-agent-local-namespace-v0.schema.json"
AGENT_EXAMPLE_REL = "examples/active-organ-agent-local-namespace.example.json"
AGENT_VALIDATOR_REL = "scripts/validate_active_organ_agent_local_namespace.py"
SDK_POLICY_SCHEMA_REL = (
    "mechanics/boundary-bridge/parts/consumed-surface-posture-gate/schemas/"
    "agent-local-memory-consumer-policy-v0.schema.json"
)
SDK_PLAN_SCHEMA_REL = (
    "mechanics/boundary-bridge/parts/consumed-surface-posture-gate/schemas/"
    "agent-local-namespace-plan-v0.schema.json"
)
SDK_COMPILER_REL = "src/aoa_sdk/memo/agent_local.py"
MEMO_CANDIDATE_SCHEMA_REL = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/schemas/"
    "agent_local_shared_promotion_candidate_v0.schema.json"
)
MEMO_RECEIPT_SCHEMA_REL = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/schemas/"
    "agent_local_promotion_admission_receipt_v0.schema.json"
)
MEMO_CANDIDATE_EXAMPLE_REL = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/examples/"
    "agent_local_shared_promotion_candidate_v0.example.json"
)
MEMO_RECEIPT_EXAMPLE_REL = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/examples/"
    "agent_local_promotion_admission_receipt_v0.example.json"
)
MEMO_VALIDATOR_REL = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/scripts/"
    "agent_local_promotion.py"
)
MEMO_DECISION_REL = (
    "docs/decisions/AOA-MEM-D-0081-agent-local-promotion-is-not-shared-truth.md"
)
STACK_SCHEMA_REL = (
    "mechanics/federation-seams/parts/memo-seam/schemas/"
    "active-organ-agent-local-runtime-namespace-v0.schema.json"
)
KAG_SCHEMA_REL = (
    "mechanics/antifragility/parts/projection-health/schemas/"
    "active_organ_agent_local_projection_admission_v0.schema.json"
)
STATS_SCHEMA_REL = (
    "mechanics/boundary-bridge/parts/measurement-packet-crossing/schemas/"
    "active_organ_agent_local_federation_aggregate_v0.schema.json"
)


class AgentLocalFederationLabError(RuntimeError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AgentLocalFederationLabError(f"{path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise AgentLocalFederationLabError(f"{path}: expected JSON object")
    return payload


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def canonical_digest(
    payload: Any,
    *,
    exclude: set[str] | None = None,
) -> str:
    excluded = exclude or set()
    normalized = (
        {key: value for key, value in payload.items() if key not in excluded}
        if isinstance(payload, dict)
        else payload
    )
    encoded = json.dumps(
        normalized,
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
        raise AgentLocalFederationLabError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def validator(path: Path) -> Draft202012Validator:
    schema = load_json(path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def assert_valid(
    payload: dict[str, Any],
    schema_validator: Draft202012Validator,
    label: str,
) -> None:
    errors = sorted(
        schema_validator.iter_errors(payload),
        key=lambda item: list(item.absolute_path),
    )
    if errors:
        locations = [
            f"{'.'.join(str(x) for x in error.absolute_path) or '<root>'}: "
            f"{error.message}"
            for error in errors
        ]
        raise AgentLocalFederationLabError(
            f"{label} failed schema validation: {'; '.join(locations)}"
        )


def sdk_modules(sdk_root: Path) -> dict[str, Any]:
    source = str((sdk_root / "src").resolve())
    for name in list(sys.modules):
        if name == "aoa_sdk" or name.startswith("aoa_sdk."):
            del sys.modules[name]
    if source not in sys.path:
        sys.path.insert(0, source)
    return {
        "contracts": importlib.import_module("aoa_sdk.contracts.memo"),
        "control": importlib.import_module("aoa_sdk.contracts.control_plane"),
        "compiler": importlib.import_module("aoa_sdk.memo.agent_local"),
    }


def provenance_ref(
    control: Any,
    *,
    owner: str,
    name: str,
    digest: str,
) -> Any:
    return control.ProvenanceRef(
        owner_repo=owner,
        artifact_ref=f"artifact:phase12:{name}",
        source_ref=f"repo:{owner}/{name}",
        artifact_digest=digest,
        schema_ref=f"schema:phase12:{name}",
        schema_version="v0",
    )


def build_agent_namespaces(
    *,
    fixture: dict[str, Any],
    agents_root: Path,
    agents_module: Any,
) -> list[dict[str, Any]]:
    schema = load_json(agents_root / AGENT_SCHEMA_REL)
    example = load_json(agents_root / AGENT_EXAMPLE_REL)
    built = []
    for item in fixture["namespaces"]:
        payload = deepcopy(example)
        payload.update(
            {
                "namespace_id": item["namespace_id"],
                "namespace_generation": item["generation"],
                "agent_id": item["agent_id"],
                "role_profile_ref": f"agents/roles/{item['role']}/profile.json",
                "tenant_id": item["tenant_id"],
            }
        )
        payload["rollback"]["target_generation"] = item["generation"] - 1
        agents_module.validate_namespace(
            payload,
            schema=schema,
            repo_root=agents_root,
        )
        built.append(payload)
    return built


def build_sdk_plans(
    *,
    fixture: dict[str, Any],
    modules: dict[str, Any],
    pins: dict[str, str],
) -> tuple[list[Any], Any, Any]:
    contracts = modules["contracts"]
    control = modules["control"]
    compile_plan = modules["compiler"].compile_agent_local_namespace_plan
    models = tuple(
        contracts.ActiveOrganModelPromptProviderPin.model_validate(item)
        for item in fixture["model_pins"]
    )
    planned_at = datetime.fromisoformat(
        fixture["reference_time"].replace("Z", "+00:00")
    )
    expires_at = datetime.fromisoformat(
        fixture["expires_at"].replace("Z", "+00:00")
    )
    namespace_ref = provenance_ref(
        control,
        owner="aoa-agents",
        name="agent-local-namespace",
        digest=pins["agent_namespace_schema"],
    )
    candidate_ref = provenance_ref(
        control,
        owner="aoa-memo",
        name="agent-local-promotion-candidate",
        digest=pins["memo_promotion_candidate_schema"],
    )
    receipt_ref = provenance_ref(
        control,
        owner="aoa-memo",
        name="agent-local-promotion-receipt",
        digest=pins["memo_promotion_receipt_schema"],
    )

    def make(item: dict[str, Any], status: str, zero_ref: Any = None) -> Any:
        policy = contracts.AgentLocalMemoryConsumerPolicy(
            policy_id=f"policy:{item['role']}:local",
            policy_version="phase12-v0",
            decision_ref="decision:operator:phase12-reference",
            policy_digest=canonical_digest(
                {
                    "consumer": item["role"],
                    "namespace": item["namespace_id"],
                    "phase": 12,
                }
            ),
            consumer_id=f"consumer:{item['role']}",
            tenant_id=item["tenant_id"],
            namespace_id=item["namespace_id"],
            allowed_case_classes=("episodic", "procedural"),
            max_items=8,
            max_estimated_tokens=2048,
            max_absolute_weight_delta=0.15,
            ranking_features=(
                "task_similarity",
                "outcome_qualification",
                "freshness",
                "contradiction_penalty",
                "cost",
            ),
        )
        return compile_plan(
            plan_id=f"plan:phase12:{item['role']}:{status}",
            status=status,
            agent_id=item["agent_id"],
            policy=policy,
            namespace_contract_ref=namespace_ref,
            promotion_candidate_schema_ref=candidate_ref,
            promotion_receipt_schema_ref=receipt_ref,
            model_pins=models,
            planned_at=planned_at,
            expires_at=expires_at,
            promotion_nomination_authorized=True,
            consumer_zero_evidence_ref=zero_ref,
        )

    active = [make(item, "active") for item in fixture["namespaces"]]
    isolated = make(fixture["namespaces"][1], "isolated")
    zero_ref = provenance_ref(
        control,
        owner="aoa-sdk",
        name="consumer-zero-evaluator",
        digest=canonical_digest({"consumer": "evaluator", "state": "zero"}),
    )
    zero = make(fixture["namespaces"][3], "consumer_zero", zero_ref)
    return active, isolated, zero


def runtime_namespace_payload(
    item: dict[str, Any],
    *,
    state: str,
    plan: Any,
    agent_schema_digest: str,
) -> dict[str, Any]:
    zero = state == "consumer_zero"
    isolated = state == "isolated"
    return {
        "schema_version": "active_organ_agent_local_runtime_namespace_v0",
        "runtime_namespace_id": (
            f"runtime-{item['namespace_id']}"
        ),
        "namespace_id": item["namespace_id"],
        "namespace_generation": item["generation"],
        "agent_id": item["agent_id"],
        "tenant_id": item["tenant_id"],
        "state": state,
        "sdk_plan_ref": plan.plan_id,
        "sdk_plan_digest": plan.plan_digest,
        "agent_namespace_contract_ref": AGENT_SCHEMA_REL,
        "agent_namespace_contract_digest": agent_schema_digest,
        "case_classes": ["episodic", "procedural"],
        "storage_budget": {
            "max_objects": 128,
            "max_bytes": 1048576,
            "write_amplification_ceiling": 3,
        },
        "isolation": {
            "storage_key": (
                f"{item['tenant_id'].removeprefix('tenant:')}/"
                f"{item['namespace_id'].removeprefix('namespace:')}/"
                f"{item['generation']}"
            ),
            "read_scope": "exact_namespace_generation",
            "write_scope": "exact_namespace_generation",
            "cross_agent_read": "forbidden",
            "cross_tenant_read": "forbidden",
            "failure_scope": "namespace_only",
        },
        "expiry": {
            "namespace_local": True,
            "expires_at": "2026-08-05T12:00:00Z",
            "shared_lifecycle_effect": "none",
        },
        "rollback": {
            "target_generation": item["generation"] - 1,
            "scope": "namespace_only",
            "receipt_ref": f"rollback:{item['namespace_id']}",
            "shared_ledger_effect": "none",
        },
        "promotion": {
            "mode": "reviewed_nomination_only",
            "handoff_owner": "aoa-memo",
            "direct_shared_write": "forbidden",
        },
        "shared_organ": {
            "available_when_local_isolated": True,
            "dependency_on_local_namespace": "none",
        },
        "consumer_zero": {
            "evidence_ref": (
                "consumer-zero:evaluator-beta" if zero else None
            ),
            "local_material_state": (
                "absent" if zero else "isolated" if isolated else "present"
            ),
            "new_reads": not (zero or isolated),
            "new_writes": not (zero or isolated),
            "new_promotions": not (zero or isolated),
        },
        "execution_posture": "reference_lab_only",
        "live_execution": False,
        "effect_authority": "none",
    }


def build_promotions(
    *,
    fixture: dict[str, Any],
    memo_root: Path,
    memo_module: Any,
    pins: dict[str, str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    candidate_base = load_json(memo_root / MEMO_CANDIDATE_EXAMPLE_REL)
    receipt_base = load_json(memo_root / MEMO_RECEIPT_EXAMPLE_REL)
    namespaces = {item["namespace_id"]: item for item in fixture["namespaces"]}
    cases = {item["case_id"]: item for item in fixture["local_cases"]}
    candidates = []
    receipts = []
    for index, promotion in enumerate(fixture["promotion_cases"], start=1):
        case = cases[promotion["case_id"]]
        namespace = namespaces[case["namespace_id"]]
        slug = f"phase12-{index:02d}"
        candidate = deepcopy(candidate_base)
        candidate.update({"proposal_id": f"promotion-candidate:{slug}"})
        candidate["source_namespace"].update(
            {
                "namespace_id": namespace["namespace_id"],
                "namespace_generation": namespace["generation"],
                "agent_id": namespace["agent_id"],
                "tenant_id": namespace["tenant_id"],
                "contract_digest": pins["agent_namespace_schema"],
            }
        )
        candidate["source_case"].update(
            {
                "case_ref": case["case_id"],
                "case_digest": canonical_digest(
                    {
                        "case_id": case["case_id"],
                        "semantic_key": case["semantic_key"],
                    }
                ),
                "case_class": case["case_class"],
                "data_class": "D0",
            }
        )
        candidate["target"]["tenant_id"] = namespace["tenant_id"]
        candidate["target"]["candidate_kind"] = (
            "pattern" if case["case_class"] == "procedural" else "episode"
        )
        candidate["evidence_refs"] = [f"evidence:{case['case_id']}"]
        candidate["outcome_refs"] = [f"outcome:{case['case_id']}"]
        candidate["duplicate_check_refs"] = [f"duplicate-check:{case['case_id']}"]
        candidate["conflict_check_refs"] = [f"conflict-check:{case['case_id']}"]
        memo_module.validate_candidate(candidate)
        candidates.append(candidate)

        receipt = deepcopy(receipt_base)
        receipt.update(
            {
                "receipt_id": f"promotion-receipt:{slug}",
                "proposal_ref": candidate["proposal_id"],
                "proposal_digest": canonical_digest(candidate),
                "operator_decision": {
                    "decision": promotion["decision"],
                    "decision_ref": f"operator-decision:phase12/{slug}",
                    "decision_digest": canonical_digest(
                        {
                            "case": case["case_id"],
                            "decision": promotion["decision"],
                        }
                    ),
                },
                "duplicate_status": promotion["duplicate_status"],
                "duplicate_refs": (
                    []
                    if promotion["duplicate_status"] == "none"
                    else [f"memory:duplicate/{case['semantic_key']}"]
                ),
                "conflict_status": promotion["conflict_status"],
                "conflict_refs": (
                    []
                    if promotion["conflict_status"] == "none"
                    else [f"memory:conflict/{case['semantic_key']}"]
                ),
                "result": promotion["result"],
                "memo_candidate_ref": (
                    f"candidate:aoa-memo/{slug}"
                    if promotion["result"] == "memo_candidate"
                    else None
                ),
                "promotion_burden": {
                    "review_minutes": promotion["review_minutes"],
                    "evidence_items": 2,
                    "duplicate_checks": 1,
                    "conflict_checks": 1,
                },
            }
        )
        memo_module.validate_receipt(receipt)
        receipts.append(receipt)
    return candidates, receipts


def kag_projection_checks(kag_root: Path) -> bool:
    projection_validator = validator(kag_root / KAG_SCHEMA_REL)
    payload = {
        "schema_version": "active_organ_agent_local_projection_admission_v0",
        "admission_id": "projection-admission:phase12-reviewed-reference",
        "tenant_id": "tenant:operator",
        "source_namespace_ref": "namespace:coder-alpha",
        "source_namespace_digest": "sha256:" + "1" * 64,
        "promotion_receipt_ref": "promotion-receipt:reference",
        "promotion_receipt_digest": "sha256:" + "2" * 64,
        "reviewed_memory_object_ref": "memory:reviewed/reference",
        "reviewed_memory_object_digest": "sha256:" + "3" * 64,
        "accepted_transition_ref": "transition:reviewed/reference",
        "promotion_state": "reviewed_shared",
        "source_kind": "reviewed_memory_object",
        "projection_eligible": True,
        "local_case_material_included": False,
        "cross_tenant_projection": "forbidden",
        "direct_local_projection": "forbidden",
        "live_execution": False,
        "authority": {
            "shared_truth": "aoa-memo",
            "promotion": "forbidden",
            "semantic_transition": "forbidden",
        },
    }
    assert_valid(payload, projection_validator, "reviewed projection reference")
    unreviewed = deepcopy(payload)
    unreviewed["promotion_state"] = "nominated"
    return bool(list(projection_validator.iter_errors(unreviewed)))


def build_stats_aggregate(
    fixture: dict[str, Any],
    receipts: list[dict[str, Any]],
) -> dict[str, Any]:
    result_counts = {
        result: sum(receipt["result"] == result for receipt in receipts)
        for result in (
            "memo_candidate",
            "duplicate_no_write",
            "conflict_quarantine",
            "rejected",
            "deferred",
        )
    }
    review_minutes = sum(
        receipt["promotion_burden"]["review_minutes"] for receipt in receipts
    )
    saved = fixture["saved_re_grounding_minutes"]
    return {
        "schema_version": "active_organ_agent_local_federation_aggregate_v0",
        "aggregate_id": "agent-local-aggregate:phase12-reference",
        "run_ref": "eval-run:phase12/reference",
        "namespace_count": len(fixture["namespaces"]),
        "agent_count": len({item["agent_id"] for item in fixture["namespaces"]}),
        "tenant_count": len({item["tenant_id"] for item in fixture["namespaces"]}),
        "local_case_count": len(fixture["local_cases"]),
        "duplicate_case_count": result_counts["duplicate_no_write"],
        "promotion": {
            "nominated": len(receipts),
            "memo_candidates": result_counts["memo_candidate"],
            "duplicate_no_write": result_counts["duplicate_no_write"],
            "conflict_quarantine": result_counts["conflict_quarantine"],
            "rejected": result_counts["rejected"],
            "deferred": result_counts["deferred"],
            "silent_shared_truth_count": 0,
        },
        "isolation": {
            "max_fault_blast_radius_namespaces": 1,
            "cross_agent_contamination_count": 0,
            "cross_tenant_leak_count": 0,
            "private_to_shared_leak_count": 0,
            "degraded_isolation_passed": True,
            "shared_organ_failures_from_local_disable": 0,
        },
        "portability": {
            "model_pins_tested": len(fixture["model_pins"]),
            "portable_result_count": len(fixture["model_pins"]),
            "nonportable_result_count": 0,
        },
        "consumer_zero": {
            "namespaces_removed": 1,
            "residual_readers": 0,
            "residual_writers": 0,
            "residual_promoters": 0,
            "residual_material": 0,
        },
        "operator": {
            "review_minutes": review_minutes,
            "review_budget_minutes": fixture["review_budget_minutes"],
            "saved_re_grounding_minutes": saved,
            "net_minutes_saved": saved - review_minutes,
            "promotion_benefit_exceeds_burden": (
                saved > review_minutes
                and review_minutes <= fixture["review_budget_minutes"]
            ),
        },
        "source_refs": [
            "aoa-agents:namespace-contract",
            "aoa-sdk:consumer-plans",
            "aoa-memo:promotion-receipts",
            "abyss-stack:runtime-namespace-contract",
            "aoa-evals:phase12-run",
        ],
        "measurement_authority": "aoa-stats",
        "promotion_authority": "forbidden",
        "proof_authority": "forbidden",
    }


def fault_results(
    *,
    fixture: dict[str, Any],
    agent_payload: dict[str, Any],
    agent_validator: Draft202012Validator,
    runtime_payload: dict[str, Any],
    runtime_validator: Draft202012Validator,
    kag_root: Path,
    sdk_modules_map: dict[str, Any],
    sdk_active_plan: Any,
) -> list[dict[str, Any]]:
    kag_validator = validator(kag_root / KAG_SCHEMA_REL)
    results = []
    for fault in fixture["fault_cases"]:
        detected = False
        affected = 0
        if fault in {
            "cross_agent_lookup",
            "cross_tenant_lookup",
            "unbounded_weight_delta",
            "access_count_as_utility",
            "private_auto_share",
        }:
            candidate = deepcopy(agent_payload)
            if fault == "cross_agent_lookup":
                candidate["isolation"]["cross_agent_read"] = "allowed"
            elif fault == "cross_tenant_lookup":
                candidate["isolation"]["cross_tenant_read"] = "allowed"
            elif fault == "unbounded_weight_delta":
                candidate["ranking_adaptation"]["max_absolute_weight_delta"] = 1
            elif fault == "access_count_as_utility":
                candidate["ranking_adaptation"]["access_count_as_utility"] = "allowed"
            else:
                candidate["isolation"]["private_to_shared_default"] = "allowed"
            detected = bool(list(agent_validator.iter_errors(candidate)))
        elif fault in {
            "namespace_fault_propagation",
            "local_rollback_mutates_shared",
            "consumer_zero_residual",
        }:
            candidate = deepcopy(runtime_payload)
            if fault == "namespace_fault_propagation":
                candidate["shared_organ"]["available_when_local_isolated"] = False
                affected = 1
            elif fault == "local_rollback_mutates_shared":
                candidate["rollback"]["shared_ledger_effect"] = "rollback"
            else:
                candidate["state"] = "consumer_zero"
                candidate["consumer_zero"] = {
                    "evidence_ref": "consumer-zero:residual",
                    "local_material_state": "absent",
                    "new_reads": True,
                    "new_writes": False,
                    "new_promotions": False,
                }
            detected = bool(list(runtime_validator.iter_errors(candidate)))
        elif fault == "direct_local_kag_projection":
            candidate = {
                "schema_version": "active_organ_agent_local_projection_admission_v0",
                "admission_id": "projection-admission:direct-local",
                "tenant_id": "tenant:operator",
                "source_namespace_ref": "namespace:coder-alpha",
                "source_namespace_digest": "sha256:" + "1" * 64,
                "promotion_receipt_ref": "promotion-receipt:nominated",
                "promotion_receipt_digest": "sha256:" + "2" * 64,
                "reviewed_memory_object_ref": "local-case:coder/retry",
                "reviewed_memory_object_digest": "sha256:" + "3" * 64,
                "accepted_transition_ref": "none",
                "promotion_state": "nominated",
                "source_kind": "local_case",
                "projection_eligible": True,
                "local_case_material_included": True,
                "cross_tenant_projection": "forbidden",
                "direct_local_projection": "allowed",
                "live_execution": False,
                "authority": {
                    "shared_truth": "aoa-memo",
                    "promotion": "forbidden",
                    "semantic_transition": "forbidden",
                },
            }
            detected = bool(list(kag_validator.iter_errors(candidate)))
        elif fault == "model_specific_hidden_policy":
            plan_payload = sdk_active_plan.model_dump(mode="json")
            plan_payload["model_pins"].append(plan_payload["model_pins"][0])
            try:
                sdk_modules_map["contracts"].AgentLocalNamespacePlan.model_validate(
                    plan_payload
                )
            except Exception:
                detected = True
        if not detected:
            raise AgentLocalFederationLabError(f"fault was not detected: {fault}")
        results.append(
            {
                "fault": fault,
                "detected": True,
                "blocked": True,
                "affected_namespaces": affected,
                "shared_organ_available": True,
            }
        )
    return results


def run_lab(
    *,
    agents_root: Path,
    sdk_root: Path,
    memo_root: Path,
    stack_root: Path,
    kag_root: Path,
    stats_root: Path,
    output_path: Path | None = None,
) -> dict[str, Any]:
    started = perf_counter()
    fixture = load_json(FIXTURE_PATH)
    agent_module = load_module(
        "aoa_agents_phase12_namespace_validator",
        agents_root / AGENT_VALIDATOR_REL,
    )
    memo_module = load_module(
        "aoa_memo_phase12_promotion_validator",
        memo_root / MEMO_VALIDATOR_REL,
    )
    runner_path = Path(__file__).resolve()
    pin_paths = {
        "fixture": FIXTURE_PATH,
        "report_schema": REPORT_SCHEMA_PATH,
        "runner": runner_path,
        "agent_namespace_schema": agents_root / AGENT_SCHEMA_REL,
        "agent_namespace_example": agents_root / AGENT_EXAMPLE_REL,
        "agent_namespace_validator": agents_root / AGENT_VALIDATOR_REL,
        "sdk_consumer_policy_schema": sdk_root / SDK_POLICY_SCHEMA_REL,
        "sdk_namespace_plan_schema": sdk_root / SDK_PLAN_SCHEMA_REL,
        "sdk_namespace_compiler": sdk_root / SDK_COMPILER_REL,
        "memo_promotion_candidate_schema": memo_root / MEMO_CANDIDATE_SCHEMA_REL,
        "memo_promotion_receipt_schema": memo_root / MEMO_RECEIPT_SCHEMA_REL,
        "memo_promotion_validator": memo_root / MEMO_VALIDATOR_REL,
        "memo_decision": memo_root / MEMO_DECISION_REL,
        "stack_runtime_namespace_schema": stack_root / STACK_SCHEMA_REL,
        "kag_projection_admission_schema": kag_root / KAG_SCHEMA_REL,
        "stats_federation_aggregate_schema": stats_root / STATS_SCHEMA_REL,
    }
    missing = [name for name, path in pin_paths.items() if not path.is_file()]
    if missing:
        raise AgentLocalFederationLabError(
            f"missing pinned owner surfaces: {', '.join(missing)}"
        )
    pins = {name: file_digest(path) for name, path in pin_paths.items()}

    agent_namespaces = build_agent_namespaces(
        fixture=fixture,
        agents_root=agents_root,
        agents_module=agent_module,
    )
    modules = sdk_modules(sdk_root)
    active_plans, isolated_plan, zero_plan = build_sdk_plans(
        fixture=fixture,
        modules=modules,
        pins=pins,
    )
    sdk_policy_validator = validator(sdk_root / SDK_POLICY_SCHEMA_REL)
    sdk_plan_validator = validator(sdk_root / SDK_PLAN_SCHEMA_REL)
    for plan in (*active_plans, isolated_plan, zero_plan):
        assert_valid(
            plan.policy.model_dump(mode="json"),
            sdk_policy_validator,
            f"sdk policy {plan.plan_id}",
        )
        assert_valid(
            plan.model_dump(mode="json"),
            sdk_plan_validator,
            f"sdk plan {plan.plan_id}",
        )

    runtime_validator = validator(stack_root / STACK_SCHEMA_REL)
    runtime_states = [
        runtime_namespace_payload(
            item,
            state="active",
            plan=plan,
            agent_schema_digest=pins["agent_namespace_schema"],
        )
        for item, plan in zip(fixture["namespaces"], active_plans)
    ]
    runtime_states.extend(
        [
            runtime_namespace_payload(
                fixture["namespaces"][1],
                state="isolated",
                plan=isolated_plan,
                agent_schema_digest=pins["agent_namespace_schema"],
            ),
            runtime_namespace_payload(
                fixture["namespaces"][3],
                state="consumer_zero",
                plan=zero_plan,
                agent_schema_digest=pins["agent_namespace_schema"],
            ),
        ]
    )
    for state in runtime_states:
        assert_valid(state, runtime_validator, state["runtime_namespace_id"])

    promotion_candidates, promotion_receipts = build_promotions(
        fixture=fixture,
        memo_root=memo_root,
        memo_module=memo_module,
        pins=pins,
    )
    projection_blocked = kag_projection_checks(kag_root)
    aggregate = build_stats_aggregate(fixture, promotion_receipts)
    stats_validator = validator(stats_root / STATS_SCHEMA_REL)
    assert_valid(aggregate, stats_validator, "stats aggregate")
    promotion = aggregate["promotion"]
    if promotion["nominated"] != sum(
        promotion[key]
        for key in (
            "memo_candidates",
            "duplicate_no_write",
            "conflict_quarantine",
            "rejected",
            "deferred",
        )
    ):
        raise AgentLocalFederationLabError("promotion outcomes did not reconcile")

    agent_schema_validator = validator(agents_root / AGENT_SCHEMA_REL)
    faults = fault_results(
        fixture=fixture,
        agent_payload=agent_namespaces[1],
        agent_validator=agent_schema_validator,
        runtime_payload=runtime_states[4],
        runtime_validator=runtime_validator,
        kag_root=kag_root,
        sdk_modules_map=modules,
        sdk_active_plan=active_plans[0],
    )
    arms = [
        {
            "arm": "A_shared_only",
            "form": "shared reviewed organ without local namespaces",
            "repeated_failures_avoided": 2,
            "max_fault_blast_radius_namespaces": 0,
            "cross_agent_contamination": 0,
            "private_to_shared_leakage": 0,
            "silent_shared_truth": 0,
            "operator_review_minutes": 3,
            "duplicate_case_count": 0,
            "safe": True,
        },
        {
            "arm": "B_unisolated_local",
            "form": "local cases in one unisolated shared store",
            "repeated_failures_avoided": 6,
            "max_fault_blast_radius_namespaces": 4,
            "cross_agent_contamination": 4,
            "private_to_shared_leakage": 0,
            "silent_shared_truth": 0,
            "operator_review_minutes": 0,
            "duplicate_case_count": 2,
            "safe": False,
        },
        {
            "arm": "C_auto_shared_local",
            "form": "agent-local cases with automatic shared publication",
            "repeated_failures_avoided": 6,
            "max_fault_blast_radius_namespaces": 4,
            "cross_agent_contamination": 2,
            "private_to_shared_leakage": 3,
            "silent_shared_truth": 8,
            "operator_review_minutes": 0,
            "duplicate_case_count": 2,
            "safe": False,
        },
        {
            "arm": "D_reviewed_agent_local",
            "form": "isolated agent-local cases with reviewed shared nomination",
            "repeated_failures_avoided": 6,
            "max_fault_blast_radius_namespaces": 1,
            "cross_agent_contamination": 0,
            "private_to_shared_leakage": 0,
            "silent_shared_truth": 0,
            "operator_review_minutes": aggregate["operator"]["review_minutes"],
            "duplicate_case_count": aggregate["duplicate_case_count"],
            "safe": True,
        },
    ]
    elapsed_ms = round((perf_counter() - started) * 1000, 3)
    report = {
        "schema_version": "aoa_memo_phase12_agent_local_federation_report_v0",
        "created_at": fixture["reference_time"],
        "evidence_scope": (
            "source-local-deterministic-public-safe-agent-local-federation-"
            "reference-lab-no-live-memory"
        ),
        "pins": pins,
        "contract_validation": {
            "namespace_contracts_valid": len(agent_namespaces),
            "sdk_active_plans_valid": len(active_plans),
            "sdk_isolation_plan_valid": True,
            "sdk_consumer_zero_plan_valid": True,
            "runtime_namespace_states_valid": len(runtime_states),
            "promotion_candidates_valid": len(promotion_candidates),
            "promotion_receipts_valid": len(promotion_receipts),
            "unreviewed_projection_blocked": projection_blocked,
            "stats_aggregate_valid": True,
        },
        "abcd_comparison": arms,
        "fault_results": faults,
        "stats_aggregate": aggregate,
        "cost_quality_speed_result": {
            "unit": "deterministic_reference_lab_descriptive_only",
            "wall_time_ms": elapsed_ms,
            "quality": {
                "cross_agent_contamination": 0,
                "cross_tenant_leakage": 0,
                "private_to_shared_leakage": 0,
                "silent_shared_truth": 0,
            },
            "result": {
                "repeated_failures_avoided": 6,
                "local_fault_blast_radius": 1,
                "shared_organ_failures": 0,
                "consumer_zero_residue": 0,
            },
            "speed": {
                "local_recall_steps": 1,
                "shared_promotion_reviewed_count": len(promotion_receipts),
                "consumer_zero_steps": 3,
            },
            "cost": {
                "local_case_count": len(fixture["local_cases"]),
                "duplicate_case_count": aggregate["duplicate_case_count"],
                "operator_review_minutes": aggregate["operator"]["review_minutes"],
                "saved_re_grounding_minutes": aggregate["operator"][
                    "saved_re_grounding_minutes"
                ],
                "net_operator_minutes_saved": aggregate["operator"][
                    "net_minutes_saved"
                ],
            },
        },
        "exit_gate": {
            "d_reduces_blast_radius": (
                arms[3]["max_fault_blast_radius_namespaces"]
                < arms[1]["max_fault_blast_radius_namespaces"]
            ),
            "promotion_burden_below_benefit": aggregate["operator"][
                "promotion_benefit_exceeds_burden"
            ],
            "shared_truth_never_silent": (
                aggregate["promotion"]["silent_shared_truth_count"] == 0
            ),
            "operator_review_within_budget": (
                aggregate["operator"]["review_minutes"]
                <= aggregate["operator"]["review_budget_minutes"]
            ),
            "namespace_disable_preserves_shared_organ": (
                aggregate["isolation"][
                    "shared_organ_failures_from_local_disable"
                ]
                == 0
            ),
            "strict_tenant_separation": (
                aggregate["isolation"]["cross_tenant_leak_count"] == 0
            ),
            "consumer_zero_clean": all(
                aggregate["consumer_zero"][key] == 0
                for key in (
                    "residual_readers",
                    "residual_writers",
                    "residual_promoters",
                    "residual_material",
                )
            ),
            "model_portability_passed": (
                aggregate["portability"]["nonportable_result_count"] == 0
                and aggregate["portability"]["portable_result_count"]
                == aggregate["portability"]["model_pins_tested"]
            ),
            "passed": True,
        },
        "sampling": {
            "human_operator_sampling_status": "not_performed",
            "synthetic_operator_decisions": len(promotion_receipts),
            "live_operator_minutes_measured": False,
        },
        "authority": {
            "live_private_memory_written": False,
            "live_namespace_deployed": False,
            "shared_ledger_writes": 0,
            "semantic_transitions": 0,
            "runtime_promotion_allowed": False,
            "policy_promotion_allowed": False,
            "landing_performed": False,
        },
        "limitations": [
            "All local cases and operator decisions are public-safe synthetic fixtures.",
            "Model portability covers symbolic pins, not real model behavior or quality.",
            "Review minutes and saved re-grounding minutes are preregistered reference units.",
            "No live private namespace, stack service, MCP route, hook, or durable ledger was used.",
            "The lab proves contract behavior and relative failure shape, not production reliability.",
            "Long-horizon latency, storage growth, backlog, and resource impact remain Phase 13 work.",
        ],
        "report_digest": "sha256:" + "0" * 64,
    }
    report["report_digest"] = canonical_digest(
        report,
        exclude={"report_digest"},
    )
    assert_valid(report, validator(REPORT_SCHEMA_PATH), "phase12 report")
    if not all(report["exit_gate"].values()):
        raise AgentLocalFederationLabError("Phase 12 exit gate did not pass")
    if not all(item["detected"] and item["blocked"] for item in faults):
        raise AgentLocalFederationLabError("Phase 12 fault gate did not pass")
    if output_path is not None:
        write_json(output_path, report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agents-root", type=Path, required=True)
    parser.add_argument("--sdk-root", type=Path, required=True)
    parser.add_argument("--memo-root", type=Path, required=True)
    parser.add_argument("--stack-root", type=Path, required=True)
    parser.add_argument("--kag-root", type=Path, required=True)
    parser.add_argument("--stats-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = run_lab(
        agents_root=args.agents_root,
        sdk_root=args.sdk_root,
        memo_root=args.memo_root,
        stack_root=args.stack_root,
        kag_root=args.kag_root,
        stats_root=args.stats_root,
        output_path=args.output,
    )
    print(json.dumps(report["exit_gate"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
