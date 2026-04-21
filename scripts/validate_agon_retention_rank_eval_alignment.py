#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "generated/agon_retention_rank_eval_alignment_registry.min.json"
SCHEMA = ROOT / "schemas/agon-retention-rank-eval-alignment-registry.schema.json"
BUILDER = ROOT / "scripts/build_agon_retention_rank_eval_alignment_registry.py"
REQUIRED_ENTRY_FIELDS = ['id', 'kind', 'owner', 'status', 'description', 'candidate_only', 'live_authority']
EXPECTED_LIVE_PROTOCOL = False
REQUIRED_STOP_LINES = {
    "no_live_verdict_authority",
    "no_durable_scar_write",
    "no_retention_execution_without_owner_review",
    "no_rank_or_trust_mutation",
    "no_closure_grant",
    "no_live_summon",
    "no_tree_of_sophia_promotion",
    "no_kag_promotion",
    "no_hidden_scheduler_action",
    "no_assistant_contestant_drift",
    "no_center_takeover_of_agent_eval_memo_stats_truth",
}


def expected_registry() -> dict:
    spec = importlib.util.spec_from_file_location("agon_retention_rank_eval_builder", BUILDER)
    if spec is None or spec.loader is None:
        raise SystemExit(f"unable to load builder: {BUILDER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_registry()


def validate_schema(data: dict) -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda err: list(err.path))
    if errors:
        first = errors[0]
        path = ".".join(str(part) for part in first.path) or "<root>"
        raise SystemExit(f"schema violation at {path}: {first.message}")


def main() -> int:
    if not REGISTRY.exists():
        raise SystemExit(f"missing registry: {REGISTRY}")
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    validate_schema(data)
    if data != expected_registry():
        raise SystemExit("generated registry drift: rebuild from config before validating")
    if data.get("live_protocol") is not EXPECTED_LIVE_PROTOCOL:
        raise SystemExit("Wave XIV registries must remain non-live protocol surfaces")
    if data.get("runtime_effect") not in ['candidate_only', 'none', 'review_surface_only', 'local_dry_run_candidate_only']:
        raise SystemExit(f"unexpected runtime_effect: {data.get('runtime_effect')}")
    entries = data.get("entries", [])
    if not entries:
        raise SystemExit("registry has no entries")
    if data.get("entry_count") != len(entries):
        raise SystemExit("entry_count does not match entries length")
    seen = set()
    for item in entries:
        missing = [field for field in REQUIRED_ENTRY_FIELDS if field not in item]
        if missing:
            raise SystemExit(f"entry {item.get('id', '<unknown>')} missing fields: {missing}")
        if item["id"] in seen:
            raise SystemExit(f"duplicate entry id: {item['id']}")
        seen.add(item["id"])
        if item.get("candidate_only") is not True:
            raise SystemExit(f"entry {item['id']} must remain candidate_only=true")
        if item.get("live_authority") is not False:
            raise SystemExit(f"entry {item['id']} must remain live_authority=false")
    stop_lines = set(data.get("stop_lines", []))
    for required_stop in sorted(REQUIRED_STOP_LINES):
        if required_stop not in stop_lines:
            raise SystemExit(f"missing stop-line: {required_stop}")
    print(f"ok: {REGISTRY.relative_to(ROOT)} entries={len(entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
