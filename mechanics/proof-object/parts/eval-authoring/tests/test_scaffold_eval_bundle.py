from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[5]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_repo


SCRIPT_PATH = (
    REPO_ROOT
    / "mechanics"
    / "proof-object"
    / "parts"
    / "eval-authoring"
    / "scripts"
    / "scaffold_eval_bundle.py"
)


def load_scaffold_module():
    spec = importlib.util.spec_from_file_location("scaffold_eval_bundle", SCRIPT_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_catalog(repo_root: Path, entries: list[dict[str, object]]) -> None:
    generated = repo_root / "generated"
    generated.mkdir(parents=True, exist_ok=True)
    (generated / "eval_catalog.min.json").write_text(
        json.dumps(
            {
                "catalog_version": 1,
                "source_of_truth": {
                    "eval_markdown": "evals/**/EVAL.md",
                    "eval_manifest": "evals/**/eval.yaml",
                },
                "evals": entries,
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def proposal(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "schema_version": "eval_need_v1",
        "name": "aoa-runtime-evidence-route-discipline",
        "proof_question": "Does runtime evidence route through candidate packets before proof review?",
        "origin_need": "OS Abyss needs runtime evidence pressure to stay below source proof authority.",
        "summary": "Checks whether runtime evidence pressure stays candidate-only before review.",
        "object_under_evaluation": "runtime evidence routing workflow",
        "category": "workflow",
        "claim_type": "bounded",
        "baseline_mode": "none",
        "report_format": "summary-with-breakdown",
        "verdict_shape": "categorical",
        "authoring_route": "new_draft_bundle",
        "expected_use_when": [
            "runtime or trace artifacts are routed toward aoa-evals",
        ],
        "blind_spot_notes": [
            "does not prove runtime health",
            "does not accept evidence as proof",
        ],
        "related_eval_refs": [],
        "candidate_evidence_refs": [
            "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json",
        ],
        "quest_refs": [
            "AOA-EV-Q-0010",
        ],
        "source_refs": [
            "mechanics/audit/README.md",
        ],
        "technique_dependencies": [],
        "skill_dependencies": [],
    }
    payload.update(overrides)
    return payload


def test_related_existing_eval_blocks_parallel_scaffold_without_allow_new(tmp_path: Path) -> None:
    module = load_scaffold_module()
    write_catalog(
        tmp_path,
        [
            {
                "name": "aoa-verification-honesty",
                "category": "workflow",
                "status": "portable",
                "summary": "Checks whether verification evidence is reported honestly.",
                "object_under_evaluation": "bounded change workflow",
                "claim_type": "bounded",
                "baseline_mode": "none",
                "report_format": "summary-with-breakdown",
                "eval_path": "evals/workflow/aoa-verification-honesty/EVAL.md",
            }
        ],
    )

    result = module.route_result(
        proposal=proposal(related_eval_refs=["aoa-verification-honesty"]),
        repo_root=tmp_path,
        allow_new=False,
        write=False,
    )

    assert result["outcome"] == "existing_route_required"
    assert result["existing_matches"][0]["name"] == "aoa-verification-honesty"
    assert not (tmp_path / "evals").exists()


def test_new_draft_requires_allow_new_even_when_no_match_exists(tmp_path: Path) -> None:
    module = load_scaffold_module()
    write_catalog(tmp_path, [])

    result = module.route_result(
        proposal=proposal(),
        repo_root=tmp_path,
        allow_new=False,
        write=False,
    )

    assert result["outcome"] == "new_draft_requires_allow_new"
    assert result["target_path"] == "evals/workflow/aoa-runtime-evidence-route-discipline"


def test_allow_new_write_creates_valid_draft_bundle(tmp_path: Path) -> None:
    module = load_scaffold_module()
    write_catalog(tmp_path, [])

    result = module.route_result(
        proposal=proposal(),
        repo_root=tmp_path,
        allow_new=True,
        write=True,
    )

    assert result["outcome"] == "created_new_draft"
    bundle_dir = tmp_path / "evals" / "workflow" / "aoa-runtime-evidence-route-discipline"
    assert (bundle_dir / "EVAL.md").is_file()
    assert (bundle_dir / "eval.yaml").is_file()
    assert (bundle_dir / "notes" / "origin-need.md").is_file()
    assert (bundle_dir / "checks" / "eval-integrity-check.md").is_file()

    issues, records = validate_repo.collect_catalog_records(tmp_path)
    assert issues == []
    assert [record.name for record in records] == ["aoa-runtime-evidence-route-discipline"]


def test_non_new_authoring_route_does_not_scaffold(tmp_path: Path) -> None:
    module = load_scaffold_module()
    write_catalog(tmp_path, [])

    result = module.route_result(
        proposal=proposal(
            authoring_route="quest_record",
            quest_refs=["AOA-EV-Q-0010"],
        ),
        repo_root=tmp_path,
        allow_new=True,
        write=True,
    )

    assert result["outcome"] == "quest_record"
    assert not (tmp_path / "evals").exists()
