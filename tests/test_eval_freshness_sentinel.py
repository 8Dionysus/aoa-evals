from __future__ import annotations

import os
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_eval_freshness_sentinel as sentinel


def write_generated_dashboard(
    root: Path,
    *,
    age_hours: float = 0.0,
    payload: dict | None = None,
) -> None:
    path = root / "generated" / "eval_readiness_dashboard.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(payload or {}) + "\n", encoding="utf-8")
    mtime = datetime(2026, 6, 25, tzinfo=timezone.utc) - timedelta(hours=age_hours)
    os.utime(path, (mtime.timestamp(), mtime.timestamp()))


def base_dashboard() -> dict:
    return {
        "mcp_runtime_status": {"status": "ok", "json": {"freshness": {}}},
        "aoa_session_memory_freshness": {"status": "ok", "json_summary": {"recommendation": "ok"}},
        "local_eval_ports": {"summary": {"active": 0, "invalid": 0}},
        "workspace_git_drift": {"summary": {"dirty_repos": 0}},
    }


def test_sentinel_records_stale_mirror_as_warning_debt(tmp_path: Path) -> None:
    write_generated_dashboard(tmp_path)
    dashboard = base_dashboard()
    dashboard["mcp_runtime_status"]["json"]["freshness"] = {
        "status": "source_with_stale_mirror",
        "mirror_is_stale": True,
        "refresh_command": "scripts/aoa-sync-federation-surfaces --layer aoa-evals",
    }
    support = {
        "summary": {
            "unsafe_side_effect_scripts": 0,
            "by_review_status": {},
            "by_recommended_route": {},
        }
    }

    payload = sentinel.build_sentinel_payload(
        dashboard=dashboard,
        support_registry=support,
        evals_root=tmp_path,
        max_generated_age_hours=24,
        now=datetime(2026, 6, 25, tzinfo=timezone.utc),
    )

    assert payload["overall_severity"] == "warning"
    stale = {item["id"]: item for item in payload["signals"]}["mcp_federation_mirror_stale"]
    assert stale["severity"] == "warning"
    assert stale["owner"] == "abyss-stack/aoa-evals-mcp"
    assert stale["next_command"] == "scripts/aoa-sync-federation-surfaces --layer aoa-evals"
    assert sentinel.exit_code(payload, strict=False) == 0
    assert sentinel.exit_code(payload, strict=True) == 2


def test_sentinel_errors_on_unresolved_support_registry_review(tmp_path: Path) -> None:
    write_generated_dashboard(tmp_path)
    support = {
        "summary": {
            "unsafe_side_effect_scripts": 0,
            "by_review_status": {"manual_review_required": 1},
            "by_recommended_route": {},
        }
    }

    payload = sentinel.build_sentinel_payload(
        dashboard=base_dashboard(),
        support_registry=support,
        evals_root=tmp_path,
        max_generated_age_hours=24,
        now=datetime(2026, 6, 25, tzinfo=timezone.utc),
    )

    assert payload["overall_severity"] == "error"
    unresolved = {
        item["id"]: item for item in payload["signals"]
    }["support_registry_unresolved_manual_review"]
    assert unresolved["severity"] == "error"
    assert "unresolved manual review" in unresolved["reason"]
    assert sentinel.exit_code(payload, strict=False) == 2


def test_sentinel_warns_on_stale_generated_dashboard(tmp_path: Path) -> None:
    write_generated_dashboard(
        tmp_path,
        age_hours=0,
        payload={
            "source_projection": {
                "schema_version": "os_abyss_eval_source_projection_v1",
                "generated_at_utc": "2026-06-23T18:00:00Z",
                "identity": "source",
            },
            "workspace_observation": {
                "scope": "filesystem_workspace",
                "observed_at_utc": "2026-06-24T18:00:00Z",
            },
            "live_observation": {
                "status": "observed",
                "observed_at_utc": "2026-06-24T18:00:00Z",
            },
        },
    )
    support = {
        "summary": {
            "unsafe_side_effect_scripts": 0,
            "by_review_status": {},
            "by_recommended_route": {},
        }
    }

    payload = sentinel.build_sentinel_payload(
        dashboard=base_dashboard(),
        support_registry=support,
        evals_root=tmp_path,
        max_generated_age_hours=24,
        now=datetime(2026, 6, 25, tzinfo=timezone.utc),
    )

    age = {item["id"]: item for item in payload["signals"]}["generated_dashboard_age"]
    assert age["severity"] == "warning"
    assert age["next_command"] == (
        "python scripts/build_eval_readiness_dashboard.py --no-live-checks --write-generated"
    )


def test_sentinel_does_not_use_recent_mtime_as_projection_freshness(tmp_path: Path) -> None:
    write_generated_dashboard(
        tmp_path,
        payload={
            "source_projection": {
                "schema_version": "os_abyss_eval_source_projection_v1",
                "generated_at_utc": "2026-06-23T18:00:00Z",
                "identity": "source",
            }
        },
    )
    payload = sentinel.build_sentinel_payload(
        dashboard=base_dashboard(),
        support_registry={"summary": {}},
        evals_root=tmp_path,
        max_generated_age_hours=24,
        now=datetime(2026, 6, 25, tzinfo=timezone.utc),
    )
    age = {item["id"]: item for item in payload["signals"]}["generated_dashboard_age"]
    assert age["severity"] == "warning"
    assert age["status"] == "30.00h"


