from __future__ import annotations

import importlib.util
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
PREPARE_PATH = BUNDLE_ROOT / "runners" / "prepare_phase13_lme_v1.py"
MODEL_PATH = BUNDLE_ROOT / "runners" / "run_phase13_model_lane.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_lexical_retrieval_uses_question_terms_not_answer_markers() -> None:
    prepare = load_module("phase13_prepare", PREPARE_PATH)
    row = {
        "question": "Which garden tool did I buy?",
        "haystack_session_ids": ["unrelated", "matching"],
        "haystack_dates": ["2026/01/01", "2026/01/02"],
        "haystack_sessions": [
            [
                {
                    "role": "user",
                    "content": "I watched a film.",
                    "has_answer": True,
                }
            ],
            [
                {
                    "role": "user",
                    "content": "The garden tool purchase was a shovel.",
                    "has_answer": False,
                }
            ],
        ],
    }

    assert prepare.lexical_indices(row)[0] == 1


def test_render_sessions_obeys_context_budget() -> None:
    prepare = load_module("phase13_prepare_budget", PREPARE_PATH)
    row = {
        "haystack_session_ids": ["one", "two"],
        "haystack_dates": ["2026/01/01", "2026/01/02"],
        "haystack_sessions": [
            [{"role": "user", "content": "x" * 2000}],
            [{"role": "user", "content": "y" * 2000}],
        ],
    }

    context, selected = prepare.render_sessions(row, [0, 1], 1000)

    assert len(context) <= 1000
    assert selected == ["one"]


def test_local_scoring_is_descriptive_and_normalized() -> None:
    model = load_module("phase13_model", MODEL_PATH)

    assert model.normalized_match(
        "The answer is: GPS system.", "GPS system"
    )
    assert model.token_f1(
        "GPS system", "GPS system not functioning"
    ) == pytest.approx(2 / 3)
    assert model.normalized_match("UNKNOWN", "GPS system") is False
    assert model.normalized_match("The answer is 5.", 5)
    assert model.token_f1("5", 5) == 1.0


def test_percentile_is_stable_for_small_samples() -> None:
    model = load_module("phase13_model_percentile", MODEL_PATH)

    assert model.percentile([], 0.95) == 0.0
    assert model.percentile([30.0, 10.0, 20.0], 0.5) == 20.0
    assert model.percentile([30.0, 10.0, 20.0], 0.99) == 30.0


def test_model_lane_resumes_exact_checkpoint_without_replaying(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    model = load_module("phase13_model_resume", MODEL_PATH)
    evidence = tmp_path / "host.json"
    evidence.write_text("{}\n", encoding="utf-8")
    evidence_sha = "sha256:" + hashlib.sha256(evidence.read_bytes()).hexdigest()
    prompts = tmp_path / "prompts.jsonl"
    rows = []
    for index, arm_id in enumerate(("A", "B")):
        prompt_text = f"prompt {index}"
        rows.append(
            {
                "prompt_id": f"prompt-{index}",
                "question_id": f"question-{index}",
                "question_type": "single-session-user",
                "arm_id": arm_id,
                "prompt": prompt_text,
                "prompt_sha256": "sha256:"
                + hashlib.sha256(prompt_text.encode()).hexdigest(),
                "expected_answer": "answer",
            }
        )
    prompts.write_text(
        "".join(json.dumps(row) + "\n" for row in rows),
        encoding="utf-8",
    )
    args = SimpleNamespace(
        prompts=prompts,
        output=tmp_path / "report.json",
        checkpoint=tmp_path / "checkpoint.jsonl",
        endpoint="http://127.0.0.1:9999",
        model_label="fixture",
        model_id="fixture-model",
        model_revision="1234567",
        runtime_id="fixture-runtime",
        resource_policy_ref=evidence,
        resource_policy_sha256=evidence_sha,
        host_status_ref=evidence,
        host_status_sha256=evidence_sha,
        seed=1307,
        max_tokens=8,
        timeout_seconds=1,
        limit=None,
        progress_every=0,
    )
    calls: list[str] = []

    def interrupted_invoke(endpoint, model_id, prompt, **kwargs):
        calls.append(prompt)
        if len(calls) == 2:
            raise KeyboardInterrupt
        return "answer", {}, 200, 1.0

    monkeypatch.setattr(model, "invoke", interrupted_invoke)
    with pytest.raises(KeyboardInterrupt):
        model.run(args)

    resumed_calls: list[str] = []

    def resumed_invoke(endpoint, model_id, prompt, **kwargs):
        resumed_calls.append(prompt)
        return "answer", {}, 200, 1.0

    monkeypatch.setattr(model, "invoke", resumed_invoke)
    report = model.run(args)

    assert calls == ["prompt 0", "prompt 1"]
    assert resumed_calls == ["prompt 1"]
    assert report["execution"]["resumed_observation_count"] == 1
    assert report["execution"]["complete_count"] == 2
