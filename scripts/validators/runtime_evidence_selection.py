"""Runtime evidence selection packet validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from jsonschema import Draft202012Validator

from validators.common import (
    ValidationIssue,
    load_json_payload,
    read_text_or_issue,
    relative_location,
    validate_against_schema,
    validate_inline_schema,
)
from validators.runtime_audit_common import RuntimeAuditContext

RUNTIME_EVIDENCE_SELECTION_SCHEMA_NAME = "runtime-evidence-selection.schema.json"
RUNTIME_EVIDENCE_SELECTION_SCHEMA_PATH = (
    "mechanics/audit/parts/selected-evidence-packets/schemas/runtime-evidence-selection.schema.json"
)
RUNTIME_EVIDENCE_SELECTION_EXAMPLES_DIR = "mechanics/audit/parts/selected-evidence-packets/examples"
TRACE_EVAL_BRIDGE_CHAOS_DOC_NAME = (
    "mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE_CHAOS_WAVE1.md"
)
TRACE_INTEGRITY_CHAOS_HOOK_NAME = (
    "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.trace-integrity-chaos.example.json"
)
MEMORY_CONTEXT_SOURCE_SCHEMA_REF = (
    "repo:abyss-stack/mechanics/governed-execution/parts/candidate-exports/schemas/"
    "runtime-memo-export-candidate.schema.json"
)
MEMORY_CONTEXT_BOUNDARY_OWNER = "aoa-memo"
MEMORY_CONTEXT_BOUNDARY_CONSUMER_POSTURE = "candidate_context_only_not_memory_authority"
MEMORY_CONTEXT_BOUNDARY_REF_FIELDS = (
    "provenance_refs",
    "freshness_refs",
    "retention_refs",
    "permission_refs",
)
MEMORY_CONTEXT_BOUNDARY_STOP_LINES = (
    "does not authorize tool use",
    "does not authorize durable memory writeback",
    "does not settle source truth",
    "does not convert stale or private context into proof",
    "does not create a local memo port",
)
RUNTIME_EVIDENCE_SELECTION_EXAMPLES: dict[str, dict[str, Any]] = {
    "runtime_evidence_selection.workhorse-local.example.json": {
        "target_eval": None,
        "source_schema_ref": "repo:abyss-stack/mechanics/inference-pilots/parts/local-trials/schemas/runtime-benchmark.schema.json",
        "candidate_eval_refs": ["candidate:fixed-baseline-runtime-latency-tradeoff"],
    },
    "runtime_evidence_selection.return-anchor-integrity.example.json": {
        "target_eval": "aoa-return-anchor-integrity",
        "source_schema_ref": "repo:abyss-stack/mechanics/governed-execution/parts/return-policy/schemas/runtime-return-event.schema.json",
        "candidate_eval_refs": ["candidate:aoa-return-anchor-integrity"],
    },
    "runtime_evidence_selection.phase-alpha-memo-recall-rerun.example.json": {
        "target_eval": "aoa-memo-recall-integrity",
        "source_schema_ref": MEMORY_CONTEXT_SOURCE_SCHEMA_REF,
        "candidate_eval_refs": ["candidate:aoa-memo-recall-integrity"],
        "memory_context_allowed_influence": "memo recall context for bundle-local review",
    },
    "runtime_evidence_selection.phase-alpha-memo-contradiction-gap.example.json": {
        "target_eval": "aoa-memo-contradiction-integrity",
        "source_schema_ref": MEMORY_CONTEXT_SOURCE_SCHEMA_REF,
        "candidate_eval_refs": ["candidate:aoa-memo-contradiction-integrity"],
        "memory_context_allowed_influence": "memo contradiction context for bundle-local review",
    },
    "runtime_evidence_selection.phase-alpha-memo-contradiction-rerun.example.json": {
        "target_eval": "aoa-memo-contradiction-integrity",
        "source_schema_ref": MEMORY_CONTEXT_SOURCE_SCHEMA_REF,
        "candidate_eval_refs": ["candidate:aoa-memo-contradiction-integrity"],
        "memory_context_allowed_influence": "memo contradiction context for bundle-local review",
    },
    "runtime_evidence_selection.phase-alpha-memo-writeback-act.example.json": {
        "target_eval": "aoa-memo-writeback-act-integrity",
        "source_schema_ref": MEMORY_CONTEXT_SOURCE_SCHEMA_REF,
        "candidate_eval_refs": ["candidate:aoa-memo-writeback-act-integrity"],
        "memory_context_allowed_influence": "memo writeback context for bundle-local review",
    },
    "runtime_evidence_selection.runtime-chaos-window.example.json": {
        "target_eval": "aoa-stress-recovery-window",
        "source_schema_ref": "repo:abyss-stack/mechanics/runtime-repair/parts/degradation-receipts/schemas/service-degradation-receipt.schema.json",
        "candidate_eval_refs": ["candidate:aoa-stress-recovery-window"],
        "allowed_ref_roots": ["mechanics"],
        "required_bounded_claim_tokens": [
            "operator-visible containment",
            "blocked repair fan-out",
            "explicit degraded continuation",
            "reviewed closeout posture",
            "recovery-legibility evidence only",
        ],
        "required_environment_invariant_tokens": [
            "same bounded runtime owner repo: abyss-stack",
            "selected evidence only, no raw live logs or rendered config snapshots",
            "reviewed closeout remains required before stronger claims",
        ],
        "required_do_not_overread_tokens": [
            "does not prove global runtime health",
            "does not replace an eval verdict",
            "does not turn example packets into live operations truth",
        ],
        "required_evidence_roles": [
            "summary",
            "case-breakdown",
            "environment-note",
            "integrity-sidecar",
        ],
        "required_artifact_ref_fragments": [
            "degradation-receipts/examples/service-degradation-receipt.",
            "repair-safe-closeout/examples/repair-safe-closeout-receipt.",
        ],
        "paired_trace_hook": {
            "path": TRACE_INTEGRITY_CHAOS_HOOK_NAME,
            "hook_id": "trace-integrity-chaos",
            "playbook_id": "AOA-P-0032",
            "eval_anchor": "aoa-witness-trace-integrity",
            "verification_surface": "proof_handoff_candidate",
            "required_contract_refs": [
                "repo:abyss-stack/mechanics/runtime-repair/parts/degradation-receipts/schemas/service-degradation-receipt.schema.json",
                "repo:aoa-memo/mechanics/recurrence-support/docs/WITNESS_TRACE_CONTRACT.md",
            ],
        },
        "bridge_doc": {
            "path": TRACE_EVAL_BRIDGE_CHAOS_DOC_NAME,
            "required_tokens": [
                "../examples/artifact_to_verdict_hook.trace-integrity-chaos.example.json",
                "../../selected-evidence-packets/examples/runtime_evidence_selection.runtime-chaos-window.example.json",
                "weaker sidecar evidence",
                "Live-log publication pressure stays with the runtime owner",
                "health pressure routes to runtime review",
                "Runtime-judge pressure routes to the runtime owner",
            ],
        },
    },
}


def _require_string_tokens(
    *,
    location: str,
    value: Any,
    field_name: str,
    tokens: Sequence[str],
    issues: list[ValidationIssue],
) -> None:
    if not isinstance(value, str):
        issues.append(ValidationIssue(f"{location}.{field_name}", f"{field_name} must be a string"))
        return
    for token in tokens:
        if token not in value:
            issues.append(ValidationIssue(location, f"{field_name} must mention '{token}'"))


def _require_list_tokens(
    *,
    location: str,
    value: Any,
    field_name: str,
    tokens: Sequence[str],
    issues: list[ValidationIssue],
) -> None:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        issues.append(ValidationIssue(f"{location}.{field_name}", f"{field_name} must be a string list"))
        return
    joined = "\n".join(value)
    for token in tokens:
        if token not in joined:
            issues.append(ValidationIssue(location, f"{field_name} must mention '{token}'"))


def _validate_runtime_degradation_pairing(
    *,
    repo_root: Path,
    location: str,
    payload: dict[str, Any],
    expectations: dict[str, Any],
    issues: list[ValidationIssue],
) -> None:
    _require_string_tokens(
        location=location,
        value=payload.get("bounded_claim"),
        field_name="bounded_claim",
        tokens=expectations.get("required_bounded_claim_tokens", ()),
        issues=issues,
    )
    _require_list_tokens(
        location=location,
        value=payload.get("environment_invariants"),
        field_name="environment_invariants",
        tokens=expectations.get("required_environment_invariant_tokens", ()),
        issues=issues,
    )
    _require_list_tokens(
        location=location,
        value=payload.get("do_not_overread"),
        field_name="do_not_overread",
        tokens=expectations.get("required_do_not_overread_tokens", ()),
        issues=issues,
    )

    selected_evidence = payload.get("selected_evidence")
    if isinstance(selected_evidence, list):
        roles = [
            item.get("evidence_role")
            for item in selected_evidence
            if isinstance(item, dict)
        ]
        for role in expectations.get("required_evidence_roles", ()):
            if role not in roles:
                issues.append(ValidationIssue(location, f"selected_evidence must include '{role}' evidence_role"))
        if any(isinstance(item, dict) and item.get("summary_only") is not True for item in selected_evidence):
            issues.append(ValidationIssue(location, "runtime degradation selected_evidence entries must stay summary_only"))
        artifact_refs = [
            item.get("artifact_ref")
            for item in selected_evidence
            if isinstance(item, dict) and isinstance(item.get("artifact_ref"), str)
        ]
        for fragment in expectations.get("required_artifact_ref_fragments", ()):
            if not any(fragment in ref for ref in artifact_refs):
                issues.append(ValidationIssue(location, f"selected_evidence artifact refs must include '{fragment}'"))

    paired_hook = expectations.get("paired_trace_hook")
    if isinstance(paired_hook, dict):
        hook_path_name = paired_hook.get("path")
        if isinstance(hook_path_name, str):
            hook_path = repo_root / hook_path_name
            hook_location = relative_location(hook_path, repo_root)
            hook_payload = load_json_payload(hook_path, issues, root=repo_root)
            if isinstance(hook_payload, dict):
                for field_name in ("hook_id", "playbook_id", "eval_anchor", "verification_surface"):
                    expected_value = paired_hook.get(field_name)
                    if hook_payload.get(field_name) != expected_value:
                        issues.append(
                            ValidationIssue(
                                hook_location,
                                f"{field_name} must equal '{expected_value}' for runtime degradation pairing",
                            )
                        )
                contract_refs = hook_payload.get("artifact_contract_refs")
                if not isinstance(contract_refs, list):
                    issues.append(ValidationIssue(f"{hook_location}.artifact_contract_refs", "artifact_contract_refs must be a list"))
                else:
                    for required_ref in paired_hook.get("required_contract_refs", ()):
                        if required_ref not in contract_refs:
                            issues.append(
                                ValidationIssue(
                                    hook_location,
                                    f"artifact_contract_refs must include '{required_ref}'",
                                )
                            )

    bridge_doc = expectations.get("bridge_doc")
    if isinstance(bridge_doc, dict):
        doc_path_name = bridge_doc.get("path")
        if isinstance(doc_path_name, str):
            doc_path = repo_root / doc_path_name
            doc_text = read_text_or_issue(doc_path, issues, root=repo_root)
            doc_location = relative_location(doc_path, repo_root)
            for token in bridge_doc.get("required_tokens", ()):
                if token not in doc_text:
                    issues.append(ValidationIssue(doc_location, f"bridge doc must mention '{token}'"))


def _is_memory_context_candidate(payload: dict[str, Any]) -> bool:
    target_eval = payload.get("target_eval")
    selection_id = payload.get("selection_id")
    return (
        payload.get("source_schema_ref") == MEMORY_CONTEXT_SOURCE_SCHEMA_REF
        or (isinstance(target_eval, str) and target_eval.startswith("aoa-memo-"))
        or (isinstance(selection_id, str) and "memo" in selection_id)
    )


def _validate_memory_context_boundary(
    *,
    location: str,
    payload: dict[str, Any],
    expected_influence: str | None,
    context: RuntimeAuditContext,
    issues: list[ValidationIssue],
) -> None:
    boundary = payload.get("memory_context_boundary")
    if not isinstance(boundary, dict):
        issues.append(
            ValidationIssue(
                f"{location}.memory_context_boundary",
                "memory_context_boundary must be present for memo context candidate evidence",
            )
        )
        return

    if payload.get("source_schema_ref") != MEMORY_CONTEXT_SOURCE_SCHEMA_REF:
        issues.append(
            ValidationIssue(
                location,
                f"memo context candidate evidence must use source_schema_ref '{MEMORY_CONTEXT_SOURCE_SCHEMA_REF}'",
            )
        )
    if boundary.get("memory_owner_repo") != MEMORY_CONTEXT_BOUNDARY_OWNER:
        issues.append(
            ValidationIssue(
                f"{location}.memory_context_boundary.memory_owner_repo",
                "memory_owner_repo must equal 'aoa-memo'",
            )
        )
    if boundary.get("consumer_posture") != MEMORY_CONTEXT_BOUNDARY_CONSUMER_POSTURE:
        issues.append(
            ValidationIssue(
                f"{location}.memory_context_boundary.consumer_posture",
                f"consumer_posture must equal '{MEMORY_CONTEXT_BOUNDARY_CONSUMER_POSTURE}'",
            )
        )
    if boundary.get("review_required") is not True:
        issues.append(
            ValidationIssue(
                f"{location}.memory_context_boundary.review_required",
                "memory context candidate evidence must require review",
            )
        )

    allowed_influence = boundary.get("allowed_influence")
    if not isinstance(allowed_influence, list) or not all(isinstance(item, str) for item in allowed_influence):
        issues.append(
            ValidationIssue(
                f"{location}.memory_context_boundary.allowed_influence",
                "allowed_influence must be a string list",
            )
        )
    elif expected_influence is not None and expected_influence not in allowed_influence:
        issues.append(
            ValidationIssue(
                f"{location}.memory_context_boundary.allowed_influence",
                f"allowed_influence must include '{expected_influence}'",
            )
        )

    _require_list_tokens(
        location=f"{location}.memory_context_boundary",
        value=boundary.get("authority_stop_lines"),
        field_name="authority_stop_lines",
        tokens=MEMORY_CONTEXT_BOUNDARY_STOP_LINES,
        issues=issues,
    )

    for field_name in MEMORY_CONTEXT_BOUNDARY_REF_FIELDS:
        refs = boundary.get(field_name)
        if not isinstance(refs, list) or not all(isinstance(item, str) for item in refs):
            issues.append(
                ValidationIssue(
                    f"{location}.memory_context_boundary.{field_name}",
                    f"{field_name} must be a string list",
                )
            )
            continue
        for index, ref in enumerate(refs):
            resolution = context.parse_repo_ref(
                ref,
                location=f"{location}.memory_context_boundary.{field_name}[{index}]",
                issues=issues,
            )
            if resolution is None:
                continue
            repo_name, _target_path, _anchor = resolution
            if repo_name not in {"aoa-evals", "aoa-memo"}:
                issues.append(
                    ValidationIssue(
                        f"{location}.memory_context_boundary.{field_name}[{index}]",
                        "memory context boundary refs must stay in aoa-evals or aoa-memo",
                    )
                )


def validate_runtime_evidence_selection_surfaces(
    repo_root: Path,
    records: Sequence[Any],
    *,
    context: RuntimeAuditContext,
    target_eval_names: set[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    selected_examples: list[tuple[Path, dict[str, Any]]] = []
    for example_name, expectations in RUNTIME_EVIDENCE_SELECTION_EXAMPLES.items():
        target_eval = expectations.get("target_eval")
        example_path = repo_root / RUNTIME_EVIDENCE_SELECTION_EXAMPLES_DIR / example_name
        if target_eval_names is None:
            selected_examples.append((example_path, expectations))
            continue
        if target_eval in target_eval_names:
            selected_examples.append((example_path, expectations))

    if not selected_examples:
        return issues

    schema_path = repo_root / RUNTIME_EVIDENCE_SELECTION_SCHEMA_PATH
    schema_location = relative_location(schema_path, repo_root)
    schema = load_json_payload(schema_path, issues, root=repo_root)
    if schema is None:
        return issues
    if not validate_inline_schema(schema, location=schema_location, issues=issues):
        return issues
    schema_validator = Draft202012Validator(schema)

    record_names = {
        getattr(record, "name")
        for record in records
        if isinstance(getattr(record, "name", None), str)
    }

    for example_path, expectations in selected_examples:
        target_eval = expectations.get("target_eval")
        allowed_ref_roots = tuple(expectations.get("allowed_ref_roots", ["Logs"]))
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

        if target_eval is not None and payload.get("target_eval") != target_eval:
            issues.append(ValidationIssue(location, f"target_eval must equal '{target_eval}'"))

        expected_schema_ref = expectations["source_schema_ref"]
        if payload.get("source_schema_ref") != expected_schema_ref:
            issues.append(ValidationIssue(location, f"source_schema_ref must equal '{expected_schema_ref}'"))

        schema_resolution = context.parse_repo_ref(
            payload.get("source_schema_ref"),
            location=f"{location}.source_schema_ref",
            issues=issues,
        )
        if schema_resolution is not None:
            repo_name, target_path, _anchor = schema_resolution
            if repo_name != "abyss-stack":
                issues.append(
                    ValidationIssue(
                        location,
                        "source_schema_ref must resolve inside abyss-stack tracked schema space",
                    )
                )
            expected_schema_path = context.abyss_stack_root / expected_schema_ref[len("repo:abyss-stack/") :]
            if target_path != expected_schema_path:
                issues.append(
                    ValidationIssue(
                        location,
                        "source_schema_ref must resolve to the expected abyss-stack schema",
                    )
                )

        expected_candidate_eval_refs = expectations["candidate_eval_refs"]
        if payload.get("candidate_eval_refs") != expected_candidate_eval_refs:
            issues.append(
                ValidationIssue(
                    location,
                    f"candidate_eval_refs must equal {expected_candidate_eval_refs!r}",
                )
            )
        elif target_eval is not None and target_eval not in record_names:
            issues.append(
                ValidationIssue(
                    location,
                    f"candidate eval '{target_eval}' does not resolve to a local bundle record",
                )
            )

        for field_name in ("source_manifests", "excluded_artifacts"):
            refs = payload.get(field_name, [])
            if refs is None:
                continue
            if not isinstance(refs, list):
                issues.append(ValidationIssue(f"{location}.{field_name}", f"{field_name} must be a list"))
                continue
            for index, ref in enumerate(refs):
                context.validate_abyss_stack_ref(
                    ref,
                    allowed_roots=allowed_ref_roots,
                    location=f"{location}.{field_name}[{index}]",
                    issues=issues,
                )

        selected_evidence = payload.get("selected_evidence")
        if not isinstance(selected_evidence, list):
            issues.append(ValidationIssue(f"{location}.selected_evidence", "selected_evidence must be a list"))
            continue
        for index, item in enumerate(selected_evidence):
            item_location = f"{location}.selected_evidence[{index}]"
            if not isinstance(item, dict):
                issues.append(ValidationIssue(item_location, "selected evidence entry must be an object"))
                continue
            context.validate_abyss_stack_ref(
                item.get("artifact_ref"),
                allowed_roots=allowed_ref_roots,
                location=f"{item_location}.artifact_ref",
                issues=issues,
            )

        if expectations.get("paired_trace_hook"):
            _validate_runtime_degradation_pairing(
                repo_root=repo_root,
                location=location,
                payload=payload,
                expectations=expectations,
                issues=issues,
            )
        if expectations.get("memory_context_allowed_influence") or _is_memory_context_candidate(payload):
            _validate_memory_context_boundary(
                location=location,
                payload=payload,
                expected_influence=expectations.get("memory_context_allowed_influence"),
                context=context,
                issues=issues,
            )

    return issues
