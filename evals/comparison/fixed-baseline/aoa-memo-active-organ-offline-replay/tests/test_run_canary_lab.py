from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import random

from jsonschema import Draft202012Validator


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = BUNDLE_ROOT / "runners" / "run_canary_lab.py"
FIXTURE_PATH = BUNDLE_ROOT / "fixtures" / "canary-orientation-cases.json"
REPORT_SCHEMA_PATH = BUNDLE_ROOT / "reports" / "canary-orientation.schema.json"


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "aoa_active_organ_canary_runner_test",
        RUNNER_PATH,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_canary_fixture_preregisters_balanced_outcome_blind_assignment() -> None:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    case_ids = fixture["positive_case_ids"]

    assert len(case_ids) == 12
    assert len(set(case_ids)) == len(case_ids)
    assert fixture["experiment"]["assignment"] == (
        "seeded-balanced-randomized-holdout"
    )
    assert fixture["experiment"]["assignment_uses_outcomes"] is False
    assert fixture["experiment"]["canary_fraction"] == 0.5
    for seed in (17, 29, 43):
        order = list(case_ids)
        random.Random(seed).shuffle(order)
        assert len(set(order[: len(order) // 2])) == 6


def test_canary_report_schema_and_digest_helpers_are_strict() -> None:
    runner = load_runner()
    schema = json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)

    payload = {
        "b": 2,
        "a": 1,
        "report_digest": "sha256:" + ("0" * 64),
    }
    assert runner.canonical_digest(
        payload,
        exclude={"report_digest"},
    ) == runner.canonical_digest({"a": 1, "b": 2})
    assert schema["properties"]["evidence_scope"]["const"] == (
        "source-local-randomized-canary-mechanism-no-deployment"
    )
    assert schema["properties"]["authority"]["properties"][
        "landing_performed"
    ]["const"] is False
