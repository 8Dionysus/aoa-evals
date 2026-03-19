from __future__ import annotations

import json
import textwrap
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_catalog
from validate_repo import (
    build_catalog_payloads,
    collect_catalog_records,
    run_validation,
    write_json_file,
)


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


def make_selection(repo_root: Path, names: list[str]) -> None:
    lines = "\n".join(f"- `{name}`" for name in names)
    write_text(
        repo_root / "EVAL_SELECTION.md",
        f"""
        # Eval Selection

        Current starter posture:
        {lines}
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
    technique_dependencies: list[dict[str, str]] | None = None,
    skill_dependencies: list[dict[str, str]] | None = None,
    relations: list[dict[str, str]] | None = None,
    evidence_entries: list[dict[str, str]] | None = None,
    support_files: dict[str, str] | None = None,
) -> None:
    bundle_dir = repo_root / "bundles" / name
    support_files = support_files or {
        "notes/origin-need.md": "# Origin Need\n",
        "examples/example-report.md": "# Example Report\n",
        "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
    }
    technique_dependencies = technique_dependencies or [
        {
            "id": "AOA-T-0001",
            "repo": "8Dionysus/aoa-techniques",
            "path": "techniques/agent-workflows/plan-diff-apply-verify-report/TECHNIQUE.md",
        }
    ]
    skill_dependencies = skill_dependencies or [
        {
            "name": "aoa-change-protocol",
            "repo": "8Dionysus/aoa-skills",
            "path": "skills/aoa-change-protocol/SKILL.md",
        }
    ]
    relations = relations or []
    frontmatter = {
        "name": name,
        "category": category,
        "status": "draft",
        "summary": "Minimal summary for validation.",
        "object_under_evaluation": "bounded test surface",
        "claim_type": claim_type,
        "baseline_mode": baseline_mode,
        "report_format": report_format,
        "technique_dependencies": [entry["id"] for entry in technique_dependencies],
        "skill_dependencies": [entry["name"] for entry in skill_dependencies],
    }
    body = textwrap.dedent(
        f"""\
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
        - {technique_dependencies[0]['id']}

        ## Skill traceability
        - {skill_dependencies[0]['name']}

        ## Adaptation points
        - point
        """
    )
    write_text(
        bundle_dir / "EVAL.md",
        "---\n"
        + yaml.safe_dump(frontmatter, sort_keys=False)
        + "---\n\n"
        + body,
    )

    manifest = {
        "name": name,
        "category": category,
        "status": "draft",
        "object_under_evaluation": "bounded test surface",
        "claim_type": claim_type,
        "baseline_mode": baseline_mode,
        "verdict_shape": verdict_shape,
        "report_format": report_format,
        "maturity_score": 2,
        "rigor_level": "bounded",
        "repeatability": "moderate",
        "portability_level": "portable",
        "review_required": True,
        "validation_strength": "baseline",
        "export_ready": True,
        "blind_spot_disclosure": "required-and-present",
        "score_interpretation_bound": "explicit",
        "technique_dependencies": technique_dependencies,
        "skill_dependencies": skill_dependencies,
        "relations": relations,
        "evidence": evidence_entries
        or [
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
    }
    write_text(bundle_dir / "eval.yaml", yaml.safe_dump(manifest, sort_keys=False))

    for relative_path, content in support_files.items():
        write_text(bundle_dir / relative_path, content)

    make_index(repo_root, name, category)
    make_selection(repo_root, [name])


def write_catalogs(repo_root: Path) -> None:
    issues, records = collect_catalog_records(repo_root)
    if issues:
        return
    full_catalog, min_catalog = build_catalog_payloads(repo_root, records)
    write_json_file(repo_root / "generated" / "eval_catalog.json", full_catalog, compact=False)
    write_json_file(repo_root / "generated" / "eval_catalog.min.json", min_catalog, compact=True)


def test_build_catalog_preserves_same_kind_relations_in_full_catalog(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-alpha",
        relations=[{"type": "complements", "target": "aoa-beta"}],
    )
    make_eval_bundle(tmp_path, name="aoa-beta")
    make_index(tmp_path, "aoa-alpha", "workflow")
    make_selection(tmp_path, ["aoa-alpha", "aoa-beta"])

    assert build_catalog.main(argv=[], repo_root=tmp_path) == 0

    full_catalog = json.loads((tmp_path / "generated" / "eval_catalog.json").read_text(encoding="utf-8"))
    alpha_entry = next(entry for entry in full_catalog["evals"] if entry["name"] == "aoa-alpha")

    assert alpha_entry["relations"] == [{"type": "complements", "target": "aoa-beta"}]
    assert alpha_entry["technique_refs"][0]["repo"] == "aoa-techniques"
    assert alpha_entry["skill_refs"][0]["repo"] == "aoa-skills"


def test_validate_repo_rejects_missing_evidence_path(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-evidence-path",
        evidence_entries=[{"kind": "origin_need", "path": "notes/missing.md"}],
    )
    write_catalogs(tmp_path)

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
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("baseline_readiness" in issue.message for issue in issues)


def test_validate_repo_rejects_mirrored_field_drift(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-field-drift")
    write_catalogs(tmp_path)

    manifest_path = tmp_path / "bundles" / "aoa-field-drift" / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["category"] = "artifact"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any("field 'category' does not match" in issue.message for issue in issues)


def test_validate_repo_rejects_technique_dependency_order_mismatch(tmp_path: Path) -> None:
    technique_dependencies = [
        {
            "id": "AOA-T-0001",
            "repo": "8Dionysus/aoa-techniques",
            "path": "techniques/agent-workflows/plan-diff-apply-verify-report/TECHNIQUE.md",
        },
        {
            "id": "AOA-T-0002",
            "repo": "aoa-techniques",
            "path": "techniques/docs/source-of-truth-layout/TECHNIQUE.md",
        },
    ]
    make_eval_bundle(
        tmp_path,
        name="aoa-technique-order-drift",
        technique_dependencies=technique_dependencies,
    )
    write_catalogs(tmp_path)

    eval_md_path = tmp_path / "bundles" / "aoa-technique-order-drift" / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    _opening, frontmatter_text, body = text.split("---", 2)
    frontmatter = yaml.safe_load(frontmatter_text)
    frontmatter["technique_dependencies"] = list(reversed(frontmatter["technique_dependencies"]))
    eval_md_path.write_text(
        f"---\n{yaml.safe_dump(frontmatter, sort_keys=False)}---{body}",
        encoding="utf-8",
    )

    issues = run_validation(tmp_path)

    assert any(
        "ordered technique refs do not match"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_skill_dependency_order_mismatch(tmp_path: Path) -> None:
    skill_dependencies = [
        {
            "name": "aoa-change-protocol",
            "repo": "8Dionysus/aoa-skills",
            "path": "skills/aoa-change-protocol/SKILL.md",
        },
        {
            "name": "aoa-approval-gate-check",
            "repo": "aoa-skills",
            "path": "skills/aoa-approval-gate-check/SKILL.md",
        },
    ]
    make_eval_bundle(
        tmp_path,
        name="aoa-skill-order-drift",
        skill_dependencies=skill_dependencies,
    )
    write_catalogs(tmp_path)

    eval_md_path = tmp_path / "bundles" / "aoa-skill-order-drift" / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    _opening, frontmatter_text, body = text.split("---", 2)
    frontmatter = yaml.safe_load(frontmatter_text)
    frontmatter["skill_dependencies"] = list(reversed(frontmatter["skill_dependencies"]))
    eval_md_path.write_text(
        f"---\n{yaml.safe_dump(frontmatter, sort_keys=False)}---{body}",
        encoding="utf-8",
    )

    issues = run_validation(tmp_path)

    assert any(
        "ordered skill refs do not match"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_repo_mismatch(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-repo-mismatch")
    write_catalogs(tmp_path)

    manifest_path = tmp_path / "bundles" / "aoa-repo-mismatch" / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["technique_dependencies"][0]["repo"] = "example/other-repo"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any("repo must resolve to 'aoa-techniques'" in issue.message for issue in issues)


def test_validate_repo_rejects_non_repo_relative_dependency_path(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-path-mismatch")
    write_catalogs(tmp_path)

    manifest_path = tmp_path / "bundles" / "aoa-path-mismatch" / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["technique_dependencies"][0]["path"] = "../techniques/test/TECHNIQUE.md"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any("path must be a concrete repo-relative path" in issue.message for issue in issues)


def test_validate_repo_missing_generated_catalogs_fail(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-missing-generated")

    issues = run_validation(tmp_path)

    assert any("file is missing" in issue.message for issue in issues if "generated/" in issue.location)


def test_validate_repo_stale_generated_catalogs_fail(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-stale-generated")
    write_catalogs(tmp_path)

    eval_md_path = tmp_path / "bundles" / "aoa-stale-generated" / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    eval_md_path.write_text(text.replace("Minimal summary for validation.", "Changed without rebuilding catalog.", 1), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any(
        "generated catalog is out of date; run 'python scripts/build_catalog.py'" in issue.message
        for issue in issues
    )


def test_targeted_validation_catches_stale_generated_catalog_for_selected_eval(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-targeted-stale-generated")
    write_catalogs(tmp_path)

    eval_md_path = tmp_path / "bundles" / "aoa-targeted-stale-generated" / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    eval_md_path.write_text(
        text.replace("Minimal summary for validation.", "Changed without rebuilding catalog.", 1),
        encoding="utf-8",
    )

    issues = run_validation(tmp_path, eval_name="aoa-targeted-stale-generated")

    assert any(
        "generated catalog entry for 'aoa-targeted-stale-generated' is out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )
    assert any(
        "generated min catalog entry for 'aoa-targeted-stale-generated' is out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_min_projection_drift(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-min-projection-drift")
    write_catalogs(tmp_path)

    min_path = tmp_path / "generated" / "eval_catalog.min.json"
    min_catalog = json.loads(min_path.read_text(encoding="utf-8"))
    min_catalog["evals"][0]["summary"] = "tampered"
    min_path.write_text(json.dumps(min_catalog), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any(
        "min catalog must stay a projection of the full catalog" in issue.message
        for issue in issues
    )


def test_validate_repo_accepts_valid_non_baseline_bundle_without_baseline_readiness(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-valid-non-baseline")
    write_catalogs(tmp_path)

    assert run_validation(tmp_path) == []


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
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    assert run_validation(tmp_path) == []
