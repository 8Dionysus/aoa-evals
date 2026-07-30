#!/usr/bin/env python3
"""Validate the C21-C23 active-organ experiment control contracts."""

from __future__ import annotations

import argparse
import copy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


PART_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = PART_ROOT / "schemas"
EXAMPLE_ROOT = PART_ROOT / "examples"

SCHEMA_PATHS = {
    "C21": SCHEMA_ROOT
    / "active-organ-model-prompt-provider-hardware-pin.schema.json",
    "C22": SCHEMA_ROOT / "active-organ-memory-experiment-manifest.schema.json",
    "C23": SCHEMA_ROOT / "active-organ-memory-run-status-receipt.schema.json",
}
POSITIVE_EXAMPLES = (
    EXAMPLE_ROOT / "active_organ_model_prompt_provider_hardware_pin.example.json",
    EXAMPLE_ROOT / "active_organ_memory_experiment_manifest.example.json",
    EXAMPLE_ROOT / "active_organ_memory_run_status_receipt.complete.example.json",
    EXAMPLE_ROOT / "active_organ_memory_run_status_receipt.partial.example.json",
    EXAMPLE_ROOT / "active_organ_memory_run_status_receipt.invalid.example.json",
    EXAMPLE_ROOT / "active_organ_memory_run_status_receipt.aborted.example.json",
    EXAMPLE_ROOT / "active_organ_memory_run_status_receipt.blocked.example.json",
)
NEGATIVE_EXAMPLES = (
    EXAMPLE_ROOT / "active_organ_experiment_contracts.negative-examples.json"
)

EXPECTED_ARMS = {
    "A": "memory_disabled",
    "B": "explicit_pull_only",
    "C": "active_organ_policy_gated",
}
REQUIRED_METRIC_AXES = {"cost", "quality", "latency", "outcome"}
RUN_STATUSES = {"complete", "partial", "invalid", "aborted", "blocked"}


class ContractError(ValueError):
    """Raised when a schema-valid payload violates cross-field semantics."""


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validators() -> dict[str, Draft202012Validator]:
    result: dict[str, Draft202012Validator] = {}
    for contract_id, path in SCHEMA_PATHS.items():
        schema = load_json(path)
        Draft202012Validator.check_schema(schema)
        result[contract_id] = Draft202012Validator(
            schema,
            format_checker=FormatChecker(),
        )
    return result


def _schema_error(
    validator: Draft202012Validator,
    payload: Any,
) -> str | None:
    errors = sorted(
        validator.iter_errors(payload),
        key=lambda error: [str(part) for part in error.absolute_path],
    )
    if not errors:
        return None
    error = errors[0]
    path = "/".join(str(part) for part in error.absolute_path) or "<root>"
    return f"{path}: {error.message}"


def _require(condition: bool, path: str, message: str) -> None:
    if not condition:
        raise ContractError(f"{path}: {message}")


def _unique_strings(items: list[dict[str, Any]], field: str, path: str) -> None:
    values = [item.get(field) for item in items]
    _require(len(values) == len(set(values)), path, f"{field} values must be unique")


