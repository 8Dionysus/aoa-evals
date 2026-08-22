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
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Callable, Sequence


PART_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_CONTRACT = PART_ROOT / "schemas" / "validation-routing-comparison-v1.contract.json"
DEFAULT_CASES = PART_ROOT / "fixtures" / "validation-routing-bounded-v1" / "cases.json"

REPORT_SCHEMA_VERSION = "validation_routing_comparison_report_v1"
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
UNSUPPORTED_METHOD_STATUS = "unsupported_missing_candidate"
FAILURE_STATES = {"stale", "unknown", "malformed", "wrong_identity", "blocked"}
REQUIRED_ADVERSARIAL_CLASSES = {
    "stale_graph",
    "unknown_dependency",
    "wrong_candidate_environment_receipt",
    "malformed_receipt",
    "unexplained_miss",
    "unbound_external_owner",
}

STATIC_PATH_RULES: tuple[tuple[str, str], ...] = (
    ("scripts/", "source_fast"),
    ("generated/", "generated"),
    ("mechanics/", "mechanics_part_local"),
    ("tests/", "behavior_tests"),
)


class ContractError(ValueError):
    """Raised when a fixture or report contract is not safe to compare."""


def load_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ContractError(f"{path} must contain a JSON object")
    return payload


def unique_strings(values: Any, *, field: str) -> list[str]:
    if not isinstance(values, list) or not all(isinstance(value, str) and value for value in values):
        raise ContractError(f"{field} must be a non-empty string array")
    if len(set(values)) != len(values):
        raise ContractError(f"{field} must not contain duplicates")
    return list(values)


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def owner_contract_signal_state(scenario: dict[str, Any]) -> str:
    signals = scenario.get("signals", {})
    signal = signals.get("owner_contracts") if isinstance(signals, dict) else None
    if not isinstance(signal, dict):
        return "unknown"

    state = signal.get("state", "unknown")
    if state != "valid":
        return state if isinstance(state, str) and state in FAILURE_STATES else "blocked"

    receipt = signal.get("receipt")
    if not isinstance(receipt, dict):
        return "malformed"
    expected = {
        "workload_id": scenario["workload_id"],
        "candidate_set_id": scenario["candidate_set_id"],
        "environment_id": scenario["environment_id"],
        "source_ref": scenario["source_ref"],
    }
    if any(key not in receipt for key in expected):
        return "malformed"
    if any(receipt.get(key) != value for key, value in expected.items()):
        return "wrong_identity"
    return "valid"


