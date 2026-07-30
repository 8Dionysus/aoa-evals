#!/usr/bin/env python3
"""Run paired, isolated fresh Codex sessions for the aoa-memo P0/P1 lane."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import statistics
import subprocess
import sys
import time
from typing import Any, Sequence

from jsonschema import Draft202012Validator, FormatChecker


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = (
    BUNDLE_ROOT / "fixtures" / "phase13-participation-codex-cases.json"
)
REPORT_SCHEMA_PATH = (
    BUNDLE_ROOT / "reports" / "phase13-participation-codex.schema.json"
)
SKILL_RE = re.compile(r"/skills/([^/'\"\s]+)/SKILL\.md")


class CodexParticipationError(RuntimeError):
    """Raised when the fresh-session lane cannot produce reviewable evidence."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CodexParticipationError(f"{path}: invalid JSON") from exc
    if not isinstance(payload, dict):
        raise CodexParticipationError(f"{path}: expected JSON object")
    return payload


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def text_digest(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def normalized_report_digest(report: dict[str, Any]) -> str:
    return canonical_digest(
        {
            key: value
            for key, value in report.items()
            if key != "report_digest"
        }
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
    fraction = position - lower
    return float(ordered[lower] * (1 - fraction) + ordered[upper] * fraction)


def validate_fixture(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    if fixture.get("schema_version") != "aoa_memo_participation_codex_cases_v0":
        raise CodexParticipationError("unsupported Codex participation fixture")
    cases = fixture.get("cases")
    if not isinstance(cases, list) or len(cases) != 4:
        raise CodexParticipationError("Codex participation fixture must have four cases")
    expected_families = {
        "explicit_orientation",
        "indirect_continuity",
        "current_source_negative",
        "raw_session_sibling",
    }
    seen_ids: set[str] = set()
    seen_families: set[str] = set()
    first_arms: list[str] = []
    for case in cases:
        if not isinstance(case, dict):
            raise CodexParticipationError("Codex participation case is not an object")
        case_id = case.get("case_id")
        family = case.get("case_family")
        prompt = case.get("prompt")
        order = case.get("arm_order")
        expectations = case.get("expectations")
        if not isinstance(case_id, str) or case_id in seen_ids:
            raise CodexParticipationError("case ids must be unique strings")
        if family not in expected_families:
            raise CodexParticipationError(f"{case_id}: unsupported case family")
        if not isinstance(prompt, str) or not prompt.strip():
            raise CodexParticipationError(f"{case_id}: prompt is empty")
        if order not in (["P0", "P1"], ["P1", "P0"]):
            raise CodexParticipationError(f"{case_id}: invalid arm order")
        if not isinstance(expectations, dict) or set(expectations) != {"P0", "P1"}:
            raise CodexParticipationError(f"{case_id}: invalid expectations")
        for arm_id, expectation in expectations.items():
            if not isinstance(expectation, dict):
                raise CodexParticipationError(
                    f"{case_id}/{arm_id}: expectation is not an object"
                )
            if expectation.get("memo_route") not in {
                "required",
                "forbidden",
                "descriptive",
            }:
                raise CodexParticipationError(
                    f"{case_id}/{arm_id}: invalid memo route expectation"
                )
            if expectation.get("max_locator_calls") not in {0, 1}:
                raise CodexParticipationError(
                    f"{case_id}/{arm_id}: invalid locator budget"
                )
        seen_ids.add(case_id)
        seen_families.add(str(family))
        first_arms.append(order[0])
    if seen_families != expected_families:
        raise CodexParticipationError("Codex participation family coverage drifted")
    if first_arms != ["P0", "P1", "P0", "P1"]:
        raise CodexParticipationError("first-arm order must alternate P0/P1")
    return cases


def dedupe(values: Sequence[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def parse_event_stream(
    stdout: str,
) -> tuple[dict[str, Any], str | None]:
    selected_skills: list[str] = []
    mcp_calls: list[dict[str, str]] = []
    thread_started = False
    turn_completed = False
    usage = {
        "input_tokens": 0,
        "cached_input_tokens": 0,
        "output_tokens": 0,
        "reasoning_output_tokens": 0,
    }
    for line_number, line in enumerate(stdout.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            return {}, f"line {line_number} is not JSON"
        if not isinstance(event, dict):
            return {}, f"line {line_number} is not an object"
        event_type = event.get("type")
        if event_type == "thread.started":
            thread_started = True
        if event_type == "turn.completed":
            turn_completed = True
            event_usage = event.get("usage", {})
            if isinstance(event_usage, dict):
                for key in usage:
                    value = event_usage.get(key, 0)
                    usage[key] = value if isinstance(value, int) and value >= 0 else 0
        if event_type != "item.completed":
            continue
        item = event.get("item", {})
        if not isinstance(item, dict):
            continue
        if item.get("type") == "command_execution":
            command = item.get("command", "")
            if isinstance(command, str):
                selected_skills.extend(SKILL_RE.findall(command))
        if item.get("type") == "mcp_tool_call":
            server = item.get("server")
            tool = item.get("tool")
            status = item.get("status")
            if all(isinstance(value, str) for value in (server, tool, status)):
                mcp_calls.append(
                    {
                        "server": server,
                        "tool": tool,
                        "status": status,
                    }
                )
    return (
        {
            "thread_started": thread_started,
            "turn_completed": turn_completed,
            "selected_skills": dedupe(selected_skills),
            "mcp_calls": mcp_calls,
            "usage": usage,
        },
        None,
    )


def score_expectation(
    observation: dict[str, Any],
    expectation: dict[str, Any],
) -> list[str]:
    failures: list[str] = []
    if observation["status"] != "complete":
        failures.append("session_not_complete")
    memo_route = expectation["memo_route"]
    memo_seen = observation["memo_selected"] or bool(observation["memo_tool_calls"])
    if memo_route == "required" and not memo_seen:
        failures.append("memo_route_missing")
    if memo_route == "forbidden" and memo_seen:
        failures.append("memo_route_unexpected")
    required_skill = expectation.get("required_selected_skill")
    if required_skill and required_skill not in observation["selected_skills"]:
        failures.append("required_skill_missing")
    required_tool = expectation.get("required_memo_tool")
    if required_tool and required_tool not in observation["memo_tool_calls"]:
        failures.append("required_memo_tool_missing")
    if observation["locator_call_count"] > expectation["max_locator_calls"]:
        failures.append("locator_budget_exceeded")
    return failures


def write_private(path: Path, value: str) -> None:
    path.write_text(value, encoding="utf-8")
    path.chmod(0o600)


def invoke_codex(
    *,
    codex_bin: str,
    home: Path,
    cwd: Path,
    model: str,
    prompt: str,
    timeout_seconds: float,
) -> tuple[int | None, str, str, float, str]:
    env = os.environ.copy()
    env["CODEX_HOME"] = str(home)
    command = [
        codex_bin,
        "exec",
        "--ephemeral",
        "--sandbox",
        "read-only",
        "--json",
        "-m",
        model,
        prompt,
    ]
    started = time.perf_counter()
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout_seconds,
        )
        latency_ms = (time.perf_counter() - started) * 1000
        return (
            result.returncode,
            result.stdout,
            result.stderr,
            latency_ms,
            "returned",
        )
    except subprocess.TimeoutExpired as exc:
        latency_ms = (time.perf_counter() - started) * 1000
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
        return None, stdout, stderr, latency_ms, "timeout"


def resolve_codex_binary(value: str) -> str:
    resolved = shutil.which(value)
    if resolved is None:
        raise CodexParticipationError(f"Codex binary is unavailable: {value}")
    return resolved


def validate_home(home: Path, arm_id: str) -> dict[str, str]:
    if not home.is_dir():
        raise CodexParticipationError(f"{arm_id}: CODEX_HOME is missing")
    if (home / "hooks.json").exists():
        raise CodexParticipationError(
            f"{arm_id}: fresh-session lane forbids hooks.json"
        )
    required = {
        f"{arm_id.lower()}_skill": home / "skills" / "aoa-memo" / "SKILL.md",
        f"{arm_id.lower()}_descriptor": (
            home / "skills" / "aoa-memo" / "agents" / "openai.yaml"
        ),
        f"{arm_id.lower()}_config": home / "config.toml",
    }
    pins: dict[str, str] = {}
    for label, path in required.items():
        if not path.is_file():
            raise CodexParticipationError(f"{arm_id}: missing {path.name}")
        pins[label] = file_digest(path)
    return pins


def arm_totals(
    observations: Sequence[dict[str, Any]],
    arm_id: str,
) -> dict[str, int]:
    totals = {
        "input_tokens": 0,
        "cached_input_tokens": 0,
        "output_tokens": 0,
        "reasoning_output_tokens": 0,
    }
    for observation in observations:
        if observation["arm_id"] != arm_id:
            continue
        for key in totals:
            totals[key] += observation["usage"][key]
    return totals


def arm_latency(
    observations: Sequence[dict[str, Any]],
    arm_id: str,
) -> dict[str, float]:
    values = [
        float(observation["latency_ms"])
        for observation in observations
        if observation["arm_id"] == arm_id
    ]
    return {
        "p50": round(statistics.median(values), 3),
        "p95": round(percentile(values, 0.95), 3),
        "max": round(max(values), 3),
    }


def observation_route_signature(observation: dict[str, Any]) -> tuple[Any, ...]:
    return (
        tuple(observation["selected_skills"]),
        tuple(
            (call["server"], call["tool"], call["status"])
            for call in observation["mcp_calls"]
        ),
    )


def build_report(
    *,
    fixture: dict[str, Any],
    observations: list[dict[str, Any]],
    source_pins: dict[str, str],
    codex_version: str,
    model: str,
    execution_fingerprint: str,
) -> dict[str, Any]:
    by_key = {
        (observation["case_family"], observation["arm_id"]): observation
        for observation in observations
    }
    p0_memo = [
        observation
        for observation in observations
        if observation["arm_id"] == "P0" and observation["memo_selected"]
    ]
    p1_memo = [
        observation
        for observation in observations
        if observation["arm_id"] == "P1" and observation["memo_selected"]
    ]
    negative = [
        observation
        for observation in observations
        if observation["case_family"] == "current_source_negative"
    ]
    sibling = [
        observation
        for observation in observations
        if observation["case_family"] == "raw_session_sibling"
    ]
    paired_delta_count = 0
    for case in fixture["cases"]:
        p0 = by_key[(case["case_family"], "P0")]
        p1 = by_key[(case["case_family"], "P1")]
        if observation_route_signature(p0) != observation_route_signature(p1):
            paired_delta_count += 1
    metrics = {
        "complete_count": sum(
            observation["status"] == "complete"
            for observation in observations
        ),
        "expectation_pass_count": sum(
            observation["expectation_passed"]
            for observation in observations
        ),
        "p0_memo_selection_count": len(p0_memo),
        "p1_memo_selection_count": len(p1_memo),
        "p0_memo_brief_count": sum(
            observation["memo_tool_calls"].count("aoa_memo_brief")
            for observation in observations
            if observation["arm_id"] == "P0"
        ),
        "p1_memo_brief_count": sum(
            observation["memo_tool_calls"].count("aoa_memo_brief")
            for observation in observations
            if observation["arm_id"] == "P1"
        ),
        "p0_memo_search_count": sum(
            observation["memo_tool_calls"].count("aoa_memo_search")
            for observation in observations
            if observation["arm_id"] == "P0"
        ),
        "p1_memo_search_count": sum(
            observation["memo_tool_calls"].count("aoa_memo_search")
            for observation in observations
            if observation["arm_id"] == "P1"
        ),
        "p0_false_positive_count": sum(
            observation["arm_id"] == "P0"
            and bool(
                observation["memo_selected"] or observation["memo_tool_calls"]
            )
            for observation in negative
        ),
        "p1_false_positive_count": sum(
            observation["arm_id"] == "P1"
            and bool(
                observation["memo_selected"] or observation["memo_tool_calls"]
            )
            for observation in negative
        ),
        "sibling_takeover_count": sum(
            observation["memo_selected"] or bool(observation["memo_tool_calls"])
            for observation in sibling
        ),
        "paired_route_delta_count": paired_delta_count,
        "arm_usage": {
            "P0": arm_totals(observations, "P0"),
            "P1": arm_totals(observations, "P1"),
        },
        "arm_latency_ms": {
            "P0": arm_latency(observations, "P0"),
            "P1": arm_latency(observations, "P1"),
        },
    }
    candidate_explicit = by_key[("explicit_orientation", "P1")]
    candidate_indirect = by_key[("indirect_continuity", "P1")]
    candidate_negative = by_key[("current_source_negative", "P1")]
    candidate_sibling = by_key[("raw_session_sibling", "P1")]
    gates = {
        "all_sessions_complete": metrics["complete_count"] == 8,
        "all_expectations_pass": metrics["expectation_pass_count"] == 8,
        "candidate_explicit_route": (
            candidate_explicit["memo_selected"]
            and candidate_explicit["memo_tool_calls"] == ["aoa_memo_brief"]
        ),
        "candidate_indirect_route": (
            candidate_indirect["memo_selected"]
            and candidate_indirect["memo_tool_calls"] == ["aoa_memo_brief"]
        ),
        "candidate_negative_silence": (
            not candidate_negative["memo_selected"]
            and not candidate_negative["memo_tool_calls"]
        ),
        "candidate_sibling_handoff": (
            "aoa-session-memory-global-route"
            in candidate_sibling["selected_skills"]
            and not candidate_sibling["memo_selected"]
            and not candidate_sibling["memo_tool_calls"]
        ),
        "single_locator_budget": all(
            observation["locator_call_count"] <= 1
            for observation in observations
        ),
        "raw_streams_digest_pinned": all(
            observation["raw_jsonl_digest"].startswith("sha256:")
            and observation["stderr_digest"].startswith("sha256:")
            for observation in observations
        ),
    }
    exit_gate_passed = all(gates.values())
    report: dict[str, Any] = {
        "schema_version": "aoa_memo_phase13_participation_codex_v0",
        "report_id": "aoa-memo-phase13-participation-codex-"
        + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "posture": "isolated_fresh_session_paired_no_live_activation",
        "source_pins": source_pins,
        "execution": {
            "codex_version": codex_version,
            "model": model,
            "sandbox": "read-only",
            "ephemeral": True,
            "hooks_present": False,
            "retry_count": 0,
            "case_count": 4,
            "observation_count": 8,
            "alternating_arm_order": True,
            "execution_fingerprint": execution_fingerprint,
        },
        "observations": observations,
        "metrics": metrics,
        "evidence_ladder": {
            "opportunity": "authored_paired_prompts_executed",
            "noticed": "fresh_session_route_selection_observed",
            "invocation": "mcp_events_observed",
            "result_returned": "mcp_completion_status_observed",
            "used_or_rejected": "route_level_only",
            "action_change": "unknown",
            "outcome": "unknown",
            "benefit_claim_allowed": False,
        },
        "gates": gates,
        "exit_gate_passed": exit_gate_passed,
        "verdict": (
            "supports isolated fresh-session P1 participation continuation"
            if exit_gate_passed
            else "does not pass isolated fresh-session P1 participation gates"
        ),
        "authority": {
            "live_activation": False,
            "codex_trust": False,
            "skill_admission": False,
            "policy_promotion": False,
            "memory_write": False,
            "production": False,
            "landing": False,
            "benefit_verdict": False,
        },
        "limitations": [
            "Four authored prompts are not natural operator traffic.",
            "Route selection and MCP completion do not prove that returned context changed an action.",
            "Token and wall latency totals are descriptive and include the whole Codex turn.",
            "The lane uses isolated CODEX_HOME directories and does not establish live hook trust.",
            "No outcome, delayed effect, longitudinal value, or operator benefit is established.",
        ],
        "report_digest": "",
    }
    report["report_digest"] = normalized_report_digest(report)
    return report


def validate_report(report: dict[str, Any]) -> None:
    schema = load_json(REPORT_SCHEMA_PATH)
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
        raise CodexParticipationError(
            f"report schema violation at {location}: {error.message}"
        )
    expected = normalized_report_digest(report)
    if report.get("report_digest") != expected:
        raise CodexParticipationError("report digest mismatch")


def run(args: argparse.Namespace) -> dict[str, Any]:
    fixture = load_json(CASES_PATH)
    cases = validate_fixture(fixture)
    codex_bin = resolve_codex_binary(args.codex_bin)
    homes = {"P0": args.p0_home.resolve(), "P1": args.p1_home.resolve()}
    cwds = {"P0": args.p0_cwd.resolve(), "P1": args.p1_cwd.resolve()}
    for arm_id, cwd in cwds.items():
        if not cwd.is_dir():
            raise CodexParticipationError(f"{arm_id}: cwd is missing")
    source_pins = {
        "fixture": file_digest(CASES_PATH),
        "runner": file_digest(Path(__file__).resolve()),
        "report_schema": file_digest(REPORT_SCHEMA_PATH),
    }
    source_pins.update(validate_home(homes["P0"], "P0"))
    source_pins.update(validate_home(homes["P1"], "P1"))
    if source_pins["p0_skill"] == source_pins["p1_skill"]:
        raise CodexParticipationError("P0 and P1 skill digests must differ")
    version_result = subprocess.run(
        [codex_bin, "--version"],
        text=True,
        capture_output=True,
        check=False,
        timeout=10,
    )
    if version_result.returncode != 0 or not version_result.stdout.strip():
        raise CodexParticipationError("unable to pin Codex version")
    codex_version = version_result.stdout.strip()
    attempt_plan = [
        {
            "case": case,
            "arm_id": arm_id,
            "prompt_sha256": text_digest(case["prompt"]),
        }
        for case in cases
        for arm_id in case["arm_order"]
    ]
    execution_fingerprint = canonical_digest(
        {
            "source_pins": source_pins,
            "codex_version": codex_version,
            "model": args.model,
            "sandbox": "read-only",
            "ephemeral": True,
            "retry_count": 0,
            "attempts": [
                {
                    "case_id": attempt["case"]["case_id"],
                    "arm_id": attempt["arm_id"],
                    "prompt_sha256": attempt["prompt_sha256"],
                }
                for attempt in attempt_plan
            ],
        }
    )
    args.output_dir.mkdir(parents=True, exist_ok=False)
    args.output_dir.chmod(0o700)
    observations: list[dict[str, Any]] = []
    for attempt_index, attempt in enumerate(attempt_plan):
        case = attempt["case"]
        arm_id = attempt["arm_id"]
        exit_code, stdout, stderr, latency_ms, process_status = invoke_codex(
            codex_bin=codex_bin,
            home=homes[arm_id],
            cwd=cwds[arm_id],
            model=args.model,
            prompt=case["prompt"],
            timeout_seconds=args.timeout_seconds,
        )
        stem = f"{attempt_index:02d}-{case['case_id']}-{arm_id}"
        raw_path = args.output_dir / f"{stem}.jsonl"
        stderr_path = args.output_dir / f"{stem}.stderr.txt"
        write_private(raw_path, stdout)
        write_private(stderr_path, stderr)
        parsed, parse_error = parse_event_stream(stdout)
        if process_status == "timeout":
            status = "timeout"
        elif parse_error is not None:
            status = "invalid_jsonl"
        elif exit_code == 0 and parsed["thread_started"] and parsed["turn_completed"]:
            status = "complete"
        else:
            status = "failed"
        if parse_error is not None:
            parsed = {
                "thread_started": False,
                "turn_completed": False,
                "selected_skills": [],
                "mcp_calls": [],
                "usage": {
                    "input_tokens": 0,
                    "cached_input_tokens": 0,
                    "output_tokens": 0,
                    "reasoning_output_tokens": 0,
                },
            }
        memo_tool_calls = [
            call["tool"]
            for call in parsed["mcp_calls"]
            if call["server"] == "aoa_memo"
            or call["tool"].startswith("aoa_memo_")
        ]
        observation: dict[str, Any] = {
            "attempt_index": attempt_index,
            "case_id": case["case_id"],
            "case_family": case["case_family"],
            "arm_id": arm_id,
            "prompt_sha256": attempt["prompt_sha256"],
            "status": status,
            "exit_code": exit_code,
            "latency_ms": round(latency_ms, 3),
            "thread_started": parsed["thread_started"],
            "turn_completed": parsed["turn_completed"],
            "selected_skills": parsed["selected_skills"],
            "mcp_calls": parsed["mcp_calls"],
            "memo_selected": "aoa-memo" in parsed["selected_skills"],
            "memo_tool_calls": memo_tool_calls,
            "locator_call_count": len(parsed["mcp_calls"]),
            "usage": parsed["usage"],
            "expectation_passed": False,
            "expectation_failures": [],
            "raw_jsonl_digest": file_digest(raw_path),
            "stderr_digest": file_digest(stderr_path),
        }
        failures = score_expectation(
            observation,
            case["expectations"][arm_id],
        )
        observation["expectation_failures"] = failures
        observation["expectation_passed"] = not failures
        observations.append(observation)
        if args.progress:
            print(
                json.dumps(
                    {
                        "attempt_index": attempt_index,
                        "case_id": case["case_id"],
                        "arm_id": arm_id,
                        "status": status,
                        "selected_skills": observation["selected_skills"],
                        "memo_tool_calls": memo_tool_calls,
                        "expectation_passed": not failures,
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )
    report = build_report(
        fixture=fixture,
        observations=observations,
        source_pins=source_pins,
        codex_version=codex_version,
        model=args.model,
        execution_fingerprint=execution_fingerprint,
    )
    validate_report(report)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_private(
        args.output,
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
    )
    return report


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--p0-home", type=Path, required=True)
    result.add_argument("--p1-home", type=Path, required=True)
    result.add_argument("--p0-cwd", type=Path, required=True)
    result.add_argument("--p1-cwd", type=Path, required=True)
    result.add_argument("--output-dir", type=Path, required=True)
    result.add_argument("--output", type=Path, required=True)
    result.add_argument("--codex-bin", default="codex")
    result.add_argument("--model", default="gpt-5.6-sol")
    result.add_argument("--timeout-seconds", type=float, default=240.0)
    result.add_argument("--progress", action="store_true")
    return result


def main() -> int:
    try:
        report = run(parser().parse_args())
    except (CodexParticipationError, OSError, subprocess.SubprocessError) as exc:
        print(f"phase13 participation Codex lane failed: {exc}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "report": report["report_id"],
                "report_digest": report["report_digest"],
                "exit_gate_passed": report["exit_gate_passed"],
                "verdict": report["verdict"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
