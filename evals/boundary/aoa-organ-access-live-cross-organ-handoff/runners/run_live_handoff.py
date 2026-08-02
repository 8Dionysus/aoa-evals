#!/usr/bin/env python3
"""Review one exact private direct-owner cross-organ handoff."""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile
from typing import Any, Callable

import jsonschema


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
REPORT_SCHEMA = BUNDLE_ROOT / "reports" / "summary.schema.json"
MAX_INPUT_BYTES = 2 * 1024 * 1024
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
SECRET_KEY_RE = re.compile(
    r"(?:^|[_-])(token|password|passwd|secret|private[_-]?key|bearer)(?:$|[_-])",
    re.IGNORECASE,
)
SECRET_VALUE_RE = re.compile(
    r"(?:Bearer\s+[A-Za-z0-9._~+/-]{12,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|gh[oprsu]_[A-Za-z0-9]{20,})",
    re.IGNORECASE,
)

EXPECTED_STAGES = (
    ("kag_evidence", "aoa-kag", "read", "observe", "awaiting_memo_candidate", "memo_candidate", "aoa-memo", "observed"),
    ("memo_candidate", "aoa-memo", "candidate", "prepare_candidate", "awaiting_eval_request", "eval_request", "aoa-evals", "candidate_created"),
    ("eval_request", "aoa-evals", "candidate", "prepare_candidate", "awaiting_eval_result", "eval_result", "aoa-evals", "request_created"),
)
EXPECTED_CALLS = (
    ("aoa-kag", "aoa-kag-mcp", "kag_search", ("kag_discover", "kag_search", "kag_read", "kag_traverse", "kag_explain")),
    ("aoa-memo", "aoa-memo-mcp-candidate", "aoa_memo_create_candidate", ("aoa_memo_create_candidate", "aoa_memo_prepare_intake_packet", "aoa_memo_prepare_forwarding_receipt")),
    ("aoa-evals", "aoa-evals-mcp-candidate-eval-request-prepare", "aoa_evals_prepare_request_candidate", ("aoa_evals_prepare_request_candidate",)),
)


