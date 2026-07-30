from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest


PART_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[5]
SCRIPT = (
    PART_ROOT / "scripts" / "validate_active_organ_experiment_contracts.py"
)
DOC = PART_ROOT / "docs" / "ACTIVE_ORGAN_EXPERIMENT_CONTRACTS.md"


def load_validator():
    spec = importlib.util.spec_from_file_location(
        "active_organ_experiment_contract_validator",
        SCRIPT,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_positive_contract_examples_and_status_coverage() -> None:
    validator = load_validator()
    result = validator.validate_all()

    assert result["ok"] is True
    assert result["contracts"] == {"C21": 1, "C22": 1, "C23": 5}
    assert set(result["c23_statuses"]) == {
        "complete",
        "partial",
        "invalid",
        "aborted",
        "blocked",
    }
    assert result["negative_cases"] == 11
    assert result["claim_limit"] == (
        "validation_only_no_benefit_or_production_authority"
    )


def test_every_negative_mutation_fails_with_expected_route() -> None:
    validator = load_validator()
    corpus = validator.load_json(validator.NEGATIVE_EXAMPLES)
    schema_validators = validator.validators()

    for case in corpus["cases"]:
        payload = copy.deepcopy(
            validator.load_json(validator.EXAMPLE_ROOT / case["base_example"])
        )
        for pointer, value in case["set"].items():
            validator.apply_json_pointer(payload, pointer, value)
        with pytest.raises(validator.ContractError) as error:
            validator.validate_payload(payload, schema_validators)
        assert case["expected_error"] in str(error.value), case["case_id"]


def test_schema_property_sweep_rejects_missing_required_and_unknown_fields() -> None:
    validator = load_validator()
    schema_validators = validator.validators()

    for example_path in validator.POSITIVE_EXAMPLES:
        payload = validator.load_json(example_path)
        contract_id = payload["contract_id"]
        schema = validator.load_json(validator.SCHEMA_PATHS[contract_id])

        unknown = copy.deepcopy(payload)
        unknown["unexpected_contract_field"] = True
        with pytest.raises(validator.ContractError):
            validator.validate_payload(unknown, schema_validators)

        for required_field in schema["required"]:
            missing = copy.deepcopy(payload)
            del missing[required_field]
            with pytest.raises(validator.ContractError):
                validator.validate_payload(missing, schema_validators)


def test_green_process_does_not_establish_benefit() -> None:
    validator = load_validator()
    invalid = validator.load_json(
        validator.EXAMPLE_ROOT
        / "active_organ_memory_run_status_receipt.invalid.example.json"
    )

    assert invalid["green_process"] is True
    assert invalid["usable_for_comparison"] is False
    assert invalid["benefit_claim_state"] == "not_established_by_run_status"
    assert invalid["authority"]["benefit_authority"] is False


def test_c22_self_digest_is_canonical_and_tamper_evident() -> None:
    validator = load_validator()
    manifest = validator.load_json(
        validator.EXAMPLE_ROOT
        / "active_organ_memory_experiment_manifest.example.json"
    )

    assert manifest["preregistration"]["manifest_sha256"] == (
        validator.normalized_c22_manifest_sha256(manifest)
    )

    tampered = copy.deepcopy(manifest)
    tampered["bounded_question"] += " Tampered."
    with pytest.raises(
        validator.ContractError,
        match="preregistration/manifest_sha256",
    ):
        validator.validate_payload(tampered)


def test_owner_boundary_and_migration_contract_are_explicit() -> None:
    text = DOC.read_text(encoding="utf-8")
    for token in (
        "aoa-memo",
        "aoa-sdk",
        "abyss-stack",
        "abyss-machine",
        "aoa-stats",
        "bounded claim and verdict",
        "production or policy authority",
        "A: `memory_disabled`",
        "B: `explicit_pull_only`",
        "C: `active_organ_policy_gated`",
        "new schema version",
        "supersedes_receipt_ref",
        "64 zeroes",
    ):
        assert token in text


def test_validator_cli_is_read_only_and_green() -> None:
    before = {
        path: path.read_bytes()
        for path in (
            *load_validator().SCHEMA_PATHS.values(),
            *load_validator().POSITIVE_EXAMPLES,
            load_validator().NEGATIVE_EXAMPLES,
        )
    }
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    after = {path: path.read_bytes() for path in before}

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["negative_cases"] == 11
    assert before == after
