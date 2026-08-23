"""Deterministic admission/reporting for the identity-bound method ABI.

The runner consumes an explicit owner apply packet. It validates and compares
the supplied rows, but it never executes the packet command or discovers live
telemetry. A successful run is contract evidence only; it is not central proof
or owner acceptance.
"""

from __future__ import annotations

import argparse
import copy
import json
from collections import defaultdict
import math
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
APPLY_SCHEMA_PATH = BUNDLE_ROOT / "fixtures" / "apply-packet.schema.json"
REPORT_SCHEMA_PATH = BUNDLE_ROOT / "reports" / "summary.schema.json"

METHOD_IDS = (
    "legacy_serial_full_release",
    "owner_focused_affected_only",
    "claim_evidence_activated_subgraph_or_tiered",
    "bounded_stable_prefix_session_measurement",
    "retry_after_fix_first_failure",
    "controlled_same_candidate_seeded_fault",
)
IDENTITY_FIELDS = (
    "workload_id",
    "candidate_or_source_identity",
    "source_ref_or_digest",
    "environment_id",
    "route_or_treatment_identity",
    "evidence_class",
    "acceptance_target",
    "cache_posture",
    "resource_posture",
)
METRIC_NAMES = (
    "wall_seconds",
    "cpu_ms",
    "peak_rss_kib",
    "io_read_bytes",
    "io_write_bytes",
    "setup_startup_seconds",
    "first_failure_latency_seconds",
    "retry_amplification",
)
CANONICAL_METRIC_UNITS = {
    "wall_seconds": "seconds",
    "cpu_ms": "milliseconds",
    "peak_rss_kib": "kibibytes",
    "io_read_bytes": "bytes",
    "io_write_bytes": "bytes",
    "setup_startup_seconds": "seconds",
    "first_failure_latency_seconds": "seconds",
    "retry_amplification": "ratio",
}
ALLOWED_OBSERVATION_EVIDENCE_CLASSES = frozenset(
    {"public-safe-contract", "reviewed-owner-packet"}
)
OBSERVATION_ARTIFACT_KINDS = frozenset({"public-safe-observation"})
NON_VALUE_STATUSES = ("unknown", "null", "excluded", "unobservable", "missing")
ALLOWED_REVIEW_STATUSES = frozenset({"reviewed", "controlled"})
OBSERVED_REVIEW_STATUS = "reviewed"
REPORT_CLAIM_BOUNDARY = (
    "This report preserves identity-bound observation or accounting dispositions "
    "only; it does not issue method effects, causal claims, proof, policy, "
    "acceptance, or a universal winner."
)
REPORT_LIMITATIONS = [
    "the runner consumes an explicit packet and never executes command.argv",
    "a generated reader or green validator is not real-session telemetry",
    "synthetic and controlled values are excluded from observed_values",
    "unknown, null, excluded, unobservable, and missing states are not zero",
    "no central proof, runtime health, policy, or human-acceptance verdict is emitted",
]
CLAIM_LIMIT_OBSERVED = (
    "identity-bound observation pair only; no effect, proof, policy, or winner claim"
)
CLAIM_LIMIT_CONTROLLED = (
    "identity-matched accounting only; controlled or synthetic values are not observed effect"
)
CLAIM_LIMIT_UNMATCHED = "no eligible identity- and parity-matched method pair"
CLAIM_LIMIT_BASELINE_MISSING = "no declared baseline row; no method pair admitted"
CLAIM_LIMIT_CANDIDATE_MISSING = "one-sided baseline; no method pair admitted"


class ContractError(ValueError):
    """Raised when the input would make comparison semantics ambiguous."""


def _reject_non_finite_json_constant(value: str) -> Any:
    raise ContractError(f"non-finite JSON numeric literal is not allowed: {value}")


def _load_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            parse_constant=_reject_non_finite_json_constant,
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot load JSON {path}: {exc}") from exc


def _unmatched_case_signature(case: dict[str, Any]) -> tuple[Any, ...]:
    return (
        case["unit_id"],
        case.get("method_id"),
        case["reason"],
        tuple(sorted(case["mismatched_fields"])),
    )


def _expected_claim_limit(unit: dict[str, Any]) -> str:
    if unit["disposition"] == "matched_observation_only":
        return CLAIM_LIMIT_OBSERVED
    if unit["disposition"] == "controlled_accounting_only":
        return CLAIM_LIMIT_CONTROLLED
    reasons = {
        case["reason"] for case in unit["unmatched_case_expectations"]
    }
    if "baseline_method_missing" in reasons:
        return CLAIM_LIMIT_BASELINE_MISSING
    if "comparison_candidate_missing" in reasons:
        return CLAIM_LIMIT_CANDIDATE_MISSING
    return CLAIM_LIMIT_UNMATCHED


