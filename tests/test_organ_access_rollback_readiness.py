from __future__ import annotations

import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
    REPO_ROOT
    / "evals"
    / "boundary"
    / "aoa-organ-access-admission-integrity"
    / "runners"
    / "review_rollback.py"
)
SPEC = importlib.util.spec_from_file_location("review_rollback", RUNNER_PATH)
assert SPEC is not None and SPEC.loader is not None
review_rollback = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(review_rollback)


def _write(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    path.chmod(0o600)
    return path


def test_rollback_negative_suite_is_green() -> None:
    report, passed = review_rollback.run_negative_suite()

    assert passed is True
    assert report["scenario_count"] == 11
    assert report["failed_count"] == 0


def test_reviews_exact_candidate_without_authorizing_effects(tmp_path: Path) -> None:
    candidate_path = _write(
        tmp_path / "candidate.json",
        review_rollback._fixture_candidate(),
    )
    report, passed = review_rollback.review_candidate(
        candidate_path,
        reviewed_at=datetime(2026, 8, 1, 0, 1, tzinfo=timezone.utc),
    )
    schema = json.loads(review_rollback.REVIEW_SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(report)

    assert passed is True
    assert report["verdict"] == "supported_bounded"
    assert report["rollback_candidate_supported"] is True
    assert report["rollback_executed"] is False
    assert report["admission_change_authorized"] is False
    assert report["actual_effects"] == []


def test_private_review_output_is_mode_0600(tmp_path: Path) -> None:
    output = tmp_path / "review" / "result.json"
    review_rollback.write_private_json(output, {"bounded": True})

    assert output.stat().st_mode & 0o777 == 0o600


def test_rejects_current_canary_route_even_when_resigned() -> None:
    candidate = review_rollback._fixture_candidate()
    candidate["last_known_good"]["canary_route"] = (
        "runbook://mcp-canary/aoa-kag/read"
    )
    review_rollback._resign(candidate)
    issues = review_rollback.validate_candidate(
        candidate,
        reviewed_at=datetime(2026, 8, 1, 0, 1, tzinfo=timezone.utc),
    )

    assert "lkg_canary_not_distinct" in issues
