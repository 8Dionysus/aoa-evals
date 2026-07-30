#!/usr/bin/env python3
"""Run a pinned no-retry local reader over prepared Phase 13 prompts."""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import os
import re
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


TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)
BUNDLE_ROOT = Path(__file__).resolve().parents[1]
REPORT_SCHEMA_PATH = (
    BUNDLE_ROOT / "reports" / "phase13-model-lane.schema.json"
)


class ModelLaneError(RuntimeError):
    """Raised when the model lane cannot produce a reviewable report."""


def verify_evidence_ref(path: Path, expected_sha256: str) -> None:
    if not path.is_file():
        raise ModelLaneError(f"evidence ref is missing: {path}")
    actual = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected_sha256:
        raise ModelLaneError(
            f"evidence ref digest mismatch: {path}: "
            f"expected {expected_sha256}, got {actual}"
        )


def canonical_digest(value: dict[str, Any]) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


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
    if not path.exists():
        append_checkpoint(
            path,
            {
                "record_type": "checkpoint_header",
                "run_fingerprint": fingerprint,
                "attempted_prompt_count": len(prompts),
            },
        )
        return []
    lines = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not lines or lines[0] != {
        "record_type": "checkpoint_header",
        "run_fingerprint": fingerprint,
        "attempted_prompt_count": len(prompts),
    }:
        raise ModelLaneError("checkpoint header does not match this run")
    observations: list[dict[str, Any]] = []
    for index, record in enumerate(lines[1:]):
        if record.get("record_type") != "observation":
            raise ModelLaneError("checkpoint contains an unknown record")
        observation = record.get("observation")
        if not isinstance(observation, dict) or index >= len(prompts):
            raise ModelLaneError("checkpoint observation is malformed")
        prompt = prompts[index]
        if (
            observation.get("attempt_index") != index
            or observation.get("prompt_id") != prompt["prompt_id"]
            or observation.get("prompt_sha256") != prompt["prompt_sha256"]
        ):
            raise ModelLaneError(
                "checkpoint observation order or prompt identity drifted"
            )
        observations.append(observation)
    return observations


def normalized_tokens(value: Any) -> list[str]:
    return TOKEN_RE.findall(str(value).casefold())


def token_f1(response: str, expected: str) -> float:
    response_tokens = normalized_tokens(response)
    expected_tokens = normalized_tokens(expected)
    if not response_tokens or not expected_tokens:
        return 0.0
    response_counts: dict[str, int] = defaultdict(int)
    expected_counts: dict[str, int] = defaultdict(int)
    for token in response_tokens:
        response_counts[token] += 1
    for token in expected_tokens:
        expected_counts[token] += 1
    overlap = sum(
        min(response_counts[token], expected_counts[token])
        for token in response_counts.keys() & expected_counts.keys()
    )
    if overlap == 0:
        return 0.0
    precision = overlap / len(response_tokens)
    recall = overlap / len(expected_tokens)
    return 2 * precision * recall / (precision + recall)


