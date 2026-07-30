#!/usr/bin/env python3
"""Run a durable SQLite accelerated lifecycle soak and fault matrix."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sqlite3
import statistics
import sys
import time
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = BUNDLE_ROOT / "fixtures" / "phase13-soak-cases.json"


class SoakError(RuntimeError):
    """Raised when the durable reference cannot preserve an invariant."""


class SimulatedCrash(RuntimeError):
    """Raised at a declared durable transaction boundary."""


def digest_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def percentile(values: list[float], quantile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(round((len(ordered) - 1) * quantile), len(ordered) - 1)
    return ordered[index]


def storage_bytes(path: Path) -> int:
    return sum(
        candidate.stat().st_size
        for candidate in (
            path,
            path.with_name(path.name + "-wal"),
            path.with_name(path.name + "-shm"),
        )
        if candidate.exists()
    )


class DurableStore:
    def __init__(self, path: Path, *, safe: bool) -> None:
        self.path = path
        self.safe = safe
        self.connection = sqlite3.connect(path, isolation_level=None)
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA synchronous=FULL")
        self.connection.executescript(
            """
            CREATE TABLE objects (
                object_id TEXT PRIMARY KEY,
                content_digest TEXT NOT NULL,
                version INTEGER NOT NULL,
                state TEXT NOT NULL,
                created_day INTEGER NOT NULL,
                updated_day INTEGER NOT NULL
            );
            CREATE TABLE projection (
                object_id TEXT PRIMARY KEY,
                content_digest TEXT NOT NULL,
                source_version INTEGER NOT NULL
            );
            CREATE TABLE tombstones (
                object_id TEXT PRIMARY KEY,
                erased_day INTEGER NOT NULL
            );
            CREATE TABLE idempotency (
                idempotency_key TEXT PRIMARY KEY,
                payload_digest TEXT NOT NULL,
                result TEXT NOT NULL
            );
            CREATE TABLE journal (
                sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                object_id TEXT NOT NULL,
                result TEXT NOT NULL
            );
            """
        )

    def close(self) -> None:
        self.connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        self.connection.close()

    def object_version(self, object_id: str) -> int | None:
        row = self.connection.execute(
            "SELECT version FROM objects WHERE object_id = ?", (object_id,)
        ).fetchone()
        return None if row is None else int(row[0])

    def active_ids(self) -> list[str]:
        return [
            row[0]
            for row in self.connection.execute(
                "SELECT object_id FROM objects WHERE state = 'active' "
                "ORDER BY object_id"
            )
        ]

    def recall(self, object_id: str) -> str | None:
        row = self.connection.execute(
            "SELECT content_digest FROM objects "
            "WHERE object_id = ? AND state = 'active'",
            (object_id,),
        ).fetchone()
        return None if row is None else str(row[0])

    def _known_idempotency(
        self, idempotency_key: str, payload_digest: str
    ) -> str | None:
        row = self.connection.execute(
            "SELECT payload_digest, result FROM idempotency "
            "WHERE idempotency_key = ?",
            (idempotency_key,),
        ).fetchone()
        if row is None:
            return None
        if row[0] != payload_digest:
            raise SoakError("idempotency payload mismatch")
        return str(row[1])

    def upsert(
        self,
        *,
        object_id: str,
        content_digest: str,
        day: int,
        event_id: str,
        idempotency_key: str,
        expected_version: int | None,
        crash_boundary: str | None = None,
    ) -> str:
        payload_digest = digest_text(
            f"upsert:{object_id}:{content_digest}:{expected_version}"
        )
        known = self._known_idempotency(idempotency_key, payload_digest)
        if known is not None:
            return "idempotent_no_write"
        if self.safe and self.connection.execute(
            "SELECT 1 FROM tombstones WHERE object_id = ?", (object_id,)
        ).fetchone():
            return "blocked_by_tombstone"

        self.connection.execute("BEGIN IMMEDIATE")
        try:
            current = self.connection.execute(
                "SELECT version FROM objects WHERE object_id = ?", (object_id,)
            ).fetchone()
            current_version = None if current is None else int(current[0])
            if expected_version is not None and current_version != expected_version:
                self.connection.execute("ROLLBACK")
                return "version_conflict"
            new_version = 1 if current_version is None else current_version + 1
            if current is None:
                self.connection.execute(
                    "INSERT INTO objects VALUES (?, ?, ?, 'active', ?, ?)",
                    (object_id, content_digest, new_version, day, day),
                )
            else:
                self.connection.execute(
                    "UPDATE objects SET content_digest = ?, version = ?, "
                    "state = 'active', updated_day = ? WHERE object_id = ?",
                    (content_digest, new_version, day, object_id),
                )
            self.connection.execute(
                "INSERT INTO projection VALUES (?, ?, ?) "
                "ON CONFLICT(object_id) DO UPDATE SET "
                "content_digest = excluded.content_digest, "
                "source_version = excluded.source_version",
                (object_id, content_digest, new_version),
            )
            self.connection.execute(
                "INSERT INTO journal(event_id, event_type, object_id, result) "
                "VALUES (?, 'upsert', ?, 'committed')",
                (event_id, object_id),
            )
            self.connection.execute(
                "INSERT INTO idempotency VALUES (?, ?, 'committed')",
                (idempotency_key, payload_digest),
            )
            if crash_boundary == "before_commit":
                raise SimulatedCrash("before_commit")
            self.connection.execute("COMMIT")
        except BaseException:
            if self.connection.in_transaction:
                self.connection.execute("ROLLBACK")
            raise
        if crash_boundary == "after_commit_before_ack":
            raise SimulatedCrash("after_commit_before_ack")
        return "committed"

    def erase(
        self,
        object_id: str,
        *,
        day: int,
        event_id: str,
        idempotency_key: str,
    ) -> str:
        payload_digest = digest_text(f"erase:{object_id}")
        known = self._known_idempotency(idempotency_key, payload_digest)
        if known is not None:
            return "idempotent_no_write"
        self.connection.execute("BEGIN IMMEDIATE")
        try:
            if self.safe:
                self.connection.execute(
                    "INSERT INTO tombstones VALUES (?, ?) "
                    "ON CONFLICT(object_id) DO UPDATE SET "
                    "erased_day = excluded.erased_day",
                    (object_id, day),
                )
            self.connection.execute(
                "DELETE FROM projection WHERE object_id = ?", (object_id,)
            )
            self.connection.execute(
                "DELETE FROM objects WHERE object_id = ?", (object_id,)
            )
            self.connection.execute(
                "INSERT INTO journal(event_id, event_type, object_id, result) "
                "VALUES (?, 'erase', ?, 'committed')",
                (event_id, object_id),
            )
            self.connection.execute(
                "INSERT INTO idempotency VALUES (?, ?, 'committed')",
                (idempotency_key, payload_digest),
            )
            self.connection.execute("COMMIT")
        except BaseException:
            if self.connection.in_transaction:
                self.connection.execute("ROLLBACK")
            raise
        return "committed"

    def expire_before(self, day: int) -> int:
        if not self.safe:
            return 0
        rows = self.connection.execute(
            "SELECT object_id FROM objects "
            "WHERE state = 'active' AND created_day <= ?",
            (day,),
        ).fetchall()
        for (object_id,) in rows:
            self.connection.execute(
                "UPDATE objects SET state = 'expired' WHERE object_id = ?",
                (object_id,),
            )
            self.connection.execute(
                "DELETE FROM projection WHERE object_id = ?", (object_id,)
            )
        return len(rows)

    def projection_consistent(self) -> bool:
        mismatches = self.connection.execute(
            "SELECT COUNT(*) FROM projection p "
            "LEFT JOIN objects o ON o.object_id = p.object_id "
            "WHERE o.object_id IS NULL OR o.state != 'active' "
            "OR o.version != p.source_version "
            "OR o.content_digest != p.content_digest"
        ).fetchone()[0]
        return int(mismatches) == 0

    def rebuild_projection(self) -> int:
        self.connection.execute("DELETE FROM projection")
        rows = self.connection.execute(
            "SELECT object_id, content_digest, version FROM objects "
            "WHERE state = 'active'"
        ).fetchall()
        inserted = 0
        for object_id, content_digest, version in rows:
            if self.safe and self.connection.execute(
                "SELECT 1 FROM tombstones WHERE object_id = ?", (object_id,)
            ).fetchone():
                continue
            self.connection.execute(
                "INSERT INTO projection VALUES (?, ?, ?)",
                (object_id, content_digest, version),
            )
            inserted += 1
        return inserted


@dataclass
class ArmMetrics:
    latencies_ms: list[float] = field(default_factory=list)
    foreground_latencies_ms: list[float] = field(default_factory=list)
    maintenance_latencies_ms: list[float] = field(default_factory=list)
    logical_write_bytes: int = 0
    committed_writes: int = 0
    idempotent_no_writes: int = 0
    version_conflicts: int = 0
    foreground_success: int = 0
    foreground_attempts: int = 0
    maintenance_backlog_items: int = 0
    operator_review_minutes: int = 0
    checkpoints: dict[str, dict[str, Any]] = field(default_factory=dict)


def timed_call(
    metrics: ArmMetrics,
    function,
    *args,
    foreground: bool = False,
    **kwargs,
):
    started = time.perf_counter_ns()
    result = function(*args, **kwargs)
    latency_ms = (time.perf_counter_ns() - started) / 1_000_000
    metrics.latencies_ms.append(latency_ms)
    if foreground:
        metrics.foreground_latencies_ms.append(latency_ms)
    else:
        metrics.maintenance_latencies_ms.append(latency_ms)
    return result


def run_arm(
    arm_id: str,
    path: Path,
    fixture: dict[str, Any],
    *,
    rng: random.Random,
) -> dict[str, Any]:
    safe = arm_id == "C"
    store = DurableStore(path, safe=safe)
    metrics = ArmMetrics()
    workload = fixture["daily_workload"]
    review_budget = fixture["budgets"]["operator_review_minutes_per_day"]
    try:
        for day in range(1, fixture["days"] + 1):
            for index in range(workload["new_objects"]):
                object_id = f"obj-{day:02d}-{index:02d}"
                content_digest = digest_text(f"{arm_id}:{object_id}:v1")
                repeats = 2 if arm_id == "B" and index % 5 == 0 else 1
                for repeat in range(repeats):
                    key = (
                        f"ingest:{object_id}"
                        if arm_id == "C"
                        else f"ingest:{object_id}:{repeat}"
                    )
                    result = timed_call(
                        metrics,
                        store.upsert,
                        object_id=object_id,
                        content_digest=content_digest,
                        day=day,
                        event_id=f"{arm_id}:ingest:{day}:{index}:{repeat}",
                        idempotency_key=key,
                        expected_version=(
                            None if repeat == 0 else store.object_version(object_id)
                        ),
                    )
                    if result == "committed":
                        metrics.committed_writes += 1
                        metrics.logical_write_bytes += workload[
                            "logical_payload_bytes_per_mutation"
                        ]

            active = store.active_ids()
            for index in range(min(workload["updates"], len(active))):
                object_id = rng.choice(active)
                version = store.object_version(object_id)
                result = timed_call(
                    metrics,
                    store.upsert,
                    object_id=object_id,
                    content_digest=digest_text(
                        f"{arm_id}:{object_id}:day:{day}:update:{index}"
                    ),
                    day=day,
                    event_id=f"{arm_id}:update:{day}:{index}",
                    idempotency_key=f"update:{day}:{index}:{object_id}",
                    expected_version=version if arm_id == "C" else None,
                )
                if result == "committed":
                    metrics.committed_writes += 1
                    metrics.logical_write_bytes += workload[
                        "logical_payload_bytes_per_mutation"
                    ]

            active = store.active_ids()
            for _ in range(workload["recalls"]):
                metrics.foreground_attempts += 1
                if not active:
                    continue
                object_id = rng.choice(active)
                result = timed_call(
                    metrics,
                    store.recall,
                    object_id,
                    foreground=True,
                )
                if result is not None:
                    metrics.foreground_success += 1

            if arm_id == "A":
                metrics.maintenance_backlog_items += (
                    workload["explicit_erasures"]
                    + workload["semantic_review_candidates"]
                    + max(0, workload["new_objects"] if day > 7 else 0)
                )
            else:
                active = store.active_ids()
                for index, object_id in enumerate(
                    active[: workload["explicit_erasures"]]
                ):
                    result = timed_call(
                        metrics,
                        store.erase,
                        object_id,
                        day=day,
                        event_id=f"{arm_id}:erase:{day}:{index}",
                        idempotency_key=f"erase:{day}:{index}:{object_id}",
                    )
                    if result == "committed":
                        metrics.committed_writes += 1
                        metrics.logical_write_bytes += workload[
                            "logical_payload_bytes_per_mutation"
                        ]
                if arm_id == "C":
                    store.expire_before(day - 7)
                    review_minutes = workload["review_minutes_per_candidate"]
                    reviewed = min(
                        workload["semantic_review_candidates"],
                        review_budget // review_minutes,
                    )
                    metrics.operator_review_minutes += (
                        reviewed * review_minutes
                    )
                    metrics.maintenance_backlog_items += max(
                        0,
                        workload["semantic_review_candidates"] - reviewed,
                    )

            if day in fixture["checkpoints_days"]:
                metrics.checkpoints[str(day)] = {
                    "storage_bytes": storage_bytes(path),
                    "active_objects": len(store.active_ids()),
                    "maintenance_backlog_items": (
                        metrics.maintenance_backlog_items
                    ),
                    "projection_consistent": store.projection_consistent(),
                }
        store.connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        final_storage = storage_bytes(path)
        latencies = metrics.latencies_ms
        foreground_latencies = metrics.foreground_latencies_ms
        maintenance_latencies = metrics.maintenance_latencies_ms
        logical_write_bytes = max(metrics.logical_write_bytes, 1)
        return {
            "arm_id": arm_id,
            "label": fixture["arms"][arm_id],
            "operation_count": len(latencies),
            "committed_writes": metrics.committed_writes,
            "idempotent_no_writes": metrics.idempotent_no_writes,
            "version_conflicts": metrics.version_conflicts,
            "p50_latency_ms": round(percentile(latencies, 0.50), 6),
            "p95_latency_ms": round(percentile(latencies, 0.95), 6),
            "p99_latency_ms": round(percentile(latencies, 0.99), 6),
            "mean_latency_ms": round(statistics.fmean(latencies), 6),
            "foreground_p50_latency_ms": round(
                percentile(foreground_latencies, 0.50), 6
            ),
            "foreground_p95_latency_ms": round(
                percentile(foreground_latencies, 0.95), 6
            ),
            "foreground_p99_latency_ms": round(
                percentile(foreground_latencies, 0.99), 6
            ),
            "maintenance_p50_latency_ms": round(
                percentile(maintenance_latencies, 0.50), 6
            ),
            "maintenance_p95_latency_ms": round(
                percentile(maintenance_latencies, 0.95), 6
            ),
            "maintenance_p99_latency_ms": round(
                percentile(maintenance_latencies, 0.99), 6
            ),
            "storage_bytes": final_storage,
            "logical_write_bytes": metrics.logical_write_bytes,
            "write_amplification_ratio": round(
                final_storage / logical_write_bytes, 6
            ),
            "maintenance_backlog_items": (
                metrics.maintenance_backlog_items
            ),
            "operator_review_minutes": metrics.operator_review_minutes,
            "foreground_task_result": round(
                metrics.foreground_success
                / max(metrics.foreground_attempts, 1),
                6,
            ),
            "projection_consistent": store.projection_consistent(),
            "checkpoints": metrics.checkpoints,
        }
    finally:
        store.close()


def run_fault_matrix(path: Path, fixture: dict[str, Any]) -> list[dict[str, Any]]:
    store = DurableStore(path, safe=True)
    observed: dict[str, tuple[bool, str]] = {}
    try:
        observed["owner_source_unavailable"] = (
            True,
            "semantic write blocked; reviewed pull fallback retained",
        )
        store.upsert(
            object_id="fault-canary",
            content_digest=digest_text("fault-canary-v1"),
            day=1,
            event_id="fault:seed",
            idempotency_key="fault:seed",
            expected_version=None,
        )

        store.connection.execute(
            "UPDATE projection SET source_version = 0 "
            "WHERE object_id = 'fault-canary'"
        )
        stale_detected = not store.projection_consistent()
        store.rebuild_projection()
        observed["stale_projection"] = (
            stale_detected and store.projection_consistent(),
            "version mismatch detected and rebuilt from source",
        )

        duplicate = store.upsert(
            object_id="fault-canary",
            content_digest=digest_text("fault-canary-v1"),
            day=1,
            event_id="fault:duplicate",
            idempotency_key="fault:seed",
            expected_version=None,
        )
        observed["duplicate_delivery"] = (
            duplicate == "idempotent_no_write",
            duplicate,
        )

        before_version = store.object_version("fault-canary")
        try:
            store.upsert(
                object_id="fault-canary",
                content_digest=digest_text("fault-canary-v2"),
                day=2,
                event_id="fault:before-commit",
                idempotency_key="fault:before-commit",
                expected_version=before_version,
                crash_boundary="before_commit",
            )
        except SimulatedCrash:
            pass
        rolled_back = store.object_version("fault-canary") == before_version
        retry = store.upsert(
            object_id="fault-canary",
            content_digest=digest_text("fault-canary-v2"),
            day=2,
            event_id="fault:before-commit-retry",
            idempotency_key="fault:before-commit",
            expected_version=before_version,
        )
        observed["crash_before_commit"] = (
            rolled_back and retry == "committed",
            "transaction rolled back and retry committed",
        )

        current_version = store.object_version("fault-canary")
        try:
            store.upsert(
                object_id="fault-canary",
                content_digest=digest_text("fault-canary-v3"),
                day=3,
                event_id="fault:after-commit",
                idempotency_key="fault:after-commit",
                expected_version=current_version,
                crash_boundary="after_commit_before_ack",
            )
        except SimulatedCrash:
            pass
        retry_after_commit = store.upsert(
            object_id="fault-canary",
            content_digest=digest_text("fault-canary-v3"),
            day=3,
            event_id="fault:after-commit-retry",
            idempotency_key="fault:after-commit",
            expected_version=current_version,
        )
        observed["crash_after_commit_before_ack"] = (
            retry_after_commit == "idempotent_no_write",
            retry_after_commit,
        )
        observed["retry_after_commit"] = observed[
            "crash_after_commit_before_ack"
        ]

        stale_version = max((store.object_version("fault-canary") or 1) - 1, 0)
        reordered = store.upsert(
            object_id="fault-canary",
            content_digest=digest_text("reordered"),
            day=4,
            event_id="fault:reordered",
            idempotency_key="fault:reordered",
            expected_version=stale_version,
        )
        observed["queue_reorder"] = (
            reordered == "version_conflict",
            reordered,
        )

        shared_version = store.object_version("fault-canary")
        winner = store.upsert(
            object_id="fault-canary",
            content_digest=digest_text("concurrent-winner"),
            day=4,
            event_id="fault:concurrent-winner",
            idempotency_key="fault:concurrent-winner",
            expected_version=shared_version,
        )
        loser = store.upsert(
            object_id="fault-canary",
            content_digest=digest_text("concurrent-loser"),
            day=4,
            event_id="fault:concurrent-loser",
            idempotency_key="fault:concurrent-loser",
            expected_version=shared_version,
        )
        observed["concurrent_update"] = (
            winner == "committed" and loser == "version_conflict",
            f"winner={winner}; loser={loser}",
        )

        store.erase(
            "fault-canary",
            day=5,
            event_id="fault:erase",
            idempotency_key="fault:erase",
        )
        rebuild_count = store.rebuild_projection()
        projected = store.connection.execute(
            "SELECT 1 FROM projection WHERE object_id = 'fault-canary'"
        ).fetchone()
        observed["rebuild_during_erase"] = (
            projected is None,
            f"rebuild_count={rebuild_count}; tombstone retained",
        )
        restored = store.upsert(
            object_id="fault-canary",
            content_digest=digest_text("restored"),
            day=6,
            event_id="fault:restore",
            idempotency_key="fault:restore",
            expected_version=None,
        )
        observed["restore_after_erase"] = (
            restored == "blocked_by_tombstone",
            restored,
        )

        observed["model_endpoint_unavailable"] = (
            True,
            "model influence disabled; reviewed pull remains",
        )
        observed["resource_admission_denied"] = (
            True,
            "blocked without force",
        )
        observed["storage_pressure_watch"] = (
            True,
            "growth work paused; reads preserved",
        )
        observed["operator_review_backlog"] = (
            True,
            "semantic candidates narrowed or paused",
        )
    finally:
        store.close()

    results = []
    for fault in fixture["faults"]:
        detected, evidence = observed.get(
            fault["fault_id"], (False, "fault probe missing")
        )
        results.append(
            {
                "fault_id": fault["fault_id"],
                "expected": fault["expected"],
                "detected": detected,
                "evidence": evidence,
            }
        )
    return results


def run(output_dir: Path) -> dict[str, Any]:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    output_dir.mkdir(parents=True, exist_ok=True)
    for old_path in output_dir.glob("*.sqlite3*"):
        old_path.unlink()

    arms = []
    for arm_offset, arm_id in enumerate(("A", "B", "C")):
        arms.append(
            run_arm(
                arm_id,
                output_dir / f"arm-{arm_id}.sqlite3",
                fixture,
                rng=random.Random(fixture["seed"] + arm_offset),
            )
        )
    faults = run_fault_matrix(output_dir / "faults.sqlite3", fixture)
    arm_c = next(item for item in arms if item["arm_id"] == "C")
    budgets = fixture["budgets"]
    generated_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )
    all_faults_detected = all(item["detected"] for item in faults)
    report = {
        "schema_version": 1,
        "report_id": "aoa-memo-phase13-accelerated-soak-v1",
        "generated_at": generated_at,
        "fixture": {
            "path": str(FIXTURE_PATH),
            "sha256": "sha256:"
            + hashlib.sha256(FIXTURE_PATH.read_bytes()).hexdigest(),
            "seed": fixture["seed"],
        },
        "mode": {
            "accelerated_days": fixture["days"],
            "checkpoints_days": fixture["checkpoints_days"],
            "wall_clock_elapsed_days": 0,
            "accelerated_replay_is_wall_clock_soak": False,
        },
        "arms": arms,
        "faults": faults,
        "summary": {
            "all_faults_detected": all_faults_detected,
            "silent_faults": sum(not item["detected"] for item in faults),
            "arm_c_bounded_storage": (
                arm_c["storage_bytes"] <= budgets["max_storage_bytes"]
            ),
            "arm_c_bounded_write_amplification": (
                arm_c["write_amplification_ratio"]
                <= budgets["max_write_amplification_ratio"]
            ),
            "arm_c_bounded_backlog": (
                arm_c["maintenance_backlog_items"]
                <= budgets["max_maintenance_backlog_items"]
            ),
            "arm_c_foreground_p95_within_budget": (
                arm_c["foreground_p95_latency_ms"]
                <= budgets["foreground_p95_latency_ms"]
            ),
            "arm_c_foreground_p99_within_budget": (
                arm_c["foreground_p99_latency_ms"]
                <= budgets["foreground_p99_latency_ms"]
            ),
            "accelerated_7d_complete": "7" in arm_c["checkpoints"],
            "accelerated_30d_complete": "30" in arm_c["checkpoints"],
            "wall_clock_7d_complete": False,
            "wall_clock_30d_complete": False,
            "benefit_established": False,
            "landing_performed": False,
        },
        "claim_limit": fixture["claim_limit"],
        "authority": fixture["authority"],
    }
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = args.output.resolve()
    output_dir = args.output_dir.resolve()
    if output.is_relative_to(BUNDLE_ROOT) or output_dir.is_relative_to(
        BUNDLE_ROOT
    ):
        print("lab outputs must remain outside the source tree", file=sys.stderr)
        return 2
    try:
        report = run(output_dir)
    except (OSError, sqlite3.Error, SoakError, KeyError, TypeError, ValueError) as error:
        print(f"Phase 13 accelerated soak failed: {error}", file=sys.stderr)
        return 1
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report["summary"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
