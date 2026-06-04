"""Runtime audit behavior validators for candidate evidence boundaries."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from jsonschema import Draft202012Validator

from validators import artifact_hooks
from validators.common import (
    ValidationIssue,
    load_mapping_entries,
    load_json_payload,
    read_text_or_issue,
    relative_location,
    validate_against_schema,
    validate_inline_schema,
)


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
TRACE_EVAL_HOOK_EXPECTATIONS = artifact_hooks.TRACE_EVAL_HOOK_EXPECTATIONS
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
RUNTIME_INTEGRITY_REVIEW_DOC_NAME = "mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md"
RUNTIME_INTEGRITY_REVIEW_SCHEMA_NAME = "runtime-integrity-review.schema.json"
RUNTIME_INTEGRITY_REVIEW_SCHEMA_PATH = (
    "mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json"
)
RUNTIME_INTEGRITY_REVIEW_EXAMPLE_NAME = (
    "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json"
)
RUNTIME_INTEGRITY_REVIEW_BUDGET_REF = (
    "Agents-of-Abyss:mechanics/experience/parts/continuity-context/CONTRACT.md#stronger-owner-split"
)
RUNTIME_INTEGRITY_REVIEW_REQUIRED_TOKENS = (
    "`candidate_only`",
    "`human_review_needed`",
    "`budget_ref`",
    "`evidence_refs`",
    "`replay_requirements`",
    "`forbidden_claims`",
    "`sealed_verdict`",
    "`activation_authority`",
    "`owner_override`",
    "`canon_write`",
    "Proof-canon pressure routes to bundle-local proof review.",
    "Runtime-continuity activation pressure routes to Experience and runtime-owner",
)
RUNTIME_INTEGRITY_REVIEW_LANDING_TOKENS = (
    "mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md",
    "mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json",
    "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json",
    "`candidate_only`",
    "`human_review_needed`",
)
RUNTIME_INTEGRITY_REVIEW_EVIDENCE_REFS = (
    "repo:aoa-evals/mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md",
    "repo:aoa-evals/mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md",
    "repo:aoa-routing/docs/LIVE_SESSION_REENTRY_ROUTE_REVIEW.md",
    "repo:aoa-agents/mechanics/checkpoint/parts/continuity-lane/docs/self-agency-continuity-lane.md",
    "repo:aoa-memo/mechanics/checkpoint/parts/checkpoint-carry-contract/schemas/inquiry_checkpoint.schema.json",
    "repo:aoa-memo/mechanics/writeback/docs/SELF_AGENCY_CONTINUITY_WRITEBACK.md",
)
RUNTIME_INTEGRITY_REVIEW_REPLAY_KEYS = (
    "selected_evidence_only",
    "owner_local_replay_required",
    "fail_closed",
    "publication_requires_review",
)
RUNTIME_INTEGRITY_REVIEW_FORBIDDEN_CLAIMS = (
    "sealed_verdict",
    "activation_authority",
    "owner_override",
    "canon_write",
)


@dataclass(frozen=True)
class RuntimeAuditContext:
    agents_of_abyss_root: Path
    abyss_stack_root: Path
    aoa_playbooks_root: Path
    repo_ref_roots: Mapping[str, Path]
    strict_sibling_compat_checks_enabled: Callable[[], bool]
    parse_repo_ref: Callable[..., tuple[str, Path, str | None] | None]
    parse_named_surface_ref: Callable[..., tuple[Path, str | None] | None]
    validate_abyss_stack_ref: Callable[..., Any]


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
            issues.append(
                ValidationIssue(location, f"playbook_id must be '{playbook_id}'")
            )

        expected_hook = TRACE_EVAL_HOOK_EXPECTATIONS[playbook_id]
        if payload.get("eval_anchor") != expected_hook["eval_anchor"]:
            issues.append(
                ValidationIssue(
                    location,
                    f"eval_anchor must be '{expected_hook['eval_anchor']}' for {playbook_id}",
                )
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
            issues.append(
                ValidationIssue(f"{location}.contract_test_refs", "contract_test_refs must be a list")
            )
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
                issues.append(
                    ValidationIssue(f"{location}.{field_name}", f"{field_name} must be a list")
                )
                continue
            for index, ref in enumerate(refs):
                context.parse_repo_ref(
                    ref,
                    location=f"{location}.{field_name}[{index}]",
                    issues=issues,
                )

    return issues


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
            issues.append(
                ValidationIssue(
                    location,
                    f"source_schema_ref must equal '{expected_schema_ref}'",
                )
            )

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
            issues.append(
                ValidationIssue(f"{location}.selected_evidence", "selected_evidence must be a list")
            )
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


def validate_runtime_integrity_review_surface(
    repo_root: Path,
    *,
    context: RuntimeAuditContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    doc_path = repo_root / RUNTIME_INTEGRITY_REVIEW_DOC_NAME
    docs_map_path = repo_root / "docs" / "README.md"
    landing_path = repo_root / "mechanics" / "agon" / "legacy" / "raw" / "AGON_WAVE10_EVAL_LANDING.md"
    schema_path = repo_root / RUNTIME_INTEGRITY_REVIEW_SCHEMA_PATH
    example_path = repo_root / RUNTIME_INTEGRITY_REVIEW_EXAMPLE_NAME

    doc_text = read_text_or_issue(doc_path, issues, root=repo_root)
    if doc_text:
        for token in RUNTIME_INTEGRITY_REVIEW_REQUIRED_TOKENS:
            if token not in doc_text:
                issues.append(
                    ValidationIssue(
                        relative_location(doc_path, repo_root),
                        f"runtime integrity review guide must mention '{token}'",
                    )
                )

    read_text_or_issue(docs_map_path, issues, root=repo_root)

    landing_text = read_text_or_issue(landing_path, issues, root=repo_root)
    if landing_text:
        for token in RUNTIME_INTEGRITY_REVIEW_LANDING_TOKENS:
            if token not in landing_text:
                issues.append(
                    ValidationIssue(
                        relative_location(landing_path, repo_root),
                        f"Agon Wave X landing note must mention '{token}'",
                    )
                )

    schema = load_json_payload(schema_path, issues, root=repo_root)
    if schema is None:
        return issues
    schema_location = relative_location(schema_path, repo_root)
    if not validate_inline_schema(schema, location=schema_location, issues=issues):
        return issues
    if schema.get("title") != "aoa-evals runtime integrity review":
        issues.append(
            ValidationIssue(
                schema_location,
                "runtime integrity review schema title must be 'aoa-evals runtime integrity review'",
            )
        )
    if schema.get("additionalProperties") is not False:
        issues.append(
            ValidationIssue(
                schema_location,
                "runtime integrity review schema must keep top-level additionalProperties set to false",
            )
        )
    required_fields = schema.get("required")
    expected_required_fields = {
        "schema_version",
        "owner_repo",
        "surface_kind",
        "status",
        "budget_ref",
        "evidence_refs",
        "replay_requirements",
        "human_review_needed",
        "forbidden_claims",
        "notes",
    }
    if not isinstance(required_fields, list) or set(required_fields) != expected_required_fields:
        issues.append(
            ValidationIssue(
                schema_location,
                "runtime integrity review schema must require the full owner-local contract field set",
            )
        )
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        issues.append(
            ValidationIssue(
                schema_location,
                "runtime integrity review schema must define object properties",
            )
        )
    else:
        const_fields = {
            "schema_version": "runtime_integrity_review_v1",
            "owner_repo": "aoa-evals",
            "surface_kind": "runtime_integrity_review",
            "status": "candidate_only",
            "budget_ref": RUNTIME_INTEGRITY_REVIEW_BUDGET_REF,
            "human_review_needed": True,
        }
        for field_name, expected_value in const_fields.items():
            field_schema = properties.get(field_name)
            if not isinstance(field_schema, dict) or field_schema.get("const") != expected_value:
                issues.append(
                    ValidationIssue(
                        schema_location,
                        f"runtime integrity review schema must keep '{field_name}' bound to its owner-local constant",
                    )
                )

        evidence_schema = properties.get("evidence_refs")
        if (
            not isinstance(evidence_schema, dict)
            or evidence_schema.get("type") != "array"
            or evidence_schema.get("uniqueItems") is not True
            or evidence_schema.get("minItems") != len(RUNTIME_INTEGRITY_REVIEW_EVIDENCE_REFS)
            or evidence_schema.get("maxItems") != len(RUNTIME_INTEGRITY_REVIEW_EVIDENCE_REFS)
        ):
            issues.append(
                ValidationIssue(
                    schema_location,
                    "runtime integrity review schema must keep evidence_refs as an exact-count unique repo-ref array",
                )
            )
        else:
            evidence_items = evidence_schema.get("items")
            if (
                not isinstance(evidence_items, dict)
                or evidence_items.get("type") != "string"
                or evidence_items.get("pattern") != r"^repo:[^\s]+/.+$"
            ):
                issues.append(
                    ValidationIssue(
                        schema_location,
                        "runtime integrity review schema must keep evidence_refs items constrained to repo-qualified refs",
                    )
                )

        replay_schema = properties.get("replay_requirements")
        if (
            not isinstance(replay_schema, dict)
            or replay_schema.get("type") != "object"
            or replay_schema.get("additionalProperties") is not False
        ):
            issues.append(
                ValidationIssue(
                    schema_location,
                    "runtime integrity review schema must keep replay_requirements as a closed object",
                )
            )
        else:
            replay_required = replay_schema.get("required")
            if not isinstance(replay_required, list) or set(replay_required) != set(
                RUNTIME_INTEGRITY_REVIEW_REPLAY_KEYS
            ):
                issues.append(
                    ValidationIssue(
                        schema_location,
                        "runtime integrity review schema must require the full replay_requirements key set",
                    )
                )
            replay_properties = replay_schema.get("properties")
            if not isinstance(replay_properties, dict):
                issues.append(
                    ValidationIssue(
                        schema_location,
                        "runtime integrity review schema must define replay_requirements properties",
                    )
                )
            else:
                for field_name in RUNTIME_INTEGRITY_REVIEW_REPLAY_KEYS:
                    field_schema = replay_properties.get(field_name)
                    if not isinstance(field_schema, dict) or field_schema.get("const") is not True:
                        issues.append(
                            ValidationIssue(
                                schema_location,
                                f"runtime integrity review schema must keep replay_requirements.{field_name} bound to true",
                            )
                        )

        forbidden_schema = properties.get("forbidden_claims")
        if (
            not isinstance(forbidden_schema, dict)
            or forbidden_schema.get("type") != "array"
            or forbidden_schema.get("uniqueItems") is not True
            or forbidden_schema.get("minItems") != len(RUNTIME_INTEGRITY_REVIEW_FORBIDDEN_CLAIMS)
            or forbidden_schema.get("maxItems") != len(RUNTIME_INTEGRITY_REVIEW_FORBIDDEN_CLAIMS)
        ):
            issues.append(
                ValidationIssue(
                    schema_location,
                    "runtime integrity review schema must keep forbidden_claims as an exact-count unique array",
                )
            )
        else:
            forbidden_items = forbidden_schema.get("items")
            forbidden_enum = forbidden_items.get("enum") if isinstance(forbidden_items, dict) else None
            if not isinstance(forbidden_enum, list) or set(forbidden_enum) != set(
                RUNTIME_INTEGRITY_REVIEW_FORBIDDEN_CLAIMS
            ):
                issues.append(
                    ValidationIssue(
                        schema_location,
                        "runtime integrity review schema must keep forbidden_claims bound to the no-authority guard set",
                    )
                )

        notes_schema = properties.get("notes")
        if (
            not isinstance(notes_schema, dict)
            or notes_schema.get("type") != "string"
            or notes_schema.get("minLength") != 1
        ):
            issues.append(
                ValidationIssue(
                    schema_location,
                    "runtime integrity review schema must keep notes as a non-empty string",
                )
            )
    schema_validator = Draft202012Validator(schema)

    payload = load_json_payload(example_path, issues, root=repo_root)
    if payload is None:
        return issues
    location = relative_location(example_path, repo_root)
    if not isinstance(payload, dict):
        issues.append(ValidationIssue(location, "runtime integrity review example must be an object"))
        return issues

    validate_against_schema(
        payload,
        location=location,
        issues=issues,
        validator=schema_validator,
    )

    if payload.get("schema_version") != "runtime_integrity_review_v1":
        issues.append(
            ValidationIssue(
                location,
                "runtime integrity review example schema_version must be 'runtime_integrity_review_v1'",
            )
        )
    if payload.get("owner_repo") != "aoa-evals":
        issues.append(ValidationIssue(location, "owner_repo must remain aoa-evals"))
    if payload.get("surface_kind") != "runtime_integrity_review":
        issues.append(ValidationIssue(location, "surface_kind must remain runtime_integrity_review"))
    if payload.get("status") != "candidate_only":
        issues.append(ValidationIssue(location, "status must remain candidate_only"))

    if payload.get("budget_ref") != RUNTIME_INTEGRITY_REVIEW_BUDGET_REF:
        issues.append(
            ValidationIssue(
                location,
                "budget_ref must stay bound to the Experience continuity-context owner split surface",
            )
        )
    else:
        context.parse_named_surface_ref(
            payload.get("budget_ref"),
            prefix_name="Agents-of-Abyss",
            repo_root=context.agents_of_abyss_root,
            location=f"{location}.budget_ref",
            issues=issues,
        )

    evidence_refs = payload.get("evidence_refs")
    resolved_evidence_refs: set[str] = set()
    if not isinstance(evidence_refs, list):
        issues.append(ValidationIssue(f"{location}.evidence_refs", "evidence_refs must be a list"))
    else:
        for index, ref in enumerate(evidence_refs):
            resolution = context.parse_repo_ref(
                ref,
                location=f"{location}.evidence_refs[{index}]",
                issues=issues,
            )
            if resolution is None:
                continue
            repo_name, target_path, anchor = resolution
            normalized_ref = f"repo:{repo_name}/{target_path.relative_to(context.repo_ref_roots[repo_name]).as_posix()}"
            if anchor:
                normalized_ref = f"{normalized_ref}#{anchor}"
            resolved_evidence_refs.add(normalized_ref)
        if resolved_evidence_refs and resolved_evidence_refs != set(RUNTIME_INTEGRITY_REVIEW_EVIDENCE_REFS):
            issues.append(
                ValidationIssue(
                    location,
                    "evidence_refs must resolve to the bounded W10 runtime integrity review surfaces",
                )
            )

    expected_replay_requirements = {field_name: True for field_name in RUNTIME_INTEGRITY_REVIEW_REPLAY_KEYS}
    if payload.get("replay_requirements") != expected_replay_requirements:
        issues.append(
            ValidationIssue(
                location,
                "replay_requirements must keep selected-evidence, owner-local replay, fail-closed, and review-required posture",
            )
        )

    if payload.get("human_review_needed") is not True:
        issues.append(ValidationIssue(location, "human_review_needed must remain true"))

    forbidden_claims = payload.get("forbidden_claims")
    if not isinstance(forbidden_claims, list):
        issues.append(
            ValidationIssue(
                f"{location}.forbidden_claims",
                "forbidden_claims must be a list",
            )
        )
    elif set(forbidden_claims) != set(RUNTIME_INTEGRITY_REVIEW_FORBIDDEN_CLAIMS):
        issues.append(
            ValidationIssue(
                location,
                "forbidden_claims must exactly preserve the bounded no-authority guard",
            )
        )

    notes = payload.get("notes")
    if not isinstance(notes, str) or "Candidate only." not in notes:
        issues.append(
            ValidationIssue(
                location,
                "runtime integrity review example notes must keep candidate-only posture explicit",
            )
        )
    elif "activation pressure to Experience or runtime-owner gates" not in notes:
        issues.append(
            ValidationIssue(
                location,
                "runtime integrity review example notes must keep activation routing explicit",
            )
        )

    return issues