class ReviewError(RuntimeError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def parse_time(value: Any, *, field: str) -> datetime:
    if not isinstance(value, str):
        raise ReviewError("invalid_time", f"{field} must be RFC 3339 text")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ReviewError("invalid_time", f"{field} is not RFC 3339") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ReviewError("invalid_time", f"{field} must be timezone-aware")
    return parsed.astimezone(timezone.utc)


def format_time(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ReviewError("duplicate_json_key", f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def reject_secret_material(value: Any, *, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if SECRET_KEY_RE.search(str(key)) and key not in {
                "credential_class",
                "token_usage",
            }:
                raise ReviewError("secret_material", f"secret-like key at {path}.{key}")
            reject_secret_material(child, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_secret_material(child, path=f"{path}[{index}]")
    elif isinstance(value, str) and SECRET_VALUE_RE.search(value):
        raise ReviewError("secret_material", f"secret-like value at {path}")


def load_private_json(path: Path, *, label: str) -> dict[str, Any]:
    try:
        info = path.lstat()
    except OSError as exc:
        raise ReviewError("missing_input", f"{label} is unavailable") from exc
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
        raise ReviewError("unsafe_input", f"{label} must be a regular non-symlink file")
    if info.st_size <= 0 or info.st_size > MAX_INPUT_BYTES:
        raise ReviewError("unsafe_input", f"{label} has an invalid size")
    if stat.S_IMODE(info.st_mode) & 0o077:
        raise ReviewError("unsafe_permissions", f"{label} must not be group/world accessible")
    try:
        payload = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_pairs,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReviewError("invalid_json", f"{label} is not valid JSON") from exc
    if not isinstance(payload, dict):
        raise ReviewError("invalid_json", f"{label} must contain an object")
    reject_secret_material(payload)
    return payload


def _without(payload: dict[str, Any], key: str) -> dict[str, Any]:
    result = dict(payload)
    result.pop(key, None)
    return result


def _assert_digest(value: Any, *, label: str) -> str:
    if not isinstance(value, str) or DIGEST_RE.fullmatch(value) is None:
        raise ReviewError("invalid_digest", f"{label} is not a sha256 digest")
    return value


def _build_run_snapshot(
    *,
    run_id: str,
    request_digest: str,
    request: dict[str, Any],
    stages: list[dict[str, Any]],
    state: str,
    next_stage_kind: str | None,
    next_owner: str | None,
    stop_reason_codes: list[str] | None = None,
) -> dict[str, Any]:
    run = {
        "schema_version": "aoa_cross_organ_orchestration_run_v1",
        "run_id": run_id,
        "request_digest": request_digest,
        "request": request,
        "stages": stages,
        "snapshot_digest": "sha256:" + ("0" * 64),
        "state": state,
        "next_stage_kind": next_stage_kind,
        "next_owner": next_owner,
        "stop_reason_codes": stop_reason_codes or [],
        "owner_tools_executed_by_sdk": False,
        "proof_computed_by_sdk": False,
        "durable_memory_written_by_sdk": False,
        "acceptance_inferred_by_sdk": False,
        "runtime_execution_authorized": False,
    }
    run["snapshot_digest"] = digest(_without(run, "snapshot_digest"))
    return run


def reconstruct_snapshot(snapshot: dict[str, Any], reviewed_at: datetime) -> None:
    if snapshot.get("schema_version") != "aoa_cross_organ_orchestration_run_v1":
        raise ReviewError("snapshot_schema", "unexpected orchestration schema")
    request = snapshot.get("request")
    if not isinstance(request, dict):
        raise ReviewError("snapshot_schema", "request is missing")
    request_digest = digest(request)
    if snapshot.get("request_digest") != request_digest:
        raise ReviewError("request_digest", "request digest mismatch")
    owners = request.get("owners")
    if not isinstance(owners, dict) or owners != {
        "acceptance_owner": "aoa-memo",
        "control_owner": "aoa-sdk",
        "evidence_owner": "aoa-kag",
        "memory_owner": "aoa-memo",
        "proof_owner": "aoa-evals",
        "runtime_owner": "abyss-stack",
    }:
        raise ReviewError("owner_contract", "owner map is not the pinned direct-owner chain")
    for field in (
        "hidden_shared_context_allowed",
        "hidden_server_chaining_allowed",
        "automatic_candidate_promotion_allowed",
        "automatic_acceptance_allowed",
        "model_confidence_is_acceptance_authority",
    ):
        if request.get(field) is not False:
            raise ReviewError("authority_boundary", f"request field {field} must be false")
    if request.get("host_visible_receipts_required") is not True:
        raise ReviewError("authority_boundary", "host-visible receipts must be required")
    expires_at = parse_time(request.get("expires_at"), field="request.expires_at")
    if reviewed_at >= expires_at:
        raise ReviewError("request_expired", "orchestration request expired before review")

    run_id = _assert_digest(snapshot.get("run_id"), label="run_id")
    expected_run_id = digest(
        {
            "schema_version": "aoa_cross_organ_orchestration_run_v1",
            "request_id": request.get("request_id"),
            "request_digest": request_digest,
            "control_owner": "aoa-sdk",
            "host_id": request.get("host_id"),
        }
    )
    if run_id != expected_run_id:
        raise ReviewError("run_identity", "run id does not match its request")
    root_input = request.get("root_input")
    if not isinstance(root_input, dict):
        raise ReviewError("snapshot_schema", "root input is missing")
    expected = _build_run_snapshot(
        run_id=run_id,
        request_digest=request_digest,
        request=request,
        stages=[],
        state="awaiting_kag_evidence",
        next_stage_kind="kag_evidence",
        next_owner="aoa-kag",
    )
    stages = snapshot.get("stages")
    if not isinstance(stages, list) or len(stages) != 3:
        raise ReviewError("stage_count", "proof review requires exactly three stages")
    previous_output = root_input
    rebuilt_stages: list[dict[str, Any]] = []
    previous_stage_digest: str | None = None
    for index, (stage, spec) in enumerate(zip(stages, EXPECTED_STAGES, strict=True)):
        if not isinstance(stage, dict) or not isinstance(stage.get("observation"), dict):
            raise ReviewError("stage_schema", f"stage {index} is malformed")
        observation = stage["observation"]
        stage_kind, owner, ceiling, effect, next_state, next_kind, next_owner, outcome = spec
        if stage.get("sequence") != index or stage.get("previous_stage_digest") != previous_stage_digest:
            raise ReviewError("stage_order", f"stage {index} sequence or predecessor drifted")
        if stage.get("stage_digest") != digest(_without(stage, "stage_digest")):
            raise ReviewError("stage_digest", f"stage {index} digest mismatch")
        if observation.get("stage_kind") != stage_kind:
            raise ReviewError("stage_order", f"stage {index} kind drifted")
        if observation.get("stage_owner") != owner:
            raise ReviewError("wrong_owner", f"stage {index} came from the wrong owner")
        if observation.get("authority_ceiling") != ceiling or observation.get("effect_class") != effect:
            raise ReviewError("authority_boundary", f"stage {index} policy contour drifted")
        if observation.get("transition_state") != "proceed" or observation.get("next_owner") != next_owner:
            raise ReviewError("transition_state", f"stage {index} did not proceed to its pinned owner")
        if observation.get("stop_reason_codes") != []:
            raise ReviewError("transition_state", f"stage {index} carries stop reasons on success")
        if observation.get("input_ref") != previous_output:
            raise ReviewError("typed_handoff", f"stage {index} input is not the previous output")
        output_ref = observation.get("output_ref")
        if not isinstance(output_ref, dict) or output_ref.get("owner") != owner:
            raise ReviewError("wrong_owner", f"stage {index} output owner drifted")
        if observation.get("source_revision") != output_ref.get("source_revision"):
            raise ReviewError("source_revision", f"stage {index} source revision drifted")
        if observation.get("output_schema_identity") != output_ref.get("schema_identity"):
            raise ReviewError("schema_drift", f"stage {index} output schema drifted")
        if observation.get("freshness_state") not in {"exact", "compatible_drift"}:
            raise ReviewError("stale_evidence", f"stage {index} evidence is not usable")
        observed_at = parse_time(observation.get("observed_at"), field=f"stage[{index}].observed_at")
        stage_expires = parse_time(observation.get("expires_at"), field=f"stage[{index}].expires_at")
        if not observed_at < reviewed_at < stage_expires or stage_expires > expires_at:
            raise ReviewError("stale_evidence", f"stage {index} is outside its evidence window")
        evidence_refs = observation.get("evidence_refs")
        if not isinstance(evidence_refs, list) or not any(
            isinstance(item, dict) and item.get("owner") == owner for item in evidence_refs
        ):
            raise ReviewError("owner_evidence", f"stage {index} lacks owner-qualified evidence")
        for evidence in evidence_refs:
            if not isinstance(evidence, dict):
                raise ReviewError("owner_evidence", f"stage {index} evidence is malformed")
            evidence_expiry = evidence.get("expires_at")
            if evidence_expiry is not None and parse_time(evidence_expiry, field="evidence.expires_at") <= reviewed_at:
                raise ReviewError("stale_evidence", f"stage {index} evidence expired")
        receipt = observation.get("receipt")
        if not isinstance(receipt, dict):
            raise ReviewError("receipt_schema", f"stage {index} receipt is missing")
        if receipt.get("receipt_digest") != digest(_without(receipt, "receipt_digest")):
            raise ReviewError("receipt_digest", f"stage {index} receipt digest mismatch")
        if receipt.get("run_id") != run_id or receipt.get("host_id") != request.get("host_id"):
            raise ReviewError("receipt_binding", f"stage {index} receipt scope drifted")
        if receipt.get("previous_snapshot_digest") != expected["snapshot_digest"]:
            raise ReviewError("replay", f"stage {index} receipt replays another snapshot")
        if receipt.get("stage_kind") != stage_kind or receipt.get("outcome") != outcome:
            raise ReviewError("receipt_binding", f"stage {index} receipt outcome drifted")
        if receipt.get("input_artifact_digest") != previous_output.get("artifact_digest") or receipt.get("output_artifact_digest") != output_ref.get("artifact_digest"):
            raise ReviewError("receipt_binding", f"stage {index} receipt artifact binding drifted")
        issued_at = parse_time(receipt.get("issued_at"), field=f"stage[{index}].receipt.issued_at")
        if issued_at < observed_at or issued_at >= stage_expires:
            raise ReviewError("expired_receipt", f"stage {index} receipt is outside the stage window")
        rebuilt_stage = deepcopy(stage)
        rebuilt_stages.append(rebuilt_stage)
        previous_stage_digest = stage["stage_digest"]
        previous_output = output_ref
        expected = _build_run_snapshot(
            run_id=run_id,
            request_digest=request_digest,
            request=request,
            stages=deepcopy(rebuilt_stages),
            state=next_state,
            next_stage_kind=next_kind,
            next_owner=next_owner,
        )
    if snapshot != expected:
        if snapshot.get("state") != "awaiting_eval_result":
            raise ReviewError("acceptance_present", "run closed or advanced before proof result")
        raise ReviewError("snapshot_digest", "snapshot does not match deterministic reconstruction")


def validate_direct_calls(
    snapshot: dict[str, Any],
    calls: tuple[dict[str, Any], ...],
    outputs: tuple[dict[str, Any], ...],
    output_paths: tuple[Path, ...],
) -> list[dict[str, Any]]:
    stages = snapshot["stages"]
    direct: list[dict[str, Any]] = []
    for index, (call, spec) in enumerate(zip(calls, EXPECTED_CALLS, strict=True)):
        owner, server_name, tool, inventory = spec
        stage_output = stages[index]["observation"]["output_ref"]
        if call.get("protocol_version") != "2025-11-25":
            raise ReviewError("protocol_pair", f"{owner} protocol drifted")
        server_info = call.get("server_info")
        if not isinstance(server_info, dict) or server_info.get("name") != server_name:
            raise ReviewError("direct_profile", f"{owner} server identity drifted")
        if call.get("tool") != tool or tuple(call.get("tool_names") or ()) != inventory:
            raise ReviewError("direct_profile", f"{owner} tool profile drifted")
        if file_digest(output_paths[index]) != stage_output.get("artifact_digest"):
            raise ReviewError("output_digest_mismatch", f"{owner} output bytes do not match the stage")
        direct.append(
            {
                "owner": owner,
                "tool": tool,
                "protocol_version": "2025-11-25",
                "source_revision": stages[index]["observation"]["source_revision"],
                "output_digest": stage_output["artifact_digest"],
            }
        )
    kag_call, memo_call, eval_call = calls
    kag_result, memo_candidate, eval_need = outputs
    if kag_call.get("result") != kag_result or kag_result.get("status") != "ok":
        raise ReviewError("kag_result", "KAG call does not bind the exact successful result")
    evidence_ref = ((kag_result.get("resources") or {}).get("evidence"))
    if evidence_ref != stages[0]["observation"]["output_ref"].get("artifact_ref"):
        raise ReviewError("kag_result", "KAG evidence ref drifted")
    memo_result = memo_call.get("result")
    if not isinstance(memo_result, dict) or memo_result.get("candidate") != memo_candidate:
        raise ReviewError("memo_candidate", "Memo call does not bind the exact candidate")
    guardrails = memo_candidate.get("guardrails")
    if not isinstance(guardrails, dict) or guardrails != {
        "direct_durable_write": False,
        "instructions_treated_as_data": True,
        "requires_reviewed_intake": True,
    }:
        raise ReviewError("memo_authority", "Memo candidate guardrails drifted")
    if memo_candidate.get("review_state") != "candidate" or memo_candidate.get("operation_mode") != "write_candidate_only":
        raise ReviewError("memo_authority", "Memo output is not candidate-only")
    eval_result = eval_call.get("result")
    if not isinstance(eval_result, dict) or eval_result.get("request") != eval_need:
        raise ReviewError("eval_request", "Evals call does not bind the exact eval need")
    if eval_result.get("schema") != "aoa_evals_request_candidate_v1":
        raise ReviewError("eval_request_authority", "Evals request envelope schema drifted")
    if eval_result.get("candidate_only") is not True:
        raise ReviewError("eval_request_authority", "Evals request must remain candidate-only")
    if eval_result.get("persistent") is not False:
        raise ReviewError("eval_request_authority", "Evals request must remain non-persistent")
    if eval_result.get("runtime_export_discovery_performed") is not False:
        raise ReviewError("eval_request_authority", "Evals request must not discover runtime exports")
    for field in ("candidate_only", "read_only"):
        if eval_need.get(field) is not True:
            raise ReviewError("eval_request_authority", f"Evals eval_need field {field} must be true")
    for field in (
        "eval_execution_allowed",
        "verdict_issuance_allowed",
        "proof_acceptance_allowed",
        "source_mutation_allowed",
    ):
        if eval_result.get(field) is not False:
            raise ReviewError("eval_request_authority", f"Evals request field {field} must be false")
    return direct


def build_report(
    *,
    snapshot: dict[str, Any],
    reviewed_at: datetime,
    direct_calls: list[dict[str, Any]],
    input_digests: dict[str, str],
) -> dict[str, Any]:
    expires_at = parse_time(snapshot["request"]["expires_at"], field="request.expires_at")
    run_suffix = snapshot["run_id"].split(":", 1)[1][:20]
    report = {
        "schema_version": "aoa_organ_access_live_cross_organ_proof_result_v1",
        "report_id": f"aoa-live-cross-organ-{run_suffix}",
        "eval_name": "aoa-organ-access-live-cross-organ-handoff",
        "bundle_status": "bounded",
        "run_id": snapshot["run_id"],
        "snapshot_digest": snapshot["snapshot_digest"],
        "proof_question": "Does this exact direct-owner KAG to Memo to Evals chain preserve typed handoffs, current evidence, proof authority in aoa-evals, and durable acceptance authority in aoa-memo without hidden chaining?",
        "reviewed_at": format_time(reviewed_at),
        "expires_at": format_time(expires_at),
        "verdict": "supported_bounded",
        "stage_count": 3,
        "direct_owner_calls": direct_calls,
        "checks": {
            "snapshot_reconstructed": True,
            "stage_and_receipt_digests_valid": True,
            "typed_handoffs_exact": True,
            "direct_profiles_exact": True,
            "owner_outputs_content_bound": True,
            "evidence_current": True,
            "authority_separation_preserved": True,
            "acceptance_absent": True,
        },
        "input_digests": input_digests,
        "authority_boundary": {
            "proof_owner": "aoa-evals",
            "acceptance_owner": "aoa-memo",
            "owner_tools_executed_by_evals": False,
            "durable_memory_written": False,
            "owner_acceptance_inferred": False,
            "admission_authorized": False,
            "runtime_execution_authorized": False,
        },
        "limitations": [
            "This result does not accept the Memo candidate or write durable memory.",
            "This result does not authorize admission, runtime effects, or rollback.",
            "This result is limited to the exact content-addressed run and expiry window.",
            "Absence of hidden chaining is bounded to the inspected direct profiles, receipts, and fixed-false orchestration contract.",
        ],
        "next_owner": "aoa-memo",
        "result_digest": "sha256:" + ("0" * 64),
    }
    report["result_digest"] = digest(_without(report, "result_digest"))
    schema = json.loads(REPORT_SCHEMA.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(report)
    return report


def write_private_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(path.parent, 0o700)
    temp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(temp, flags, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
        os.chmod(path, 0o600)
    finally:
        if temp.exists():
            temp.unlink()


def review(
    *,
    snapshot_path: Path,
    kag_call_path: Path,
    kag_result_path: Path,
    memo_call_path: Path,
    memo_candidate_path: Path,
    eval_call_path: Path,
    eval_need_path: Path,
    reviewed_at: datetime,
) -> dict[str, Any]:
    paths = (
        snapshot_path,
        kag_call_path,
        kag_result_path,
        memo_call_path,
        memo_candidate_path,
        eval_call_path,
        eval_need_path,
    )
    labels = ("snapshot", "kag_call", "kag_result", "memo_call", "memo_candidate", "eval_call", "eval_need")
    payloads = tuple(load_private_json(path, label=label) for path, label in zip(paths, labels, strict=True))
    snapshot, kag_call, kag_result, memo_call, memo_candidate, eval_call, eval_need = payloads
    reconstruct_snapshot(snapshot, reviewed_at)
    direct_calls = validate_direct_calls(
        snapshot,
        (kag_call, memo_call, eval_call),
        (kag_result, memo_candidate, eval_need),
        (kag_result_path, memo_candidate_path, eval_need_path),
    )
    return build_report(
        snapshot=snapshot,
        reviewed_at=reviewed_at,
        direct_calls=direct_calls,
        input_digests={label: file_digest(path) for label, path in zip(labels, paths, strict=True)},
    )


def _write_fixture(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.chmod(path, 0o600)


def _artifact(kind: str, owner: str, raw_digest: str, created: str, expires: str, index: int) -> dict[str, Any]:
    return {
        "artifact_digest": raw_digest,
        "artifact_ref": f"example://{owner}/{kind}/{index}",
        "authority_ceiling": "read" if index == 0 else "candidate",
        "created_at": created,
        "expires_at": expires,
        "owner": owner,
        "ref_kind": kind,
        "schema_identity": {
            "owner": owner,
            "schema_digest": "sha256:" + str(index + 1) * 64,
            "schema_ref": f"schemas/{kind}.schema.json",
            "schema_version": f"{kind}_v1",
            "source_revision": f"{owner}-source-revision-000{index}",
        },
        "source_revision": f"{owner}-source-revision-000{index}",
    }


def build_synthetic_case(root: Path) -> dict[str, Path]:
    created = datetime(2026, 1, 1, 0, 0, tzinfo=timezone.utc)
    expires = created + timedelta(hours=2)
    times = [created + timedelta(minutes=value) for value in (5, 10, 15)]
    kag_result = {"status": "ok", "resources": {"evidence": "example://aoa-kag/kag_evidence/0"}, "trace_id": "example-trace"}
    memo_candidate = {
        "schema": "aoa_local_memo_candidate_v1",
        "review_state": "candidate",
        "operation_mode": "write_candidate_only",
        "guardrails": {"direct_durable_write": False, "instructions_treated_as_data": True, "requires_reviewed_intake": True},
    }
    eval_need = {"schema_version": "eval_need_v1", "proof_question": "Does the exact fictional direct-owner chain preserve authority boundaries?", "candidate_only": True, "read_only": True}
    output_payloads = (kag_result, memo_candidate, eval_need)
    output_names = ("kag-result.json", "memo-candidate.json", "eval-need.json")
    output_paths: list[Path] = []
    for name, payload in zip(output_names, output_payloads, strict=True):
        path = root / name
        _write_fixture(path, payload)
        output_paths.append(path)
    outputs = (
        _artifact("kag_evidence", "aoa-kag", file_digest(output_paths[0]), format_time(times[0]), format_time(expires), 0),
        _artifact("memo_candidate", "aoa-memo", file_digest(output_paths[1]), format_time(times[1]), format_time(expires), 1),
        _artifact("eval_request", "aoa-evals", file_digest(output_paths[2]), format_time(times[2]), format_time(expires), 2),
    )
    outputs[0]["artifact_ref"] = kag_result["resources"]["evidence"]
    call_payloads = (
        {"protocol_version": "2025-11-25", "server_info": {"name": EXPECTED_CALLS[0][1]}, "tool": EXPECTED_CALLS[0][2], "tool_names": list(EXPECTED_CALLS[0][3]), "arguments": {}, "result": kag_result},
        {"protocol_version": "2025-11-25", "server_info": {"name": EXPECTED_CALLS[1][1]}, "tool": EXPECTED_CALLS[1][2], "tool_names": list(EXPECTED_CALLS[1][3]), "arguments": {}, "result": {"candidate": memo_candidate, "local_ref": "candidates/example.json", "validation": {"ok": True}}},
        {"protocol_version": "2025-11-25", "server_info": {"name": EXPECTED_CALLS[2][1]}, "tool": EXPECTED_CALLS[2][2], "tool_names": list(EXPECTED_CALLS[2][3]), "arguments": {}, "result": {"schema": "aoa_evals_request_candidate_v1", "request": eval_need, "candidate_only": True, "persistent": False, "runtime_export_discovery_performed": False, "eval_execution_allowed": False, "verdict_issuance_allowed": False, "proof_acceptance_allowed": False, "source_mutation_allowed": False}},
    )
    call_names = ("kag-call.json", "memo-call.json", "eval-call.json")
    call_paths: list[Path] = []
    for name, payload in zip(call_names, call_payloads, strict=True):
        path = root / name
        _write_fixture(path, payload)
        call_paths.append(path)
    root_input = {
        "artifact_digest": "sha256:" + "a" * 64,
        "artifact_ref": "example://abyss-stack/intent/1",
        "authority_ceiling": "read",
        "created_at": format_time(created),
        "expires_at": format_time(expires),
        "owner": "abyss-stack",
        "ref_kind": "orchestration_intent",
        "schema_identity": {"owner": "abyss-stack", "schema_digest": "sha256:" + "b" * 64, "schema_ref": "schemas/intent.json", "schema_version": "intent_v1", "source_revision": "abyss-stack-source"},
        "source_revision": "abyss-stack-source",
    }
    request = {
        "schema_version": "aoa_cross_organ_orchestration_request_v1",
        "request_id": "synthetic-direct-owner",
        "intent": "Synthetic direct-owner proof scenario",
        "requested_by": "test",
        "host_id": "synthetic-host",
        "owners": {"acceptance_owner": "aoa-memo", "control_owner": "aoa-sdk", "evidence_owner": "aoa-kag", "memory_owner": "aoa-memo", "proof_owner": "aoa-evals", "runtime_owner": "abyss-stack"},
        "root_input": root_input,
        "stage_contracts": [],
        "evidence_refs": [{"owner": "abyss-stack"}],
        "created_at": format_time(created),
        "expires_at": format_time(expires),
        "hidden_shared_context_allowed": False,
        "hidden_server_chaining_allowed": False,
        "automatic_candidate_promotion_allowed": False,
        "automatic_acceptance_allowed": False,
        "model_confidence_is_acceptance_authority": False,
        "host_visible_receipts_required": True,
    }
    request_digest = digest(request)
    run_id = digest({"schema_version": "aoa_cross_organ_orchestration_run_v1", "request_id": request["request_id"], "request_digest": request_digest, "control_owner": "aoa-sdk", "host_id": request["host_id"]})
    current = _build_run_snapshot(run_id=run_id, request_digest=request_digest, request=request, stages=[], state="awaiting_kag_evidence", next_stage_kind="kag_evidence", next_owner="aoa-kag")
    stages: list[dict[str, Any]] = []
    previous = root_input
    previous_stage_digest: str | None = None
    for index, (output, spec) in enumerate(zip(outputs, EXPECTED_STAGES, strict=True)):
        stage_kind, owner, ceiling, effect, state, next_kind, next_owner, outcome = spec
        observation = {
            "stage_kind": stage_kind,
            "stage_owner": owner,
            "source_revision": output["source_revision"],
            "input_ref": previous,
            "output_ref": output,
            "input_schema_identity": previous["schema_identity"],
            "output_schema_identity": output["schema_identity"],
            "evidence_refs": [{"owner": owner, "artifact_ref": f"example://evidence/{index}", "artifact_digest": "sha256:" + str(index + 4) * 64, "observed_at": format_time(times[index]), "expires_at": format_time(expires)}],
            "freshness_state": "exact",
            "observed_at": format_time(times[index]),
            "expires_at": format_time(expires),
            "authority_ceiling": ceiling,
            "effect_class": effect,
            "applied_state": "not_applied" if index == 0 else "candidate_only",
            "receipt": {
                "schema_version": "aoa_host_stage_receipt_v1",
                "receipt_id": f"receipt-{index}",
                "receipt_ref": f"example://receipt/{index}",
                "receipt_digest": "sha256:" + "0" * 64,
                "host_id": request["host_id"],
                "run_id": run_id,
                "stage_kind": stage_kind,
                "previous_snapshot_digest": current["snapshot_digest"],
                "input_artifact_digest": previous["artifact_digest"],
                "output_artifact_digest": output["artifact_digest"],
                "issued_at": format_time(times[index] + timedelta(seconds=1)),
                "outcome": outcome,
                "owner_receipt_refs": [],
            },
            "next_owner": next_owner,
            "transition_state": "proceed",
            "stop_reason_codes": [],
            "review_ref": None,
            "acceptance_decision": None,
            "mcp_tools_executed_by_sdk": False,
            "model_confidence_is_acceptance_authority": False,
        }
        observation["receipt"]["receipt_digest"] = digest(_without(observation["receipt"], "receipt_digest"))
        stage = {"schema_version": "aoa_cross_organ_stage_v1", "sequence": index, "previous_stage_digest": previous_stage_digest, "stage_digest": "sha256:" + "0" * 64, "observation": observation}
        stage["stage_digest"] = digest(_without(stage, "stage_digest"))
        stages.append(stage)
        previous = output
        previous_stage_digest = stage["stage_digest"]
        current = _build_run_snapshot(run_id=run_id, request_digest=request_digest, request=request, stages=deepcopy(stages), state=state, next_stage_kind=next_kind, next_owner=next_owner)
    snapshot_path = root / "snapshot.json"
    _write_fixture(snapshot_path, current)
    return {"snapshot": snapshot_path, "kag_call": call_paths[0], "kag_result": output_paths[0], "memo_call": call_paths[1], "memo_candidate": output_paths[1], "eval_call": call_paths[2], "eval_need": output_paths[2]}


def _review_case(paths: dict[str, Path], reviewed_at: datetime) -> dict[str, Any]:
    return review(
        snapshot_path=paths["snapshot"],
        kag_call_path=paths["kag_call"],
        kag_result_path=paths["kag_result"],
        memo_call_path=paths["memo_call"],
        memo_candidate_path=paths["memo_candidate"],
        eval_call_path=paths["eval_call"],
        eval_need_path=paths["eval_need"],
        reviewed_at=reviewed_at,
    )


def run_scenarios() -> dict[str, Any]:
    reviewed_at = datetime(2026, 1, 1, 0, 30, tzinfo=timezone.utc)
    results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="aoa-live-cross-organ-") as directory:
        root = Path(directory)
        os.chmod(root, 0o700)
        paths = build_synthetic_case(root)
        report = _review_case(paths, reviewed_at)
        results.append({"case": "valid_direct_owner_chain", "accepted": report["verdict"] == "supported_bounded", "issue_code": None})

        mutations: tuple[tuple[str, str, Callable[[dict[str, Path]], None]], ...] = (
            ("stale_kag", "stale_evidence", lambda p: _mutate_snapshot(p["snapshot"], lambda s: s["stages"][0]["observation"].update({"freshness_state": "stale_readable"}))),
            ("malformed_memo_candidate", "output_digest_mismatch", lambda p: _mutate_json(p["memo_candidate"], lambda c: c["guardrails"].update({"direct_durable_write": True}))),
            ("eval_rejection", "eval_request_authority", lambda p: _mutate_json(p["eval_call"], lambda c: c["result"].update({"candidate_only": False}))),
            ("wrong_owner", "wrong_owner", lambda p: _mutate_snapshot(p["snapshot"], lambda s: s["stages"][1]["observation"].update({"stage_owner": "wrong-owner"}))),
            ("expired_receipt", "expired_receipt", lambda p: _mutate_snapshot(p["snapshot"], lambda s: s["stages"][1]["observation"]["receipt"].update({"issued_at": s["stages"][1]["observation"]["expires_at"]}))),
            ("replay", "replay", lambda p: _mutate_replay_snapshot(p["snapshot"])),
            ("schema_drift", "schema_drift", lambda p: _mutate_snapshot(p["snapshot"], lambda s: s["stages"][1]["observation"].update({"output_schema_identity": {**s["stages"][1]["observation"]["output_schema_identity"], "schema_digest": "sha256:" + "f" * 64}}))),
            ("acceptance_absent", "acceptance_present", lambda p: _mutate_snapshot(p["snapshot"], lambda s: s.update({"state": "accepted", "next_stage_kind": None, "next_owner": None}))),
            ("unexpected_tool", "direct_profile", lambda p: _mutate_json(p["memo_call"], lambda c: c["tool_names"].append("hidden_proxy"))),
        )
        for case_id, expected_code, mutate in mutations:
            case_root = root / case_id
            case_root.mkdir(mode=0o700)
            case_paths = build_synthetic_case(case_root)
            mutate(case_paths)
            try:
                _review_case(case_paths, reviewed_at)
            except ReviewError as exc:
                results.append({"case": case_id, "accepted": False, "issue_code": exc.code, "expected_issue_code": expected_code})
            else:
                results.append({"case": case_id, "accepted": True, "issue_code": None, "expected_issue_code": expected_code})
    passed = results[0]["accepted"] and all(
        not item["accepted"] and item["issue_code"] == item["expected_issue_code"]
        for item in results[1:]
    )
    return {
        "eval_name": "aoa-organ-access-live-cross-organ-handoff",
        "verdict": "supports bounded claim" if passed else "does not support bounded claim",
        "cases": results,
        "claim_limit": "Offline fictional scenarios prove runner behavior only; they do not prove a live owner call, acceptance, admission, or effect.",
    }


def _mutate_json(path: Path, mutate: Callable[[dict[str, Any]], None]) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    mutate(payload)
    _write_fixture(path, payload)


def _resign_snapshot(snapshot: dict[str, Any]) -> None:
    request = snapshot["request"]
    request_digest = digest(request)
    run_id = snapshot["run_id"]
    current = _build_run_snapshot(run_id=run_id, request_digest=request_digest, request=request, stages=[], state="awaiting_kag_evidence", next_stage_kind="kag_evidence", next_owner="aoa-kag")
    stages: list[dict[str, Any]] = []
    previous_stage_digest: str | None = None
    for index, (stage, spec) in enumerate(zip(snapshot["stages"], EXPECTED_STAGES, strict=False)):
        receipt = stage["observation"]["receipt"]
        receipt["previous_snapshot_digest"] = current["snapshot_digest"]
        receipt["receipt_digest"] = digest(_without(receipt, "receipt_digest"))
        stage["sequence"] = index
        stage["previous_stage_digest"] = previous_stage_digest
        stage["stage_digest"] = digest(_without(stage, "stage_digest"))
        stages.append(stage)
        previous_stage_digest = stage["stage_digest"]
        _, _, _, _, state, next_kind, next_owner, _ = spec
        current = _build_run_snapshot(run_id=run_id, request_digest=request_digest, request=request, stages=deepcopy(stages), state=state, next_stage_kind=next_kind, next_owner=next_owner)
    preserved_state = snapshot.get("state")
    if preserved_state == "accepted":
        current["state"] = "accepted"
        current["next_stage_kind"] = None
        current["next_owner"] = None
        current["snapshot_digest"] = digest(_without(current, "snapshot_digest"))
    snapshot.clear()
    snapshot.update(current)


def _mutate_snapshot(path: Path, mutate: Callable[[dict[str, Any]], None]) -> None:
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    mutate(snapshot)
    _resign_snapshot(snapshot)
    _write_fixture(path, snapshot)


def _mutate_replay_snapshot(path: Path) -> None:
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    replayed_stage = snapshot["stages"][2]
    receipt = replayed_stage["observation"]["receipt"]
    receipt["previous_snapshot_digest"] = snapshot["stages"][0]["observation"][
        "receipt"
    ]["previous_snapshot_digest"]
    receipt["receipt_digest"] = digest(_without(receipt, "receipt_digest"))
    replayed_stage["stage_digest"] = digest(
        _without(replayed_stage, "stage_digest")
    )
    snapshot["snapshot_digest"] = digest(_without(snapshot, "snapshot_digest"))
    _write_fixture(path, snapshot)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("run-scenarios")
    review_parser = subparsers.add_parser("review")
    for name in ("snapshot", "kag-call", "kag-result", "memo-call", "memo-candidate", "eval-call", "eval-need", "output"):
        review_parser.add_argument(f"--{name}", required=True)
    review_parser.add_argument("--reviewed-at")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "run-scenarios":
        result = run_scenarios()
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["verdict"] == "supports bounded claim" else 1
    reviewed_at = (
        parse_time(args.reviewed_at, field="reviewed_at")
        if args.reviewed_at
        else datetime.now(timezone.utc)
    )
    try:
        report = review(
            snapshot_path=Path(args.snapshot),
            kag_call_path=Path(args.kag_call),
            kag_result_path=Path(args.kag_result),
            memo_call_path=Path(args.memo_call),
            memo_candidate_path=Path(args.memo_candidate),
            eval_call_path=Path(args.eval_call),
            eval_need_path=Path(args.eval_need),
            reviewed_at=reviewed_at,
        )
        write_private_json(Path(args.output), report)
    except ReviewError as exc:
        print(json.dumps({"verdict": "rejected", "issue_code": exc.code, "message": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps({"verdict": report["verdict"], "report_id": report["report_id"], "run_id": report["run_id"], "result_digest": report["result_digest"], "next_owner": report["next_owner"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
