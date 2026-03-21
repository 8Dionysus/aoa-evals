from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_catalog
import eval_section_contract
from validate_repo import build_capsule_payload, build_catalog_payloads, collect_catalog_records

from test_validate_repo import make_eval_bundle


def test_build_catalog_projects_expected_routing_surface(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-catalog-shape",
        relations=[{"type": "complements", "target": "aoa-catalog-shape-2"}],
    )
    make_eval_bundle(tmp_path, name="aoa-catalog-shape-2")

    issues, records = collect_catalog_records(tmp_path)
    assert issues == []

    full_catalog, min_catalog = build_catalog_payloads(tmp_path, records)
    capsules = build_capsule_payload(tmp_path, records, full_catalog)
    sections, section_issues = eval_section_contract.build_sections_payload(tmp_path, records)
    assert section_issues == []

    assert full_catalog["catalog_version"] == 1
    assert full_catalog["source_of_truth"] == {
        "eval_markdown": "bundles/*/EVAL.md",
        "eval_manifest": "bundles/*/eval.yaml",
    }
    entry = next(item for item in full_catalog["evals"] if item["name"] == "aoa-catalog-shape")
    assert entry["technique_refs"] == [
        {
            "id": "AOA-T-0001",
            "repo": "aoa-techniques",
            "path": "techniques/agent-workflows/plan-diff-apply-verify-report/TECHNIQUE.md",
        }
    ]
    assert entry["skill_refs"] == [
        {
            "name": "aoa-change-protocol",
            "repo": "aoa-skills",
            "path": "skills/aoa-change-protocol/SKILL.md",
        }
    ]
    assert entry["relations"] == [{"type": "complements", "target": "aoa-catalog-shape-2"}]
    assert entry["evidence"] == [
        {"kind": "origin_need", "path": "notes/origin-need.md"},
        {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
    ]

    min_entry = next(item for item in min_catalog["evals"] if item["name"] == "aoa-catalog-shape")
    assert set(min_entry) == {
        "name",
        "category",
        "status",
        "summary",
        "object_under_evaluation",
        "claim_type",
        "baseline_mode",
        "verdict_shape",
        "report_format",
        "maturity_score",
        "rigor_level",
        "repeatability",
        "portability_level",
        "review_required",
        "validation_strength",
        "export_ready",
        "technique_dependencies",
        "skill_dependencies",
        "eval_path",
    }

    capsule_entry = next(item for item in capsules["evals"] if item["name"] == "aoa-catalog-shape")
    assert capsule_entry == {
        "name": "aoa-catalog-shape",
        "category": "workflow",
        "status": "draft",
        "summary": "Minimal summary for validation.",
        "bounded_claim_short": "under these conditions, the bounded claim holds on this surface.",
        "use_when_short": "bounded review matters; the workflow claim is the real question",
        "do_not_use_short": "the task is unbounded; the main question is something else",
        "verdict_shape": "categorical",
        "blind_spot_short": "broad general strength; stable behavior across time; downstream artifact excellence",
        "what_this_does_not_prove": "proof of general capability; proof of total safety; proof that every nearby surface is strong",
        "technique_dependencies": ["AOA-T-0001"],
        "skill_dependencies": ["aoa-change-protocol"],
        "eval_path": "bundles/aoa-catalog-shape/EVAL.md",
    }

    section_entry = next(item for item in sections["evals"] if item["name"] == "aoa-catalog-shape")
    assert sections["section_version"] == 1
    assert section_entry["verdict_shape"] == "categorical"
    assert [section["key"] for section in section_entry["sections"]] == [
        "intent",
        "object_under_evaluation",
        "bounded_claim",
        "trigger_boundary",
        "inputs",
        "fixtures_and_case_surface",
        "scoring_or_verdict_logic",
        "baseline_or_comparison_mode",
        "execution_contract",
        "outputs",
        "failure_modes",
        "blind_spots",
        "interpretation_guidance",
        "verification",
        "technique_traceability",
        "skill_traceability",
        "adaptation_points",
    ]


def test_build_catalog_check_passes_after_write(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-check-pass")

    full_path, min_path, capsule_path, sections_path = build_catalog.write_catalogs(tmp_path)

    assert full_path.name == "eval_catalog.json"
    assert min_path.name == "eval_catalog.min.json"
    assert capsule_path.name == "eval_capsules.json"
    assert sections_path.name == "eval_sections.full.json"
    assert build_catalog.check_catalogs(tmp_path) == []


def test_build_catalog_rejects_invalid_dependency_contract(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-invalid-contract")

    manifest_path = tmp_path / "bundles" / "aoa-invalid-contract" / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["technique_dependencies"][0]["repo"] = "example/other-repo"
    manifest["technique_dependencies"][0]["path"] = "../bad/path.md"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    try:
        build_catalog.write_catalogs(tmp_path)
    except ValueError as exc:
        assert "repo must resolve to 'aoa-techniques'" in str(exc)
    else:
        raise AssertionError("write_catalogs should reject invalid dependency contracts")

    problems = build_catalog.check_catalogs(tmp_path)
    assert problems
    assert "source validation failed" in problems[0]


def test_build_catalog_rejects_missing_required_section_contract(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-missing-section")

    eval_md_path = tmp_path / "bundles" / "aoa-missing-section" / "EVAL.md"
    eval_md_path.write_text(
        eval_md_path.read_text(encoding="utf-8").replace(
            "## Skill traceability\n- aoa-change-protocol\n\n",
            "",
        ),
        encoding="utf-8",
    )

    try:
        build_catalog.write_catalogs(tmp_path)
    except ValueError as exc:
        assert "missing required section 'Skill traceability'" in str(exc)
    else:
        raise AssertionError("write_catalogs should reject missing required section contract")
