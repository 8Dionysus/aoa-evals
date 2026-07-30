from __future__ import annotations

import importlib.util
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = BUNDLE_ROOT / "runners" / "run_phase13_wall_clock_soak.py"


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "phase13_wall_clock_soak", RUNNER_PATH
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_wall_clock_completion_cannot_be_created_by_tick_count() -> None:
    runner = load_runner()
    now = datetime.now(UTC)

    assert (now - (now - timedelta(hours=100))).total_seconds() < 7 * 86400
    assert runner.percentile([1.0] * 100, 0.99) == 1.0


def test_percentile_and_optional_extrema_are_empty_safe() -> None:
    runner = load_runner()

    assert runner.percentile([], 0.99) == 0.0
    assert runner.optional_min([]) is None
    assert runner.optional_max([]) is None
    assert runner.optional_min([3, 1, 2]) == 1
    assert runner.optional_max([3, 1, 2]) == 3
