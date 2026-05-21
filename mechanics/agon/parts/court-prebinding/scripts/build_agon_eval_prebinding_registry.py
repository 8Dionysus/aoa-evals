#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'config/agon_eval_prebindings.seed.json'
GENERATED = ROOT / 'generated/agon_eval_prebinding_registry.min.json'
RECORD_KEY = 'prebindings'
REGISTRY_SCHEMA = 'agon_eval_prebinding_registry_v1'


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding='utf-8'))


def build(config: dict) -> dict:
    records = config.get(RECORD_KEY, [])
    def ref(r):
        return r.get('prebinding_ref') or r.get('request_ref') or r.get('lane_ref')
    return {
        'schema_version': REGISTRY_SCHEMA,
        'source': str(CONFIG.relative_to(ROOT)),
        'wave': config.get('wave'),
        'owner_repo': config.get('owner_repo'),
        'status': config.get('status'),
        'live_protocol': config.get('live_protocol'),
        'runtime_effect': config.get('runtime_effect'),
        'record_key': RECORD_KEY,
        'record_count': len(records),
        'record_refs': sorted(ref(r) for r in records),
        'records': sorted(records, key=ref),
        'required_stop_lines': config.get('required_stop_lines', []),
        'notes': config.get('notes', ''),
    }


def dump_min(obj: dict) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n'


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    config = load(CONFIG)
    generated = build(config)
    rendered = dump_min(generated)
    if args.check:
        if not GENERATED.exists():
            print(f'missing generated surface: {GENERATED}', file=sys.stderr)
            return 1
        current = GENERATED.read_text(encoding='utf-8')
        if current != rendered:
            print(f'generated surface drift: {GENERATED}', file=sys.stderr)
            return 1
        return 0
    GENERATED.parent.mkdir(parents=True, exist_ok=True)
    GENERATED.write_text(rendered, encoding='utf-8')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
