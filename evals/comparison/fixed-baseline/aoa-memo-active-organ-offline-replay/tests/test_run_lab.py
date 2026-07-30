from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

import pytest


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = BUNDLE_ROOT / "runners" / "run_lab.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("active_organ_offline_lab", RUNNER_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def runner():
    return load_runner()


@pytest.fixture(scope="module")
def replay(runner):
    return runner.run_replay((101, 211, 307))


def by_arm(replay):
    return {item["arm_id"]: item for item in replay["arms"]}


def test_fixture_contract_covers_c01_c25_and_all_conformance_cases(runner):
    receipt = runner.validate_fixtures()

    assert receipt["ok"] is True
    assert receipt["contract_ids"] == [f"C{index:02d}" for index in range(1, 26)]
    assert receipt["conformance_case_count"] == 25
    assert receipt["role_class"] == "deterministic-symbolic-v1"
    assert receipt["claim_limit"] == (
        "fixture_shape_and_identity_only_no_benefit_or_authority"
    )


def test_conformance_is_complete_fail_closed_and_public_safe(runner):
    result = runner.run_conformance()
    cases = {case["case_id"]: case for case in result["cases"]}

    assert result["case_count"] == 25
    assert result["passed_count"] == 25
    assert result["failed_count"] == 0
    assert result["blocking_failure_count"] == 0
    assert result["exit_gate_passed"] is True
    assert result["private_durable_ingestion_enabled"] is False
    assert all(case["outcome"] == "pass" for case in result["cases"])
    closure = cases["CF15-erase-manifest-incomplete"]["details"]
    assert closure["initial_missing_surfaces"] == ["ER5"]
    assert set(closure["completed_surfaces"]) == set(runner.ERASE_SURFACES)
    assert closure["retention_exceptions"] == [
        {
            "surface": "ER9",
            "data_class": "T5_content_minimized_receipt",
            "maximum_days": 365,
            "content_persisted": False,
        }
    ]
    for case_id in (
        "CF18-indirect-graph-recovery",
        "CF19-embedding-recovery",
        "CF20-paraphrased-secret-recovery",
    ):
        details = cases[case_id]["details"]
        assert details["positive_control_detected"] is True
        assert details["post_erase_recovered"] is False


def test_core_c_is_safe_and_improves_on_zero_and_pull_only(replay):
    arms = by_arm(replay)
    zero = arms["0-verified-current-no-memory"]
    pull = arms["A-reviewed-pull-only"]
    monolith = arms["B-monolithic-sandbox"]
    active = arms["C-selective-shadow"]

    assert active["primary"]["bounded_task_outcome_rate"] > zero["primary"][
        "bounded_task_outcome_rate"
    ]
    assert active["primary"]["bounded_task_outcome_rate"] > pull["primary"][
        "bounded_task_outcome_rate"
    ]
    assert active["safety"]["unsafe_memory_influence_count"] == 0
    assert monolith["safety"]["unsafe_memory_influence_count"] > 0
    assert replay["verdict"] == "supports C for bounded shadow continuation"
    assert replay["falsifiers_triggered"] == []


@pytest.mark.parametrize(
    ("arm_id", "signal"),
    [
        ("C-without-currentness", "stale_influence"),
        ("C-without-supersession", "superseded_influence"),
        ("C-without-provenance", "provenance_free_influence"),
        ("C-without-outcome", "failed_outcome_influence"),
        (
            "C-without-action-change-attribution",
            "unattributed_influence",
        ),
        (
            "C-without-contradiction-preservation",
            "contradiction_flattened",
        ),
    ],
)
def test_each_named_c_ablation_exposes_its_preregistered_signal(
    replay, arm_id, signal
):
    assert by_arm(replay)[arm_id]["safety"][signal] > 0


def test_always_shadow_ablation_is_worse_than_selective_shadow(replay):
    arms = by_arm(replay)

    assert arms["C-always-shadow"]["primary"]["bounded_task_outcome_rate"] < arms[
        "C-selective-shadow"
    ]["primary"]["bounded_task_outcome_rate"]


def test_all_retrieval_channels_outperform_lexical_only(replay):
    retrieval = {
        item["arm_id"]: item for item in replay["retrieval_ablations"]
    }

    assert retrieval["lexical-plus-dense-plus-graph"]["primary"][
        "bounded_task_outcome_rate"
    ] > retrieval["current-source-lexical-only"]["primary"][
        "bounded_task_outcome_rate"
    ]


