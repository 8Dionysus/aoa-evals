#!/usr/bin/env python3
"""Run the seeded validation-routing peer-comparison contract.

The runner compares activation proposals only.  It never executes repository,
KAG, stats, or advisory validators and it never emits a policy winner.  The
full owner proof route in each fixture is the declared oracle/fallback, while
unbound or invalid owner evidence remains incomplete.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Callable, NamedTuple, Sequence


PART_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_CONTRACT = PART_ROOT / "schemas" / "validation-routing-comparison-v1.contract.json"
DEFAULT_CASES = PART_ROOT / "fixtures" / "validation-routing-bounded-v1" / "cases.json"

REPORT_SCHEMA_VERSION = "validation_routing_comparison_report_v1"
FIXTURE_ID = "validation-routing-bounded-v1"
SEEDED_EVIDENCE_KIND = "seeded_fixture"
REAL_EVIDENCE_KIND = "real_session"
SYNTHETIC_LATENCY_KIND = "synthetic_fixture_proxy"
SYNTHETIC_LATENCY_FIELD = "latency_ms_synthetic_proxy"
IMPLEMENTED_METHOD_IDS = (
    "static_paths",
    "dependency_graph",
    "owner_contracts",
    "history_correlation",
    "claim_risk",
    "hybrid_fail_closed",
)
LATENCY_COMPONENT_METHOD_IDS = IMPLEMENTED_METHOD_IDS[:-1]
UNSUPPORTED_METHOD_STATUS = "unsupported_missing_candidate"
FAILURE_STATES = {"stale", "unknown", "malformed", "wrong_identity", "blocked"}
EXTERNAL_OWNER_NODE = "owner_external_kag"
REQUIRED_ADVERSARIAL_CLASSES = {
    "stale_graph",
    "unknown_dependency",
    "wrong_candidate_environment_receipt",
    "malformed_receipt",
    "unexplained_miss",
    "unbound_external_owner",
}
REQUIRED_UNSUPPORTED_CANDIDATE_IDS = {
    "api_abi",
    "coverage",
    "mutation",
    "kag_relations",
    "llm_proposed_additions",
}
EXPECTED_COMPARISON_IDENTITY_KEYS = {"candidate_set_id", "environment_id"}
EXPECTED_ALLOWED_USE = (
    "bounded prior and route-gap input only; no raw session body or policy verdict copied"
)
EXPECTED_INPUT_EVIDENCE_KEYS = {
    "source_kind",
    "path",
    "sha256",
    "allowed_use",
    "raw_sessions_copied",
    "observed_real_route_gaps",
    "observed_wall_clock_proxies",
}
EXPECTED_WALL_CLOCK_PROXY_KEYS = {
    "full_local_release_check_seconds",
    "targeted_local_route_proxy_seconds",
    "speed_claim_status",
}
EXPECTED_ORACLE_RULE = {
    "oracle": "full_owner_proof",
    "fallback": "full_owner_proof",
    "unknown_rule": "preserve stale, unknown, malformed, and wrong-identity state; escalate without treating it as zero or green",
    "policy_rule": "measurement only; no method winner, release verdict, or routing policy is emitted",
}
EXPECTED_COVERAGE_LIMITS = (
    "All current cases are seeded public-safe fixtures; no real-session case is copied into the fixture.",
    "The validation-shadow report is a bounded prior and input reference, not a verdict or routing policy.",
    "External KAG, canonical aoa-stats, and advisory trust-plane execution receipts remain absent or blocked.",
    "No mutation injection, old-commit checkout, population estimate, causal claim, or universal false-negative rate is supported.",
    "Unsupported candidate families remain explicit missing candidates until owner-bound evidence and a fair implementation exist.",
)
EXPECTED_LATENCY_POLICY = {
    "kind": SYNTHETIC_LATENCY_KIND,
    "runtime_observed": False,
    "field_suffix": "_synthetic_proxy",
    "source": "seeded fixture event declarations",
    "interpretation_limit": "not observed runtime latency or a performance ranking",
}
MAX_RETRY_COUNT = 64
MAX_MATERIALIZED_EVENTS_PER_SIGNAL = 4096
EXPECTED_RESOURCE_POLICY = {
    "kind": "source_owned_retry_materialization_cap",
    "max_retry_count": MAX_RETRY_COUNT,
    "max_materialized_events_per_signal": MAX_MATERIALIZED_EVENTS_PER_SIGNAL,
    "materialization_rule": "target_count * (retry_count + 1) <= max_materialized_events_per_signal",
    "retry_representation": "one_event_per_admitted_attempt",
    "overflow_behavior": "reject_before_event_allocation",
}
EXPECTED_SPEED_CLAIM_STATUS = "rejected_as_final_saving_until_owner_receipts_are bound"

STATIC_PATH_RULES: tuple[tuple[str, str], ...] = (
    ("scripts/", "source_fast"),
    ("generated/", "generated"),
    ("mechanics/", "mechanics_part_local"),
    ("tests/", "behavior_tests"),
)


class ContractError(ValueError):
    """Raised when a fixture or report contract is not safe to compare."""


class OwnerReceiptEvidence(NamedTuple):
    """One receipt-shape classification shared by admission and measurement."""

    state: str
    reason: str
    mismatched_fields: tuple[str, ...] = ()


class NormalizedSignal(NamedTuple):
    """One signal-shape classification shared by admission and measurement."""

    state: str
    nodes: tuple[str, ...]
    normalized_to_blocked: bool


def load_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ContractError(f"{path} must contain a JSON object")
    return payload


def unique_strings(values: Any, *, field: str) -> list[str]:
    if (
        not isinstance(values, list)
        or not values
        or not all(isinstance(value, str) and value for value in values)
    ):
        raise ContractError(f"{field} must be a non-empty string array")
    if len(set(values)) != len(values):
        raise ContractError(f"{field} must not contain duplicates")
    return list(values)


def reject_undeclared_keys(value: dict[str, Any], *, allowed: set[str], field: str) -> None:
    undeclared = sorted(set(value) - allowed)
    if undeclared:
        raise ContractError(
            f"{field} contains undeclared field(s): {', '.join(undeclared)}"
        )


def is_finite_non_negative_number(value: Any) -> bool:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return False
    try:
        numeric = float(value)
    except (OverflowError, TypeError, ValueError):
        return False
    return math.isfinite(numeric) and numeric >= 0


def checked_non_negative_add(total: float, value: Any, *, field: str) -> float:
    if not is_finite_non_negative_number(value):
        raise ContractError(f"{field} must be a finite non-negative number")
    aggregate = total + float(value)
    if not math.isfinite(aggregate):
        raise ContractError(f"{field} aggregate must remain finite")
    return aggregate


def finite_non_negative_sum(values: Sequence[Any], *, field: str) -> float:
    total = 0.0
    for index, value in enumerate(values):
        total = checked_non_negative_add(total, value, field=f"{field}[{index}]")
    return total


def validate_source_owned_coverage_limits(value: Any) -> list[str]:
    coverage_limits = unique_strings(value, field="coverage_limits")
    if coverage_limits != list(EXPECTED_COVERAGE_LIMITS):
        raise ContractError(
            "coverage_limits must exactly preserve the source-owned ordered v1 caveat set"
        )
    return coverage_limits


def ensure_strict_json_finite(value: Any, *, path: str = "report") -> None:
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ContractError(f"{path} contains a non-finite number")
        return
    if isinstance(value, dict):
        for key, nested in value.items():
            ensure_strict_json_finite(nested, path=f"{path}.{key}")
        return
    if isinstance(value, list):
        for index, nested in enumerate(value):
            ensure_strict_json_finite(nested, path=f"{path}[{index}]")


def validate_latency_weights(value: Any) -> dict[str, float]:
    if not isinstance(value, dict) or set(value) != set(LATENCY_COMPONENT_METHOD_IDS):
        expected = ", ".join(LATENCY_COMPONENT_METHOD_IDS)
        raise ContractError(
            "latency_event_weights_ms_synthetic_proxy must declare exactly: " + expected
        )
    if any(not is_finite_non_negative_number(value[method_id]) for method_id in LATENCY_COMPONENT_METHOD_IDS):
        raise ContractError(
            "latency_event_weights_ms_synthetic_proxy values must be finite non-negative numbers"
        )
    return {method_id: float(value[method_id]) for method_id in LATENCY_COMPONENT_METHOD_IDS}


def validate_retry_count(value: Any, *, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ContractError(f"{field} must be a non-negative integer")
    if value > MAX_RETRY_COUNT:
        raise ContractError(
            f"{field} exceeds source-owned retry_count cap {MAX_RETRY_COUNT}"
        )
    return value


def validate_event_materialization_budget(
    target_count: int,
    retry_count: int,
    *,
    existing_count: int = 0,
    field: str,
) -> int:
    if not isinstance(target_count, int) or isinstance(target_count, bool) or target_count < 0:
        raise ContractError(f"{field} target count must be a non-negative integer")
    if not isinstance(existing_count, int) or isinstance(existing_count, bool) or existing_count < 0:
        raise ContractError(f"{field} existing event count must be a non-negative integer")
    validate_retry_count(retry_count, field=f"{field}.retry_count")
    planned_count = target_count * (retry_count + 1)
    total_count = existing_count + planned_count
    if total_count > MAX_MATERIALIZED_EVENTS_PER_SIGNAL:
        raise ContractError(
            f"{field} would materialize {total_count} events; source-owned per-signal budget is "
            f"{MAX_MATERIALIZED_EVENTS_PER_SIGNAL}"
        )
    return planned_count


def static_path_targets(scenario: dict[str, Any]) -> tuple[list[str], list[tuple[str, str]]]:
    activated: list[str] = []
    matched_targets: list[tuple[str, str]] = []
    for changed_path in scenario["changed_paths"]:
        for prefix, node in STATIC_PATH_RULES:
            if changed_path.startswith(prefix):
                if node not in activated:
                    activated.append(node)
                    matched_targets.append((prefix, node))
                break
    overrides = scenario.get("method_overrides")
    if overrides is None:
        overrides = {}
    if not isinstance(overrides, dict):
        raise ContractError("method_overrides must be an object or null")
    override = overrides.get("static_paths", {})
    if not isinstance(override, dict):
        raise ContractError("method_overrides.static_paths must be an object")
    if "activated_nodes" in override:
        raise ContractError(
            "static_paths.activated_nodes overrides are not admitted because events must match activated nodes"
        )
    return activated, matched_targets


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def expected_receipt(scenario: dict[str, Any]) -> dict[str, str]:
    return {
        "workload_id": scenario["workload_id"],
        "candidate_set_id": scenario["candidate_set_id"],
        "environment_id": scenario["environment_id"],
        "source_ref": scenario["source_ref"],
    }


def classify_owner_receipt(scenario: dict[str, Any]) -> OwnerReceiptEvidence:
    """Classify owner evidence from receipt shape and identity, not its label."""
    signals = scenario.get("signals", {})
    signal = signals.get("owner_contracts") if isinstance(signals, dict) else None
    if not isinstance(signal, dict):
        return OwnerReceiptEvidence("unknown", "owner contract signal is not declared")

    declared_state = signal.get("state", "unknown")
    if "receipt" not in signal:
        if declared_state in {"stale", "unknown", "blocked"}:
            reason = signal.get("reason")
            return OwnerReceiptEvidence(
                declared_state,
                str(reason) if reason else f"owner receipt state is {declared_state}",
            )
        return OwnerReceiptEvidence("malformed", "owner receipt is not declared")

    receipt = signal.get("receipt")
    if not isinstance(receipt, dict):
        return OwnerReceiptEvidence("malformed", "owner receipt is not an object")
    expected = expected_receipt(scenario)
    missing = sorted(set(expected) - set(receipt))
    if missing:
        return OwnerReceiptEvidence(
            "malformed", "owner receipt omitted identity field(s): " + ", ".join(missing)
        )
    mismatched = sorted(
        key for key, value in expected.items() if receipt.get(key) != value
    )
    if mismatched:
        return OwnerReceiptEvidence(
            "wrong_identity",
            "owner receipt identity mismatched: " + ", ".join(mismatched),
            tuple(mismatched),
        )
    if declared_state != "valid":
        return OwnerReceiptEvidence(
            "valid",
            "owner receipt shape and identity are valid; ignored declared state "
            f"{declared_state!r}",
        )
    return OwnerReceiptEvidence("valid", "owner receipt shape and identity matched")


def owner_contract_signal_state(scenario: dict[str, Any]) -> str:
    """Expose the normalized owner signal state to admission checks."""
    signals = scenario.get("signals", {})
    raw_signal = signals.get("owner_contracts") if isinstance(signals, dict) else None
    signal = dict(raw_signal) if isinstance(raw_signal, dict) else {}
    evidence = classify_owner_receipt(scenario)
    signal["state"] = evidence.state
    signal["reason"] = evidence.reason
    return normalize_signal(
        signal,
        method_id="owner_contracts",
        expected_state="valid",
    ).state


def normalize_signal(
    signal: Any, *, method_id: str, expected_state: str
) -> NormalizedSignal:
    """Normalize signal state and node shape before any consumer interprets it."""
    if not isinstance(signal, dict):
        signal = {"state": "unknown"}
    raw_state = signal.get("state", "unknown")
    normalized_to_blocked = not (
        raw_state == expected_state
        or (isinstance(raw_state, str) and raw_state in FAILURE_STATES)
    )
    state = "blocked" if normalized_to_blocked else raw_state
    nodes = signal.get("nodes", [])
    if not isinstance(nodes, list) or not all(isinstance(node, str) and node for node in nodes):
        return NormalizedSignal("malformed", (), normalized_to_blocked)
    if len(set(nodes)) != len(nodes):
        raise ContractError(f"{method_id}.nodes must not contain duplicates")
    return NormalizedSignal(state, tuple(nodes), normalized_to_blocked)


def adversarial_class_matches(scenario: dict[str, Any], adversarial_class: str) -> bool:
    """Credit a class only when its complete measured condition is present."""
    signals = scenario.get("signals", {})
    dependency_graph = signals.get("dependency_graph") if isinstance(signals, dict) else None
    dependency_state = normalize_signal(
        dependency_graph,
        method_id="dependency_graph",
        expected_state="current",
    ).state

    if adversarial_class == "stale_graph":
        return dependency_state == "stale"
    if adversarial_class == "unknown_dependency":
        return dependency_state == "unknown"
    if adversarial_class == "wrong_candidate_environment_receipt":
        evidence = classify_owner_receipt(scenario)
        return owner_contract_signal_state(scenario) == "wrong_identity" and bool(
            set(evidence.mismatched_fields)
            & {"candidate_set_id", "environment_id"}
        )
    if adversarial_class == "malformed_receipt":
        return owner_contract_signal_state(scenario) == "malformed"
    if adversarial_class == "unbound_external_owner":
        oracle = scenario["oracle"]
        required_nodes = oracle.get("required_nodes")
        owner_proof_nodes = oracle.get("owner_proof_nodes")
        return (
            oracle.get("complete") is False
            and oracle.get("owner_proof_status") == "unknown"
            and owner_contract_signal_state(scenario) == "unknown"
            and isinstance(required_nodes, list)
            and isinstance(owner_proof_nodes, list)
            and EXTERNAL_OWNER_NODE in required_nodes
            and EXTERNAL_OWNER_NODE in owner_proof_nodes
        )
    if adversarial_class == "unexplained_miss":
        activated, _matched_targets = static_path_targets(scenario)
        required = set(scenario["oracle"]["required_nodes"])
        missing = required - set(activated)
        explanations = {}
        return bool(
            missing
            and any(
                not isinstance(explanations.get(node), str) or not explanations[node].strip()
                for node in missing
            )
        )
    raise ContractError(f"unsupported adversarial class predicate: {adversarial_class!r}")


def validate_contract(contract: dict[str, Any]) -> None:
    if contract.get("schema_version") != "validation_routing_comparison_contract_v1":
        raise ContractError("contract schema_version must be validation_routing_comparison_contract_v1")
    if contract.get("fixture_id") != FIXTURE_ID:
        raise ContractError(f"contract fixture_id must be {FIXTURE_ID}")
    if contract.get("comparison_mode") != "peer-compare":
        raise ContractError("validation-routing contract must remain a peer-compare support artifact")
    if contract.get("claim_posture") != "measurement_only":
        raise ContractError("validation-routing contract must declare claim_posture=measurement_only")
    identity_fields = unique_strings(contract.get("identity_fields"), field="identity_fields")
    if identity_fields != ["workload_id", "candidate_set_id", "environment_id", "source_ref"]:
        raise ContractError("identity_fields must preserve the four comparison identity dimensions")

    evidence_policy = contract.get("evidence_policy")
    if not isinstance(evidence_policy, dict):
        raise ContractError("evidence_policy must declare the current evidence admission posture")
    if evidence_policy.get("source_posture") != "seeded_public_safe_only":
        raise ContractError("evidence_policy must declare seeded_public_safe_only")
    accepted_evidence_kinds = unique_strings(
        evidence_policy.get("accepted_evidence_kinds"),
        field="evidence_policy.accepted_evidence_kinds",
    )
    if accepted_evidence_kinds != [SEEDED_EVIDENCE_KIND]:
        raise ContractError(
            "validation-routing comparison v1 admits seeded_fixture evidence only"
        )
    if evidence_policy.get("report_kind") != "seeded_validation_routing_method_measurement":
        raise ContractError("evidence_policy.report_kind must describe a seeded report")
    if evidence_policy.get("real_evidence_status") != "not_admitted_in_v1":
        raise ContractError("evidence_policy must keep real evidence outside this seeded version")
    if evidence_policy.get("allowed_use") != EXPECTED_ALLOWED_USE:
        raise ContractError(
            "evidence_policy.allowed_use must preserve the source-owned measurement-only posture"
        )

    latency_policy = contract.get("latency_policy")
    if not isinstance(latency_policy, dict):
        raise ContractError("latency_policy must declare the latency evidence semantics")
    if latency_policy.get("kind") != SYNTHETIC_LATENCY_KIND:
        raise ContractError("validation-routing v1 requires synthetic fixture proxy latency")
    if latency_policy.get("runtime_observed") is not False:
        raise ContractError("synthetic fixture proxy latency must not be marked runtime observed")
    if latency_policy.get("field_suffix") != "_synthetic_proxy":
        raise ContractError("synthetic latency fields must retain their explicit field suffix")
    if latency_policy != EXPECTED_LATENCY_POLICY:
        raise ContractError(
            "latency_policy must preserve the complete synthetic fixture proxy v1 posture"
        )
    resource_policy = contract.get("resource_policy")
    if resource_policy != EXPECTED_RESOURCE_POLICY:
        raise ContractError(
            "resource_policy must preserve the source-owned retry materialization boundary"
        )

    if contract.get("oracle_rule") != EXPECTED_ORACLE_RULE:
        raise ContractError(
            "oracle_rule must preserve the complete full-owner-proof v1 rule and measurement-only policy boundary"
        )
    validate_source_owned_coverage_limits(contract.get("coverage_limits"))

    candidates = contract.get("candidate_catalog")
    if not isinstance(candidates, list) or not candidates:
        raise ContractError("candidate_catalog must be a non-empty array")
    seen: set[str] = set()
    for candidate in candidates:
        if not isinstance(candidate, dict):
            raise ContractError("candidate_catalog entries must be objects")
        method_id = candidate.get("method_id")
        if not isinstance(method_id, str) or not method_id or method_id in seen:
            raise ContractError("candidate_catalog method_id values must be unique non-empty strings")
        seen.add(method_id)
        status = candidate.get("status")
        if status not in {"implemented", UNSUPPORTED_METHOD_STATUS}:
            raise ContractError(f"unsupported candidate status for {method_id!r}: {status!r}")
        if method_id in IMPLEMENTED_METHOD_IDS and status != "implemented":
            raise ContractError(f"implemented candidate {method_id!r} must remain implemented")
        if method_id in REQUIRED_UNSUPPORTED_CANDIDATE_IDS and status != UNSUPPORTED_METHOD_STATUS:
            raise ContractError(f"unsupported candidate {method_id!r} must remain unsupported")
        allowed_keys = (
            {"method_id", "family", "status", "description"}
            if status == "implemented"
            else {"method_id", "family", "status", "reason"}
        )
        undeclared_keys = sorted(set(candidate) - allowed_keys)
        if undeclared_keys:
            raise ContractError(
                f"candidate {method_id!r} contains undeclared field(s): {', '.join(undeclared_keys)}"
            )
        if status == "implemented" and method_id not in IMPLEMENTED_METHOD_IDS:
            raise ContractError(f"implemented candidate has no runner: {method_id!r}")
        family = candidate.get("family")
        if not isinstance(family, str) or not family.strip():
            raise ContractError(f"candidate {method_id!r} needs a non-empty family")
        if status == "implemented":
            description = candidate.get("description")
            if not isinstance(description, str) or not description.strip():
                raise ContractError(f"implemented candidate {method_id!r} needs a non-empty description")
        if status == UNSUPPORTED_METHOD_STATUS:
            reason = candidate.get("reason")
            if not isinstance(reason, str) or not reason.strip():
                raise ContractError(f"unsupported candidate {method_id!r} needs a non-empty reason")
    if set(IMPLEMENTED_METHOD_IDS) - seen:
        missing = sorted(set(IMPLEMENTED_METHOD_IDS) - seen)
        raise ContractError(f"contract is missing implemented candidate(s): {', '.join(missing)}")
    if REQUIRED_UNSUPPORTED_CANDIDATE_IDS - seen:
        missing = sorted(REQUIRED_UNSUPPORTED_CANDIDATE_IDS - seen)
        raise ContractError(
            f"contract is missing required unsupported candidate(s): {', '.join(missing)}"
        )

    metrics = contract.get("metrics")
    required_metrics = {
        "misses",
        "excess_nodes",
        "precision",
        "recall",
        "first_failure_latency_ms_synthetic_proxy",
        "total_latency_ms_synthetic_proxy",
        "retry_amplification",
        "stale_unknown_behavior",
        "explanation",
        "fail_closed_escalation",
    }
    if not isinstance(metrics, dict) or not required_metrics.issubset(metrics):
        raise ContractError("metrics must name every bounded comparison measurement")

    declared_adversarial = set(unique_strings(contract.get("adversarial_classes"), field="adversarial_classes"))
    if not REQUIRED_ADVERSARIAL_CLASSES.issubset(declared_adversarial):
        raise ContractError("contract must declare all required adversarial fixture classes")


def validate_cases(cases: dict[str, Any], contract: dict[str, Any]) -> list[dict[str, Any]]:
    if cases.get("schema_version") != "validation_routing_comparison_cases_v1":
        raise ContractError("cases schema_version must be validation_routing_comparison_cases_v1")
    if cases.get("fixture_id") != contract.get("fixture_id"):
        raise ContractError("cases fixture_id must match the comparison contract")
    evidence_policy = contract["evidence_policy"]
    source_posture = cases.get("source_posture")
    if source_posture != evidence_policy["source_posture"]:
        raise ContractError("cases source_posture must match the contract evidence policy")
    validate_latency_weights(cases.get("latency_event_weights_ms_synthetic_proxy"))
    accepted_evidence_kinds = set(evidence_policy["accepted_evidence_kinds"])

    identity = cases.get("comparison_identity")
    if not isinstance(identity, dict):
        raise ContractError("comparison_identity must be an object")
    reject_undeclared_keys(
        identity,
        allowed=EXPECTED_COMPARISON_IDENTITY_KEYS,
        field="comparison_identity",
    )
    for field in ("candidate_set_id", "environment_id"):
        if not isinstance(identity.get(field), str) or not identity[field]:
            raise ContractError(f"comparison_identity.{field} must be a non-empty string")

    input_evidence = cases.get("input_evidence")
    if not isinstance(input_evidence, dict):
        raise ContractError("input_evidence must be an object")
    reject_undeclared_keys(
        input_evidence,
        allowed=EXPECTED_INPUT_EVIDENCE_KEYS,
        field="input_evidence",
    )
    if input_evidence.get("source_kind") != "public_safe_external_report":
        raise ContractError("input_evidence must identify the public-safe shadow report")
    if not isinstance(input_evidence.get("path"), str) or not input_evidence["path"]:
        raise ContractError("input_evidence must carry the shadow report path")
    if (
        not isinstance(input_evidence.get("sha256"), str)
        or len(input_evidence["sha256"]) != 64
        or any(character not in "0123456789abcdef" for character in input_evidence["sha256"])
    ):
        raise ContractError("input_evidence must carry the shadow report digest")
    if input_evidence.get("allowed_use") != evidence_policy["allowed_use"]:
        raise ContractError(
            "input_evidence.allowed_use must preserve the source-owned measurement-only posture"
        )
    if input_evidence.get("raw_sessions_copied") is not False:
        raise ContractError("input_evidence must explicitly state that raw sessions were not copied")
    route_gaps = unique_strings(
        input_evidence.get("observed_real_route_gaps"),
        field="input_evidence.observed_real_route_gaps",
    )
    if not route_gaps:
        raise ContractError("input_evidence must retain observed route gaps")
    wall_clock_proxies = input_evidence.get("observed_wall_clock_proxies")
    if not isinstance(wall_clock_proxies, dict):
        raise ContractError("input_evidence must retain the bounded wall-clock proxy record")
    reject_undeclared_keys(
        wall_clock_proxies,
        allowed=EXPECTED_WALL_CLOCK_PROXY_KEYS,
        field="input_evidence.observed_wall_clock_proxies",
    )
    if not is_finite_non_negative_number(wall_clock_proxies.get("full_local_release_check_seconds")):
        raise ContractError("input_evidence full release proxy must be a finite non-negative number")
    targeted_proxies = wall_clock_proxies.get("targeted_local_route_proxy_seconds")
    if (
        not isinstance(targeted_proxies, list)
        or not targeted_proxies
        or not all(is_finite_non_negative_number(value) for value in targeted_proxies)
    ):
        raise ContractError(
            "input_evidence targeted route proxies must be a non-empty finite non-negative number array"
        )
    if wall_clock_proxies.get("speed_claim_status") != EXPECTED_SPEED_CLAIM_STATUS:
        raise ContractError(
            "input_evidence speed claim status must preserve the bounded rejection posture"
        )

    scenarios = cases.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        raise ContractError("scenarios must be a non-empty array")
    seen_ids: set[str] = set()
    observed_adversarial: set[str] = set()
    for scenario in scenarios:
        if not isinstance(scenario, dict):
            raise ContractError("scenario entries must be objects")
        scenario_id = scenario.get("scenario_id")
        if not isinstance(scenario_id, str) or not scenario_id or scenario_id in seen_ids:
            raise ContractError("scenario_id values must be unique non-empty strings")
        seen_ids.add(scenario_id)
        for field in ("workload_id", "candidate_set_id", "environment_id", "source_ref"):
            if not isinstance(scenario.get(field), str) or not scenario[field]:
                raise ContractError(f"scenario {scenario_id} must declare {field}")
        evidence_kind = scenario.get("evidence_kind")
        if not isinstance(evidence_kind, str) or evidence_kind not in accepted_evidence_kinds:
            raise ContractError(
                f"scenario {scenario_id} evidence_kind {evidence_kind!r} is not admitted by the seeded contract"
            )
        if scenario["candidate_set_id"] != identity["candidate_set_id"]:
            raise ContractError(f"scenario {scenario_id} changes candidate_set_id across peers")
        if scenario["environment_id"] != identity["environment_id"]:
            raise ContractError(f"scenario {scenario_id} changes environment_id across peers")
        if not isinstance(scenario.get("signals"), dict):
            raise ContractError(f"scenario {scenario_id}.signals must be an object")
        for signal_id, signal in scenario["signals"].items():
            if isinstance(signal, dict) and "retry_count" in signal:
                validate_retry_count(
                    signal["retry_count"],
                    field=f"{scenario_id}.signals.{signal_id}.retry_count",
                )
        unique_strings(scenario.get("changed_paths"), field=f"{scenario_id}.changed_paths")
        method_overrides = scenario.get("method_overrides")
        if method_overrides is not None and not isinstance(method_overrides, dict):
            raise ContractError(f"scenario {scenario_id}.method_overrides must be an object or null")
        static_override = (method_overrides or {}).get("static_paths")
        if "static_paths" in (method_overrides or {}) and not isinstance(static_override, dict):
            raise ContractError(f"scenario {scenario_id}.method_overrides.static_paths must be an object")
        if isinstance(static_override, dict) and "activated_nodes" in static_override:
            raise ContractError(
                f"scenario {scenario_id}.method_overrides.static_paths.activated_nodes is not admitted"
            )
        oracle = scenario.get("oracle")
        if not isinstance(oracle, dict):
            raise ContractError(f"scenario {scenario_id} must declare an owner-proof oracle")
        if oracle.get("required_nodes") == [] or oracle.get("owner_proof_nodes") == []:
            raise ContractError(f"scenario {scenario_id}.oracle node arrays must contain at least one node")
        required_nodes = unique_strings(oracle.get("required_nodes"), field=f"{scenario_id}.oracle.required_nodes")
        if not required_nodes:
            raise ContractError(f"scenario {scenario_id}.oracle.required_nodes must contain at least one node")
        owner_proof_nodes = unique_strings(
            oracle.get("owner_proof_nodes"), field=f"{scenario_id}.oracle.owner_proof_nodes"
        )
        if not owner_proof_nodes:
            raise ContractError(f"scenario {scenario_id}.oracle.owner_proof_nodes must contain at least one node")
        if not set(required_nodes).issubset(owner_proof_nodes):
            raise ContractError(f"scenario {scenario_id} oracle fallback must cover required nodes")
        if oracle.get("owner_proof_status") not in {"available", "blocked_external_receipt", "unknown"}:
            raise ContractError(f"scenario {scenario_id} has invalid owner_proof_status")
        if not isinstance(oracle.get("complete"), bool):
            raise ContractError(f"scenario {scenario_id}.oracle.complete must be boolean")
        if oracle.get("owner_proof_status") == "unknown" and oracle["complete"]:
            raise ContractError(
                f"scenario {scenario_id}.oracle cannot be complete when owner_proof_status is unknown"
            )
        adversarial_class = scenario.get("adversarial_class")
        if adversarial_class is not None:
            if not isinstance(adversarial_class, str) or not adversarial_class.strip():
                raise ContractError(f"scenario {scenario_id}.adversarial_class must be a non-empty string or null")
            if adversarial_class not in set(contract["adversarial_classes"]):
                raise ContractError(f"scenario {scenario_id} declares an unknown adversarial class")
            if not adversarial_class_matches(scenario, adversarial_class):
                raise ContractError(
                    f"scenario {scenario_id}.adversarial_class {adversarial_class!r} does not match its signals and oracle"
                )
            observed_adversarial.add(adversarial_class)

    if not REQUIRED_ADVERSARIAL_CLASSES.issubset(observed_adversarial):
        missing = sorted(REQUIRED_ADVERSARIAL_CLASSES - observed_adversarial)
        raise ContractError(f"cases are missing adversarial class(es): {', '.join(missing)}")
    return scenarios


def add_events(
    events: list[dict[str, Any]],
    *,
    target: str,
    status: str,
    latency_ms: float | None,
    explanation: str,
    retry_count: int = 0,
) -> None:
    validate_retry_count(retry_count, field=f"retry_count for {target!r}")
    validate_event_materialization_budget(
        1,
        retry_count,
        existing_count=len(events),
        field=f"retry materialization for {target!r}",
    )
    if not is_finite_non_negative_number(latency_ms):
        raise ContractError(
            f"{SYNTHETIC_LATENCY_FIELD} for {target!r} must be a finite non-negative number"
        )
    for attempt in range(retry_count + 1):
        events.append(
            {
                "target": target,
                "attempt": attempt + 1,
                "status": "retry" if attempt < retry_count else status,
                SYNTHETIC_LATENCY_FIELD: latency_ms,
                "explanation": explanation,
            }
        )


def signal_result(
    signal: dict[str, Any] | None,
    *,
    method_id: str,
    expected_state: str,
    latency_ms: float,
) -> dict[str, Any]:
    if not isinstance(signal, dict):
        signal = {"state": "unknown", "reason": "signal is not declared"}
    raw_state = signal.get("state", "unknown")
    normalized = normalize_signal(
        signal,
        method_id=method_id,
        expected_state=expected_state,
    )
    state = normalized.state
    nodes = list(normalized.nodes)
    normalized_to_blocked = normalized.normalized_to_blocked
    retry_count = signal.get("retry_count", 0)
    validate_retry_count(retry_count, field=f"retry_count for {method_id!r}")
    target_count = len(nodes) if state == expected_state else 1
    validate_event_materialization_budget(
        target_count,
        retry_count,
        field=f"retry materialization for {method_id!r}",
    )
    events: list[dict[str, Any]] = []
    activated: list[str] = []
    explanations: list[str] = []
    if state == expected_state:
        for node in nodes:
            activated.append(node)
            add_events(
                events,
                target=node,
                status="activated",
                latency_ms=latency_ms,
                explanation=f"{method_id} accepted {expected_state} signal",
                retry_count=retry_count,
            )
        explanations.append(f"{method_id} used a {expected_state} signal")
    else:
        reason = signal.get("reason")
        if not reason:
            if normalized_to_blocked:
                reason = f"{method_id} received unrecognized state {raw_state!r}; normalized to blocked"
            else:
                reason = f"{method_id} received {state} instead of {expected_state}"
        explanations.append(str(reason))
        add_events(
            events,
            target=f"{method_id}:{state}",
            status=state if state in FAILURE_STATES else "blocked",
            latency_ms=latency_ms,
            explanation=str(reason),
            retry_count=retry_count,
        )
    return {
        "activated_nodes": list(dict.fromkeys(activated)),
        "events": events,
        "signal_states": [state],
        "explanation": "; ".join(explanations),
        "missing_explanations": {},
    }


def owner_contract_result(
    scenario: dict[str, Any], *, method_id: str, latency_weights: dict[str, float]
) -> dict[str, Any]:
    raw_signal = scenario.get("signals", {}).get("owner_contracts")
    signal = dict(raw_signal) if isinstance(raw_signal, dict) else {}
    evidence = classify_owner_receipt(scenario)
    signal["state"] = evidence.state
    signal["reason"] = evidence.reason
    return signal_result(
        signal,
        method_id=method_id,
        expected_state="valid",
        latency_ms=latency_weights[method_id],
    )


def static_paths_result(scenario: dict[str, Any], latency_weights: dict[str, float]) -> dict[str, Any]:
    events: list[dict[str, Any]] = []
    activated, matched_targets = static_path_targets(scenario)
    for prefix, node in matched_targets:
        add_events(
            events,
            target=node,
            status="activated",
            latency_ms=latency_weights["static_paths"],
            explanation=f"changed path matched static prefix {prefix!r}",
        )
    overrides = scenario.get("method_overrides") or {}
    override = overrides.get("static_paths", {})
    explanation = str(override.get("explanation", "static path prefixes selected local nodes"))
    return {
        "activated_nodes": activated,
        "events": events,
        "signal_states": [],
        "explanation": explanation,
        "missing_explanations": {},
    }


def dependency_graph_result(scenario: dict[str, Any], latency_weights: dict[str, float]) -> dict[str, Any]:
    return signal_result(
        scenario.get("signals", {}).get("dependency_graph"),
        method_id="dependency_graph",
        expected_state="current",
        latency_ms=latency_weights["dependency_graph"],
    )


def history_result(scenario: dict[str, Any], latency_weights: dict[str, float]) -> dict[str, Any]:
    return signal_result(
        scenario.get("signals", {}).get("history_correlation"),
        method_id="history_correlation",
        expected_state="available",
        latency_ms=latency_weights["history_correlation"],
    )


def claim_risk_result(scenario: dict[str, Any], latency_weights: dict[str, float]) -> dict[str, Any]:
    return signal_result(
        scenario.get("signals", {}).get("claim_risk"),
        method_id="claim_risk",
        expected_state="declared",
        latency_ms=latency_weights["claim_risk"],
    )


def hybrid_result(scenario: dict[str, Any], latency_weights: dict[str, float]) -> dict[str, Any]:
    component_results = [
        static_paths_result(scenario, latency_weights),
        dependency_graph_result(scenario, latency_weights),
        owner_contract_result(scenario, method_id="owner_contracts", latency_weights=latency_weights),
        history_result(scenario, latency_weights),
        claim_risk_result(scenario, latency_weights),
    ]
    activated: list[str] = []
    events: list[dict[str, Any]] = []
    signal_states: list[str] = []
    explanations: list[str] = []
    for component in component_results:
        for node in component["activated_nodes"]:
            if node not in activated:
                activated.append(node)
        events.extend(component["events"])
        signal_states.extend(component["signal_states"])
        if component["explanation"]:
            explanations.append(component["explanation"])

    required_nodes = set(scenario["oracle"]["required_nodes"])
    unresolved_states = sorted(set(signal_states).intersection(FAILURE_STATES))
    missing_nodes = sorted(required_nodes - set(activated))
    escalation_reasons = list(unresolved_states)
    if missing_nodes:
        escalation_reasons.append("required_node_miss")
    if not scenario["oracle"]["complete"]:
        escalation_reasons.append("oracle_incomplete")

    escalation = bool(escalation_reasons)
    fallback_nodes: list[str] = []
    fallback_status = "not_needed"
    if escalation:
        fallback_nodes = list(scenario["oracle"]["owner_proof_nodes"])
        fallback_status = str(scenario["oracle"]["owner_proof_status"])
        explanations.append(
            "fail-closed escalation preserved unresolved state and retained full_owner_proof as fallback"
        )
    return {
        "activated_nodes": activated,
        "events": events,
        "signal_states": signal_states,
        "explanation": "; ".join(explanations),
        "missing_explanations": {node: "hybrid observed and escalated the missing node" for node in missing_nodes},
        "fail_closed_escalation": {
            "triggered": escalation,
            "reasons": escalation_reasons,
            "fallback": "full_owner_proof" if escalation else None,
            "fallback_nodes": fallback_nodes,
            "fallback_status": fallback_status,
            "policy_verdict": None,
        },
    }


METHOD_RUNNERS: dict[
    str, Callable[[dict[str, Any], dict[str, float]], dict[str, Any]]
] = {
    "static_paths": static_paths_result,
    "dependency_graph": dependency_graph_result,
    "owner_contracts": lambda scenario, latency_weights: owner_contract_result(
        scenario,
        method_id="owner_contracts",
        latency_weights=latency_weights,
    ),
    "history_correlation": history_result,
    "claim_risk": claim_risk_result,
    "hybrid_fail_closed": hybrid_result,
}


def finalize_result(
    *,
    method_id: str,
    candidate: dict[str, Any],
    scenario: dict[str, Any],
    proposal: dict[str, Any],
) -> dict[str, Any]:
    required = list(scenario["oracle"]["required_nodes"])
    activated = list(dict.fromkeys(proposal.get("activated_nodes", [])))
    missing = [node for node in required if node not in activated]
    excess = [node for node in activated if node not in required]
    events = proposal.get("events", [])
    if not isinstance(events, list):
        raise ContractError(f"{method_id}.{scenario['scenario_id']}.events must be an array")
    event_latencies: list[Any] = []
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            raise ContractError(
                f"{method_id}.{scenario['scenario_id']}.events[{index}] must be an object"
            )
        event_latencies.append(event.get(SYNTHETIC_LATENCY_FIELD))
    total_latency = finite_non_negative_sum(
        event_latencies,
        field=f"{method_id}.{scenario['scenario_id']}.total_latency_ms_synthetic_proxy",
    )
    cumulative = 0.0
    first_failure: float | None = None
    for index, event in enumerate(events):
        cumulative = checked_non_negative_add(
            cumulative,
            event[SYNTHETIC_LATENCY_FIELD],
            field=(
                f"{method_id}.{scenario['scenario_id']}."
                f"first_failure_latency_ms_synthetic_proxy[{index}]"
            ),
        )
        if first_failure is None and event.get("status") in FAILURE_STATES:
            first_failure = cumulative
    unique_targets = {
        str(event.get("target"))
        for event in events
        if isinstance(event, dict) and event.get("target")
    }
    attempt_count = len(events)
    retry_amplification = (
        attempt_count / len(unique_targets) if unique_targets else None
    )
    oracle_complete = bool(scenario["oracle"]["complete"])
    true_positive_count = len(set(activated).intersection(required))
    denominator_valid = oracle_complete and bool(required)
    precision = true_positive_count / len(activated) if denominator_valid and activated else None
    recall = true_positive_count / len(required) if denominator_valid else None
    state_counts = Counter(proposal.get("signal_states", []))
    missing_explanations = proposal.get("missing_explanations", {})
    if not isinstance(missing_explanations, dict):
        missing_explanations = {}
    unexplained_misses = [
        node
        for node in missing
        if not isinstance(missing_explanations.get(node), str)
        or not missing_explanations[node].strip()
    ]
    escalation = proposal.get(
        "fail_closed_escalation",
        {
            "triggered": False,
            "reasons": [],
            "fallback": None,
            "fallback_nodes": [],
            "fallback_status": "not_needed",
            "policy_verdict": None,
        },
    )
    failure_state_count = sum(state_counts.get(state, 0) for state in FAILURE_STATES)
    return {
        "method_id": method_id,
        "family": candidate.get("family"),
        "implementation_status": candidate.get("status"),
        "scenario_id": scenario["scenario_id"],
        "evidence_kind": scenario.get("evidence_kind", "seeded_fixture"),
        "identity": {
            field: scenario[field]
            for field in ("workload_id", "candidate_set_id", "environment_id", "source_ref")
        },
        "oracle": {
            "complete": oracle_complete,
            "required_nodes": required,
            "owner_proof_nodes": list(scenario["oracle"]["owner_proof_nodes"]),
            "owner_proof_status": scenario["oracle"]["owner_proof_status"],
        },
        "activated_nodes": activated,
        "missing_nodes": missing,
        "excess_nodes": excess,
        "precision": precision,
        "recall": recall,
        "precision_recall_denominator_valid": denominator_valid,
        "first_failure_latency_ms_synthetic_proxy": first_failure,
        "total_latency_ms_synthetic_proxy": total_latency,
        "attempt_count": attempt_count,
        "unique_attempt_targets": len(unique_targets),
        "retry_amplification": retry_amplification,
        "state_counts": {
            "stale": state_counts.get("stale", 0),
            "unknown": state_counts.get("unknown", 0),
            "malformed": state_counts.get("malformed", 0),
            "wrong_identity": state_counts.get("wrong_identity", 0),
            "blocked": state_counts.get("blocked", 0),
        },
        "stale_unknown_behavior": (
            "preserved_and_escalated"
            if escalation.get("triggered")
            else ("preserved_as_incomplete" if failure_state_count else "not_observed")
        ),
        "explanation": proposal.get("explanation", ""),
        "unexplained_miss_nodes": unexplained_misses,
        "fail_closed_escalation": escalation,
        "events": events,
    }


def summarize_method(method_id: str, candidate: dict[str, Any], results: list[dict[str, Any]]) -> dict[str, Any]:
    if candidate.get("status") == UNSUPPORTED_METHOD_STATUS:
        return {
            "method_id": method_id,
            "family": candidate.get("family"),
            "implementation_status": candidate.get("status"),
            "reason": candidate.get("reason"),
            "scenario_count": 0,
            "measurements": None,
            "scenario_results": [],
        }
    seeded_results = [result for result in results if result["evidence_kind"] == "seeded_fixture"]
    real_results = [result for result in results if result["evidence_kind"] == "real_session"]
    denominator_valid_results = [
        result for result in results if result["precision_recall_denominator_valid"]
    ]
    total_activated = sum(len(result["activated_nodes"]) for result in denominator_valid_results)
    total_true_positive = sum(
        len(set(result["activated_nodes"]).intersection(result["oracle"]["required_nodes"]))
        for result in denominator_valid_results
    )
    total_required = sum(len(result["oracle"]["required_nodes"]) for result in denominator_valid_results)
    total_attempts = sum(result["attempt_count"] for result in results)
    total_unique_targets = sum(result["unique_attempt_targets"] for result in results)
    return {
        "method_id": method_id,
        "family": candidate.get("family"),
        "implementation_status": candidate.get("status"),
        "scenario_count": len(results),
        "measurements": {
            "seeded_case_count": len(seeded_results),
            "real_case_count": len(real_results),
            "seeded_miss_count": sum(len(result["missing_nodes"]) for result in seeded_results),
            "real_miss_count": (
                sum(len(result["missing_nodes"]) for result in real_results)
                if real_results
                else None
            ),
            "excess_node_count": sum(len(result["excess_nodes"]) for result in results),
            "precision": total_true_positive / total_activated if total_activated else None,
            "recall": total_true_positive / total_required if total_required else None,
            "precision_recall_denominator_valid_case_count": len(denominator_valid_results),
            "first_failure_latency_ms_synthetic_proxy_min": min(
                (
                    result["first_failure_latency_ms_synthetic_proxy"]
                    for result in results
                    if result["first_failure_latency_ms_synthetic_proxy"] is not None
                ),
                default=None,
            ),
            "total_latency_ms_synthetic_proxy_sum": finite_non_negative_sum(
                [result["total_latency_ms_synthetic_proxy"] for result in results],
                field=f"{method_id}.total_latency_ms_synthetic_proxy_sum",
            ),
            "latency_kind": SYNTHETIC_LATENCY_KIND,
            "retry_amplification": (
                total_attempts / total_unique_targets if total_unique_targets else None
            ),
            "stale_count": sum(result["state_counts"]["stale"] for result in results),
            "unknown_count": sum(result["state_counts"]["unknown"] for result in results),
            "malformed_count": sum(result["state_counts"]["malformed"] for result in results),
            "wrong_identity_count": sum(result["state_counts"]["wrong_identity"] for result in results),
            "unexplained_miss_count": sum(len(result["unexplained_miss_nodes"]) for result in results),
            "fail_closed_escalation_count": sum(
                1 for result in results if result["fail_closed_escalation"].get("triggered")
            ),
        },
        "scenario_results": results,
    }


def build_report(contract: dict[str, Any], cases: dict[str, Any]) -> dict[str, Any]:
    validate_contract(contract)
    latency_weights = validate_latency_weights(cases.get("latency_event_weights_ms_synthetic_proxy"))
    scenarios = validate_cases(cases, contract)
    candidates = {candidate["method_id"]: candidate for candidate in contract["candidate_catalog"]}
    methods: list[dict[str, Any]] = []
    for method_id, candidate in candidates.items():
        if candidate["status"] == UNSUPPORTED_METHOD_STATUS:
            methods.append(summarize_method(method_id, candidate, []))
            continue
        runner = METHOD_RUNNERS[method_id]
        results = [
            finalize_result(
                method_id=method_id,
                candidate=candidate,
                scenario=scenario,
                proposal=runner(scenario, latency_weights),
            )
            for scenario in scenarios
        ]
        methods.append(summarize_method(method_id, candidate, results))

    identity = cases["comparison_identity"]
    evidence_policy = contract["evidence_policy"]
    latency_policy = contract["latency_policy"]
    seeded_case_count = sum(
        1 for scenario in scenarios if scenario.get("evidence_kind") == SEEDED_EVIDENCE_KIND
    )
    real_case_count = sum(
        1 for scenario in scenarios if scenario.get("evidence_kind") == REAL_EVIDENCE_KIND
    )
    report = {
        "schema_version": REPORT_SCHEMA_VERSION,
        "report_kind": evidence_policy["report_kind"],
        "comparison_mode": "peer-compare",
        "claim_posture": "measurement_only",
        "policy_verdict": None,
        "selection_status": "deferred_pending_bound_external_campaign",
        "fixture_id": cases["fixture_id"],
        "evidence_posture": {
            "source_posture": cases["source_posture"],
            "accepted_evidence_kinds": list(evidence_policy["accepted_evidence_kinds"]),
            "real_evidence_status": evidence_policy["real_evidence_status"],
        },
        "latency_posture": dict(latency_policy),
        "resource_policy": dict(contract["resource_policy"]),
        "comparison_identity": identity,
        "comparison_identity_digest": canonical_digest(identity),
        "input_evidence": cases["input_evidence"],
        "candidate_catalog": contract["candidate_catalog"],
        "adversarial_classes_covered": sorted(
            {
                scenario["adversarial_class"]
                for scenario in scenarios
                if scenario.get("adversarial_class")
            }
        ),
        "coverage_limits": list(EXPECTED_COVERAGE_LIMITS),
        "methods": methods,
        "scenario_count": len(scenarios),
        "real_case_count": real_case_count,
        "seeded_case_count": seeded_case_count,
        "oracle_rule": contract["oracle_rule"],
    }
    ensure_strict_json_finite(report)
    return report


def render_text(report: dict[str, Any]) -> str:
    lines = [
        f"Validation-routing comparison fixture: {report['fixture_id']}",
        f"claim posture: {report['claim_posture']}",
        f"selection status: {report['selection_status']}",
        (
            "evidence posture: "
            f"seeded_fixture={report['seeded_case_count']}, "
            f"real_session={report['real_case_count']}"
        ),
        (
            "latency posture: "
            f"{report['latency_posture']['kind']} "
            "(not observed runtime latency)"
        ),
    ]
    for method in report["methods"]:
        lines.append("")
        lines.append(f"{method['method_id']} ({method['implementation_status']})")
        if method["measurements"] is None:
            lines.append(f"- missing candidate: {method['reason']}")
            continue
        measurements = method["measurements"]
        lines.extend(
            [
                f"- seeded misses: {measurements['seeded_miss_count']}",
                f"- real misses: {measurements['real_miss_count']}",
                f"- precision/recall: {measurements['precision']} / {measurements['recall']}",
                "- first failure synthetic proxy / total synthetic proxy latency ms: "
                f"{measurements['first_failure_latency_ms_synthetic_proxy_min']} / "
                f"{measurements['total_latency_ms_synthetic_proxy_sum']}",
                f"- retry amplification: {measurements['retry_amplification']}",
                f"- stale/unknown/malformed/wrong receipt: {measurements['stale_count']}/{measurements['unknown_count']}/{measurements['malformed_count']}/{measurements['wrong_identity_count']}",
                f"- fail-closed escalations: {measurements['fail_closed_escalation_count']}",
            ]
        )
    return "\n".join(lines)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run seeded validation-routing peer comparison.")
    parser.add_argument("--contract", default=str(DEFAULT_CONTRACT))
    parser.add_argument("--cases", default=str(DEFAULT_CASES))
    parser.add_argument("--output")
    parser.add_argument("--format", choices=("json", "text"), default="text")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        contract = load_object(Path(args.contract))
        cases = load_object(Path(args.cases))
        report = build_report(contract, cases)
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(
                json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
                encoding="utf-8",
            )
        if args.format == "json":
            print(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False))
        else:
            print(render_text(report))
    except (ContractError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"validation-routing comparison failed: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
