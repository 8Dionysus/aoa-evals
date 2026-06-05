"""Runtime evidence selection packet validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from jsonschema import Draft202012Validator

from validators.common import (
    ValidationIssue,
    load_json_payload,
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
        "source_schema_ref": "repo:abyss-stack/mechanics/governed-execution/parts/candidate-exports/schemas/runtime-memo-export-candidate.schema.json",
        "candidate_eval_refs": ["candidate:aoa-memo-recall-integrity"],
    },
    "runtime_evidence_selection.phase-alpha-memo-contradiction-gap.example.json": {
        "target_eval": "aoa-memo-contradiction-integrity",
        "source_schema_ref": "repo:abyss-stack/mechanics/governed-execution/parts/candidate-exports/schemas/runtime-memo-export-candidate.schema.json",
        "candidate_eval_refs": ["candidate:aoa-memo-contradiction-integrity"],
    },
    "runtime_evidence_selection.phase-alpha-memo-contradiction-rerun.example.json": {
        "target_eval": "aoa-memo-contradiction-integrity",
        "source_schema_ref": "repo:abyss-stack/mechanics/governed-execution/parts/candidate-exports/schemas/runtime-memo-export-candidate.schema.json",
        "candidate_eval_refs": ["candidate:aoa-memo-contradiction-integrity"],
    },
    "runtime_evidence_selection.phase-alpha-memo-writeback-act.example.json": {
        "target_eval": "aoa-memo-writeback-act-integrity",
        "source_schema_ref": "repo:abyss-stack/mechanics/governed-execution/parts/candidate-exports/schemas/runtime-memo-export-candidate.schema.json",
        "candidate_eval_refs": ["candidate:aoa-memo-writeback-act-integrity"],
    },
    "runtime_evidence_selection.runtime-chaos-window.example.json": {
        "target_eval": "aoa-stress-recovery-window",
        "source_schema_ref": "repo:abyss-stack/mechanics/runtime-repair/parts/degradation-receipts/schemas/service-degradation-receipt.schema.json",
        "candidate_eval_refs": ["candidate:aoa-stress-recovery-window"],
        "allowed_ref_roots": ["mechanics"],
    },
}


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

    return issues
