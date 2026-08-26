from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "evals/boundary/aoa-organ-access-admission-integrity"


def test_progressive_exposure_matched_fixtures_and_report_contract() -> None:
    generator = BUNDLE / "runners/generate_exposure_fixtures.py"
    generated = subprocess.run(
        [sys.executable, str(generator), "--check"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert generated.returncode == 0, generated.stdout + generated.stderr

    runner = BUNDLE / "runners/review_exposure.py"
    result = subprocess.run(
        [sys.executable, str(runner), "run-scenarios"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    schema = json.loads(
        (BUNDLE / "reports/progressive-exposure.schema.json").read_text(
            encoding="utf-8"
        )
    )
    errors = sorted(Draft202012Validator(schema).iter_errors(report), key=str)
    assert not errors
    assert report["integrity_verdict"] == "supports_bounded_claim"
    assert report["economy"]["status"] == "not_run_baseline_admission_missing"
    assert report["activation_authorized"] is False
    assert report["execution_authorized"] is False
