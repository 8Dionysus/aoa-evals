#!/usr/bin/env python3
"""Run a passive natural-load wall-clock durability campaign."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import shutil
import sqlite3
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = BUNDLE_ROOT / "fixtures" / "phase13-wall-clock-soak.json"
SCHEMA_PATH = BUNDLE_ROOT / "reports" / "phase13-wall-clock-soak.schema.json"
RUNNER_PATH = Path(__file__).resolve()
ARM_IDS = ("A", "B", "C")


class WallClockSoakError(RuntimeError):
    """Raised when campaign identity or durable evidence drifts."""


def utc_now() -> datetime:
    return datetime.now(UTC)


def render_time(value: datetime) -> str:
    return value.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        handle.write(json.dumps(value, indent=2, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def append_jsonl(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def percentile(values: list[float], quantile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(round((len(ordered) - 1) * quantile), len(ordered) - 1)
    return ordered[index]


def memory_observation() -> dict[str, Any]:
    meminfo: dict[str, int] = {}
    for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
        key, raw_value = line.split(":", 1)
        parts = raw_value.strip().split()
        if parts:
            meminfo[key] = int(parts[0]) * 1024
    pressure: dict[str, float] = {}
    for line in Path("/proc/pressure/memory").read_text(
        encoding="utf-8"
    ).splitlines():
        parts = line.split()
        lane = parts[0]
        values = dict(item.split("=", 1) for item in parts[1:])
        pressure[f"{lane}_avg10"] = float(values["avg10"])
    return {
        "mem_available_bytes": meminfo["MemAvailable"],
        "psi_some_avg10": pressure["some_avg10"],
        "psi_full_avg10": pressure["full_avg10"],
    }


def thermal_observation() -> dict[str, Any]:
    values: list[float] = []
    candidates = [
        *Path("/sys/class/hwmon").glob("hwmon*/temp*_input"),
        *Path("/sys/class/thermal").glob("thermal_zone*/temp"),
    ]
    for path in candidates:
        try:
            raw = float(path.read_text(encoding="utf-8").strip())
        except (OSError, ValueError):
            continue
        temperature_c = raw / 1000 if raw > 1000 else raw
        if 0 < temperature_c < 200:
            values.append(temperature_c)
    if not values:
        raise WallClockSoakError("no valid host temperature input")
    return {"maximum_temperature_c": max(values)}


def host_observation() -> dict[str, Any]:
    try:
        storage = shutil.disk_usage("/srv")
        return {
            "ok": True,
            "memory": memory_observation(),
            "thermal": thermal_observation(),
            "storage": {
                "srv_total_bytes": storage.total,
                "srv_used_bytes": storage.used,
                "srv_free_bytes": storage.free,
            },
            "error": None,
        }
    except (OSError, ValueError, KeyError, WallClockSoakError) as error:
        return {
            "ok": False,
            "memory": None,
            "thermal": None,
            "storage": None,
            "error": str(error),
        }


def database_observation(
    path: Path,
    *,
    read_probes: int,
) -> dict[str, Any]:
    started = time.perf_counter()
    connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    latencies: list[float] = []
    try:
        quick_check = connection.execute("PRAGMA quick_check").fetchone()[0]
        mismatch_count = int(
            connection.execute(
                "SELECT COUNT(*) FROM projection p "
                "LEFT JOIN objects o ON o.object_id = p.object_id "
                "WHERE o.object_id IS NULL OR o.state != 'active' "
                "OR o.version != p.source_version "
                "OR o.content_digest != p.content_digest"
            ).fetchone()[0]
        )
        active_ids = [
            row[0]
            for row in connection.execute(
                "SELECT object_id FROM objects WHERE state = 'active' "
                "ORDER BY object_id LIMIT 100"
            )
        ]
        for index in range(read_probes):
            probe_started = time.perf_counter_ns()
            if active_ids:
                connection.execute(
                    "SELECT content_digest FROM objects "
                    "WHERE object_id = ? AND state = 'active'",
                    (active_ids[index % len(active_ids)],),
                ).fetchone()
            latencies.append(
                (time.perf_counter_ns() - probe_started) / 1_000_000
            )
    finally:
        connection.close()
    return {
        "path": str(path),
        "quick_check": quick_check,
        "projection_mismatch_count": mismatch_count,
        "active_probe_population": len(active_ids),
        "read_probe_count": len(latencies),
        "read_latency_ms": {
            "p50": round(percentile(latencies, 0.50), 6),
            "p95": round(percentile(latencies, 0.95), 6),
            "p99": round(percentile(latencies, 0.99), 6),
            "maximum": round(max(latencies, default=0.0), 6),
        },
        "observation_latency_ms": round(
            (time.perf_counter() - started) * 1000, 6
        ),
    }


def campaign_paths(root: Path) -> dict[str, Path]:
    return {
        "state": root / "state.json",
        "receipts": root / "receipts.jsonl",
        "lock": root / "campaign.lock",
        "status": root / "status.json",
    }


def init_campaign(
    campaign_root: Path,
    accelerated_root: Path,
    accelerated_report: Path,
) -> dict[str, Any]:
    paths = campaign_paths(campaign_root)
    if paths["state"].exists():
        raise WallClockSoakError("campaign state already exists")
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    databases = {
        arm_id: accelerated_root / f"arm-{arm_id}.sqlite3"
        for arm_id in ARM_IDS
    }
    missing = [
        str(path)
        for path in [accelerated_report, *databases.values()]
        if not path.is_file()
    ]
    if missing:
        raise WallClockSoakError(
            "campaign inputs are missing: " + ", ".join(missing)
        )
    now = utc_now()
    state = {
        "schema_version": 1,
        "campaign_id": "aoa-memo-phase13-wall-clock-"
        + now.strftime("%Y%m%dT%H%M%SZ"),
        "started_at": render_time(now),
        "last_sample_at": None,
        "sample_count": 0,
        "fixture": {
            "path": str(FIXTURE_PATH),
            "sha256": sha256_file(FIXTURE_PATH),
        },
        "runner": {
            "path": str(RUNNER_PATH),
            "sha256": sha256_file(RUNNER_PATH),
        },
        "accelerated_report": {
            "path": str(accelerated_report),
            "sha256": sha256_file(accelerated_report),
        },
        "databases": {
            arm_id: {
                "path": str(path),
                "sha256": sha256_file(path),
            }
            for arm_id, path in databases.items()
        },
        "authority": fixture["authority"],
    }
    atomic_json(paths["state"], state)
    return state


def sample_campaign(campaign_root: Path) -> dict[str, Any]:
    paths = campaign_paths(campaign_root)
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    paths["lock"].parent.mkdir(parents=True, exist_ok=True)
    with paths["lock"].open("a+", encoding="utf-8") as lock_handle:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
        if not paths["state"].is_file():
            raise WallClockSoakError("campaign state is missing")
        state = json.loads(paths["state"].read_text(encoding="utf-8"))
        now = utc_now()
        if state["last_sample_at"] is not None:
            last = parse_time(state["last_sample_at"])
            elapsed = (now - last).total_seconds()
            if elapsed < fixture["minimum_interval_seconds"]:
                return {
                    "sampled": False,
                    "reason": "minimum_interval_not_elapsed",
                    "remaining_seconds": round(
                        fixture["minimum_interval_seconds"] - elapsed, 3
                    ),
                }
        source_checks = {
            "fixture": sha256_file(FIXTURE_PATH)
            == state["fixture"]["sha256"],
            "runner": sha256_file(RUNNER_PATH)
            == state["runner"]["sha256"],
            "accelerated_report": sha256_file(
                Path(state["accelerated_report"]["path"])
            )
            == state["accelerated_report"]["sha256"],
            "databases": all(
                sha256_file(Path(item["path"])) == item["sha256"]
                for item in state["databases"].values()
            ),
        }
        source_ok = all(source_checks.values())
        database_observations = []
        if source_ok:
            database_observations = [
                {
                    "arm_id": arm_id,
                    **database_observation(
                        Path(state["databases"][arm_id]["path"]),
                        read_probes=fixture["read_probes_per_arm"],
                    ),
                }
                for arm_id in ARM_IDS
            ]
        integrity_ok = bool(database_observations) and all(
            item["quick_check"] == "ok"
            and item["projection_mismatch_count"] == 0
            for item in database_observations
        )
        receipt = {
            "schema_version": 1,
            "campaign_id": state["campaign_id"],
            "sample_index": state["sample_count"],
            "observed_at": render_time(now),
            "source_ok": source_ok,
            "source_checks": source_checks,
            "integrity_ok": integrity_ok,
            "database_observations": database_observations,
            "host": host_observation(),
            "authority": fixture["authority"],
        }
        append_jsonl(paths["receipts"], receipt)
        state["last_sample_at"] = receipt["observed_at"]
        state["sample_count"] += 1
        atomic_json(paths["state"], state)
        return {"sampled": True, "receipt": receipt}


def read_receipts(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def optional_min(values: list[float | int]) -> float | int | None:
    return min(values) if values else None


def optional_max(values: list[float | int]) -> float | int | None:
    return max(values) if values else None


def build_status(campaign_root: Path) -> dict[str, Any]:
    paths = campaign_paths(campaign_root)
    if not paths["state"].is_file():
        raise WallClockSoakError("campaign state is missing")
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    state = json.loads(paths["state"].read_text(encoding="utf-8"))
    receipts = read_receipts(paths["receipts"])
    now = utc_now()
    elapsed_seconds = max(
        0.0, (now - parse_time(state["started_at"])).total_seconds()
    )
    expected_samples = (
        int(elapsed_seconds // fixture["sample_interval_seconds"]) + 1
    )
    sample_coverage = min(len(receipts) / expected_samples, 1.0)
    host_successes = sum(item["host"]["ok"] for item in receipts)
    host_success_ratio = host_successes / max(len(receipts), 1)
    source_failures = sum(not item["source_ok"] for item in receipts)
    integrity_failures = sum(not item["integrity_ok"] for item in receipts)
    dates = {item["observed_at"][:10] for item in receipts}
    read_latencies = [
        observation["read_latency_ms"]["maximum"]
        for receipt in receipts
        for observation in receipt["database_observations"]
    ]
    host_receipts = [item["host"] for item in receipts if item["host"]["ok"]]
    completion = fixture["completion"]

    common_complete = (
        sample_coverage >= completion["minimum_sample_coverage_ratio"]
        and host_success_ratio
        >= completion["minimum_host_probe_success_ratio"]
        and integrity_failures <= completion["maximum_integrity_failures"]
        and source_failures <= completion["maximum_source_drift_failures"]
    )
    report = {
        "schema_version": 1,
        "report_id": "aoa-memo-phase13-wall-clock-soak-status-v1",
        "campaign_id": state["campaign_id"],
        "started_at": state["started_at"],
        "observed_at": render_time(now),
        "elapsed_seconds": round(elapsed_seconds, 3),
        "elapsed_days": round(elapsed_seconds / 86400, 6),
        "sample_count": len(receipts),
        "expected_sample_count": expected_samples,
        "sample_coverage_ratio": round(sample_coverage, 6),
        "host_probe_success_ratio": round(host_success_ratio, 6),
        "unique_sample_dates": len(dates),
        "integrity_failures": integrity_failures,
        "source_drift_failures": source_failures,
        "read_latency_ms": {
            "p50": round(percentile(read_latencies, 0.50), 6),
            "p95": round(percentile(read_latencies, 0.95), 6),
            "p99": round(percentile(read_latencies, 0.99), 6),
            "maximum": round(max(read_latencies, default=0.0), 6),
        },
        "host_extrema": {
            "minimum_mem_available_bytes": optional_min(
                [
                    item["memory"]["mem_available_bytes"]
                    for item in host_receipts
                ]
            ),
            "maximum_memory_psi_some_avg10": optional_max(
                [
                    item["memory"]["psi_some_avg10"]
                    for item in host_receipts
                ]
            ),
            "maximum_memory_psi_full_avg10": optional_max(
                [
                    item["memory"]["psi_full_avg10"]
                    for item in host_receipts
                ]
            ),
            "maximum_temperature_c": optional_max(
                [
                    item["thermal"]["maximum_temperature_c"]
                    for item in host_receipts
                ]
            ),
            "minimum_srv_free_bytes": optional_min(
                [
                    item["storage"]["srv_free_bytes"]
                    for item in host_receipts
                ]
            ),
        },
        "wall_clock_7d_complete": (
            common_complete
            and elapsed_seconds >= completion["seven_day_elapsed_seconds"]
            and len(dates) >= completion["minimum_unique_dates_7d"]
        ),
        "wall_clock_30d_complete": (
            common_complete
            and elapsed_seconds >= completion["thirty_day_elapsed_seconds"]
            and len(dates) >= completion["minimum_unique_dates_30d"]
        ),
        "benefit_established": False,
        "claim_limit": fixture["claim_limit"],
        "authority": fixture["authority"],
    }
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(
            schema, format_checker=FormatChecker()
        ).iter_errors(report),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        detail = "\n".join(
            f"{'/'.join(map(str, error.absolute_path))}: {error.message}"
            for error in errors
        )
        raise WallClockSoakError(
            f"wall-clock status schema validation failed:\n{detail}"
        )
    atomic_json(paths["status"], report)
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("--campaign-root", type=Path, required=True)
    init_parser.add_argument("--accelerated-root", type=Path, required=True)
    init_parser.add_argument("--accelerated-report", type=Path, required=True)
    sample_parser = subparsers.add_parser("sample")
    sample_parser.add_argument("--campaign-root", type=Path, required=True)
    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("--campaign-root", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    campaign_root = args.campaign_root.resolve()
    if campaign_root.is_relative_to(BUNDLE_ROOT):
        print("campaign root must remain outside the source tree", file=sys.stderr)
        return 2
    try:
        if args.command == "init":
            init_campaign(
                campaign_root,
                args.accelerated_root.resolve(),
                args.accelerated_report.resolve(),
            )
            sample_campaign(campaign_root)
        elif args.command == "sample":
            result = sample_campaign(campaign_root)
            if not result["sampled"]:
                print(json.dumps(result, sort_keys=True))
                return 0
        report = build_status(campaign_root)
    except (
        WallClockSoakError,
        OSError,
        sqlite3.Error,
        KeyError,
        TypeError,
        ValueError,
    ) as error:
        print(f"Phase 13 wall-clock soak failed: {error}", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