def _validate_schema(payload: Any) -> None:
    schema = _load_json(APPLY_SCHEMA_PATH)
    errors = sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda error: list(error.path))
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.path) or "$"
        raise ContractError(f"apply packet schema error at {location}: {error.message}")


def validate_report(report: Any) -> None:
    """Validate report shape and preserve admission-counter parity with units."""

    schema = _load_json(REPORT_SCHEMA_PATH)
    errors = sorted(Draft202012Validator(schema).iter_errors(report), key=lambda error: list(error.path))
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.path) or "$"
        raise ContractError(f"report schema error at {location}: {error.message}")

    if report["claim_boundary"] != REPORT_CLAIM_BOUNDARY:
        raise ContractError("report claim_boundary must preserve the canonical boundary")
    if report["limitations"] != REPORT_LIMITATIONS:
        raise ContractError("report limitations must preserve the canonical limitations")

    units = report["comparison_units"]
    expected = {
        "observation_count": sum(len(unit["method_ids"]) for unit in units),
        "unit_count": len(units),
        "matched_unit_count": sum(
            unit["disposition"] == "matched_observation_only" for unit in units
        ),
        "controlled_accounting_unit_count": sum(
            unit["disposition"] == "controlled_accounting_only" for unit in units
        ),
        "unmatched_unit_count": sum(unit["disposition"] == "unmatched" for unit in units),
        "matched_pair_count": sum(unit["matched_pair_count"] for unit in units),
        "eligible_real_pairs": sum(unit["observed_pair_count"] for unit in units),
    }
    for field, expected_value in expected.items():
        actual_value = report["admission"][field]
        if actual_value != expected_value:
            raise ContractError(
                f"report admission.{field}={actual_value!r} does not match comparison_units-derived {expected_value!r}"
            )

    unit_ids = [unit["unit_id"] for unit in units]
    if len(unit_ids) != len(set(unit_ids)):
        duplicates = sorted(
            {unit_id for unit_id in unit_ids if unit_ids.count(unit_id) > 1}
        )
        raise ContractError(
            "report comparison_units contains duplicate unit_id values: "
            + ", ".join(duplicates)
        )

    unit_by_id = {unit["unit_id"]: unit for unit in units}
    unmatched_case_unit_ids = {case["unit_id"] for case in report["unmatched_cases"]}
    unknown_case_units = unmatched_case_unit_ids - unit_by_id.keys()
    if unknown_case_units:
        raise ContractError(
            "report unmatched_cases contains unknown unit IDs: "
            + ", ".join(sorted(unknown_case_units))
        )
    expected_case_units = {
        unit["unit_id"]
        for unit in units
        if unit["disposition"] == "unmatched" or unit["mismatched_fields"]
    }
    missing_case_units = expected_case_units - unmatched_case_unit_ids
    if missing_case_units:
        raise ContractError(
            "report unmatched_cases omits units with unmatched reasons: "
            + ", ".join(sorted(missing_case_units))
        )

    cases_by_unit: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for case in report["unmatched_cases"]:
        cases_by_unit[case["unit_id"]].append(case)

    for unit in units:
        method_count = len(unit["method_ids"])
        expected_claim_limit = _expected_claim_limit(unit)
        if unit["claim_limit"] != expected_claim_limit:
            raise ContractError(
                "report claim_limit must preserve the canonical boundary for unit "
                f"{unit['unit_id']!r}"
            )
        admitted_method_ids = {
            method_id
            for binding in unit["matched_identity_bindings"]
            for method_id in binding["method_ids"]
        }
        provenance_by_method: dict[
            str, list[frozenset[tuple[str, str, str, str, str]]]
        ] = defaultdict(list)
        provenance_digests: dict[str, set[str]] = defaultdict(set)
        for binding in unit["matched_identity_bindings"]:
            binding_provenance_by_method: dict[
                str, set[tuple[str, str, str, str, str]]
            ] = defaultdict(set)
            for provenance in binding["evidence_provenance"]:
                binding_provenance_by_method[provenance["method_id"]].add(
                    (
                        provenance["ref"],
                        provenance["digest"],
                        provenance["kind"],
                        provenance["evidence_class"],
                        provenance["measurement_origin"],
                    )
                )
                provenance_digests[provenance["ref"]].add(provenance["digest"])
            for method_id, provenance_set in binding_provenance_by_method.items():
                provenance_by_method[method_id].append(frozenset(provenance_set))
        conflicting_provenance = {
            ref: sorted(digests)
            for ref, digests in provenance_digests.items()
            if len(digests) > 1
        }
        if conflicting_provenance:
            raise ContractError(
                "report matched identity provenance has conflicting digests per ref: "
                f"{conflicting_provenance!r}"
            )
        binding_origins: list[dict[str, set[str]]] = []
        for binding in unit["matched_identity_bindings"]:
            origins_by_method: dict[str, set[str]] = defaultdict(set)
            for provenance in binding["evidence_provenance"]:
                origins_by_method[provenance["method_id"]].add(
                    provenance["measurement_origin"]
                )
            if set(origins_by_method) != set(binding["method_ids"]) or any(
                len(origins) != 1 for origins in origins_by_method.values()
            ):
                raise ContractError(
                    "report matched identity provenance must bind one "
                    "measurement_origin per admitted method for unit "
                    f"{unit['unit_id']!r}"
                )
            binding_origins.append(origins_by_method)
        unit_origins_by_method: dict[str, set[str]] = defaultdict(set)
        for origins_by_method in binding_origins:
            for method_id, origins in origins_by_method.items():
                unit_origins_by_method[method_id].update(origins)
        conflicting_method_origins = {
            method_id: sorted(origins)
            for method_id, origins in unit_origins_by_method.items()
            if len(origins) > 1
        }
        if conflicting_method_origins:
            raise ContractError(
                "report measurement_origin must stay consistent per method "
                "across bindings for unit "
                f"{unit['unit_id']!r}: {conflicting_method_origins!r}"
            )
        inconsistent_repeated_provenance = sorted(
            method_id
            for method_id, provenance_sets in provenance_by_method.items()
            if len(set(provenance_sets)) > 1
        )
        if inconsistent_repeated_provenance:
            raise ContractError(
                "report matched identity provenance must stay consistent per "
                "repeated method across bindings for unit "
                f"{unit['unit_id']!r}: "
                + ", ".join(inconsistent_repeated_provenance)
            )
        bound_observation_refs = {
            provenance["ref"]
            for binding in unit["matched_identity_bindings"]
            for provenance in binding["evidence_provenance"]
        }
        if unit["matched_identity_bindings"] and bound_observation_refs != set(
            unit["observation_refs"]
        ):
            raise ContractError(
                "report observation_refs must match matched identity provenance "
                f"for unit {unit['unit_id']!r}: "
                f"declared={sorted(unit['observation_refs'])!r}, "
                f"bound={sorted(bound_observation_refs)!r}"
            )
        binding_identities = [
            binding["identity"] for binding in unit["matched_identity_bindings"]
        ]
        if binding_identities and any(
            identity != binding_identities[0] for identity in binding_identities[1:]
        ):
            raise ContractError(
                "report matched identity bindings must preserve one identity snapshot "
                f"for unit {unit['unit_id']!r}"
            )

        covered_observed_pair_count = 0
        for binding, origins_by_method in zip(
            unit["matched_identity_bindings"], binding_origins
        ):
            binding_method_ids = set(binding["method_ids"])
            has_observed_metric = any(
                binding_method_ids
                <= {
                    value["method_id"]
                    for value in metric["observed_values"]
                }
                for metric in unit["metric_coverage"].values()
            )
            if has_observed_metric:
                if any(
                    origins_by_method[method_id] != {"observed"}
                    for method_id in binding_method_ids
                ):
                    raise ContractError(
                        "report observed metric coverage requires observed "
                        "measurement_origin for every bound method in unit "
                        f"{unit['unit_id']!r}"
                    )
                covered_observed_pair_count += 1
        if covered_observed_pair_count != unit["observed_pair_count"]:
            raise ContractError(
                "report observed_pair_count does not match bindings with jointly "
                f"measured metric coverage for unit {unit['unit_id']!r}: "
                f"declared={unit['observed_pair_count']!r}, "
                f"covered={covered_observed_pair_count!r}"
            )

        rejected_method_ids = (
            set(unit["method_ids"])
            - admitted_method_ids
            - {report["baseline_target"]}
        )
        unit_cases = cases_by_unit.get(unit["unit_id"], [])
        case_method_ids = {
            case["method_id"]
            for case in unit_cases
            if case.get("method_id") is not None
        }
        unknown_case_method_ids = case_method_ids - set(unit["method_ids"])
        if unknown_case_method_ids:
            raise ContractError(
                "report unmatched_cases names method IDs outside their unit: "
                + ", ".join(sorted(unknown_case_method_ids))
            )
        admitted_case_method_ids = case_method_ids & admitted_method_ids
        if admitted_case_method_ids:
            raise ContractError(
                "report unmatched_cases names admitted method IDs: "
                + ", ".join(sorted(admitted_case_method_ids))
            )
        missing_rejected_method_ids = rejected_method_ids - case_method_ids
        if missing_rejected_method_ids:
            raise ContractError(
                "report unmatched_cases omits rejected method IDs for unit "
                f"{unit['unit_id']!r}: "
                + ", ".join(sorted(missing_rejected_method_ids))
            )
        expected_reason_fields = set(unit["mismatched_fields"])
        case_reason_fields = {
            field
            for case in unit_cases
            for field in case["mismatched_fields"]
        }
        if case_reason_fields != expected_reason_fields:
            missing_reason_fields = expected_reason_fields - case_reason_fields
            extra_reason_fields = case_reason_fields - expected_reason_fields
            details = []
            if missing_reason_fields:
                details.append("missing=" + ",".join(sorted(missing_reason_fields)))
            if extra_reason_fields:
                details.append("unexpected=" + ",".join(sorted(extra_reason_fields)))
            raise ContractError(
                "report unmatched_cases reason parity failed for unit "
                f"{unit['unit_id']!r}: "
                + "; ".join(details)
            )
        expected_unit_cases = unit["unmatched_case_expectations"]
        if any(
            case["unit_id"] != unit["unit_id"] for case in expected_unit_cases
        ):
            raise ContractError(
                "report unmatched_case_expectations contains a case for a different "
                f"unit under {unit['unit_id']!r}"
            )
        if sorted(map(_unmatched_case_signature, unit_cases)) != sorted(
            map(_unmatched_case_signature, expected_unit_cases)
        ):
            raise ContractError(
                "report unmatched_cases candidate-specific mismatch parity failed "
                f"for unit {unit['unit_id']!r}"
            )

        for metric_name, metric in unit["metric_coverage"].items():
            for bucket_name in ("observed_values", "controlled_values"):
                for value in metric[bucket_name]:
                    if not math.isfinite(value["value"]):
                        raise ContractError(
                            f"report {metric_name}.{bucket_name} value must be finite "
                            f"for unit {unit['unit_id']!r}"
                        )
            state_count = sum(metric["state_counts"].values()) + metric["synthetic_count"]
            if state_count != method_count:
                raise ContractError(
                    f"report {metric_name}.state_counts plus synthetic_count={state_count!r} "
                    f"does not match method count {method_count!r} for unit {unit['unit_id']!r}"
                )
            emitted_value_count = sum(
                len(metric[bucket_name])
                for bucket_name in ("observed_values", "controlled_values")
            )
            if metric["state_counts"]["known"] < emitted_value_count:
                raise ContractError(
                    f"report {metric_name}.state_counts.known does not cover emitted "
                    f"values for unit {unit['unit_id']!r}: "
                    f"known={metric['state_counts']['known']!r}, "
                    f"emitted={emitted_value_count!r}"
                )
        for metric in unit["metric_coverage"].values():
            for bucket_name, expected_origin in (
                ("observed_values", "observed"),
                ("controlled_values", "controlled"),
            ):
                for value in metric[bucket_name]:
                    if value["method_id"] not in admitted_method_ids:
                        raise ContractError(
                            f"report {bucket_name} contains method_id={value['method_id']!r} "
                            f"outside admitted bindings for unit {unit['unit_id']!r}"
                        )
                    if unit_origins_by_method[value["method_id"]] != {expected_origin}:
                        raise ContractError(
                            f"report {bucket_name} requires {expected_origin} "
                            "measurement_origin for bound method "
                            f"{value['method_id']!r} in unit {unit['unit_id']!r}"
                        )