def adversarial_class_matches(scenario: dict[str, Any], adversarial_class: str) -> bool:
    signals = scenario.get("signals", {})
    dependency_graph = signals.get("dependency_graph") if isinstance(signals, dict) else None
    dependency_state = dependency_graph.get("state") if isinstance(dependency_graph, dict) else None

    if adversarial_class == "stale_graph":
        return dependency_state == "stale"
    if adversarial_class == "unknown_dependency":
        return dependency_state == "unknown"
    if adversarial_class == "wrong_candidate_environment_receipt":
        return owner_contract_signal_state(scenario) == "wrong_identity"
    if adversarial_class == "malformed_receipt":
        return owner_contract_signal_state(scenario) == "malformed"
    if adversarial_class == "unbound_external_owner":
        oracle = scenario["oracle"]
        return (
            oracle.get("complete") is False
            and oracle.get("owner_proof_status") == "unknown"
            and owner_contract_signal_state(scenario) == "unknown"
        )
    if adversarial_class == "unexplained_miss":
        proposal = static_paths_result(scenario)
        required = set(scenario["oracle"]["required_nodes"])
        activated = set(proposal["activated_nodes"])
        missing = required - activated
        explanations = proposal.get("missing_explanations", {})
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

    latency_policy = contract.get("latency_policy")
    if not isinstance(latency_policy, dict):
        raise ContractError("latency_policy must declare the latency evidence semantics")
    if latency_policy.get("kind") != SYNTHETIC_LATENCY_KIND:
        raise ContractError("validation-routing v1 requires synthetic fixture proxy latency")
    if latency_policy.get("runtime_observed") is not False:
        raise ContractError("synthetic fixture proxy latency must not be marked runtime observed")
    if latency_policy.get("field_suffix") != "_synthetic_proxy":
        raise ContractError("synthetic latency fields must retain their explicit field suffix")

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
        if status == "implemented" and method_id not in IMPLEMENTED_METHOD_IDS:
            raise ContractError(f"implemented candidate has no runner: {method_id!r}")
        family = candidate.get("family")
        if not isinstance(family, str) or not family.strip():
            raise ContractError(f"candidate {method_id!r} needs a non-empty family")
        if method_id in IMPLEMENTED_METHOD_IDS and status != "implemented":
            raise ContractError(f"implemented candidate {method_id!r} must remain implemented")
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
    accepted_evidence_kinds = set(evidence_policy["accepted_evidence_kinds"])

    identity = cases.get("comparison_identity")
    if not isinstance(identity, dict):
        raise ContractError("comparison_identity must be an object")
    for field in ("candidate_set_id", "environment_id"):
        if not isinstance(identity.get(field), str) or not identity[field]:
            raise ContractError(f"comparison_identity.{field} must be a non-empty string")

    input_evidence = cases.get("input_evidence")
    if not isinstance(input_evidence, dict):
        raise ContractError("input_evidence must be an object")
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
    if not isinstance(input_evidence.get("allowed_use"), str) or not input_evidence["allowed_use"]:
        raise ContractError("input_evidence must declare its bounded allowed use")
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
    if not isinstance(wall_clock_proxies.get("full_local_release_check_seconds"), (int, float)):
        raise ContractError("input_evidence full release proxy must be numeric")
    targeted_proxies = wall_clock_proxies.get("targeted_local_route_proxy_seconds")
    if (
        not isinstance(targeted_proxies, list)
        or not targeted_proxies
        or not all(isinstance(value, (int, float)) for value in targeted_proxies)
    ):
        raise ContractError("input_evidence targeted route proxies must be a non-empty number array")
    if not isinstance(wall_clock_proxies.get("speed_claim_status"), str):
        raise ContractError("input_evidence speed claim status must be explicit")

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
        if evidence_kind not in accepted_evidence_kinds:
            raise ContractError(
                f"scenario {scenario_id} evidence_kind {evidence_kind!r} is not admitted by the seeded contract"
            )
        if scenario["candidate_set_id"] != identity["candidate_set_id"]:
            raise ContractError(f"scenario {scenario_id} changes candidate_set_id across peers")
        if scenario["environment_id"] != identity["environment_id"]:
            raise ContractError(f"scenario {scenario_id} changes environment_id across peers")
        unique_strings(scenario.get("changed_paths"), field=f"{scenario_id}.changed_paths")
        oracle = scenario.get("oracle")
        if not isinstance(oracle, dict):
            raise ContractError(f"scenario {scenario_id} must declare an owner-proof oracle")
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
    if not isinstance(retry_count, int) or retry_count < 0:
        raise ContractError(f"retry_count for {target!r} must be a non-negative integer")
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
    normalized_to_blocked = not (
        raw_state == expected_state
        or (isinstance(raw_state, str) and raw_state in FAILURE_STATES)
    )
    state = "blocked" if normalized_to_blocked else raw_state
    nodes = signal.get("nodes", [])
    if not isinstance(nodes, list) or not all(isinstance(node, str) and node for node in nodes):
        state = "malformed"
        nodes = []
    elif len(set(nodes)) != len(nodes):
        raise ContractError(f"{method_id}.nodes must not contain duplicates")
    retry_count = signal.get("retry_count", 0)
    if not isinstance(retry_count, int) or isinstance(retry_count, bool) or retry_count < 0:
        raise ContractError(f"retry_count for {method_id!r} must be a non-negative integer")
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


def expected_receipt(scenario: dict[str, Any]) -> dict[str, str]:
    return {
        "workload_id": scenario["workload_id"],
        "candidate_set_id": scenario["candidate_set_id"],
        "environment_id": scenario["environment_id"],
        "source_ref": scenario["source_ref"],
    }


