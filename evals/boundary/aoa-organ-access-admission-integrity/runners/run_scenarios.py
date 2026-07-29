#!/usr/bin/env python3
"""Validate bounded OS Abyss organ-access proof packets and negative scenarios."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = BUNDLE_ROOT / "schemas" / "organ-access-proof-packet.schema.json"
SCENARIO_ROOT = BUNDLE_ROOT / "fixtures" / "scenarios"

EXPECTED_EVIDENCE_KIND = {
    "declared": "source_declaration",
    "owner_reviewed": "owner_review",
    "packaged": "package_receipt",
    "exported": "export_receipt",
    "deployed": "deploy_receipt",
    "process_alive": "process_observation",
    "endpoint_ready": "endpoint_probe",
    "registry_indexed": "registry_observation",
    "consumer_registered": "consumer_registration",
    "schema_observed": "consumer_schema_observation",
    "call_succeeded": "call_receipt",
    "result_grounded": "owner_grounding_review",
    "freshness_satisfied": "freshness_review",
    "owner_accepted": "owner_acceptance_receipt",
    "cross_organ_proven": "cross_organ_trace",
    "rollback_proven": "rollback_receipt",
}

EXPECTED_REVISION_SLOT = {
    "declared": "source",
    "owner_reviewed": "source",
    "packaged": "package",
    "exported": "package",
    "deployed": "deploy",
    "process_alive": "deploy",
    "endpoint_ready": "deploy",
    "registry_indexed": "deploy",
    "consumer_registered": "consumer_schema",
    "schema_observed": "consumer_schema",
    "call_succeeded": "deploy",
    "result_grounded": "source",
    "freshness_satisfied": "deploy",
    "owner_accepted": "source",
    "cross_organ_proven": "deploy",
    "rollback_proven": "deploy",
}

ASSERTED_FIELDS = {
    "observed_at",
    "evidence_ref",
    "evidence_kind",
    "revision",
}

CLAIM_BOUNDARY = (
    "The report validates a public source packet contract and its negative "
    "inference rules only; it does not prove a live organ, owner acceptance, "
    "control-plane admission, or rollback."
)

LIMITATIONS = [
    "No live MCP process, registry, consumer, or owner result is observed.",
    "Evidence references are structurally checked but are not authenticated by this runner.",
    "A passing result cannot authorize admission, infer acceptance, or raise effect authority.",
]
LIVE_REVIEW_CLAIM_LIMIT = (
    "This central bounded review proves only that the exact packet satisfies "
    "the organ-access source contract and that the checked-in negative "
    "inference scenarios pass at the pinned source revision. It does not "
    "authenticate external evidence, infer owner acceptance, authorize "
    "admission or effects, prove cross-organ benefit, or prove rollback."
)


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return payload


def canonical_digest(value: Any) -> str:
    rendered = json.dumps(
        value,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(rendered).hexdigest()


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def write_private_json(path: Path, value: dict[str, Any]) -> None:
    destination = path.expanduser().absolute()
    destination.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    destination.parent.chmod(0o700)
    if destination.is_symlink():
        raise ValueError(f"{destination}: output cannot be a symlink")
    rendered = (
        json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.",
        dir=destination.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(rendered)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o600)
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    normalized = value
    if len(normalized) > 10 and normalized[10] in {"t", "T"}:
        normalized = normalized[:10] + "T" + normalized[11:]
    if normalized.endswith(("z", "Z")):
        normalized = normalized[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def schema_issues(packet: dict[str, Any]) -> set[str]:
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    issues: set[str] = set()
    for error in validator.iter_errors(packet):
        path = ".".join(str(part) for part in error.absolute_path) or "packet"
        issues.add(f"schema:{path}:{error.validator}")
    return issues


def semantic_issues(packet: dict[str, Any]) -> set[str]:
    issues: set[str] = set()
    window = packet.get("observation_window")
    window_started_at = (
        parse_time(window.get("started_at")) if isinstance(window, dict) else None
    )
    window_ended_at = (
        parse_time(window.get("ended_at")) if isinstance(window, dict) else None
    )
    revisions = packet.get("revisions")
    maturity = packet.get("maturity")
    asserted_axes: set[str] = set()

    if isinstance(maturity, dict):
        for axis, expected_kind in EXPECTED_EVIDENCE_KIND.items():
            evidence = maturity.get(axis)
            if not isinstance(evidence, dict) or evidence.get("state") != "asserted":
                continue
            asserted_axes.add(axis)

            missing = ASSERTED_FIELDS - evidence.keys()
            if missing or not (evidence.get("expires_at") or evidence.get("freshness_policy")):
                issues.add(f"asserted_axis_missing_required_evidence:{axis}")

            actual_kind = evidence.get("evidence_kind")
            if actual_kind != expected_kind:
                issues.add(f"axis_evidence_kind_mismatch:{axis}")
            if axis == "result_grounded" and actual_kind == "endpoint_probe":
                issues.add("endpoint_ready_does_not_imply_result_grounded")
            if axis == "owner_accepted" and actual_kind == "central_eval_result":
                issues.add("central_eval_does_not_imply_owner_accepted")

            revision = evidence.get("revision")
            expected_slot = EXPECTED_REVISION_SLOT[axis]
            expected_revision = (
                revisions.get(expected_slot) if isinstance(revisions, dict) else None
            )
            if isinstance(revision, str) and revision != expected_revision:
                issues.add(f"axis_revision_slot_mismatch:{axis}")

            observed_at = parse_time(evidence.get("observed_at"))
            expires_at = parse_time(evidence.get("expires_at"))
            if (
                observed_at is not None
                and window_started_at is not None
                and observed_at < window_started_at
            ) or (
                observed_at is not None
                and window_ended_at is not None
                and observed_at > window_ended_at
            ):
                issues.add(f"axis_observation_outside_packet_window:{axis}")
            if observed_at is not None and expires_at is not None and expires_at <= observed_at:
                issues.add(f"axis_freshness_window_invalid:{axis}")
            if (
                expires_at is not None
                and window_ended_at is not None
                and expires_at < window_ended_at
            ):
                issues.add(f"axis_evidence_expired_within_observation_window:{axis}")

    result = packet.get("result")
    if isinstance(result, dict):
        if (
            result.get("verdict") == "supports_bounded_contract"
            and not asserted_axes
        ):
            issues.add("positive_verdict_requires_asserted_evidence")
        if result.get("admission_change_authorized") is not False:
            issues.add("admission_change_not_authorized_by_central_proof")
        if result.get("owner_acceptance_inferred") is not False:
            issues.add("owner_acceptance_must_not_be_inferred")
        if result.get("higher_effect_authorized") is not False:
            issues.add("higher_effect_not_authorized_by_lower_plane")
            if packet.get("policy_plane") in {"read", "candidate"}:
                issues.add("read_or_candidate_plane_cannot_authorize_effect")

    if isinstance(window, dict):
        if (
            window_started_at is not None
            and window_ended_at is not None
            and window_ended_at < window_started_at
        ):
            issues.add("observation_window_invalid")

    return issues


def validate_packet(packet: dict[str, Any]) -> list[str]:
    return sorted(schema_issues(packet) | semantic_issues(packet))


def scenario_packet(scenario: dict[str, Any], path: Path) -> dict[str, Any]:
    inline_packet = scenario.get("packet")
    packet_ref = scenario.get("packet_ref")
    if isinstance(inline_packet, dict) and packet_ref is None:
        packet = copy.deepcopy(inline_packet)
    elif isinstance(packet_ref, str) and inline_packet is None:
        ref_path = (BUNDLE_ROOT / packet_ref).resolve()
        if BUNDLE_ROOT not in ref_path.parents:
            raise ValueError(f"{path}: packet_ref escapes the bundle")
        packet = load_json(ref_path)
    else:
        raise ValueError(f"{path}: provide exactly one of packet or packet_ref")

    mutations = scenario.get("mutations", [])
    if not isinstance(mutations, list):
        raise ValueError(f"{path}: mutations must be an array")
    for mutation in mutations:
        if not isinstance(mutation, dict):
            raise ValueError(f"{path}: every mutation must be an object")
        field_path = mutation.get("path")
        action = mutation.get("action")
        if not isinstance(field_path, str) or action not in {"set", "delete"}:
            raise ValueError(f"{path}: mutation requires path and set/delete action")
        parts = field_path.split(".")
        target: Any = packet
        for part in parts[:-1]:
            if not isinstance(target, dict) or part not in target:
                raise ValueError(f"{path}: mutation path not found: {field_path}")
            target = target[part]
        if not isinstance(target, dict):
            raise ValueError(f"{path}: mutation parent is not an object: {field_path}")
        if action == "set":
            if "value" not in mutation:
                raise ValueError(f"{path}: set mutation requires value")
            target[parts[-1]] = copy.deepcopy(mutation["value"])
        elif parts[-1] in target:
            del target[parts[-1]]
        else:
            raise ValueError(f"{path}: delete path not found: {field_path}")
    return packet


def run_scenarios() -> tuple[dict[str, Any], bool]:
    breakdown: list[dict[str, Any]] = []
    for path in sorted(SCENARIO_ROOT.glob("*.json")):
        scenario = load_json(path)
        scenario_id = scenario.get("scenario_id")
        expected = scenario.get("expected")
        expected_codes = scenario.get("expected_codes", [])
        if not isinstance(scenario_id, str):
            raise ValueError(f"{path}: scenario_id must be a string")
        if expected not in {"accept", "reject"}:
            raise ValueError(f"{path}: expected must be accept or reject")
        if not isinstance(expected_codes, list) or not all(
            isinstance(item, str) for item in expected_codes
        ):
            raise ValueError(f"{path}: expected_codes must be a string array")
        packet = scenario_packet(scenario, path)

        observed_codes = validate_packet(packet)
        observed = "accept" if not observed_codes else "reject"
        code_match = set(expected_codes).issubset(observed_codes)
        passed = observed == expected and code_match
        breakdown.append(
            {
                "scenario_id": scenario_id,
                "expected": expected,
                "observed": observed,
                "expected_codes": sorted(expected_codes),
                "observed_codes": observed_codes,
                "outcome": "pass" if passed else "fail",
            }
        )

    passed_count = sum(item["outcome"] == "pass" for item in breakdown)
    failed_count = len(breakdown) - passed_count
    report = {
        "eval_name": "aoa-organ-access-admission-integrity",
        "bundle_status": "bounded",
        "object_under_evaluation": (
            "OS Abyss organ-access proof packet and its admission inferences"
        ),
        "verdict": (
            "supports bounded claim"
            if failed_count == 0
            else "does not support bounded claim"
        ),
        "claim_boundary": CLAIM_BOUNDARY,
        "limitations": LIMITATIONS,
        "scenario_count": len(breakdown),
        "passed_count": passed_count,
        "failed_count": failed_count,
        "per_scenario_breakdown": breakdown,
    }
    return report, failed_count == 0 and bool(breakdown)


def review_packet(
    packet_path: Path,
    *,
    reviewed_at: datetime,
) -> tuple[dict[str, Any], bool]:
    if reviewed_at.tzinfo is None or reviewed_at.utcoffset() is None:
        raise ValueError("reviewed_at must be timezone-aware")
    packet = load_json(packet_path)
    issues = validate_packet(packet)
    suite_report, suite_passed = run_scenarios()
    accepted = not issues
    report = {
        "schema_version": "aoa_organ_access_packet_review_v1",
        "eval_name": "aoa-organ-access-admission-integrity",
        "bundle_status": "bounded",
        "reviewed_at": reviewed_at.astimezone(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
        "packet": {
            "packet_ref": packet_path.expanduser().absolute().as_posix(),
            "packet_digest": canonical_digest(packet),
            "packet_id": packet.get("packet_id"),
            "organ_id": packet.get("organ_id"),
            "capability_id": packet.get("capability_id"),
            "result_verdict": (
                packet.get("result", {}).get("verdict")
                if isinstance(packet.get("result"), dict)
                else None
            ),
        },
        "source_contract": {
            "eval_ref": (
                "evals/boundary/aoa-organ-access-admission-integrity/EVAL.md"
            ),
            "eval_digest": file_digest(BUNDLE_ROOT / "EVAL.md"),
            "manifest_ref": (
                "evals/boundary/aoa-organ-access-admission-integrity/eval.yaml"
            ),
            "manifest_digest": file_digest(BUNDLE_ROOT / "eval.yaml"),
            "packet_schema_ref": (
                "evals/boundary/aoa-organ-access-admission-integrity/"
                "schemas/organ-access-proof-packet.schema.json"
            ),
            "packet_schema_digest": file_digest(SCHEMA_PATH),
        },
        "packet_validation": {
            "accepted_by_source_contract": accepted,
            "issues": issues,
        },
        "negative_suite": {
            "verdict": suite_report["verdict"],
            "scenario_count": suite_report["scenario_count"],
            "passed_count": suite_report["passed_count"],
            "failed_count": suite_report["failed_count"],
            "report_digest": canonical_digest(suite_report),
        },
        "verdict": (
            "supported_bounded"
            if accepted and suite_passed
            else "rejected_contract"
        ),
        "central_proof_asserted": accepted and suite_passed,
        "owner_acceptance_inferred": False,
        "admission_change_authorized": False,
        "higher_effect_authorized": False,
        "cross_organ_benefit_asserted": False,
        "rollback_proven": False,
        "actual_effects": [],
        "limitations": [
            *LIMITATIONS,
            (
                "A source-contract-valid insufficient_evidence packet remains "
                "insufficient evidence; review does not promote its maturity axes."
            ),
            (
                "The report is a private bounded review artifact, not an "
                "owner-acceptance or live-publication receipt."
            ),
        ],
        "claim_limit": LIVE_REVIEW_CLAIM_LIMIT,
    }
    return report, accepted and suite_passed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("run-scenarios", help="run all checked-in scenarios")
    validate = subparsers.add_parser(
        "validate-packet", help="validate one organ-access proof packet"
    )
    validate.add_argument("packet_path", type=Path)
    review = subparsers.add_parser(
        "review-packet",
        help="emit one private bounded packet review after source-suite replay",
    )
    review.add_argument("packet_path", type=Path)
    review.add_argument("--output", type=Path, required=True)
    review.add_argument("--reviewed-at")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "run-scenarios":
        report, passed = run_scenarios()
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if passed else 1

    if args.command == "review-packet":
        reviewed_at = (
            parse_time(args.reviewed_at)
            if args.reviewed_at
            else datetime.now(timezone.utc)
        )
        if reviewed_at is None or reviewed_at.tzinfo is None:
            raise ValueError("--reviewed-at must be an aware RFC 3339 timestamp")
        report, passed = review_packet(
            args.packet_path,
            reviewed_at=reviewed_at,
        )
        write_private_json(args.output, report)
        print(
            json.dumps(
                {
                    "schema_version": report["schema_version"],
                    "eval_name": report["eval_name"],
                    "packet_digest": report["packet"]["packet_digest"],
                    "verdict": report["verdict"],
                    "central_proof_asserted": report[
                        "central_proof_asserted"
                    ],
                    "output": args.output.expanduser().absolute().as_posix(),
                    "claim_limit": report["claim_limit"],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0 if passed else 1

    packet = load_json(args.packet_path)
    issues = validate_packet(packet)
    result = {
        "accepted_by_source_contract": not issues,
        "claim_boundary": CLAIM_BOUNDARY,
        "issues": issues,
        "limitations": LIMITATIONS,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
