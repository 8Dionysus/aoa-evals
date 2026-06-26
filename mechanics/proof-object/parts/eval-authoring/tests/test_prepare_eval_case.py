from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[5]
SCRIPT_DIR = (
    REPO_ROOT
    / "mechanics"
    / "proof-object"
    / "parts"
    / "eval-authoring"
    / "scripts"
)
SCRIPT_PATH = SCRIPT_DIR / "prepare_eval_case.py"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))


def load_prepare_module():
    spec = importlib.util.spec_from_file_location("prepare_eval_case", SCRIPT_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_catalog(repo_root: Path, entries: list[dict[str, object]]) -> None:
    generated = repo_root / "generated"
    generated.mkdir(parents=True, exist_ok=True)
    (generated / "eval_catalog.min.json").write_text(
        json.dumps({"evals": entries}, indent=2),
        encoding="utf-8",
    )


def proposal(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "schema_version": "eval_need_v1",
        "name": "aoa-new-route-discipline",
        "proof_question": "Does the agent keep route discipline before eval authoring?",
        "origin_need": "OS Abyss needs fast eval case collection without bypassing owner gates.",
        "summary": "Checks whether eval case pressure is collected before source proof authoring.",
        "object_under_evaluation": "eval case authoring workflow",
        "category": "workflow",
        "claim_type": "bounded",
        "baseline_mode": "none",
        "report_format": "summary-with-breakdown",
        "verdict_shape": "categorical",
        "authoring_route": "new_draft_bundle",
        "expected_use_when": ["a new eval case appears during repository work"],
        "blind_spot_notes": ["does not create an eval bundle"],
        "related_eval_refs": [],
        "candidate_evidence_refs": ["candidate:local-pressure"],
        "quest_refs": [],
        "source_refs": ["mechanics/proof-object/parts/eval-authoring/README.md"],
        "technique_dependencies": [],
        "skill_dependencies": [],
    }
    payload.update(overrides)
    return payload


def catalog_entry(name: str) -> dict[str, object]:
    return {
        "name": name,
        "category": "workflow",
        "status": "bounded",
        "summary": "Checks route discipline before source proof authoring.",
        "object_under_evaluation": "eval case authoring workflow",
        "claim_type": "bounded",
        "baseline_mode": "none",
        "report_format": "summary-with-breakdown",
        "eval_path": f"evals/workflow/{name}/EVAL.md",
    }


def test_prepare_case_builds_route_kit_without_writing_bundle(tmp_path: Path) -> None:
    module = load_prepare_module()
    write_catalog(tmp_path, [])

    payload = module.build_case_kit(
        proposal=proposal(),
        repo_root=tmp_path,
    )

    assert payload["schema_version"] == module.SCHEMA_VERSION
    assert payload["valid"] is True
    assert payload["route_check"]["outcome"] == "new_draft_requires_allow_new"
    assert payload["draft_plan"]["outcome"] == "dry_run_new_draft"
    assert payload["recommended_next_step"] == "review_existing_matches_then_run_scaffold_dry_run_with_allow_new"
    assert "scaffold_eval_bundle.py" in payload["scaffold_commands"]["draft_dry_run_after_review"]
    assert not (tmp_path / "evals").exists()


def test_prepare_case_routes_existing_match_before_parallel_scaffold(tmp_path: Path) -> None:
    module = load_prepare_module()
    write_catalog(tmp_path, [catalog_entry("aoa-existing-route-discipline")])

    payload = module.build_case_kit(
        proposal=proposal(related_eval_refs=["aoa-existing-route-discipline"]),
        repo_root=tmp_path,
    )

    assert payload["valid"] is True
    assert payload["route_check"]["outcome"] == "existing_route_required"
    assert payload["route_check"]["existing_matches"][0]["name"] == "aoa-existing-route-discipline"
    assert payload["recommended_next_step"] == "inspect_existing_matches_before_scaffolding_parallel_eval"
    assert not (tmp_path / "evals").exists()


def test_prepare_case_writes_only_eval_need_proposal(tmp_path: Path) -> None:
    module = load_prepare_module()
    write_catalog(tmp_path, [])
    proposal_path = tmp_path / "cases" / "aoa-new-route-discipline.eval_need.json"

    payload = module.build_case_kit(
        proposal=proposal(),
        repo_root=tmp_path,
        proposal_output_path=proposal_path.as_posix(),
    )

    assert payload["valid"] is True
    assert payload["proposal_write"]["status"] == "written"
    assert proposal_path.is_file()
    assert json.loads(proposal_path.read_text(encoding="utf-8"))["schema_version"] == "eval_need_v1"
    assert not (tmp_path / "evals").exists()


def test_prepare_case_does_not_write_invalid_proposal(tmp_path: Path) -> None:
    module = load_prepare_module()
    write_catalog(tmp_path, [])
    proposal_path = tmp_path / "cases" / "bad.eval_need.json"

    payload = module.build_case_kit(
        proposal=proposal(expected_use_when=[]),
        repo_root=tmp_path,
        proposal_output_path=proposal_path.as_posix(),
    )

    assert payload["valid"] is False
    assert payload["proposal_write"]["status"] == "blocked"
    assert not proposal_path.exists()


def test_prepare_case_cli_outputs_json_and_writes_proposal(tmp_path: Path) -> None:
    write_catalog(tmp_path, [])
    proposal_path = tmp_path / "cases" / "aoa-cli-route-discipline.eval_need.json"
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--repo-root",
            str(tmp_path),
            "--name",
            "aoa-cli-route-discipline",
            "--proof-question",
            "Does CLI case preparation preserve route-first eval authoring?",
            "--origin-need",
            "New eval cases need a small repeatable proposal collection tool.",
            "--summary",
            "Checks whether CLI case preparation emits proposal and route commands.",
            "--object-under-evaluation",
            "CLI eval case preparation workflow",
            "--expected-use-when",
            "an agent needs to collect a fresh eval case",
            "--blind-spot",
            "does not create the source eval bundle",
            "--candidate-evidence-ref",
            "candidate:cli",
            "--source-ref",
            "mechanics/proof-object/parts/eval-authoring/README.md",
            "--write-proposal",
            str(proposal_path),
            "--json",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    payload = json.loads(completed.stdout)

    assert completed.returncode == 0
    assert payload["valid"] is True
    assert payload["proposal_write"]["status"] == "written"
    assert proposal_path.is_file()
    assert not (tmp_path / "evals").exists()