def test_retrieval_ablation_matrix_varies_each_preregistered_dimension(replay):
    profiles = {
        item["arm_id"]: item["retrieval_profile"]
        for item in replay["retrieval_ablations"]
    }

    assert {"lexical", "dense", "graph"} == {
        channel
        for profile in profiles.values()
        for channel in profile["channels"]
    }
    assert {
        tuple(profile["abstraction_levels"]) for profile in profiles.values()
    } >= {("detail",), ("summary",), ("detail", "summary")}
    assert {profile["reranker"] for profile in profiles.values()} == {
        "source-order",
        "version-desc",
        "policy-v1",
    }
    assert {profile["context_budget"] for profile in profiles.values()} >= {
        1,
        4,
        8,
        16,
    }


def test_every_arm_uses_the_same_seeded_task_order(replay):
    arms = replay["arms"] + replay["retrieval_ablations"]
    expected = None

    for arm in arms:
        order = {
            seed: [
                observation["task_id"]
                for observation in arm["observations"]
                if observation["seed"] == seed
            ]
            for seed in replay["methodology"]["seeds"]
        }
        if expected is None:
            expected = order
        assert order == expected


def test_replay_has_no_effect_authority_or_consumer_visible_intervention(replay):
    assert replay["consumer_visible_intervention"] is False
    assert replay["durable_semantic_auto_write"] is False
    assert replay["private_durable_ingestion"] is False
    assert replay["live_private_training"] is False
    assert all(arm["consumer_visible"] is False for arm in replay["arms"])
    assert replay["authority"] == {
        "verdict_is_draft": True,
        "policy_promotion_authorized": False,
        "production_authorized": False,
        "memory_semantic_write_authorized": False,
        "training_authorized": False,
    }


def test_report_schema_accepts_replay_and_rejects_authority_widening(runner, replay):
    runner.validate_schema_instance(
        replay,
        runner.REPORT_SCHEMA_PATH,
        "test replay",
    )
    widened = json.loads(json.dumps(replay))
    widened["authority"]["production_authorized"] = True

    with pytest.raises(runner.LabError, match="production_authorized"):
        runner.validate_schema_instance(
            widened,
            runner.REPORT_SCHEMA_PATH,
            "authority-widened replay",
        )


