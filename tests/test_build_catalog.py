from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_catalog
from validate_repo import build_catalog_payloads, collect_catalog_records

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


def test_build_catalog_check_passes_after_write(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-check-pass")

    full_path, min_path = build_catalog.write_catalogs(tmp_path)

    assert full_path.name == "eval_catalog.json"
    assert min_path.name == "eval_catalog.min.json"
    assert build_catalog.check_catalogs(tmp_path) == []