def _require_exact_method_set(packet: dict[str, Any]) -> None:
    declared = packet["comparison"]["method_ids"]
    if len(declared) != len(set(declared)):
        raise ContractError("comparison.method_ids contains a duplicate method collision")
    if set(declared) != set(METHOD_IDS):
        raise ContractError("comparison.method_ids must contain exactly the six canonical method IDs")


def _check_prerequisites(packet: dict[str, Any]) -> None:
    required = [item for item in packet["prerequisites"] if item["required"]]
    if not required:
        raise ContractError("at least one required prerequisite must be declared")
    blocked = [item["id"] for item in required if item["status"] != "known"]
    if blocked:
        raise ContractError(f"required prerequisites are not known: {', '.join(blocked)}")


def _check_source_identity(packet: dict[str, Any]) -> None:
    if packet["source_digest"] != packet["environment"]["source_digest"]:
        raise ContractError("packet source_digest does not match environment.source_digest")
    if packet["environment"]["source_ref"] != packet["source_ref"]:
        raise ContractError("packet source_ref does not match environment.source_ref")


def _check_collisions(observations: list[dict[str, Any]]) -> None:
    seen: set[tuple[str, str]] = set()
    for observation in observations:
        key = (observation["unit_id"], observation["method_id"])
        if key in seen:
            raise ContractError(
                f"duplicate observation collision for unit_id={key[0]!r}, method_id={key[1]!r}"
            )
        seen.add(key)


