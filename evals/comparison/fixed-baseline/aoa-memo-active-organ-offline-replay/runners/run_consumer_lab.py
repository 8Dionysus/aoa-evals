#!/usr/bin/env python3
"""Run the source-local Phase 5 Codex owner-orientation comparison."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import random
import re
import statistics
import sys
import time
from typing import Any, Sequence

from jsonschema import Draft202012Validator, FormatChecker


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = BUNDLE_ROOT / "fixtures" / "consumer-orientation-cases.json"
CONSUMER_REPORT_SCHEMA_PATH = (
    BUNDLE_ROOT / "reports" / "consumer-orientation.schema.json"
)
SEEDS = (101, 211, 307)
PLANNED_AT = datetime(2026, 7, 29, 9, 0, tzinfo=timezone.utc)
PRODUCED_AT = "2026-07-29T09:01:00Z"
OBSERVED_AT = "2026-07-29T09:02:00Z"
EXPIRED_AT = "2026-07-29T12:00:00Z"
PROFILE_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "examples/codex_owner_orientation_v0.consumer-profile.json"
)
POLICY_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "examples/codex_owner_orientation_v0.influence-policy.json"
)
MEMO_PIN_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "examples/codex_owner_orientation_v0.sdk-compatibility-pin.json"
)
MEMO_BUILDER_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "scripts/codex_owner_orientation_packet.py"
)
SDK_PLAN_SCHEMA_RELATIVE = (
    "mechanics/boundary-bridge/parts/consumed-surface-posture-gate/"
    "schemas/codex-owner-orientation-plan-v0.schema.json"
)
STACK_PIN_RELATIVE = (
    "mechanics/federation-seams/parts/memo-seam/examples/"
    "codex_owner_orientation_runtime_compatibility_pin_v0.json"
)
STACK_C20_RELATIVE = (
    "mechanics/federation-seams/parts/memo-seam/schemas/"
    "active-organ-runtime-delivery-receipt.schema.json"
)
HOST_EXAMPLES_RELATIVE = (
    "mechanics/host-facts/examples/active_organ_host_contracts_v1.examples.json"
)
SDK_REGISTRY_RELATIVE = "src/aoa_sdk/memo/registry.py"
SDK_DEPENDENCY_MANIFEST_RELATIVE = "pyproject.toml"
STACK_CORE_RELATIVE = "mcp/services/aoa-memo-mcp/src/aoa_memo_mcp/core.py"


class ConsumerLabError(RuntimeError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConsumerLabError(f"{path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ConsumerLabError(f"{path}: expected JSON object")
    return value


def file_digest(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def normalized_report_digest(report: dict[str, Any]) -> str:
    return canonical_digest(
        {
            key: value
            for key, value in report.items()
            if key != "report_digest"
        }
    )


def validate_consumer_report(report: dict[str, Any]) -> None:
    schema = load_json(CONSUMER_REPORT_SCHEMA_PATH)
    errors = sorted(
        Draft202012Validator(
            schema,
            format_checker=FormatChecker(),
        ).iter_errors(report),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        error = errors[0]
        location = ".".join(str(item) for item in error.absolute_path) or "<root>"
        raise ConsumerLabError(
            f"consumer report schema violation at {location}: {error.message}"
        )
    expected = normalized_report_digest(report)
    if report.get("report_digest") != expected:
        raise ConsumerLabError(
            "consumer report digest mismatch: "
            f"{report.get('report_digest')} != {expected}"
        )


def percentile(values: Sequence[float], quantile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return float(ordered[0])
    position = (len(ordered) - 1) * quantile
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return float(ordered[lower] * (1 - weight) + ordered[upper] * weight)


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9_-]+", text.casefold())


def lexical_score(query: str, path: str, content: str) -> int:
    lowered = f"{path}\n{content}".casefold()
    query_text = query.casefold().strip()
    score = 40 if query_text and query_text in lowered else 0
    for token in tokens(query):
        if token in lowered:
            score += 10
    return score


def resolve_source_ref(
    source_ref: str,
    *,
    memo_root: Path,
    stack_root: Path,
) -> Path:
    clean = source_ref.split("#", 1)[0]
    if clean.startswith("repo:"):
        owner_and_path = clean.removeprefix("repo:")
        owner, relative = owner_and_path.split("/", 1)
        if owner == "aoa-memo":
            root = memo_root
        elif owner == "abyss-stack":
            root = stack_root
        else:
            raise ConsumerLabError(f"unsupported baseline source owner: {owner}")
        path = (root / relative).resolve()
        if not path.is_relative_to(root):
            raise ConsumerLabError(f"source ref escaped owner root: {source_ref}")
        return path
    path = (memo_root / clean).resolve()
    if not path.is_relative_to(memo_root):
        raise ConsumerLabError(f"source ref escaped aoa-memo: {source_ref}")
    return path


def source_baseline(
    query: str,
    cases: list[dict[str, Any]],
    *,
    memo_root: Path,
    stack_root: Path,
) -> dict[str, Any]:
    started = time.perf_counter()
    candidates = []
    bytes_scanned = 0
    for case in cases:
        path = resolve_source_ref(
            case["baseline_source_ref"],
            memo_root=memo_root,
            stack_root=stack_root,
        )
        if not path.is_file():
            raise ConsumerLabError(f"baseline source is missing: {path}")
        content = path.read_text(encoding="utf-8")
        encoded_size = len(content.encode("utf-8"))
        bytes_scanned += encoded_size
        candidates.append(
            {
                "object_id": case["expected_object_id"],
                "source_ref": case["baseline_source_ref"],
                "source_path": path,
                "content": content,
                "score": lexical_score(
                    query,
                    case["baseline_source_ref"],
                    content,
                ),
                "bytes": encoded_size,
            }
        )
    candidates.sort(key=lambda item: (-item["score"], item["object_id"]))
    elapsed_ms = (time.perf_counter() - started) * 1000
    selected = candidates[0]
    return {
        "selected_object_id": selected["object_id"],
        "source_ref": selected["source_ref"],
        "source_current": selected["source_path"].is_file(),
        "estimated_context_tokens": max(1, (selected["bytes"] + 3) // 4),
        "bytes_scanned": bytes_scanned,
        "filesystem_reads": len(candidates),
        "operator_attention_units": 1,
        "latency_ms": elapsed_ms,
    }


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ConsumerLabError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def import_owner_implementations(
    *,
    sdk_root: Path,
    memo_root: Path,
    stack_root: Path,
) -> dict[str, Any]:
    sdk_src = str(sdk_root / "src")
    stack_src = str(stack_root / "mcp/services/aoa-memo-mcp/src")
    for path in (sdk_src, stack_src):
        if path not in sys.path:
            sys.path.insert(0, path)
    os.environ["AOA_SDK_REPO_PATH_AOA_MEMO"] = str(memo_root)
    os.environ["AOA_ABYSS_STACK_ROOT"] = str(stack_root)

    from aoa_sdk import AoASDK
    from aoa_sdk.contracts.control_plane import ProvenanceRef
    from aoa_sdk.contracts.memo import (
        ActiveOrganAnchorFreshness,
        ActiveOrganPolicyPin,
        CodexOwnerOrientationProfile,
        RecallIntent,
    )
    from aoa_memo_mcp.core import AoAMemoMCPState

    memo_builder = load_module(
        "aoa_memo_owner_orientation_packet",
        memo_root / MEMO_BUILDER_RELATIVE,
    )
    return {
        "AoASDK": AoASDK,
        "ProvenanceRef": ProvenanceRef,
        "ActiveOrganAnchorFreshness": ActiveOrganAnchorFreshness,
        "ActiveOrganPolicyPin": ActiveOrganPolicyPin,
        "CodexOwnerOrientationProfile": CodexOwnerOrientationProfile,
        "RecallIntent": RecallIntent,
        "AoAMemoMCPState": AoAMemoMCPState,
        "memo_builder": memo_builder,
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


def build_intent(
    types: dict[str, Any],
    *,
    case_id: str,
    recall_mode: str,
    seed: int,
    memo_root: Path,
    machine_root: Path,
    profile: Any,
):
    host_examples = machine_root / HOST_EXAMPLES_RELATIVE
    host_digest = file_digest(host_examples)
    anchor_path = memo_root / "MEMORY_INDEX.md"
    anchor_ref = provenance_ref(
        types,
        owner_repo="aoa-memo",
        artifact_ref="MEMORY_INDEX.md",
        source_ref="repo:aoa-memo/MEMORY_INDEX.md",
        artifact_digest=file_digest(anchor_path),
        schema_ref="docs/memory/MEMORY_MODEL.md",
        schema_version="active-organ-phase5-candidate",
    )
    c18 = provenance_ref(
        types,
        owner_repo="abyss-machine",
        artifact_ref=f"C18:{HOST_EXAMPLES_RELATIVE}",
        source_ref=f"repo:abyss-machine/{HOST_EXAMPLES_RELATIVE}#C18-current",
        artifact_digest=host_digest,
        schema_ref="schemas/active-organ-host-capability-snapshot-reference.schema.json",
        schema_version="1.0.0",
    )
    c19 = provenance_ref(
        types,
        owner_repo="abyss-machine",
        artifact_ref=f"C19:{HOST_EXAMPLES_RELATIVE}",
        source_ref=f"repo:abyss-machine/{HOST_EXAMPLES_RELATIVE}#C19-start",
        artifact_digest=host_digest,
        schema_ref="schemas/active-organ-host-resource-storage-plan-reference.schema.json",
        schema_version="1.0.0",
    )
    return types["RecallIntent"](
        intent_id=f"intent:consumer-lab:{case_id}:{seed}",
        idempotency_key=f"intent:consumer-lab:{case_id}:{seed}",
        trigger_id="operator-explicit-pull",
        anchor_id=f"repo:aoa-memo:{case_id}:{seed}",
        anchor_ref=anchor_ref,
        anchor_freshness=types["ActiveOrganAnchorFreshness"](
            observed_at=PLANNED_AT,
            valid_at=PLANNED_AT,
            expires_at=datetime(2026, 7, 29, 12, 0, tzinfo=timezone.utc),
        ),
        consumer_id=profile.consumer_id,
        tenant_id="owner-local",
        model_prompt_provider_pin=profile.model_prompt_provider_pin,
        data_class="D0",
        risk_class="R1",
        mode="explicit_public_pull",
        recall_mode=recall_mode,
        requested_scopes=("workspace",),
        policy_pin=types["ActiveOrganPolicyPin"](
            policy_id=profile.influence_policy.policy_id,
            policy_version=profile.influence_policy.policy_version,
            decision_ref="decision:aoa-memo-active-organ-phase1-v1",
            policy_digest=profile.influence_policy.sha256,
        ),
        source_refs=(c18, c19),
        requested_at=PLANNED_AT,
        expires_at=datetime(2026, 7, 29, 12, 0, tzinfo=timezone.utc),
    )


def run_consumer_lab(
    *,
    sdk_root: Path,
    memo_root: Path,
    stack_root: Path,
    machine_root: Path,
    seeds: Sequence[int],
) -> dict[str, Any]:
    for label, root in (
        ("aoa-sdk", sdk_root),
        ("aoa-memo", memo_root),
        ("abyss-stack", stack_root),
        ("abyss-machine", machine_root),
    ):
        if not root.is_dir():
            raise ConsumerLabError(f"{label} root is unavailable: {root}")
    fixture = load_json(CASES_PATH)
    cases = fixture.get("cases")
    if not isinstance(cases, list) or len(cases) < 8:
        raise ConsumerLabError("consumer lab requires at least eight cases")
    case_ids = [case.get("case_id") for case in cases]
    if len(case_ids) != len(set(case_ids)):
        raise ConsumerLabError("consumer case ids must be unique")
    allowed_recall_modes = {
        "semantic",
        "episodic",
        "procedural",
        "lineage",
        "source_route",
    }
    invalid_modes = [
        case.get("recall_mode")
        for case in cases
        if case.get("recall_mode") not in allowed_recall_modes
    ]
    if invalid_modes:
        raise ConsumerLabError(
            f"consumer cases require explicit valid recall modes: {invalid_modes}"
        )
    if len(seeds) < 3 or len(set(seeds)) != len(seeds):
        raise ConsumerLabError("consumer lab requires at least three unique seeds")

    types = import_owner_implementations(
        sdk_root=sdk_root,
        memo_root=memo_root,
        stack_root=stack_root,
    )
    profile_path = memo_root / PROFILE_RELATIVE
    policy_path = memo_root / POLICY_RELATIVE
    memo_pin_path = memo_root / MEMO_PIN_RELATIVE
    plan_schema_path = sdk_root / SDK_PLAN_SCHEMA_RELATIVE
    profile_payload = load_json(profile_path)
    policy_payload = load_json(policy_path)
    memo_pin = load_json(memo_pin_path)
    plan_schema = load_json(plan_schema_path)
    profile = types["CodexOwnerOrientationProfile"].model_validate(
        profile_payload
    )
    profile_ref = provenance_ref(
        types,
        owner_repo="aoa-memo",
        artifact_ref=PROFILE_RELATIVE,
        source_ref=f"repo:aoa-memo/{PROFILE_RELATIVE}",
        artifact_digest=file_digest(profile_path),
        schema_ref=(
            "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
            "schemas/codex_owner_orientation_profile_v0.schema.json"
        ),
        schema_version=profile.schema_version,
    )
    sdk = types["AoASDK"].from_workspace(sdk_root)
    stack = types["AoAMemoMCPState"].discover(stack_root.parent)

    observations = []
    rollback_observations = []
    for seed in seeds:
        ordered = list(cases)
        random.Random(seed).shuffle(ordered)
        for case in ordered:
            baseline = source_baseline(
                case["query"],
                cases,
                memo_root=memo_root,
                stack_root=stack_root,
            )
            intent = build_intent(
                types,
                case_id=case["case_id"],
                recall_mode=case["recall_mode"],
                seed=seed,
                memo_root=memo_root,
                machine_root=machine_root,
                profile=profile,
            )
            started = time.perf_counter()
            plan = sdk.memo.plan_owner_orientation(
                intent=intent,
                profile=profile,
                profile_ref=profile_ref,
                consumer_mode="bounded",
                query=case["query"],
                planned_at=PLANNED_AT,
            )
            plan_payload = plan.model_dump(mode="json")
            bundle = types["memo_builder"].build_owner_orientation_bundle(
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
            delivery = stack.deliver_owner_orientation(
                plan=plan_payload,
                memo_bundle=bundle,
                observed_at=OBSERVED_AT,
                target_ref=f"codex:consumer-lab:{case['case_id']}:{seed}",
            )
            active_latency_ms = (time.perf_counter() - started) * 1000
            selected = (
                delivery["memory_payload"][0]
                if delivery["memory_payload"]
                else None
            )
            expected = case["expected_object_id"]
            baseline_correct = baseline["selected_object_id"] == expected
            active_correct = (
                selected is not None and selected["object_id"] == expected
            )
            source_path = resolve_source_ref(
                selected["source_route"] if selected else "",
                memo_root=memo_root,
                stack_root=stack_root,
            ) if selected else None
            observations.append(
                {
                    "seed": seed,
                    "case_id": case["case_id"],
                    "recall_mode": case["recall_mode"],
                    "expected_object_id": expected,
                    "baseline": {
                        **{
                            key: value
                            for key, value in baseline.items()
                            if key != "source_path"
                        },
                        "correct": baseline_correct,
                        "current": (
                            baseline_correct and baseline["source_current"]
                        ),
                    },
                    "active": {
                        "selected_object_id": (
                            selected["object_id"] if selected else None
                        ),
                        "source_route": (
                            selected["source_route"] if selected else None
                        ),
                        "query_digest": plan_payload["query_digest"],
                        "recall_intent_id": plan_payload["recall_intent"][
                            "intent_id"
                        ],
                        "recall_intent_digest": canonical_digest(
                            plan_payload["recall_intent"]
                        ),
                        "plan_digest": plan_payload["plan_digest"],
                        "recall_packet_ref": bundle["recall_packet"][
                            "instance_id"
                        ],
                        "recall_packet_digest": bundle["recall_packet"][
                            "content_digest"
                        ],
                        "intervention_decision_ref": bundle[
                            "intervention_decision"
                        ]["instance_id"],
                        "intervention_decision_digest": bundle[
                            "intervention_decision"
                        ]["content_digest"],
                        "runtime_receipt_id": delivery["runtime_receipt"][
                            "receipt_id"
                        ],
                        "runtime_receipt_digest": canonical_digest(
                            delivery["runtime_receipt"]
                        ),
                        "correct": active_correct,
                        "current": bool(
                            active_correct
                            and selected["current_recall_status"]
                            in {"preferred", "allowed"}
                            and source_path is not None
                            and source_path.is_file()
                        ),
                        "source_route_correct": bool(
                            selected
                            and selected["source_route"]
                            == case["baseline_source_ref"]
                        ),
                        "estimated_context_tokens": sum(
                            item["estimated_tokens"]
                            for item in plan_payload["items"]
                        ),
                        "bytes_scanned": sum(
                            (
                                memo_root / ref["artifact_ref"]
                            ).stat().st_size
                            for ref in (
                                plan_payload["memory_object_catalog_ref"],
                                plan_payload["memory_object_capsules_ref"],
                            )
                        ),
                        "filesystem_reads": 2,
                        "operator_attention_units": (
                            1 if selected is not None else 0
                        ),
                        "latency_ms": active_latency_ms,
                        "delivery_state": delivery["delivery_state"],
                        "c20_reason": delivery["runtime_receipt"]["result"][
                            "reason_code"
                        ],
                        "unsafe_authority_count": int(
                            delivery["effect_authority"] != "none"
                            or delivery["action_use"] != "forbidden"
                            or delivery["persistence_performed"]
                            or delivery["reranking_performed"]
                            or delivery["reselection_performed"]
                        ),
                    },
                }
            )

        rollback_case = ordered[0]
        intent = build_intent(
            types,
            case_id=f"{rollback_case['case_id']}-rollback",
            recall_mode=rollback_case["recall_mode"],
            seed=seed,
            memo_root=memo_root,
            machine_root=machine_root,
            profile=profile,
        )
        rollback_started = time.perf_counter()
        off_plan = sdk.memo.plan_owner_orientation(
            intent=intent,
            profile=profile,
            profile_ref=profile_ref,
            consumer_mode="off",
            query=rollback_case["query"],
            planned_at=PLANNED_AT,
        )
        off_payload = off_plan.model_dump(mode="json")
        off_bundle = types["memo_builder"].build_owner_orientation_bundle(
            plan=off_payload,
            plan_schema=plan_schema,
            plan_schema_path=plan_schema_path,
            profile=profile_payload,
            profile_path=profile_path,
            policy=policy_payload,
            policy_path=policy_path,
            compatibility_pin=memo_pin,
            produced_at=PRODUCED_AT,
        )
        off_delivery = stack.deliver_owner_orientation(
            plan=off_payload,
            memo_bundle=off_bundle,
            observed_at=OBSERVED_AT,
            target_ref=f"codex:consumer-lab:rollback:{seed}",
        )
        rollback_observations.append(
            {
                "seed": seed,
                "latency_ms": (
                    time.perf_counter() - rollback_started
                )
                * 1000,
                "status": off_payload["status"],
                "delivery_state": off_delivery["delivery_state"],
                "memory_payload_count": len(off_delivery["memory_payload"]),
                "reason": off_delivery["runtime_receipt"]["result"][
                    "reason_code"
                ],
                "passed": (
                    off_payload["status"] == "off"
                    and off_delivery["delivery_state"] == "suppressed"
                    and not off_delivery["memory_payload"]
                    and not off_delivery["persistence_performed"]
                ),
            }
        )

    def arm_summary(name: str) -> dict[str, Any]:
        rows = [observation[name] for observation in observations]
        return {
            "observation_count": len(rows),
            "outcome_rate": statistics.fmean(
                float(row["correct"]) for row in rows
            ),
            "currentness_rate": statistics.fmean(
                float(row["current"]) for row in rows
            ),
            "source_route_rate": (
                statistics.fmean(
                    float(row.get("source_route_correct", False))
                    for row in rows
                )
                if name == "active"
                else 1.0
            ),
            "mean_latency_ms": statistics.fmean(
                row["latency_ms"] for row in rows
            ),
            "p95_latency_ms": percentile(
                [row["latency_ms"] for row in rows],
                0.95,
            ),
            "mean_estimated_context_tokens": statistics.fmean(
                row["estimated_context_tokens"] for row in rows
            ),
            "mean_bytes_scanned": statistics.fmean(
                row["bytes_scanned"] for row in rows
            ),
            "mean_filesystem_reads": statistics.fmean(
                row["filesystem_reads"] for row in rows
            ),
            "mean_operator_attention_units": statistics.fmean(
                row["operator_attention_units"] for row in rows
            ),
            "unsafe_authority_count": sum(
                row.get("unsafe_authority_count", 0) for row in rows
            ),
        }

    baseline_summary = arm_summary("baseline")
    active_summary = arm_summary("active")
    rollback_passed = all(item["passed"] for item in rollback_observations)
    exit_gate = (
        active_summary["outcome_rate"] >= baseline_summary["outcome_rate"]
        and active_summary["currentness_rate"]
        >= baseline_summary["currentness_rate"]
        and active_summary["source_route_rate"] == 1.0
        and active_summary["p95_latency_ms"] <= 500.0
        and active_summary["mean_estimated_context_tokens"] <= 900.0
        and active_summary["unsafe_authority_count"] == 0
        and rollback_passed
    )
    report = {
        "schema_version": "codex_owner_orientation_consumer_report_v0",
        "created_at": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "consumer_id": "codex_owner_orientation_v0",
        "evidence_scope": "source-local-production-like-no-deployment",
        "case_fixture": {
            "case_count": len(cases),
            "sha256": file_digest(CASES_PATH),
        },
        "seeds": list(seeds),
        "pins": {
            "consumer_report_schema": file_digest(
                CONSUMER_REPORT_SCHEMA_PATH
            ),
            "consumer_runner": file_digest(Path(__file__)),
            "consumer_fixture": file_digest(CASES_PATH),
            "sdk_plan_schema": file_digest(plan_schema_path),
            "sdk_registry": file_digest(sdk_root / SDK_REGISTRY_RELATIVE),
            "sdk_dependency_manifest": file_digest(
                sdk_root / SDK_DEPENDENCY_MANIFEST_RELATIVE
            ),
            "memo_profile": file_digest(profile_path),
            "memo_policy": file_digest(policy_path),
            "memo_sdk_compatibility": file_digest(memo_pin_path),
            "memo_packet_builder": file_digest(
                memo_root / MEMO_BUILDER_RELATIVE
            ),
            "stack_runtime_compatibility": file_digest(
                stack_root / STACK_PIN_RELATIVE
            ),
            "stack_c20_schema": file_digest(stack_root / STACK_C20_RELATIVE),
            "stack_delivery_core": file_digest(
                stack_root / STACK_CORE_RELATIVE
            ),
            "host_contract_examples": file_digest(
                machine_root / HOST_EXAMPLES_RELATIVE
            ),
        },
        "arms": {
            "0_verified_current_source_lexical": baseline_summary,
            "A_reviewed_explicit_pull_bounded": active_summary,
        },
        "paired_observations": observations,
        "rollback": {
            "target": "verified-current-no-memory",
            "passed": rollback_passed,
            "observations": rollback_observations,
        },
        "budgets": {
            "p95_latency_ms": 500.0,
            "mean_estimated_context_tokens": 900.0,
            "unsafe_authority_count": 0,
        },
        "exit_gate_passed": exit_gate,
        "verdict": (
            "supports bounded source-local A continuation"
            if exit_gate
            else "does not support bounded source-local A continuation"
        ),
        "authority": {
            "production_authorized": False,
            "deployment_authorized": False,
            "policy_promotion_authorized": False,
            "landing_authorized": False,
            "memory_write_authorized": False,
            "effect_authority": "none",
        },
        "limitations": [
            "Source-local production-like execution is not a deployed Codex hook.",
            "Public reviewed owner-orientation cases are not private-task outcome evidence.",
            "Warm filesystem cache and one host do not establish production latency.",
            "Context-token estimates are deterministic byte estimates, not provider billing.",
            "C20 receipts prove delivery state only, not user benefit.",
        ],
    }
    report["report_digest"] = normalized_report_digest(report)
    validate_consumer_report(report)
    return report


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--sdk-root", type=Path, required=True)
    result.add_argument("--memo-root", type=Path, required=True)
    result.add_argument("--stack-root", type=Path, required=True)
    result.add_argument("--machine-root", type=Path, required=True)
    result.add_argument("--seeds", type=int, nargs="+", default=list(SEEDS))
    result.add_argument("--output", type=Path, required=True)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        report = run_consumer_lab(
            sdk_root=args.sdk_root.resolve(),
            memo_root=args.memo_root.resolve(),
            stack_root=args.stack_root.resolve(),
            machine_root=args.machine_root.resolve(),
            seeds=tuple(args.seeds),
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
    except (ConsumerLabError, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"consumer orientation lab: invalid: {exc}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "ok": report["exit_gate_passed"],
                "output": args.output.as_posix(),
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
