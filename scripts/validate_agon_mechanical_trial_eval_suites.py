#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / 'config/agon_mechanical_trial_eval_suites.seed.json'
OUT = ROOT / 'generated/agon_mechanical_trial_eval_suite_registry.min.json'
ITEM_KEY = 'eval_suites'
REQUIRED_FIELDS = ['id', 'trial_id', 'required_prechecks', 'allowed_outputs']
FORBIDDEN_TRUE_FIELDS = ['live_verdict_authority', 'durable_scar_write', 'rank_mutation', 'retention_execution', 'tos_promotion']
EXPECTED_COUNT = 7

def fail(msg):
    print(msg, file=sys.stderr)
    return 1

def digest_obj(obj):
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def expected_registry(data, items):
    return {
        'registry_id': data.get('registry_id', 'agon.mechanical_trial_eval_suite.registry.v0'),
        'wave': data.get('wave', 'XIII'),
        'runtime_posture': data.get('runtime_posture', 'candidate_only'),
        'count': len(items),
        ITEM_KEY: items,
        'digest': digest_obj(items),
    }

def validate_item(item):
    for field in REQUIRED_FIELDS:
        if field not in item:
            return f'missing required field {field} in {item}'
    if item.get('live_protocol') is not False:
        return f'live_protocol must be false for {item.get("id") or item.get("trial_id") or item.get("binding_id")}'
    if item.get('runtime_effect') not in (None, 'none', 'local_dry_run_candidate_only', 'candidate_only'):
        return f'invalid runtime_effect for {item.get("id") or item.get("trial_id") or item.get("binding_id")}'
    for field in FORBIDDEN_TRUE_FIELDS:
        if item.get(field) is True:
            return f'forbidden true field {field} in {item.get("id") or item.get("trial_id") or item.get("binding_id")}'
    return None

def main():
    if not SRC.exists():
        return fail(f'missing source {SRC}')
    data = json.loads(SRC.read_text(encoding='utf-8'))
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
    if reg != expected_registry(data, items):
        return fail('generated registry does not match source rebuild')
    print(json.dumps({'ok': True, 'item_key': ITEM_KEY, 'count': len(items)}, sort_keys=True))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
