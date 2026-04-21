#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import pathlib
import sys
from typing import Any

from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / 'config/agon_slc_eval_alignment.seed.json'
OUT = ROOT / 'generated/agon_slc_eval_alignment_registry.min.json'
ENTRY_SCHEMA = ROOT / 'schemas' / 'agon-slc-eval-alignment.schema.json'
REGISTRY_SCHEMA = ROOT / 'schemas' / 'agon-slc-eval-alignment-registry.schema.json'
BUILDER = ROOT / 'scripts' / 'build_agon_slc_eval_alignment_registry.py'
ITEM_KEY = 'eval_alignments'
EXPECTED_COUNT = 8
UNIQUE_KEY_FIELD = 'alignment_id'
REQUIRED_STOP_LINES = ['no_live_verdict_authority', 'no_durable_scar_write', 'no_retention_execution', 'no_rank_or_trust_mutation', 'no_tree_of_sophia_promotion', 'no_kag_promotion', 'no_hidden_scheduler_action', 'no_assistant_contestant_drift', 'no_auto_doctrine_rewrite', 'no_school_as_authority', 'no_lineage_as_canon', 'no_campaign_as_live_arena', 'no_center_takeover_of_owner_truth']
REQUIRED_FORBIDDEN = ['live_verdict_authority', 'durable_scar_write', 'retention_execution', 'rank_mutation', 'trust_mutation', 'tree_of_sophia_promotion', 'kag_promotion', 'hidden_scheduler_action', 'assistant_contestant_drift', 'auto_doctrine_rewrite', 'school_authority', 'lineage_canonization', 'live_campaign_arena']
ALLOWED_RUNTIME = ('none', 'candidate_only', 'local_dry_run_candidate_only', 'local_rehearsal_candidate_only')
ALLOWED_CANONICAL_STATUS = ('non_canonical_candidate', 'not_canon', 'not_applicable')


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def load_builder():
    spec = importlib.util.spec_from_file_location('_agon_wave16_builder', BUILDER)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError(f'cannot load builder {BUILDER}')
    spec.loader.exec_module(module)
    return module


def schema_error(schema_path: pathlib.Path, payload: Any, label: str) -> str | None:
    schema = load_json(schema_path)
    errors = sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda error: [str(part) for part in error.path])
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


def validate_item(item: dict[str, Any]) -> str | None:
    key = item.get(UNIQUE_KEY_FIELD)
    if not isinstance(key, str) or not key:
        return f'missing {UNIQUE_KEY_FIELD}'
    if item.get('wave') != 'XVI':
        return f'{key} wave must be XVI'
    if item.get('live_protocol') is not False:
        return f'{key} live_protocol must be false'
    if item.get('assistant_contestant_allowed') is not None and item.get('assistant_contestant_allowed') is not False:
        return f'{key} assistant_contestant_allowed must be false when present'
    if item.get('runtime_effect') not in ALLOWED_RUNTIME:
        return f'{key} invalid runtime_effect: {item.get("runtime_effect")}'
    if item.get('authority_posture') != 'non_authority':
        return f'{key} authority_posture must be non_authority'
    if item.get('canonical_status') not in ALLOWED_CANONICAL_STATUS:
        return f'{key} canonical_status must remain non-canonical'
    if item.get('review_status') != 'candidate_only':
        return f'{key} review_status must be candidate_only'

    stop_err = require_string_list(item.get('stop_lines'), 'stop_lines', key)
    if stop_err:
        return stop_err
    stop_lines = set(item['stop_lines'])
    for required in REQUIRED_STOP_LINES:
        if required not in stop_lines:
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
    if source.get('wave') != 'XVI':
        return fail('source wave must be XVI')
    if source.get('wave_name') != 'Schools / Lineages / Campaigns':
        return fail('source wave_name mismatch')
    if source.get('runtime_posture') != 'candidate_only':
        return fail('source runtime_posture must be candidate_only')
    items = source.get(ITEM_KEY)
    if not isinstance(items, list):
        return fail(f'source {ITEM_KEY} must be a list')
    if len(items) != EXPECTED_COUNT:
        return fail(f'expected {EXPECTED_COUNT} items in {ITEM_KEY}, got {len(items)}')

    seen: set[str] = set()
    for item in items:
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
    expected = load_builder().build()
    if registry != expected:
        return fail('generated registry is stale or does not match builder output')
    err = schema_error(REGISTRY_SCHEMA, registry, 'generated registry')
    if err:
        return fail(err)
    if registry.get('count') != len(registry.get(ITEM_KEY, [])):
        return fail('generated count does not match generated item length')
    if registry.get('count') != EXPECTED_COUNT:
        return fail(f'generated count must be {EXPECTED_COUNT}')

    print(json.dumps({'ok': True, 'item_key': ITEM_KEY, 'count': EXPECTED_COUNT}, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(validate())
