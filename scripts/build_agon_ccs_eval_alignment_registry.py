#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'config' / 'agon_ccs_eval_alignment.seed.json'
OUT = ROOT / 'generated' / 'agon_ccs_eval_alignment_registry.min.json'


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def build(seed: dict) -> dict:
    return {
        'registry_id': seed['registry_id'],
        'version': seed['version'],
        'wave': seed['wave'],
        'home_repo': seed['home_repo'],
        'status': seed['status'],
        'live_protocol': False,
        'runtime_effect': 'none',
        'center_registry': seed['center_registry'],
        'alignment_count': len(seed['alignments']),
        'alignment_ids': [a['alignment_id'] for a in seed['alignments']],
        'law_families': sorted(set(a['law_family'] for a in seed['alignments'])),
        'eval_prebinding_ids': [a['eval_prebinding_id'] for a in seed['alignments']],
        'stop_lines': seed['stop_lines'],
        'alignments': seed['alignments'],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    expected = build(load_json(CONFIG))
    text = json.dumps(expected, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n'
    if args.check:
        if not OUT.exists():
            raise SystemExit(f'missing generated registry: {OUT}')
        if OUT.read_text(encoding='utf-8') != text:
            raise SystemExit('generated/agon_ccs_eval_alignment_registry.min.json is out of date')
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding='utf-8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