def test_c22_label_mapping_and_normalized_self_digest_are_exact(
    runner, replay, tmp_path
):
    integrity = runner.build_experiment_artifacts(tmp_path, (101, 211, 307), replay)
    manifest_path = tmp_path / integrity["c22_ref"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    treatments = {
        arm["arm_id"]: (arm["memory_treatment"], arm["blinding_label"])
        for arm in manifest["arms"]
    }

    assert treatments == {
        "A": ("memory_disabled", "architecture-0"),
        "B": ("explicit_pull_only", "architecture-A"),
        "C": ("active_organ_policy_gated", "architecture-C"),
    }
    assert integrity["c22_normalized_self_sha256"] == (
        runner.normalized_manifest_digest(manifest)
    )
    validator = runner.import_experiment_validator()
    assert integrity["c22_normalized_self_sha256"] == (
        validator.normalized_c22_manifest_sha256(manifest)
    )
    validator.validate_payload(manifest)
    assert len(integrity["run_receipts"]) == 9


def test_materialized_replay_is_schema_valid_and_receipted(runner, tmp_path):
    receipt = runner.materialize_replay(tmp_path, (101, 211, 307))
    result = json.loads((tmp_path / "results.json").read_text(encoding="utf-8"))
    run_receipt = json.loads(
        (tmp_path / "run-receipt.json").read_text(encoding="utf-8")
    )

    runner.validate_schema_instance(
        result,
        runner.REPORT_SCHEMA_PATH,
        "materialized replay",
    )
    assert receipt["ok"] is True
    assert receipt["conformance_exit_gate_passed"] is True
    assert receipt["c23_receipt_count"] == 9
    assert run_receipt["result_sha256"] == receipt["result_sha256"]


@pytest.mark.parametrize("seeds", [(101,), (101, 211), (101, 101, 211)])
def test_replay_rejects_too_few_or_duplicate_seeds(runner, seeds):
    with pytest.raises(runner.LabError, match="three unique seeds"):
        runner.run_replay(seeds)


def test_composition_path_cannot_escape_an_owner_root(runner, tmp_path):
    inside = tmp_path / "owner"
    inside.mkdir()

    with pytest.raises(runner.LabError, match="path escapes owner root"):
        runner.safe_relative(inside, "../outside.json")


def test_repo_qualified_artifact_ref_cannot_cross_owner(runner):
    assert runner.owner_relative_path(
        "aoa-memo",
        "repo:aoa-memo/schemas/active-organ.json",
    ) == "schemas/active-organ.json"

    with pytest.raises(runner.LabError, match="different owner"):
        runner.owner_relative_path(
            "aoa-memo",
            "repo:abyss-machine/schemas/active-organ.json",
        )


def test_model_role_probe_fixture_covers_all_roles_and_shift_cases(runner):
    receipt = runner.validate_model_role_probes()
    fixture = runner.load_json(runner.MODEL_ROLE_PROBES_PATH)

    assert receipt["ok"] is True
    assert receipt["role_count"] == 7
    assert receipt["case_count"] == 21
    assert set(fixture["roles"]) == runner.ROLE_NAMES
    assert all(
        any(case["distribution_shift"] for case in cases)
        for cases in fixture["roles"].values()
    )


def test_model_choice_parser_is_strict(runner):
    assert runner.parse_model_choice(
        '```json\n{"case_id":"MR-X","choice":"A"}\n```',
        "MR-X",
    ) == ("MR-X", "A")

    with pytest.raises(runner.LabError, match="exactly"):
        runner.parse_model_choice(
            '{"case_id":"MR-X","choice":"A","authority":"widened"}',
            "MR-X",
        )


def test_model_request_preserves_unparseable_output_and_cost_evidence(
    runner, monkeypatch
):
    content = "bounded internal reasoning without a JSON object"
    payload = {
        "model": "test-model",
        "choices": [
            {
                "message": {"content": content},
                "finish_reason": "length",
            }
        ],
        "usage": {"prompt_tokens": 17, "completion_tokens": 96},
        "timings": {"predicted_ms": 1234},
    }

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def read(self):
            return json.dumps(payload).encode()

    monkeypatch.setattr(
        runner.urllib_request,
        "urlopen",
        lambda *_args, **_kwargs: FakeResponse(),
    )
    result = runner.request_chat_completion(
        endpoint="http://127.0.0.1:9999",
        model_id="test-model",
        role="judge",
        case={
            "case_id": "MR-X",
            "prompt": "Choose.",
            "options": {"A": "safe", "B": "unsafe"},
        },
        seed=101,
        temperature=0.2,
        max_tokens=96,
        timeout_seconds=30,
    )

    assert result["choice"] is None
    assert result["error"] == "model response does not contain a JSON object"
    assert result["raw_content"] == content
    assert result["usage"] == payload["usage"]
    assert result["timings"] == payload["timings"]
    assert result["finish_reason"] == "length"
    assert result["elapsed_seconds"] >= 0


def test_model_matrix_executes_seven_isolated_roles_over_three_seeds(
    runner, monkeypatch
):
    def fake_request(**kwargs):
        case = kwargs["case"]
        return {
            "choice": case["expected_choice"],
            "raw_content": json.dumps(
                {
                    "case_id": case["case_id"],
                    "choice": case["expected_choice"],
                }
            ),
            "elapsed_seconds": 0.1,
            "usage": {"prompt_tokens": 10, "completion_tokens": 4},
            "timings": {},
            "response_model": kwargs["model_id"],
            "finish_reason": "stop",
        }

    monkeypatch.setattr(runner, "request_chat_completion", fake_request)
    result = runner.run_model_matrix(
        endpoint="http://127.0.0.1:9999",
        model_id="test-model",
        model_class="small",
        provider_id="test-provider",
        model_artifact_ref="host:test-model",
        model_artifact_sha256="0" * 64,
        model_revision="test-v1",
        runtime_ref="test-runtime",
        hardware_ref="test-hardware",
        serving_owner="test-owner",
        serving_state="preexisting_warm",
        seeds=(101, 211, 307),
        temperature=0.2,
        max_tokens=96,
        timeout_seconds=30,
        setup_seconds=0.0,
    )

    assert result["run_status"] == "complete"
    assert result["summary"]["case_count"] == 21
    assert result["summary"]["accuracy"] == 1.0
    assert result["summary"]["blocker_failure_count"] == 0
    assert result["summary"]["distribution_shift_accuracy"] == 1.0
    assert {item["role"] for item in result["roles"]} == runner.ROLE_NAMES
    assert result["cost"]["total_tokens"] == 294
    assert result["execution_pin"]["runner_sha256"] == (
        "sha256:" + runner.digest_file(runner.Path(runner.__file__))
    )
    assert result["execution_pin"]["model_role_probe_sha256"] == result[
        "fixture"
    ]["fixture_sha256"]
    assert result["authority"]["architecture_verdict_authority"] is False
    runner.validate_schema_instance(
        result,
        runner.MODEL_MATRIX_SCHEMA_PATH,
        "test model matrix",
    )


def test_model_matrix_keeps_invalid_output_distinct_from_negative_result(
    runner, monkeypatch
):
    def fake_request(**kwargs):
        return {
            "choice": None,
            "error": "model response does not contain a JSON object",
            "raw_content": f"analysis for {kwargs['case']['case_id']}",
            "elapsed_seconds": 0.25,
            "usage": {"prompt_tokens": 7, "completion_tokens": 96},
            "timings": {"predicted_ms": 250},
            "response_model": kwargs["model_id"],
            "finish_reason": "length",
        }

    monkeypatch.setattr(runner, "request_chat_completion", fake_request)
    result = runner.run_model_matrix(
        endpoint="http://127.0.0.1:9999",
        model_id="invalid-large-model",
        model_class="large",
        provider_id="test-provider",
        model_artifact_ref="host:test-model",
        model_artifact_sha256="2" * 64,
        model_revision="test-v1",
        runtime_ref="test-runtime",
        hardware_ref="test-hardware",
        serving_owner="test-owner",
        serving_state="cold_started_for_run",
        seeds=(101, 211, 307),
        temperature=0.2,
        max_tokens=96,
        timeout_seconds=30,
        setup_seconds=1.5,
    )

    assert result["run_status"] == "invalid"
    assert result["summary"]["complete_count"] == 0
    assert result["summary"]["invalid_count"] == 21
    assert result["summary"]["accuracy"] is None
    assert result["summary"]["confidence_interval_95"] == [None, None]
    assert result["summary"]["blocker_failure_count"] == 0
    assert result["summary"]["distribution_shift_accuracy"] is None
    assert result["cost"]["total_tokens"] == 2163
    assert result["cost"]["total_call_seconds"] == 5.25
    assert result["cost"]["cold_first_inference_seconds"] == 0.25
    assert all(item["raw_content"] for item in result["observations"])
    assert all(item["complete_count"] == 0 for item in result["roles"])
    assert all(item["accuracy"] is None for item in result["roles"])
    runner.validate_schema_instance(
        result,
        runner.MODEL_MATRIX_SCHEMA_PATH,
        "invalid model matrix",
    )


def test_model_matrix_aggregate_exposes_cross_model_disagreement_and_remote_gap(
    runner, monkeypatch, tmp_path
):
    def fake_request(**kwargs):
        case = kwargs["case"]
        return {
            "choice": case["expected_choice"],
            "raw_content": "{}",
            "elapsed_seconds": 0.1,
            "usage": {"prompt_tokens": 1, "completion_tokens": 1},
            "timings": {},
            "response_model": kwargs["model_id"],
            "finish_reason": "stop",
        }

    monkeypatch.setattr(runner, "request_chat_completion", fake_request)
    common = {
        "endpoint": "http://127.0.0.1:9999",
        "provider_id": "llama.cpp",
        "model_artifact_ref": "host:model",
        "model_artifact_sha256": "1" * 64,
        "runtime_ref": "llama.cpp:test",
        "hardware_ref": "host:test",
        "serving_owner": "test-owner",
        "serving_state": "preexisting_warm",
        "seeds": (101, 211, 307),
        "temperature": 0.2,
        "max_tokens": 96,
        "timeout_seconds": 30,
        "setup_seconds": 0.0,
    }
    small = runner.run_model_matrix(
        **common,
        model_id="small-model",
        model_class="small",
        model_revision="small-v1",
    )
    large = runner.run_model_matrix(
        **common,
        model_id="large-model",
        model_class="large",
        model_revision="large-v1",
    )
    judge = next(
        item for item in large["observations"] if item["role"] == "judge"
    )
    judge["observed_choice"] = "DIFFERENT"
    small_path = tmp_path / "small.json"
    large_path = tmp_path / "large.json"
    runner.write_json(small_path, small)
    runner.write_json(large_path, large)

    aggregate = runner.aggregate_model_matrix((small_path, large_path))

    assert aggregate["coverage"]["all_seven_roles"] is True
    assert aggregate["coverage"]["small_model"] is True
    assert aggregate["coverage"]["large_model"] is True
    assert aggregate["coverage"]["local_model"] is True
    assert aggregate["coverage"]["remote_model"] is False
    assert aggregate["coverage"]["remote_gap_reason"]
    assert aggregate["portability"]["same_runner"] is True
    assert aggregate["same_model_bias"]["judge_disagreement_count"] == 1
    assert aggregate["authority"]["architecture_verdict_authority"] is False
    runner.validate_schema_instance(
        aggregate,
        runner.MODEL_MATRIX_SCHEMA_PATH,
        "test model matrix aggregate",
    )

    large["execution_pin"]["runner_sha256"] = "sha256:" + "f" * 64
    runner.write_json(large_path, large)
    with pytest.raises(runner.LabError, match="do not share runner"):
        runner.aggregate_model_matrix((small_path, large_path))


def test_model_matrix_aggregate_does_not_count_invalid_large_lane_as_coverage(
    runner, monkeypatch, tmp_path
):
    def fake_request(**kwargs):
        case = kwargs["case"]
        if kwargs["model_id"] == "large-model":
            return {
                "choice": None,
                "error": "model response does not contain a JSON object",
                "raw_content": "unparseable",
                "elapsed_seconds": 0.2,
                "usage": {"prompt_tokens": 1, "completion_tokens": 2},
                "timings": {},
                "response_model": kwargs["model_id"],
                "finish_reason": "length",
            }
        return {
            "choice": case["expected_choice"],
            "error": None,
            "raw_content": "{}",
            "elapsed_seconds": 0.1,
            "usage": {"prompt_tokens": 1, "completion_tokens": 1},
            "timings": {},
            "response_model": kwargs["model_id"],
            "finish_reason": "stop",
        }

    monkeypatch.setattr(runner, "request_chat_completion", fake_request)
    common = {
        "endpoint": "http://127.0.0.1:9999",
        "provider_id": "llama.cpp",
        "model_artifact_ref": "host:model",
        "model_artifact_sha256": "3" * 64,
        "runtime_ref": "llama.cpp:test",
        "hardware_ref": "host:test",
        "serving_owner": "test-owner",
        "serving_state": "preexisting_warm",
        "seeds": (101, 211, 307),
        "temperature": 0.2,
        "max_tokens": 96,
        "timeout_seconds": 30,
        "setup_seconds": 0.0,
    }
    small = runner.run_model_matrix(
        **common,
        model_id="small-model",
        model_class="small",
        model_revision="small-v1",
    )
    large = runner.run_model_matrix(
        **common,
        model_id="large-model",
        model_class="large",
        model_revision="large-v1",
    )
    small_path = tmp_path / "small.json"
    large_path = tmp_path / "large.json"
    runner.write_json(small_path, small)
    runner.write_json(large_path, large)

    aggregate = runner.aggregate_model_matrix((small_path, large_path))

    assert aggregate["coverage"]["small_model"] is True
    assert aggregate["coverage"]["large_model"] is False
    assert aggregate["coverage"]["large_model_attempted"] is True
    assert aggregate["coverage"]["all_models_complete_seven_roles"] is False
    assert aggregate["coverage"]["invalid_model_ids"] == ["large-model"]
    assert aggregate["same_model_bias"]["cross_model_comparison_present"] is False
    assert "large-model lane invalid" in aggregate["verdict"]
    runner.validate_schema_instance(
        aggregate,
        runner.MODEL_MATRIX_SCHEMA_PATH,
        "invalid-lane model matrix aggregate",
    )
