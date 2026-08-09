from __future__ import annotations

import base64
import json
import hashlib
import stat
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError


REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_ROOT = REPO_ROOT / "evals" / "boundary" / "aoa-organ-access-admission-integrity"
RUNNER = BUNDLE_ROOT / "runners" / "run_scenarios.py"
MATERIALIZER = BUNDLE_ROOT / "runners" / "materialize_live_packet.py"


def run_runner(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(RUNNER), *args],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def canonical_digest(value: object) -> str:
    raw = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def sdk_canonical_digest(value: object) -> str:
    raw = json.dumps(
        value,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def write_json(path: Path, payload: object, *, mode: int = 0o640) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    path.chmod(mode)
    return path


def live_packet_inputs(tmp_path: Path) -> dict[str, Path]:
    source_revision = "0ff913279868735b41a17aab84c0c89341d7cb77"
    package_digest = "sha256:" + ("a" * 64)
    deploy_tree_digest = package_digest
    schema_digest = "sha256:" + ("c" * 64)
    registry = {
        "schema_version": "aoa_organ_registry_source_v1",
        "registry_id": "os-abyss-wave1-test",
        "workspace_owner": "os-abyss",
        "authored_at": "2026-07-28T14:59:00Z",
        "expires_at": "2026-07-29T00:00:00Z",
        "contains_secrets": False,
        "default_admission": "deny",
        "owner_decision_refs": [],
        "records": [
            {
                "organ_id": "aoa-kag",
                "registry_state": "shadow",
                "owners": {
                    "source_owner": "aoa-kag",
                    "access_owner": "aoa-kag",
                    "control_owner": "aoa-sdk",
                    "runtime_owner": "abyss-stack",
                    "proof_owner": "aoa-evals",
                    "acceptance_owner": "aoa-kag",
                },
                "revisions": {
                    "source": {
                        "revision": source_revision,
                        "digest": None,
                        "schema_digest": None,
                    }
                },
                "maturity": {
                    "declared": {
                        "state": "asserted",
                        "freshness_policy": "wave1-test-declaration-v1",
                        "evidence": {
                            "owner": "aoa-kag",
                            "evidence_ref": ("owner://aoa-kag/decision/AOA-KAG-D-0015"),
                            "revision": source_revision,
                            "observed_at": "2026-07-28T14:59:00Z",
                            "expires_at": "2026-07-29T00:00:00Z",
                        },
                    }
                },
                "capabilities": [
                    {
                        "capability_id": "knowledge-retrieval",
                        "summary": (
                            "Owner-qualified knowledge retrieval with "
                            "source-preserving handoff."
                        ),
                        "policy_family": "read",
                        "credential_class": "kag-read",
                        "task_intent_terms": [
                            "knowledge",
                            "provenance",
                            "relations",
                        ],
                        "owner_payload_schema_ref": ("owner://aoa-kag/schema/payload"),
                        "eval_refs": ["eval://aoa-organ-access-admission-integrity"],
                        "primitives": [
                            {
                                "primitive_id": "retrieve-knowledge",
                                "kind": "tool",
                                "effect_class": "observe",
                                "policy_family": "read",
                                "input_schema_ref": ("owner://aoa-kag/schema/input"),
                                "output_schema_ref": ("owner://aoa-kag/schema/output"),
                                "approval_required": False,
                                "approval_owner": None,
                                "idempotency": "read_only",
                                "rollback_route": None,
                                "maximum_blast_radius": ("read-only owner response"),
                                "annotations_are_security_enforcement": False,
                            }
                        ],
                    }
                ],
            }
        ],
    }
    registry_path = write_json(
        tmp_path / "registry.json",
        registry,
        mode=0o600,
    )

    deployment_body = {
        "schema_version": "abyss_stack_mcp_deployment_manifest_v1",
        "digest_scope": "abyss_stack_mcp_deployment_body_v1",
        "provider": "abyss-stack",
        "deployed_at": "2026-07-28T15:01:00Z",
        "contains_secrets": False,
        "source": {
            "owner": "abyss-stack",
            "revision": "8bcfe0edf7ad499d666207ca2087d8db9df4d7a9",
            "path": "mcp/services",
            "tree_digest": package_digest,
        },
        "deployment": {
            "runtime_owner": "abyss-stack",
            "path": "Configs/mcp/services",
            "sync_delete_mode": False,
            "tree_digest": deploy_tree_digest,
        },
        "services": [
            {
                "service_id": "aoa-kag-mcp",
                "package_name": "aoa-kag-mcp",
                "package_version": "0.1.0",
                "package_source_revision": ("8bcfe0edf7ad499d666207ca2087d8db9df4d7a9"),
                "package_artifact_kind": "source_projection",
                "package_digest": package_digest,
                "source_tree": {"tree_digest": package_digest},
                "deployed_tree": {"tree_digest": deploy_tree_digest},
                "parity_state": "exact",
            }
        ],
        "parity_state": "exact",
        "runtime_observation_state": "not_observed",
        "claim_limit": "Fixture deployment receipt has a bounded claim only.",
    }
    manifest_id = canonical_digest(deployment_body)
    record_name = manifest_id.removeprefix("sha256:") + ".json"
    deployment = {
        **deployment_body,
        "manifest_id": manifest_id,
        "record_ref": f"Logs/mcp/deployments/records/{record_name}",
        "latest_ref": "Logs/mcp/deployments/latest.json",
    }
    deployment_path = write_json(
        tmp_path / "deployments" / "latest.json",
        deployment,
    )
    write_json(
        tmp_path / "deployments" / "records" / record_name,
        deployment,
    )

    observation = {
        "schema_version": "abyss_stack_runtime_observation_v1",
        "provider": "abyss-stack",
        "provider_watermark": "fixture-wave1",
        "generated_at": "2026-07-28T15:02:00Z",
        "expires_at": "2026-07-28T15:10:00Z",
        "contains_secrets": False,
        "subjects": [
            {
                "organ_id": "aoa-kag",
                "policy_family": "read",
                "owners": {
                    "source_owner": "aoa-kag",
                    "access_owner": "aoa-kag",
                    "runtime_owner": "abyss-stack",
                    "proof_owner": "aoa-evals",
                    "acceptance_owner": "aoa-kag",
                },
                "source": {"revision": source_revision},
                "package": {
                    "name": "aoa-kag-mcp",
                    "version": "0.1.0",
                    "source_revision": ("8bcfe0edf7ad499d666207ca2087d8db9df4d7a9"),
                    "artifact_digest": package_digest,
                    "expected_deploy_tree_digest": deploy_tree_digest,
                },
                "deploy": {
                    "revision": ("8bcfe0edf7ad499d666207ca2087d8db9df4d7a9"),
                    "manifest_ref": deployment["record_ref"],
                    "manifest_digest": manifest_id,
                    "tree_digest": deploy_tree_digest,
                },
                "process": {
                    "unit_name": "aoa-organ-mcp-read@aoa-kag.service",
                    "executable_ref": ("/srv/AbyssOS/.codex/bin/aoa-kag-mcp-server.py"),
                    "process_identity": "systemd:aoa-kag:321",
                    "active": True,
                    "evidence": {
                        "state": "exact",
                        "observed_at": "2026-07-28T15:02:00Z",
                        "expires_at": "2026-07-28T15:10:00Z",
                        "evidence_refs": [
                            {
                                "owner": "abyss-stack",
                                "evidence_ref": (
                                    "systemd://user/"
                                    "aoa-organ-mcp-read@aoa-kag.service:321"
                                ),
                                "revision": (
                                    "8bcfe0edf7ad499d666207ca2087d8db9df4d7a9"
                                ),
                                "observed_at": "2026-07-28T15:02:00Z",
                                "expires_at": "2026-07-28T15:10:00Z",
                            }
                        ],
                        "reason_codes": [],
                    },
                },
                "registry": {
                    "registry_id": "os-abyss-wave1-test",
                    "registry_digest": canonical_digest(registry["records"][0]),
                    "registry_state": "shadow",
                },
            }
        ],
    }
    observation_path = tmp_path / "observation.json"

    owner_payload = {
        "schema_version": "aoa-kag-mcp-capabilities-v1",
        "owners": [
            {
                "repo": "aoa-kag",
                "manifest_uri": "aoa-kag://owners/aoa-kag/manifest",
            }
        ],
        "projection": {
            "distribution": {"state": "active"},
            "digest": "f" * 64,
            "updated_at": "2026-07-28T15:02:30Z",
        },
        "resource_templates": ["aoa-kag://owners/{repo}/manifest"],
    }
    result_digest = canonical_digest(owner_payload)
    result_artifact_ref = (
        "results/aoa-kag/" + result_digest.removeprefix("sha256:") + ".json"
    )
    canary_body = {
        "schema_version": "abyss_stack_mcp_canary_receipt_v1",
        "issuer": "abyss-stack",
        "consumer_id": "abyss-stack-mcp-canary",
        "organ_id": "aoa-kag",
        "policy_family": "read",
        "service_id": "aoa-kag-mcp",
        "endpoint_ref": "http://127.0.0.1:5425/mcp",
        "canary_route": "runbook://mcp-canary/aoa-kag/read",
        "tool_name": "kag_discover",
        "tool_arguments_digest": "sha256:" + ("d" * 64),
        "observed_at": "2026-07-28T15:03:00Z",
        "expires_at": "2026-07-28T15:10:00Z",
        "protocol_version": "2025-11-25",
        "server_name": "aoa-kag-mcp",
        "server_version": "0.1.0",
        "server_schema_digest": schema_digest,
        "selected_tool_schema_digest": "sha256:" + ("e" * 64),
        "inventory_counts": {
            "tools": 5,
            "resources": 1,
            "resource_templates": 8,
            "prompts": 0,
        },
        "call_succeeded": True,
        "result_contract_matched": True,
        "result_schema_identity": "aoa-kag-mcp-capabilities-v1",
        "result_digest": result_digest,
        "result_artifact_ref": result_artifact_ref,
        "call_latency_ms": 12,
        "total_latency_ms": 28,
        "reason_codes": [],
        "contains_secrets": False,
        "content_trust": "untrusted_data",
        "instruction_authority": "none",
        "claim_limit": (
            "This stack-issued receipt proves one authenticated loopback MCP "
            "schema observation and bounded read canary only. It does not prove "
            "owner grounding, owner freshness, owner acceptance, central proof, "
            "admission, or rollback."
        ),
    }
    canary = {
        "receipt_id": canonical_digest(canary_body),
        **canary_body,
    }
    canary_root = tmp_path / "private-canary"
    canary_path = write_json(
        canary_root
        / "records"
        / "aoa-kag"
        / (canary["receipt_id"].removeprefix("sha256:") + ".json"),
        canary,
        mode=0o600,
    )
    result_artifact_body = {
        "schema_version": "abyss_stack_mcp_canary_result_artifact_v1",
        "issuer": "abyss-stack",
        "organ_id": canary["organ_id"],
        "policy_family": "read",
        "service_id": canary["service_id"],
        "canary_route": canary["canary_route"],
        "tool_name": canary["tool_name"],
        "tool_arguments_digest": canary["tool_arguments_digest"],
        "observed_at": canary["observed_at"],
        "result_schema_identity": canary["result_schema_identity"],
        "result_digest": result_digest,
        "owner_payload": owner_payload,
        "contains_secrets": False,
        "content_trust": "untrusted_data",
        "instruction_authority": "none",
        "claim_limit": (
            "This private artifact preserves one bounded MCP canary result for "
            "independent owner review. Stack capture and content addressing do "
            "not prove owner grounding, freshness, acceptance, central proof, "
            "admission, or rollback."
        ),
    }
    result_artifact = {
        "artifact_id": canonical_digest(result_artifact_body),
        **result_artifact_body,
    }
    result_path = write_json(
        canary_root / result_artifact_ref,
        result_artifact,
        mode=0o600,
    )
    owner_schema_digest = "sha256:" + ("f" * 64)
    review_body = {
        "schema_version": "aoa_organ_owner_result_review_v1",
        "review_owner": "aoa-kag",
        "organ_id": "aoa-kag",
        "capability_id": "knowledge-retrieval",
        "primitive_id": "retrieve-knowledge",
        "owners": registry["records"][0]["owners"],
        "capture": {
            "capture_owner": "abyss-stack",
            "capture_receipt_ref": canary_path.relative_to(canary_root).as_posix(),
            "capture_receipt_id": canary["receipt_id"],
            "result_artifact_ref": result_path.relative_to(canary_root).as_posix(),
            "result_artifact_id": result_artifact["artifact_id"],
            "organ_id": "aoa-kag",
            "capability_id": "knowledge-retrieval",
            "primitive_id": "retrieve-knowledge",
            "result_digest": result_digest,
            "result_schema_identity": canary["result_schema_identity"],
            "server_schema_digest": canary["server_schema_digest"],
            "primitive_schema_digest": canary["selected_tool_schema_digest"],
            "observed_at": "2026-07-28T15:03:00+00:00",
            "expires_at": "2026-07-28T15:10:00+00:00",
        },
        "source_revision": {
            "revision": source_revision,
            "schema_digest": owner_schema_digest,
        },
        "owner_payload_schema_ref": "owner://aoa-kag/schema/payload",
        "owner_payload_schema_digest": owner_schema_digest,
        "reviewed_at": "2026-07-28T15:03:30+00:00",
        "expires_at": "2026-07-28T15:08:30+00:00",
        "grounding_state": "grounded",
        "freshness_state": "exact",
        "freshness_policy": {
            "policy_id": "kag-owner-source-parity-v1",
            "max_age_seconds": 300,
            "stale_readable_seconds": 0,
            "cache_scope": "task",
            "provider_watermark_required": True,
        },
        "provider_watermark": "aoa-kag-source-index:fixture",
        "grounding_evidence": [
            {
                "owner": "aoa-kag",
                "evidence_ref": "schemas/kag-mcp-capabilities.schema.json",
                "revision": source_revision,
                "observed_at": "2026-07-28T15:03:30+00:00",
                "expires_at": "2026-07-28T15:08:30+00:00",
            }
        ],
        "reason_codes": [],
        "owner_accepted": False,
        "central_proof_asserted": False,
        "admission_asserted": False,
        "cross_organ_proven": False,
        "rollback_proven": False,
        "contains_secrets": False,
        "self_report_is_security_authority": False,
        "claim_limit": (
            "This owner-issued review proves only the named owner's schema "
            "grounding and freshness assessment for one content-addressed "
            "captured result. It does not prove owner acceptance, central "
            "proof, admission, cross-organ benefit, execution authorization, "
            "or rollback."
        ),
    }
    owner_review = {
        **review_body,
        "review_id": sdk_canonical_digest(review_body),
    }
    owner_review_path = write_json(
        canary_root
        / "reviews"
        / "aoa-kag"
        / (owner_review["review_id"].removeprefix("sha256:") + ".json"),
        owner_review,
        mode=0o600,
    )
    canary_evidence_ref = {
        "owner": "abyss-stack",
        "evidence_ref": canary_path.absolute().as_posix(),
        "revision": canary["receipt_id"],
        "observed_at": canary["observed_at"],
        "expires_at": canary["expires_at"],
    }
    observation["subjects"][0]["endpoint"] = {
        "transport": "streamable-http",
        "endpoint_ref": canary["endpoint_ref"],
        "protocol_versions": [canary["protocol_version"]],
        "ready": True,
        "server_schema_digest": canary["server_schema_digest"],
        "evidence": {
            "state": "exact",
            "observed_at": canary["observed_at"],
            "expires_at": canary["expires_at"],
            "evidence_refs": [canary_evidence_ref],
            "reason_codes": [],
        },
    }
    observation["subjects"][0]["canary"] = {
        "succeeded": False,
        "result_grounded": False,
        "canary_route": canary["canary_route"],
        "canary_ref": None,
        "evidence": {
            "state": "blocked",
            "observed_at": canary["observed_at"],
            "expires_at": canary["expires_at"],
            "evidence_refs": [canary_evidence_ref],
            "reason_codes": ["owner-grounding-review-required"],
        },
    }
    write_json(observation_path, observation, mode=0o600)
    output_root = tmp_path / "private-output"
    output_root.mkdir(mode=0o700)
    return {
        "registry": registry_path,
        "deployment": deployment_path,
        "observation": observation_path,
        "canary": canary_path,
        "result": result_path,
        "owner_review": owner_review_path,
        "output": output_root / "packet.json",
    }


def run_materializer(
    paths: dict[str, Path],
    *,
    include_owner_review: bool = False,
) -> subprocess.CompletedProcess[str]:
    command = [
        sys.executable,
        str(MATERIALIZER),
        "--organ",
        "aoa-kag",
        "--registry",
        str(paths["registry"]),
        "--deployment",
        str(paths["deployment"]),
        "--observation",
        str(paths["observation"]),
        "--canary",
        str(paths["canary"]),
        "--result",
        str(paths["result"]),
    ]
    if include_owner_review:
        command.extend(["--owner-review", str(paths["owner_review"])])
    command.extend(
        [
            "--output",
            str(paths["output"]),
            "--materialized-at",
            "2026-07-28T15:04:00Z",
        ]
    )
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def upgrade_canary_inputs_to_v2(paths: dict[str, Path]) -> None:
    canary_path = paths["canary"]
    canary = json.loads(canary_path.read_text(encoding="utf-8"))
    old_receipt_id = canary["receipt_id"]
    signer_id = "sha256:" + ("1" * 64)
    attestation = base64.urlsafe_b64encode(b"a" * 64).rstrip(b"=").decode("ascii")
    canary.update(
        {
            "schema_version": "abyss_stack_mcp_canary_receipt_v2",
            "signer_id": signer_id,
            "attestation_algorithm": "ed25519",
            "attestation": attestation,
        }
    )
    unsigned_canary = {
        key: value
        for key, value in canary.items()
        if key not in {"receipt_id", "attestation"}
    }
    canary["receipt_id"] = canonical_digest(unsigned_canary)
    new_canary_path = (
        canary_path.parent
        / f"{canary['receipt_id'].removeprefix('sha256:')}.json"
    )
    write_json(new_canary_path, canary, mode=0o600)
    canary_path.unlink()
    paths["canary"] = new_canary_path

    result_path = paths["result"]
    result = json.loads(result_path.read_text(encoding="utf-8"))
    result.update(
        {
            "schema_version": "abyss_stack_mcp_canary_result_artifact_v2",
            "signer_id": signer_id,
            "attestation_algorithm": "ed25519",
            "attestation": attestation,
        }
    )
    unsigned_result = {
        key: value
        for key, value in result.items()
        if key not in {"artifact_id", "attestation"}
    }
    result["artifact_id"] = canonical_digest(unsigned_result)
    write_json(result_path, result, mode=0o600)

    observation_path = paths["observation"]
    observation = json.loads(observation_path.read_text(encoding="utf-8"))
    subject = observation["subjects"][0]
    for section in ("endpoint", "canary"):
        evidence = subject[section]["evidence"]["evidence_refs"][0]
        evidence["evidence_ref"] = new_canary_path.absolute().as_posix()
        evidence["revision"] = canary["receipt_id"]
    write_json(observation_path, observation, mode=0o600)

    assert old_receipt_id != canary["receipt_id"]


def upgrade_canary_inputs_to_v3(paths: dict[str, Path]) -> None:
    upgrade_canary_inputs_to_v2(paths)
    canary_path = paths["canary"]
    canary = json.loads(canary_path.read_text(encoding="utf-8"))
    old_receipt_id = canary["receipt_id"]
    deployment = json.loads(paths["deployment"].read_text(encoding="utf-8"))
    service = deployment["services"][0]
    canary.update(
        {
            "schema_version": "abyss_stack_mcp_canary_receipt_v3",
            "claim_limit": (
                "This stack-issued receipt proves one authenticated loopback MCP "
                "schema observation, bounded read canary, and exact named-systemd "
                "process identity unchanged across the probe only. It does not prove "
                "owner grounding, owner freshness, owner acceptance, central proof, "
                "admission, or rollback."
            ),
            "deployment_manifest_id": deployment["manifest_id"],
            "deployment_service_id": service["service_id"],
            "deployment_source_revision": service["package_source_revision"],
            "deployment_package_digest": service["package_digest"],
            "deployment_tree_digest": service["deployed_tree"]["tree_digest"],
            "deployment_deployed_at": deployment["deployed_at"],
        }
    )
    unsigned_canary = {
        key: value
        for key, value in canary.items()
        if key not in {"receipt_id", "attestation"}
    }
    canary["receipt_id"] = canonical_digest(unsigned_canary)
    new_canary_path = (
        canary_path.parent
        / f"{canary['receipt_id'].removeprefix('sha256:')}.json"
    )
    write_json(new_canary_path, canary, mode=0o600)
    canary_path.unlink()
    paths["canary"] = new_canary_path

    observation_path = paths["observation"]
    observation = json.loads(observation_path.read_text(encoding="utf-8"))
    subject = observation["subjects"][0]
    for section in ("endpoint", "canary"):
        evidence = subject[section]["evidence"]["evidence_refs"][0]
        evidence["evidence_ref"] = new_canary_path.absolute().as_posix()
        evidence["revision"] = canary["receipt_id"]
    write_json(observation_path, observation, mode=0o600)

    assert old_receipt_id != canary["receipt_id"]


def upgrade_registry_input_to_v2(paths: dict[str, Path]) -> None:
    registry_path = paths["registry"]
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    record = registry["records"][0]
    contour = {
        "contour_id": "read",
        "policy_family": "read",
        "authority_class": "read",
        "credential_class": "kag-read",
        "registry_state": record.pop("registry_state"),
        "revisions": record.pop("revisions"),
        "maturity": record.pop("maturity"),
        "capabilities": record.pop("capabilities"),
    }
    contour["maturity"]["declared"] = {
        "state": "not_asserted",
        "freshness_policy": None,
        "evidence": None,
    }
    record["contours"] = [contour]
    registry["schema_version"] = "aoa_organ_registry_source_v2"
    write_json(registry_path, registry, mode=0o600)

    observation_path = paths["observation"]
    observation = json.loads(observation_path.read_text(encoding="utf-8"))
    subject = observation["subjects"][0]
    source_revision = contour["revisions"]["source"]["revision"]
    subject["source"]["evidence"] = {
        "state": "exact",
        "observed_at": "2026-07-28T15:02:00Z",
        "expires_at": "2026-07-28T15:10:00Z",
        "evidence_refs": [
            {
                "owner": record["owners"]["source_owner"],
                "evidence_ref": "owner://aoa-kag/source/fixture",
                "revision": source_revision,
                "observed_at": "2026-07-28T15:02:00Z",
                "expires_at": "2026-07-28T15:10:00Z",
            }
        ],
        "reason_codes": [],
    }
    subject["registry"]["registry_digest"] = canonical_digest(contour)
    write_json(observation_path, observation, mode=0o600)


def test_checked_in_scenarios_match_bounded_expectations() -> None:
    completed = run_runner("run-scenarios")
    assert completed.returncode == 0, completed.stderr or completed.stdout
    report = json.loads(completed.stdout)
    assert report["scenario_count"] == 11
    assert report["passed_count"] == 11
    assert report["failed_count"] == 0
    assert report["verdict"] == "supports bounded claim"

    schema = json.loads(
        (BUNDLE_ROOT / "reports" / "summary.schema.json").read_text(encoding="utf-8")
    )
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(report)


def test_valid_packet_and_honest_insufficient_evidence_are_accepted() -> None:
    for name in ("valid-read.json", "insufficient-read.json"):
        completed = run_runner(
            "validate-packet", str(BUNDLE_ROOT / "fixtures" / "packets" / name)
        )
        assert completed.returncode == 0, completed.stderr or completed.stdout
        payload = json.loads(completed.stdout)
        assert payload["accepted_by_source_contract"] is True
        assert payload["issues"] == []


def test_example_report_matches_report_contract() -> None:
    schema = json.loads(
        (BUNDLE_ROOT / "reports" / "summary.schema.json").read_text(encoding="utf-8")
    )
    example = json.loads(
        (BUNDLE_ROOT / "reports" / "example-report.json").read_text(encoding="utf-8")
    )
    Draft202012Validator(schema).validate(example)
    assert example["limitations"]
    assert example["failed_count"] == 0


def test_private_packet_review_binds_source_and_preserves_claim_limits(
    tmp_path: Path,
) -> None:
    packet = (
        BUNDLE_ROOT / "fixtures" / "packets" / "insufficient-read.json"
    )
    output = tmp_path / "private-review" / "report.json"
    completed = run_runner(
        "review-packet",
        str(packet),
        "--output",
        str(output),
        "--reviewed-at",
        "2026-07-29T02:40:00Z",
    )

    assert completed.returncode == 0, completed.stderr or completed.stdout
    summary = json.loads(completed.stdout)
    report = json.loads(output.read_text(encoding="utf-8"))
    schema = json.loads(
        (BUNDLE_ROOT / "reports" / "live-review.schema.json").read_text(
            encoding="utf-8"
        )
    )
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(report)
    assert stat.S_IMODE(output.stat().st_mode) == 0o600
    assert summary["verdict"] == "supported_bounded"
    assert report["packet"]["result_verdict"] == "insufficient_evidence"
    assert report["packet_validation"] == {
        "accepted_by_source_contract": True,
        "issues": [],
    }
    assert report["negative_suite"]["scenario_count"] == 11
    assert report["negative_suite"]["failed_count"] == 0
    assert report["central_proof_asserted"] is True
    assert report["owner_acceptance_inferred"] is False
    assert report["admission_change_authorized"] is False
    assert report["higher_effect_authorized"] is False
    assert report["cross_organ_benefit_asserted"] is False
    assert report["rollback_proven"] is False
    assert report["actual_effects"] == []


def test_private_packet_review_rejects_contract_violation(
    tmp_path: Path,
) -> None:
    packet = json.loads(
        (
            BUNDLE_ROOT / "fixtures" / "packets" / "insufficient-read.json"
        ).read_text(encoding="utf-8")
    )
    packet["result"]["admission_change_authorized"] = True
    packet_path = write_json(tmp_path / "invalid-packet.json", packet)
    output = tmp_path / "private-review" / "report.json"
    completed = run_runner(
        "review-packet",
        str(packet_path),
        "--output",
        str(output),
        "--reviewed-at",
        "2026-07-29T02:40:00Z",
    )

    assert completed.returncode == 1
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["verdict"] == "rejected_contract"
    assert report["central_proof_asserted"] is False
    assert (
        "admission_change_not_authorized_by_central_proof"
        in report["packet_validation"]["issues"]
    )


@pytest.mark.parametrize(
    "mutation",
    [
        "failed_count",
        "passed_count",
        "scenario_count",
        "failed_outcome",
    ],
)
def test_positive_report_rejects_self_contradictory_counts_and_outcomes(
    mutation: str,
) -> None:
    schema = json.loads(
        (BUNDLE_ROOT / "reports" / "summary.schema.json").read_text(encoding="utf-8")
    )
    example = json.loads(
        (BUNDLE_ROOT / "reports" / "example-report.json").read_text(encoding="utf-8")
    )
    payload = deepcopy(example)
    if mutation == "failed_count":
        payload["failed_count"] = 1
    elif mutation == "passed_count":
        payload["passed_count"] = 10
    elif mutation == "scenario_count":
        payload["scenario_count"] = 10
    else:
        payload["per_scenario_breakdown"][0]["outcome"] = "fail"

    with pytest.raises(ValidationError):
        Draft202012Validator(schema).validate(payload)


def test_negative_scenarios_cover_forbidden_admission_inferences() -> None:
    expected_codes = set()
    for scenario_path in sorted(
        (BUNDLE_ROOT / "fixtures" / "scenarios").glob("*.json")
    ):
        scenario = json.loads(scenario_path.read_text(encoding="utf-8"))
        expected_codes.update(scenario["expected_codes"])

    assert "endpoint_ready_does_not_imply_result_grounded" in expected_codes
    assert "central_eval_does_not_imply_owner_accepted" in expected_codes
    assert "read_or_candidate_plane_cannot_authorize_effect" in expected_codes
    assert "admission_change_not_authorized_by_central_proof" in expected_codes
    assert (
        "axis_evidence_expired_within_observation_window:freshness_satisfied"
        in expected_codes
    )
    assert "positive_verdict_requires_asserted_evidence" in expected_codes
    assert "axis_revision_slot_mismatch:deployed" in expected_codes
    assert "observation_window_invalid" in expected_codes


def test_live_materializer_asserts_only_independently_bound_axes(
    tmp_path: Path,
) -> None:
    paths = live_packet_inputs(tmp_path)
    completed = run_materializer(paths)
    assert completed.returncode == 0, completed.stderr or completed.stdout
    summary = json.loads(completed.stdout)
    packet = json.loads(paths["output"].read_text(encoding="utf-8"))

    assert summary["verdict"] == "insufficient_evidence"
    assert summary["asserted_axes"] == [
        "call_succeeded",
        "declared",
        "deployed",
        "endpoint_ready",
        "exported",
        "packaged",
        "process_alive",
        "registry_indexed",
        "schema_observed",
    ]
    assert stat.S_IMODE(paths["output"].stat().st_mode) == 0o600
    assert packet["result"]["admission_change_authorized"] is False
    assert packet["result"]["owner_acceptance_inferred"] is False
    assert packet["result"]["higher_effect_authorized"] is False
    for axis in (
        "owner_reviewed",
        "consumer_registered",
        "result_grounded",
        "freshness_satisfied",
        "owner_accepted",
        "cross_organ_proven",
        "rollback_proven",
    ):
        assert packet["maturity"][axis] == {"state": "not_asserted"}

    validated = run_runner("validate-packet", str(paths["output"]))
    assert validated.returncode == 0, validated.stderr or validated.stdout
    result = json.loads(validated.stdout)
    assert result["accepted_by_source_contract"] is True
    assert result["issues"] == []


def test_live_materializer_accepts_attested_canary_v2_shape(
    tmp_path: Path,
) -> None:
    paths = live_packet_inputs(tmp_path)
    upgrade_canary_inputs_to_v2(paths)

    completed = run_materializer(paths)

    assert completed.returncode == 0, completed.stderr or completed.stdout
    packet = json.loads(paths["output"].read_text(encoding="utf-8"))
    assert packet["maturity"]["call_succeeded"]["state"] == "asserted"


def test_live_materializer_accepts_deployment_bound_canary_v3_shape(
    tmp_path: Path,
) -> None:
    paths = live_packet_inputs(tmp_path)
    upgrade_canary_inputs_to_v3(paths)

    completed = run_materializer(paths)

    assert completed.returncode == 0, completed.stderr or completed.stdout
    packet = json.loads(paths["output"].read_text(encoding="utf-8"))
    assert packet["maturity"]["call_succeeded"]["state"] == "asserted"


def test_live_materializer_rejects_v3_deployment_binding_drift(
    tmp_path: Path,
) -> None:
    paths = live_packet_inputs(tmp_path)
    upgrade_canary_inputs_to_v3(paths)
    canary = json.loads(paths["canary"].read_text(encoding="utf-8"))
    canary["deployment_tree_digest"] = "sha256:" + ("9" * 64)
    unsigned = {
        key: value
        for key, value in canary.items()
        if key not in {"receipt_id", "attestation"}
    }
    canary["receipt_id"] = canonical_digest(unsigned)
    write_json(paths["canary"], canary, mode=0o600)

    completed = run_materializer(paths)

    assert completed.returncode == 1
    assert "v3 canary does not bind the selected deployment" in completed.stderr
    assert not paths["output"].exists()


def test_live_materializer_accepts_v2_read_contour_with_owner_source_observation(
    tmp_path: Path,
) -> None:
    paths = live_packet_inputs(tmp_path)
    upgrade_canary_inputs_to_v3(paths)
    upgrade_registry_input_to_v2(paths)

    completed = run_materializer(paths)

    assert completed.returncode == 0, completed.stderr or completed.stdout
    packet = json.loads(paths["output"].read_text(encoding="utf-8"))
    assert packet["maturity"]["declared"]["state"] == "asserted"
    assert packet["maturity"]["declared"]["evidence_ref"] == (
        "owner://aoa-kag/source/fixture"
    )


def test_live_materializer_rejects_v2_result_signer_drift(
    tmp_path: Path,
) -> None:
    paths = live_packet_inputs(tmp_path)
    upgrade_canary_inputs_to_v2(paths)
    result = json.loads(paths["result"].read_text(encoding="utf-8"))
    result["signer_id"] = "sha256:" + ("2" * 64)
    unsigned = {
        key: value
        for key, value in result.items()
        if key not in {"artifact_id", "attestation"}
    }
    result["artifact_id"] = canonical_digest(unsigned)
    write_json(paths["result"], result, mode=0o600)

    completed = run_materializer(paths)

    assert completed.returncode == 1
    assert "result artifact signer does not match" in completed.stderr
    assert not paths["output"].exists()


def test_live_materializer_asserts_only_exact_owner_review_axes(
    tmp_path: Path,
) -> None:
    paths = live_packet_inputs(tmp_path)
    completed = run_materializer(paths, include_owner_review=True)
    assert completed.returncode == 0, completed.stderr or completed.stdout
    summary = json.loads(completed.stdout)
    packet = json.loads(paths["output"].read_text(encoding="utf-8"))

    assert summary["verdict"] == "insufficient_evidence"
    assert packet["capability_id"] == "knowledge-retrieval"
    assert packet["maturity"]["result_grounded"]["state"] == "asserted"
    assert packet["maturity"]["result_grounded"]["evidence_kind"] == (
        "owner_grounding_review"
    )
    assert packet["maturity"]["freshness_satisfied"]["state"] == "asserted"
    assert packet["maturity"]["freshness_satisfied"]["evidence_kind"] == (
        "freshness_review"
    )
    for axis in (
        "owner_reviewed",
        "consumer_registered",
        "owner_accepted",
        "cross_organ_proven",
        "rollback_proven",
    ):
        assert packet["maturity"][axis] == {"state": "not_asserted"}
    assert packet["result"]["admission_change_authorized"] is False
    assert packet["result"]["owner_acceptance_inferred"] is False
    assert packet["result"]["higher_effect_authorized"] is False

    validated = run_runner("validate-packet", str(paths["output"]))
    assert validated.returncode == 0, validated.stderr or validated.stdout
    result = json.loads(validated.stdout)
    assert result["accepted_by_source_contract"] is True
    assert result["issues"] == []


def test_live_materializer_does_not_promote_blocked_owner_freshness(
    tmp_path: Path,
) -> None:
    paths = live_packet_inputs(tmp_path)
    review = json.loads(paths["owner_review"].read_text(encoding="utf-8"))
    review["freshness_state"] = "blocked"
    review["provider_watermark"] = None
    review["reason_codes"] = ["owner-freshness-blocked"]
    review_body = {key: value for key, value in review.items() if key != "review_id"}
    review["review_id"] = sdk_canonical_digest(review_body)
    write_json(paths["owner_review"], review, mode=0o600)

    completed = run_materializer(paths, include_owner_review=True)

    assert completed.returncode == 0, completed.stderr or completed.stdout
    packet = json.loads(paths["output"].read_text(encoding="utf-8"))
    assert packet["maturity"]["result_grounded"]["state"] == "asserted"
    assert packet["maturity"]["freshness_satisfied"] == {"state": "not_asserted"}


def test_live_materializer_rejects_owner_review_authority_escalation(
    tmp_path: Path,
) -> None:
    paths = live_packet_inputs(tmp_path)
    review = json.loads(paths["owner_review"].read_text(encoding="utf-8"))
    review["owner_accepted"] = True
    review_body = {key: value for key, value in review.items() if key != "review_id"}
    review["review_id"] = sdk_canonical_digest(review_body)
    write_json(paths["owner_review"], review, mode=0o600)

    completed = run_materializer(paths, include_owner_review=True)

    assert completed.returncode == 1
    assert "cannot assert owner accepted" in completed.stderr
    assert not paths["output"].exists()


def test_live_materializer_rejects_tampered_owner_review(
    tmp_path: Path,
) -> None:
    paths = live_packet_inputs(tmp_path)
    review = json.loads(paths["owner_review"].read_text(encoding="utf-8"))
    review["capture"]["result_digest"] = "sha256:" + ("9" * 64)
    write_json(paths["owner_review"], review, mode=0o600)

    completed = run_materializer(paths, include_owner_review=True)

    assert completed.returncode == 1
    assert "content address is invalid" in completed.stderr
    assert not paths["output"].exists()


def test_live_materializer_rejects_tampered_canary_without_output(
    tmp_path: Path,
) -> None:
    paths = live_packet_inputs(tmp_path)
    canary = json.loads(paths["canary"].read_text(encoding="utf-8"))
    canary["server_version"] = "99.0.0"
    write_json(paths["canary"], canary, mode=0o600)

    completed = run_materializer(paths)

    assert completed.returncode == 1
    assert "content address is invalid" in completed.stderr
    assert not paths["output"].exists()


def test_live_materializer_rejects_tampered_result_artifact(
    tmp_path: Path,
) -> None:
    paths = live_packet_inputs(tmp_path)
    artifact = json.loads(paths["result"].read_text(encoding="utf-8"))
    artifact["owner_payload"]["owners"] = []
    write_json(paths["result"], artifact, mode=0o600)

    completed = run_materializer(paths)

    assert completed.returncode == 1
    assert "owner payload digest is invalid" in completed.stderr
    assert not paths["output"].exists()


def test_live_materializer_rejects_cross_input_deploy_drift(
    tmp_path: Path,
) -> None:
    paths = live_packet_inputs(tmp_path)
    observation = json.loads(paths["observation"].read_text(encoding="utf-8"))
    observation["subjects"][0]["package"]["artifact_digest"] = "sha256:" + ("9" * 64)
    write_json(paths["observation"], observation, mode=0o600)

    completed = run_materializer(paths)

    assert completed.returncode == 1
    assert "does not bind the selected deployment" in completed.stderr
    assert not paths["output"].exists()


def test_live_materializer_requires_private_source_inputs(
    tmp_path: Path,
) -> None:
    paths = live_packet_inputs(tmp_path)
    paths["registry"].chmod(0o640)

    completed = run_materializer(paths)

    assert completed.returncode == 1
    assert "must not be group/world accessible" in completed.stderr
    assert not paths["output"].exists()


def test_live_materializer_rejects_secret_bearing_namespaced_keys(
    tmp_path: Path,
) -> None:
    paths = live_packet_inputs(tmp_path)
    registry = json.loads(paths["registry"].read_text(encoding="utf-8"))
    registry["read_bearer_token"] = "must-not-cross"
    write_json(paths["registry"], registry, mode=0o600)

    completed = run_materializer(paths)

    assert completed.returncode == 1
    assert "secret-bearing key is forbidden" in completed.stderr
    assert not paths["output"].exists()


def test_live_materializer_requires_observation_to_bind_canary_endpoint(
    tmp_path: Path,
) -> None:
    paths = live_packet_inputs(tmp_path)
    observation = json.loads(paths["observation"].read_text(encoding="utf-8"))
    observation["subjects"][0]["endpoint"]["endpoint_ref"] = "http://127.0.0.1:6553/mcp"
    write_json(paths["observation"], observation, mode=0o600)

    completed = run_materializer(paths)

    assert completed.returncode == 1
    assert "does not bind the canary receipt" in completed.stderr
    assert not paths["output"].exists()


def test_live_materializer_does_not_coerce_missing_owner_identity(
    tmp_path: Path,
) -> None:
    paths = live_packet_inputs(tmp_path)
    registry = json.loads(paths["registry"].read_text(encoding="utf-8"))
    registry["records"][0]["owners"]["control_owner"] = None
    write_json(paths["registry"], registry, mode=0o600)
    observation = json.loads(paths["observation"].read_text(encoding="utf-8"))
    observation["subjects"][0]["registry"]["registry_digest"] = canonical_digest(
        registry["records"][0]
    )
    write_json(paths["observation"], observation, mode=0o600)

    completed = run_materializer(paths)

    assert completed.returncode == 1
    assert "registry lacks owner, source, or control identity" in completed.stderr
    assert not paths["output"].exists()
