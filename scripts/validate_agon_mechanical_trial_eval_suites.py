#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, pathlib, sys
from jsonschema import Draft202012Validator
ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / 'config/agon_mechanical_trial_eval_suites.seed.json'
OUT = ROOT / 'generated/agon_mechanical_trial_eval_suite_registry.min.json'
ITEM_SCHEMA = ROOT / 'schemas/agon_mechanical_trial_eval_suites.schema.json'
REGISTRY_SCHEMA = ROOT / 'schemas/agon_mechanical_trial_eval_suites-registry.schema.json'
ITEM_KEY = 'eval_suites'
REGISTRY_ID = 'agon.mechanical_trial_eval_suite.registry.v0'
WAVE = 'XIII'
RUNTIME_POSTURE = 'candidate_only'
REQUIRED_FIELDS = ['id', 'trial_id', 'required_prechecks', 'allowed_outputs', 'live_protocol', 'runtime_effect', 'live_verdict_authority', 'durable_scar_write', 'rank_mutation', 'retention_execution', 'tos_promotion']
FORBIDDEN_TRUE_FIELDS = ['live_verdict_authority', 'durable_scar_write', 'rank_mutation', 'retention_execution', 'tos_promotion']
EXPECTED_COUNT = 7

def fail(msg):
    print(msg, file=sys.stderr)
    return 1

def digest_obj(obj):
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def load_schema(path):
    return json.loads(path.read_text(encoding='utf-8'))

def load_registry_schema():
    schema = load_schema(REGISTRY_SCHEMA)
    schema = json.loads(json.dumps(schema))
    schema['properties'][ITEM_KEY]['items'] = load_schema(ITEM_SCHEMA)
    return schema

def schema_error(schema, payload):
    errors = sorted(
        Draft202012Validator(schema).iter_errors(payload),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    if not errors:
        return None
    error = errors[0]
    path = '.'.join(str(part) for part in error.absolute_path)
    if path:
        return f'schema violation at {path}: {error.message}'
    return f'schema violation: {error.message}'

def expected_registry(data, items):
    return {
        'registry_id': REGISTRY_ID,
        'wave': WAVE,
        'runtime_posture': RUNTIME_POSTURE,
        'count': len(items),
        ITEM_KEY: items,
        'digest': digest_obj(items),
    }

def validate_item(item):
    item_schema = load_schema(ITEM_SCHEMA)
    item_schema_error = schema_error(item_schema, item)
    if item_schema_error:
        return item_schema_error
    for field in REQUIRED_FIELDS:
        if field not in item:
            return f'missing required field {field} in {item}'
    if item.get('live_protocol') is not False:
        return f'live_protocol must be false for {item.get("id") or item.get("trial_id") or item.get("binding_id")}'
    if item.get('runtime_effect') not in ('none', 'local_dry_run_candidate_only', 'candidate_only'):
        return f'invalid runtime_effect for {item.get("id") or item.get("trial_id") or item.get("binding_id")}'
    for field in FORBIDDEN_TRUE_FIELDS:
        if item.get(field) is not False:
            return f'{field} must be false in {item.get("id") or item.get("trial_id") or item.get("binding_id")}'
    return None

def main():
    if not SRC.exists():
        return fail(f'missing source {SRC}')
    data = json.loads(SRC.read_text(encoding='utf-8'))
    if data.get('registry_id') != REGISTRY_ID:
        return fail(f'source registry_id must be {REGISTRY_ID}')
    if data.get('wave') != WAVE:
        return fail(f'source wave must be {WAVE}')
    if data.get('runtime_posture') != RUNTIME_POSTURE:
        return fail(f'source runtime_posture must be {RUNTIME_POSTURE}')
    items = data.get(ITEM_KEY, [])
    if len(items) != EXPECTED_COUNT:
        return fail(f'expected {EXPECTED_COUNT} items in {ITEM_KEY}, got {len(items)}')
    seen = set()
    for item in items:
        key = item.get('id') or item.get('trial_id') or item.get('binding_id') or item.get('suite_id') or item.get('run_id')
        if not key:
            return fail(f'missing item key in {item}')
        if key in seen:
            return fail(f'duplicate item key {key}')
        seen.add(key)
        err = validate_item(item)
        if err:
            return fail(err)
    if not OUT.exists():
        return fail(f'missing generated registry {OUT}')
    reg = json.loads(OUT.read_text(encoding='utf-8'))
    registry_schema = load_registry_schema()
    registry_schema_error = schema_error(registry_schema, reg)
    if registry_schema_error:
        return fail(registry_schema_error)
    if reg != expected_registry(data, items):
        return fail('generated registry does not match source rebuild')
    print(json.dumps({'ok': True, 'item_key': ITEM_KEY, 'count': len(items)}, sort_keys=True))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