def owner_contract_result(scenario: dict[str, Any], *, method_id: str) -> dict[str, Any]:
    signal = scenario.get("signals", {}).get("owner_contracts")
    if not isinstance(signal, dict):
        return signal_result(None, method_id=method_id, expected_state="valid", latency_ms=4.0)
    state = signal.get("state", "unknown")
    if state != "valid":
        return signal_result(signal, method_id=method_id, expected_state="valid", latency_ms=4.0)
    receipt = signal.get("receipt")
    if not isinstance(receipt, dict):
        malformed = {**signal, "state": "malformed", "reason": "owner receipt is not an object"}
        return signal_result(malformed, method_id=method_id, expected_state="valid", latency_ms=4.0)
    expected = expected_receipt(scenario)
    if any(key not in receipt for key in expected):
        malformed = {**signal, "state": "malformed", "reason": "owner receipt omitted an identity field"}
        return signal_result(malformed, method_id=method_id, expected_state="valid", latency_ms=4.0)
    if any(receipt.get(key) != value for key, value in expected.items()):
        wrong = {
            **signal,
            "state": "wrong_identity",
            "reason": "owner receipt workload, candidate, environment, or source identity mismatched",
        }
        return signal_result(wrong, method_id=method_id, expected_state="valid", latency_ms=4.0)
    return signal_result(signal, method_id=method_id, expected_state="valid", latency_ms=4.0)


def static_paths_result(scenario: dict[str, Any]) -> dict[str, Any]:
    events: list[dict[str, Any]] = []
    activated: list[str] = []
    for changed_path in scenario["changed_paths"]:
        for prefix, node in STATIC_PATH_RULES:
            if changed_path.startswith(prefix):
                if node not in activated:
                    activated.append(node)
                add_events(
                    events,
                    target=node,
                    status="activated",
                    latency_ms=1.5,
                    explanation=f"changed path matched static prefix {prefix!r}",
                )
                break
    override = scenario.get("method_overrides", {}).get("static_paths", {})
    explanation = str(override.get("explanation", "static path prefixes selected local nodes"))
    if "activated_nodes" in override:
        activated = unique_strings(override["activated_nodes"], field="static_paths.activated_nodes")
    return {
        "activated_nodes": activated,
        "events": events,
        "signal_states": [],
        "explanation": explanation,
        "missing_explanations": {},
    }


def dependency_graph_result(scenario: dict[str, Any]) -> dict[str, Any]:
    return signal_result(
        scenario.get("signals", {}).get("dependency_graph"),
        method_id="dependency_graph",
        expected_state="current",
        latency_ms=3.5,
    )


def history_result(scenario: dict[str, Any]) -> dict[str, Any]:
    return signal_result(
        scenario.get("signals", {}).get("history_correlation"),
        method_id="history_correlation",
        expected_state="available",
        latency_ms=5.0,
    )


def claim_risk_result(scenario: dict[str, Any]) -> dict[str, Any]:
    return signal_result(
        scenario.get("signals", {}).get("claim_risk"),
        method_id="claim_risk",
        expected_state="declared",
        latency_ms=2.0,
    )


def hybrid_result(scenario: dict[str, Any]) -> dict[str, Any]:
    component_results = [
        static_paths_result(scenario),
        dependency_graph_result(scenario),
        owner_contract_result(scenario, method_id="owner_contracts"),
        history_result(scenario),
        claim_risk_result(scenario),
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


METHOD_RUNNERS: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
    "static_paths": static_paths_result,
    "dependency_graph": dependency_graph_result,
    "owner_contracts": lambda scenario: owner_contract_result(scenario, method_id="owner_contracts"),
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
    total_latency = sum(
        float(event[SYNTHETIC_LATENCY_FIELD])
        for event in events
        if isinstance(event, dict) and isinstance(event.get(SYNTHETIC_LATENCY_FIELD), (int, float))
    )
    cumulative = 0.0
    first_failure: float | None = None
    for event in events:
        if not isinstance(event, dict):
            continue
        latency = event.get(SYNTHETIC_LATENCY_FIELD)
        if isinstance(latency, (int, float)):
            cumulative += float(latency)
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
            "total_latency_ms_synthetic_proxy_sum": sum(
                result["total_latency_ms_synthetic_proxy"] for result in results
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
                proposal=runner(scenario),
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
    return {
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
        "coverage_limits": contract["coverage_limits"],
        "methods": methods,
        "scenario_count": len(scenarios),
        "real_case_count": real_case_count,
        "seeded_case_count": seeded_case_count,
        "oracle_rule": contract["oracle_rule"],
    }


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
            output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if args.format == "json":
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print(render_text(report))
    except (ContractError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"validation-routing comparison failed: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