def _check_observation_semantics(observations: list[dict[str, Any]]) -> None:
    for observation in observations:
        if observation["measurement_origin"] != "unobservable":
            continue
        known_metrics = [
            metric_name
            for metric_name in METRIC_NAMES
            if observation["metrics"][metric_name]["status"] == "known"
        ]
        if known_metrics:
            raise ContractError(
                "measurement_origin=unobservable cannot carry known metrics: "
                + ", ".join(known_metrics)
            )


def _check_metric_units(observations: list[dict[str, Any]]) -> None:
    for observation in observations:
        for metric_name, expected_unit in CANONICAL_METRIC_UNITS.items():
            actual_unit = observation["metrics"][metric_name]["unit"]
            if actual_unit != expected_unit:
                raise ContractError(
                    f"{metric_name} must use canonical unit {expected_unit!r}; got {actual_unit!r}"
                )


def _check_metric_finiteness(observations: list[dict[str, Any]]) -> None:
    for observation in observations:
        for metric_name in METRIC_NAMES:
            measurement = observation["metrics"][metric_name]
            if measurement["status"] == "known" and not math.isfinite(measurement["value"]):
                raise ContractError(
                    f"{metric_name} known value must be finite before admission"
                )


def _check_command_finiteness(packet: dict[str, Any]) -> None:
    if not math.isfinite(packet["command"]["timeout_seconds"]):
        raise ContractError("command.timeout_seconds must be finite before admission")


