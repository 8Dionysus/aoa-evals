from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = BUNDLE_ROOT / "runners" / "run_phase13_accelerated_soak.py"
SCHEMA_PATH = BUNDLE_ROOT / "reports" / "phase13-accelerated-soak.schema.json"


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "phase13_accelerated_soak", RUNNER_PATH
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_accelerated_soak_is_durable_but_never_wall_clock(
    tmp_path: Path,
) -> None:
    runner = load_runner()
    report = runner.run(tmp_path)
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    Draft202012Validator(schema).validate(report)
    assert report["mode"] == {
        "accelerated_days": 30,
        "checkpoints_days": [7, 30],
        "wall_clock_elapsed_days": 0,
        "accelerated_replay_is_wall_clock_soak": False,
    }
    assert report["summary"]["accelerated_7d_complete"] is True
    assert report["summary"]["accelerated_30d_complete"] is True
    assert report["summary"]["wall_clock_7d_complete"] is False
    assert report["summary"]["wall_clock_30d_complete"] is False
    assert report["summary"]["benefit_established"] is False
    assert report["summary"]["landing_performed"] is False
    for arm in report["arms"]:
        assert arm["foreground_p99_latency_ms"] >= (
            arm["foreground_p50_latency_ms"]
        )
        assert arm["maintenance_p99_latency_ms"] >= (
            arm["maintenance_p50_latency_ms"]
        )


def test_fault_matrix_executes_transaction_and_erasure_guards(
    tmp_path: Path,
) -> None:
    runner = load_runner()
    fixture = json.loads(runner.FIXTURE_PATH.read_text(encoding="utf-8"))
    faults = {
        item["fault_id"]: item
        for item in runner.run_fault_matrix(tmp_path / "faults.sqlite3", fixture)
    }

    assert len(faults) == 14
    assert all(item["detected"] for item in faults.values())
    assert faults["duplicate_delivery"]["evidence"] == "idempotent_no_write"
    assert faults["crash_after_commit_before_ack"]["evidence"] == (
        "idempotent_no_write"
    )
    assert faults["queue_reorder"]["evidence"] == "version_conflict"
    assert faults["concurrent_update"]["evidence"] == (
        "winner=committed; loser=version_conflict"
    )
    assert faults["restore_after_erase"]["evidence"] == "blocked_by_tombstone"
