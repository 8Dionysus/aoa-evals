from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[5]
PART_ROOT = REPO_ROOT / "mechanics" / "proof-object" / "parts" / "eval-authoring"
SCRIPT_DIR = PART_ROOT / "scripts"
SCRIPT_PATH = SCRIPT_DIR / "eval_forge_route.py"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))


def load_forge_module():
    spec = importlib.util.spec_from_file_location("eval_forge_route", SCRIPT_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_catalog(repo_root: Path, entries: list[dict[str, object]]) -> None:
    generated = repo_root / "generated"
    generated.mkdir(parents=True, exist_ok=True)
    (generated / "eval_catalog.min.json").write_text(
        json.dumps({"evals": entries}, indent=2) + "\n",
        encoding="utf-8",
    )


def proposal(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "schema_version": "eval_need_v1",
        "name": "aoa-new-forge-route",
        "proof_question": "Does the forge route eval pressure before authoring?",
        "origin_need": "Agents need a fast design route that still checks existing surfaces.",
        "summary": "Routes new eval pressure through design gates before source bundle work.",
        "object_under_evaluation": "eval forge route",
        "category": "workflow",
        "claim_type": "bounded",
        "baseline_mode": "none",
        "report_format": "summary-with-breakdown",
        "verdict_shape": "categorical",
        "authoring_route": "new_draft_bundle",
        "expected_use_when": ["new eval pressure has owner refs and repeatable signs"],
        "blind_spot_notes": ["does not create proof or write a source bundle"],
        "related_eval_refs": [],
        "candidate_evidence_refs": ["candidate:forge"],
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
        "summary": "Routes new eval pressure through design gates before source bundle work.",
        "object_under_evaluation": "eval forge route",
        "claim_type": "bounded",
        "baseline_mode": "none",
        "report_format": "summary-with-breakdown",
        "eval_path": f"evals/workflow/{name}/EVAL.md",
    }


def test_archetype_registry_validates_and_covers_expected_routes() -> None:
    forge = load_forge_module()
    registry, errors = forge.load_registry(REPO_ROOT)

    ids = {item["id"] for item in registry["archetypes"]}
    assert errors == []
    assert registry["schema_version"] == "eval_forge_archetype_registry_v1"
    assert len(ids) >= 18
    assert {
        "trace-trajectory-eval",
        "tool-correctness-eval",
        "local-intake-pressure-packet",
        "local-runnable-suite",
        "aoa-skills-trigger-eval",
        "human-review-rubric",
        "central-proof-bundle-draft",
        "longitudinal-window-eval",
    }.issubset(ids)


def test_candidate_packet_routes_to_skill_trigger_without_promotion() -> None:
    forge = load_forge_module()
    packet_path = (
        REPO_ROOT
        / "mechanics/audit/parts/candidate-readers/packets/session-mining/"
        "aoa-eval-keyword-mining-blindspot.eval_candidate.json"
    )
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    case = forge.candidate_packet_case(packet, packet_path=packet_path.as_posix())

    payload = forge.build_forge_route(case=case, repo_root=REPO_ROOT)

    assert payload["candidate_admissibility"]["decision"] == "keep"
    assert payload["selected_archetype_id"] == "aoa-skills-trigger-eval"
    assert payload["worksheet"]["proof_authority"] is False
    assert payload["worksheet"]["promotion_allowed"] is False
    assert payload["owner_route"]["recommended_next_command"].endswith("--json")


def test_criteria_packet_routes_to_human_review_rubric() -> None:
    forge = load_forge_module()
    packet_path = (
        REPO_ROOT
        / "mechanics/audit/parts/candidate-readers/packets/session-mining/"
        "aoa-eval-criteria-before-mining.eval_candidate.json"
    )
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    case = forge.candidate_packet_case(packet, packet_path=packet_path.as_posix())

    payload = forge.build_forge_route(case=case, repo_root=REPO_ROOT)

    assert payload["candidate_admissibility"]["decision"] == "keep"
    assert payload["selected_archetype_id"] == "human-review-rubric"
    assert payload["scaffold_posture"]["status"] == "not_applicable"


def test_keyword_only_manual_case_is_rejected(tmp_path: Path) -> None:
    forge = load_forge_module()
    args = forge.parse_args(["--case-id", "manual:weak", "--objective", "eval"])
    case = forge.manual_case(args)

    payload = forge.build_forge_route(case=case, repo_root=tmp_path)

    assert payload["candidate_admissibility"]["decision"] == "reject"
    assert payload["scaffold_posture"]["status"] == "blocked"
    assert payload["worksheet_write"]["status"] == "not_requested"


def test_local_port_inventory_routes_to_local_intake(tmp_path: Path) -> None:
    forge = load_forge_module()
    inventory_path = tmp_path / "local-port-inventory.json"
    inventory_path.write_text(
        json.dumps(
            {
                "repos": [
                    {
                        "repo_id": "aoa-routing",
                        "inventory_status": "active",
                        "root": "/srv/AbyssOS/aoa-routing",
                        "port_path": "evals/PORT.yaml",
                        "pressure_counts": {
                            "active_total": 1,
                            "intake_packets": 1,
                            "suite_notes": 0,
                            "report_notes": 0,
                        },
                        "route_recommendation": {
                            "action": "review local intake before central adoption",
                            "route_key": "local_intake",
                            "proof_boundary": "local pressure is not central proof",
                        },
                        "owner_boundary": {"owner_repo": "aoa-routing"},
                    }
                ]
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    case = forge.local_port_case(
        "aoa-routing",
        repo_root=REPO_ROOT,
        workspace_root=tmp_path,
        inventory_path=inventory_path.as_posix(),
    )
    payload = forge.build_forge_route(case=case, repo_root=tmp_path)

    assert payload["candidate_admissibility"]["decision"] == "keep"
    assert payload["selected_archetype_id"] == "local-intake-pressure-packet"
    assert payload["owner_route"]["owner_repo"] == "repo-local evals/"


def test_existing_catalog_match_blocks_parallel_scaffold(tmp_path: Path) -> None:
    forge = load_forge_module()
    write_catalog(tmp_path, [catalog_entry("aoa-existing-forge-route")])
    case = forge.proposal_case(
        proposal(
            name="aoa-existing-forge-route",
            related_eval_refs=["aoa-existing-forge-route"],
        ),
        proposal_path="cases/aoa-existing-forge-route.eval_need.json",
    )

    payload = forge.build_forge_route(case=case, repo_root=tmp_path)

    assert payload["candidate_admissibility"]["decision"] == "duplicate"
    assert payload["existing_surface_check"]["matches"][0]["name"] == "aoa-existing-forge-route"
    assert payload["scaffold_posture"]["status"] == "blocked"


def test_write_worksheet_writes_no_bundle(tmp_path: Path) -> None:
    forge = load_forge_module()
    write_catalog(tmp_path, [])
    worksheet_path = tmp_path / "worksheets" / "aoa-new-forge-route.eval_design.json"
    case = forge.proposal_case(
        proposal(),
        proposal_path="cases/aoa-new-forge-route.eval_need.json",
    )

    payload = forge.build_forge_route(
        case=case,
        repo_root=tmp_path,
        write_worksheet_path=worksheet_path.as_posix(),
    )

    assert payload["worksheet_write"]["status"] == "written"
    assert worksheet_path.is_file()
    assert json.loads(worksheet_path.read_text(encoding="utf-8"))["schema_version"] == "eval_design_worksheet_v1"
    assert not (tmp_path / "evals").exists()


def test_eval_forge_cli_outputs_json_for_real_packet() -> None:
    packet_path = (
        REPO_ROOT
        / "mechanics/audit/parts/candidate-readers/packets/session-mining/"
        "aoa-eval-keyword-mining-blindspot.eval_candidate.json"
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--repo-root",
            str(REPO_ROOT),
            "--candidate-packet",
            str(packet_path),
            "--json",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    payload = json.loads(completed.stdout)

    assert completed.returncode == 0
    assert payload["schema_version"] == "eval_forge_route_v1"
    assert payload["selected_archetype_id"] == "aoa-skills-trigger-eval"
    assert payload["worksheet"]["proof_authority"] is False


def test_real_session_packets_and_routes_remain_candidate_only() -> None:
    forge = load_forge_module()
    packet_dir = REPO_ROOT / "mechanics/audit/parts/candidate-readers/packets/session-mining"

    packet_paths = sorted(packet_dir.glob("*.eval_candidate.json"))
    assert packet_paths

    for packet_path in packet_paths:
        packet = json.loads(packet_path.read_text(encoding="utf-8"))

        assert packet["candidate_only"] is True
        assert packet["proof_authority"] is False
        assert packet["promotion_allowed"] is False
        assert "central_proof_promotion" in packet["forbidden_effects"]

        case = forge.candidate_packet_case(packet, packet_path=packet_path.as_posix())
        payload = forge.build_forge_route(case=case, repo_root=REPO_ROOT)

        assert payload["worksheet"]["proof_authority"] is False
        assert payload["worksheet"]["promotion_allowed"] is False
        assert "candidate_auto_acceptance" in payload["forbidden_actions"]
        assert payload["scaffold_posture"].get("write_allowed") is False


def test_criteria_worksheet_example_validates_and_remains_non_proof() -> None:
    forge = load_forge_module()
    worksheet_path = (
        PART_ROOT
        / "examples/aoa_eval_criteria_before_mining.eval_design_worksheet.example.json"
    )
    schema_path = PART_ROOT / "schemas/eval-design-worksheet.schema.json"

    worksheet = json.loads(worksheet_path.read_text(encoding="utf-8"))
    errors = forge.validate_json(worksheet, schema_path)

    assert errors == []
    assert worksheet["selected_archetype_id"] == "human-review-rubric"
    assert worksheet["proof_authority"] is False
    assert worksheet["promotion_allowed"] is False
