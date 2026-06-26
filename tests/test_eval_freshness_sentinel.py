from __future__ import annotations

import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_eval_freshness_sentinel as sentinel


def write_generated_dashboard(root: Path, *, age_hours: float = 0.0) -> None:
    path = root / "generated" / "eval_readiness_dashboard.json"
    path.parent.mkdir(parents=True)
    path.write_text("{}\n", encoding="utf-8")
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
    write_generated_dashboard(tmp_path, age_hours=30)
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
    assert age["next_command"] == "python scripts/build_eval_readiness_dashboard.py --write-generated"
