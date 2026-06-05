from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validate_repo import run_validation
from validators import (
    artifact_hooks,
    readout_contexts,
    root_context,
    runtime_evidence_selection as runtime_evidence_selection_validator,
    runtime_integrity_review_common as runtime_integrity_review_common_validator,
    runtime_integrity_review_docs as runtime_integrity_review_docs_validator,
    runtime_integrity_review_example as runtime_integrity_review_example_validator,
    runtime_integrity_review_schema as runtime_integrity_review_schema_validator,
    runtime_trace_eval_bridge as runtime_trace_eval_bridge_validator,
)
from validators.source_eval_collection import collect_catalog_records
from validate_repo_fixtures import (
    make_abyss_stack_schema,
    make_eval_bundle,
    make_index,
    make_repo_docs,
    make_roadmap,
    make_selection,
    write_catalogs,
)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def copy_repo_text(repo_root: Path, relative_path: str) -> None:
    source = REPO_ROOT / relative_path
    if not source.exists():
        raise FileNotFoundError(source)
    destination = repo_root / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def write_json_payload(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_repo_ref_parser_keeps_sibling_refs_as_boundary_shape_by_default(
    tmp_path: Path,
    monkeypatch,
) -> None:
    issues: list[root_context.ValidationIssue] = []
    sibling_root = tmp_path / "aoa-playbooks"
    sibling_root.mkdir()
    monkeypatch.setattr(root_context, "REPO_REF_ROOTS",
        {
            **root_context.REPO_REF_ROOTS,
            "aoa-playbooks": sibling_root,
        },
    )
    monkeypatch.delenv(root_context.STRICT_SIBLING_COMPAT_ENV, raising=False)

    parsed = root_context.parse_repo_ref(
        "repo:aoa-playbooks/playbooks/moved/PLAYBOOK.md#expected-artifacts",
        location="example.ref",
        issues=issues,
    )

    assert parsed is not None
    assert issues == []


def test_repo_ref_parser_resolves_sibling_refs_in_strict_compat_mode(
    tmp_path: Path,
    monkeypatch,
) -> None:
    issues: list[root_context.ValidationIssue] = []
    sibling_root = tmp_path / "aoa-playbooks"
    sibling_root.mkdir()
    monkeypatch.setattr(root_context, "REPO_REF_ROOTS",
        {
            **root_context.REPO_REF_ROOTS,
            "aoa-playbooks": sibling_root,
        },
    )
    monkeypatch.setenv(root_context.STRICT_SIBLING_COMPAT_ENV, "1")

    parsed = root_context.parse_repo_ref(
        "repo:aoa-playbooks/playbooks/moved/PLAYBOOK.md#expected-artifacts",
        location="example.ref",
        issues=issues,
    )

    assert parsed is None
    assert any("reference target does not exist" in issue.message for issue in issues)


def test_repo_ref_parser_rejects_missing_sibling_root_in_strict_compat_mode(
    tmp_path: Path,
    monkeypatch,
) -> None:
    issues: list[root_context.ValidationIssue] = []
    missing_root = tmp_path / "missing-aoa-playbooks"
    monkeypatch.setattr(root_context, "REPO_REF_ROOTS",
        {
            **root_context.REPO_REF_ROOTS,
            "aoa-playbooks": missing_root,
        },
    )
    monkeypatch.setenv(root_context.STRICT_SIBLING_COMPAT_ENV, "1")

    parsed = root_context.parse_repo_ref(
        "repo:aoa-playbooks/playbooks/current/PLAYBOOK.md#expected-artifacts",
        location="example.ref",
        issues=issues,
    )

    assert parsed is None
    assert any("strict sibling compatibility requires available repo root" in issue.message for issue in issues)


def _write_return_anchor_evidence_surface(tmp_path: Path, *, source_schema_ref: str) -> None:
    make_eval_bundle(tmp_path, name="aoa-starter-alpha")
    make_eval_bundle(tmp_path, name="aoa-return-anchor-integrity")
    make_index(tmp_path, "aoa-starter-alpha", "workflow")
    make_selection(tmp_path, ["aoa-starter-alpha"])
    make_roadmap(tmp_path, ["aoa-starter-alpha"])
    make_repo_docs(tmp_path, starter_names=["aoa-starter-alpha"])
    write_runtime_evidence_selection_example(
        tmp_path,
        filename="runtime_evidence_selection.return-anchor-integrity.example.json",
        source_schema_ref=source_schema_ref,
        candidate_eval_refs=["candidate:aoa-return-anchor-integrity"],
    )
    write_catalogs(tmp_path)


def _set_abyss_stack_ref_roots(monkeypatch, *, repo_root: Path, abyss_stack_root: Path) -> None:
    monkeypatch.setattr(root_context, "ABYSS_STACK_ROOT", abyss_stack_root)
    monkeypatch.setattr(root_context, "REPO_REF_ROOTS",
        {
            "aoa-evals": repo_root,
            "aoa-agents": root_context.AOA_AGENTS_ROOT,
            "aoa-playbooks": root_context.AOA_PLAYBOOKS_ROOT,
            "aoa-memo": root_context.AOA_MEMO_ROOT,
            "abyss-stack": abyss_stack_root,
        },
    )


def write_runtime_evidence_selection_example(
    repo_root: Path,
    *,
    filename: str,
    source_schema_ref: str,
    candidate_eval_refs: list[str],
) -> None:
    write_text(
        repo_root / runtime_evidence_selection_validator.RUNTIME_EVIDENCE_SELECTION_SCHEMA_PATH,
        """
        {
          "$schema": "https://json-schema.org/draft/2020-12/schema",
          "$id": "https://aoa-evals/mechanics/audit/parts/selected-evidence-packets/schemas/runtime-evidence-selection.schema.json",
          "title": "aoa-evals runtime evidence selection",
          "type": "object",
          "additionalProperties": false,
          "required": [
            "surface_type",
            "selection_id",
            "source_repo",
            "source_schema_ref",
            "source_manifests",
            "bounded_claim",
            "promotion_target",
            "comparison_mode",
            "selected_evidence",
            "environment_invariants",
            "do_not_overread",
            "review_posture"
          ],
          "properties": {
            "surface_type": {"const": "runtime_evidence_selection"},
            "selection_id": {"type": "string"},
            "source_repo": {"const": "abyss-stack"},
            "source_schema_ref": {"type": "string"},
            "source_manifests": {"type": "array", "items": {"type": "string"}, "minItems": 1},
            "bounded_claim": {"type": "string", "minLength": 1},
            "promotion_target": {"type": "string", "enum": ["local-only", "evidence-sidecar", "bundle-candidate"]},
            "comparison_mode": {"type": "string", "enum": ["none", "fixed-baseline", "peer-compare", "longitudinal-window"]},
            "candidate_eval_refs": {"type": "array", "items": {"type": "string"}},
            "selected_evidence": {
              "type": "array",
              "minItems": 1,
              "items": {
                "type": "object",
                "additionalProperties": false,
                "required": ["artifact_ref", "evidence_role", "summary_only"],
                "properties": {
                  "artifact_ref": {"type": "string"},
                  "evidence_role": {"type": "string"},
                  "summary_only": {"type": "boolean"}
                }
              }
            },
            "environment_invariants": {"type": "array", "items": {"type": "string"}, "minItems": 1},
            "environment_deltas": {"type": "array", "items": {"type": "string"}},
            "excluded_artifacts": {"type": "array", "items": {"type": "string"}},
            "do_not_overread": {"type": "array", "items": {"type": "string"}, "minItems": 1},
            "review_posture": {
              "type": "object",
              "additionalProperties": false,
              "required": ["portable_enough", "comparison_hygiene_named", "human_review_required"],
              "properties": {
                "portable_enough": {"type": "boolean"},
                "comparison_hygiene_named": {"type": "boolean"},
                "human_review_required": {"type": "boolean"}
              }
            }
          }
        }
        """,
    )
    write_text(
        repo_root / runtime_evidence_selection_validator.RUNTIME_EVIDENCE_SELECTION_EXAMPLES_DIR / filename,
        json.dumps(
            {
                "surface_type": "runtime_evidence_selection",
                "selection_id": "return-anchor-integrity-wrapper-v1",
                "source_repo": "abyss-stack",
                "source_schema_ref": source_schema_ref,
                "source_manifests": [
                    "repo:abyss-stack/Logs/agent-api/runs/2026-03-26T120500Z__return-aware-route__case-a/return.manifest.json"
                ],
                "bounded_claim": "Bounded return-aware runtime evidence can support anchor-fidelity reading without becoming a final-quality claim.",
                "promotion_target": "evidence-sidecar",
                "comparison_mode": "none",
                "candidate_eval_refs": candidate_eval_refs,
                "selected_evidence": [
                    {
                        "artifact_ref": "repo:abyss-stack/Logs/agent-api/runs/2026-03-26T120500Z__return-aware-route__case-a/return-event.summary.json",
                        "evidence_role": "summary",
                        "summary_only": True,
                    },
                    {
                        "artifact_ref": "repo:abyss-stack/Logs/agent-api/notes/return-integrity-sidecar-v1.md",
                        "evidence_role": "integrity-sidecar",
                        "summary_only": True,
                    },
                ],
                "environment_invariants": [
                    "same wrapper policy family",
                    "same return-aware route family",
                ],
                "environment_deltas": [
                    "route family varies across cases while return policy remains unchanged"
                ],
                "excluded_artifacts": [
                    "repo:abyss-stack/Logs/agent-api/runs/2026-03-26T120500Z__return-aware-route__case-a/raw/full-transcript.jsonl"
                ],
                "do_not_overread": [
                    "does not prove final answer quality"
                ],
                "review_posture": {
                    "portable_enough": False,
                    "comparison_hygiene_named": True,
                    "human_review_required": True,
                },
            },
            indent=2,
        )
        + "\n",
    )

def test_validate_runtime_evidence_selection_uses_repo_local_schema(tmp_path: Path) -> None:
    write_runtime_evidence_selection_example(
        tmp_path,
        filename="runtime_evidence_selection.return-anchor-integrity.example.json",
        source_schema_ref="repo:abyss-stack/mechanics/governed-execution/parts/return-policy/schemas/runtime-return-event.schema.json",
        candidate_eval_refs=["candidate:aoa-return-anchor-integrity"],
    )
    schema_path = tmp_path / runtime_evidence_selection_validator.RUNTIME_EVIDENCE_SELECTION_SCHEMA_PATH
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    schema["required"].append("repo_local_only")
    schema["properties"]["repo_local_only"] = {"type": "string"}
    write_json_payload(schema_path, schema)

    issues = runtime_evidence_selection_validator.validate_runtime_evidence_selection_surfaces(
        tmp_path,
        records=[],
        context=readout_contexts.runtime_audit_context(),
        target_eval_names={"aoa-return-anchor-integrity"},
    )

    assert any(
        issue.location == "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.return-anchor-integrity.example.json"
        and "repo_local_only" in issue.message
        for issue in issues
    )


def test_validate_runtime_evidence_selection_reports_missing_expected_examples_in_full_run(tmp_path: Path) -> None:
    write_text(
        tmp_path / runtime_evidence_selection_validator.RUNTIME_EVIDENCE_SELECTION_SCHEMA_PATH,
        """
        {
          "$schema": "https://json-schema.org/draft/2020-12/schema",
          "type": "object"
        }
        """,
    )

    issues = runtime_evidence_selection_validator.validate_runtime_evidence_selection_surfaces(
        tmp_path,
        records=[],
        context=readout_contexts.runtime_audit_context(),
    )

    assert any(
        issue.location.endswith("runtime_evidence_selection.workhorse-local.example.json")
        and "file is missing" in issue.message
        for issue in issues
    )


def test_validate_runtime_evidence_selection_accepts_example_backed_runtime_chaos_window() -> None:
    issues, records = collect_catalog_records(REPO_ROOT)

    assert issues == []
    assert (
        runtime_evidence_selection_validator.validate_runtime_evidence_selection_surfaces(
            REPO_ROOT,
            records,
            context=readout_contexts.runtime_audit_context(),
            target_eval_names={"aoa-stress-recovery-window"},
        )
        == []
    )


def test_resolve_abyss_stack_root_prefers_source_checkout_over_runtime_tree(
    tmp_path: Path,
    monkeypatch,
) -> None:
    runtime_like_root = tmp_path / "srv" / "abyss-stack"
    write_text(runtime_like_root / "Configs" / "README.md", "# Runtime mirror\n")

    home_root = tmp_path / "home" / "dionysus"
    source_root = home_root / "src" / "abyss-stack"
    write_text(source_root / "README.md", "# abyss-stack\n")
    write_text(source_root / "scripts" / "validate_stack.py", "print('ok')\n")
    write_text(
        source_root
        / "mechanics"
        / "governed-execution"
        / "parts"
        / "return-policy"
        / "schemas"
        / "runtime-return-event.schema.json",
        "{}\n",
    )

    monkeypatch.setenv("HOME", str(home_root))
    monkeypatch.delenv("ABYSS_STACK_ROOT", raising=False)

    resolved = root_context.resolve_abyss_stack_root(runtime_like_root)

    assert resolved == source_root.resolve()


def test_resolve_abyss_stack_root_respects_env_override(
    tmp_path: Path,
    monkeypatch,
) -> None:
    default_root = tmp_path / "srv" / "abyss-stack"
    override_root = tmp_path / "custom" / "abyss-stack"
    monkeypatch.setenv("ABYSS_STACK_ROOT", str(override_root))

    resolved = root_context.resolve_abyss_stack_root(default_root)

    assert resolved == override_root.resolve()


def test_validate_repo_accepts_return_runtime_evidence_selection_for_non_starter_bundle(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _write_return_anchor_evidence_surface(
        tmp_path,
        source_schema_ref="repo:abyss-stack/mechanics/governed-execution/parts/return-policy/schemas/runtime-return-event.schema.json",
    )

    abyss_stack_root = tmp_path / "abyss-stack"
    make_abyss_stack_schema(tmp_path, "runtime-return-event.schema.json")
    _set_abyss_stack_ref_roots(monkeypatch, repo_root=tmp_path, abyss_stack_root=abyss_stack_root)

    issues = run_validation(tmp_path, eval_name="aoa-return-anchor-integrity")

    assert issues == []


def test_validate_repo_rejects_return_runtime_evidence_selection_outside_tracked_schema_space(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _write_return_anchor_evidence_surface(
        tmp_path,
        source_schema_ref="repo:abyss-stack/docs/RECURRENCE_RUNTIME_POLICY.md",
    )

    abyss_stack_root = tmp_path / "abyss-stack"
    write_text(abyss_stack_root / "docs" / "RECURRENCE_RUNTIME_POLICY.md", "# Recurrence Runtime Policy\n")
    _set_abyss_stack_ref_roots(monkeypatch, repo_root=tmp_path, abyss_stack_root=abyss_stack_root)

    issues = run_validation(tmp_path, eval_name="aoa-return-anchor-integrity")

    assert any(
        "source_schema_ref must equal 'repo:abyss-stack/mechanics/governed-execution/parts/return-policy/schemas/runtime-return-event.schema.json'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_accepts_non_tracked_abyss_stack_logs_refs_for_return_runtime_evidence(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _write_return_anchor_evidence_surface(
        tmp_path,
        source_schema_ref="repo:abyss-stack/mechanics/governed-execution/parts/return-policy/schemas/runtime-return-event.schema.json",
    )

    abyss_stack_root = tmp_path / "abyss-stack"
    make_abyss_stack_schema(tmp_path, "runtime-return-event.schema.json")
    _set_abyss_stack_ref_roots(monkeypatch, repo_root=tmp_path, abyss_stack_root=abyss_stack_root)

    issues = run_validation(tmp_path, eval_name="aoa-return-anchor-integrity")

    assert not any(
        "reference target does not exist: abyss-stack/Logs/" in issue.message
        for issue in issues
    )


def test_validate_repo_allows_return_anchor_integrity_as_public_non_starter_bundle(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _write_return_anchor_evidence_surface(
        tmp_path,
        source_schema_ref="repo:abyss-stack/mechanics/governed-execution/parts/return-policy/schemas/runtime-return-event.schema.json",
    )

    abyss_stack_root = tmp_path / "abyss-stack"
    make_abyss_stack_schema(tmp_path, "runtime-return-event.schema.json")
    _set_abyss_stack_ref_roots(monkeypatch, repo_root=tmp_path, abyss_stack_root=abyss_stack_root)

    assert run_validation(tmp_path, eval_name="aoa-return-anchor-integrity") == []


def test_validate_runtime_integrity_review_surface_accepts_repo_contract() -> None:
    schema_validation = runtime_integrity_review_schema_validator.runtime_integrity_review_schema_validation(
        REPO_ROOT
    )

    assert runtime_integrity_review_docs_validator.validate_runtime_integrity_review_doc_surfaces(REPO_ROOT) == []
    assert schema_validation.issues == []
    assert runtime_integrity_review_example_validator.validate_runtime_integrity_review_example_surface(
        REPO_ROOT,
        context=readout_contexts.runtime_audit_context(),
        schema_validator=schema_validation.validator,
    ) == []


def test_validate_runtime_integrity_review_surface_requires_all_declared_doc_fields(tmp_path: Path) -> None:
    for relative_path in (
        "docs/README.md",
        "mechanics/agon/legacy/raw/AGON_WAVE10_EVAL_LANDING.md",
        "mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md",
        "mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json",
        "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json",
    ):
        copy_repo_text(tmp_path, relative_path)

    doc_path = tmp_path / runtime_integrity_review_common_validator.RUNTIME_INTEGRITY_REVIEW_DOC_NAME
    doc_text = doc_path.read_text(encoding="utf-8").replace("`evidence_refs`", "evidence refs", 1)
    doc_path.write_text(doc_text, encoding="utf-8")

    issues = runtime_integrity_review_docs_validator.validate_runtime_integrity_review_doc_surfaces(tmp_path)

    assert any(
        issue.location == "mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md"
        and "runtime integrity review guide must mention '`evidence_refs`'" == issue.message
        for issue in issues
    )


def test_validate_runtime_integrity_review_surface_uses_repo_local_schema(tmp_path: Path) -> None:
    for relative_path in (
        "docs/README.md",
        "mechanics/agon/legacy/raw/AGON_WAVE10_EVAL_LANDING.md",
        "mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md",
        "mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json",
        "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json",
    ):
        copy_repo_text(tmp_path, relative_path)

    schema_path = tmp_path / runtime_integrity_review_common_validator.RUNTIME_INTEGRITY_REVIEW_SCHEMA_PATH
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    schema["required"].append("repo_local_only")
    schema["properties"]["repo_local_only"] = {"type": "string"}
    write_json_payload(schema_path, schema)

    issues = runtime_integrity_review_example_validator.validate_runtime_integrity_review_example_surface(
        tmp_path,
        context=readout_contexts.runtime_audit_context(),
    )

    assert any(
        issue.location == "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json"
        and "repo_local_only" in issue.message
        for issue in issues
    )


def test_validate_runtime_integrity_review_surface_rejects_weakened_schema_contract(tmp_path: Path) -> None:
    for relative_path in (
        "docs/README.md",
        "mechanics/agon/legacy/raw/AGON_WAVE10_EVAL_LANDING.md",
        "mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md",
        "mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json",
        "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json",
    ):
        copy_repo_text(tmp_path, relative_path)

    schema_path = tmp_path / runtime_integrity_review_common_validator.RUNTIME_INTEGRITY_REVIEW_SCHEMA_PATH
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    schema["properties"]["evidence_refs"]["minItems"] = 1
    write_json_payload(schema_path, schema)

    issues = runtime_integrity_review_schema_validator.validate_runtime_integrity_review_schema_surface(tmp_path)

    assert any(
        issue.location == "mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json"
        and "evidence_refs as an exact-count unique repo-ref array" in issue.message
        for issue in issues
    )


def test_validate_runtime_integrity_review_surface_rejects_open_top_level_schema(tmp_path: Path) -> None:
    for relative_path in (
        "docs/README.md",
        "mechanics/agon/legacy/raw/AGON_WAVE10_EVAL_LANDING.md",
        "mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md",
        "mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json",
        "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json",
    ):
        copy_repo_text(tmp_path, relative_path)

    schema_path = tmp_path / runtime_integrity_review_common_validator.RUNTIME_INTEGRITY_REVIEW_SCHEMA_PATH
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    schema["additionalProperties"] = True
    write_json_payload(schema_path, schema)

    issues = runtime_integrity_review_schema_validator.validate_runtime_integrity_review_schema_surface(tmp_path)

    assert any(
        issue.location == "mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json"
        and "top-level additionalProperties set to false" in issue.message
        for issue in issues
    )


def test_validate_runtime_integrity_review_surface_rejects_missing_center_anchor(
    tmp_path: Path,
    monkeypatch,
) -> None:
    repo_root = tmp_path / "aoa-evals"
    for relative_path in (
        "docs/README.md",
        "mechanics/agon/legacy/raw/AGON_WAVE10_EVAL_LANDING.md",
        "mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md",
        "mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json",
        "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json",
    ):
        copy_repo_text(repo_root, relative_path)

    routing_root = tmp_path / "aoa-routing"
    write_text(routing_root / "docs" / "LIVE_SESSION_REENTRY_ROUTE_REVIEW.md", "# Live Session Reentry Route Review\n")
    agents_root = tmp_path / "aoa-agents"
    write_text(
        agents_root
        / "mechanics"
        / "checkpoint"
        / "parts"
        / "continuity-lane"
        / "docs"
        / "self-agency-continuity-lane.md",
        "# Self-Agency Continuity Lane\n",
    )
    memo_root = tmp_path / "aoa-memo"
    write_text(memo_root / "schemas" / "inquiry_checkpoint.schema.json", "{\n  \"type\": \"object\"\n}\n")
    write_text(
        memo_root / "docs" / "SELF_AGENCY_CONTINUITY_WRITEBACK.md",
        "# Self-Agency Continuity Writeback\n",
    )
    center_root = tmp_path / "Agents-of-Abyss"
    write_text(
        center_root / "mechanics" / "experience" / "parts" / "continuity-context" / "CONTRACT.md",
        "# Continuity Context Contract\n",
    )

    monkeypatch.setattr(root_context, "AGENTS_OF_ABYSS_ROOT", center_root)
    monkeypatch.setattr(root_context, "REPO_REF_ROOTS",
        {
            "aoa-evals": repo_root,
            "aoa-routing": routing_root,
            "aoa-agents": agents_root,
            "aoa-memo": memo_root,
        },
    )

    issues = runtime_integrity_review_example_validator.validate_runtime_integrity_review_example_surface(
        repo_root,
        context=readout_contexts.runtime_audit_context(),
    )

    assert any(
        issue.location == "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json.budget_ref"
        and "anchor 'stronger-owner-split' was not found" in issue.message
        for issue in issues
    )


def test_validate_runtime_integrity_review_surface_rejects_anchor_drift_in_evidence_refs(
    tmp_path: Path,
    monkeypatch,
) -> None:
    repo_root = tmp_path / "aoa-evals"
    for relative_path in (
        "docs/README.md",
        "mechanics/agon/legacy/raw/AGON_WAVE10_EVAL_LANDING.md",
        "mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md",
        "mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md",
        "mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md",
        "mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json",
        "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json",
    ):
        copy_repo_text(repo_root, relative_path)

    example_path = repo_root / runtime_integrity_review_common_validator.RUNTIME_INTEGRITY_REVIEW_EXAMPLE_NAME
    payload = json.loads(example_path.read_text(encoding="utf-8"))
    payload["evidence_refs"][0] = "repo:aoa-evals/mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md#purpose"
    write_json_payload(example_path, payload)

    routing_root = tmp_path / "aoa-routing"
    write_text(routing_root / "docs" / "LIVE_SESSION_REENTRY_ROUTE_REVIEW.md", "# Live Session Reentry Route Review\n")
    agents_root = tmp_path / "aoa-agents"
    write_text(
        agents_root
        / "mechanics"
        / "checkpoint"
        / "parts"
        / "continuity-lane"
        / "docs"
        / "self-agency-continuity-lane.md",
        "# Self-Agency Continuity Lane\n",
    )
    memo_root = tmp_path / "aoa-memo"
    write_text(memo_root / "schemas" / "inquiry_checkpoint.schema.json", "{\n  \"type\": \"object\"\n}\n")
    write_text(
        memo_root / "docs" / "SELF_AGENCY_CONTINUITY_WRITEBACK.md",
        "# Self-Agency Continuity Writeback\n",
    )
    center_root = tmp_path / "Agents-of-Abyss"
    write_text(
        center_root / "mechanics" / "experience" / "parts" / "continuity-context" / "CONTRACT.md",
        "# Continuity Context Contract\n\n## Stronger Owner Split\n",
    )

    monkeypatch.setattr(root_context, "AGENTS_OF_ABYSS_ROOT", center_root)
    monkeypatch.setattr(root_context, "REPO_REF_ROOTS",
        {
            "aoa-evals": repo_root,
            "aoa-routing": routing_root,
            "aoa-agents": agents_root,
            "aoa-memo": memo_root,
        },
    )

    issues = runtime_integrity_review_example_validator.validate_runtime_integrity_review_example_surface(
        repo_root,
        context=readout_contexts.runtime_audit_context(),
    )

    assert any(
        issue.location == "mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json"
        and "bounded W10 runtime integrity review surfaces" in issue.message
        for issue in issues
    )


def test_validate_trace_eval_bridge_surfaces_keeps_local_example_checks_when_playbooks_missing(
    tmp_path: Path,
    monkeypatch,
) -> None:
    write_text(
        tmp_path / runtime_trace_eval_bridge_validator.ARTIFACT_VERDICT_HOOK_SCHEMA_PATH,
        """
        {
          "$schema": "https://json-schema.org/draft/2020-12/schema",
          "type": "object",
          "required": ["repo_local_only"],
          "properties": {
            "repo_local_only": {"type": "string"}
          }
        }
        """,
    )
    write_json_payload(tmp_path / "generated" / "eval_catalog.min.json", {"evals": []})
    write_json_payload(
        tmp_path
        / "mechanics/checkpoint/parts/self-agent-posture/examples/artifact_to_verdict_hook.self-agent-checkpoint-rollout.example.json",
        {},
    )
    monkeypatch.setattr(root_context, "AOA_PLAYBOOKS_ROOT", tmp_path / "missing-playbooks")
    monkeypatch.setattr(
        runtime_trace_eval_bridge_validator,
        "ARTIFACT_VERDICT_HOOK_EXAMPLES",
        {"AOA-P-0006": "mechanics/checkpoint/parts/self-agent-posture/examples/artifact_to_verdict_hook.self-agent-checkpoint-rollout.example.json"},
    )

    issues = runtime_trace_eval_bridge_validator.validate_trace_eval_bridge_surfaces(
        tmp_path,
        [],
        context=readout_contexts.runtime_audit_context(),
    )

    assert any(
        issue.location == "mechanics/checkpoint/parts/self-agent-posture/examples/artifact_to_verdict_hook.self-agent-checkpoint-rollout.example.json"
        and "repo_local_only" in issue.message
        for issue in issues
    )


def test_artifact_hook_expectations_use_current_aoa_agents_mechanics_refs() -> None:
    refs = [
        ref
        for expectation in artifact_hooks.TRACE_EVAL_HOOK_EXPECTATIONS.values()
        for ref in expectation["artifact_contract_refs"]
        if ref.startswith("repo:aoa-agents/")
    ]

    assert refs
    assert not any(ref.startswith("repo:aoa-agents/schemas/") for ref in refs)
    assert not any("repo:aoa-agents/examples/alpha_reference_routes/" in ref for ref in refs)
    assert (
        "repo:aoa-agents/mechanics/checkpoint/parts/self-agent-checkpoint/schemas/self-agent-checkpoint.schema.json"
        in refs
    )
    assert (
        "repo:aoa-agents/mechanics/runtime-seam/parts/artifact-contracts/schemas/artifact.route_decision.schema.json"
        in refs
    )
