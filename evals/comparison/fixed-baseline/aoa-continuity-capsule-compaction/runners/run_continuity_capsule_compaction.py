#!/usr/bin/env python3
"""Run a deterministic, field-level continuity capsule comparison.

This runner consumes only an explicit packet.  It does not read session
storage, execute a provider, contact a runtime, or turn a synthetic packet
into a live compaction claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Mapping, Sequence
from datetime import datetime
from pathlib import Path
from typing import Any

EVAL_NAME = "aoa-continuity-capsule-compaction"
INPUT_SCHEMA_VERSION = "aoa_continuity_capsule_compaction_input_v1"
CAPSULE_SCHEMA_VERSION = "continuity_capsule_v1"
MATERIALIZATION_SCHEMA_VERSION = "continuity_capsule_materialization_v1"
CAPSULE_OWNER_REPO = "aoa-session-memory"
CAPSULE_REF_PREFIX = "continuity-capsule:"
MAX_STRING_LENGTH = 65_536
MAX_LIST_ITEMS = 256
MAX_EVIDENCE_REFS = 512
MAX_PROTECTED_TAIL_BYTES = 512 * 1024
MAX_CASES = 128
CONTENT_FIELDS = (
    "capsule_id",
    "goal",
    "constraints",
    "completed",
    "current_work",
    "blockers",
    "exact_decisions",
    "open_obligations",
    "evidence_refs",
    "omissions_uncertainty",
)
CAPSULE_FIELDS = (
    "schema_version",
    *CONTENT_FIELDS,
    "source_watermark",
    "compaction_event",
    "protected_tail_posture",
)
PRESERVATION_FIELDS = (
    *CONTENT_FIELDS,
    "source_watermark",
    "compaction_event",
    "protected_tail_posture",
    "portable_tail_policy",
    "private_tail_digest",
    "private_tail_bytes",
)


class ContinuityCapsuleInputError(ValueError):
    """Raised when a comparison packet is structurally unsafe to read."""


def _canonical_digest(payload: Mapping[str, Any]) -> str:
    try:
        encoded = json.dumps(
            payload,
            allow_nan=False,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError) as exc:
        raise ContinuityCapsuleInputError(
            "continuity packet must be canonical JSON"
        ) from exc
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _require_mapping(value: Any, *, label: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ContinuityCapsuleInputError(f"{label} must be an object")
    return dict(value)


def _require_digest(value: Any, *, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 71
        or not value.startswith("sha256:")
        or any(character not in "0123456789abcdef" for character in value[7:])
    ):
        raise ContinuityCapsuleInputError(f"{label} must be a lowercase sha256 digest")
    return value


def _require_string(value: Any, *, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContinuityCapsuleInputError(f"{label} must be a non-empty string")
    if len(value) > MAX_STRING_LENGTH:
        raise ContinuityCapsuleInputError(f"{label} exceeds its length ceiling")
    return value


def _require_nonnegative_int(value: Any, *, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ContinuityCapsuleInputError(f"{label} must be a non-negative integer")
    return value


def _require_timestamp(value: Any, *, label: str) -> str:
    text = _require_string(value, label=label)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContinuityCapsuleInputError(
            f"{label} must be an RFC3339 timestamp"
        ) from exc
    if parsed.tzinfo is None:
        raise ContinuityCapsuleInputError(f"{label} must include a timezone")
    return text


def _require_string_list(value: Any, *, label: str) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise ContinuityCapsuleInputError(f"{label} must be a list of strings")
    if len(value) > MAX_LIST_ITEMS:
        raise ContinuityCapsuleInputError(f"{label} exceeds its item ceiling")
    return [
        _require_string(item, label=f"{label}[{index}]")
        for index, item in enumerate(value)
    ]


def _require_keys(value: Mapping[str, Any], expected: set[str], *, label: str) -> None:
    if set(value) != expected:
        raise ContinuityCapsuleInputError(f"{label} has an unexpected or missing field")


def _validate_ref(
    value: Any,
    *,
    digest: str,
    label: str,
    object_id: str | None = None,
) -> dict[str, Any]:
    ref = _require_mapping(value, label=label)
    _require_keys(
        ref,
        {"object_id", "owner_repo", "schema_version", "digest"},
        label=label,
    )
    if (
        not _require_string(ref["object_id"], label=f"{label}.object_id").startswith(
            CAPSULE_REF_PREFIX
        )
        or ref["owner_repo"] != CAPSULE_OWNER_REPO
        or ref["schema_version"] != CAPSULE_SCHEMA_VERSION
    ):
        raise ContinuityCapsuleInputError(f"{label} has the wrong owner or schema")
    if _require_digest(ref["digest"], label=f"{label}.digest") != digest:
        raise ContinuityCapsuleInputError(f"{label} is not bound to the capsule digest")
    if object_id is not None and ref["object_id"] != object_id:
        raise ContinuityCapsuleInputError(f"{label} changes the capsule object id")
    return ref


def _validate_posture(value: Any, *, label: str) -> dict[str, Any]:
    posture = _require_mapping(value, label=label)
    _require_keys(
        posture,
        {
            "mode",
            "portable_tail_policy",
            "private_tail_digest",
            "private_tail_bytes",
        },
        label=label,
    )
    if posture["mode"] != "verbatim_private_tail":
        raise ContinuityCapsuleInputError(f"{label}.mode is not verbatim")
    if posture["portable_tail_policy"] != "omitted":
        raise ContinuityCapsuleInputError(
            f"{label}.portable_tail_policy is not omitted"
        )
    _require_digest(
        posture["private_tail_digest"], label=f"{label}.private_tail_digest"
    )
    tail_bytes = _require_nonnegative_int(
        posture["private_tail_bytes"], label=f"{label}.private_tail_bytes"
    )
    if tail_bytes > MAX_PROTECTED_TAIL_BYTES:
        raise ContinuityCapsuleInputError(f"{label}.private_tail_bytes is invalid")
    return posture


def _validate_goal(value: Any, *, label: str) -> dict[str, Any]:
    goal = _require_mapping(value, label=label)
    for field in ("goal_id", "title", "source_ref", "content"):
        _require_string(goal.get(field), label=f"{label}.{field}")
    _require_digest(goal.get("digest"), label=f"{label}.digest")
    _canonical_digest(goal)
    return goal


def _validate_watermark(value: Any, *, label: str) -> dict[str, Any]:
    watermark = _require_mapping(value, label=label)
    _require_string(watermark.get("source_ref"), label=f"{label}.source_ref")
    _require_digest(watermark.get("source_digest"), label=f"{label}.source_digest")
    _require_nonnegative_int(watermark.get("generation"), label=f"{label}.generation")
    _require_timestamp(watermark.get("observed_at"), label=f"{label}.observed_at")
    _canonical_digest(watermark)
    return watermark


def _validate_compaction_event(value: Any, *, label: str) -> dict[str, Any]:
    event = _require_mapping(value, label=label)
    for field in ("event_ref", "session_id"):
        _require_string(event.get(field), label=f"{label}.{field}")
    _require_nonnegative_int(event.get("sequence"), label=f"{label}.sequence")
    _require_timestamp(event.get("occurred_at"), label=f"{label}.occurred_at")
    if event.get("kind") != "compaction":
        raise ContinuityCapsuleInputError(f"{label}.kind must be compaction")
    _canonical_digest(event)
    return event


def _validate_content(value: Any, *, label: str) -> dict[str, Any]:
    content = _require_mapping(value, label=label)
    _require_keys(content, set(CONTENT_FIELDS), label=label)
    _require_string(content["capsule_id"], label=f"{label}.capsule_id")
    _validate_goal(content["goal"], label=f"{label}.goal")
    for field in (
        "constraints",
        "completed",
        "current_work",
        "blockers",
        "exact_decisions",
        "open_obligations",
    ):
        _require_string_list(content[field], label=f"{label}.{field}")
    evidence_refs = content["evidence_refs"]
    if not isinstance(evidence_refs, list) or len(evidence_refs) > MAX_EVIDENCE_REFS:
        raise ContinuityCapsuleInputError(f"{label}.evidence_refs is invalid")
    for index, ref in enumerate(evidence_refs):
        mapping = _require_mapping(ref, label=f"{label}.evidence_refs[{index}]")
        if not mapping:
            raise ContinuityCapsuleInputError(
                f"{label}.evidence_refs[{index}] must not be empty"
            )
        _canonical_digest(mapping)
    _require_mapping(
        content["omissions_uncertainty"],
        label=f"{label}.omissions_uncertainty",
    )
    _canonical_digest(content)
    return content


def _validate_capsule(value: Any) -> dict[str, Any]:
    capsule = _require_mapping(value, label="baseline_capsule")
    expected = {
        "schema_version",
        "capsule_id",
        "capsule_ref",
        "capsule_digest",
        *CONTENT_FIELDS,
        "source_watermark",
        "compaction_event",
        "protected_tail_posture",
    }
    _require_keys(capsule, expected, label="baseline_capsule")
    if capsule["schema_version"] != CAPSULE_SCHEMA_VERSION:
        raise ContinuityCapsuleInputError("baseline capsule has the wrong schema")
    capsule_id = _require_string(
        capsule["capsule_id"], label="baseline_capsule.capsule_id"
    )
    digest = _require_digest(
        capsule["capsule_digest"], label="baseline_capsule.capsule_digest"
    )
    _validate_ref(
        capsule["capsule_ref"],
        digest=digest,
        label="baseline_capsule.capsule_ref",
        object_id=f"{CAPSULE_REF_PREFIX}{capsule_id}",
    )
    _validate_content(
        {field: capsule[field] for field in CONTENT_FIELDS},
        label="baseline_capsule.content",
    )
    _validate_watermark(
        capsule["source_watermark"], label="baseline_capsule.source_watermark"
    )
    _validate_compaction_event(
        capsule["compaction_event"], label="baseline_capsule.compaction_event"
    )
    _validate_posture(
        capsule["protected_tail_posture"],
        label="baseline_capsule.protected_tail_posture",
    )
    payload = {
        key: capsule[key]
        for key in capsule
        if key not in {"capsule_ref", "capsule_digest"}
    }
    if _canonical_digest(payload) != digest:
        raise ContinuityCapsuleInputError(
            "baseline capsule digest does not match content"
        )
    return capsule


def _validate_view(
    value: Any,
    *,
    expected_view: str,
    capsule_ref: Mapping[str, Any],
    capsule_digest: str,
) -> dict[str, Any]:
    view = _require_mapping(value, label=f"{expected_view}_view")
    expected = {
        "schema_version",
        "view",
        "capsule_ref",
        "capsule_digest",
        "content",
        "source_watermark",
        "compaction_event",
        "protected_tail_posture",
        "view_digest",
    }
    if expected_view == "private":
        expected.add("protected_tail")
    _require_keys(view, expected, label=f"{expected_view}_view")
    if (
        view["schema_version"] != MATERIALIZATION_SCHEMA_VERSION
        or view["view"] != expected_view
        or view["capsule_digest"] != capsule_digest
    ):
        raise ContinuityCapsuleInputError(
            f"{expected_view}_view changes the capsule identity"
        )
    admitted_ref = _validate_ref(
        view["capsule_ref"],
        digest=capsule_digest,
        label=f"{expected_view}_view.capsule_ref",
        object_id=str(capsule_ref["object_id"]),
    )
    if admitted_ref != dict(capsule_ref):
        raise ContinuityCapsuleInputError(
            f"{expected_view}_view changes the capsule ref"
        )
    _validate_content(view["content"], label=f"{expected_view}_view.content")
    _validate_watermark(
        view["source_watermark"], label=f"{expected_view}_view.source_watermark"
    )
    _validate_compaction_event(
        view["compaction_event"], label=f"{expected_view}_view.compaction_event"
    )
    _validate_posture(
        view["protected_tail_posture"],
        label=f"{expected_view}_view.protected_tail_posture",
    )
    if expected_view == "portable" and "protected_tail" in view:
        raise ContinuityCapsuleInputError("portable_view exposes protected_tail")
    if expected_view == "private":
        if not isinstance(view["protected_tail"], str):
            raise ContinuityCapsuleInputError("private_view.protected_tail is not text")
        posture = view["protected_tail_posture"]
        tail = view["protected_tail"].encode("utf-8")
        if (
            "sha256:" + hashlib.sha256(tail).hexdigest()
            != posture["private_tail_digest"]
            or len(tail) != posture["private_tail_bytes"]
        ):
            raise ContinuityCapsuleInputError(
                "private protected tail does not match posture"
            )
    view_digest = _require_digest(
        view["view_digest"], label=f"{expected_view}_view.view_digest"
    )
    payload = {key: view[key] for key in view if key != "view_digest"}
    if _canonical_digest(payload) != view_digest:
        raise ContinuityCapsuleInputError(
            f"{expected_view}_view digest does not match content"
        )
    return view


def _check(
    checks: list[dict[str, Any]],
    *,
    field: str,
    baseline_present: bool,
    portable_present: bool,
    private_present: bool,
    preserved: bool,
    reason: str,
) -> None:
    checks.append(
        {
            "field": field,
            "baseline_present": baseline_present,
            "portable_present": portable_present,
            "private_present": private_present,
            "preserved": preserved,
            "reason": reason,
        }
    )


def compare_case(case: Mapping[str, Any]) -> dict[str, Any]:
    case_id = str(case.get("case_id", "unknown-case"))
    checks: list[dict[str, Any]] = []
    try:
        baseline = _validate_capsule(case.get("baseline_capsule"))
        digest = str(baseline["capsule_digest"])
        ref = baseline["capsule_ref"]
        portable = _validate_view(
            case.get("portable_view"),
            expected_view="portable",
            capsule_ref=ref,
            capsule_digest=digest,
        )
        private = _validate_view(
            case.get("private_view"),
            expected_view="private",
            capsule_ref=ref,
            capsule_digest=digest,
        )
        for field in CONTENT_FIELDS:
            _check(
                checks,
                field=field,
                baseline_present=field in baseline,
                portable_present=field in portable["content"],
                private_present=field in private["content"],
                preserved=(
                    baseline[field]
                    == portable["content"][field]
                    == private["content"][field]
                ),
                reason="canonical content matches both materializations",
            )
        for field in ("source_watermark", "compaction_event", "protected_tail_posture"):
            _check(
                checks,
                field=field,
                baseline_present=field in baseline,
                portable_present=field in portable,
                private_present=field in private,
                preserved=(baseline[field] == portable[field] == private[field]),
                reason="metadata matches the canonical capsule in both views",
            )
        posture = baseline["protected_tail_posture"]
        _check(
            checks,
            field="portable_tail_policy",
            baseline_present=True,
            portable_present="protected_tail" not in portable,
            private_present=True,
            preserved=(
                posture["portable_tail_policy"] == "omitted"
                and "protected_tail" not in portable
            ),
            reason="portable view omits the protected tail",
        )
        private_tail = private["protected_tail"].encode("utf-8")
        _check(
            checks,
            field="private_tail_digest",
            baseline_present=True,
            portable_present=True,
            private_present=True,
            preserved=(
                "sha256:" + hashlib.sha256(private_tail).hexdigest()
                == posture["private_tail_digest"]
            ),
            reason="private view retains the protected-tail digest",
        )
        _check(
            checks,
            field="private_tail_bytes",
            baseline_present=True,
            portable_present=True,
            private_present=True,
            preserved=len(private_tail) == posture["private_tail_bytes"],
            reason="private view retains the protected-tail byte count",
        )
    except (ContinuityCapsuleInputError, TypeError, KeyError) as exc:
        checks.append(
            {
                "field": "packet_integrity",
                "baseline_present": False,
                "portable_present": False,
                "private_present": False,
                "preserved": False,
                "reason": str(exc),
            }
        )

    passed = sum(1 for check in checks if check["preserved"])
    failed = len(checks) - passed
    if failed == 0 and checks:
        reading = "no material regression"
    elif passed and failed:
        reading = "mixed regression signal"
    else:
        reading = "regression present"
    return {
        "case_id": case_id,
        "baseline_note": "The canonical capsule is the fixed field-preservation baseline.",
        "candidate_note": (
            "The paired portable and private materializations were checked for exact identity, "
            "content, metadata, and protected-tail posture."
        ),
        "comparative_reading": reading,
        "comparison_note": (
            f"{passed} of {len(checks)} required preservation checks passed; "
            "this is a packet-level reading only."
        ),
        "field_checks": checks,
    }


def build_report(payload: Mapping[str, Any]) -> dict[str, Any]:
    packet = _require_mapping(payload, label="input packet")
    _require_keys(
        packet, {"schema_version", "case_family", "cases"}, label="input packet"
    )
    if packet.get("schema_version") != INPUT_SCHEMA_VERSION:
        raise ContinuityCapsuleInputError("input packet has the wrong schema")
    case_family = packet.get("case_family")
    _require_string(case_family, label="case_family")
    cases = packet.get("cases")
    if (
        not isinstance(cases, Sequence)
        or isinstance(cases, (str, bytes, bytearray))
        or not cases
    ):
        raise ContinuityCapsuleInputError("cases must be a non-empty list")
    if len(cases) > MAX_CASES:
        raise ContinuityCapsuleInputError("cases exceeds the supported cardinality")
    normalized_cases: list[Mapping[str, Any]] = []
    seen_ids: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, Mapping):
            raise ContinuityCapsuleInputError(f"cases[{index}] must be an object")
        _require_keys(
            case,
            {"case_id", "baseline_capsule", "portable_view", "private_view"},
            label=f"cases[{index}]",
        )
        case_id = case.get("case_id")
        if not isinstance(case_id, str) or not case_id:
            raise ContinuityCapsuleInputError(f"cases[{index}].case_id is invalid")
        if case_id in seen_ids:
            raise ContinuityCapsuleInputError(f"duplicate case_id: {case_id}")
        seen_ids.add(case_id)
        normalized_cases.append(case)

    comparisons = [compare_case(case) for case in normalized_cases]
    readings = [item["comparative_reading"] for item in comparisons]
    if all(reading == "no material regression" for reading in readings):
        verdict = "no material regression"
    elif all(reading == "regression present" for reading in readings):
        verdict = "regression present"
    else:
        verdict = "mixed regression signal"
    return {
        "eval_name": EVAL_NAME,
        "bundle_status": "draft",
        "object_under_evaluation": (
            "evidence-backed continuity capsule preservation across paired compaction materializations"
        ),
        "comparison_mode": "fixed-baseline",
        "baseline_target": "canonical continuity capsule before compaction",
        "case_family": case_family,
        "preservation_fields": list(PRESERVATION_FIELDS),
        "admission": {
            "case_count": len(comparisons),
            "preserved_case_count": readings.count("no material regression"),
            "mixed_case_count": readings.count("mixed regression signal"),
            "failed_case_count": readings.count("regression present"),
            "real_session_evidence": False,
            "runtime_execution": False,
            "baseline_ready": False,
        },
        "verdict": verdict,
        "claim_boundary": (
            "This draft report reads only field preservation in a supplied capsule packet; it does not prove a real compaction event, runtime reinjection, semantic continuity, or economy improvement."
        ),
        "limitations": [
            "The packet is synthetic or owner-supplied and is not a live session trace.",
            "The runner does not execute session-memory hooks, SDK continuation, or abyss-stack runtime paths.",
            "A positive field reading does not establish baseline admission, promotion, or owner acceptance.",
        ],
        "per_case_comparisons": comparisons,
    }


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContinuityCapsuleInputError(f"cannot read JSON input {path}") from exc
    return _require_mapping(value, label="input packet")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args(argv)
    report = build_report(_load_json(args.input))
    args.output.write_text(
        json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
