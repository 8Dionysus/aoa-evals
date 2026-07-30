from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = BUNDLE_ROOT / "runners" / "run_phase13_evidence_lab.py"
PLAN_PATH = BUNDLE_ROOT / "fixtures" / "phase13-evidence-plan.json"
SCHEMA_PATH = BUNDLE_ROOT / "reports" / "phase13-evidence.schema.json"
OS_REPLAY_PATH = BUNDLE_ROOT / "fixtures" / "phase13-os-replay-cases.json"


def load_runner():
    spec = importlib.util.spec_from_file_location("phase13_evidence_runner", RUNNER_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_phase13_plan_preserves_partial_and_no_authority_posture() -> None:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    benchmarks = {
        item["benchmark_id"]: item for item in plan["public_benchmarks"]
    }

    assert plan["os_replay"]["status"] == "partial"
    assert plan["os_replay"]["privacy_posture"] == (
        "refs_only_no_raw_transcript_bodies"
    )
    assert benchmarks["longmemeval-v2"]["missing_scored_artifacts"]
    assert (
        benchmarks["locomo-plus"]["source_repo"]["license_status"]
        == "unresolved_no_license_file"
    )
    assert sum(
        len(ids)
        for benchmark in benchmarks.values()
        for ids in benchmark["selected_cases"].values()
    ) == 44
    assert all(value is False for value in plan["authority"].values())
    assert plan["soak"]["accelerated_replay_is_wall_clock_soak"] is False
    assert {
        item["evidence_id"] for item in plan["frontier_delta"]
    } == {
        "pm-bench-2026-07",
        "memsyco-bench-2026-07",
        "evomembench-2026-05",
    }
    assert all(
        item["status"] == "candidate_unexecuted"
        for item in plan["frontier_delta"]
    )


def test_os_replay_fixture_separates_reviewed_outcomes_from_scoring() -> None:
    fixture = json.loads(OS_REPLAY_PATH.read_text(encoding="utf-8"))

    assert fixture["privacy_posture"] == "refs_only_no_raw_transcript_bodies"
    assert fixture["typed_route_status"]["status"] == "generation_incompatible"
    assert len(fixture["cases"]) == 6
    assert len(fixture["reviewed_outcomes"]) == 6
    assert fixture["scoring_posture"] == {
        "prepared_case_count": 6,
        "reviewed_case_count": 6,
        "observed_operator_correction_count": 4,
        "scored_case_count": 0,
        "model_runs_complete": 0,
        "outcome_attribution_established": False,
        "benefit_established": False,
    }
    assert all(value is False for value in fixture["authority"].values())
    for case in fixture["cases"]:
        assert case["start_raw_ref"].startswith("raw:line:")
        assert case["expected_invariants"]
        assert case["current_owner_refs"]
        assert "intent" not in case
        assert "outcome" not in case
    for case in fixture["reviewed_outcomes"]:
        assert [
            item["role"] for item in case["bounded_raw_evidence"]
        ] == ["intent", "closeout", "terminal"]
        assert case["raw_bodies_embedded"] is False
        assert case["review"]["invariants_satisfied"] is True
        assert case["review"]["benefit_attribution"] == "not_established"
        assert case["r1_counterfactual"]["status"] == "unexecuted"


def test_streaming_array_reader_does_not_require_whole_file(tmp_path: Path) -> None:
    runner = load_runner()
    path = tmp_path / "rows.json"
    rows = [
        {"id": "a", "payload": "x" * 1_100_000},
        {"id": "b", "payload": "y" * 1_100_000},
    ]
    path.write_text(json.dumps(rows), encoding="utf-8")

    observed = list(runner.iter_json_array(path))

    assert [item["id"] for item in observed] == ["a", "b"]


def test_deterministic_selection_is_order_independent() -> None:
    runner = load_runner()
    forward = {"x": ["three", "one", "two"], "y": ["beta", "alpha"]}
    reverse = {key: list(reversed(value)) for key, value in forward.items()}

    assert runner.deterministic_selection(forward, {"x": 2, "y": 1}) == (
        runner.deterministic_selection(reverse, {"x": 2, "y": 1})
    )


def test_artifact_check_fails_closed_on_digest_drift(tmp_path: Path) -> None:
    runner = load_runner()
    artifact = tmp_path / "data.json"
    artifact.write_text("[]\n", encoding="utf-8")
    plan = {
        "public_benchmarks": [
            {
                "benchmark_id": "fixture",
                "artifacts": [
                    {
                        "relative_path": "data.json",
                        "bytes": artifact.stat().st_size,
                        "sha256": "0" * 64,
                    }
                ],
            }
        ]
    }

    checks, resolved = runner.artifact_checks(plan, tmp_path)

    assert checks[0]["status"] == "digest_mismatch"
    assert resolved == {}


def test_report_schema_forbids_benefit_and_landing_claims() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    benefit_schema = schema["properties"]["summary"]["properties"][
        "benefit_established"
    ]
    landing_schema = schema["properties"]["summary"]["properties"][
        "landing_performed"
    ]

    assert list(Draft202012Validator(benefit_schema).iter_errors(False)) == []
    assert list(Draft202012Validator(landing_schema).iter_errors(False)) == []
    assert list(Draft202012Validator(benefit_schema).iter_errors(True))
    assert list(Draft202012Validator(landing_schema).iter_errors(True))


def test_streaming_array_reader_rejects_non_array(tmp_path: Path) -> None:
    runner = load_runner()
    path = tmp_path / "object.json"
    path.write_text('{"not": "an array"}', encoding="utf-8")

    with pytest.raises(runner.EvidenceError, match="expected a JSON array"):
        list(runner.iter_json_array(path))


def test_reviewed_os_replay_fails_closed_on_raw_evidence_drift(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = load_runner()
    aoa_root = tmp_path / "aoa"
    session_dir = aoa_root / "sessions" / "fixture-session"
    block_dir = session_dir / "raw" / "blocks"
    block_dir.mkdir(parents=True)
    block_path = block_dir / "001__fixture.raw.jsonl"
    events = [
        {
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "user",
                "phase": None,
            },
        },
        {
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "assistant",
                "phase": "final_answer",
            },
        },
        {
            "type": "event_msg",
            "payload": {
                "type": "task_complete",
                "role": None,
                "phase": None,
            },
        },
    ]
    block_path.write_text(
        "".join(json.dumps(event) + "\n" for event in events),
        encoding="utf-8",
    )
    block_digest = runner.sha256_file(block_path)
    index = {
        "session_id": "fixture-session",
        "generation_id": "fixture-generation",
        "task_episodes": [
            {
                "episode_id": "task-0001",
                "stable_id": "fixture-session:task-0001:000001",
                "status": "closed",
                "event_range": {"from_line": 1, "to_line": 3},
                "start_user_ref": {"raw_ref": "raw:line:1"},
                "verification_refs": [],
                "answer_refs": [],
                "closeout_refs": [{"raw_ref": "raw:line:2"}],
            }
        ],
        "raw_blocks": {
            "blocks": [
                {
                    "path": str(block_path),
                    "status": "sealed",
                    "sha256": block_digest,
                    "source_range": {"from_line": 1, "to_line": 3},
                    "line_count": 3,
                }
            ]
        },
    }
    index_path = session_dir / "session.index.json"
    index_path.write_text(
        json.dumps(index, indent=2) + "\n",
        encoding="utf-8",
    )
    index_digest = runner.sha256_file(index_path)
    evidence = [
        {
            "role": "intent",
            "raw_ref": "raw:line:1",
            "block_ref": str(block_path.relative_to(aoa_root)),
            "block_sha256": block_digest,
            "block_line": 1,
            "envelope": {
                "event_type": "response_item",
                "item_type": "message",
                "role": "user",
                "phase": None,
            },
        },
        {
            "role": "closeout",
            "raw_ref": "raw:line:2",
            "block_ref": str(block_path.relative_to(aoa_root)),
            "block_sha256": block_digest,
            "block_line": 2,
            "envelope": {
                "event_type": "response_item",
                "item_type": "message",
                "role": "assistant",
                "phase": "final_answer",
            },
        },
        {
            "role": "terminal",
            "raw_ref": "raw:line:3",
            "block_ref": str(block_path.relative_to(aoa_root)),
            "block_sha256": block_digest,
            "block_line": 3,
            "envelope": {
                "event_type": "event_msg",
                "item_type": "task_complete",
                "role": None,
                "phase": None,
            },
        },
    ]
    fixture = {
        "privacy_posture": "refs_only_no_raw_transcript_bodies",
        "cases": [
                        {
                            "case_id": "prepared-fixture",
                "session_id": "fixture-session",
                "session_index_ref": str(index_path.relative_to(aoa_root)),
                "session_index_sha256": index_digest,
                "session_index_generation_id": "fixture-generation",
                "episode_id": "task-0001",
                "stable_episode_id": "fixture-session:task-0001:000001",
                "start_raw_ref": "raw:line:1",
                "closeout_ref_samples": ["raw:line:2"],
                "ref_counts": {
                    "verification": 0,
                    "answer": 0,
                    "closeout": 1,
                },
                "expected_invariants": ["raw outranks projection"],
                "current_owner_refs": ["fixture-owner"],
            }
        ],
        "reviewed_outcomes": [
            {
                "case_id": "reviewed-fixture",
                "session_id": "fixture-session",
                "session_index_ref": str(index_path.relative_to(aoa_root)),
                "session_index_sha256": index_digest,
                "session_index_generation_id": "fixture-generation",
                "episode_id": "task-0001",
                "stable_episode_id": "fixture-session:task-0001:000001",
                "episode_ref_counts": {
                    "verification": 0,
                    "answer": 0,
                    "closeout": 1,
                },
                "bounded_raw_evidence": evidence,
                "task_abstraction": "Verify one bounded legacy outcome.",
                "expected_invariants": ["raw outranks projection"],
                "current_owner_refs": ["fixture-owner"],
                "review": {
                    "reviewer_role": "bounded_source_evidence_review",
                    "outcome_state": "complete",
                    "operator_correction_count": 1,
                    "operator_load_observation": "One correction was observed.",
                    "projection_limitation": "",
                    "invariants_satisfied": True,
                    "benefit_attribution": "not_established",
                },
                "r1_counterfactual": {
                    "status": "unexecuted",
                    "eligible_owner_orientation": True,
                    "hypothesis": "The owner route may reduce correction cost.",
                },
                "raw_bodies_embedded": False,
            }
        ],
        "scoring_posture": {
            "prepared_case_count": 1,
            "reviewed_case_count": 1,
            "observed_operator_correction_count": 1,
            "scored_case_count": 0,
            "model_runs_complete": 0,
            "outcome_attribution_established": False,
            "benefit_established": False,
        },
    }
    fixture_path = tmp_path / "os-replay.json"
    fixture_path.write_text(
        json.dumps(fixture, indent=2) + "\n",
        encoding="utf-8",
    )
    anchor_path = tmp_path / "os-replay-anchors.json"
    anchor_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "posture": (
                    "closed_episode_inside_mutable_session_projection"
                ),
                "anchors": [
                    {
                        "case_id": "prepared-fixture",
                        "session_index_ref": str(
                            index_path.relative_to(aoa_root)
                        ),
                        "session_index_review_cutoff_sha256": index_digest,
                        "session_index_generation_id": "fixture-generation",
                        "episode_id": "task-0001",
                        "stable_episode_id": (
                            "fixture-session:task-0001:000001"
                        ),
                        "episode_projection_sha256": (
                            runner.canonical_sha256(
                                index["task_episodes"][0]
                            ).removeprefix("sha256:")
                        ),
                            "claim_limit": (
                                "Unrelated projection tails may change."
                            ),
                        },
                        {
                            "case_id": "reviewed-fixture",
                            "session_index_ref": str(
                                index_path.relative_to(aoa_root)
                            ),
                            "session_index_review_cutoff_sha256": index_digest,
                            "session_index_generation_id": "fixture-generation",
                            "episode_id": "task-0001",
                            "stable_episode_id": (
                                "fixture-session:task-0001:000001"
                            ),
                            "episode_projection_sha256": (
                                runner.canonical_sha256(
                                    index["task_episodes"][0]
                                ).removeprefix("sha256:")
                            ),
                            "claim_limit": (
                                "Unrelated projection tails may change."
                            ),
                        }
                    ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(runner, "OS_REPLAY_PATH", fixture_path)
    monkeypatch.setattr(runner, "OS_REPLAY_ANCHOR_PATH", anchor_path)

    assert runner.validate_os_replay(aoa_root) == fixture

    index["unrelated_projection_tail"] = {"episode_id": "task-0002"}
    index_path.write_text(
        json.dumps(index, indent=2) + "\n",
        encoding="utf-8",
    )
    fixture_path.write_text(
        json.dumps(fixture, indent=2) + "\n",
        encoding="utf-8",
    )

    assert runner.validate_os_replay(aoa_root) == fixture

    index["task_episodes"][0]["unreviewed_projection_change"] = True
    index_path.write_text(
        json.dumps(index, indent=2) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(runner.EvidenceError, match="episode projection digest"):
        runner.validate_os_replay(aoa_root)
    del index["task_episodes"][0]["unreviewed_projection_change"]
    index_path.write_text(
        json.dumps(index, indent=2) + "\n",
        encoding="utf-8",
    )

    fixture["reviewed_outcomes"][0]["bounded_raw_evidence"][1]["envelope"][
        "phase"
    ] = "commentary"
    fixture_path.write_text(
        json.dumps(fixture, indent=2) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(runner.EvidenceError, match="envelope drift"):
        runner.validate_os_replay(aoa_root)

    fixture["reviewed_outcomes"][0]["bounded_raw_evidence"][1]["envelope"][
        "phase"
    ] = "final_answer"
    fixture_path.write_text(
        json.dumps(fixture, indent=2) + "\n",
        encoding="utf-8",
    )
    block_path.write_text(
        block_path.read_text(encoding="utf-8").replace(
            "final_answer",
            "commentary",
        ),
        encoding="utf-8",
    )
    with pytest.raises(runner.EvidenceError, match="block digest drift"):
        runner.validate_os_replay(aoa_root)