def normalized_c22_manifest_sha256(payload: dict[str, Any]) -> str:
    """Hash C22 after replacing its self-digest field with the v1 zero token."""
    normalized = copy.deepcopy(payload)
    normalized["preregistration"]["manifest_sha256"] = "sha256:" + "0" * 64
    encoded = (
        json.dumps(
            normalized,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _validate_c21(payload: dict[str, Any]) -> None:
    _require(
        payload["authority"]["evidence_only"] is True,
        "authority/evidence_only",
        "C21 is evidence only",
    )
    _require(
        payload["privacy"]["refs_only"] is True,
        "privacy/refs_only",
        "C21 must persist references only",
    )


def _validate_c22(payload: dict[str, Any]) -> None:
    arms = payload["arms"]
    arm_ids = [arm["arm_id"] for arm in arms]
    _require(
        len(arms) == 3 and set(arm_ids) == set(EXPECTED_ARMS),
        "arms",
        "exactly one A, B, and C arm is required",
    )
    _require(len(arm_ids) == len(set(arm_ids)), "arms", "arm_id values must be unique")

    by_id = {arm["arm_id"]: arm for arm in arms}
    for arm_id, expected_treatment in EXPECTED_ARMS.items():
        _require(
            by_id[arm_id]["memory_treatment"] == expected_treatment,
            f"arms/{arm_id}/memory_treatment",
            f"must be {expected_treatment}",
        )

    reference_fields = (
        "memory_policy_ref",
        "recall_policy_ref",
        "intervention_policy_ref",
        "forgetting_policy_ref",
    )
    for field in reference_fields:
        _require(
            by_id["A"][field] is None,
            f"arms/A/{field}",
            "memory-disabled control must not carry a memory policy reference",
        )
        for arm_id in ("B", "C"):
            _require(
                isinstance(by_id[arm_id][field], str) and bool(by_id[arm_id][field]),
                f"arms/{arm_id}/{field}",
                "memory treatment must carry an explicit owner reference",
            )

    metrics = payload["metrics"]
    _unique_strings(metrics, "metric_id", "metrics")
    axes = {metric["axis"] for metric in metrics}
    _require(
        REQUIRED_METRIC_AXES <= axes,
        "metrics",
        "cost, quality, latency, and outcome axes are all required",
    )
    _unique_strings(payload["falsifiers"], "falsifier_id", "falsifiers")
    _unique_strings(payload["stop_conditions"], "condition_id", "stop_conditions")

    covered_arms = {
        arm_id
        for pin in payload["environment_pins"]
        for arm_id in pin["applies_to_arms"]
    }
    _require(
        set(EXPECTED_ARMS) <= covered_arms,
        "environment_pins",
        "every A/B/C arm must be covered by an exact environment pin",
    )
    _require(
        payload["preregistration"]["manifest_sha256"]
        == normalized_c22_manifest_sha256(payload),
        "preregistration/manifest_sha256",
        (
            "must equal the canonical v1 self-digest with "
            "preregistration.manifest_sha256 replaced by sha256 plus 64 zeroes"
        ),
    )


def _parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _validate_c23(payload: dict[str, Any]) -> None:
    status = payload["run_status"]
    _require(status in RUN_STATUSES, "run_status", "unknown run status")
    _require(
        payload["benefit_claim_state"] == "not_established_by_run_status",
        "benefit_claim_state",
        "run status cannot establish benefit",
    )

    started_at = _parse_timestamp(payload["started_at"])
    recorded_at = _parse_timestamp(payload["recorded_at"])
    ended_value = payload["ended_at"]
    ended_at = _parse_timestamp(ended_value) if ended_value is not None else None
    if ended_at is not None:
        _require(ended_at >= started_at, "ended_at", "must not precede started_at")
        _require(recorded_at >= ended_at, "recorded_at", "must not precede ended_at")
    else:
        _require(recorded_at >= started_at, "recorded_at", "must not precede started_at")

    checks = payload["checks"]
    if status == "complete":
        _require(ended_at is not None, "ended_at", "complete run must have ended")
        _require(
            payload["process_exit_code"] == 0,
            "process_exit_code",
            "complete run must exit zero",
        )
        for field in ("execution_complete", "usable_for_comparison", "green_process"):
            _require(payload[field] is True, field, "complete run must set this true")
        for field in ("skipped", "blocked"):
            _require(not checks[field], f"checks/{field}", "complete run must be empty")
        for field in ("missing_evidence", "invalidation_reasons"):
            _require(not payload[field], field, "complete run must be empty")
        for field in ("evidence_refs", "output_refs", "measurement_refs"):
            _require(bool(payload[field]), field, "complete run requires this evidence")

    elif status == "partial":
        _require(
            payload["execution_complete"] is False,
            "execution_complete",
            "partial run cannot be complete",
        )
        _require(
            payload["usable_for_comparison"] is False,
            "usable_for_comparison",
            "partial run cannot be comparable",
        )
        _require(
            bool(checks["skipped"] or checks["blocked"] or payload["missing_evidence"]),
            "missing_evidence",
            "partial run must state skipped, blocked, or missing evidence",
        )

    elif status == "invalid":
        _require(
            payload["usable_for_comparison"] is False,
            "usable_for_comparison",
            "invalid run cannot be comparable",
        )
        _require(
            bool(payload["invalidation_reasons"]),
            "invalidation_reasons",
            "invalid run must state at least one reason",
        )

    elif status == "aborted":
        _require(ended_at is not None, "ended_at", "aborted run must have ended")
        for field in ("execution_complete", "usable_for_comparison", "green_process"):
            _require(payload[field] is False, field, "aborted run must set this false")
        _require(
            bool(payload["stop_condition_refs"]),
            "stop_condition_refs",
            "aborted run must identify its stop condition",
        )

    elif status == "blocked":
        for field in ("execution_complete", "usable_for_comparison", "green_process"):
            _require(payload[field] is False, field, "blocked run must set this false")
        _require(
            bool(checks["blocked"]),
            "checks/blocked",
            "blocked run must identify a blocked check",
        )
        _require(
            bool(payload["missing_evidence"]),
            "missing_evidence",
            "blocked run must identify missing evidence",
        )

    if payload["arm_id"] == "A":
        _require(
            not payload["runtime_delivery_receipt_refs"],
            "runtime_delivery_receipt_refs",
            "memory-disabled arm must not cite active-organ delivery",
        )


def validate_payload(
    payload: Any,
    schema_validators: dict[str, Draft202012Validator] | None = None,
) -> None:
    _require(isinstance(payload, dict), "<root>", "payload must be an object")
    contract_id = payload.get("contract_id")
    active_validators = schema_validators or validators()
    _require(
        contract_id in active_validators,
        "contract_id",
        "must identify C21, C22, or C23",
    )
    schema_problem = _schema_error(active_validators[contract_id], payload)
    if schema_problem:
        raise ContractError(schema_problem)
    if contract_id == "C21":
        _validate_c21(payload)
    elif contract_id == "C22":
        _validate_c22(payload)
    else:
        _validate_c23(payload)


def apply_json_pointer(payload: Any, pointer: str, value: Any) -> None:
    _require(pointer.startswith("/"), "negative_case/set", "must be a JSON pointer")
    parts = [
        part.replace("~1", "/").replace("~0", "~")
        for part in pointer.lstrip("/").split("/")
    ]
    target = payload
    for part in parts[:-1]:
        if isinstance(target, list):
            target = target[int(part)]
        else:
            target = target[part]
    leaf = parts[-1]
    if isinstance(target, list):
        target[int(leaf)] = value
    else:
        target[leaf] = value


def validate_negative_cases(
    schema_validators: dict[str, Draft202012Validator] | None = None,
) -> int:
    active_validators = schema_validators or validators()
    corpus = load_json(NEGATIVE_EXAMPLES)
    cases = corpus.get("cases")
    _require(isinstance(cases, list) and bool(cases), "cases", "must be non-empty")
    seen: set[str] = set()
    for case in cases:
        case_id = case["case_id"]
        _require(case_id not in seen, "cases", f"duplicate case_id {case_id}")
        seen.add(case_id)
        payload = copy.deepcopy(load_json(EXAMPLE_ROOT / case["base_example"]))
        for pointer, value in case["set"].items():
            apply_json_pointer(payload, pointer, value)
        try:
            validate_payload(payload, active_validators)
        except ContractError as exc:
            _require(
                case["expected_error"] in str(exc),
                f"cases/{case_id}/expected_error",
                f"expected {case['expected_error']!r}, got {str(exc)!r}",
            )
        else:
            raise ContractError(
                f"cases/{case_id}: negative case unexpectedly passed validation"
            )
    return len(cases)


def validate_all() -> dict[str, Any]:
    active_validators = validators()
    statuses: set[str] = set()
    contract_counts = {"C21": 0, "C22": 0, "C23": 0}
    for path in POSITIVE_EXAMPLES:
        payload = load_json(path)
        validate_payload(payload, active_validators)
        contract_counts[payload["contract_id"]] += 1
        if payload["contract_id"] == "C23":
            statuses.add(payload["run_status"])
    _require(statuses == RUN_STATUSES, "examples", "all five C23 statuses are required")
    negative_count = validate_negative_cases(active_validators)
    return {
        "ok": True,
        "contracts": contract_counts,
        "c23_statuses": sorted(statuses),
        "negative_cases": negative_count,
        "claim_limit": "validation_only_no_benefit_or_production_authority",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON output")
    args = parser.parse_args(argv)
    try:
        result = validate_all()
    except (ContractError, KeyError, IndexError, TypeError, ValueError) as exc:
        print(f"active-organ experiment contracts: invalid: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