def _check_observation_evidence(packet: dict[str, Any]) -> None:
    artifacts_by_ref: dict[str, dict[str, Any]] = {}
    for artifact in packet["artifacts"]:
        ref = artifact["ref"]
        if ref in artifacts_by_ref:
            raise ContractError(f"duplicate artifact reference: {ref!r}")
        artifacts_by_ref[ref] = artifact

    for observation in packet["observations"]:
        identity_class = observation["identity"]["evidence_class"]
        for evidence_ref in observation["evidence_refs"]:
            artifact = artifacts_by_ref.get(evidence_ref)
            if artifact is None:
                raise ContractError(
                    f"observation evidence_ref is not declared in packet artifacts: {evidence_ref!r}"
                )
            artifact_kind = artifact["kind"]
            if artifact_kind not in OBSERVATION_ARTIFACT_KINDS:
                raise ContractError(
                    f"observation evidence_ref uses disallowed artifact kind: {artifact_kind!r}"
                )
            evidence_class = artifact["evidence_class"]
            if evidence_class not in ALLOWED_OBSERVATION_EVIDENCE_CLASSES:
                raise ContractError(
                    f"observation evidence_ref uses disallowed evidence class: {evidence_class!r}"
                )
            if evidence_class != identity_class:
                raise ContractError(
                    f"observation evidence class does not match identity.evidence_class for {evidence_ref!r}"
                )


def _identity_mismatches(
    baseline: dict[str, Any], candidate: dict[str, Any]
) -> list[str]:
    mismatches: list[str] = []
    for field in IDENTITY_FIELDS:
        if baseline["identity"][field] != candidate["identity"][field]:
            mismatches.append(f"identity.{field}")
    for field in ("cache_posture", "resource_posture"):
        if baseline["identity"][field]["status"] != "known":
            mismatches.append(f"identity.{field}.status")
    return mismatches


def _packet_binding_mismatches(
    observation: dict[str, Any], packet: dict[str, Any]
) -> list[str]:
    identity = observation["identity"]
    environment = packet["environment"]
    mismatches: list[str] = []
    if identity["environment_id"] != environment["environment_id"]:
        mismatches.append("identity.environment_id")
    if identity["source_ref_or_digest"] != packet["source_digest"]:
        mismatches.append("identity.source_ref_or_digest")
    for field in ("cache_posture", "resource_posture"):
        if identity[field] != environment[field]:
            mismatches.append(f"identity.{field}.packet_binding")
    return mismatches


def _jointly_known_metric_names(
    baseline: dict[str, Any], candidate: dict[str, Any]
) -> list[str]:
    return [
        metric_name
        for metric_name, expected_unit in CANONICAL_METRIC_UNITS.items()
        if baseline["metrics"][metric_name]["status"] == "known"
        and candidate["metrics"][metric_name]["status"] == "known"
        and baseline["metrics"][metric_name]["unit"]
        == candidate["metrics"][metric_name]["unit"]
        == expected_unit
    ]


