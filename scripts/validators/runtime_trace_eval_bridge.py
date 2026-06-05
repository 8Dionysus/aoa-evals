"""Trace/eval bridge and artifact-verdict hook validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from jsonschema import Draft202012Validator

from validators import artifact_hooks
from validators.common import (
    ValidationIssue,
    load_json_payload,
    load_mapping_entries,
    relative_location,
    validate_against_schema,
    validate_inline_schema,
)
from validators.runtime_audit_common import RuntimeAuditContext

ARTIFACT_VERDICT_HOOK_SCHEMA_NAME = "artifact-to-verdict-hook.schema.json"
ARTIFACT_VERDICT_HOOK_SCHEMA_PATH = (
    "mechanics/audit/parts/artifact-verdict-hooks/schemas/artifact-to-verdict-hook.schema.json"
)
ARTIFACT_VERDICT_HOOK_EXAMPLES_DIR = "mechanics/audit/parts/artifact-verdict-hooks/examples"
ARTIFACT_VERDICT_HOOK_EXAMPLE_DIRS = (
    ARTIFACT_VERDICT_HOOK_EXAMPLES_DIR,
    "mechanics/checkpoint/parts/a2a-summon-return/examples",
    "mechanics/checkpoint/parts/restartable-inquiry/examples",
    "mechanics/checkpoint/parts/self-agent-posture/examples",
)
ARTIFACT_VERDICT_HOOK_EXAMPLES = artifact_hooks.ARTIFACT_VERDICT_HOOK_EXAMPLES
RUNTIME_POLICY_HOOK_EXPECTATIONS = artifact_hooks.RUNTIME_POLICY_HOOK_EXPECTATIONS
TRACE_EVAL_HOOK_EXPECTATIONS = artifact_hooks.TRACE_EVAL_HOOK_EXPECTATIONS
RUNTIME_POLICY_ARTIFACT_FIELDS = (
    "authorization_artifacts",
    "approval_artifacts",
    "fallback_or_rollback_artifacts",
)


def expected_contract_test_refs(record: Any, repo_root: Path) -> set[str]:
    refs: set[str] = set()
    manifest = getattr(record, "manifest", {})
    bundle_dir = getattr(record, "bundle_dir", None)
    if not isinstance(manifest, dict) or not isinstance(bundle_dir, Path):
        return refs
    for item in manifest.get("evidence", []):
        if not isinstance(item, dict):
            continue
        if item.get("kind") not in {"integrity_check", "support_note"}:
            continue
        raw_path = item.get("path")
        if not isinstance(raw_path, str) or not raw_path:
            continue
        refs.add(f"repo:aoa-evals/{relative_location(bundle_dir, repo_root)}/{raw_path}")
    return refs


def _validate_runtime_policy_boundary(
    *,
    location: str,
    playbook_id: str,
    payload: dict[str, Any],
    issues: list[ValidationIssue],
) -> None:
    expected_boundary = RUNTIME_POLICY_HOOK_EXPECTATIONS.get(playbook_id)
    if expected_boundary is None:
        return

    boundary = payload.get("runtime_policy_boundary")
    if not isinstance(boundary, dict):
        issues.append(
            ValidationIssue(
                location,
                f"runtime_policy_boundary is required for policy-sensitive hook {playbook_id}",
            )
        )
        return

    for field_name, expected_value in expected_boundary.items():
        if boundary.get(field_name) != expected_value:
            issues.append(
                ValidationIssue(
                    f"{location}.runtime_policy_boundary.{field_name}",
                    f"{field_name} must match the policy-sensitive hook expectation",
                )
            )

    artifact_inputs = payload.get("artifact_inputs")
    artifact_input_set = set(artifact_inputs) if isinstance(artifact_inputs, list) else set()
    for field_name in RUNTIME_POLICY_ARTIFACT_FIELDS:
        artifacts = boundary.get(field_name)
        if not isinstance(artifacts, list):
            continue
        missing = [artifact for artifact in artifacts if artifact not in artifact_input_set]
        if missing:
            issues.append(
                ValidationIssue(
                    f"{location}.runtime_policy_boundary.{field_name}",
                    f"{field_name} entries must resolve inside artifact_inputs: {', '.join(missing)}",
                )
            )


def validate_trace_eval_bridge_surfaces(
    repo_root: Path,
    records: Sequence[Any],
    *,
    context: RuntimeAuditContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    schema_path = repo_root / ARTIFACT_VERDICT_HOOK_SCHEMA_PATH
    schema_location = relative_location(schema_path, repo_root)
    schema = load_json_payload(schema_path, issues, root=repo_root)
    if schema is None:
        return issues
    if not validate_inline_schema(schema, location=schema_location, issues=issues):
        return issues
    schema_validator = Draft202012Validator(schema)

    playbooks_by_id: dict[str, dict[str, Any]] | None = None
    if context.strict_sibling_compat_checks_enabled() and not context.aoa_playbooks_root.exists():
        issues.append(
            ValidationIssue(
                relative_location(context.aoa_playbooks_root, repo_root),
                "strict sibling compatibility requires available aoa-playbooks root",
            )
        )
    elif context.strict_sibling_compat_checks_enabled():
        playbook_registry_path = context.aoa_playbooks_root / "generated" / "playbook_registry.min.json"
        playbook_registry_location = relative_location(playbook_registry_path, repo_root)
        playbook_registry = load_json_payload(playbook_registry_path, issues, root=repo_root)
        playbooks_by_id = load_mapping_entries(
            playbook_registry,
            array_key="playbooks",
            key_name="id",
            location=playbook_registry_location,
            issues=issues,
        )

    eval_catalog_path = repo_root / "generated" / "eval_catalog.min.json"
    eval_catalog_location = relative_location(eval_catalog_path, repo_root)
    eval_catalog = load_json_payload(eval_catalog_path, issues, root=repo_root)
    evals_by_name = load_mapping_entries(
        eval_catalog,
        array_key="evals",
        key_name="name",
        location=eval_catalog_location,
        issues=issues,
    )

    records_by_name = {
        getattr(record, "name"): record
        for record in records
        if isinstance(getattr(record, "name", None), str)
    }

    for playbook_id, example_name in ARTIFACT_VERDICT_HOOK_EXAMPLES.items():
        example_path = repo_root / example_name
        location = relative_location(example_path, repo_root)
        payload = load_json_payload(example_path, issues, root=repo_root)
        if payload is None:
            continue
        if not isinstance(payload, dict):
            issues.append(ValidationIssue(location, "example payload must be an object"))
            continue

        validate_against_schema(
            payload,
            location=location,
            issues=issues,
            validator=schema_validator,
        )

        if payload.get("playbook_id") != playbook_id:
            issues.append(ValidationIssue(location, f"playbook_id must be '{playbook_id}'"))

        expected_hook = TRACE_EVAL_HOOK_EXPECTATIONS[playbook_id]
        if payload.get("eval_anchor") != expected_hook["eval_anchor"]:
            issues.append(
                ValidationIssue(
                    location,
                    f"eval_anchor must be '{expected_hook['eval_anchor']}' for {playbook_id}",
                )
            )

        _validate_runtime_policy_boundary(
            location=location,
            playbook_id=playbook_id,
            payload=payload,
            issues=issues,
        )

        eval_anchor = payload.get("eval_anchor")
        if not isinstance(eval_anchor, str):
            continue
        catalog_entry = evals_by_name.get(eval_anchor)
        if catalog_entry is None:
            issues.append(
                ValidationIssue(
                    location,
                    f"eval_anchor '{eval_anchor}' does not resolve in generated/eval_catalog.min.json",
                )
            )
            continue

        playbook_entry = playbooks_by_id.get(playbook_id) if playbooks_by_id is not None else None
        if playbooks_by_id is not None:
            if playbook_entry is None:
                issues.append(
                    ValidationIssue(location, f"playbook_id '{playbook_id}' does not resolve in aoa-playbooks")
                )
                continue

            playbook_eval_anchors = playbook_entry.get("eval_anchors")
            if not isinstance(playbook_eval_anchors, list) or eval_anchor not in playbook_eval_anchors:
                issues.append(
                    ValidationIssue(
                        location,
                        f"eval_anchor '{eval_anchor}' is not present in aoa-playbooks eval_anchors for {playbook_id}",
                    )
                )

            expected_artifacts = playbook_entry.get("expected_artifacts")
            if payload.get("artifact_inputs") != expected_artifacts:
                issues.append(
                    ValidationIssue(
                        location,
                        "artifact_inputs must exactly match aoa-playbooks expected_artifacts",
                    )
                )
            if not isinstance(expected_artifacts, list) or payload.get("verification_surface") not in expected_artifacts:
                issues.append(
                    ValidationIssue(
                        location,
                        "verification_surface must resolve inside the playbook artifact input set",
                    )
                )

        if payload.get("artifact_contract_refs") != expected_hook["artifact_contract_refs"]:
            issues.append(
                ValidationIssue(
                    location,
                    "artifact_contract_refs do not match the bounded cross-repo contract refs for this hook",
                )
            )

        if payload.get("trace_surfaces") != expected_hook["trace_surfaces"]:
            issues.append(
                ValidationIssue(
                    location,
                    "trace_surfaces do not match the bounded sidecar posture for this hook",
                )
            )

        if payload.get("verification_surface") != expected_hook["verification_surface"]:
            issues.append(
                ValidationIssue(
                    location,
                    f"verification_surface must be '{expected_hook['verification_surface']}'",
                )
            )

        expected_bundle_ref = f"repo:aoa-evals/{catalog_entry.get('eval_path')}"
        if payload.get("verdict_bundle_ref") != expected_bundle_ref:
            issues.append(
                ValidationIssue(
                    location,
                    f"verdict_bundle_ref must equal '{expected_bundle_ref}'",
                )
            )

        verdict_bundle_resolution = context.parse_repo_ref(
            payload.get("verdict_bundle_ref"),
            location=f"{location}.verdict_bundle_ref",
            issues=issues,
        )
        if verdict_bundle_resolution is not None:
            _repo_name, verdict_bundle_path, _anchor = verdict_bundle_resolution
            expected_bundle_path = repo_root / str(catalog_entry.get("eval_path"))
            if verdict_bundle_path != expected_bundle_path:
                issues.append(
                    ValidationIssue(
                        location,
                        "verdict_bundle_ref must resolve to the selected eval anchor bundle path",
                    )
                )

        record = records_by_name.get(eval_anchor)
        if record is None:
            issues.append(
                ValidationIssue(
                    location,
                    f"eval anchor '{eval_anchor}' does not resolve to a local bundle record",
                )
            )
            continue

        record_manifest = getattr(record, "manifest", {})
        expected_report_expectation = {
            "report_format": record_manifest.get("report_format"),
            "verdict_shape": record_manifest.get("verdict_shape"),
            "review_required": record_manifest.get("review_required"),
        }
        if payload.get("report_expectation") != expected_report_expectation:
            issues.append(
                ValidationIssue(
                    location,
                    "report_expectation must exactly match the selected eval bundle manifest",
                )
            )

        resolved_contract_test_refs: set[str] = set()
        contract_test_refs = payload.get("contract_test_refs")
        if not isinstance(contract_test_refs, list):
            issues.append(ValidationIssue(f"{location}.contract_test_refs", "contract_test_refs must be a list"))
        else:
            for index, ref in enumerate(contract_test_refs):
                resolution = context.parse_repo_ref(
                    ref,
                    location=f"{location}.contract_test_refs[{index}]",
                    issues=issues,
                )
                if resolution is None:
                    continue
                repo_name, target_path, _anchor = resolution
                resolved_contract_test_refs.add(
                    f"repo:{repo_name}/{target_path.relative_to(context.repo_ref_roots[repo_name]).as_posix()}"
                )
        if resolved_contract_test_refs and resolved_contract_test_refs != expected_contract_test_refs(record, repo_root):
            issues.append(
                ValidationIssue(
                    location,
                    "contract_test_refs must resolve to the selected bundle's integrity check and support note",
                )
            )

        for field_name in ("artifact_contract_refs", "trace_surfaces"):
            refs = payload.get(field_name)
            if not isinstance(refs, list):
                issues.append(ValidationIssue(f"{location}.{field_name}", f"{field_name} must be a list"))
                continue
            for index, ref in enumerate(refs):
                context.parse_repo_ref(
                    ref,
                    location=f"{location}.{field_name}[{index}]",
                    issues=issues,
                )

    return issues
