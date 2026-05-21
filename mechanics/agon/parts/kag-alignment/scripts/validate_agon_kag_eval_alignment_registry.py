#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import pathlib
import sys
from typing import Any

from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / 'config/agon_kag_eval_alignment.seed.json'
OUT = ROOT / 'generated/agon_kag_eval_alignment_registry.min.json'
ENTRY_SCHEMA = ROOT / 'schemas/agon-kag-eval-alignment.schema.json'
REGISTRY_SCHEMA = ROOT / 'schemas/agon-kag-eval-alignment-registry.schema.json'
BUILDER = ROOT / 'scripts/build_agon_kag_eval_alignment_registry.py'
ITEM_KEY = 'eval_alignments'
REGISTRY_ID = 'agon.kag_eval_alignment.registry.v1'
WAVE = 'XVII'
WAVE_NAME = 'KAG Promotion Path'
RUNTIME_POSTURE = 'candidate_only'
EXPECTED_COUNT = 7
UNIQUE_KEY_FIELD = 'alignment_id'
REQUIRED_FORBIDDEN = ['live_verdict_authority', 'durable_scar_write', 'retention_execution', 'rank_mutation', 'trust_mutation', 'tree_of_sophia_promotion', 'direct_tos_promotion', 'kag_canonization', 'kag_source_truth_claim', 'hidden_scheduler_action', 'assistant_contestant_drift', 'auto_doctrine_rewrite', 'center_takeover_of_owner_truth', 'unreviewed_kag_promotion', 'single_event_promotion', 'stats_promotion_authority', 'eval_promotion_authority']
REQUIRED_STOP_LINES = ['no_live_verdict_authority', 'no_durable_scar_write', 'no_retention_execution', 'no_rank_or_trust_mutation', 'no_tree_of_sophia_promotion', 'no_direct_tos_promotion', 'no_kag_as_canon', 'no_kag_as_source_truth', 'no_hidden_scheduler_action', 'no_assistant_contestant_drift', 'no_auto_doctrine_rewrite', 'no_center_takeover_of_owner_truth', 'no_kag_promotion_without_owner_review', 'no_promotion_from_single_event', 'no_stats_as_promotion_authority', 'no_eval_as_promotion_authority']
ALLOWED_RUNTIME = ['none', 'candidate_only', 'local_dry_run_candidate_only', 'local_rehearsal_candidate_only']


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def load_builder():
    spec = importlib.util.spec_from_file_location('_agon_seed_builder', BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f'cannot load builder {BUILDER}')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def schema_error(schema_path: pathlib.Path, payload: Any, label: str) -> str | None:
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(payload),
        key=lambda error: [str(part) for part in error.path],
    )
    if not errors:
        return None
    error = errors[0]
    path = '.'.join(str(part) for part in error.path) or '<root>'
    return f'{label} schema violation at {path}: {error.message}'


def require_string_list(value: Any, field: str, key: str) -> str | None:
    if not isinstance(value, list) or not value:
        return f'{key} {field} must be a non-empty list'
    if any(not isinstance(item, str) or not item for item in value):
        return f'{key} {field} must contain non-empty strings only'
    return None


def validate_source_metadata(source: dict[str, Any]) -> str | None:
    expected = {
        'registry_id': REGISTRY_ID,
        'wave': WAVE,
        'wave_name': WAVE_NAME,
        'runtime_posture': RUNTIME_POSTURE,
    }
    for field, expected_value in expected.items():
        if source.get(field) != expected_value:
            return f'source {field} must be {expected_value!r}'
    return None


def validate_item(item: dict[str, Any]) -> str | None:
    key = item.get(UNIQUE_KEY_FIELD)
    if not isinstance(key, str) or not key:
        return f'missing {UNIQUE_KEY_FIELD}'
    if item.get('wave') != WAVE:
        return f'{key} wave must be {WAVE}'
    if item.get('live_protocol') is not False:
        return f'{key} live_protocol must be false'
    if item.get('assistant_contestant_allowed') is not False:
        return f'{key} assistant_contestant_allowed must be false'
    if item.get('runtime_effect') not in ALLOWED_RUNTIME:
        return f'{key} invalid runtime_effect: {item.get("runtime_effect")}'
    if item.get('review_status') != 'candidate_only':
        return f'{key} review_status must be candidate_only'
    if item.get('authority_posture') != 'non_authority':
        return f'{key} authority_posture must be non_authority'
    if item.get('source_truth_posture') != 'owner_retained':
        return f'{key} source_truth_posture must be owner_retained'
    if item.get('canonical_status') != 'not_canon':
        return f'{key} canonical_status must be not_canon'
    if item.get('kag_status') != 'candidate_only':
        return f'{key} kag_status must be candidate_only'
    stop_err = require_string_list(item.get('stop_lines'), 'stop_lines', key)
    if stop_err:
        return stop_err
    stops = set(item['stop_lines'])
    for required in REQUIRED_STOP_LINES:
        if required not in stops:
            return f'{key} missing stop-line {required}'
    forbidden_err = require_string_list(item.get('forbidden_effects'), 'forbidden_effects', key)
    if forbidden_err:
        return forbidden_err
    forbidden = set(item['forbidden_effects'])
    for required in REQUIRED_FORBIDDEN:
        if required not in forbidden:
            return f'{key} missing forbidden effect {required}'
    return None


def validate() -> int:
    if not SRC.exists():
        return fail(f'missing source {SRC}')
    if not OUT.exists():
        return fail(f'missing generated registry {OUT}')
    for schema_path in (ENTRY_SCHEMA, REGISTRY_SCHEMA):
        if not schema_path.exists():
            return fail(f'missing schema {schema_path}')

    source = load_json(SRC)
    err = validate_source_metadata(source)
    if err:
        return fail(err)
    items = source.get(ITEM_KEY)
    if not isinstance(items, list):
        return fail(f'source {ITEM_KEY} must be a list')
    if len(items) != EXPECTED_COUNT:
        return fail(f'expected {EXPECTED_COUNT} source items, got {len(items)}')

    seen: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            return fail(f'source {ITEM_KEY} entries must be objects')
        err = schema_error(ENTRY_SCHEMA, item, f'source {UNIQUE_KEY_FIELD}')
        if err:
            return fail(err)
        err = validate_item(item)
        if err:
            return fail(err)
        key = item[UNIQUE_KEY_FIELD]
        if key in seen:
            return fail(f'duplicate {UNIQUE_KEY_FIELD} {key}')
        seen.add(key)

    registry = load_json(OUT)
    try:
        expected_registry = load_builder().build()
    except Exception as exc:  # builder errors should become validation failures, not tracebacks.
        return fail(f'cannot rebuild expected registry: {exc}')
    if registry != expected_registry:
        return fail('generated registry is stale or does not match builder output')
    err = schema_error(REGISTRY_SCHEMA, registry, 'generated registry')
    if err:
        return fail(err)
    if registry.get('count') != EXPECTED_COUNT:
        return fail(f'generated count must be {EXPECTED_COUNT}')
    if registry.get('count') != len(registry.get(ITEM_KEY, [])):
        return fail('generated count does not match generated item length')

    print(json.dumps({'ok': True, 'item_key': ITEM_KEY, 'count': EXPECTED_COUNT}, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(validate())