def _metric_coverage(
    rows: list[dict[str, Any]],
    *,
    eligible_observed_method_ids: set[str],
    eligible_controlled_method_ids: set[str],
) -> dict[str, Any]:
    coverage: dict[str, Any] = {}
    for metric_name in METRIC_NAMES:
        status_counts = {
            "known": 0,
            "unknown": 0,
            "null": 0,
            "excluded": 0,
            "unobservable": 0,
            "missing": 0,
        }
        observed_values: list[dict[str, Any]] = []
        controlled_values: list[dict[str, Any]] = []
        synthetic_count = 0
        for row in rows:
            measurement = row["metrics"][metric_name]
            status = measurement["status"]
            origin = row["measurement_origin"]
            if status in NON_VALUE_STATUSES:
                status_counts[status] += 1
            elif origin == "synthetic":
                synthetic_count += 1
            else:
                status_counts["known"] += 1
                value = {"method_id": row["method_id"], "value": measurement["value"], "unit": measurement["unit"]}
                if origin == "observed" and row["method_id"] in eligible_observed_method_ids:
                    observed_values.append(value)
                elif (
                    origin == "controlled"
                    and row["method_id"] in eligible_controlled_method_ids
                ):
                    controlled_values.append(value)
        coverage[metric_name] = {
            "state_counts": status_counts,
            "observed_values": observed_values,
            "controlled_values": controlled_values,
            "synthetic_count": synthetic_count,
        }
    return coverage


def _identity_snapshot(identity: dict[str, Any]) -> dict[str, Any]:
    return {field: copy.deepcopy(identity[field]) for field in IDENTITY_FIELDS}


def _evidence_provenance(
    rows: tuple[dict[str, Any], ...], packet: dict[str, Any]
) -> list[dict[str, Any]]:
    artifacts_by_ref = {artifact["ref"]: artifact for artifact in packet["artifacts"]}
    provenance: list[dict[str, Any]] = []
    for row in rows:
        for evidence_ref in sorted(row["evidence_refs"]):
            artifact = artifacts_by_ref[evidence_ref]
            provenance.append(
                {
                    "method_id": row["method_id"],
                    "ref": evidence_ref,
                    "digest": artifact["digest"],
                    "kind": artifact["kind"],
                    "evidence_class": artifact["evidence_class"],
                    "measurement_origin": row["measurement_origin"],
                }
            )
    return provenance


def _matched_identity_binding(
    baseline: dict[str, Any], candidate: dict[str, Any], packet: dict[str, Any]
) -> dict[str, Any]:
    return {
        "method_ids": [baseline["method_id"], candidate["method_id"]],
        "identity": _identity_snapshot(baseline["identity"]),
        "evidence_provenance": _evidence_provenance((baseline, candidate), packet),
    }


