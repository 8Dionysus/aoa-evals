from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from jsonschema import Draft202012Validator


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = BUNDLE_ROOT / "runners" / "run_episodic_utility_lab.py"
FIXTURE_PATH = BUNDLE_ROOT / "fixtures" / "episodic-utility-cases.json"
REPORT_SCHEMA_PATH = BUNDLE_ROOT / "reports" / "episodic-utility.schema.json"


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "aoa_active_organ_episodic_utility_runner_test",
        RUNNER_PATH,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_phase9_fixture_covers_required_utility_and_adversarial_routes() -> None:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    cases = fixture["cases"]
    states = {case["expected_proposal_state"] for case in cases}
    mutations = {case["synthetic_mutation"] for case in cases}

    assert len(cases) == 6
    assert states == {
        "bounded_adjustment_proposed",
        "frozen",
        "preserve_critical",
    }
    assert {
        "accidental_success",
        "terminal_failure",
        "critical_harm",
    }.issubset(mutations)
    assert any(case["reward_hacking_passed"] is False for case in cases)
    assert all(case["access_count_probe"] == [0, 1000000] for case in cases)
    assert fixture["forbidden_effects"] == [
        "semantic_promotion",
        "semantic_deletion",
        "semantic_retraction",
        "owner_change",
        "tenant_expansion",
        "permission_expansion",
        "automatic_policy_self_approval",
    ]


def test_phase9_report_schema_and_digest_helper_are_strict() -> None:
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
        "source-local-outcome-qualified-utility-mechanism-no-deployment"
    )
    assert schema["properties"]["authority"]["properties"][
        "landing_performed"
    ]["const"] is False