def normalized_match(response: str, expected: str) -> bool:
    response_norm = " ".join(normalized_tokens(response))
    expected_norm = " ".join(normalized_tokens(expected))
    return bool(
        response_norm
        and expected_norm
        and (expected_norm in response_norm or response_norm in expected_norm)
    )


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
                    "You are a bounded memory benchmark reader. Follow the "
                    "requested short-answer format and never invent evidence."
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
        raise ModelLaneError(
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
        raise ModelLaneError(
            f"endpoint error after {latency_ms:.3f} ms: {error}"
        ) from error
    latency_ms = (time.perf_counter() - started) * 1000
    if not isinstance(response_payload, dict):
        raise ModelLaneError("response envelope is not an object")
    choices = response_payload.get("choices", [])
    if not isinstance(choices, list) or not choices:
        raise ModelLaneError("response has no choices")
    if not isinstance(choices[0], dict):
        raise ModelLaneError("response choice is not an object")
    message = choices[0].get("message", {})
    if not isinstance(message, dict):
        raise ModelLaneError("response message is not an object")
    content = message.get("content")
    if not isinstance(content, str):
        raise ModelLaneError("response content is not a string")
    usage = response_payload.get("usage", {})
    if not isinstance(usage, dict):
        raise ModelLaneError("response usage is not an object")
    return content, usage, status_code, latency_ms


def percentile(values: list[float], quantile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(round((len(ordered) - 1) * quantile), len(ordered) - 1)
    return ordered[index]


def run(args: argparse.Namespace) -> dict[str, Any]:
    verify_evidence_ref(
        args.resource_policy_ref, args.resource_policy_sha256
    )
    verify_evidence_ref(args.host_status_ref, args.host_status_sha256)
    prompts_raw = args.prompts.read_bytes()
    prompts_sha256 = "sha256:" + hashlib.sha256(prompts_raw).hexdigest()
    prompts = [
        json.loads(line)
        for line in prompts_raw.decode().splitlines()
        if line.strip()
    ]
    if args.limit is not None:
        prompts = prompts[: args.limit]
    run_fingerprint = canonical_digest(
        {
            "prompts_sha256": prompts_sha256,
            "attempted_prompt_count": len(prompts),
            "model_label": args.model_label,
            "model_id": args.model_id,
            "model_revision": args.model_revision,
            "runtime_id": args.runtime_id,
            "endpoint": args.endpoint,
            "resource_policy_sha256": args.resource_policy_sha256,
            "host_status_sha256": args.host_status_sha256,
            "seed": args.seed,
            "temperature": 0,
            "max_tokens": args.max_tokens,
        }
    )
    checkpoint_path = (
        args.checkpoint
        if args.checkpoint is not None
        else Path(str(args.output) + ".observations.jsonl")
    )
    observations = load_checkpoint(
        checkpoint_path,
        fingerprint=run_fingerprint,
        prompts=prompts,
    )
    resumed_observation_count = len(observations)
    for index, prompt in enumerate(
        prompts[resumed_observation_count:],
        start=resumed_observation_count,
    ):
        observation = {
            "prompt_id": prompt["prompt_id"],
            "question_id": prompt["question_id"],
            "question_type": prompt["question_type"],
            "arm_id": prompt["arm_id"],
            "prompt_sha256": prompt["prompt_sha256"],
            "attempt_index": index,
            "retry_count": 0,
        }
        try:
            content, usage, status_code, latency_ms = invoke(
                args.endpoint,
                args.model_id,
                prompt["prompt"],
                max_tokens=args.max_tokens,
                seed=args.seed,
                timeout_seconds=args.timeout_seconds,
            )
            observation.update(
                {
                    "status": "complete",
                    "http_status": status_code,
                    "latency_ms": round(latency_ms, 3),
                    "response": content,
                    "usage": usage,
                    "normalized_match": normalized_match(
                        content, prompt["expected_answer"]
                    ),
                    "token_f1": round(
                        token_f1(content, prompt["expected_answer"]), 6
                    ),
                    "error": None,
                }
            )
        except ModelLaneError as error:
            observation.update(
                {
                    "status": "invalid",
                    "http_status": None,
                    "latency_ms": None,
                    "response": None,
                    "usage": {},
                    "normalized_match": False,
                    "token_f1": 0.0,
                    "error": str(error),
                }
            )
        observations.append(observation)
        append_checkpoint(
            checkpoint_path,
            {
                "record_type": "observation",
                "observation": observation,
            },
        )
        if args.progress_every and (index + 1) % args.progress_every == 0:
            print(
                f"completed {index + 1}/{len(prompts)} prompt attempts",
                file=sys.stderr,
                flush=True,
            )

    complete = [item for item in observations if item["status"] == "complete"]
    by_arm: dict[str, Any] = {}
    for arm_id in ("A", "B", "C"):
        items = [item for item in complete if item["arm_id"] == arm_id]
        latencies = [item["latency_ms"] for item in items]
        by_arm[arm_id] = {
            "attempted": sum(
                item["arm_id"] == arm_id for item in observations
            ),
            "complete": len(items),
            "normalized_match_rate": (
                sum(item["normalized_match"] for item in items) / len(items)
                if items
                else 0.0
            ),
            "mean_token_f1": (
                statistics.fmean(item["token_f1"] for item in items)
                if items
                else 0.0
            ),
            "p50_latency_ms": percentile(latencies, 0.50),
            "p95_latency_ms": percentile(latencies, 0.95),
            "p99_latency_ms": percentile(latencies, 0.99),
        }
    generated_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )
    return {
        "schema_version": 1,
        "report_id": f"aoa-memo-phase13-model-{args.model_label}",
        "generated_at": generated_at,
        "model": {
            "label": args.model_label,
            "model_id": args.model_id,
            "model_revision": args.model_revision,
            "runtime_id": args.runtime_id,
            "endpoint": args.endpoint,
            "resource_policy_ref": str(args.resource_policy_ref),
            "resource_policy_sha256": args.resource_policy_sha256,
            "host_status_ref": str(args.host_status_ref),
            "host_status_sha256": args.host_status_sha256,
            "seed": args.seed,
            "temperature": 0,
            "max_tokens": args.max_tokens,
        },
        "input": {
            "path": str(args.prompts),
            "sha256": prompts_sha256,
            "attempted_prompt_count": len(prompts),
        },
        "execution": {
            "complete_count": len(complete),
            "invalid_count": len(observations) - len(complete),
            "resumed_observation_count": resumed_observation_count,
            "checkpoint_path": str(checkpoint_path),
            "checkpoint_sha256": (
                "sha256:"
                + hashlib.sha256(checkpoint_path.read_bytes()).hexdigest()
            ),
            "hidden_retry": False,
            "resource_admission_bypassed": False,
        },
        "by_arm": by_arm,
        "observations": observations,
        "claim_limit": (
            "Normalized match and token F1 are local descriptive heuristics, "
            "not official LongMemEval scores or an active-organ benefit verdict."
        ),
        "authority": {
            "benefit_verdict": False,
            "policy_promotion": False,
            "production": False,
            "training": False,
            "landing": False,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--model-label", required=True)
    parser.add_argument("--model-id", required=True)
    parser.add_argument("--model-revision", required=True)
    parser.add_argument("--runtime-id", required=True)
    parser.add_argument("--resource-policy-ref", type=Path, required=True)
    parser.add_argument("--resource-policy-sha256", required=True)
    parser.add_argument("--host-status-ref", type=Path, required=True)
    parser.add_argument("--host-status-sha256", required=True)
    parser.add_argument("--seed", type=int, default=1307)
    parser.add_argument("--max-tokens", type=int, default=80)
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--progress-every", type=int, default=6)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    checkpoint_path = (
        args.checkpoint
        if args.checkpoint is not None
        else Path(str(args.output) + ".observations.jsonl")
    )
    if (
        args.output.resolve().is_relative_to(BUNDLE_ROOT)
        or checkpoint_path.resolve().is_relative_to(BUNDLE_ROOT)
    ):
        print("model lab outputs must remain outside the source tree", file=sys.stderr)
        return 2
    try:
        report = run(args)
        schema = json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
        errors = sorted(
            Draft202012Validator(
                schema, format_checker=FormatChecker()
            ).iter_errors(report),
            key=lambda error: list(error.absolute_path),
        )
        if errors:
            detail = "\n".join(
                f"{'/'.join(map(str, error.absolute_path))}: {error.message}"
                for error in errors
            )
            raise ModelLaneError(
                f"model report schema validation failed:\n{detail}"
            )
    except (ModelLaneError, OSError, ValueError, KeyError, TypeError) as error:
        print(f"Phase 13 model lane failed: {error}", file=sys.stderr)
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
