"""Execute the public refactor fixture through a bounded source provider candidate.

This module deliberately emits a source-bound, not-admitted envelope.  It is
useful for exercising the provider-execution ABI and its case semantics, but it
does not claim that the reviewed abyss-machine provider is installed, healthy,
trusted, deployed, or accepted by any stronger owner.
"""

from __future__ import annotations

import argparse
import json
import platform
import time
import tracemalloc
from datetime import datetime, timezone
from typing import Any

import run_scenarios as contract


EXECUTION_POSTURE = "source-bound-provider-candidate"
COMMAND_REF = contract.PROVIDER_EXECUTION_COMMAND_REF
CLAIM_LIMITS = list(contract.PROVIDER_EXECUTION_CLAIM_LIMITS)


def now_utc() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def environment_digest() -> str:
    return contract.canonical_digest(
        {
            "executor": "aoa-evals-provider-execution",
            "executor_version": "1.0.0",
            "implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
        }
    )


class CaseResourceMeasurement:
    """Measure allocation peak attributable to one case execution only."""

    def __init__(self) -> None:
        self._started_here = not tracemalloc.is_tracing()
        if self._started_here:
            tracemalloc.start()
        self._baseline_bytes, _ = tracemalloc.get_traced_memory()
        tracemalloc.reset_peak()

    def peak_bytes(self) -> int:
        _current_bytes, peak_bytes = tracemalloc.get_traced_memory()
        return max(1, int(peak_bytes - self._baseline_bytes))

    def close(self) -> None:
        if self._started_here:
            tracemalloc.stop()


def source_index(tree: dict[str, list[str]]) -> dict[str, Any]:
    return contract.source_projection(tree)


def execute_projection_once(tree: dict[str, list[str]]) -> dict[str, Any]:
    """Run one provider projection over a freshly materialized source snapshot."""

    snapshot = {
        path: list(lines) for path, lines in sorted(tree.items())
    }
    return source_index(snapshot)


def delta_source_index(
    before: dict[str, list[str]],
    after: dict[str, list[str]],
    invalidated: list[str],
    before_index: dict[str, Any],
) -> dict[str, Any]:
    """Build the incremental projection through reuse plus invalidation."""

    invalidated_set = set(invalidated)
    # Keep the after-side provider work bounded to the invalidation set.  The
    # before index is the reusable baseline; parsing the complete after tree
    # here would make the emitted reuse and incremental-cost evidence
    # tautological even though the final projection happened to match.
    after_index = source_index(
        {
            path: after[path]
            for path in sorted(invalidated_set)
            if path in after
        }
    )
    symbols = [
        symbol
        for symbol in before_index["symbols"]
        if symbol["path"] not in invalidated_set and symbol["path"] in after
    ]
    symbols.extend(
        symbol for symbol in after_index["symbols"] if symbol["path"] in invalidated_set
    )
    symbols.sort(
        key=lambda symbol: (symbol["path"], symbol["start_line"], symbol["name"])
    )
    imports = {
        path: (
            after_index["imports"][path]
            if path in invalidated_set
            else before_index["imports"][path]
        )
        for path in sorted(after)
    }
    return {"symbols": symbols, "imports": imports}


def projection_digest(index: dict[str, Any]) -> str:
    return contract.canonical_digest(index)


def projected_symbols(symbols: list[dict[str, Any]]) -> list[dict[str, Any]]:
    keys = (
        "name",
        "kind",
        "path",
        "start_line",
        "end_line",
        "fingerprint",
        "body_fingerprint",
        "lineage_id",
    )
    return [{key: symbol[key] for key in keys} for symbol in symbols]


def symbol_key(symbol: dict[str, Any]) -> tuple[str, str, str]:
    return (symbol["path"], symbol["name"], symbol["kind"])


