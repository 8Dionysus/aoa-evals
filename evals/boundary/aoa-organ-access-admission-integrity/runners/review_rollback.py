#!/usr/bin/env python3
"""Review one exact stack rollback candidate without executing rollback."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import stat
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_SCHEMA = BUNDLE_ROOT / "schemas" / "rollback-readiness-candidate.schema.json"
REVIEW_SCHEMA = BUNDLE_ROOT / "reports" / "rollback-review.schema.json"
RUNNER_PATH = Path(__file__).resolve()
MAX_INPUT_BYTES = 2 * 1024 * 1024
MAX_FUTURE_SKEW = timedelta(seconds=30)
CLAIM_LIMIT = (
    "This bounded review proves only that one exact stack-issued rollback "
    "candidate satisfies the source contract and its checked-in negative "
    "invariants. It does not authenticate the live files by itself, execute "
    "rollback, authorize admission or effects, or prove post-rollback health."
)


class RollbackReviewError(ValueError):
    """A private rollback candidate or review output is unsafe."""


def canonical_digest(value: Any) -> str:
    raw = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _no_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise RollbackReviewError("JSON input contains duplicate object keys")
        result[key] = value
    return result


def read_private_json(path: Path) -> dict[str, Any]:
    absolute = path.expanduser().absolute()
    if absolute.is_symlink() or not absolute.is_file():
        raise RollbackReviewError("candidate must be a regular non-symlink file")
    metadata = absolute.stat()
    if not stat.S_ISREG(metadata.st_mode) or stat.S_IMODE(metadata.st_mode) & 0o077:
        raise RollbackReviewError("candidate must not be group/world accessible")
    if metadata.st_size > MAX_INPUT_BYTES:
        raise RollbackReviewError("candidate exceeds the bounded input size")
    try:
        payload = json.loads(
            absolute.read_text(encoding="utf-8"),
            object_pairs_hook=_no_duplicate_pairs,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RollbackReviewError("candidate is unreadable or invalid JSON") from exc
    if not isinstance(payload, dict):
        raise RollbackReviewError("candidate must be a JSON object")
    return payload


def write_private_json(path: Path, payload: dict[str, Any]) -> None:
    destination = path.expanduser().absolute()
    destination.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    destination.parent.chmod(0o700)
    if destination.is_symlink():
        raise RollbackReviewError("review output cannot be a symlink")
    rendered = (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", dir=destination.parent
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
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed.astimezone(timezone.utc)


def _contains_secret_material(value: Any, key: str = "") -> bool:
    lowered = key.lower()
    if any(marker in lowered for marker in ("token", "password", "secret_value", "private_key")):
        return True
    if isinstance(value, dict):
        return any(_contains_secret_material(item, str(name)) for name, item in value.items())
    if isinstance(value, list):
        return any(_contains_secret_material(item, key) for item in value)
    if isinstance(value, str):
        return "-----BEGIN PRIVATE KEY-----" in value or "bearer " in value.lower()
    return False


def validate_candidate(
    candidate: dict[str, Any], *, reviewed_at: datetime
) -> list[str]:
    issues: set[str] = set()
    schema = json.loads(CANDIDATE_SCHEMA.read_text(encoding="utf-8"))
    for error in Draft202012Validator(
        schema, format_checker=FormatChecker()
    ).iter_errors(candidate):
        path = ".".join(str(item) for item in error.absolute_path) or "candidate"
        issues.add(f"schema:{path}:{error.validator}")
    unsigned = dict(candidate)
    claimed = unsigned.pop("candidate_id", None)
    if claimed != canonical_digest(unsigned):
        issues.add("candidate_content_address_mismatch")
    if _contains_secret_material(candidate):
        issues.add("secret_material_present")
    generated_at = parse_time(candidate.get("generated_at"))
    expires_at = parse_time(candidate.get("expires_at"))
    observation = candidate.get("observation")
    observation_generated = (
        parse_time(observation.get("generated_at")) if isinstance(observation, dict) else None
    )
    observation_expires = (
        parse_time(observation.get("expires_at")) if isinstance(observation, dict) else None
    )
    if (
        generated_at is None
        or expires_at is None
        or expires_at <= generated_at
        or generated_at > reviewed_at + MAX_FUTURE_SKEW
        or expires_at <= reviewed_at
    ):
        issues.add("candidate_window_invalid")
    if (
        observation_generated is None
        or observation_expires is None
        or (generated_at is not None and observation_generated > generated_at)
        or (expires_at is not None and observation_expires < expires_at)
    ):
        issues.add("observation_window_does_not_cover_candidate")
    source = candidate.get("source_package")
    target = candidate.get("last_known_good")
    if isinstance(source, dict) and isinstance(target, dict):
        if not (
            source.get("source_tree_digest")
            == source.get("deployed_tree_digest")
            == target.get("package_digest")
            == target.get("deploy_tree_digest")
        ):
            issues.add("source_package_identity_mismatch")
        manifest_digest = target.get("deploy_manifest_digest")
        expected_ref = (
            "Logs/mcp/deployments/records/"
            + str(manifest_digest).removeprefix("sha256:")
            + ".json"
        )
        if target.get("deploy_manifest_ref") != expected_ref:
            issues.add("manifest_ref_identity_mismatch")
        if not str(target.get("canary_route") or "").endswith("/last-known-good"):
            issues.add("lkg_canary_not_distinct")
        if "/rollback-canaries/records/" not in str(target.get("canary_ref") or ""):
            issues.add("lkg_canary_receipt_lane_invalid")
    checks = candidate.get("checks")
    if isinstance(checks, dict) and checks.get("runtime_effect_executed") is not False:
        issues.add("runtime_effect_not_permitted")
    for field in (
        "execution_authorized",
        "admission_authorized",
        "rollback_executed",
        "contains_secrets",
    ):
        if candidate.get(field) is not False:
            issues.add(f"authority_ceiling_exceeded:{field}")
    return sorted(issues)


def _fixture_candidate() -> dict[str, Any]:
    generated = datetime(2026, 8, 1, 0, 0, tzinfo=timezone.utc)
    digest_a = "sha256:" + "a" * 64
    digest_b = "sha256:" + "b" * 64
    body: dict[str, Any] = {
        "schema_version": "abyss_stack_mcp_rollback_candidate_v1",
        "issuer": "abyss-stack",
        "organ_id": "aoa-kag",
        "policy_family": "read",
        "generated_at": generated.isoformat().replace("+00:00", "Z"),
        "expires_at": (generated + timedelta(minutes=5)).isoformat().replace("+00:00", "Z"),
        "rollback_route": "runbook://mcp-rollback/aoa-kag/read",
        "observation": {
            "observation_ref": "/private/observation.json",
            "observation_digest": digest_b,
            "generated_at": (generated - timedelta(seconds=1)).isoformat().replace("+00:00", "Z"),
            "expires_at": (generated + timedelta(minutes=5)).isoformat().replace("+00:00", "Z"),
        },
        "registry": {"registry_id": "private-shadow", "registry_digest": digest_b, "registry_state": "shadow"},
        "source_package": {
            "source_root_owner": "abyss-stack", "source_revision": "1" * 40,
            "source_tree_digest": digest_a, "deployed_tree_digest": digest_a,
            "file_count": 5, "byte_count": 100
        },
        "last_known_good": {
            "consumer_registration_ref": "consumer-registration://codex/aoa-kag/example",
            "package_digest": digest_a, "deploy_revision": "1" * 40,
            "deploy_tree_digest": digest_a,
            "deploy_manifest_ref": "Logs/mcp/deployments/records/" + "b" * 64 + ".json",
            "deploy_manifest_digest": digest_b,
            "unit_name": "aoa-organ-mcp-read@aoa-kag.service",
            "credential_class": "kag-read",
            "executable_ref": "/private/bin/aoa-kag-mcp-server.py",
            "process_identity": "systemd-user:aoa-organ-mcp-read@aoa-kag.service:executable:sha256:" + "c" * 64,
            "canary_route": "runbook://mcp-canary/aoa-kag/read/last-known-good",
            "canary_ref": "/private/rollback-canaries/records/aoa-kag/example.json"
        },
        "checks": {
            "immutable_manifest_verified": True, "source_commit_available": True,
            "source_package_reproduced": True, "deployed_package_exact": True,
            "unit_and_executable_exact": True, "credential_present_without_read": True,
            "consumer_registration_exact": True, "lkg_canary_distinct_and_grounded": True,
            "runtime_effect_executed": False
        },
        "execution_authorized": False, "admission_authorized": False,
        "rollback_executed": False, "contains_secrets": False,
        "claim_limits": [
            "This fictional packet names one bounded last-known-good contour only.",
            "It carries no credential bytes and authorizes no runtime operation.",
            "It does not authorize admission, process restart, or consumer mutation.",
            "A live stack projector must independently revalidate every exact input."
        ]
    }
    body["candidate_id"] = canonical_digest(body)
    return body


def _resign(candidate: dict[str, Any]) -> None:
    body = dict(candidate)
    body.pop("candidate_id", None)
    candidate["candidate_id"] = canonical_digest(body)


def run_negative_suite() -> tuple[dict[str, Any], bool]:
    reviewed_at = datetime(2026, 8, 1, 0, 1, tzinfo=timezone.utc)
    scenarios: list[tuple[str, dict[str, Any], bool, str | None]] = []
    valid = _fixture_candidate()
    scenarios.append(("valid-bounded-candidate", valid, True, None))
    mutations = [
        ("runtime-effect", ("checks", "runtime_effect_executed"), True, "runtime_effect_not_permitted"),
        ("admission-authorized", ("admission_authorized",), True, "authority_ceiling_exceeded:admission_authorized"),
        ("source-drift", ("source_package", "source_tree_digest"), "sha256:" + "d" * 64, "source_package_identity_mismatch"),
        ("manifest-ref-drift", ("last_known_good", "deploy_manifest_ref"), "Logs/mcp/deployments/records/" + "e" * 64 + ".json", "manifest_ref_identity_mismatch"),
        ("current-canary", ("last_known_good", "canary_route"), "runbook://mcp-canary/aoa-kag/read", "lkg_canary_not_distinct"),
        ("expired", ("expires_at",), "2026-08-01T00:00:00Z", "candidate_window_invalid"),
        ("observation-too-short", ("observation", "expires_at"), "2026-08-01T00:02:00Z", "observation_window_does_not_cover_candidate"),
        ("registry-unadmitted-state", ("registry", "registry_state"), "candidate", "schema:registry.registry_state:enum"),
        ("pid-process-target", ("last_known_good", "process_identity"), "systemd-user:unit:pid:1", "schema:last_known_good.process_identity:pattern"),
    ]
    for scenario_id, path, value, expected_code in mutations:
        candidate = copy.deepcopy(valid)
        target: Any = candidate
        for part in path[:-1]:
            target = target[part]
        target[path[-1]] = value
        _resign(candidate)
        scenarios.append((scenario_id, candidate, False, expected_code))
    wrong_id = copy.deepcopy(valid)
    wrong_id["candidate_id"] = "sha256:" + "0" * 64
    scenarios.append(("content-address-drift", wrong_id, False, "candidate_content_address_mismatch"))
    breakdown: list[dict[str, Any]] = []
    for scenario_id, candidate, expected_accept, expected_code in scenarios:
        issues = validate_candidate(candidate, reviewed_at=reviewed_at)
        accepted = not issues
        passed = accepted is expected_accept and (
            expected_code is None or expected_code in issues
        )
        breakdown.append(
            {
                "scenario_id": scenario_id,
                "expected": "accept" if expected_accept else "reject",
                "observed": "accept" if accepted else "reject",
                "expected_code": expected_code,
                "observed_codes": issues,
                "outcome": "pass" if passed else "fail",
            }
        )
    failed = sum(item["outcome"] == "fail" for item in breakdown)
    report = {
        "verdict": "supports bounded claim" if failed == 0 else "does not support bounded claim",
        "scenario_count": len(breakdown),
        "passed_count": len(breakdown) - failed,
        "failed_count": failed,
        "breakdown": breakdown,
    }
    return report, failed == 0


def review_candidate(
    candidate_path: Path, *, reviewed_at: datetime
) -> tuple[dict[str, Any], bool]:
    if reviewed_at.tzinfo is None or reviewed_at.utcoffset() is None:
        raise RollbackReviewError("reviewed_at must be timezone-aware")
    reviewed_at = reviewed_at.astimezone(timezone.utc)
    candidate = read_private_json(candidate_path)
    issues = validate_candidate(candidate, reviewed_at=reviewed_at)
    suite, suite_passed = run_negative_suite()
    accepted = not issues and suite_passed
    refs = {
        "eval_ref": "evals/boundary/aoa-organ-access-admission-integrity/EVAL.md",
        "manifest_ref": "evals/boundary/aoa-organ-access-admission-integrity/eval.yaml",
        "candidate_schema_ref": "evals/boundary/aoa-organ-access-admission-integrity/schemas/rollback-readiness-candidate.schema.json",
        "review_schema_ref": "evals/boundary/aoa-organ-access-admission-integrity/reports/rollback-review.schema.json",
        "runner_ref": "evals/boundary/aoa-organ-access-admission-integrity/runners/review_rollback.py",
    }
    report = {
        "schema_version": "aoa_organ_access_rollback_review_v1",
        "eval_name": "aoa-organ-access-admission-integrity",
        "bundle_status": "bounded",
        "reviewed_at": reviewed_at.isoformat().replace("+00:00", "Z"),
        "candidate": {
            "candidate_ref": candidate_path.expanduser().absolute().as_posix(),
            "candidate_digest": canonical_digest(candidate),
            "candidate_id": candidate.get("candidate_id"),
            "organ_id": candidate.get("organ_id"),
            "policy_family": candidate.get("policy_family"),
        },
        "source_contract": {
            **refs,
            "eval_digest": file_digest(BUNDLE_ROOT / "EVAL.md"),
            "manifest_digest": file_digest(BUNDLE_ROOT / "eval.yaml"),
            "candidate_schema_digest": file_digest(CANDIDATE_SCHEMA),
            "review_schema_digest": file_digest(REVIEW_SCHEMA),
            "runner_digest": file_digest(RUNNER_PATH),
        },
        "candidate_validation": {
            "accepted_by_source_contract": not issues,
            "issues": issues,
        },
        "negative_suite": {
            "verdict": suite["verdict"],
            "scenario_count": suite["scenario_count"],
            "passed_count": suite["passed_count"],
            "failed_count": suite["failed_count"],
            "report_digest": canonical_digest(suite),
        },
        "verdict": "supported_bounded" if accepted else "rejected_contract",
        "rollback_candidate_supported": accepted,
        "rollback_executed": False,
        "admission_change_authorized": False,
        "higher_effect_authorized": False,
        "actual_effects": [],
        "limitations": [
            "The runner validates the exact candidate contract but does not authenticate live stack files by itself.",
            "A stack projector must rebind the review to the unchanged observation, deployment record, consumer, and LKG canary.",
            "Readiness is not rollback execution and does not prove health after a future restoration.",
            "The review cannot authorize admission, process lifecycle effects, consumer mutation, or credential access."
        ],
        "claim_limit": CLAIM_LIMIT,
    }
    schema = json.loads(REVIEW_SCHEMA.read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(report))
    if errors:
        raise RollbackReviewError("produced rollback review failed its schema")
    return report, accepted


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("run-scenarios")
    review = subparsers.add_parser("review-candidate")
    review.add_argument("candidate_path", type=Path)
    review.add_argument("--output", type=Path, required=True)
    review.add_argument("--reviewed-at")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "run-scenarios":
        report, passed = run_negative_suite()
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if passed else 1
    reviewed_at = parse_time(args.reviewed_at) if args.reviewed_at else datetime.now(timezone.utc)
    if reviewed_at is None:
        raise RollbackReviewError("--reviewed-at must be an aware RFC 3339 timestamp")
    report, passed = review_candidate(args.candidate_path, reviewed_at=reviewed_at)
    write_private_json(args.output, report)
    print(json.dumps({
        "schema_version": report["schema_version"],
        "eval_name": report["eval_name"],
        "candidate_digest": report["candidate"]["candidate_digest"],
        "verdict": report["verdict"],
        "rollback_candidate_supported": report["rollback_candidate_supported"],
        "rollback_executed": False,
        "admission_change_authorized": False,
        "output": args.output.expanduser().absolute().as_posix(),
        "claim_limit": report["claim_limit"],
    }, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