def test_sentinel_marks_legacy_and_invalid_timestamps_explicitly(tmp_path: Path) -> None:
    write_generated_dashboard(
        tmp_path,
        payload={
            "source_projection": {
                "schema_version": "os_abyss_eval_source_projection_v1",
                "generated_at_utc": "not-a-timestamp",
                "identity": "source",
            },
            "workspace_observation": {
                "scope": "filesystem_workspace",
                "observed_at_utc": "2030-01-01T00:00:00Z",
            },
            "live_observation": {"status": "not_observed", "observed_at_utc": None},
        },
    )
    payload = sentinel.build_sentinel_payload(
        dashboard=base_dashboard(),
        support_registry={"summary": {}},
        evals_root=tmp_path,
        max_generated_age_hours=24,
        now=datetime(2026, 6, 25, tzinfo=timezone.utc),
    )
    signals = {item["id"]: item for item in payload["signals"]}
    assert signals["generated_dashboard_age"]["status"] == "malformed"
    assert signals["workspace_observation_age"]["status"] == "future"
    assert signals["live_observation_age"]["status"] == "not_observed"
    assert payload["overall_severity"] == "error"


@pytest.mark.parametrize(
    ("dashboard", "expected_status", "expected_severity"),
    [
        ({}, "legacy/unknown", "warning"),
        ({"source_projection": {}}, "missing", "error"),
        (
            {"source_projection": {"generated_at_utc": None}},
            "malformed",
            "error",
        ),
        (
            {"source_projection": {"generated_at_utc": False}},
            "malformed",
            "error",
        ),
        (
            {"source_projection": {"generated_at_utc": 0}},
            "malformed",
            "error",
        ),
        (
            {"source_projection": {"generated_at_utc": []}},
            "malformed",
            "error",
        ),
        (
            {"source_projection": "2026-09-22T00:00:00Z"},
            "malformed",
            "error",
        ),
    ],
    ids=[
        "legacy-layer-absent",
        "new-layer-field-missing",
        "null",
        "false",
        "zero",
        "list",
        "scalar-layer",
    ],
)
def test_sentinel_distinguishes_legacy_missing_and_malformed_source_timestamps(
    tmp_path: Path,
    dashboard: dict,
    expected_status: str,
    expected_severity: str,
) -> None:
    write_generated_dashboard(tmp_path, payload=dashboard)

    result = sentinel.generated_age_signal(
        tmp_path,
        max_age_hours=24,
        now=datetime(2026, 6, 25, tzinfo=timezone.utc),
    )

    assert result["status"] == expected_status
    assert result["severity"] == expected_severity


def test_sentinel_does_not_treat_broken_json_as_legacy(tmp_path: Path) -> None:
    path = tmp_path / "generated" / "eval_readiness_dashboard.json"
    path.parent.mkdir(parents=True)
    path.write_text("{broken\n", encoding="utf-8")

    signals = [
        sentinel.generated_age_signal(
            tmp_path,
            max_age_hours=24,
            now=datetime(2026, 6, 25, tzinfo=timezone.utc),
        ),
        sentinel.workspace_observation_age_signal(
            tmp_path,
            max_age_hours=24,
            now=datetime(2026, 6, 25, tzinfo=timezone.utc),
        ),
        sentinel.live_observation_age_signal(
            tmp_path,
            max_age_hours=24,
            now=datetime(2026, 6, 25, tzinfo=timezone.utc),
        ),
    ]

    assert [item["status"] for item in signals] == ["malformed"] * 3
    assert all(item["severity"] == "error" for item in signals)
    assert all(item["status"] != "legacy/unknown" for item in signals)


def test_sentinel_treats_invalid_utf8_as_malformed_dashboard(tmp_path: Path) -> None:
    path = tmp_path / "generated" / "eval_readiness_dashboard.json"
    path.parent.mkdir(parents=True)
    path.write_bytes(b"\xff\xfe")

    result = sentinel.generated_age_signal(
        tmp_path,
        max_age_hours=24,
        now=datetime(2026, 6, 25, tzinfo=timezone.utc),
    )

    assert result["status"] == "malformed"
    assert result["severity"] == "error"


def test_sentinel_reports_dashboard_read_error_separately_from_legacy(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = tmp_path / "generated" / "eval_readiness_dashboard.json"
    path.parent.mkdir(parents=True)
    path.write_text("{}\n", encoding="utf-8")

    def fail_read(*_args: object, **_kwargs: object) -> str:
        raise OSError("synthetic read failure")

    monkeypatch.setattr(Path, "read_text", fail_read)
    result = sentinel.generated_age_signal(
        tmp_path,
        max_age_hours=24,
        now=datetime(2026, 6, 25, tzinfo=timezone.utc),
    )

    assert result["status"] == "read_error"
    assert result["severity"] == "error"
