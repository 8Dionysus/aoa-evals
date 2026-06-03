from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import eval_section_contract
import validate_repo
from validate_repo import (
    collect_catalog_records,
    run_validation,
)


from validate_repo_fixtures import (
    add_fixed_baseline_proof_artifacts,
    add_longitudinal_proof_artifacts,
    add_materialized_proof_artifacts,
    eval_dir_for_test,
    make_eval_bundle,
    write_catalogs,
    write_text,
)


def test_eval_selection_rejects_generic_heading(tmp_path: Path) -> None:
    write_text(
        tmp_path / "EVAL_SELECTION.md",
        """
        # Eval Selection

        This file is the repository-wide chooser for public eval bundles.

        Current starter posture:
        - `aoa-alpha`
        """,
    )

    issues = validate_repo.validate_eval_selection(tmp_path, ["aoa-alpha"])

    assert any(
        issue.location == "EVAL_SELECTION.md"
        and "# Eval Bundle Selection Chooser" in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_missing_evidence_path(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-evidence-path",
        evidence_entries=[{"kind": "origin_need", "path": "notes/missing.md"}],
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("evidence path 'notes/missing.md' does not exist" in issue.message for issue in issues)


def test_validate_repo_requires_origin_need_for_starter_bundle(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-origin-need",
        evidence_entries=[{"kind": "integrity_check", "path": "checks/eval-integrity-check.md"}],
        support_files={
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("starter bundle must include an evidence entry with kind 'origin_need'" in issue.message for issue in issues)


def test_validate_repo_requires_baseline_readiness_for_non_none_baseline(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-baseline-readiness",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[{"kind": "origin_need", "path": "notes/origin-need.md"}],
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("baseline_readiness" in issue.message for issue in issues)


def test_validate_repo_requires_portable_review_for_portable_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-portable-review",
        status="portable",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("status 'portable' requires an evidence entry with kind 'portable_review'" in issue.message for issue in issues)


def test_validate_repo_requires_portable_review_for_baseline_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-baseline-portable-review",
        status="baseline",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/comparison-contract.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/comparison-contract.md": "# Comparison Contract\nbaseline target\nnoisy variation\nstyle-only overread\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("status 'baseline' requires an evidence entry with kind 'portable_review'" in issue.message for issue in issues)


def test_validate_repo_requires_local_shaped_portability_for_bounded_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-bounded-portability-drift",
        status="bounded",
        portability_level="portable",
    )

    issues = run_validation(tmp_path)

    assert any(
        "status 'bounded' requires portability_level 'local-shaped' but found 'portable'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_requires_local_shaped_portability_for_draft_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-draft-portability-drift",
        status="draft",
        portability_level="portable",
    )

    issues = run_validation(tmp_path)

    assert any(
        "status 'draft' requires portability_level 'local-shaped' but found 'portable'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_requires_portable_portability_for_baseline_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-baseline-portability-drift",
        status="baseline",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        portability_level="local-shaped",
    )

    issues = run_validation(tmp_path)

    assert any(
        "status 'baseline' requires portability_level 'portable' but found 'local-shaped'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_requires_broad_portability_for_canonical_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-canonical-portability-drift",
        status="canonical",
        public_safety_reviewed_at="2026-04-16",
        portability_level="portable",
    )

    issues = run_validation(tmp_path)

    assert any(
        "status 'canonical' requires portability_level 'broad' but found 'portable'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_requires_public_safety_review_date_for_canonical_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-canonical-missing-public-safety-review",
        status="canonical",
    )

    issues = run_validation(tmp_path)

    assert any(
        "status 'canonical' requires public_safety_reviewed_at" in issue.message
        for issue in issues
    )


def test_validate_repo_requires_valid_calendar_public_safety_review_date(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-canonical-invalid-public-safety-review",
        status="canonical",
        public_safety_reviewed_at="2026-99-99",
    )

    issues = run_validation(tmp_path)

    assert any(
        "public_safety_reviewed_at must be a valid calendar date" in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_future_public_safety_review_date(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-canonical-future-public-safety-review",
        status="canonical",
        public_safety_reviewed_at="2099-01-01",
        portability_level="broad",
    )

    issues = run_validation(tmp_path)

    assert any(
        "public_safety_reviewed_at must not be in the future" in issue.message
        for issue in issues
    )


def test_validate_repo_requires_support_note_for_bounded_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-bounded-review-note",
        status="bounded",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("status 'bounded' requires an evidence entry with kind 'support_note'" in issue.message for issue in issues)


def test_validate_repo_requires_bounded_review_language_for_bounded_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-weak-bounded-review-note",
        status="bounded",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/bounded-promotion-review.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/bounded-promotion-review.md": "# Bounded Review\nA useful note, but no explicit promotion language.\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("status 'bounded' requires a support_note that records approve-for-bounded outcome plus failure and readout distinctions" in issue.message for issue in issues)


def test_validate_repo_requires_canonical_readiness_for_canonical_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-canonical-readiness",
        status="canonical",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "portable_review", "path": "notes/portable-review.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/portable-review.md": "# Portable Review\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("status 'canonical' requires an evidence entry with kind 'canonical_readiness'" in issue.message for issue in issues)


def test_validate_repo_requires_artifact_process_doctrine_guide(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-artifact-review-rubric", category="artifact")
    write_catalogs(tmp_path)
    (tmp_path / "docs" / "guides" / "ARTIFACT_PROCESS_SEPARATION_GUIDE.md").unlink()

    issues = run_validation(tmp_path, eval_name="aoa-artifact-review-rubric")

    assert any("ARTIFACT_PROCESS_SEPARATION_GUIDE.md" in issue.location or "ARTIFACT_PROCESS_SEPARATION_GUIDE.md" in issue.message for issue in issues)


def test_validate_repo_accepts_valid_non_baseline_bundle_without_baseline_readiness(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-valid-non-baseline")
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-valid-non-baseline") == []


def test_validate_repo_accepts_valid_bounded_bundle_with_review_note(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-valid-bounded", status="bounded")
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-valid-bounded") == []


def test_validate_repo_accepts_valid_baseline_bundle_with_readiness_evidence(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-valid-baseline",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/comparison-contract.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/comparison-contract.md": "# Comparison Contract\nbaseline target\nnoisy variation\nstyle-only overread\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    add_fixed_baseline_proof_artifacts(tmp_path, bundle_name="aoa-valid-baseline")
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-valid-baseline") == []


def test_validate_repo_accepts_valid_baseline_status_bundle_with_portable_review(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-valid-baseline-status",
        status="baseline",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_fixed_baseline_proof_artifacts(
        tmp_path,
        bundle_name="aoa-valid-baseline-status",
        status="baseline",
    )
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-valid-baseline-status") == []


def test_validate_repo_accepts_valid_longitudinal_bundle_with_materialized_artifacts(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-valid-longitudinal-materialized",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_longitudinal_proof_artifacts(
        tmp_path,
        bundle_name="aoa-valid-longitudinal-materialized",
    )
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-valid-longitudinal-materialized") == []


def test_validate_repo_allows_local_run_without_sibling_dependency_repos(monkeypatch) -> None:
    missing_techniques_root = REPO_ROOT / ".tmp" / "missing-aoa-techniques"
    missing_skills_root = REPO_ROOT / ".tmp" / "missing-aoa-skills"
    missing_agents_root = REPO_ROOT / ".tmp" / "missing-aoa-agents"
    missing_playbooks_root = REPO_ROOT / ".tmp" / "missing-aoa-playbooks"
    missing_memo_root = REPO_ROOT / ".tmp" / "missing-aoa-memo"
    missing_abyss_stack_root = REPO_ROOT / ".tmp" / "missing-abyss-stack"

    monkeypatch.setattr(validate_repo, "AOA_TECHNIQUES_ROOT", missing_techniques_root)
    monkeypatch.setattr(validate_repo, "AOA_SKILLS_ROOT", missing_skills_root)
    monkeypatch.setattr(validate_repo, "AOA_AGENTS_ROOT", missing_agents_root)
    monkeypatch.setattr(validate_repo, "AOA_PLAYBOOKS_ROOT", missing_playbooks_root)
    monkeypatch.setattr(validate_repo, "AOA_MEMO_ROOT", missing_memo_root)
    monkeypatch.setattr(validate_repo, "ABYSS_STACK_ROOT", missing_abyss_stack_root)
    monkeypatch.setattr(
        validate_repo,
        "REPO_REF_ROOTS",
        {
            "aoa-evals": validate_repo.REPO_ROOT,
            "aoa-techniques": missing_techniques_root,
            "aoa-skills": missing_skills_root,
            "aoa-agents": missing_agents_root,
            "aoa-playbooks": missing_playbooks_root,
            "aoa-memo": missing_memo_root,
            "abyss-stack": missing_abyss_stack_root,
        },
    )

    issues = run_validation(REPO_ROOT)

    assert not any(
        "dependency target does not exist: aoa-techniques/" in issue.message
        or "dependency target does not exist: aoa-skills/" in issue.message
        or "reference target does not exist: aoa-agents/" in issue.message
        or "reference target does not exist: aoa-playbooks/" in issue.message
        or "reference target does not exist: aoa-memo/" in issue.message
        or "reference target does not exist: abyss-stack/" in issue.message
        or "does not resolve in aoa-playbooks" in issue.message
        for issue in issues
    )


def test_duplicate_eval_headings_are_detected_before_dict_normalization(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-duplicate-headings")
    eval_md_path = eval_dir_for_test(tmp_path, "aoa-duplicate-headings") / "EVAL.md"
    eval_md_text = eval_md_path.read_text(encoding="utf-8")
    eval_md_path.write_text(
        eval_md_text.replace(
            "## Object under evaluation",
            "## Intent\nSecond intent block.\n\n## Object under evaluation",
            1,
        ),
        encoding="utf-8",
    )

    issues, records = collect_catalog_records(tmp_path)
    sections, section_issues = eval_section_contract.build_sections_payload(tmp_path, records)

    assert sections["evals"] == []
    assert any("duplicate top-level section 'Intent'" in issue.message for issue in issues)
    assert any("duplicate top-level section 'Intent'" in issue.message for issue in section_issues)


def test_real_repo_has_expected_non_local_shaped_portability_bundles() -> None:
    issues, records = collect_catalog_records(REPO_ROOT)

    assert issues == []
    non_local_shaped = {
        record.name: record.manifest["portability_level"]
        for record in records
        if record.manifest["portability_level"] != "local-shaped"
    }
    assert non_local_shaped == {
        "aoa-artifact-review-rubric": "portable",
        "aoa-bounded-change-quality": "portable",
        "aoa-local-text-contract-fit": "portable",
        "aoa-regression-same-task": "portable",
        "aoa-ring-application-discipline": "portable",
        "aoa-verification-honesty": "portable",
    }


def test_validate_repo_accepts_valid_bundle_with_materialized_proof_artifacts(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-valid-proof-artifacts")
    add_materialized_proof_artifacts(
        tmp_path,
        bundle_name="aoa-valid-proof-artifacts",
        report_schema={
            "type": "object",
            "additionalProperties": False,
            "required": [
                "eval_name",
                "bundle_status",
                "object_under_evaluation",
                "verdict",
                "claim_boundary",
                "limitations",
            ],
            "properties": {
                "eval_name": {"const": "aoa-valid-proof-artifacts"},
                "bundle_status": {"const": "draft"},
                "object_under_evaluation": {"const": "bounded test surface"},
                "verdict": {"type": "string"},
                "claim_boundary": {"type": "string"},
                "limitations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
            },
        },
        report_example={
            "eval_name": "aoa-valid-proof-artifacts",
            "bundle_status": "draft",
            "object_under_evaluation": "bounded test surface",
            "verdict": "supports bounded claim",
            "claim_boundary": "bounded machine-readable proof artifact for validation",
            "limitations": ["still bounded"],
        },
    )
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-valid-proof-artifacts") == []