def _unit_result(
    unit_id: str,
    rows: list[dict[str, Any]],
    baseline_method_id: str,
    packet: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    baseline_rows = [row for row in rows if row["method_id"] == baseline_method_id]
    unmatched: list[dict[str, Any]] = []
    if not baseline_rows:
        unmatched = [
            {
                "unit_id": unit_id,
                "reason": "baseline_method_missing",
                "method_id": row["method_id"],
                "mismatched_fields": ["baseline_method_id"],
            }
            for row in rows
        ]
        return (
            {
                "unit_id": unit_id,
                "disposition": "unmatched",
                "matched_pair_count": 0,
                "observed_pair_count": 0,
                "method_ids": sorted({row["method_id"] for row in rows}),
                "review_statuses": sorted({row["review_status"] for row in rows}),
                "evidence_classes": sorted({row["identity"]["evidence_class"] for row in rows}),
                "identity_match": False,
                "mismatched_fields": ["baseline_method_id"],
                "observation_refs": sorted({ref for row in rows for ref in row["evidence_refs"]}),
                "matched_identity_bindings": [],
                "unmatched_case_expectations": copy.deepcopy(unmatched),
                "metric_coverage": _metric_coverage(
                    rows,
                    eligible_observed_method_ids=set(),
                    eligible_controlled_method_ids=set(),
                ),
                "claim_limit": "no declared baseline row; no method pair admitted",
            },
            unmatched,
        )

    baseline = baseline_rows[0]
    candidates = [row for row in rows if row["method_id"] != baseline_method_id]
    if not candidates:
        reason = "comparison_candidate_missing"
        unmatched = [
            {
                "unit_id": unit_id,
                "reason": reason,
                "method_id": baseline_method_id,
                "mismatched_fields": ["comparison_candidate_method_id"],
            }
        ]
        return (
            {
                "unit_id": unit_id,
                "disposition": "unmatched",
                "matched_pair_count": 0,
                "observed_pair_count": 0,
                "method_ids": [baseline_method_id],
                "review_statuses": sorted({row["review_status"] for row in rows}),
                "evidence_classes": sorted({row["identity"]["evidence_class"] for row in rows}),
                "identity_match": False,
                "mismatched_fields": ["comparison_candidate_method_id"],
                "observation_refs": sorted({ref for row in rows for ref in row["evidence_refs"]}),
                "matched_identity_bindings": [],
                "unmatched_case_expectations": copy.deepcopy(unmatched),
                "metric_coverage": _metric_coverage(
                    rows,
                    eligible_observed_method_ids=set(),
                    eligible_controlled_method_ids=set(),
                ),
                "claim_limit": "one-sided baseline; no method pair admitted",
            },
            unmatched,
        )

    all_mismatches: list[str] = []
    pair_count = 0
    observed_pair_count = 0
    controlled_pair_count = 0
    eligible_observed_method_ids: set[str] = set()
    eligible_controlled_method_ids: set[str] = set()
    matched_identity_bindings: list[dict[str, Any]] = []
    for candidate in candidates:
        mismatches = _identity_mismatches(baseline, candidate)
        mismatches.extend(_packet_binding_mismatches(baseline, packet))
        mismatches.extend(_packet_binding_mismatches(candidate, packet))
        if baseline["review_status"] not in ALLOWED_REVIEW_STATUSES:
            mismatches.append("review_status.baseline")
        if candidate["review_status"] not in ALLOWED_REVIEW_STATUSES:
            mismatches.append(f"review_status.{candidate['method_id']}")
        if (
            baseline["measurement_origin"] == "observed"
            and baseline["review_status"] != OBSERVED_REVIEW_STATUS
        ):
            mismatches.append("review_status.baseline_observed_requires_reviewed")
        if (
            candidate["measurement_origin"] == "observed"
            and candidate["review_status"] != OBSERVED_REVIEW_STATUS
        ):
            mismatches.append(
                f"review_status.{candidate['method_id']}_observed_requires_reviewed"
            )
        if baseline["measurement_origin"] == "unobservable":
            mismatches.append("measurement_origin.baseline")
        if candidate["measurement_origin"] == "unobservable":
            mismatches.append(f"measurement_origin.{candidate['method_id']}")
        if (
            baseline["measurement_origin"] == "observed"
            and candidate["measurement_origin"] == "observed"
            and not _jointly_known_metric_names(baseline, candidate)
        ):
            mismatches.append("metric_coverage.no_jointly_known_metric")
        if mismatches:
            all_mismatches.extend(mismatches)
            unmatched.append(
                {
                    "unit_id": unit_id,
                    "reason": "identity_or_parity_mismatch",
                    "method_id": candidate["method_id"],
                    "mismatched_fields": sorted(set(mismatches)),
                }
            )
        else:
            pair_count += 1
            matched_identity_bindings.append(
                _matched_identity_binding(baseline, candidate, packet)
            )
            if baseline["measurement_origin"] == "observed" and candidate["measurement_origin"] == "observed":
                observed_pair_count += 1
                eligible_observed_method_ids.update({baseline_method_id, candidate["method_id"]})
            else:
                controlled_pair_count += 1
                eligible_controlled_method_ids.update(
                    row["method_id"]
                    for row in (baseline, candidate)
                    if row["measurement_origin"] == "controlled"
                )

    method_ids = [method_id for method_id in METHOD_IDS if method_id in {row["method_id"] for row in rows}]
    review_statuses = sorted({row["review_status"] for row in rows})
    evidence_classes = sorted({row["identity"]["evidence_class"] for row in rows})
    all_refs = {ref for row in rows for ref in row["evidence_refs"]}
    bound_refs = {
        provenance["ref"]
        for binding in matched_identity_bindings
        for provenance in binding["evidence_provenance"]
    }
    refs = sorted(bound_refs if matched_identity_bindings else all_refs)
    if observed_pair_count:
        disposition = "matched_observation_only"
        claim_limit = CLAIM_LIMIT_OBSERVED
    elif controlled_pair_count:
        disposition = "controlled_accounting_only"
        claim_limit = CLAIM_LIMIT_CONTROLLED
    else:
        disposition = "unmatched"
        claim_limit = CLAIM_LIMIT_UNMATCHED
        if not unmatched:
            unmatched.append({"unit_id": unit_id, "reason": "no_eligible_pair", "mismatched_fields": []})

    result = {
        "unit_id": unit_id,
        "disposition": disposition,
        "matched_pair_count": pair_count,
        "observed_pair_count": observed_pair_count,
        "method_ids": method_ids,
        "review_statuses": review_statuses,
        "evidence_classes": evidence_classes,
        "identity_match": pair_count > 0,
        "mismatched_fields": sorted(set(all_mismatches)),
        "observation_refs": refs,
        "matched_identity_bindings": matched_identity_bindings,
        "unmatched_case_expectations": copy.deepcopy(unmatched),
        "metric_coverage": _metric_coverage(
            rows,
            eligible_observed_method_ids=eligible_observed_method_ids,
            eligible_controlled_method_ids=eligible_controlled_method_ids,
        ),
        "claim_limit": claim_limit,
    }
    return result, unmatched


def build_report(packet: dict[str, Any]) -> dict[str, Any]:
    """Validate a packet and return a stable report payload."""

    _validate_schema(packet)
    _check_command_finiteness(packet)
    _require_exact_method_set(packet)
    _check_prerequisites(packet)
    _check_source_identity(packet)
    _check_observation_evidence(packet)
    _check_collisions(packet["observations"])
    _check_metric_units(packet["observations"])
    _check_metric_finiteness(packet["observations"])
    _check_observation_semantics(packet["observations"])

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for observation in packet["observations"]:
        grouped[observation["unit_id"]].append(observation)

    units: list[dict[str, Any]] = []
    unmatched_cases: list[dict[str, Any]] = []
    for unit_id in sorted(grouped):
        rows = sorted(grouped[unit_id], key=lambda row: row["method_id"])
        unit, unit_unmatched = _unit_result(
            unit_id,
            rows,
            packet["comparison"]["baseline_method_id"],
            packet,
        )
        units.append(unit)
        unmatched_cases.extend(unit_unmatched)

    for unit in units:
        binding_count = len(unit["matched_identity_bindings"])
        if binding_count != unit["matched_pair_count"]:
            raise ContractError(
                "matched_identity_bindings must preserve one binding per admitted pair"
            )
        if unit["disposition"] == "matched_observation_only" and binding_count == 0:
            raise ContractError(
                "matched_observation_only requires matched identity provenance"
            )

    matched_units = [unit for unit in units if unit["disposition"] == "matched_observation_only"]
    controlled_units = [unit for unit in units if unit["disposition"] == "controlled_accounting_only"]
    report = {
        "eval_name": packet["eval_name"],
        "bundle_status": "draft",
        "object_under_evaluation": "identity-bound comparison of validation methods under an explicit workload, candidate, environment, treatment, evidence, acceptance, cache, and resource contract",
        "comparison_mode": "fixed-baseline",
        "baseline_target": packet["comparison"]["baseline_method_id"],
        "method_set": list(METHOD_IDS),
        "identity_contract": {
            "required_fields": list(IDENTITY_FIELDS),
            "exact_match_required": True,
            "known_cache_and_resource_required_for_observed_pair": True,
            "allowed_evidence_classes": sorted(ALLOWED_OBSERVATION_EVIDENCE_CLASSES),
        },
        "selection_apply_contract": {
            "required_fields": [
                "verdict",
                "owner",
                "source_ref",
                "source_digest",
                "environment",
                "command.argv",
                "command.cwd",
                "command.timeout_seconds",
                "command.accepted_exit_codes",
                "prerequisites",
                "artifacts",
                "pass_criteria",
                "effect_authority",
                "expected_effect",
                "proof_authority",
                "proof_limit",
            ],
            "received_verdict": packet["verdict"],
            "ready_for_owner_apply": True,
            "proof_authority": packet["proof_authority"],
        },
        "admission": {
            "observation_count": len(packet["observations"]),
            "unit_count": len(units),
            "matched_unit_count": len(matched_units),
            "controlled_accounting_unit_count": len(controlled_units),
            "unmatched_unit_count": len(units) - len(matched_units) - len(controlled_units),
            "matched_pair_count": sum(unit["matched_pair_count"] for unit in units),
            "eligible_real_pairs": sum(unit["observed_pair_count"] for unit in units),
            "unknown_is_not_zero": True,
            "method_effect_admitted": False,
        },
        "comparison_units": units,
        "unmatched_cases": unmatched_cases,
        "verdict": "matched_observation_only" if matched_units else "not_admitted",
        "policy_verdict": None,
        "claim_boundary": REPORT_CLAIM_BOUNDARY,
        "limitations": copy.deepcopy(REPORT_LIMITATIONS),
    }
    validate_report(report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="apply packet JSON")
    parser.add_argument("--output", required=True, type=Path, help="report JSON")
    args = parser.parse_args(argv)
    packet = _load_json(args.input)
    if not isinstance(packet, dict):
        raise ContractError("apply packet root must be an object")
    report = build_report(packet)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ContractError as exc:
        raise SystemExit(f"identity-bound method comparison rejected: {exc}")
