from __future__ import annotations

import textwrap
from pathlib import Path

from scripts.validate_repo import run_validation


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def make_index(repo_root: Path, name: str, category: str) -> None:
    write_text(
        repo_root / "EVAL_INDEX.md",
        f"""
        # EVAL_INDEX

        ## Starter eval bundles

        | name | category | status | summary |
        |---|---|---|---|
        | {name} | {category} | draft | Minimal summary for validation. |
        """,
    )


def make_eval_bundle(
    repo_root: Path,
    *,
    name: str,
    category: str = "workflow",
    claim_type: str = "bounded",
    baseline_mode: str = "none",
    verdict_shape: str = "categorical",
    report_format: str = "summary",
    evidence_entries: list[dict[str, str]] | None = None,
    support_files: dict[str, str] | None = None,
) -> None:
    bundle_dir = repo_root / "bundles" / name
    support_files = support_files or {"notes/origin-need.md": "# Origin Need\n"}

    write_text(
        bundle_dir / "EVAL.md",
        f"""
        ---
        name: {name}
        category: {category}
        status: draft
        summary: Minimal summary for validation.
        object_under_evaluation: bounded test surface
        claim_type: {claim_type}
        baseline_mode: {baseline_mode}
        report_format: {report_format}
        technique_dependencies:
          - AOA-T-0001
        skill_dependencies:
          - aoa-change-protocol
        ---

        # {name}

        ## Intent
        Minimal intent.

        ## Object under evaluation
        Minimal object.

        ## Bounded claim
        Minimal bounded claim.

        ## Trigger boundary
        Use this eval when:
        - one

        Do not use this eval when:
        - two

        ## Inputs
        - input

        ## Fixtures and case surface
        - fixture

        ## Scoring or verdict logic
        - logic

        ## Baseline or comparison mode
        - mode

        ## Execution contract
        - contract

        ## Outputs
        - output

        ## Failure modes
        - failure

        ## Blind spots
        - blind spot

        ## Interpretation guidance
        - guidance

        ## Verification
        - verify

        ## Technique traceability
        - AOA-T-0001

        ## Skill traceability
        - aoa-change-protocol

        ## Adaptation points
        - point
        """,
    )

    manifest_lines = [
        f"name: {name}",
        f"category: {category}",
        "status: draft",
        "object_under_evaluation: bounded test surface",
        f"claim_type: {claim_type}",
        f"baseline_mode: {baseline_mode}",
        f"verdict_shape: {verdict_shape}",
        f"report_format: {report_format}",
        "maturity_score: 2",
        "rigor_level: bounded",
        "repeatability: moderate",
        "portability_level: portable",
        "review_required: true",
        "validation_strength: baseline",
        "export_ready: true",
        "blind_spot_disclosure: required-and-present",
        "score_interpretation_bound: explicit",
        "",
        "technique_dependencies:",
        "  - id: AOA-T-0001",
        "    repo: 8Dionysus/aoa-techniques",
        "    path: techniques/agent-workflows/plan-diff-apply-verify-report/TECHNIQUE.md",
        "",
        "skill_dependencies:",
        "  - name: aoa-change-protocol",
        "    repo: 8Dionysus/aoa-skills",
        "    path: skills/aoa-change-protocol/SKILL.md",
        "",
        "relations: []",
    ]

    if evidence_entries:
        manifest_lines.append("evidence:")
        for entry in evidence_entries:
            manifest_lines.append(f"  - kind: {entry['kind']}")
            manifest_lines.append(f"    path: {entry['path']}")
    else:
        manifest_lines.append("evidence: []")

    write_text(bundle_dir / "eval.yaml", "\n".join(manifest_lines) + "\n")

    for relative_path, content in support_files.items():
        write_text(bundle_dir / relative_path, content)

    make_index(repo_root, name, category)


def test_validate_repo_rejects_missing_evidence_path(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-evidence-path",
        evidence_entries=[{"kind": "origin_need", "path": "notes/missing.md"}],
    )

    issues = run_validation(tmp_path)

    assert any("evidence path 'notes/missing.md' does not exist" in issue.message for issue in issues)


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

    issues = run_validation(tmp_path)

    assert any("baseline_readiness" in issue.message for issue in issues)


def test_validate_repo_accepts_valid_non_baseline_bundle_without_baseline_readiness(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-valid-non-baseline",
        evidence_entries=[{"kind": "origin_need", "path": "notes/origin-need.md"}],
    )

    issues = run_validation(tmp_path)

    assert issues == []


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
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
        },
    )

    issues = run_validation(tmp_path)

    assert issues == []
