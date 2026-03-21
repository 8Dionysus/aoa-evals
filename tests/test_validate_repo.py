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
import eval_section_contract
from validate_repo import (
    NO_ADDITIONAL_STARTER_BUNDLES_TEXT,
    build_capsule_payload,
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

        ## Planned starter bundles

        {NO_ADDITIONAL_STARTER_BUNDLES_TEXT}
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


def make_roadmap(
    repo_root: Path,
    current_public_surface_names: list[str] | None = None,
    *,
    include_absence_note: bool = True,
) -> None:
    current_public_surface_names = current_public_surface_names or []
    current_surface_block = ""
    if current_public_surface_names:
        surface_lines = "\n".join(
            f"- `{name}` as the current public surface for validation."
            for name in current_public_surface_names
        )
        current_surface_block = f"\nCurrent public surface:\n{surface_lines}\n"

    next_candidate_line = (
        f"- {NO_ADDITIONAL_STARTER_BUNDLES_TEXT}"
        if include_absence_note
        else "- placeholder next candidate"
    )

    write_text(
        repo_root / "docs" / "ROADMAP.md",
        f"""
        # Roadmap

        ## What should happen next

        Highest-priority additions:
        - placeholder

        Next likely cross-surface candidate after the current public starter set:
        {next_candidate_line}
        {current_surface_block}
        """,
    )


def make_eval_bundle(
    repo_root: Path,
    *,
    name: str,
    category: str = "workflow",
    status: str = "draft",
    claim_type: str = "bounded",
    baseline_mode: str = "none",
    verdict_shape: str = "categorical",
    report_format: str = "summary",
    technique_dependencies: list[dict[str, str]] | None = None,
    skill_dependencies: list[dict[str, str]] | None = None,
    relations: list[dict[str, str]] | None = None,
    evidence_entries: list[dict[str, str]] | None = None,
    support_files: dict[str, str] | None = None,
    section_overrides: dict[str, str] | None = None,
) -> None:
    bundle_dir = repo_root / "bundles" / name
    support_files = dict(support_files or {
        "notes/origin-need.md": "# Origin Need\n",
        "examples/example-report.md": "# Example Report\n",
        "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
    })
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
    if evidence_entries is None:
        evidence_entries = [
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ]
        if status in {"portable", "baseline", "canonical"}:
            evidence_entries.append(
                {"kind": "portable_review", "path": "notes/portable-review.md"}
            )
            support_files.setdefault("notes/portable-review.md", "# Portable Review\n")
        if status == "canonical":
            evidence_entries.append(
                {"kind": "canonical_readiness", "path": "notes/canonical-readiness.md"}
            )
            support_files.setdefault(
                "notes/canonical-readiness.md",
                "# Canonical Readiness\n",
            )
        if baseline_mode != "none":
            evidence_entries.append(
                {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"}
            )
            support_files.setdefault(
                "notes/baseline-readiness.md",
                "# Baseline Readiness\n",
            )
        if report_format == "comparative-summary":
            if baseline_mode == "longitudinal-window":
                evidence_entries.append(
                    {"kind": "support_note", "path": "notes/window-contract.md"}
                )
                support_files.setdefault(
                    "notes/window-contract.md",
                    textwrap.dedent(
                        """\
                        # Window Contract

                        ordered window sequence
                        anchor workflow surface
                        no clear directional movement
                        """
                    ),
                )
            elif baseline_mode == "peer-compare":
                evidence_entries.append(
                    {"kind": "support_note", "path": "notes/comparison-contract.md"}
                )
                support_files.setdefault(
                    "notes/comparison-contract.md",
                    textwrap.dedent(
                        """\
                        # Comparison Contract

                        matched conditions
                        side-by-side interpretation
                        """
                    ),
                )
            else:
                evidence_entries.append(
                    {"kind": "support_note", "path": "notes/comparison-contract.md"}
                )
                support_files.setdefault(
                    "notes/comparison-contract.md",
                    textwrap.dedent(
                        """\
                        # Comparison Contract

                        baseline target
                        noisy variation
                        style-only overread
                        """
                    ),
                )
    frontmatter = {
        "name": name,
        "category": category,
        "status": status,
        "summary": "Minimal summary for validation.",
        "object_under_evaluation": "bounded test surface",
        "claim_type": claim_type,
        "baseline_mode": baseline_mode,
        "report_format": report_format,
        "technique_dependencies": [entry["id"] for entry in technique_dependencies],
        "skill_dependencies": [entry["name"] for entry in skill_dependencies],
    }
    section_bodies = {
        "Intent": "Minimal intent.",
        "Object under evaluation": "Minimal object.",
        "Bounded claim": textwrap.dedent(
            """\
            This eval is designed to support a claim like:

            under these conditions, the bounded claim holds on this surface.

            This eval does not support claims such as:
            - broad general strength
            - total safety
            """
        ).strip(),
        "Trigger boundary": textwrap.dedent(
            """\
            Use this eval when:
            - bounded review matters
            - the workflow claim is the real question

            Do not use this eval when:
            - the task is unbounded
            - the main question is something else
            """
        ).strip(),
        "Inputs": "- input",
        "Fixtures and case surface": "- fixture",
        "Scoring or verdict logic": "- logic",
        "Baseline or comparison mode": "- mode",
        "Execution contract": "- contract",
        "Outputs": "- output",
        "Failure modes": "- failure",
        "Blind spots": textwrap.dedent(
            """\
            This eval does not prove:
            - broad general strength
            - stable behavior across time
            - downstream artifact excellence
            """
        ).strip(),
        "Interpretation guidance": textwrap.dedent(
            """\
            Treat a positive result as support for one bounded claim:
            the bounded claim holds on this surface.

            Do not treat a positive result as:
            - proof of general capability
            - proof of total safety
            - proof that every nearby surface is strong
            """
        ).strip(),
        "Verification": "- verify",
        "Technique traceability": "- " + (technique_dependencies[0]["id"] if technique_dependencies else "none"),
        "Skill traceability": "- " + (skill_dependencies[0]["name"] if skill_dependencies else "none"),
        "Adaptation points": "- point",
    }
    if section_overrides:
        section_bodies.update(section_overrides)

    body_sections = [f"# {name}"]
    for heading in (
        "Intent",
        "Object under evaluation",
        "Bounded claim",
        "Trigger boundary",
        "Inputs",
        "Fixtures and case surface",
        "Scoring or verdict logic",
        "Baseline or comparison mode",
        "Execution contract",
        "Outputs",
        "Failure modes",
        "Blind spots",
        "Interpretation guidance",
        "Verification",
        "Technique traceability",
        "Skill traceability",
        "Adaptation points",
    ):
        body_sections.append(f"## {heading}\n{section_bodies[heading]}")
    body = "\n\n".join(body_sections) + "\n"
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
        "status": status,
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
        "evidence": evidence_entries,
    }
    write_text(bundle_dir / "eval.yaml", yaml.safe_dump(manifest, sort_keys=False))

    for relative_path, content in support_files.items():
        write_text(bundle_dir / relative_path, content)

    make_index(repo_root, name, category)
    make_selection(repo_root, [name])
    make_roadmap(repo_root, [name])


def write_catalogs(repo_root: Path) -> None:
    issues, records = collect_catalog_records(repo_root)
    if issues:
        return
    full_catalog, min_catalog = build_catalog_payloads(repo_root, records)
    capsules = build_capsule_payload(repo_root, records, full_catalog)
    sections, section_issues = eval_section_contract.build_sections_payload(repo_root, records)
    if section_issues:
        return
    write_json_file(repo_root / "generated" / "eval_catalog.json", full_catalog, compact=False)
    write_json_file(repo_root / "generated" / "eval_catalog.min.json", min_catalog, compact=True)
    write_json_file(repo_root / "generated" / "eval_capsules.json", capsules, compact=False)
    write_json_file(repo_root / "generated" / "eval_sections.full.json", sections, compact=False)


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


def test_validate_repo_requires_support_note_for_comparative_summary(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-comparison-contract",
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

    issues = run_validation(tmp_path)

    assert any("report_format 'comparative-summary' requires an evidence entry with kind 'support_note'" in issue.message for issue in issues)


def test_validate_repo_requires_roadmap_current_public_surface_to_be_a_starter_bundle(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-alpha")
    make_eval_bundle(tmp_path, name="aoa-beta")
    make_index(tmp_path, "aoa-alpha", "workflow")
    make_selection(tmp_path, ["aoa-alpha"])
    make_roadmap(tmp_path, ["aoa-beta"])
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("roadmap 'Current public surface' eval 'aoa-beta' must appear in EVAL_INDEX.md starter bundles" in issue.message for issue in issues)


def test_validate_repo_requires_absence_note_sync_between_roadmap_and_index(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-absence-note-drift")
    make_roadmap(tmp_path, ["aoa-absence-note-drift"], include_absence_note=False)
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("absence note" in issue.message for issue in issues)


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


def test_validate_repo_missing_generated_capsules_fail(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-missing-capsules")
    write_catalogs(tmp_path)

    (tmp_path / "generated" / "eval_capsules.json").unlink()

    issues = run_validation(tmp_path)

    assert any(
        issue.location == "generated/eval_capsules.json" and "file is missing" in issue.message
        for issue in issues
    )


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


def test_validate_repo_stale_generated_capsules_fail(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-stale-capsules")
    write_catalogs(tmp_path)

    eval_md_path = tmp_path / "bundles" / "aoa-stale-capsules" / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    eval_md_path.write_text(
        text.replace(
            "under these conditions, the bounded claim holds on this surface.",
            "under these conditions, the bounded claim changed without rebuilding capsules.",
            1,
        ),
        encoding="utf-8",
    )

    issues = run_validation(tmp_path)

    assert any(
        "generated capsules are out of date; run 'python scripts/build_catalog.py'" in issue.message
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


def test_targeted_validation_catches_stale_generated_capsule_for_selected_eval(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-targeted-stale-capsule")
    write_catalogs(tmp_path)

    eval_md_path = tmp_path / "bundles" / "aoa-targeted-stale-capsule" / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    eval_md_path.write_text(
        text.replace(
            "under these conditions, the bounded claim holds on this surface.",
            "under these conditions, the bounded claim drifted after generation.",
            1,
        ),
        encoding="utf-8",
    )

    issues = run_validation(tmp_path, eval_name="aoa-targeted-stale-capsule")

    assert any(
        "generated capsule entry for 'aoa-targeted-stale-capsule' is out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )


def test_targeted_validation_catches_stale_catalog_metadata(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-targeted-metadata-drift")
    write_catalogs(tmp_path)

    full_path = tmp_path / "generated" / "eval_catalog.json"
    min_path = tmp_path / "generated" / "eval_catalog.min.json"
    full_catalog = json.loads(full_path.read_text(encoding="utf-8"))
    min_catalog = json.loads(min_path.read_text(encoding="utf-8"))
    full_catalog["catalog_version"] = 999
    min_catalog["source_of_truth"] = {"broken": True}
    full_path.write_text(json.dumps(full_catalog), encoding="utf-8")
    min_path.write_text(json.dumps(min_catalog), encoding="utf-8")

    issues = run_validation(tmp_path, eval_name="aoa-targeted-metadata-drift")

    assert any(
        "generated catalog metadata is out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )
    assert any(
        "generated min catalog metadata is out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_capsule_source_section_without_derivable_content(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-capsule-source",
        section_overrides={"Interpretation guidance": ""},
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any(
        "missing capsule source section 'Interpretation guidance'" in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_capsule_catalog_alignment_drift(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-capsule-alignment-drift")
    write_catalogs(tmp_path)

    capsule_path = tmp_path / "generated" / "eval_capsules.json"
    capsules = json.loads(capsule_path.read_text(encoding="utf-8"))
    capsules["evals"] = []
    capsule_path.write_text(json.dumps(capsules), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any(
        "capsules are missing eval 'aoa-capsule-alignment-drift' from generated/eval_catalog.json"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_missing_generated_sections(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-missing-sections-surface")
    write_catalogs(tmp_path)
    (tmp_path / "generated" / "eval_sections.full.json").unlink()

    issues = run_validation(tmp_path)

    assert any("file is missing" in issue.message for issue in issues if issue.location.endswith("eval_sections.full.json"))


def test_validate_repo_rejects_stale_generated_sections(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-stale-sections-surface")
    write_catalogs(tmp_path)

    eval_md_path = tmp_path / "bundles" / "aoa-stale-sections-surface" / "EVAL.md"
    eval_md_path.write_text(
        eval_md_path.read_text(encoding="utf-8").replace(
            "## Adaptation points\n- point\n",
            "## Adaptation points\n- point\n- another point\n",
        ),
        encoding="utf-8",
    )

    issues = run_validation(tmp_path)

    assert any(
        "generated sections are out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_section_catalog_alignment_drift(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-section-alignment-drift")
    write_catalogs(tmp_path)

    sections_path = tmp_path / "generated" / "eval_sections.full.json"
    sections = json.loads(sections_path.read_text(encoding="utf-8"))
    sections["evals"][0]["status"] = "promoted"
    sections_path.write_text(json.dumps(sections), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any(
        "generated section entry for 'aoa-section-alignment-drift' must align with full catalog field 'status'"
        in issue.message
        for issue in issues
    )


def test_targeted_validation_catches_stale_generated_section_for_selected_eval(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-targeted-stale-sections")
    write_catalogs(tmp_path)

    eval_md_path = tmp_path / "bundles" / "aoa-targeted-stale-sections" / "EVAL.md"
    eval_md_path.write_text(
        eval_md_path.read_text(encoding="utf-8").replace(
            "## Adaptation points\n- point\n",
            "## Adaptation points\n- point\n- another point\n",
        ),
        encoding="utf-8",
    )

    issues = run_validation(tmp_path, eval_name="aoa-targeted-stale-sections")

    assert any(
        "generated section entry for 'aoa-targeted-stale-sections' is out of date; run 'python scripts/build_catalog.py'"
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


def test_validate_repo_reports_malformed_full_catalog_projection_error(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-malformed-full-catalog")
    write_catalogs(tmp_path)

    full_path = tmp_path / "generated" / "eval_catalog.json"
    full_catalog = json.loads(full_path.read_text(encoding="utf-8"))
    del full_catalog["evals"]
    full_path.write_text(json.dumps(full_catalog), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any(
        "generated catalog is malformed; min projection could not be computed" in issue.message
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

    assert run_validation(tmp_path) == []
