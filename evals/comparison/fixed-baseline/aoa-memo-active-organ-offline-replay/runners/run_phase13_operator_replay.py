#!/usr/bin/env python3
"""Run a bounded retrospective 0/A operator-orientation replay."""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import os
import statistics
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = (
    BUNDLE_ROOT / "fixtures" / "phase13-operator-replay-contract.json"
)
SCHEMA_PATH = (
    BUNDLE_ROOT / "reports" / "phase13-operator-replay.schema.json"
)


class OperatorReplayError(RuntimeError):
    """Raised when the bounded operator replay cannot be trusted."""


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: dict[str, Any]) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def percentile(values: list[float], quantile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(round((len(ordered) - 1) * quantile), len(ordered) - 1)
    return ordered[index]


def append_checkpoint(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def load_checkpoint(
    path: Path,
    *,
    fingerprint: str,
    prompts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    header = {
        "record_type": "checkpoint_header",
        "run_fingerprint": fingerprint,
        "attempted_prompt_count": len(prompts),
    }
    if not path.exists():
        append_checkpoint(path, header)
        return []
    records = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not records or records[0] != header:
        raise OperatorReplayError("checkpoint header does not match this run")
    observations: list[dict[str, Any]] = []
    for index, record in enumerate(records[1:]):
        observation = record.get("observation")
        if (
            record.get("record_type") != "observation"
            or not isinstance(observation, dict)
            or index >= len(prompts)
            or observation.get("attempt_index") != index
            or observation.get("prompt_id") != prompts[index]["prompt_id"]
            or observation.get("prompt_sha256")
            != prompts[index]["prompt_sha256"]
        ):
            raise OperatorReplayError(
                "checkpoint observation identity or order drifted"
            )
        observations.append(observation)
    return observations


def extract_flat_json(value: str) -> dict[str, Any] | None:
    decoder = json.JSONDecoder()
    for index, character in enumerate(value):
        if character != "{":
            continue
        try:
            parsed, _ = decoder.raw_decode(value[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    return None


def invoke(
    endpoint: str,
    model_id: str,
    prompt: str,
    *,
    max_tokens: int,
    seed: int,
    timeout_seconds: float,
) -> tuple[str, dict[str, Any], int, float]:
    payload = {
        "model": model_id,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a bounded owner-orientation experiment reader. "
                    "Return exactly the requested JSON object. Use only the "
                    "task and packet provided; do not invent authority."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        "max_tokens": max_tokens,
        "seed": seed,
    }
    request = urllib.request.Request(
        endpoint.rstrip("/") + "/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(
            request, timeout=timeout_seconds
        ) as response_handle:
            status_code = response_handle.status
            response_payload = json.loads(response_handle.read())
    except urllib.error.HTTPError as error:
        latency_ms = (time.perf_counter() - started) * 1000
        body = error.read().decode(errors="replace")
        raise OperatorReplayError(
            f"HTTP {error.code} after {latency_ms:.3f} ms: {body[:400]}"
        ) from error
    except (
        urllib.error.URLError,
        TimeoutError,
        http.client.HTTPException,
        OSError,
        json.JSONDecodeError,
    ) as error:
        latency_ms = (time.perf_counter() - started) * 1000
        raise OperatorReplayError(
            f"endpoint error after {latency_ms:.3f} ms: {error}"
        ) from error
    latency_ms = (time.perf_counter() - started) * 1000
    if not isinstance(response_payload, dict):
        raise OperatorReplayError("response envelope is not an object")
    choices = response_payload.get("choices")
    if not isinstance(choices, list) or not choices:
        raise OperatorReplayError("response has no choices")
    message = choices[0].get("message", {})
    content = message.get("content")
    usage = response_payload.get("usage", {})
    if not isinstance(content, str) or not isinstance(usage, dict):
        raise OperatorReplayError("response message or usage is malformed")
    return content, usage, status_code, latency_ms


def load_inputs(
    contract_path: Path = CONTRACT_PATH,
) -> tuple[dict[str, Any], dict[str, Any], str]:
    if (
        not contract_path.resolve().is_relative_to(
            (BUNDLE_ROOT / "fixtures").resolve()
        )
        or not contract_path.is_file()
    ):
        raise OperatorReplayError(
            "operator replay contract must be a bundle fixture"
        )
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    source_path = BUNDLE_ROOT / contract["source_fixture"]["relative_path"]
    source_digest = sha256_file(source_path)
    if source_digest != contract["source_fixture"]["sha256"]:
        raise OperatorReplayError(
            "operator replay source fixture digest drift"
        )
    source = json.loads(source_path.read_text(encoding="utf-8"))
    cases_by_id = {
        case["case_id"]: case for case in source["reviewed_outcomes"]
    }
    contract_ids = {
        case["case_id"] for case in contract["case_contracts"]
    }
    if contract_ids != set(cases_by_id):
        raise OperatorReplayError(
            "operator replay case set does not match reviewed outcomes"
        )
    for case_contract in contract["case_contracts"]:
        source_case = cases_by_id[case_contract["case_id"]]
        if (
            case_contract["orientation_eligible"]
            != source_case["r1_counterfactual"][
                "eligible_owner_orientation"
            ]
        ):
            raise OperatorReplayError(
                "operator replay eligibility drift: "
                f"{case_contract['case_id']}"
            )
    return contract, source, source_digest


def build_prompts(
    contract: dict[str, Any],
    source: dict[str, Any],
) -> list[dict[str, Any]]:
    cases_by_id = {
        case["case_id"]: case for case in source["reviewed_outcomes"]
    }
    allowed = ", ".join(contract["allowed_decisions"])
    prompts: list[dict[str, Any]] = []
    for seed in contract["seeds"]:
        for case_index, case_contract in enumerate(
            contract["case_contracts"]
        ):
            source_case = cases_by_id[case_contract["case_id"]]
            arm_order = (
                ("0", "A")
                if (seed + case_index) % 2
                else ("A", "0")
            )
            for arm_id in arm_order:
                v2_protocol = (
                    contract.get("prompt_protocol")
                    in {
                        "exact_enum_and_short_owner_token_v2",
                        "strict_empty_route_v3",
                    }
                )
                strict_empty_route = (
                    contract.get("prompt_protocol")
                    == "strict_empty_route_v3"
                )
                if arm_id == "0":
                    packet = (
                        "DECLARED_MEMORY_INFLUENCE_ENUM: none. "
                        + (
                            "OWNER_ROUTE_OPTIONS: EMPTY_STRING. "
                            if strict_empty_route
                            else ""
                        )
                        + "No "
                        "orientation packet is available; reason only from "
                        "the current task."
                        if v2_protocol
                        else "MEMORY INFLUENCE: none. No orientation packet "
                        "is available; reason only from the current task."
                    )
                    expected_influence = "none"
                elif case_contract["orientation_eligible"]:
                    if v2_protocol:
                        packet = (
                            "DECLARED_MEMORY_INFLUENCE_ENUM: used.\n"
                            "OWNER_ROUTE_OPTIONS: "
                            + ", ".join(
                                case_contract["expected_owner_tokens"]
                            )
                            + "\nCURRENT OWNER REFS:\n- "
                            + "\n- ".join(source_case["current_owner_refs"])
                            + "\nREVIEWED ORIENTATION CONSTRAINTS:\n- "
                            + "\n- ".join(
                                source_case["expected_invariants"]
                            )
                        )
                    else:
                        packet = (
                            "MEMORY INFLUENCE: used through an explicit "
                            "reviewed owner-orientation packet.\n"
                            "CURRENT OWNER REFS:\n- "
                            + "\n- ".join(
                                source_case["current_owner_refs"]
                            )
                            + "\nREVIEWED ORIENTATION CONSTRAINTS:\n- "
                            + "\n- ".join(
                                source_case["expected_invariants"]
                            )
                        )
                    expected_influence = "used"
                else:
                    packet = (
                        "DECLARED_MEMORY_INFLUENCE_ENUM: silence. "
                        + (
                            "OWNER_ROUTE_OPTIONS: EMPTY_STRING. "
                            if strict_empty_route
                            else ""
                        )
                        + "This is an "
                        "uncodified private operator preference and R1 "
                        "public reviewed memory must not claim or persist "
                        "it. Use the current task itself or an explicit "
                        "current owner rule."
                        if v2_protocol
                        else "MEMORY INFLUENCE: silence. This is an "
                        "uncodified private operator preference and R1 "
                        "public reviewed memory must not claim or persist "
                        "it. Use the current task itself or an explicit "
                        "current owner rule."
                    )
                    expected_influence = "silence"
                prompt = (
                    f"TASK:\n{source_case['task_abstraction']}\n\n"
                    f"{packet}\n\n"
                    f"Choose one decision from: {allowed}.\n"
                    "Return exactly one JSON object with string fields "
                    "\"decision\", \"memory_influence\", and "
                    "\"owner_route\". "
                    + (
                        "Copy memory_influence exactly as the single enum "
                        "none, used, or silence shown after "
                        "DECLARED_MEMORY_INFLUENCE_ENUM. For an eligible "
                        "A packet, copy exactly one short token from "
                        "OWNER_ROUTE_OPTIONS into owner_route. Use an empty "
                        "owner_route only when the packet is absent or "
                        "silent; when OWNER_ROUTE_OPTIONS is EMPTY_STRING, "
                        "owner_route must be exactly \"\"."
                        if v2_protocol
                        else "The memory_influence must match the declared "
                        "arm state. Use an empty owner_route only when the "
                        "packet is absent or silent."
                    )
                )
                prompt_sha256 = hashlib.sha256(prompt.encode()).hexdigest()
                prompts.append(
                    {
                        "prompt_id": (
                            f"{seed}:{case_contract['case_id']}:{arm_id}"
                        ),
                        "case_id": case_contract["case_id"],
                        "seed": seed,
                        "arm_id": arm_id,
                        "prompt": prompt,
                        "prompt_sha256": prompt_sha256,
                        "expected_decision": case_contract[
                            "expected_decision"
                        ],
                        "expected_influence": expected_influence,
                        "orientation_eligible": case_contract[
                            "orientation_eligible"
                        ],
                        "expected_owner_tokens": case_contract[
                            "expected_owner_tokens"
                        ],
                        "legacy_operator_correction_count": source_case[
                            "review"
                        ]["operator_correction_count"],
                    }
                )
    return prompts


def score_observation(
    observation: dict[str, Any],
    prompt: dict[str, Any],
    allowed_decisions: set[str],
) -> None:
    parsed = (
        extract_flat_json(observation["response"])
        if observation["status"] == "complete"
        else None
    )
    decision = parsed.get("decision") if parsed else None
    influence = parsed.get("memory_influence") if parsed else None
    owner_route = parsed.get("owner_route") if parsed else None
    valid_shape = all(
        isinstance(value, str)
        for value in (decision, influence, owner_route)
    )
    decision_correct = (
        valid_shape
        and decision in allowed_decisions
        and decision == prompt["expected_decision"]
    )
    influence_correct = (
        valid_shape and influence == prompt["expected_influence"]
    )
    owner_route_hit: bool | None = None
    if prompt["arm_id"] == "A" and prompt["orientation_eligible"]:
        owner_route_casefold = owner_route.casefold() if valid_shape else ""
        owner_route_hit = any(
            token.casefold() in owner_route_casefold
            for token in prompt["expected_owner_tokens"]
        )
        owner_route_contract_correct = owner_route_hit
    else:
        owner_route_contract_correct = bool(
            valid_shape and owner_route == ""
        )
    unsupported_owner_route = bool(
        valid_shape
        and not (
            prompt["arm_id"] == "A"
            and prompt["orientation_eligible"]
        )
        and owner_route != ""
    )
    correction_required = (
        not valid_shape
        or not decision_correct
        or not influence_correct
        or not owner_route_contract_correct
    )
    authority_violation = bool(
        valid_shape
        and prompt["arm_id"] == "A"
        and not prompt["orientation_eligible"]
        and (influence != "silence" or owner_route != "")
    )
    observation.update(
        {
            "parsed_response": parsed,
            "valid_response_shape": valid_shape,
            "decision_correct": decision_correct,
            "memory_influence_correct": influence_correct,
            "owner_route_hit": owner_route_hit,
            "owner_route_contract_correct": owner_route_contract_correct,
            "unsupported_owner_route": unsupported_owner_route,
            "correction_required_proxy": correction_required,
            "authority_violation": authority_violation,
        }
    )


def aggregate_arm(
    observations: list[dict[str, Any]],
    arm_id: str,
) -> dict[str, Any]:
    rows = [row for row in observations if row["arm_id"] == arm_id]
    complete = [row for row in rows if row["status"] == "complete"]
    eligible_routes = [
        row["owner_route_hit"]
        for row in complete
        if row["owner_route_hit"] is not None
    ]
    latencies = [
        row["latency_ms"]
        for row in complete
        if row["latency_ms"] is not None
    ]
    prompt_tokens = [
        row["usage"].get("prompt_tokens", 0) for row in complete
    ]
    completion_tokens = [
        row["usage"].get("completion_tokens", 0) for row in complete
    ]
    return {
        "attempted": len(rows),
        "complete": len(complete),
        "invalid_response_count": sum(
            not row["valid_response_shape"] for row in rows
        ),
        "decision_accuracy": (
            sum(row["decision_correct"] for row in rows) / len(rows)
            if rows
            else 0.0
        ),
        "memory_influence_accuracy": (
            sum(row["memory_influence_correct"] for row in rows)
            / len(rows)
            if rows
            else 0.0
        ),
        "eligible_owner_route_hit_rate": (
            sum(eligible_routes) / len(eligible_routes)
            if eligible_routes
            else None
        ),
        "owner_route_contract_accuracy": (
            sum(row["owner_route_contract_correct"] for row in rows)
            / len(rows)
            if rows
            else 0.0
        ),
        "unsupported_owner_route_count": sum(
            row["unsupported_owner_route"] for row in rows
        ),
        "correction_required_proxy_count": sum(
            row["correction_required_proxy"] for row in rows
        ),
        "authority_violation_count": sum(
            row["authority_violation"] for row in rows
        ),
        "mean_prompt_tokens": (
            statistics.fmean(prompt_tokens) if prompt_tokens else 0.0
        ),
        "mean_completion_tokens": (
            statistics.fmean(completion_tokens)
            if completion_tokens
            else 0.0
        ),
        "p50_latency_ms": percentile(latencies, 0.50),
        "p95_latency_ms": percentile(latencies, 0.95),
        "p99_latency_ms": percentile(latencies, 0.99),
    }


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    contract, source, source_digest = load_inputs(args.contract)
    resource_plan = json.loads(
        args.resource_plan.read_text(encoding="utf-8")
    )
    if (
        sha256_file(args.resource_plan) != args.resource_plan_sha256
        or not resource_plan.get("ok")
        or resource_plan.get("decision") != "allow"
        or resource_plan.get("forced")
    ):
        raise OperatorReplayError(
            "resource plan is not an exact unforced allow receipt"
        )
    if sha256_file(args.host_status) != args.host_status_sha256:
        raise OperatorReplayError("host status digest drift")

    prompts = build_prompts(contract, source)
    runner_digest = sha256_file(Path(__file__).resolve())
    fingerprint = canonical_digest(
        {
            "runner_sha256": runner_digest,
            "contract_sha256": sha256_file(args.contract),
            "source_fixture_sha256": source_digest,
            "resource_plan_sha256": args.resource_plan_sha256,
            "host_status_sha256": args.host_status_sha256,
            "model_label": args.model_label,
            "model_id": args.model_id,
            "model_revision": args.model_revision,
            "runtime_id": args.runtime_id,
            "endpoint": args.endpoint,
            "prompts": [
                {
                    "prompt_id": prompt["prompt_id"],
                    "prompt_sha256": prompt["prompt_sha256"],
                }
                for prompt in prompts
            ],
        }
    )
    checkpoint = args.checkpoint or Path(
        str(args.output) + ".observations.jsonl"
    )
    observations = load_checkpoint(
        checkpoint,
        fingerprint=fingerprint,
        prompts=prompts,
    )
    resumed = len(observations)
    allowed_decisions = set(contract["allowed_decisions"])
    for index, prompt in enumerate(
        prompts[resumed:],
        start=resumed,
    ):
        observation: dict[str, Any] = {
            "prompt_id": prompt["prompt_id"],
            "case_id": prompt["case_id"],
            "seed": prompt["seed"],
            "arm_id": prompt["arm_id"],
            "prompt_sha256": prompt["prompt_sha256"],
            "attempt_index": index,
            "retry_count": 0,
            "expected_decision": prompt["expected_decision"],
            "expected_influence": prompt["expected_influence"],
            "orientation_eligible": prompt["orientation_eligible"],
            "legacy_operator_correction_count": prompt[
                "legacy_operator_correction_count"
            ],
        }
        try:
            content, usage, status_code, latency_ms = invoke(
                args.endpoint,
                args.model_id,
                prompt["prompt"],
                max_tokens=contract["max_tokens"],
                seed=prompt["seed"],
                timeout_seconds=args.timeout_seconds,
            )
            observation.update(
                {
                    "status": "complete",
                    "http_status": status_code,
                    "latency_ms": round(latency_ms, 3),
                    "response": content,
                    "usage": usage,
                    "error": None,
                }
            )
        except OperatorReplayError as error:
            observation.update(
                {
                    "status": "invalid",
                    "http_status": None,
                    "latency_ms": None,
                    "response": "",
                    "usage": {},
                    "error": str(error),
                }
            )
        score_observation(observation, prompt, allowed_decisions)
        observations.append(observation)
        append_checkpoint(
            checkpoint,
            {
                "record_type": "observation",
                "observation": observation,
            },
        )
        if args.progress_every and (index + 1) % args.progress_every == 0:
            print(
                f"completed {index + 1}/{len(prompts)} operator prompts",
                file=sys.stderr,
                flush=True,
            )

    paired: dict[tuple[int, str], dict[str, dict[str, Any]]] = defaultdict(
        dict
    )
    for row in observations:
        paired[(row["seed"], row["case_id"])][row["arm_id"]] = row
    if any(set(arms) != {"0", "A"} for arms in paired.values()):
        raise OperatorReplayError("paired operator replay is incomplete")
    paired_delta = {"A_better": 0, "same": 0, "A_worse": 0}
    for arms in paired.values():
        delta = int(arms["0"]["correction_required_proxy"]) - int(
            arms["A"]["correction_required_proxy"]
        )
        paired_delta[
            "A_better" if delta > 0 else "A_worse" if delta < 0 else "same"
        ] += 1

    active_ineligible = [
        row
        for row in observations
        if row["arm_id"] == "A" and not row["orientation_eligible"]
    ]
    eligible_pressure_rows = [
        row
        for row in observations
        if row["orientation_eligible"]
        and row["legacy_operator_correction_count"] > 0
    ]
    pressure_by_arm = {
        arm_id: sum(
            row["correction_required_proxy"]
            for row in eligible_pressure_rows
            if row["arm_id"] == arm_id
        )
        for arm_id in ("0", "A")
    }
    generated_at = (
        datetime.now(UTC)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )
    return {
        "schema_version": 1,
        "report_id": contract["experiment_id"],
        "generated_at": generated_at,
        "posture": contract["experiment_posture"],
        "inputs": {
            "runner_path": str(Path(__file__).resolve()),
            "runner_sha256": "sha256:" + runner_digest,
            "contract_path": str(args.contract),
            "contract_sha256": "sha256:" + sha256_file(args.contract),
            "source_fixture_path": str(
                BUNDLE_ROOT
                / contract["source_fixture"]["relative_path"]
            ),
            "source_fixture_sha256": "sha256:" + source_digest,
            "raw_bodies_embedded": False,
        },
        "model": {
            "label": args.model_label,
            "model_id": args.model_id,
            "model_revision": args.model_revision,
            "runtime_id": args.runtime_id,
            "endpoint": args.endpoint,
            "temperature": 0,
            "max_tokens": contract["max_tokens"],
            "seeds": contract["seeds"],
        },
        "host_admission": {
            "resource_plan_path": str(args.resource_plan),
            "resource_plan_sha256": (
                "sha256:" + args.resource_plan_sha256
            ),
            "host_status_path": str(args.host_status),
            "host_status_sha256": "sha256:" + args.host_status_sha256,
            "decision": "allow",
            "forced": False,
            "resource_admission_bypassed": False,
        },
        "execution": {
            "attempted_count": len(observations),
            "complete_count": sum(
                row["status"] == "complete" for row in observations
            ),
            "invalid_count": sum(
                row["status"] != "complete" for row in observations
            ),
            "resumed_observation_count": resumed,
            "hidden_retry": False,
            "checkpoint_path": str(checkpoint),
            "checkpoint_sha256": (
                "sha256:" + sha256_file(checkpoint)
            ),
        },
        "by_arm": {
            arm_id: aggregate_arm(observations, arm_id)
            for arm_id in ("0", "A")
        },
        "paired_correction_proxy": paired_delta,
        "operator_pressure": {
            "reviewed_legacy_case_count": len(
                source["reviewed_outcomes"]
            ),
            "observed_legacy_operator_correction_count": sum(
                case["review"]["operator_correction_count"]
                for case in source["reviewed_outcomes"]
            ),
            "eligible_legacy_correction_case_count": len(
                {
                    row["case_id"]
                    for row in eligible_pressure_rows
                }
            ),
            "eligible_model_correction_proxy_by_arm": pressure_by_arm,
            "proxy_delta_0_minus_A": (
                pressure_by_arm["0"] - pressure_by_arm["A"]
            ),
            "outcome_attribution_established": False,
            "operator_workload_reduction_established": False,
        },
        "silence": {
            "required_count": len(active_ineligible),
            "correct_count": sum(
                row["memory_influence_correct"]
                for row in active_ineligible
            ),
            "specificity": (
                sum(
                    row["memory_influence_correct"]
                    for row in active_ineligible
                )
                / len(active_ineligible)
                if active_ineligible
                else 0.0
            ),
        },
        "observations": observations,
        "claim_limits": contract["claim_limits"],
        "authority": contract["authority"],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, default=CONTRACT_PATH)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--model-label", required=True)
    parser.add_argument("--model-id", required=True)
    parser.add_argument("--model-revision", required=True)
    parser.add_argument("--runtime-id", required=True)
    parser.add_argument("--resource-plan", type=Path, required=True)
    parser.add_argument("--resource-plan-sha256", required=True)
    parser.add_argument("--host-status", type=Path, required=True)
    parser.add_argument("--host-status-sha256", required=True)
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    parser.add_argument("--progress-every", type=int, default=4)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    checkpoint = args.checkpoint or Path(
        str(args.output) + ".observations.jsonl"
    )
    if (
        args.output.resolve().is_relative_to(BUNDLE_ROOT)
        or checkpoint.resolve().is_relative_to(BUNDLE_ROOT)
    ):
        print(
            "operator replay outputs must remain outside the source tree",
            file=sys.stderr,
        )
        return 2
    try:
        report = build_report(args)
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        errors = sorted(
            Draft202012Validator(
                schema, format_checker=FormatChecker()
            ).iter_errors(report),
            key=lambda error: list(error.absolute_path),
        )
        if errors:
            detail = "\n".join(
                f"{'/'.join(map(str, error.absolute_path))}: "
                f"{error.message}"
                for error in errors
            )
            raise OperatorReplayError(
                f"operator replay schema validation failed:\n{detail}"
            )
    except (
        OperatorReplayError,
        OSError,
        ValueError,
        KeyError,
        TypeError,
    ) as error:
        print(f"Phase 13 operator replay failed: {error}", file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report["execution"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
