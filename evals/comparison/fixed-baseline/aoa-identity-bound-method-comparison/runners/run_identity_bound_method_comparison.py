"""Deterministic admission/reporting for the identity-bound method ABI.

The runner consumes an explicit owner apply packet. It validates and compares
the supplied rows, but it never executes the packet command or discovers live
telemetry. A successful run is contract evidence only; it is not central proof
or owner acceptance.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
import math
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
APPLY_SCHEMA_PATH = BUNDLE_ROOT / "fixtures" / "apply-packet.schema.json"

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


def _validate_schema(payload: Any) -> None:
    schema = _load_json(APPLY_SCHEMA_PATH)
    errors = sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda error: list(error.path))
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.path) or "$"
        raise ContractError(f"apply packet schema error at {location}: {error.message}")


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
    rows: list[dict[str, Any]], *, eligible_observed_method_ids: set[str]
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
                elif origin == "controlled":
                    controlled_values.append(value)
        coverage[metric_name] = {
            "state_counts": status_counts,
            "observed_values": observed_values,
            "controlled_values": controlled_values,
            "synthetic_count": synthetic_count,
        }
    return coverage


def _unit_result(
    unit_id: str,
    rows: list[dict[str, Any]],
    baseline_method_id: str,
    packet: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    baseline_rows = [row for row in rows if row["method_id"] == baseline_method_id]
    unmatched: list[dict[str, Any]] = []
    if not baseline_rows:
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
                "metric_coverage": _metric_coverage(rows, eligible_observed_method_ids=set()),
                "claim_limit": "no declared baseline row; no method pair admitted",
            },
            [{"unit_id": unit_id, "reason": "baseline_method_missing", "mismatched_fields": ["baseline_method_id"]}],
        )

    baseline = baseline_rows[0]
    candidates = [row for row in rows if row["method_id"] != baseline_method_id]
    if not candidates:
        reason = "comparison_candidate_missing"
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
                "metric_coverage": _metric_coverage(rows, eligible_observed_method_ids=set()),
                "claim_limit": "one-sided baseline; no method pair admitted",
            },
            [{"unit_id": unit_id, "reason": reason, "mismatched_fields": ["comparison_candidate_method_id"]}],
        )

    all_mismatches: list[str] = []
    pair_count = 0
    observed_pair_count = 0
    controlled_pair_count = 0
    eligible_observed_method_ids: set[str] = set()
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
            if baseline["measurement_origin"] == "observed" and candidate["measurement_origin"] == "observed":
                observed_pair_count += 1
                eligible_observed_method_ids.update({baseline_method_id, candidate["method_id"]})
            else:
                controlled_pair_count += 1

    method_ids = [method_id for method_id in METHOD_IDS if method_id in {row["method_id"] for row in rows}]
    review_statuses = sorted({row["review_status"] for row in rows})
    evidence_classes = sorted({row["identity"]["evidence_class"] for row in rows})
    refs = sorted({ref for row in rows for ref in row["evidence_refs"]})
    if observed_pair_count:
        disposition = "matched_observation_only"
        claim_limit = "identity-bound observation pair only; no effect, proof, policy, or winner claim"
    elif controlled_pair_count:
        disposition = "controlled_accounting_only"
        claim_limit = "identity-matched accounting only; controlled or synthetic values are not observed effect"
    else:
        disposition = "unmatched"
        claim_limit = "no eligible identity- and parity-matched method pair"
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
        "metric_coverage": _metric_coverage(
            rows, eligible_observed_method_ids=eligible_observed_method_ids
        ),
        "claim_limit": claim_limit,
    }
    return result, unmatched


def build_report(packet: dict[str, Any]) -> dict[str, Any]:
    """Validate a packet and return a stable report payload."""

    _validate_schema(packet)
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
    for unit_id, rows in grouped.items():
        unit, unit_unmatched = _unit_result(
            unit_id,
            rows,
            packet["comparison"]["baseline_method_id"],
            packet,
        )
        units.append(unit)
        unmatched_cases.extend(unit_unmatched)

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
        "claim_boundary": "This report preserves identity-bound observation or accounting dispositions only; it does not issue method effects, causal claims, proof, policy, acceptance, or a universal winner.",
        "limitations": [
            "the runner consumes an explicit packet and never executes command.argv",
            "a generated reader or green validator is not real-session telemetry",
            "synthetic and controlled values are excluded from observed_values",
            "unknown, null, excluded, unobservable, and missing states are not zero",
            "no central proof, runtime health, policy, or human-acceptance verdict is emitted",
        ],
    }
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
