#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'config/agon_eval_prebindings.seed.json'
GENERATED = ROOT / 'generated/agon_eval_prebinding_registry.min.json'
RECORD_KEY = 'prebindings'
BUILDER = ROOT / 'scripts' / 'build_agon_eval_prebinding_registry.py'
FORBIDDEN_TRUE_FLAGS = [
    'live_authority',
    'writes_durable_state',
    'mutates_rank',
    'promotes_to_tos',
    'opens_arena_session',
    'runs_hidden_scheduler',
]


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding='utf-8'))


def load_builder():
    spec = importlib.util.spec_from_file_location('wave7_builder', BUILDER)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def fail(msg: str) -> int:
    print(msg, file=sys.stderr)
    return 1


def main() -> int:
    if not CONFIG.exists():
        return fail(f'missing config: {CONFIG}')
    if not GENERATED.exists():
        return fail(f'missing generated: {GENERATED}')
    config = load(CONFIG)
    generated = load(GENERATED)
    if config.get('live_protocol') is not False:
        return fail('config must remain pre-protocol: live_protocol=false')
    if config.get('runtime_effect') != 'none':
        return fail('config must keep runtime_effect=none')
    records = config.get(RECORD_KEY)
    if not isinstance(records, list) or not records:
        return fail(f'config must contain non-empty {RECORD_KEY}')
    seen = set()
    for record in records:
        ref = record.get('prebinding_ref') or record.get('request_ref') or record.get('lane_ref')
        if not ref:
            return fail('record missing ref')
        if ref in seen:
            return fail(f'duplicate record ref: {ref}')
        seen.add(ref)
        if record.get('runtime_effect') != 'none':
            return fail(f'{ref} must keep runtime_effect=none')
        for flag in FORBIDDEN_TRUE_FLAGS:
            if record.get(flag) is True:
                return fail(f'{ref} forbidden true flag: {flag}')
        if record.get('live_protocol') is True:
            return fail(f'{ref} must not claim live_protocol')
    builder = load_builder()
    expected = builder.build(config)
    if expected != generated:
        return fail('generated surface does not match builder output')

    return 0

if __name__ == '__main__':
    raise SystemExit(main())
