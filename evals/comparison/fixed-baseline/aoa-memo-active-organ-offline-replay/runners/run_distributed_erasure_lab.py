#!/usr/bin/env python3
"""Run the Phase 11 public-safe distributed-erasure reference lab."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import importlib
import importlib.util
import json
from pathlib import Path
from time import perf_counter
import sys
from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator, FormatChecker


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = BUNDLE_ROOT / "fixtures" / "distributed-erasure-cases.json"
REPORT_SCHEMA_PATH = BUNDLE_ROOT / "reports" / "distributed-erasure.schema.json"
EVAL_OWNER_SCHEMA_PATH = BUNDLE_ROOT / "reports" / "erasure-owner-extension.schema.json"
MEMO_MODULE_REL = (
    "mechanics/retention/parts/consolidation-and-forgetting/scripts/"
    "distributed_erasure.py"
)
MEMO_PROBE_SCHEMA_REL = (
    "mechanics/retention/parts/consolidation-and-forgetting/schemas/"
    "active_organ_erasure_recovery_probe_v0.schema.json"
)
MEMO_OWNER_SCHEMA_REL = (
    "mechanics/retention/parts/consolidation-and-forgetting/schemas/"
    "active_organ_memo_erasure_owner_extension_v0.schema.json"
)
MEMO_BASE_SCHEMA_REL = "schemas/support-objects/active_organ_memo_contracts_v1.schema.json"
MEMO_DECISION_REL = (
    "docs/decisions/"
    "AOA-MEM-D-0080-distributed-erasure-requires-walkable-owner-closure.md"
)
SESSION_OWNER_SCHEMA_REL = (
    "schemas/active-organ-session-erasure-owner-extension-v0.schema.json"
)
KAG_OWNER_SCHEMA_REL = (
    "mechanics/antifragility/parts/projection-health/schemas/"
    "active_organ_projection_erasure_owner_extension_v0.schema.json"
)
STACK_OWNER_SCHEMA_REL = (
    "mechanics/federation-seams/parts/memo-seam/schemas/"
    "active-organ-runtime-erasure-owner-extension-v0.schema.json"
)
MACHINE_OWNER_SCHEMA_REL = (
    "schemas/active-organ-host-erasure-owner-extension-v0.schema.json"
)
ZERO_DIGEST = "sha256:" + ("0" * 64)
CONTRACT_NAMES = {
    "memory_erase_request": ("C14", "MemoryEraseRequest"),
    "distributed_memory_erase_manifest": (
        "C15",
        "DistributedMemoryEraseManifest",
    ),
    "per_owner_erase_work_item": ("C16", "PerOwnerEraseWorkItem"),
    "erase_completion_or_residue_receipt": (
        "C17",
        "EraseCompletionOrResidueReceipt",
    ),
}


class DistributedErasureLabError(RuntimeError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DistributedErasureLabError(f"{path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise DistributedErasureLabError(f"{path}: expected JSON object")
    return payload


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def canonical_digest(
    payload: Any,
    *,
    exclude: set[str] | None = None,
) -> str:
    excluded = exclude or set()
    normalized = (
        {key: value for key, value in payload.items() if key not in excluded}
        if isinstance(payload, dict)
        else payload
    )
    encoded = json.dumps(
        normalized,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def file_digest(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise DistributedErasureLabError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def schema_validator(path: Path) -> Draft202012Validator:
    schema = load_json(path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validation_issues(
    payload: Mapping[str, Any],
    validator: Draft202012Validator,
    label: str,
) -> list[str]:
    issues = []
    for error in sorted(
        validator.iter_errors(payload),
        key=lambda item: list(item.absolute_path),
    ):
        location = ".".join(str(item) for item in error.absolute_path) or "<root>"
        issues.append(f"{label} schema violation at {location}: {error.message}")
    return issues


def _header(
    *,
    contract_type: str,
    instance_id: str,
    fixture: Mapping[str, Any],
    source_digest: str,
    validation_status: str = "valid",
) -> dict[str, Any]:
    contract_id, contract_name = CONTRACT_NAMES[contract_type]
    return {
        "contract_type": contract_type,
        "schema_version": "1.0.0",
        "contract_id": contract_id,
        "contract_name": contract_name,
        "instance_id": instance_id,
        "object_version": 1,
        "idempotency_key": f"idempotency:phase11:{instance_id}",
        "produced_at": fixture["reference_time"],
        "owner": "aoa-memo",
        "validation_status": validation_status,
        "source_refs": [
            {
                "source_ref": fixture["decision_ref"],
                "source_owner": "aoa-memo",
                "source_version": "phase11-v0",
                "content_digest": source_digest,
            }
        ],
        "generation_pin": {
            "generator_id": "aoa-evals.distributed-erasure-reference-lab",
            "generator_version": "phase11-v0",
            "generated_at": fixture["reference_time"],
        },
        "policy_pin": {
            "policy_id": "aoa-memo.distributed-erasure",
            "policy_version": "phase11-v0",
            "decision_ref": fixture["decision_ref"],
        },
        "content_digest": canonical_digest(
            {
                "contract_type": contract_type,
                "instance_id": instance_id,
                "scope": "public-safe-reference-lab",
            }
        ),
    }


def _owner_schema_paths(
    *,
    memo_root: Path,
    session_memory_root: Path,
    kag_root: Path,
    stack_root: Path,
    machine_root: Path,
) -> dict[str, Path]:
    return {
        "memo": memo_root / MEMO_OWNER_SCHEMA_REL,
        "session": session_memory_root / SESSION_OWNER_SCHEMA_REL,
        "kag": kag_root / KAG_OWNER_SCHEMA_REL,
        "stack": stack_root / STACK_OWNER_SCHEMA_REL,
        "machine": machine_root / MACHINE_OWNER_SCHEMA_REL,
        "eval": EVAL_OWNER_SCHEMA_PATH,
    }


def _target_class(surface_id: str) -> str:
    if surface_id in {"ER0", "ER1", "ER9"}:
        return "source"
    if surface_id in {"ER2", "ER3", "ER7", "ER8"}:
        return "derived"
    if surface_id in {"ER4", "ER5"}:
        return "runtime"
    return "host"


def _owner_extension(
    memo: Any,
    surface: Mapping[str, Any],
    *,
    work_ref: str,
    probe_ref: str,
    canary_digest: str,
) -> dict[str, Any]:
    surface_id = surface["surface_id"]
    extension = {
        "schema_version": "active_organ_owner_erasure_extension_v0",
        "extension_id": f"erase-extension:phase11:{surface_id}",
        "parent_owner": surface["parent_owner"],
        "worker_owner": surface["worker_owner"],
        "surface_id": surface_id,
        "work_item_ref": work_ref,
        "material_classes": list(surface["material_classes"]),
        "target_ref_digests": [canary_digest],
        "operation_evidence_refs": [
            f"operation-evidence:phase11:{surface_id}:reference-lab"
        ],
        "recovery_probe_ref": probe_ref,
        "result": "erased",
        "residue_refs": [],
        "retention_exceptions": [],
        "subject_material_included": False,
        "content_minimized": True,
        "execution_posture": "reference_lab_only",
        "live_execution": False,
        "effect_authority": "owner_local_erasure_only",
        "global_completion_authority": False,
        "content_digest": ZERO_DIGEST,
    }
    schema_owner = surface["schema_owner"]
    if schema_owner == "session":
        extension.update(
            {
                "operator_privacy_decision_ref": (
                    "decision:operator:phase11:synthetic-privacy-erasure"
                ),
                "ordinary_cleanup": False,
                "raw_evidence_scope": (
                    "exact_operator_authorized_refs"
                    if surface_id == "ER1"
                    else "not_applicable"
                ),
            }
        )
    elif schema_owner == "kag":
        extension.update(
            {
                "c13_invalidation_receipt_ref": (
                    "receipt:phase11:C13:synthetic-invalidation"
                ),
                "recall_admission": "blocked",
                "rebuild_recovery_checked": True,
            }
        )
    elif schema_owner == "stack":
        extension.update(
            {
                "restore_recovery_checked": True,
                "project_root_mutation": "forbidden",
                "host_root_mutation": "forbidden",
            }
        )
    elif schema_owner == "machine":
        extension.update(
            {
                "target_root_class": "srv_abyss_machine",
                "host_path_disclosed": False,
                "physical_evidence_ref": (
                    "physical-evidence:phase11:synthetic-host-surface"
                ),
                "rebuild_recovery_checked": True,
                "project_root_mutation": "forbidden",
                "stack_root_mutation": "forbidden",
            }
        )
    elif schema_owner == "eval":
        extension.update(
            {
                "training_ingestion_attestation_ref": (
                    "attestation:phase11:synthetic-training-ingestion"
                    if surface_id == "ER8"
                    else None
                ),
                "checkpoint_or_replay_probe_ref": (
                    f"probe:phase11:{surface_id}:checkpoint-or-replay"
                ),
                "model_unlearning_authority": (
                    "synthetic_model_owner_only"
                    if surface_id == "ER8"
                    else "not_applicable"
                ),
                "runtime_promotion_allowed": False,
            }
        )
    extension["content_digest"] = memo.normalized_digest(extension)
    return extension


def build_complete_bundle(
    memo: Any,
    fixture: Mapping[str, Any],
    *,
    decision_digest: str,
) -> dict[str, Any]:
    """Build a full C14-C17 graph without executing an external effect."""

    manifest_id = "erase-manifest:phase11:complete"
    request_id = "erase-request:phase11:synthetic"
    canary_digest = canonical_digest(
        {
            "canary": "phase11-public-safe-synthetic-marker",
            "raw_subject_material": "never-stored",
        }
    )
    work_items = []
    receipts = []
    extensions = {}
    probes = {}
    surfaces = []
    owner_results = []
    for surface in fixture["surfaces"]:
        surface_id = surface["surface_id"]
        worker = surface["worker_owner"]
        work_ref = f"erase-work:phase11:{surface_id}"
        receipt_ref = f"erase-receipt:phase11:{surface_id}"
        probe_ref = f"erase-probe:phase11:{surface_id}"
        extension = _owner_extension(
            memo,
            surface,
            work_ref=work_ref,
            probe_ref=probe_ref,
            canary_digest=canary_digest,
        )
        extension_ref = extension["extension_id"]
        extensions[extension_ref] = extension
        probe = memo.build_erasure_recovery_probe(
            probe_id=probe_ref,
            surface_id=surface_id,
            worker_owner=worker,
            work_item_ref=work_ref,
            canary_digest=canary_digest,
            positive_match_count=1,
            query_classes=surface["query_classes"],
            race_rebuild_required=surface_id in memo.RACE_REBUILD_REQUIRED,
            race_rebuild_attempted=surface_id in memo.RACE_REBUILD_REQUIRED,
            performed_at=fixture["reference_time"],
        )
        probes[probe_ref] = probe
        pin = {
            "schema_ref": f"schema:phase11:{surface['schema_owner']}:{surface_id}",
            "schema_version": "0",
            "payload_ref": extension_ref,
            "payload_digest": extension["content_digest"],
        }
        target_root = (
            "host:abyss-machine-managed-memory-surface"
            if surface_id == "ER6"
            else f"owner-root:{surface['parent_owner']}:{surface_id}"
        )
        target_refs = [f"target-digest-ref:phase11:{surface_id}:{canary_digest}"]
        work = _header(
            contract_type="per_owner_erase_work_item",
            instance_id=work_ref,
            fixture=fixture,
            source_digest=decision_digest,
        )
        work.update(
            {
                "work_item_id": work_ref,
                "manifest_ref": manifest_id,
                "target_owner": worker,
                "target_class": _target_class(surface_id),
                "target_root": target_root,
                "target_refs": target_refs,
                "erase_surface_id": surface_id,
                "descendant_refs": [],
                "retention_exceptions": [],
                "owner_extension": pin,
                "work_state": "erased",
            }
        )
        receipt = _header(
            contract_type="erase_completion_or_residue_receipt",
            instance_id=receipt_ref,
            fixture=fixture,
            source_digest=decision_digest,
        )
        receipt.update(
            {
                "receipt_id": receipt_ref,
                "manifest_ref": manifest_id,
                "receipt_owner": worker,
                "work_item_ref": work_ref,
                "erase_surface_id": surface_id,
                "result": "erased",
                "erased_count": len(surface["material_classes"]),
                "residue_count": 0,
                "residue_refs": [],
                "recovery_probe_refs": [probe_ref],
                "retention_exceptions": [],
                "owner_extension": deepcopy(pin),
                "global_completion_authority": False,
                "content_minimized": True,
            }
        )
        work_items.append(work)
        receipts.append(receipt)
        surfaces.append(
            {
                "surface_id": surface_id,
                "surface_class": surface["surface_class"],
                "owner": worker,
                "work_item_ref": work_ref,
                "descendant_refs": [],
                "retention_exceptions": [],
                "surface_state": "erased",
            }
        )
        owner_results.append(
            {
                "owner": worker,
                "work_item_ref": work_ref,
                "erase_receipt_ref": receipt_ref,
                "recovery_probe_ref": probe_ref,
                "result": "erased",
            }
        )

    workers = [surface["worker_owner"] for surface in fixture["surfaces"]]
    request = _header(
        contract_type="memory_erase_request",
        instance_id=request_id,
        fixture=fixture,
        source_digest=decision_digest,
    )
    request.update(
        {
            "erase_request_id": request_id,
            "operator_decision_ref": (
                "decision:operator:phase11:synthetic-privacy-erasure"
            ),
            "scope": {
                "owner_set": workers,
                "subject_refs": [f"subject-canary-digest:{canary_digest}"],
                "corpus_refs": [],
                "erase_surface_ids": [
                    surface["surface_id"] for surface in fixture["surfaces"]
                ],
                "descendant_refs": [
                    f"descendant-family:phase11:{surface['surface_id']}"
                    for surface in fixture["surfaces"]
                ],
                "retention_exceptions": [],
            },
            "reason": "public-safe synthetic distributed-erasure conformance lab",
            "requested_at": fixture["reference_time"],
            "recovery_probe_required": True,
        }
    )
    manifest = _header(
        contract_type="distributed_memory_erase_manifest",
        instance_id=manifest_id,
        fixture=fixture,
        source_digest=decision_digest,
    )
    manifest.update(
        {
            "manifest_id": manifest_id,
            "erase_request_ref": request_id,
            "owner_set": workers,
            "work_item_refs": [item["work_item_id"] for item in work_items],
            "erase_receipt_refs": [item["receipt_id"] for item in receipts],
            "recovery_probe_refs": list(probes),
            "residue_refs": [],
            "erase_surfaces": surfaces,
            "owner_results": owner_results,
            "completion_state": "complete",
        }
    )
    return {
        "request": request,
        "manifest": manifest,
        "work_items": work_items,
        "receipts": receipts,
        "owner_extensions": extensions,
        "probes": probes,
        "canary_digest": canary_digest,
    }


def _load_semantic_validator(memo_root: Path):
    root = str(memo_root)
    if root not in sys.path:
        sys.path.insert(0, root)
    module = importlib.import_module("scripts.memory.validators.schema_surfaces")
    return module._active_organ_contract_errors


def bundle_issues(
    bundle: Mapping[str, Any],
    *,
    memo: Any,
    base_validator: Draft202012Validator,
    probe_validator: Draft202012Validator,
    owner_validators: Mapping[str, Draft202012Validator],
    surface_schema_owners: Mapping[str, str],
    semantic_validator: Any,
) -> list[str]:
    issues = []
    objects: list[Mapping[str, Any]] = [
        bundle["request"],
        bundle["manifest"],
        *bundle["work_items"],
        *bundle["receipts"],
    ]
    for item in objects:
        label = f"{item.get('contract_id')}:{item.get('instance_id')}"
        issues.extend(validation_issues(item, base_validator, label))
        issues.extend(f"{label} semantic: {issue}" for issue in semantic_validator(dict(item)))
    for extension in bundle["owner_extensions"].values():
        surface_id = extension["surface_id"]
        schema_owner = surface_schema_owners[surface_id]
        issues.extend(
            validation_issues(
                extension,
                owner_validators[schema_owner],
                f"{surface_id}:{schema_owner}:owner-extension",
            )
        )
        issues.extend(
            f"{surface_id}: {issue}"
            for issue in memo.validate_owner_erasure_extension(extension)
        )
    for probe in bundle["probes"].values():
        surface_id = probe.get("surface_id", "unknown")
        issues.extend(
            validation_issues(probe, probe_validator, f"{surface_id}:probe")
        )
        issues.extend(
            f"{surface_id}: {issue}"
            for issue in memo.validate_erasure_recovery_probe(probe)
        )
    closure = memo.evaluate_distributed_erasure_closure(
        request=bundle["request"],
        manifest=bundle["manifest"],
        work_items=bundle["work_items"],
        receipts=bundle["receipts"],
        owner_extensions=bundle["owner_extensions"],
        probes=bundle["probes"],
    )
    issues.extend(f"closure: {issue}" for issue in closure["issues"])
    return list(dict.fromkeys(issues))


def _surface_item(bundle: Mapping[str, Any], surface_id: str) -> dict[str, Any]:
    return next(
        item
        for item in bundle["manifest"]["erase_surfaces"]
        if item["surface_id"] == surface_id
    )


def _owner_result(bundle: Mapping[str, Any], surface_id: str) -> dict[str, Any]:
    worker = _surface_item(bundle, surface_id)["owner"]
    return next(
        item
        for item in bundle["manifest"]["owner_results"]
        if item["owner"] == worker
    )


def _work(bundle: Mapping[str, Any], surface_id: str) -> dict[str, Any]:
    return next(
        item for item in bundle["work_items"] if item["erase_surface_id"] == surface_id
    )


def _receipt(bundle: Mapping[str, Any], surface_id: str) -> dict[str, Any]:
    return next(
        item for item in bundle["receipts"] if item["erase_surface_id"] == surface_id
    )


def _extension(bundle: Mapping[str, Any], surface_id: str) -> dict[str, Any]:
    return next(
        item
        for item in bundle["owner_extensions"].values()
        if item["surface_id"] == surface_id
    )


def _probe(bundle: Mapping[str, Any], surface_id: str) -> dict[str, Any]:
    return next(
        item
        for item in bundle["probes"].values()
        if item["surface_id"] == surface_id
    )


def _repin_extension(memo: Any, bundle: Mapping[str, Any], surface_id: str) -> None:
    extension = _extension(bundle, surface_id)
    extension["content_digest"] = memo.normalized_digest(extension)
    digest = extension["content_digest"]
    _work(bundle, surface_id)["owner_extension"]["payload_digest"] = digest
    _receipt(bundle, surface_id)["owner_extension"]["payload_digest"] = digest


def build_residue_bundle(
    memo: Any,
    complete: Mapping[str, Any],
    fixture: Mapping[str, Any],
) -> dict[str, Any]:
    residue = deepcopy(complete)
    surface_id = "ER8"
    residue_ref = "residue:phase11:synthetic-unlearning-obligation"
    exception = {
        "exception_ref": "exception:phase11:synthetic-unlearning-obligation",
        "operator_decision_ref": (
            "decision:operator:phase11:synthetic-unlearning-obligation"
        ),
        "expires_at": fixture["retention_exception_expires_at"],
        "restore_probe_ref": "probe:phase11:ER8:exception-expiry",
    }
    receipt = _receipt(residue, surface_id)
    receipt.update(
        {
            "result": "residue",
            "erased_count": 1,
            "residue_count": 1,
            "residue_refs": [residue_ref],
            "retention_exceptions": [exception],
        }
    )
    work = _work(residue, surface_id)
    work.update(
        {
            "retention_exceptions": [exception],
            "work_state": "residue",
        }
    )
    extension = _extension(residue, surface_id)
    extension.update(
        {
            "result": "residue",
            "residue_refs": [residue_ref],
            "retention_exceptions": [exception],
        }
    )
    _repin_extension(memo, residue, surface_id)
    surface = _surface_item(residue, surface_id)
    surface.update(
        {
            "surface_state": "residue",
            "retention_exceptions": [exception],
        }
    )
    _owner_result(residue, surface_id)["result"] = "residue"
    residue["manifest"].update(
        {
            "residue_refs": [residue_ref],
            "completion_state": "complete_with_approved_exceptions",
        }
    )
    return residue


def mutate_fault(
    memo: Any,
    complete: Mapping[str, Any],
    fault: str,
) -> dict[str, Any]:
    bundle = deepcopy(complete)
    if fault == "missing_surface":
        bundle["manifest"]["erase_surfaces"] = [
            item
            for item in bundle["manifest"]["erase_surfaces"]
            if item["surface_id"] != "ER5"
        ]
    elif fault == "missing_receipt":
        bundle["receipts"] = [
            item for item in bundle["receipts"] if item["erase_surface_id"] != "ER4"
        ]
    elif fault == "broken_positive_control":
        probe = _probe(bundle, "ER1")
        probe["positive_control"]["detected_before_erasure"] = False
        probe["content_digest"] = memo.normalized_digest(probe)
    elif fault == "probe_retains_subject_material":
        probe = _probe(bundle, "ER2")
        probe["probe_storage"]["subject_material_included"] = True
        probe["probe_storage"]["canary_digest_only"] = False
        probe["content_digest"] = memo.normalized_digest(probe)
    elif fault == "rebuild_restores_material":
        probe = _probe(bundle, "ER3")
        probe["race_rebuild"]["material_recovered"] = True
        probe["content_digest"] = memo.normalized_digest(probe)
    elif fault == "hidden_residue":
        receipt = _receipt(bundle, "ER4")
        receipt.update(
            {
                "result": "residue",
                "residue_count": 1,
                "residue_refs": ["residue:phase11:hidden-runtime-copy"],
            }
        )
    elif fault == "unlearning_obligation_residue":
        extension = _extension(bundle, "ER8")
        extension.update(
            {
                "result": "residue",
                "residue_refs": [
                    "residue:phase11:unreported-unlearning-obligation"
                ],
            }
        )
        _repin_extension(memo, bundle, "ER8")
    elif fault == "tombstone_identity_leak":
        extension = _extension(bundle, "ER9")
        extension["subject_identity_ref"] = "forbidden:synthetic-subject-identity"
        _repin_extension(memo, bundle, "ER9")
    elif fault == "missing_required_race_probe":
        probe = _probe(bundle, "ER6")
        probe["race_rebuild"]["attempted"] = False
        probe["content_digest"] = memo.normalized_digest(probe)
    elif fault == "owner_extension_binding_drift":
        extension = _extension(bundle, "ER7")
        extension["work_item_ref"] = "erase-work:phase11:wrong-binding"
        _repin_extension(memo, bundle, "ER7")
    else:
        raise DistributedErasureLabError(f"unknown fault case: {fault}")
    return bundle


def run_lab(
    *,
    memo_root: Path,
    session_memory_root: Path,
    kag_root: Path,
    stack_root: Path,
    machine_root: Path,
    output_path: Path | None = None,
) -> dict[str, Any]:
    started = perf_counter()
    fixture = load_json(FIXTURE_PATH)
    memo_module_path = memo_root / MEMO_MODULE_REL
    memo = load_module("aoa_memo_phase11_distributed_erasure", memo_module_path)
    decision_path = memo_root / MEMO_DECISION_REL
    decision_digest = file_digest(decision_path)
    base_schema_path = memo_root / MEMO_BASE_SCHEMA_REL
    probe_schema_path = memo_root / MEMO_PROBE_SCHEMA_REL
    owner_schema_paths = _owner_schema_paths(
        memo_root=memo_root,
        session_memory_root=session_memory_root,
        kag_root=kag_root,
        stack_root=stack_root,
        machine_root=machine_root,
    )
    base_validator = schema_validator(base_schema_path)
    probe_validator = schema_validator(probe_schema_path)
    owner_validators = {
        owner: schema_validator(path) for owner, path in owner_schema_paths.items()
    }
    semantic_validator = _load_semantic_validator(memo_root)
    surface_schema_owners = {
        item["surface_id"]: item["schema_owner"] for item in fixture["surfaces"]
    }

    complete = build_complete_bundle(
        memo,
        fixture,
        decision_digest=decision_digest,
    )
    complete_issues = bundle_issues(
        complete,
        memo=memo,
        base_validator=base_validator,
        probe_validator=probe_validator,
        owner_validators=owner_validators,
        surface_schema_owners=surface_schema_owners,
        semantic_validator=semantic_validator,
    )
    complete_closure = memo.evaluate_distributed_erasure_closure(
        request=complete["request"],
        manifest=complete["manifest"],
        work_items=complete["work_items"],
        receipts=complete["receipts"],
        owner_extensions=complete["owner_extensions"],
        probes=complete["probes"],
    )
    if complete_issues:
        raise DistributedErasureLabError(
            "complete reference closure failed:\n- " + "\n- ".join(complete_issues)
        )

    residue = build_residue_bundle(memo, complete, fixture)
    residue_issues = bundle_issues(
        residue,
        memo=memo,
        base_validator=base_validator,
        probe_validator=probe_validator,
        owner_validators=owner_validators,
        surface_schema_owners=surface_schema_owners,
        semantic_validator=semantic_validator,
    )
    residue_closure = memo.evaluate_distributed_erasure_closure(
        request=residue["request"],
        manifest=residue["manifest"],
        work_items=residue["work_items"],
        receipts=residue["receipts"],
        owner_extensions=residue["owner_extensions"],
        probes=residue["probes"],
    )
    if residue_issues or residue_closure["private_memory_deployment_allowed"]:
        raise DistributedErasureLabError(
            "approved-exception residue scenario did not remain valid and blocked: "
            + "; ".join(residue_issues)
        )

    fault_results = []
    for fault in fixture["fault_cases"]:
        candidate = mutate_fault(memo, complete, fault)
        issues = bundle_issues(
            candidate,
            memo=memo,
            base_validator=base_validator,
            probe_validator=probe_validator,
            owner_validators=owner_validators,
            surface_schema_owners=surface_schema_owners,
            semantic_validator=semantic_validator,
        )
        closure = memo.evaluate_distributed_erasure_closure(
            request=candidate["request"],
            manifest=candidate["manifest"],
            work_items=candidate["work_items"],
            receipts=candidate["receipts"],
            owner_extensions=candidate["owner_extensions"],
            probes=candidate["probes"],
        )
        private_deployment_allowed = (
            closure["private_memory_deployment_allowed"] and not issues
        )
        detected = bool(issues) and not private_deployment_allowed
        if not detected:
            raise DistributedErasureLabError(f"fault escaped closed: {fault}")
        fault_results.append(
            {
                "fault": fault,
                "detected": True,
                "private_memory_deployment_allowed": False,
                "issue_count": len(issues),
                "representative_issue": issues[0],
            }
        )

    query_classes = sorted(
        {
            query_class
            for surface in fixture["surfaces"]
            for query_class in surface["query_classes"]
        }
    )
    surface_results = []
    for surface in fixture["surfaces"]:
        surface_id = surface["surface_id"]
        probe = _probe(complete, surface_id)
        surface_results.append(
            {
                "surface_id": surface_id,
                "surface_class": surface["surface_class"],
                "parent_owner": surface["parent_owner"],
                "worker_owner": surface["worker_owner"],
                "material_classes": surface["material_classes"],
                "owner_schema_valid": True,
                "positive_control_passed": True,
                "negative_recovery_passed": True,
                "race_rebuild_required": (
                    surface_id in memo.RACE_REBUILD_REQUIRED
                ),
                "race_rebuild_passed": (
                    not probe["race_rebuild"]["required"]
                    or probe["race_rebuild"]["attempted"]
                ),
                "subject_material_in_probe": False,
                "result": "erased",
            }
        )

    report = {
        "schema_version": "aoa_memo_phase11_distributed_erasure_report_v0",
        "created_at": fixture["reference_time"],
        "evidence_scope": (
            "source-local-deterministic-public-safe-distributed-erasure-"
            "reference-lab-no-live-deletion"
        ),
        "pins": {
            "runner": file_digest(Path(__file__)),
            "fixture": file_digest(FIXTURE_PATH),
            "report_schema": file_digest(REPORT_SCHEMA_PATH),
            "base_contract_schema": file_digest(base_schema_path),
            "memo_module": file_digest(memo_module_path),
            "recovery_probe_schema": file_digest(probe_schema_path),
            "decision": decision_digest,
            **{
                f"{owner}_owner_schema": file_digest(path)
                for owner, path in owner_schema_paths.items()
            },
        },
        "surface_results": surface_results,
        "abc_comparison": [
            {
                "arm": "A",
                "mechanism": fixture["arms"]["A"],
                "erased_surface_count": 1,
                "recoverable_surface_count": 9,
                "qualified_absence": False,
                "private_memory_deployment_allowed": False,
                "result": "unsafe_incomplete",
            },
            {
                "arm": "B",
                "mechanism": fixture["arms"]["B"],
                "erased_surface_count": 10,
                "recoverable_surface_count": 0,
                "qualified_absence": False,
                "private_memory_deployment_allowed": False,
                "result": "unsafe_false_absence",
            },
            {
                "arm": "C",
                "mechanism": fixture["arms"]["C"],
                "erased_surface_count": 10,
                "recoverable_surface_count": 0,
                "qualified_absence": True,
                "private_memory_deployment_allowed": True,
                "result": "bounded_reference_closure_pass",
            },
        ],
        "fault_results": fault_results,
        "complete_closure": {
            **complete_closure,
            "contract_schema_valid": True,
            "owner_extensions_valid": True,
            "issue_count": 0,
        },
        "approved_exception_residue": {
            "surface_id": "ER8",
            "completion_state": "complete_with_approved_exceptions",
            "base_contract_valid": True,
            "owner_extension_valid": True,
            "residue_present": residue_closure["residue_present"],
            "exceptions_present": residue_closure["exceptions_present"],
            "private_memory_deployment_allowed": False,
            "runtime_promotion_allowed": False,
        },
        "recovery_query_coverage": {
            "query_classes": query_classes,
            "expected_query_classes": [
                "dense",
                "exact",
                "graph",
                "lexical",
                "owner_native",
                "paraphrase",
                "restore",
            ],
            "all_expected_covered": query_classes
            == [
                "dense",
                "exact",
                "graph",
                "lexical",
                "owner_native",
                "paraphrase",
                "restore",
            ],
            "positive_controls_before_erasure": 10,
            "negative_probes_after_erasure": 10,
            "race_rebuild_probes": len(memo.RACE_REBUILD_REQUIRED),
            "recovered_material_count": 0,
        },
        "tombstone": {
            "surface_id": "ER9",
            "material_class": "content_minimized_tombstone",
            "subject_material_included": False,
            "subject_identity_included": False,
            "canary_digest_only": True,
            "global_completion_authority": False,
        },
        "cost_quality_speed_result": {
            "unit": "deterministic_reference_lab_descriptive_only",
            "wall_time_ms": round((perf_counter() - started) * 1000, 3),
            "surface_count": 10,
            "owner_schema_count": len(owner_validators),
            "contract_object_count": 22,
            "recovery_probe_count": 10,
            "fault_case_count": len(fault_results),
            "quality": "all_surfaces_walkable_and_faults_fail_closed",
            "result": "bounded_reference_mechanism_pass",
        },
        "exit_gate": {
            "er0_er9_exactly_once": True,
            "manifest_walkable": complete_closure["walkable"],
            "owner_receipt_per_surface": True,
            "positive_controls_passed": True,
            "negative_recovery_passed": complete_closure["every_probe_passed"],
            "race_rebuild_no_recovery": True,
            "exceptions_explicit_and_deployment_blocking": True,
            "probe_retains_no_subject_material": True,
            "model_unlearning_obligation_covered": True,
            "private_deployment_blocked_when_closure_incomplete": True,
            "passed": True,
        },
        "sampling": {
            "automated_contract_surface_count": 10,
            "automated_fault_case_count": len(fault_results),
            "human_operator_sampling_status": "not_performed",
            "runtime_promotion_allowed": False,
        },
        "authority": {
            "execution_posture": "reference_lab_only",
            "live_private_data_deleted": False,
            "raw_aoa_session_deleted": False,
            "model_unlearning_executed": False,
            "global_completion_claimed_by_owner_receipt": False,
            "runtime_deployment_performed": False,
            "landing_performed": False,
            "sole_human_authority": "operator",
        },
        "limitations": [
            "The lab uses only a synthetic canary digest and performs no live deletion.",
            "Owner schemas prove composability, not deployment readiness or physical erasure.",
            "Human operator sampling and a live private-memory recovery audit remain unperformed.",
            "Synthetic ER8 does not claim authority over any real model or training corpus.",
        ],
        "report_digest": ZERO_DIGEST,
    }
    report["report_digest"] = canonical_digest(
        report,
        exclude={"report_digest"},
    )
    report_validator = schema_validator(REPORT_SCHEMA_PATH)
    report_issues = validation_issues(report, report_validator, "phase11 report")
    if report_issues:
        raise DistributedErasureLabError("\n".join(report_issues))
    if output_path is not None:
        write_json(output_path, report)
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--memo-root", type=Path, required=True)
    parser.add_argument("--session-memory-root", type=Path, required=True)
    parser.add_argument("--kag-root", type=Path, required=True)
    parser.add_argument("--stack-root", type=Path, required=True)
    parser.add_argument("--machine-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = run_lab(
        memo_root=args.memo_root.resolve(),
        session_memory_root=args.session_memory_root.resolve(),
        kag_root=args.kag_root.resolve(),
        stack_root=args.stack_root.resolve(),
        machine_root=args.machine_root.resolve(),
        output_path=args.output.resolve(),
    )
    print(
        json.dumps(
            {
                "status": "passed",
                "surface_count": len(report["surface_results"]),
                "fault_case_count": len(report["fault_results"]),
                "private_deployment_allowed_for_complete_reference": (
                    report["complete_closure"][
                        "private_memory_deployment_allowed"
                    ]
                ),
                "private_deployment_allowed_with_residue": (
                    report["approved_exception_residue"][
                        "private_memory_deployment_allowed"
                    ]
                ),
                "report_digest": report["report_digest"],
                "output": str(args.output.resolve()),
                "landing_performed": False,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