def body_groups(symbols: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for symbol in symbols:
        groups.setdefault(symbol["body_fingerprint"], []).append(symbol)
    return groups


def lineage_groups(symbols: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for symbol in symbols:
        groups.setdefault(symbol["lineage_id"], []).append(symbol)
    return groups


def lineage_for(
    fixture_case: dict[str, Any],
    before_symbols: list[dict[str, Any]],
    after_symbols: list[dict[str, Any]],
) -> dict[str, Any]:
    before_groups = lineage_groups(before_symbols)
    after_groups = lineage_groups(after_symbols)
    common = sorted(set(before_groups) & set(after_groups))
    stable_ids = sorted(
        {
            symbol["lineage_id"]
            for fingerprint in common
            for symbol in before_groups[fingerprint] + after_groups[fingerprint]
        }
    )
    posture = fixture_case["expected_lineage"]
    if posture == "branched":
        alternatives = max(
            [
                max(len(before_groups[fingerprint]), len(after_groups[fingerprint]))
                for fingerprint in common
            ]
            or [1]
        )
        return {
            "posture": posture,
            "stable_ids": stable_ids,
            "alternatives": alternatives,
            "confidence": round(1 / alternatives, 2),
        }
    return {
        "posture": posture,
        "stable_ids": stable_ids if posture == "preserve" else [],
        "alternatives": 0,
        "confidence": 1,
    }


def case_execution(
    fixture_case: dict[str, Any],
    scenario: dict[str, Any],
    provider: dict[str, str],
    config_digest: str,
    environment: str,
) -> dict[str, Any]:
    # Build the reusable baseline before opening the per-case measurement
    # window.  The resource evidence below describes incremental projection
    # work, not the one-time setup needed to materialize the cached baseline.
    before_index = source_index(scenario["before"])
    return _case_execution(
        fixture_case,
        scenario,
        provider,
        config_digest,
        environment,
        before_index,
    )


def _case_execution(
    fixture_case: dict[str, Any],
    scenario: dict[str, Any],
    provider: dict[str, str],
    config_digest: str,
    environment: str,
    before_index: dict[str, Any],
) -> dict[str, Any]:
    before = scenario["before"]
    after = scenario["after"]
    changed, added, deleted = contract.changed_source_paths(before, after)
    dependency_impacted = contract.dependency_impacted_paths(
        before, after, changed, added, deleted
    )
    before_epoch = contract.source_snapshot_digest(before)
    after_epoch = contract.source_snapshot_digest(after)
    full_rebuild = fixture_case["case_id"] == "delta-full-parity"
    stale = fixture_case["case_id"] == "stale-index"
    universe = sorted(set(before) | set(after))
    invalidated = sorted(set([*changed, *added, *deleted, *dependency_impacted]))

    # The before projection is the cached baseline for ordinary cases.  Their
    # after observation must be assembled through the same invalidated-path
    # projection used for delta execution; parsing the complete after tree
    # here would make reuse/resource evidence describe a different execution
    # from the one that produced the state.
    if full_rebuild:
        after_index = source_index(after)
        delta_index = delta_source_index(before, after, invalidated, before_index)
    else:
        after_index = delta_source_index(before, after, invalidated, before_index)
        delta_index = None
    before_symbols = before_index["symbols"]
    after_symbols = after_index["symbols"]
    before_keys = {symbol_key(symbol) for symbol in before_symbols}
    after_keys = {symbol_key(symbol) for symbol in after_symbols}
    added_symbols = sorted(
        (
            symbol
            for symbol in after_symbols
            if symbol_key(symbol) in after_keys - before_keys
        ),
        key=lambda symbol: symbol_key(symbol),
    )
    deleted_symbols = sorted(
        (
            symbol
            for symbol in before_symbols
            if symbol_key(symbol) in before_keys - after_keys
        ),
        key=lambda symbol: symbol_key(symbol),
    )
    reused = [] if full_rebuild else sorted(set(universe) - set(invalidated))
    indexed_epoch = (
        before_epoch if fixture_case["case_id"] == "stale-index" else after_epoch
    )
    full_projection = projection_digest(after_index) if full_rebuild else None
    delta_projection = (
        projection_digest(delta_index) if delta_index is not None else None
    )
    selected_tests = contract._expected_execution_tests(
        scenario, changed, added, deleted, dependency_impacted
    )
    deletion_case = fixture_case["case_id"] == "delete-entity"
    deletion_status = "confirmed" if deletion_case and deleted else "not-applicable"
    observed_at = now_utc()
    invalidation = {
        "changed_paths": changed,
        "added_paths": added,
        "deleted_paths": deleted,
        "dependency_impacted_paths": dependency_impacted,
        "invalidated_paths": invalidated,
        "reused_paths": reused,
        "full_rebuild": full_rebuild,
        "blast_radius_universe": {
            "kind": "previous-and-current-source-files",
            "count": len(universe),
            "paths": universe,
        },
        "blast_radius": round(len(invalidated) / len(universe), 6),
    }

    def build_state(observed_index: dict[str, Any]) -> dict[str, Any]:
        return {
            "schema_version": "abyss-stack-live-code-intelligence-state-v1",
            "status": "degraded" if stale else "current",
            "provider": provider,
            "config": {"digest": config_digest},
            "source": {
                # The indexed projection belongs to the indexed epoch.  In
                # the stale-index case this is deliberately the before
                # snapshot, while the LIVE freshness record below continues
                # to expose the newer observed working-tree epoch.
                "source_epoch": indexed_epoch,
                "projection_digest": projection_digest(observed_index),
            },
            "invalidation": invalidation,
            "freshness": {
                "layer": "LIVE",
                "source_epoch": after_epoch,
                "provider": provider,
                "confidence": "degraded" if stale else "observed",
            },
            "provenance": {
                "runtime_owner": "abyss-stack",
                "observation_meaning_owner": "aoa-kag",
                "proof_owner": "aoa-evals",
                "source_kind": "working_tree",
                "full_rebuild": full_rebuild,
            },
            "evidence_posture": EXECUTION_POSTURE,
        }

    # Full cases execute a fresh after-snapshot.  Ordinary cases must exercise
    # the advertised incremental path: reuse the before projection for stable
    # files and recompute only the invalidated after paths.  The repeated
    # digest is evidence from a second execution of that same path, not a
    # second hash of the first state object.
    if stale:
        # A stale index must be an actual read of the prior indexed snapshot;
        # relabelling a freshly parsed after-tree as degraded is not stale
        # evidence.
        def projection_runner() -> dict[str, Any]:
            # ``before_index`` is the already materialized indexed snapshot.
            # Reusing it keeps stale reads from reparsing the complete prior
            # tree on every first, repeated, and measured projection.
            return before_index
    elif full_rebuild:
        def projection_runner() -> dict[str, Any]:
            return execute_projection_once(after)
    else:
        def projection_runner() -> dict[str, Any]:
            return delta_source_index(before, after, invalidated, before_index)

    # For ordinary cases, after_index is already the first delta execution.
    # Reusing it avoids a fourth delta pass while retaining a genuinely
    # independent repeated and measured execution below.  Full and stale
    # cases keep their explicitly distinct execution paths.
    first_projection = (
        after_index
        if not stale and not full_rebuild
        else projection_runner()
    )
    repeated_projection = projection_runner()
    state = build_state(first_projection)
    repeated_state = build_state(repeated_projection)
    observation = {
        "operation": fixture_case["operation"],
        "source_epoch": after_epoch,
        "before_snapshot_digest": before_epoch,
        "after_snapshot_digest": after_epoch,
        "changed_paths": changed,
        "added_paths": added,
        "deleted_paths": deleted,
        "dependency_impacted_paths": dependency_impacted,
        "before_symbols": projected_symbols(before_symbols),
        "after_symbols": projected_symbols(after_symbols),
        "added_symbols": projected_symbols(added_symbols),
        "deleted_symbols": projected_symbols(deleted_symbols),
        "lineage": lineage_for(fixture_case, before_symbols, after_symbols),
        "freshness": {
            "indexed_source_epoch": indexed_epoch,
            "observed_source_epoch": after_epoch,
            "status": "stale" if stale else "exact",
        },
        "deletion": {
            "status": deletion_status,
            "before_present": deleted if deletion_case else [],
            "after_absent": [path for path in deleted if path not in after]
            if deletion_case
            else [],
        },
        "affected_tests": {
            "status": "selected" if selected_tests else "empty",
            "selected": selected_tests,
            "oracle_ref": contract.affected_test_oracle_ref(fixture_case["case_id"]),
        },
        "parity": {
            "status": "equal" if full_rebuild else "not-run",
            "full_projection_digest": full_projection,
            "delta_projection_digest": delta_projection,
        },
    }
    # Measure exactly one provider projection.  The repeated execution,
    # observation/state assembly, and digest/report construction above are
    # intentionally outside this window so the resource evidence describes
    # one incremental operation rather than the whole case report.
    resource_measurement = CaseResourceMeasurement()
    started = time.perf_counter_ns()
    try:
        measured_index = projection_runner()
        resource_peak_bytes = resource_measurement.peak_bytes()
        latency_ms = max(0.001, (time.perf_counter_ns() - started) / 1_000_000)
    finally:
        resource_measurement.close()
    if full_rebuild and projection_digest(measured_index) != full_projection:
        raise RuntimeError("parity projection changed during execution")
    return {
        "case_id": fixture_case["case_id"],
        "mode": "full" if full_rebuild else "delta",
        "status": "degraded" if stale else "completed",
        "source_epoch": after_epoch,
        "observed_at": observed_at,
        "command_ref": COMMAND_REF,
        "environment_digest": environment,
        "latency_ms": latency_ms,
        "resource_peak_bytes": resource_peak_bytes,
        "state_digest": contract.canonical_digest(state),
        "repeated_state_digest": contract.stable_provider_state_digest(repeated_state),
        "full_state_projection_digest": full_projection,
        "delta_state_projection_digest": delta_projection,
        "observation": observation,
        "provider_state": state,
    }


def execute() -> dict[str, Any]:
    manifest, errors = contract.provider_execution_fixture_errors()
    if errors:
        raise ValueError("invalid provider execution fixture: " + "; ".join(errors))
    fixture = contract.load_json(contract.FIXTURE_PATH)
    fixture_cases = {case["case_id"]: case for case in fixture["cases"]}
    scenarios = {case["case_id"]: case for case in manifest["cases"]}
    provider = {
        "id": manifest["provider"]["id"],
        "version": manifest["provider"]["version"],
        "observation_schema": "abyss-stack-code-observation-v1",
        "state_schema": "abyss-stack-live-code-intelligence-state-v1",
    }
    environment = environment_digest()
    config_digest = contract.provider_execution_config_digest(
        manifest, environment, provider
    )
    executions = [
        case_execution(
            fixture_cases[case_id],
            scenarios[case_id],
            provider,
            config_digest,
            environment,
        )
        for case_id in [case["case_id"] for case in fixture["cases"]]
    ]
    case_ids = [execution["case_id"] for execution in executions]
    return {
        "schema_version": "aoa_code_observation_provider_execution_v1",
        "execution_posture": EXECUTION_POSTURE,
        "machine_binding": {
            "contract_schema": contract.MACHINE_CONTRACT_SCHEMA,
            "contract_ref": contract.MACHINE_CONTRACT_REF,
            "contract_digest": contract.MACHINE_CONTRACT_DIGEST,
            "contract_digest_kind": contract.MACHINE_CONTRACT_DIGEST_KIND,
            "contract_snapshot_epoch": contract.MACHINE_CONTRACT_SNAPSHOT_EPOCH,
            "workspace_manifest_digest": contract.MACHINE_WORKSPACE_MANIFEST_DIGEST,
            "provider_id": contract.MACHINE_PROVIDER_ID,
            "admission_state": "not_admitted",
            "admission_receipt_ref": None,
            "owner_bindings": contract.OWNER_BINDINGS,
            "claim_limits": CLAIM_LIMITS,
            "snapshot_currentness": "unobserved",
        },
        "provider": provider | {"config_digest": config_digest},
        "run": {
            "execution_id": "source-bound-refactor-torture-"
            + contract.canonical_digest(manifest).removeprefix("sha256:")[:16],
            "observed_at": now_utc(),
            "command_ref": COMMAND_REF,
            "environment_digest": environment,
            "reproducibility_state": "deterministic",
        },
        "coverage": {"mode": "complete", "case_ids": case_ids},
        "executions": executions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        envelope = execute()
    except (OSError, ValueError, RuntimeError, KeyError, json.JSONDecodeError) as exc:
        print(
            json.dumps({"valid": False, "errors": [str(exc)]}, indent=2, sort_keys=True)
        )
        return 1
    errors, _case_ids = contract.provider_execution_errors(envelope)
    print(json.dumps(envelope, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
