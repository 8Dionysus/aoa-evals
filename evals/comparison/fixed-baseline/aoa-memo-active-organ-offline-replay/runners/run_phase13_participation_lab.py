#!/usr/bin/env python3
"""Run the source-local aoa-memo participation and hook-composition lab."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import statistics
import subprocess
import sys
import time
from typing import Any, Sequence

from jsonschema import Draft202012Validator, FormatChecker


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = BUNDLE_ROOT / "fixtures" / "phase13-participation-trigger-corpus.json"
REPORT_SCHEMA_PATH = BUNDLE_ROOT / "reports" / "phase13-participation.schema.json"

MEMO_HOOK_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "scripts/aoa_memo_participation_hook.py"
)
MEMO_RECEIPT_SCHEMA_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "schemas/aoa_memo_participation_receipt_v0.schema.json"
)
MEMO_FRAGMENT_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "config/codex-hooks.aoa-memo-participation-shadow.fragment.json"
)
MEMO_FRAGMENT_SCHEMA_RELATIVE = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/"
    "schemas/aoa_memo_participation_hook_fragment_v0.schema.json"
)
MEMO_SKILL_RELATIVE = "skills/aoa-memo/SKILL.md"
MEMO_SKILL_CONTRACT_RELATIVE = "skills/aoa-memo/references/contract.yaml"
MEMO_SKILL_MANIFEST_RELATIVE = "skills/port.manifest.json"

STACK_COMPOSITOR_RELATIVE = (
    "mechanics/config-projection/parts/codex-hooks/"
    "scripts/render_codex_hooks.py"
)
STACK_FRAGMENT_SCHEMA_RELATIVE = (
    "mechanics/config-projection/parts/codex-hooks/"
    "schemas/codex-hooks-fragment.schema.json"
)
STACK_RECEIPT_SCHEMA_RELATIVE = (
    "mechanics/config-projection/parts/codex-hooks/"
    "schemas/codex-hooks-composition-receipt.schema.json"
)


class ParticipationLabError(RuntimeError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ParticipationLabError(f"{path.name}: invalid JSON") from exc
    if not isinstance(payload, dict):
        raise ParticipationLabError(f"{path.name}: expected JSON object")
    return payload


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(payload: Any) -> str:
    encoded = json.dumps(
        payload,
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
        raise ParticipationLabError(
            f"participation report schema violation at {location}: {error.message}"
        )
    expected = normalized_report_digest(report)
    if report.get("report_digest") != expected:
        raise ParticipationLabError("participation report digest mismatch")


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
    return float(
        ordered[lower] * (1 - fraction) + ordered[upper] * fraction
    )


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ParticipationLabError(f"{path.name}: cannot load source module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def receipt_log_path(state_root: Path, session_id: str) -> Path:
    digest = hashlib.sha256(session_id.encode("utf-8")).hexdigest()
    return state_root / "sessions" / f"{digest}.jsonl"


def load_receipt_log(state_root: Path, session_id: str) -> list[dict[str, Any]]:
    path = receipt_log_path(state_root, session_id)
    if not path.is_file():
        raise ParticipationLabError("expected hook receipt log is missing")
    receipts: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        payload = json.loads(line)
        if not isinstance(payload, dict):
            raise ParticipationLabError("hook receipt is not an object")
        receipts.append(payload)
    return receipts


def run_hook(
    hook_script: Path,
    state_root: Path,
    event: dict[str, Any],
) -> tuple[subprocess.CompletedProcess[str], float]:
    started = time.perf_counter()
    result = subprocess.run(
        [
            sys.executable,
            str(hook_script),
            "observe",
            "--state-root",
            str(state_root),
        ],
        input=json.dumps(event, ensure_ascii=False),
        text=True,
        capture_output=True,
        check=False,
        timeout=5,
    )
    latency_ms = (time.perf_counter() - started) * 1000
    if result.returncode != 0:
        raise ParticipationLabError("memo participation hook returned non-zero")
    return result, latency_ms


def workspace_cwd(workspace: str) -> str:
    if workspace == "other":
        return "/lab/public-safe-task"
    if workspace == "tree-of-sophia":
        return "/srv/AbyssOS/Tree-of-Sophia"
    return f"/srv/AbyssOS/{workspace}"


def base_event(
    event_name: str,
    *,
    session_id: str,
    turn_id: str,
    cwd: str,
) -> dict[str, Any]:
    return {
        "session_id": session_id,
        "transcript_path": "/private/SECRET-TRANSCRIPT-PATH.jsonl",
        "cwd": cwd,
        "hook_event_name": event_name,
        "model": "gpt-5.6-sol",
        "permission_mode": "dontAsk",
        "turn_id": turn_id,
    }


def handler_keys(hooks: dict[str, Any]) -> list[tuple[str, str, str, str]]:
    keys: list[tuple[str, str, str, str]] = []
    for event_name, groups in hooks.items():
        for group in groups:
            matcher = str(group.get("matcher", ""))
            for handler in group["hooks"]:
                keys.append(
                    (
                        event_name,
                        matcher,
                        handler["command"],
                        str(handler.get("commandWindows", "")),
                    )
                )
    return keys


def validate_skill_contract(
    memo_root: Path,
) -> tuple[dict[str, Any], dict[str, str]]:
    skill_path = memo_root / MEMO_SKILL_RELATIVE
    contract_path = memo_root / MEMO_SKILL_CONTRACT_RELATIVE
    manifest_path = memo_root / MEMO_SKILL_MANIFEST_RELATIVE
    skill = skill_path.read_text(encoding="utf-8")
    contract = contract_path.read_text(encoding="utf-8")
    manifest = load_json(manifest_path)
    bundles = [
        bundle
        for bundle in manifest.get("bundles", [])
        if isinstance(bundle, dict) and bundle.get("name") == "aoa-memo"
    ]
    if len(bundles) != 1:
        raise ParticipationLabError("aoa-memo skill manifest must have one bundle")
    version = bundles[0].get("version")
    result = {
        "bundle_version": version,
        "materiality_trigger_present": (
            "reviewed prior decisions" in skill
            and "even when none is named" in skill
        ),
        "fast_lane_present": "## Fast orientation" in skill,
        "one_brief_budget_present": (
            "aoa_memo_brief(repo, intent)` exactly once" in skill
        ),
        "silence_present": (
            "correct silence is a successful" in skill
            and "choose `silence`" in skill
        ),
        "deep_gate_present": (
            "## Deep owner route" in skill
            and "references/contract.yaml" in skill
            and "references/source-return.md" in skill
        ),
        "sibling_handoffs_present": (
            "aoa-memo-writeback" in skill
            and "session-memory route" in skill
        ),
        "session_memory_dependency": not (
            "session_memory_dependency: false" in contract
            and "does not depend on" in skill
        ),
        "prompt_visibility_checked": False,
        "fresh_session_selection_checked": False,
    }
    if result["bundle_version"] != "0.1.22":
        raise ParticipationLabError("aoa-memo participation skill version is not 0.1.22")
    pins = {
        "memo_skill": file_digest(skill_path),
        "memo_skill_contract": file_digest(contract_path),
        "memo_skill_manifest": file_digest(manifest_path),
    }
    return result, pins


def validate_trigger_fixture(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    if fixture.get("schema_version") != "aoa_memo_participation_trigger_corpus_v0":
        raise ParticipationLabError("unsupported participation trigger corpus")
    cases = fixture.get("cases")
    if not isinstance(cases, list) or len(cases) < 10:
        raise ParticipationLabError("participation trigger corpus is too small")
    required_families = {"direct", "indirect", "incomplete", "negative", "edge"}
    observed_families = {
        case.get("case_family")
        for case in cases
        if isinstance(case, dict)
    }
    if not required_families.issubset(observed_families):
        raise ParticipationLabError("participation trigger families are incomplete")
    ids = [case.get("case_id") for case in cases if isinstance(case, dict)]
    if len(ids) != len(set(ids)):
        raise ParticipationLabError("participation trigger case ids are duplicated")
    return cases


def validate_receipts(
    state_root: Path,
    receipt_schema: dict[str, Any],
    hook_module: Any,
) -> tuple[bool, bool, set[str], int]:
    schema_validator = Draft202012Validator(
        receipt_schema,
        format_checker=FormatChecker(),
    )
    logs_valid = True
    chains_valid = True
    events: set[str] = set()
    count = 0
    for path in sorted((state_root / "sessions").glob("*.jsonl")):
        receipts: list[dict[str, Any]] = []
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                if not line:
                    continue
                payload = json.loads(line)
                schema_validator.validate(payload)
                receipts.append(payload)
                events.add(payload["event_name"])
                count += 1
        except (OSError, json.JSONDecodeError, ValueError):
            logs_valid = False
            continue
        if hook_module.verify_chain(receipts):
            chains_valid = False
    return logs_valid, chains_valid, events, count


def run_composition(
    *,
    stack_root: Path,
    memo_root: Path,
    native_hooks: Path,
    state_root: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    compositor = stack_root / STACK_COMPOSITOR_RELATIVE
    fragment = memo_root / MEMO_FRAGMENT_RELATIVE
    hook_script = memo_root / MEMO_HOOK_RELATIVE
    binding_values = {
        "AOA_MEMO_HOOK_SCRIPT": str(hook_script.resolve()),
        "AOA_MEMO_STATE_ROOT": str(state_root.resolve()),
    }

    native_before = file_digest(native_hooks)
    standalone = subprocess.run(
        [
            sys.executable,
            str(compositor),
            "--fragment",
            str(native_hooks),
        ],
        text=True,
        capture_output=True,
        check=False,
        timeout=10,
    )
    if standalone.returncode != 0:
        raise ParticipationLabError("standalone native hook composition failed")
    standalone_output = json.loads(standalone.stdout)
    native_payload = load_json(native_hooks)

    target = state_root / "composed-hooks.candidate.json"
    receipt_path = state_root / "composition-receipt.json"
    backup_dir = state_root / "composition-backups"
    shutil.copyfile(native_hooks, target)
    target.chmod(0o640)
    command = [
        sys.executable,
        str(compositor),
        "--fragment",
        str(native_hooks),
        "--fragment",
        str(fragment),
        "--binding",
        f"AOA_MEMO_HOOK_SCRIPT={binding_values['AOA_MEMO_HOOK_SCRIPT']}",
        "--binding",
        f"AOA_MEMO_STATE_ROOT={binding_values['AOA_MEMO_STATE_ROOT']}",
        "--write",
        str(target),
        "--receipt",
        str(receipt_path),
        "--backup-dir",
        str(backup_dir),
    ]
    result = subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=False,
        timeout=10,
    )
    if result.returncode != 0:
        raise ParticipationLabError("combined hook composition failed")
    composed = load_json(target)
    receipt = load_json(receipt_path)
    receipt_schema = load_json(stack_root / STACK_RECEIPT_SCHEMA_RELATIVE)
    Draft202012Validator(
        receipt_schema,
        format_checker=FormatChecker(),
    ).validate(receipt)

    native_keys = handler_keys(native_payload["hooks"])
    combined_keys = handler_keys(composed["hooks"])
    receipt_serialized = json.dumps(receipt, ensure_ascii=False)
    details = {
        "native_source_digest": native_before,
        "memo_fragment_digest": file_digest(fragment),
        "output_digest": file_digest(target),
        "composition_receipt_digest": receipt["receipt_digest"],
        "fragment_order": [
            item["fragment_id"]
            for item in receipt["fragments"]
        ],
        "event_count": len(composed["hooks"]),
        "native_handler_count": len(native_keys),
        "combined_handler_count": len(combined_keys),
        "standalone_native_preserved": (
            standalone_output.get("hooks") == native_payload.get("hooks")
            and all(key in combined_keys for key in native_keys)
        ),
        "owner_metadata_removed": set(composed) == {"description", "hooks"},
        "unresolved_binding_count": json.dumps(composed).count("{{"),
        "disposable_atomic_write": True,
        "backup_created": any(backup_dir.iterdir()),
        "live_config_touched": False,
        "codex_trust_established": False,
    }
    checks = {
        "native_unchanged": file_digest(native_hooks) == native_before,
        "composition_receipt_valid": (
            receipt["receipt_digest"]
            == canonical_digest(
                {
                    key: value
                    for key, value in receipt.items()
                    if key != "receipt_digest"
                }
            )
        ),
        "raw_binding_value_in_receipt": any(
            value in receipt_serialized
            for value in binding_values.values()
        ),
        "composition_output_bytes": target.stat().st_size,
    }
    return details, checks, composed


def run_participation_lab(
    *,
    memo_root: Path,
    stack_root: Path,
    native_hooks: Path,
    state_root: Path,
) -> dict[str, Any]:
    if state_root.exists() and any(state_root.iterdir()):
        raise ParticipationLabError("state root must be absent or empty")
    state_root.mkdir(parents=True, exist_ok=True, mode=0o700)
    state_root.chmod(0o700)

    fixture = load_json(CASES_PATH)
    cases = validate_trigger_fixture(fixture)
    skill_contract, skill_pins = validate_skill_contract(memo_root)

    hook_script = memo_root / MEMO_HOOK_RELATIVE
    receipt_schema_path = memo_root / MEMO_RECEIPT_SCHEMA_RELATIVE
    fragment_path = memo_root / MEMO_FRAGMENT_RELATIVE
    fragment_schema_path = memo_root / MEMO_FRAGMENT_SCHEMA_RELATIVE
    compositor_path = stack_root / STACK_COMPOSITOR_RELATIVE
    stack_fragment_schema_path = stack_root / STACK_FRAGMENT_SCHEMA_RELATIVE
    stack_receipt_schema_path = stack_root / STACK_RECEIPT_SCHEMA_RELATIVE
    source_paths = (
        hook_script,
        receipt_schema_path,
        fragment_path,
        fragment_schema_path,
        compositor_path,
        stack_fragment_schema_path,
        stack_receipt_schema_path,
        native_hooks,
    )
    missing = [path.name for path in source_paths if not path.is_file()]
    if missing:
        raise ParticipationLabError("required source paths are missing")

    Draft202012Validator(
        load_json(fragment_schema_path),
    ).validate(load_json(fragment_path))
    hook_module = load_module(hook_script, "aoa_memo_participation_hook_lab")
    receipt_schema = load_json(receipt_schema_path)

    hook_stdout_empty = True
    hook_stderr_empty = True
    latencies: list[float] = []
    observations: list[dict[str, Any]] = []
    forbidden_prompts: list[str] = []
    forbidden_cwds: list[str] = []
    false_positive_count = 0
    false_negative_count = 0

    for case in cases:
        case_id = case["case_id"]
        session_id = f"participation-lab:{case_id}"
        cwd = workspace_cwd(case["workspace"])
        event = base_event(
            "UserPromptSubmit",
            session_id=session_id,
            turn_id=f"turn:{case_id}",
            cwd=cwd,
        )
        event["prompt"] = case["prompt"]
        result, latency_ms = run_hook(hook_script, state_root, event)
        hook_stdout_empty &= result.stdout == ""
        hook_stderr_empty &= result.stderr == ""
        latencies.append(latency_ms)
        case_receipts = load_receipt_log(state_root, session_id)
        if len(case_receipts) != 1:
            raise ParticipationLabError("prompt case did not emit exactly one receipt")
        receipt = case_receipts[0]
        Draft202012Validator(
            receipt_schema,
            format_checker=FormatChecker(),
        ).validate(receipt)
        observed = receipt["observation"]
        passed = (
            observed["route_class"] == case["expected_route"]
            and observed["opportunity_class"]
            == case["expected_opportunity_class"]
            and observed["opportunity_state"]
            == case["expected_opportunity_state"]
        )
        if case["expected_route"] == "none" and observed["route_class"] != "none":
            false_positive_count += 1
        if case["expected_route"] != "none" and observed["route_class"] == "none":
            false_negative_count += 1
        observations.append(
            {
                "case_id": case_id,
                "case_family": case["case_family"],
                "expected_route": case["expected_route"],
                "observed_route": observed["route_class"],
                "expected_opportunity_state": case["expected_opportunity_state"],
                "observed_opportunity_state": observed["opportunity_state"],
                "passed": passed,
                "latency_ms": round(latency_ms, 3),
                "receipt_digest": receipt["receipt_digest"],
            }
        )
        forbidden_prompts.append(case["prompt"])
        forbidden_cwds.append(cwd)

    lifecycle_session = "participation-lab:lifecycle"
    lifecycle_events = [
        {
            **base_event(
                "SessionStart",
                session_id=lifecycle_session,
                turn_id="turn:lifecycle",
                cwd="/srv/AbyssOS/aoa-memo",
            ),
            "source": "resume",
        },
        {
            **base_event(
                "PreCompact",
                session_id=lifecycle_session,
                turn_id="turn:lifecycle",
                cwd="/srv/AbyssOS/aoa-memo",
            ),
            "trigger": "auto",
        },
        {
            **base_event(
                "PostCompact",
                session_id=lifecycle_session,
                turn_id="turn:lifecycle",
                cwd="/srv/AbyssOS/aoa-memo",
            ),
            "trigger": "auto",
        },
        {
            **base_event(
                "Stop",
                session_id=lifecycle_session,
                turn_id="turn:lifecycle",
                cwd="/srv/AbyssOS/aoa-memo",
            ),
            "stop_hook_active": False,
            "last_assistant_message": "SECRET-ASSISTANT-MESSAGE",
        },
        {
            **base_event(
                "PostToolUse",
                session_id=lifecycle_session,
                turn_id="turn:lifecycle",
                cwd="/srv/AbyssOS/aoa-memo",
            ),
            "tool_name": "mcp__aoa_memo__aoa_memo_brief",
            "tool_use_id": "tool:synthetic-lab",
            "tool_input": {"intent": "SECRET-TOOL-INPUT"},
            "tool_response": {
                "content": [
                    {
                        "type": "text",
                        "text": "SECRET-MEMORY-RESULT",
                    }
                ]
            },
        },
        {
            **base_event(
                "SessionEnd",
                session_id=lifecycle_session,
                turn_id="turn:lifecycle",
                cwd="/srv/AbyssOS/aoa-memo",
            ),
            "reason": "other",
        },
    ]
    for event in lifecycle_events:
        result, _ = run_hook(hook_script, state_root, event)
        hook_stdout_empty &= result.stdout == ""
        hook_stderr_empty &= result.stderr == ""

    summary_result = subprocess.run(
        [
            sys.executable,
            str(hook_script),
            "summary",
            "--state-root",
            str(state_root),
        ],
        text=True,
        capture_output=True,
        check=False,
        timeout=10,
    )
    if summary_result.returncode != 0:
        raise ParticipationLabError("memo participation summary is invalid")
    hook_summary = json.loads(summary_result.stdout)

    logs_valid, chains_valid, events_seen, receipt_count = validate_receipts(
        state_root,
        receipt_schema,
        hook_module,
    )
    receipt_files = sorted((state_root / "sessions").glob("*.jsonl"))
    persisted_receipts = "\n".join(
        path.read_text(encoding="utf-8")
        for path in receipt_files
    )
    case_marker_leak_count = sum(
        1
        for case in cases
        if f"MARKER-{case['case_id']}" in persisted_receipts
    )
    raw_prompt_persisted = any(
        prompt in persisted_receipts
        for prompt in forbidden_prompts
    )
    cwd_persisted = any(
        cwd in persisted_receipts
        for cwd in forbidden_cwds
    )

    composition, composition_checks, composed_config = run_composition(
        stack_root=stack_root,
        memo_root=memo_root,
        native_hooks=native_hooks,
        state_root=state_root,
    )

    privacy = {
        "raw_prompt_persisted": raw_prompt_persisted,
        "transcript_path_persisted": (
            "SECRET-TRANSCRIPT-PATH" in persisted_receipts
        ),
        "cwd_persisted": cwd_persisted,
        "tool_input_persisted": "SECRET-TOOL-INPUT" in persisted_receipts,
        "tool_response_persisted": "SECRET-MEMORY-RESULT" in persisted_receipts,
        "assistant_message_persisted": (
            "SECRET-ASSISTANT-MESSAGE" in persisted_receipts
        ),
        "case_marker_leak_count": case_marker_leak_count,
        "raw_binding_value_in_composition_receipt": (
            composition_checks["raw_binding_value_in_receipt"]
        ),
    }

    exact_match_count = sum(
        1 for observation in observations if observation["passed"]
    )
    source_pins = {
        "participation_runner": file_digest(Path(__file__)),
        "participation_trigger_corpus": file_digest(CASES_PATH),
        "participation_report_schema": file_digest(REPORT_SCHEMA_PATH),
        "memo_participation_hook": file_digest(hook_script),
        "memo_participation_receipt_schema": file_digest(receipt_schema_path),
        "memo_hook_fragment": file_digest(fragment_path),
        "memo_hook_fragment_schema": file_digest(fragment_schema_path),
        "stack_hook_compositor": file_digest(compositor_path),
        "stack_hook_fragment_schema": file_digest(stack_fragment_schema_path),
        "stack_hook_receipt_schema": file_digest(stack_receipt_schema_path),
        "native_hook_input": file_digest(native_hooks),
        **skill_pins,
    }

    gates = {
        "trigger_corpus_exact": exact_match_count == len(cases),
        "trigger_families_complete": {
            case["case_family"]
            for case in cases
        } == {"direct", "indirect", "incomplete", "negative", "edge"},
        "skill_contract_exact": (
            all(
                skill_contract[field]
                for field in (
                    "materiality_trigger_present",
                    "fast_lane_present",
                    "one_brief_budget_present",
                    "silence_present",
                    "deep_gate_present",
                    "sibling_handoffs_present",
                )
            )
            and skill_contract["session_memory_dependency"] is False
        ),
        "receipt_schema_valid": logs_valid,
        "receipt_hash_chains_valid": chains_valid,
        "hook_output_silent": hook_stdout_empty and hook_stderr_empty,
        "hook_failures_zero": hook_summary["counts"]["hook_failures"] == 0,
        "content_minimized": not any(
            (
                privacy["raw_prompt_persisted"],
                privacy["transcript_path_persisted"],
                privacy["cwd_persisted"],
                privacy["tool_input_persisted"],
                privacy["tool_response_persisted"],
                privacy["assistant_message_persisted"],
                bool(privacy["case_marker_leak_count"]),
                privacy["raw_binding_value_in_composition_receipt"],
            )
        ),
        "independent_composition_exact": (
            composition["standalone_native_preserved"]
            and composition["owner_metadata_removed"]
            and composition["unresolved_binding_count"] == 0
            and composition["backup_created"]
            and composition_checks["native_unchanged"]
            and composition_checks["composition_receipt_valid"]
        ),
        "benefit_claim_closed": (
            hook_summary["claims"]["benefit_claim_allowed"] is False
            and hook_summary["claims"]["noticed"] == "unknown"
            and hook_summary["claims"]["outcome"] == "unknown"
        ),
        "live_config_untouched": composition["live_config_touched"] is False,
    }
    exit_gate_passed = all(gates.values())
    receipt_state_bytes = sum(path.stat().st_size for path in receipt_files)

    report = {
        "schema_version": "aoa_memo_phase13_participation_lab_v0",
        "report_id": "aoa-memo-phase13-participation-mechanism-20260729",
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "posture": "source_local_shadow_mechanism_no_live_activation",
        "source_pins": source_pins,
        "variants": {
            "P0": "named_baseline_not_executed_in_mechanism_lab",
            "P1": "two_speed_skill_source_validated",
            "P2": "shadow_hook_and_composition_executed_disposably",
            "P3": "selective_route_only_cue_closed_not_executed",
        },
        "skill_contract": skill_contract,
        "trigger_corpus": {
            "case_count": len(cases),
            "families": sorted(
                {
                    case["case_family"]
                    for case in cases
                }
            ),
            "exact_match_count": exact_match_count,
            "false_positive_count": false_positive_count,
            "false_negative_count": false_negative_count,
            "observations": observations,
        },
        "lifecycle": {
            "events_seen": sorted(events_seen),
            "receipt_count": receipt_count,
            "receipt_logs_valid": logs_valid,
            "hash_chains_valid": chains_valid,
            "hook_stdout_empty": hook_stdout_empty,
            "hook_stderr_empty": hook_stderr_empty,
            "hook_failure_count": hook_summary["counts"]["hook_failures"],
        },
        "composition": composition,
        "privacy": privacy,
        "evidence_ladder": {
            "opportunity": "synthetic_corpus_observed",
            "noticed": "unknown",
            "invocation": "synthetic_posttool_observed",
            "result_returned": "synthetic_posttool_observed",
            "used_or_rejected": "unknown",
            "action_change": "unknown",
            "outcome": "unknown",
            "benefit_claim_allowed": False,
        },
        "performance": {
            "prompt_hook_observation_count": len(latencies),
            "p50_hook_latency_ms": round(statistics.median(latencies), 3),
            "p95_hook_latency_ms": round(percentile(latencies, 0.95), 3),
            "max_hook_latency_ms": round(max(latencies), 3),
            "receipt_state_bytes": receipt_state_bytes,
            "composed_config_bytes": composition_checks[
                "composition_output_bytes"
            ],
        },
        "gates": gates,
        "exit_gate_passed": exit_gate_passed,
        "verdict": (
            "supports source-local H0 participation mechanism continuation"
            if exit_gate_passed
            else "does not support source-local H0 participation mechanism continuation"
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
            "Synthetic trigger matches do not prove that a Codex model noticed or selected the skill.",
            "The synthetic PostToolUse event proves receipt mechanics, not natural MCP invocation.",
            "The composed file is disposable and was not trusted or installed as the live Codex hook definition.",
            "No memory packet or route-only cue was injected into model context.",
            "Invocation and result-return stages do not establish use, action change, outcome, or benefit.",
            "P0 versus P1 fresh-session behavior and natural operator value remain separate held-out work.",
        ],
        "report_digest": "",
    }
    report["report_digest"] = normalized_report_digest(report)
    validate_report(report)
    return report


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--memo-root", type=Path, required=True)
    result.add_argument("--stack-root", type=Path, required=True)
    result.add_argument("--native-hooks", type=Path, required=True)
    result.add_argument("--state-root", type=Path, required=True)
    result.add_argument("--output", type=Path, required=True)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        report = run_participation_lab(
            memo_root=args.memo_root.resolve(),
            stack_root=args.stack_root.resolve(),
            native_hooks=args.native_hooks.resolve(),
            state_root=args.state_root.resolve(),
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
    except (
        ParticipationLabError,
        OSError,
        ValueError,
        KeyError,
        TypeError,
        subprocess.SubprocessError,
    ) as exc:
        print(f"participation lab: invalid: {exc}", file=sys.stderr)
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
